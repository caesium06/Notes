#!/usr/bin/env python3
"""
Download images referenced in a Markdown file and rewrite links to local paths.

Handles:
  1. ![Title](https://direct/image/url.jpg)   -> downloaded directly
  2. ![Title](IMG_QUERY: search terms)        -> searched across several open image sources
  3. [Title](https://.../file.jpg)            -> plain links ending in an image extension

Sources for IMG_QUERY placeholders (tried in the order given by --sources):
  openverse  Openverse: CC-licensed photos (Flickr, Wikimedia Commons content, museums, ...).
             Anonymous limit is about 20 requests/minute and 200/day.
  met        Metropolitan Museum of Art Open Access (public-domain objects only)
  cleveland  Cleveland Museum of Art Open Access (CC0 works only)
  artic      Art Institute of Chicago (public-domain works only). OFF by default: its image
             server returns 403 to scripts and its search matches loosely.
  wikimedia  Wikimedia Commons directly. OFF by default; add it with --sources.

Rate-limit handling (HTTP 429):
  - Requests are spaced per host (Openverse 3.2s, Art Institute 1.1s, Wikimedia --delay).
  - 429/5xx are retried with exponential backoff, honouring Retry-After.
  - If a host keeps returning 429, or asks for a very long wait (for example, a daily quota
    is used up), that host is skipped for the rest of the run instead of stalling the script.
  - Already-downloaded images are cached on disk, so rerunning only retries failures.

Usage:
  python download_images.py notes.md
  python download_images.py notes.md --strip-failed
  python download_images.py notes.md --sources openverse,met,wikimedia
"""
import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlencode, urlparse

BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
BOT_UA = "SSCNotesImageDownloader/2.0 (personal study notes; python-urllib)"
API_HOSTS = {
    "api.openverse.org",
    "collectionapi.metmuseum.org",
    "openaccess-api.clevelandart.org",
    "api.artic.edu",
}

CONTENT_TYPE_EXT = {
    "image/jpeg": ".jpg", "image/png": ".png", "image/gif": ".gif",
    "image/webp": ".webp", "image/svg+xml": ".svg", "image/bmp": ".bmp",
    "image/tiff": ".tif",
}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".tif", ".tiff"}
COMMONS_OK_MIME = {"image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml"}

# Thumbnail widths Wikimedia serves without special treatment.
STANDARD_WIDTHS = [20, 40, 60, 120, 250, 330, 500, 960, 1280, 1920, 3840]

MAX_CANDIDATES_PER_QUERY = 3
MAX_BACKOFF = 120
WIKI_MAX_BACKOFF = 30
WIKI_RETRIES = 2
MAX_BYTES = 15_000_000   # larger files are skipped (the next URL for the same image is tried)
MIN_BYTES = 4_000        # smaller files are almost always error placeholders
DEFAULT_INTERVAL = 0.3
MIN_INTERVAL = {"openverse.org": 3.2, "artic.edu": 1.1}

# Runtime settings, overwritten from CLI args in main.
SETTINGS = {"delay": 1.5, "retries": 5}
DISABLED = set()      # host groups skipped for the rest of this run
_last_request = {}

LINK_PATTERN = re.compile(
    r"(?P<bang>!?)\[(?P<alt>[^\]]*)\]\(\s*"
    r"(?:IMG_QUERY\s*:\s*(?P<query>[^)\r\n]+)"
    r"|(?P<url>https?://(?:[^()\s]+|\([^()\s]*\))+))"
    r"\s*\)",
    re.I,
)
FENCE_PATTERN = re.compile(
    r"^(?P<fence>```|~~~)(?P<lang>[^\r\n]*)\r?\n(?P<body>.*?)^(?P=fence)[ \t]*\r?$\r?\n?",
    re.S | re.M,
)
WRAPPER_LANGS = {"markdown", "md", ""}


# --------------------------------------------------------------------------- HTTP

class RateLimited(Exception):
    def __init__(self, group, wait=None):
        text = f"rate limited by {group}"
        if wait:
            text += f" (Retry-After {wait:.0f}s)"
        super().__init__(text)
        self.group = group
        self.wait = wait


def note_disabled(error: RateLimited):
    if error.group not in DISABLED:
        DISABLED.add(error.group)
        print(f"  ! {error}; skipping {error.group} for the rest of this run")


def host_group(url: str) -> str:
    """Hosts that share a rate limit map to one group, e.g. api.artic.edu and www.artic.edu."""
    host = (urlparse(url).hostname or "").lower()
    if host.endswith(("wikimedia.org", "wikipedia.org")):
        return "wikimedia"
    parts = host.split(".")
    if len(parts) >= 3 and len(parts[-1]) == 2 and parts[-2] in {"co", "com", "org", "net", "ac", "gov", "edu"}:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


