from pathlib import Path

from .config import UNIVERSITIES
from .process import (
    convert_md_headings_to_html,
    add_search_and_filter,
    update_index_date,
    add_position_count,
    merge_job_markdowns,
)


def find_repo_root(start: Path) -> Path:
    """
    Find the repository root by walking upward until we see the 'swedjobs' package directory.
    This makes running the module stable regardless of current working directory.
    """
    p = start
    for _ in range(10):
        if (p / "swedjobs").is_dir():
            return p
        p = p.parent
    return start  # fallback


REPO_ROOT = find_repo_root(Path(__file__).resolve().parent)

DATA_DIR = REPO_ROOT / "data"
HTML_DIR = DATA_DIR / "cache"
RAW_DIR = DATA_DIR / "raw"

# Keep this as your Sphinx source dir for now (you can rename to docs/ later)
CONTENT_DIR = REPO_ROOT / "content"


def main() -> int:
    # Ensure directories exist
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    for uni in UNIVERSITIES:
        slug = uni["slug"]
        name = uni["name"]
        url = uni["url"]
        fetcher = uni["fetcher"]
        parser = uni["parser"]

        html_file = HTML_DIR / f"latest_{slug}_page.html"
        raw_md = RAW_DIR / f"{slug}.md"
        processed_md = CONTENT_DIR / f"{slug}.md"

        print(f"\nScraping jobs for {name}...")
        fetcher(url, save_to=str(html_file))

        jobs = parser(str(html_file))

        raw_md.parent.mkdir(parents=True, exist_ok=True)
        with open(raw_md, "w", encoding="utf-8") as f:
            f.write(f"# {name}\n\n")
            for job in jobs:
                f.write(f"### {job['title']}\n")
                f.write(f"- **Link:** [View job posting]({job['url']})\n")
                f.write(f"- **Department:** {job['department']}\n")
                f.write(f"- **Published:** {job['published']}\n")
                f.write(f"- **Deadline:** {job['deadline']}\n\n")

        print(f"Processing jobs for {name}...")
        convert_md_headings_to_html(str(raw_md), str(processed_md))
        add_search_and_filter(Path(processed_md))
        add_position_count(str(processed_md))

    # Update index date if index exists
    index_md = CONTENT_DIR / "index.md"
    if index_md.exists():
        update_index_date(path=str(index_md))
    else:
        print(f"Skipping index date update: {index_md} not found")

    print("\nAll universities processed successfully!")

    # Merge all raw markdowns into one file
    merged_md = RAW_DIR / "current_positions.md"
    merge_job_markdowns(str(RAW_DIR), str(merged_md))

    convert_md_headings_to_html(str(merged_md), str(CONTENT_DIR / "current_positions.md"))
    add_search_and_filter(Path(CONTENT_DIR / "current_positions.md"))
    add_position_count(str(CONTENT_DIR / "current_positions.md"))

    print("\nAll universities merged successfully!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())




