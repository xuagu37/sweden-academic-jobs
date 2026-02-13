import argparse
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
    This ensures stable paths regardless of how the module is executed.
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
CONTENT_DIR = REPO_ROOT / "content"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scrape Swedish academic job postings and build markdown pages."
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available university slugs and exit.",
    )
    parser.add_argument(
        "--only",
        type=str,
        default=None,
        help="Run only one university by slug (e.g., lund, kth).",
    )

    args = parser.parse_args()

    if args.list:
        print("Available universities:\n")
        for u in UNIVERSITIES:
            print(f"{u['slug']}\t{u['name']}")
        return 0

    selected = UNIVERSITIES
    if args.only:
        selected = [u for u in UNIVERSITIES if u["slug"] == args.only]
        if not selected:
            print(f"Unknown slug: {args.only}")
            print("Use --list to see valid slugs.")
            return 2

    # Ensure directories exist
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    for uni in selected:
        slug = uni["slug"]
        name = uni["name"]
        url = uni["url"]
        fetcher = uni["fetcher"]
        job_parser = uni["parser"]

        html_file = HTML_DIR / f"latest_{slug}_page.html"
        raw_md = RAW_DIR / f"{slug}.md"
        processed_md = CONTENT_DIR / f"{slug}.md"

        print(f"\nScraping jobs for {name}...")
        fetcher(url, save_to=str(html_file))

        jobs = job_parser(str(html_file))
        job_count = len(jobs)
        print(f"Found {job_count} jobs for {name}")

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

    print("\nUniversities processed successfully!")

    # Merge all raw markdown files
    merged_md = RAW_DIR / "all_current_jobs.md"
    merge_job_markdowns(str(RAW_DIR), str(merged_md))

    convert_md_headings_to_html(
        str(merged_md),
        str(CONTENT_DIR / "all_current_jobs.md"),
    )
    add_search_and_filter(Path(CONTENT_DIR / "all_current_jobs.md"))
    add_position_count(str(CONTENT_DIR / "all_current_jobs.md"))

    print("\nAll universities merged successfully!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