def headers_for(url: str) -> dict:
    host = (urlparse(url).hostname or "").lower()
    if host_group(url) == "wikimedia" or host in API_HOSTS:
        headers = {"User-Agent": BOT_UA, "Accept": "*/*"}
        if host == "api.artic.edu":
            headers["AIC-User-Agent"] = BOT_UA  # courtesy header requested by the API docs
        return headers
    return {"User-Agent": BROWSER_UA, "Accept": "*/*"}


def throttle(group: str):
    interval = SETTINGS["delay"] if group == "wikimedia" else MIN_INTERVAL.get(group, DEFAULT_INTERVAL)
    wait = _last_request.get(group, 0.0) + interval - time.monotonic()
    if wait > 0:
        time.sleep(wait)
    _last_request[group] = time.monotonic()


def retry_after_seconds(error):
    if isinstance(error, urllib.error.HTTPError):
        value = error.headers.get("Retry-After")
        if value:
            try:
                return float(value)
            except ValueError:
                return None  # HTTP-date form; fall back to exponential backoff
    return None


def http_get(url: str, timeout: int = 45):
    group = host_group(url)
    if group in DISABLED:
        raise RateLimited(group)

    is_wiki = group == "wikimedia"
    retries = WIKI_RETRIES if is_wiki else SETTINGS["retries"]
    cap = WIKI_MAX_BACKOFF if is_wiki else MAX_BACKOFF
    last_error = None

    for attempt in range(retries):
        throttle(group)
        try:
            req = urllib.request.Request(url, headers=headers_for(url))
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read(MAX_BYTES + 1)
                if len(body) > MAX_BYTES:
                    raise ValueError(f"file larger than {MAX_BYTES // 1_000_000} MB")
                return body, resp.headers.get_content_type()
        except urllib.error.HTTPError as e:
            last_error = e
            if e.code == 429:
                wait = retry_after_seconds(e)
                if wait is not None and wait > cap:
                    raise RateLimited(group, wait)          # e.g. daily quota used up
                if attempt < retries - 1:
                    delay = min(wait if wait is not None else 5 * (2 ** attempt), cap)
                    print(f"  HTTP 429 from {group}, retrying in {delay:.0f}s "
                          f"(attempt {attempt + 2}/{retries})")
                    time.sleep(delay)
                    continue
                raise RateLimited(group, wait)
            if e.code in (500, 502, 503, 504) and attempt < retries - 1:
                delay = min(5 * (2 ** attempt), cap)
                print(f"  HTTP {e.code} from {group}, retrying in {delay:.0f}s")
                time.sleep(delay)
                continue
            raise
        except (urllib.error.URLError, TimeoutError) as e:
            last_error = e
            if attempt < retries - 1:
                delay = min(5 * (2 ** attempt), cap)
                print(f"  Network error ({e}), retrying in {delay:.0f}s")
                time.sleep(delay)
                continue
            raise
    raise last_error


def extract_real_image_url(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.hostname or ""
    if "google." in host:
        params = parse_qs(parsed.query)
        for key in ("imgurl", "url", "q"):
            if key in params:
                candidate = unquote(params[key][0])
                if candidate.startswith(("http://", "https://")):
                    return candidate
    return url


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text or "").strip()


def snap_width(width: int) -> int:
    """Largest standard Wikimedia thumbnail width not exceeding the request."""
    sizes = [w for w in STANDARD_WIDTHS if w <= width]
    return sizes[-1] if sizes else STANDARD_WIDTHS[0]


def fmt_license(lic: str, version: str = "") -> str:
    if not lic:
        return "See source"
    upper = lic.upper()
    base = upper if upper in ("CC0", "PDM") else f"CC {upper}"
    return f"{base} {version}".strip()


# --------------------------------------------------------------------- search providers
# Every provider returns a list of candidates:
#   {"urls": [try-first, fallback...], "source": page URL, "license": str,
#    "author": str, "title": str, "provider": str}

def search_openverse(query: str, width: int):
    params = urlencode({"q": query, "page_size": 8, "mature": "false"})
    data, _ = http_get(f"https://api.openverse.org/v1/images/?{params}", timeout=30)
    out = []
    for r in json.loads(data).get("results") or []:
        original, thumb = r.get("url"), r.get("thumbnail")
        if original and host_group(original) != "wikimedia":
            urls = [original, thumb]          # full size first, Openverse proxy as fallback
        else:
            urls = [thumb, original]          # avoid hitting upload.wikimedia.org directly
        urls = [u for u in urls if u]
        if not urls:
            continue
        out.append({
            "urls": urls,
            "source": r.get("foreign_landing_url") or "",
            "license": fmt_license(r.get("license") or "", r.get("license_version") or ""),
            "author": r.get("creator") or "",
            "title": r.get("title") or "",
            "provider": f"Openverse/{r.get('source') or r.get('provider') or 'unknown'}",
        })
    return out


