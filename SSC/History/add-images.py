#!/usr/bin/env python3
"""
Fill IMG_QUERY placeholders in a Markdown file with images YOU choose.

For every placeholder like
    ![Great Bath at Mohenjo-daro](IMG_QUERY: Great Bath Mohenjo-daro site)
the script shows the title and search terms, opens a Google Images search for them,
and asks you to paste a link. It downloads the image into an images/ folder next to the
note and rewrites the line to  ![Great Bath at Mohenjo-daro](images/<file>).

Links you can paste:
  - a direct image URL (.jpg/.png/.webp/...)
  - a Google Images "imgres" link (the image URL is extracted from it)
  - a normal web page (Wikimedia Commons File: page, Wikipedia, Britannica, ...):
    the page's main image (og:image) is used
  - a local file path (e.g. a screenshot you saved)

At the prompt:  Enter = skip for now,  s = reopen the search,  q = save and quit.
Progress is written to the note after every image, so quitting loses nothing.
Skipped placeholders stay in the note; run the script again to finish them.

Usage:
  python add_images.py "SSC/History/8-gupta empire.md"
  python add_images.py notes.md --no-open        # don't open the browser
  python add_images.py notes.md --engine wikimedia   # open Wikimedia Commons search instead

Standard library only; no installs needed.
"""
import argparse
import hashlib
import re
import shutil
import sys
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path
from urllib.parse import parse_qs, quote_plus, unquote, urljoin, urlparse

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
MAX_BYTES = 25_000_000

PLACEHOLDER = re.compile(
    r"!\[(?P<alt>[^\]]*)\]\(\s*IMG_QUERY\s*:\s*(?P<query>[^)\r\n]+?)\s*\)", re.I
)
FENCE = re.compile(
    r"^(?P<fence>```|~~~)(?P<lang>[^\r\n]*)\r?\n(?P<body>.*?)^(?P=fence)[ \t]*\r?$",
    re.S | re.M,
)
MARKDOWN_LANGS = {"", "markdown", "md"}  # fences of these kinds are notes, not code

ENGINES = {
    "google": "https://www.google.com/search?tbm=isch&q={q}",
    "bing": "https://www.bing.com/images/search?q={q}",
    "wikimedia": "https://commons.wikimedia.org/w/index.php?search={q}&ns6=1&title=Special:MediaSearch&type=image",
}


# ----------------------------------------------------------------- markdown handling

def segments(content: str):
    """Split into (text, is_code) pieces so real code blocks are never touched."""
    pos = 0
    for m in FENCE.finditer(content):
        if m.start() > pos:
            yield content[pos:m.start()], False
        is_code = m.group("lang").strip().lower() not in MARKDOWN_LANGS
        yield m.group(0), is_code
        pos = m.end()
    if pos < len(content):
        yield content[pos:], False


def find_placeholders(content: str):
    """Unique (query, alt) pairs in order of first appearance."""
    seen, out = set(), []
    for text, is_code in segments(content):
        if is_code:
            continue
        for m in PLACEHOLDER.finditer(text):
            query = m.group("query").strip()
            if query not in seen:
                seen.add(query)
                out.append((query, m.group("alt").strip()))
    return out


def apply_mapping(content: str, mapping: dict) -> str:
    def sub(m):
        local = mapping.get(m.group("query").strip())
        return f"![{m.group('alt').strip()}]({local})" if local else m.group(0)

    return "".join(
        text if is_code else PLACEHOLDER.sub(sub, text) for text, is_code in segments(content)
    )


# ---------------------------------------------------------------------- downloading

def sniff_ext(data: bytes):
    """Identify the image type from its first bytes (content-types can lie)."""
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return ".gif"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    if data[:2] == b"BM":
        return ".bmp"
    head = data[:2048].lstrip().lower()
    if head.startswith(b"<svg") or (head.startswith(b"<?xml") and b"<svg" in data[:4096].lower()):
        return ".svg"
    return None


def fetch(url: str):
    origin = f"{urlparse(url).scheme}://{urlparse(url).netloc}/"
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "image/*,text/html;q=0.8,*/*;q=0.5", "Referer": origin}
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        data = resp.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError(f"file is larger than {MAX_BYTES // 1_000_000} MB")
    return data


def unwrap_search_link(url: str) -> str:
    """Google/Bing result links hide the real image URL in a query parameter."""
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    params = parse_qs(parsed.query)
    if "google." in host:
        for key in ("imgurl", "url"):
            if key in params:
                return unquote(params[key][0])
    if "bing.com" in host and "mediaurl" in params:
        return unquote(params["mediaurl"][0])
    return url


