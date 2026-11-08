#!/usr/bin/env python3
"""
Convert a Markdown (.md) file to an A4 PDF with a two-column page layout.

Install:
    py -m pip install markdown playwright
    py -m playwright install chromium

Usage:
    py md_to_pdf.py "Seating Arrangement.md"
    py md_to_pdf.py "Seating Arrangement.md" -o "Seating Arrangement.pdf"
    py md_to_pdf.py notes.md --css custom.css
"""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
from html import escape

import markdown
from playwright.async_api import async_playwright


DEFAULT_CSS = r"""
@page {
    size: A4 portrait;
    margin: 9mm;
}

* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 8.2pt;
    line-height: 1.22;
    color: #202020;
}

/* Two balanced reading columns on each A4 page */
body {
    column-count: 2;
    column-gap: 9mm;
    column-rule: 0.5pt solid #c8c8c8;
    column-fill: balance;
}

/* Let the document title use the full page width */
h1 {
    column-span: all;
    font-size: 15pt;
    line-height: 1.15;
    margin: 0 0 8pt;
    padding: 0 0 5pt;
    border-bottom: 1pt solid #777;
    break-after: avoid;
}

h2, h3 {
    font-size: 10pt;
    line-height: 1.15;
    margin: 7pt 0 3pt;
    break-after: avoid;
}

p {
    margin: 2pt 0 4pt;
    orphans: 2;
    widows: 2;
}

ul, ol {
    margin: 2pt 0 5pt;
    padding-left: 14pt;
}

li {
    margin: 0 0 2pt;
}

table {
    width: 100%;
    border-collapse: collapse;
    table-layout: auto;
    font-size: 7.2pt;
    line-height: 1.15;
    margin: 3pt 0 6pt;
    break-inside: avoid;
}

th, td {
    border: 0.5pt solid #b8b8b8;
    padding: 2.5pt 3pt;
    text-align: left;
    vertical-align: top;
    overflow-wrap: anywhere;
}

th {
    background: #eeeeee;
    font-weight: bold;
}

tr {
    break-inside: avoid;
}

blockquote, pre, img {
    break-inside: avoid;
}

code {
    font-family: Consolas, "Courier New", monospace;
    font-size: 0.92em;
}

hr {
    border: 0;
    border-top: 0.5pt solid #ccc;
    margin: 5pt 0;
}

/* Keep links readable in printed notes */
a {
    color: inherit;
    text-decoration: none;
}
"""


def convert_markdown(md_path: Path, pdf_path: Path, extra_css: str = "") -> None:
    source = md_path.read_text(encoding="utf-8-sig")

    html_body = markdown.markdown(
        source,
        extensions=[
            "tables",
            "fenced_code",
            "sane_lists",
            "smarty",
        ],
        output_format="html5",
    )

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(md_path.stem)}</title>
<style>
{DEFAULT_CSS}
{extra_css}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

    async def render() -> None:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.set_content(document, wait_until="networkidle")
            await page.pdf(
                path=str(pdf_path),
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
                display_header_footer=False,
            )
            await browser.close()

    asyncio.run(render())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert Markdown to an A4 PDF with a two-column layout."
    )
    parser.add_argument("input", type=Path, help="Input Markdown file")
    parser.add_argument(
        "-o", "--output", type=Path,
        help="Output PDF path (default: same name as input)"
    )
    parser.add_argument(
        "--css", type=Path,
        help="Optional CSS file to override or extend the built-in styling"
    )
    args = parser.parse_args()

    md_path = args.input.expanduser().resolve()
    if not md_path.is_file():
        raise SystemExit(f"Input file not found: {md_path}")
    if md_path.suffix.lower() not in {".md", ".markdown"}:
        raise SystemExit("Input must be a .md or .markdown file.")

    pdf_path = (
        args.output.expanduser().resolve()
        if args.output
        else md_path.with_suffix(".pdf")
    )

    extra_css = ""
    if args.css:
        css_path = args.css.expanduser().resolve()
        if not css_path.is_file():
            raise SystemExit(f"CSS file not found: {css_path}")
        extra_css = css_path.read_text(encoding="utf-8-sig")

    convert_markdown(md_path, pdf_path, extra_css)
    print(f"PDF created: {pdf_path}")


if __name__ == "__main__":
    main()