def search_met(query: str, width: int):
    base = "https://collectionapi.metmuseum.org/public/collection"
    params = urlencode({"q": query, "hasImages": "true"})
    try:
        # /v1/search was scheduled for retirement on 1 Oct 2026; /v1.1/search replaces it.
        data, _ = http_get(f"{base}/v1.1/search?{params}", timeout=30)
    except urllib.error.HTTPError as e:
        if e.code not in (404, 410):
            raise
        data, _ = http_get(f"{base}/v1/search?{params}", timeout=30)

    ids = (json.loads(data).get("objectIDs") or [])[:6]
    out = []
    for oid in ids:
        if len(out) >= MAX_CANDIDATES_PER_QUERY:
            break
        try:
            raw, _ = http_get(f"{base}/v1/objects/{oid}", timeout=30)
            obj = json.loads(raw)
        except RateLimited:
            raise
        except Exception:
            continue
        if not obj.get("isPublicDomain"):
            continue
        urls = [u for u in (obj.get("primaryImage"), obj.get("primaryImageSmall")) if u]
        if not urls:
            continue
        out.append({
            "urls": urls,
            "source": obj.get("objectURL") or "",
            "license": "Public domain (Met Open Access, CC0)",
            "author": obj.get("artistDisplayName") or obj.get("culture") or "",
            "title": obj.get("title") or "",
            "provider": "Met Museum",
        })
    return out


def search_cleveland(query: str, width: int):
    params = urlencode({"q": query, "has_image": 1, "limit": 10})
    data, _ = http_get(f"https://openaccess-api.clevelandart.org/api/artworks/?{params}", timeout=30)
    out = []
    for art in json.loads(data).get("data") or []:
        # Only CC0 works come with freely usable images.
        if (art.get("share_license_status") or "").upper() != "CC0":
            continue
        images = art.get("images") or {}
        urls = [(images.get(k) or {}).get("url") for k in ("web", "print")]
        urls = [u for u in urls if u]
        if not urls:
            continue
        creators = art.get("creators") or []
        out.append({
            "urls": urls,
            "source": art.get("url") or "",
            "license": "CC0",
            "author": (creators[0].get("description") if creators else "") or "",
            "title": art.get("title") or "",
            "provider": "Cleveland Museum of Art",
        })
    return out


def search_artic(query: str, width: int):
    params = urlencode({
        "q": query,
        "fields": "id,title,image_id,is_public_domain,artist_display",
        "limit": 10,
    })
    data, _ = http_get(f"https://api.artic.edu/api/v1/artworks/search?{params}", timeout=30)
    payload = json.loads(data)
    iiif = ((payload.get("config") or {}).get("iiif_url") or "https://www.artic.edu/iiif/2").rstrip("/")
    out = []
    for art in payload.get("data") or []:
        if not art.get("is_public_domain") or not art.get("image_id"):
            continue
        out.append({
            "urls": [f"{iiif}/{art['image_id']}/full/843,/0/default.jpg"],  # size recommended by AIC
            "source": f"https://www.artic.edu/artworks/{art.get('id')}",
            "license": "Public domain (CC0)",
            "author": (art.get("artist_display") or "").split("\n")[0],
            "title": art.get("title") or "",
            "provider": "Art Institute of Chicago",
        })
    return out


def search_commons(query: str, width: int):
    api = (
        "https://commons.wikimedia.org/w/api.php?action=query&format=json"
        "&generator=search&gsrnamespace=6&gsrlimit=10"
        f"&gsrsearch={quote(query)}"
        "&prop=imageinfo&iiprop=url|mime|extmetadata"
        f"&iiurlwidth={width}"
    )
    data, _ = http_get(api, timeout=30)
    pages = json.loads(data).get("query", {}).get("pages", {})
    out = []
    for page in sorted(pages.values(), key=lambda p: p.get("index", 999)):
        info = (page.get("imageinfo") or [None])[0]
        if not info or info.get("mime") not in COMMONS_OK_MIME:
            continue
        meta = info.get("extmetadata", {})
        urls = [info.get("thumburl") or info["url"], info["url"]]
        out.append({
            "urls": list(dict.fromkeys(urls)),
            "source": info.get("descriptionurl", ""),
            "license": strip_html(meta.get("LicenseShortName", {}).get("value", "")),
            "author": strip_html(meta.get("Artist", {}).get("value", "")),
            "title": page.get("title", ""),
            "provider": "Wikimedia Commons",
        })
    return out