def page_image_url(html: bytes, base_url: str):
    text = html.decode("utf-8", errors="ignore")
    for tag in re.findall(r"<meta\b[^>]*>", text, flags=re.I):
        if re.search(r'(?:property|name)\s*=\s*["\'](?:og:image|twitter:image)["\']', tag, re.I):
            m = re.search(r'content\s*=\s*["\']([^"\']+)["\']', tag, re.I)
            if m:
                return urljoin(base_url, m.group(1).replace("&amp;", "&"))
    return None


def get_image(source: str):
    """Return (bytes, ext, final_url) for a link or local path, or raise."""
    local = Path(source.strip('"\'')).expanduser()
    if not source.lower().startswith(("http://", "https://")) and local.is_file():
        data = local.read_bytes()
        ext = sniff_ext(data)
        if not ext:
            raise ValueError("that file is not an image")
        return data, ext, str(local)

    url = unwrap_search_link(source)
    if not url.lower().startswith(("http://", "https://")):
        raise ValueError("not a web link or an existing file path")

    data = fetch(url)
    ext = sniff_ext(data)
    if ext:
        return data, ext, url

    # Probably a web page: use its main image.
    image_url = page_image_url(data, url)
    if not image_url:
        raise ValueError("that link is a page with no main image; open the image itself and copy its address")
    data = fetch(image_url)
    ext = sniff_ext(data)
    if not ext:
        raise ValueError("the page's main image could not be read")
    return data, ext, image_url


def save_image(data: bytes, ext: str, alt: str, key: str, folder: Path) -> str:
    digest = hashlib.sha256(key.encode()).hexdigest()[:10]
    slug = re.sub(r"[^\w-]", "_", alt.lower())[:50].strip("_") or "image"
    name = f"{slug}_{digest}{ext}"
    (folder / name).write_bytes(data)
    return f"images/{name}"


# ----------------------------------------------------------------------------- main

def ask(prompt: str) -> str:
    try:
        return input(prompt).strip()
    except EOFError:
        return "q"


def open_search(engine: str, query: str, enabled: bool):
    url = ENGINES[engine].format(q=quote_plus(query))
    print(f"  Search: {url}")
    if enabled:
        webbrowser.open(url)


def run(note: Path, engine: str, open_browser: bool):
    if not note.is_file():
        sys.exit(f"File not found: {note}")

    content = note.read_text(encoding="utf-8-sig")
    todo = find_placeholders(content)
    if not todo:
        print("No IMG_QUERY placeholders found. Nothing to do.")
        return


    folder = note.parent / "images"
    folder.mkdir(exist_ok=True)

    print(f"{len(todo)} placeholder(s) in {note.name}")
    print("Paste an image link or file path. Enter = skip, s = search again, q = quit.\n")

    mapping, done, skipped = {}, 0, 0
    for index, (query, alt) in enumerate(todo, 1):
        print(f"[{index}/{len(todo)}] {alt or query}")
        print(f"  Looking for: {query}")
        open_search(engine, query, open_browser)

        while True:
            answer = ask("  Link > ")
            if answer.lower() == "q":
                print("\nQuitting. Progress is saved.")
                return finish(done, skipped, len(todo) - index + 1)
            if answer.lower() == "s":
                open_search(engine, query, True)
                continue
            if not answer:
                skipped += 1
                print("  Skipped.\n")
                break
            try:
                data, ext, final_url = get_image(answer)
            except (urllib.error.URLError, TimeoutError, ValueError, OSError) as error:
                print(f"  Could not use that link: {error}\n  Try another link, or press Enter to skip.")
                continue
            local = save_image(data, ext, alt or query, final_url, folder)
            mapping[query] = local
            content = apply_mapping(content, {query: local})
            note.write_text(content, encoding="utf-8")  # save after every image
            done += 1
            print(f"  Saved {local} ({len(data) // 1024} KB)\n")
            break

    finish(done, skipped, 0)


def finish(done: int, skipped: int, remaining: int):
    print("=" * 40)
    print(f"Saved py  : {done}")
    print(f"Skipped : {skipped} (still placeholders)")
    if remaining:
        print(f"Not asked yet: {remaining}")
    print("Run the script again to finish the rest.")
    print("=" * 40)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Fill IMG_QUERY placeholders with links you provide.")
    ap.add_argument("file", help="Markdown file to process")
    ap.add_argument("--engine", choices=sorted(ENGINES), default="google",
                    help="Search site to open for each placeholder (default: google)")
    ap.add_argument("--no-open", action="store_true", help="Print the search link but do not open a browser")
    args = ap.parse_args()
    run(Path(args.file).resolve(), args.engine, not args.no_open)