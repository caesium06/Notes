#!/usr/bin/env python3
"""
Download images referenced in a Markdown file and rewrite links to local paths.

Handles:
  1. ![Title](https://direct/image/url.jpg)   -> downloaded directly
  2. ![Title](IMG_QUERY: search terms)        -> resolved via Wikimedia Commons, then downloaded
  3. [Title](https://.../file.jpg)            -> plain links ending in an image extension

Usage:
  python download_images.py notes.md
  python download_images.py notes.md --strip-failed
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
from urllib.parse import parse_qs, quote, unquote, urlparse

BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
WIKI_UA = "SSCNotesImageDownloader/1.0 (personal study notes; python-urllib)"

CONTENT_TYPE_EXT = {
    "image/jpeg": ".jpg", "image/png": ".png", "image/gif": ".gif",
    "image/webp": ".webp", "image/svg+xml": ".svg", "image/bmp": ".bmp",
    "image/tiff": ".tif",
}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".tif", ".tiff"}
COMMONS_OK_MIME = {"image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml"}

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


def headers_for(url: str) -> dict:
    host = (urlparse(url).hostname or "").lower()
    ua = WIKI_UA if host.endswith(("wikimedia.org", "wikipedia.org")) else BROWSER_UA
    return {"User-Agent": ua, "Accept": "*/*"}


def http_get(url: str, timeout: int = 45, retries: int = 3):
    last_error = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers_for(url))
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read(), resp.headers.get_content_type()
        except urllib.error.HTTPError as e:
            last_error = e
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
                continue
            raise
        except (urllib.error.URLError, TimeoutError) as e:
            last_error = e
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
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


def commons_search(query: str, width: int, delay: float):
    api = (
        "https://commons.wikimedia.org/w/api.php?action=query&format=json"
        "&generator=search&gsrnamespace=6&gsrlimit=10"
        f"&gsrsearch={quote(query)}"
        "&prop=imageinfo&iiprop=url|mime|extmetadata"
        f"&iiurlwidth={width}"
    )
    time.sleep(delay)
    data, _ = http_get(api, timeout=30)
    pages = json.loads(data).get("query", {}).get("pages", {})
    for page in sorted(pages.values(), key=lambda p: p.get("index", 999)):
        info = (page.get("imageinfo") or [None])[0]
        if not info or info.get("mime") not in COMMONS_OK_MIME:
            continue
        meta = info.get("extmetadata", {})
        return {
            "url": info.get("thumburl") or info["url"],
            "source": info.get("descriptionurl", ""),
            "license": strip_html(meta.get("LicenseShortName", {}).get("value", "")),
            "author": strip_html(meta.get("Artist", {}).get("value", "")),
            "title": page.get("title", ""),
        }
    return None


def resolve_query(query: str, width: int, delay: float):
    words = query.split()
    attempts = [query]
    if len(words) > 4:
        attempts.append(" ".join(words[:4]))
    if len(words) > 2:
        attempts.append(" ".join(words[:2]))
    for q in attempts:
        try:
            result = commons_search(q, width, delay)
        except Exception as error:
            print(f"  Search error for '{q}': {error}")
            continue
        if result:
            return result
    return None


def download_image(url: str, alt: str, folder: Path):
    target_url = extract_real_image_url(url)
    digest = hashlib.sha256(target_url.encode()).hexdigest()[:10]

    existing = list(folder.glob(f"*_{digest}.*"))
    if existing:
        print(f"Cached: {existing[0].name}")
        return f"images/{existing[0].name}"

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

        clean = re.sub(r"[^\w-]", "_", alt.lower())[:50].strip("_") or "image"
        filename = f"{clean}_{digest}{ext}"
        (folder / filename).write_bytes(data)
        print(f"Downloaded: {filename}")
        return f"images/{filename}"
    except Exception as error:
        print(f"Failed: {alt}\n  Reason: {error}")
        return None


def process_markdown(file_path: str, strip_failed: bool, width: int, delay: float):
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

    cache = {}
    credits = []
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
                found = resolve_query(query, width, delay)
                if found:
                    local = download_image(found["url"], alt or query, image_folder)
                    if local:
                        credits.append((local, alt or query, found))
                    cache[key] = local
                else:
                    print(f"  No Commons result for: {query}")
                    cache[key] = None
            local = cache[key]
        else:
            key = f"u:{url}"
            if key not in cache:
                cache[key] = download_image(url, alt, image_folder)
            local = cache[key]

        if local:
            stats["success"] += 1
            return f"![{alt}]({local})"

        stats["failed"] += 1
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
        lines = ["# Image Credits\n"]
        for local, alt, info in credits:
            lines.append(
                f"- **{alt}** (`{local}`): {info['title']} | "
                f"{info['author'] or 'Unknown author'} | {info['license'] or 'See source'} | {info['source']}"
            )
        (image_folder / "CREDITS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\n" + "=" * 45)
    print("IMAGE DOWNLOAD SUMMARY")
    print("=" * 45)
    print(f"Image links found : {stats['found']}")
    print(f"Placeholders      : {stats['queries']}")
    print(f"Successfully saved: {stats['success']}")
    print(f"Failed            : {stats['failed']}{' (removed)' if strip_failed else ' (left unchanged; rerun to retry)'}")
    print(f"Image directory   : {image_folder}")
    print(f"Backup file       : {backup}")
    if credits:
        print(f"Credits file      : {image_folder / 'CREDITS.md'}")
    print("=" * 45)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Download Markdown images and localize links.")
    ap.add_argument("file", help="Markdown file to process")
    ap.add_argument("--strip-failed", action="store_true")
    ap.add_argument("--width", type=int, default=1200)
    ap.add_argument("--delay", type=float, default=0.5)
    args = ap.parse_args()
    process_markdown(args.file, args.strip_failed, args.width, args.delay)