# name -> (rate-limit group, search function)
PROVIDERS = {
    "openverse": ("openverse.org", search_openverse),
    "met": ("metmuseum.org", search_met),
    "cleveland": ("clevelandart.org", search_cleveland),
    "artic": ("artic.edu", search_artic),
    "wikimedia": ("wikimedia", search_commons),
}
DEFAULT_SOURCES = "openverse,met,cleveland"   # artic is opt-in: its image server returns 403 to scripts


# ------------------------------------------------------------------------ downloading

def download_image(url: str, alt: str, folder: Path):
    target_url = extract_real_image_url(url)
    digest = hashlib.sha256(target_url.encode()).hexdigest()[:10]

    existing = list(folder.glob(f"*_{digest}.*"))
    if existing:
        print(f"Cached: {existing[0].name}")
        return f"images/{existing[0].name}"

    if host_group(target_url) in DISABLED:
        return None

    try:
        data, content_type = http_get(target_url)
        ext = CONTENT_TYPE_EXT.get(content_type)
        if ext is None:
            url_ext = Path(urlparse(target_url).path).suffix.lower()
            if content_type in ("application/octet-stream", "binary/octet-stream") and url_ext in IMAGE_EXTS:
                ext = ".jpg" if url_ext == ".jpeg" else url_ext
            else:
                print(f"Skipped (not an image: {content_type}): {alt}")
                return None
        if len(data) < MIN_BYTES and ext != ".svg":
            print(f"Skipped (only {len(data)} bytes, probably a placeholder): {alt}")
            return None

        clean = re.sub(r"[^\w-]", "_", alt.lower())[:50].strip("_") or "image"
        filename = f"{clean}_{digest}{ext}"
        (folder / filename).write_bytes(data)
        print(f"Downloaded: {filename}")
        return f"images/{filename}"
    except RateLimited as error:
        note_disabled(error)
        return None
    except Exception as error:
        print(f"Failed: {alt}\n  Reason: {error}")
        return None


def resolve_and_download(query: str, alt: str, folder: Path, width: int, sources):
    """
    Most specific query first, searched across every enabled source, then progressively
    shorter queries. For each hit the candidate URLs are tried in order, then the next hit.
    Returns (local_path, candidate) or (None, None).
    """
    words = query.split()
    attempts = [query]
    if len(words) > 4:
        attempts.append(" ".join(words[:4]))
    if len(words) > 2:
        attempts.append(" ".join(words[:2]))

    tried = set()
    for q in attempts:
        for name in sources:
            group, search = PROVIDERS[name]
            if group in DISABLED:
                continue
            try:
                candidates = search(q, width)
            except RateLimited as error:
                note_disabled(error)
                continue
            except Exception as error:
                print(f"  {name}: search error for '{q}': {error}")
                continue

            for cand in candidates[:MAX_CANDIDATES_PER_QUERY]:
                key = cand["urls"][0]
                if key in tried:
                    continue
                tried.add(key)
                for url in cand["urls"]:
                    local = download_image(url, alt, folder)
                    if local:
                        print(f"  Source: {cand['provider']} | {cand['title'][:70]}")
                        return local, cand
                print(f"  {name}: could not download '{cand['title'][:50]}', trying next result")
    return None, None


# ----------------------------------------------------------------------------- main

