#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert a Markdown job list to Xiaohongshu-style images (auto-split into multiple pages).

Expected MD format (English, e.g. linkoping.md):

# Linköping University (or any title)

### Job title 1
- **Link:** https://...
- **Deadline:** YYYY-MM-DD

### Job title 2
- **Deadline:** YYYY-MM-DD
- **Link:** https://...

Notes:
- Renders ONLY: Position title + Deadline (links are ignored and never drawn)
- Adds a column header row: "Position | Deadline"
- Deadline column prints ONLY the date (YYYY-MM-DD)
- Job titles can wrap
- Auto-splits by max image height (--max-height)

Usage (mac example):
  python md_to_xhs_image.py linkoping.md -o output.png --font "/System/Library/Fonts/Hiragino Sans GB.ttc"

Output:
  output_01.png, output_02.png, ...
"""

import argparse
import os
import re
from datetime import datetime
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont

# More robust date matching:
# - 2026-02-15
# - 15 Feb 2026 / 15 February 2026 (optional comma)
# - 15/02/2026 or 15.02.2026 or 15-02-2026
# - 2026/02/15 or 2026.2.5 or 2026-2-5
DATE_RE = re.compile(
    r"("
    r"\d{4}-\d{1,2}-\d{1,2}"
    r"|"
    r"\d{1,2}\s+[A-Za-z]{3,9},?\s+\d{4}"
    r"|"
    r"\d{1,2}[./-]\d{1,2}[./-]\d{4}"
    r"|"
    r"\d{4}[./-]\d{1,2}[./-]\d{1,2}"
    r"|"
    r"\d{1,2}\.[A-Za-z]{3,9}\.\d{4}"   # <-- add this
    r")",
    re.IGNORECASE,
)



def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def normalize_university_name(name: str) -> str:
    mapping = {
        "chalmers university of technology": "Chalmers",
        "swedish university of agricultural sciences": "SLU",
        "linköping university": "Linköping University",
        "lund university": "Lund University",
        "uppsala university": "Uppsala University",
        "kth royal institute of technology": "KTH",
        "karolinska institutet": "Karolinska Institutet",
    }

    low = name.lower().strip()
    for full, short in mapping.items():
        if full in low:
            return short
    return name  # fallback


def normalize_date(date_str: str) -> str:
    """
    Convert supported date formats to YYYY-MM-DD (best effort).
    If cannot parse, returns original string.
    """
    s = date_str.strip()
    s = s.replace(",", "")  # "15 Feb, 2026" -> "15 Feb 2026"

    # handle "15.Feb.2026" / "01.Mar.2026" -> "15 Feb 2026" / "01 Mar 2026"
    s = re.sub(r"^(\d{1,2})\.([A-Za-z]{3,9})\.(\d{4})$", r"\1 \2 \3", s)

    # Try common formats first
    for fmt in (
        "%Y-%m-%d",
        "%d %b %Y",
        "%d %B %Y",
        "%d/%m/%Y",
        "%d.%m.%Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%Y.%m.%d",
        "%Y-%m-%d",
    ):
        try:
            dt = datetime.strptime(s, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass

    # Handle numeric dates with single-digit month/day: 2026-2-5 or 2026/2/5 or 2026.2.5
    s2 = re.sub(r"[./]", "-", s)
    try:
        if re.fullmatch(r"\d{4}-\d{1,2}-\d{1,2}", s2):
            y, m, d = s2.split("-")
            dt = datetime(int(y), int(m), int(d))
            return dt.strftime("%Y-%m-%d")
    except Exception:
        pass

    # Handle dd-m-yyyy where d/m may be 1 digit
    try:
        if re.fullmatch(r"\d{1,2}-\d{1,2}-\d{4}", s2):
            d, m, y = s2.split("-")
            dt = datetime(int(y), int(m), int(d))
            return dt.strftime("%Y-%m-%d")
    except Exception:
        pass

    return s



def parse_md(md: str):
    """
    Parse Markdown and keep ONLY PhD/Doctoral jobs.

    Expected format:

    # Title

    ### Job title
    - **Link:** ...
    - **Deadline:** <various formats>
    """

    title = None
    items = []
    current_job = None

    phd_kw = (
        "phd",
        "ph.d",
        "doctoral",
        "doctorate",
        "doctorate student",
        "doctoral student",
    )

    exclude_kw = (
        "postdoc",
        "post-doc",
        "postdoctoral",
        "post doctoral",
    )

    for raw in md.splitlines():
        line = raw.strip()

        # Document title
        if line.startswith("# "):
            raw_title = line[2:].strip()
            title = normalize_university_name(raw_title)
            continue

        # Job title (accept ### and ##)
        if line.startswith("### "):
            current_job = line[4:].strip()
            continue
        if line.startswith("## "):
            current_job = line[3:].strip()
            continue

        # Deadline line: just look for a date anywhere in the line,
        # and then normalize it.
        m = DATE_RE.search(line)
        if m and current_job:
            date_raw = m.group(1)
            date_norm = normalize_date(date_raw)

            job_low = current_job.lower()
            if any(k in job_low for k in phd_kw) and not any(e in job_low for e in exclude_kw):
                items.append((current_job, date_norm))
            continue

    if not title:
        title = "PhD Positions"

    return title, items


def sort_items(items):
    def key(x):
        try:
            return datetime.strptime(x[1], "%Y-%m-%d")
        except Exception:
            return datetime.max  # unparsed dates go last

    return sorted(items, key=key)


def wrap_text(draw, text, font, max_width):
    """
    Word-aware wrapping for English.
    Falls back to character wrapping if a single word is too long.
    """
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = word if not current_line else current_line + " " + word

        if draw.textlength(test_line, font=font) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)

            # If single word is longer than max_width → fallback to char wrap
            if draw.textlength(word, font=font) > max_width:
                broken = ""
                for ch in word:
                    test = broken + ch
                    if draw.textlength(test, font=font) <= max_width:
                        broken = test
                    else:
                        lines.append(broken)
                        broken = ch
                current_line = broken
            else:
                current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def load_font(font_path: str, size: int):
    if not os.path.exists(font_path):
        raise FileNotFoundError(
            f"Font not found: {font_path}\n"
            f"Tip: pass --font with an absolute path (mac example: "
            f'--font "/System/Library/Fonts/Hiragino Sans GB.ttc")'
        )
    return ImageFont.truetype(font_path, size)


def compute_row_layout(
    items: List[Tuple[str, str]],
    font_path: str,
    width: int,
    pad: int,
    font_job_size: int,
    font_deadline_size: int,
    col_gap: int,
    left_ratio: float,
    row_top_pad: int,
    row_bottom_pad: int,
    bg=(255, 255, 255),
):
    """Precompute wrapped lines + row heights with a dummy draw object."""
    content_w = width - pad * 2
    left_w = int(content_w * left_ratio)
    dl_x = pad + left_w + col_gap

    tmp = Image.new("RGB", (width, 10), bg)
    d = ImageDraw.Draw(tmp)

    font_job = load_font(font_path, font_job_size)
    font_deadline = load_font(font_path, font_deadline_size)

    rows = []
    for job, deadline in items:
        job_lines = wrap_text(d, job, font_job, left_w)
        job_h = len(job_lines) * (font_job.size + 10)

        dl_text = deadline
        dl_h = font_deadline.size + 6

        row_h = max(job_h, dl_h) + row_top_pad + row_bottom_pad
        rows.append(
            {
                "job": job,
                "deadline": deadline,
                "job_lines": job_lines,
                "dl_text": dl_text,
                "row_h": row_h,
            }
        )

    return {
        "left_w": left_w,
        "dl_x": dl_x,
        "rows": rows,
    }


def split_into_pages(
    rows: List[dict],
    header_h: int,
    header_row_height: int,
    footer_h: int,
    max_height: int,
):
    """Greedy split: add rows until next row would exceed max_height."""
    pages = []
    current = []
    current_h = header_h + header_row_height + footer_h

    for r in rows:
        if current and (current_h + r["row_h"]) > max_height:
            pages.append(current)
            current = []
            current_h = header_h + header_row_height + footer_h

        current.append(r)
        current_h += r["row_h"]

    if current:
        pages.append(current)

    return pages


def render_one_page(
    header: str,
    page_index: int,
    page_total: int,
    page_rows: List[dict],
    out_path: str,
    font_path: str,
    width: int = 1080,
    pad: int = 72,
    header_h: int = 170,
    header_row_height: int = 70,
    footer_h: int = 90,
    left_w: int = 700,
    dl_x: int = 800,
    bg=(255, 255, 255),
    header_bg=(16, 82, 160),
    text_color=(20, 20, 20),
    accent=(16, 82, 160),
    divider=(230, 235, 240),
    font_header_size: int = 30,
    font_job_size: int = 30,
    font_deadline_size: int = 24,
    font_colhead_size: int = 30,
    font_small_size: int = 24,
):
    # Fonts
    font_header = load_font(font_path, font_header_size)
    font_job = load_font(font_path, font_job_size)
    font_deadline = load_font(font_path, font_deadline_size)
    font_colhead = load_font(font_path, font_colhead_size)
    font_small = load_font(font_path, font_small_size)

    # Page height
    rows_h = sum(r["row_h"] for r in page_rows)
    height = header_h + header_row_height + rows_h + footer_h

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([0, 0, width, header_h], fill=header_bg)

    # Header with page info
    header_with_page = f"{header} ({page_index}/{page_total})" if page_total > 1 else header
    header_lines = wrap_text(draw, header_with_page, font_header, width - pad * 2)

    y_text = (header_h - (len(header_lines) * (font_header.size + 8))) // 2
    for line in header_lines:
        draw.text((pad, y_text), line, font=font_header, fill=(255, 255, 255))
        y_text += font_header.size + 8

    # Start below header
    y = header_h

    # Column header row
    draw.line([pad, y, width - pad, y], fill=divider, width=2)
    y += 18
    draw.text((pad + 20, y), "Position", font=font_colhead, fill=accent)
    draw.text((dl_x, y), "Deadline", font=font_colhead, fill=accent)
    y += header_row_height - 18
    draw.line([pad, y, width - pad, y], fill=divider, width=2)

    # Rows
    row_top_pad = 18
    bullet_r = 7

    for r in page_rows:
        # bullet
        x0 = pad
        cy = y + row_top_pad + (font_job.size // 2)
        draw.ellipse([x0, cy - bullet_r, x0 + bullet_r * 2, cy + bullet_r], fill=accent)

        # job title
        text_x = x0 + bullet_r * 2 + 16
        text_y = y + row_top_pad
        for line in r["job_lines"]:
            draw.text((text_x, text_y), line, font=font_job, fill=text_color)
            text_y += font_job.size + 10

        # deadline
        dl_y = y + row_top_pad
        draw.text((dl_x, dl_y), r["dl_text"], font=font_deadline, fill=accent)

        y += r["row_h"]
        draw.line([pad, y, width - pad, y], fill=divider, width=2)

    # Footer
    today = datetime.today().strftime("%Y-%m-%d")
    footer_text = f"Updated on: {today}"
    ft_lines = wrap_text(draw, footer_text, font_small, width - pad * 2)
    fy = y + 20
    for line in ft_lines:
        draw.text((pad, fy), line, font=font_small, fill=(120, 120, 120))
        fy += font_small.size + 6

    img.save(out_path)
    return out_path


def output_paths(base_output: str, n_pages: int):
    base, ext = os.path.splitext(base_output)
    if not ext:
        ext = ".png"
    if n_pages == 1:
        return [base + ext]
    return [f"{base}_{i:02d}{ext}" for i in range(1, n_pages + 1)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md_file", help="Input markdown file (e.g. linkoping.md)")
    ap.add_argument("-o", "--output", default="xhs_jobs.png", help="Base output image path (PNG recommended)")
    ap.add_argument(
        "--font",
        default="SimHei.ttf",
        help='Path to a TTF/TTC font. mac example: "/System/Library/Fonts/Hiragino Sans GB.ttc"',
    )
    ap.add_argument("--width", type=int, default=1080, help="Image width, default 1080 (XHS friendly)")
    ap.add_argument("--max-height", type=int, default=1400, help="Max height per image (default 1400)")
    ap.add_argument("--left-ratio", type=float, default=0.82, help="Job title column width ratio (default 0.82)")
    ap.add_argument("--job-font", type=int, default=30, help="Job title font size (default 30)")
    ap.add_argument("--deadline-font", type=int, default=24, help="Deadline font size (default 24)")
    ap.add_argument("--colhead-font", type=int, default=30, help="Column header font size (default 30)")
    ap.add_argument("--header-font", type=int, default=56, help="Header font size (default 56)")
    ap.add_argument("--footer-font", type=int, default=24, help="Footer font size (default 24)")
    args = ap.parse_args()

    md = read_text(args.md_file)
    header, items = parse_md(md)
    if not items:
        print(f"⚠ No items found in {args.md_file}. Skipping.")
        return

    items = sort_items(items)

    # constants (keep consistent with rendering)
    pad = 72
    header_h = 170
    header_row_height = 70
    footer_h = 90
    col_gap = 60
    row_top_pad = 18
    row_bottom_pad = 18

    layout = compute_row_layout(
        items=items,
        font_path=args.font,
        width=args.width,
        pad=pad,
        font_job_size=args.job_font,
        font_deadline_size=args.deadline_font,
        col_gap=col_gap,
        left_ratio=args.left_ratio,
        row_top_pad=row_top_pad,
        row_bottom_pad=row_bottom_pad,
    )

    pages = split_into_pages(
        rows=layout["rows"],
        header_h=header_h,
        header_row_height=header_row_height,
        footer_h=footer_h,
        max_height=args.max_height,
    )

    outs = output_paths(args.output, len(pages))
    for i, (page_rows, out_path) in enumerate(zip(pages, outs), start=1):
        render_one_page(
            header=header,
            page_index=i,
            page_total=len(pages),
            page_rows=page_rows,
            out_path=out_path,
            font_path=args.font,
            width=args.width,
            pad=pad,
            header_h=header_h,
            header_row_height=header_row_height,
            footer_h=footer_h,
            left_w=layout["left_w"],
            dl_x=layout["dl_x"],
            font_header_size=args.header_font,
            font_job_size=args.job_font,
            font_deadline_size=args.deadline_font,
            font_colhead_size=args.colhead_font,
            font_small_size=args.footer_font,
        )
        print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