def process_markdown(file_path: str, strip_failed: bool, width: int, sources):
    md_file = Path(file_path).resolve()
    if not md_file.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    image_folder = md_file.parent / "images"
    image_folder.mkdir(exist_ok=True)

    # utf-8-sig strips a BOM if the editor added one
    content = md_file.read_text(encoding="utf-8-sig")
    backup = md_file.with_name(md_file.name + ".bak")
    if not backup.exists():
        backup.write_text(content, encoding="utf-8")

    print(f"Sources: {', '.join(sources)}")

    cache = {}
    credits = []
    failed_items = []
    stats = {"found": 0, "success": 0, "failed": 0, "queries": 0}

    def replace(match):
        bang = match.group("bang")
        alt = match.group("alt").strip()
        query = match.group("query")
        url = match.group("url")

        if not bang and url:
            if Path(urlparse(url).path).suffix.lower() not in IMAGE_EXTS:
                return match.group(0)

        stats["found"] += 1

        if query:
            query = query.strip()
            key = f"q:{query}"
            if key not in cache:
                stats["queries"] += 1
                print(f"Resolving: {query}")
                local, info = resolve_and_download(query, alt or query, image_folder, width, sources)
                if local:
                    credits.append((local, alt or query, info))
                else:
                    print(f"  No downloadable result for: {query}")
                cache[key] = local
            local = cache[key]
            label = query
        else:
            key = f"u:{url}"
            if key not in cache:
                cache[key] = download_image(url, alt, image_folder)
            local = cache[key]
            label = url

        if local:
            stats["success"] += 1
            return f"![{alt}]({local})"

        stats["failed"] += 1
        failed_items.append(f"{alt or label}  <-  {label}")
        return "" if strip_failed else match.group(0)

    # Real code fences are left alone. Fences labelled markdown/md (or unlabelled)
    # are treated as wrappers: fence lines removed, inside processed.
    out, pos = [], 0
    for m in FENCE_PATTERN.finditer(content):
        out.append(LINK_PATTERN.sub(replace, content[pos:m.start()]))
        lang = m.group("lang").strip().lower()
        if lang in WRAPPER_LANGS:
            out.append(LINK_PATTERN.sub(replace, m.group("body")))
        else:
            out.append(m.group(0))
        pos = m.end()
    out.append(LINK_PATTERN.sub(replace, content[pos:]))
    updated = "".join(out)

    md_file.write_text(updated, encoding="utf-8")

    if credits:
        credits_file = image_folder / "CREDITS.md"
        # Merge with credits from earlier runs so reruns do not wipe them.
        existing_lines = []
        if credits_file.exists():
            existing_lines = [
                ln for ln in credits_file.read_text(encoding="utf-8").splitlines()
                if ln.startswith("- ")
            ]
        new_lines = [
            f"- **{alt}** (`{local}`): {info['title'] or 'Untitled'} | "
            f"{info['author'] or 'Unknown author'} | {info['license'] or 'See source'} | "
            f"{info['provider']} | {info['source']}"
            for local, alt, info in credits
        ]
        seen, merged = set(), []
        for ln in existing_lines + new_lines:
            marker = re.search(r"\(`([^`]+)`\)", ln)
            key = marker.group(1) if marker else ln
            if key in seen:
                continue
            seen.add(key)
            merged.append(ln)
        credits_file.write_text("# Image Credits\n\n" + "\n".join(merged) + "\n", encoding="utf-8")

    print("\n" + "=" * 45)
    print("IMAGE DOWNLOAD SUMMARY")
    print("=" * 45)
    print(f"Image links found : {stats['found']}")
    print(f"Placeholders      : {stats['queries']}")
    print(f"Successfully saved: {stats['success']}")
    print(f"Failed            : {stats['failed']}{' (removed)' if strip_failed else ' (left unchanged; rerun to retry)'}")
    for item in failed_items:
        print(f"  - {item}")
    if DISABLED:
        print(f"Rate-limited      : {', '.join(sorted(DISABLED))} (skipped this run; try again later)")
    print(f"Image directory   : {image_folder}")
    print(f"Backup file       : {backup}")
    if credits:
        print(f"Credits file      : {image_folder / 'CREDITS.md'} (check titles match your topic)")
    print("=" * 45)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Download Markdown images and localize links.")
    ap.add_argument("file", help="Markdown file to process")
    ap.add_argument("--strip-failed", action="store_true",
                    help="Remove image lines that could not be downloaded")
    ap.add_argument("--sources", default=DEFAULT_SOURCES,
                    help="Comma-separated sources in order of preference. Available: "
                         + ", ".join(PROVIDERS) + f" (default: {DEFAULT_SOURCES})")
    ap.add_argument("--width", type=int, default=1280,
                    help="Wikimedia thumbnail width, snapped to a standard size (default 1280)")
    ap.add_argument("--delay", type=float, default=1.5,
                    help="Minimum seconds between Wikimedia requests (default 1.5)")
    ap.add_argument("--retries", type=int, default=5,
                    help="Attempts per request on 429/5xx/network errors (default 5)")
    args = ap.parse_args()

    chosen = [s.strip().lower() for s in args.sources.split(",") if s.strip()]
    unknown = [s for s in chosen if s not in PROVIDERS]
    if unknown or not chosen:
        ap.error(f"unknown --sources {unknown or ''}; choose from: {', '.join(PROVIDERS)}")

    SETTINGS["delay"] = max(args.delay, 0.0)
    SETTINGS["retries"] = max(args.retries, 1)
    process_markdown(args.file, args.strip_failed, snap_width(args.width), chosen)