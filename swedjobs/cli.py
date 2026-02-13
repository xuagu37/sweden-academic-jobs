from pathlib import Path

from swedjobs.fetcher import fetch_html, fetch_all_pages_ki
from swedjobs.parser import (
    parse_jobs_lund, parse_jobs_uppsala, parse_jobs_stockholm, parse_jobs_gothenburg,
    parse_jobs_ki, parse_jobs_kth, parse_jobs_linkoping, parse_jobs_umea,
    parse_jobs_orebro, parse_jobs_lulea, parse_jobs_malmo, parse_jobs_chalmers,
    parse_jobs_slu, parse_jobs_karlstad, parse_jobs_sodertorn, parse_jobs_dalarna,
    parse_jobs_gavle, parse_jobs_malardalen
)
from swedjobs.process import (
    convert_md_headings_to_html, add_search_and_filter,
    update_index_date, add_position_count, merge_job_markdowns
)

# -------------------------
# Centralized path config
# -------------------------
def find_repo_root(start: Path) -> Path:
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


def main():
    # Ensure directories exist (safe no-op if they already exist)
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    universities = [
        {
            "name": "Lund University",
            "url": "https://www.lunduniversity.lu.se/vacancies",
            "html_file": HTML_DIR / "latest_lund_page.html",
            "raw_md": RAW_DIR / "lund.md",
            "processed_md": CONTENT_DIR / "lund.md",
            "fetcher": fetch_html,
            "parser": parse_jobs_lund,
        },
        {
            "name": "Uppsala University",
            "url": "https://www.uu.se/en/about-uu/join-us/jobs-and-vacancies?start=200",
            "html_file": HTML_DIR / "latest_uppsala_page.html",
            "raw_md": RAW_DIR / "uppsala.md",
            "processed_md": CONTENT_DIR / "uppsala.md",
            "fetcher": fetch_html,
            "parser": parse_jobs_uppsala,
        },
        {
            "name": "Stockholm University",
            "url": "https://su.varbi.com/en/what:findjob/?showresult=1&categories=1&checklist=1&orglevel=1&ref=1&nologin=1&nocity=1&nocounty=1&nocountry=1&nolocalefield=1&nolocalegroup=1&hideColumns=town&norefsearch=1",
            "html_file": HTML_DIR / "latest_stockholm_page.html",
            "raw_md": RAW_DIR / "stockholm.md",
            "processed_md": CONTENT_DIR / "stockholm.md",
            "fetcher": fetch_html,
            "parser": parse_jobs_stockholm,
        },
        {
            "name": "Gothenburg University",
            "url": "https://www.gu.se/en/work-at-the-university-of-gothenburg/vacancies",
            "html_file": HTML_DIR / "latest_gothenburg_page.html",
            "raw_md": RAW_DIR / "gothenburg.md",
            "processed_md": CONTENT_DIR / "gothenburg.md",
            "fetcher": fetch_html,
            "parser": parse_jobs_gothenburg,
        },
        {
            "name": "Karolinska Institute",
            "url": "https://ki.se/en/vacancies?page=",
            "html_file": HTML_DIR / "latest_ki_page.html",
            "raw_md": RAW_DIR / "ki.md",
            "processed_md": CONTENT_DIR / "ki.md",
            "fetcher": fetch_all_pages_ki,
            "parser": parse_jobs_ki,
        },
        {
            "name": "KTH",
            "url": "https://www.kth.se/lediga-jobb?l=en",
            "html_file": HTML_DIR / "latest_kth_page.html",
            "raw_md": RAW_DIR / "kth.md",
            "processed_md": CONTENT_DIR / "kth.md",
            "fetcher": fetch_html,
            "parser": parse_jobs_kth,
        },
        {
            "name": "Linköping University",
            "url": "https://liu.se/en/work-at-liu/vacancies",
            "html_file": HTML_DIR / "latest_linkoping_page.html",
            "raw_md": RAW_DIR / "linkoping.md",
            "processed_md": CONTENT_DIR / "linkoping.md",
            "fetcher": fetch_html,
            "parser": parse_jobs_linkoping,
        },
        {
            "name": "Umeå University",
            "url": "https://www.umu.se/en/work-with-us/open-positions/",
            "html_file": HTML_DIR / "latest_umea_page.html",
            "raw_md": RAW_DIR / "umea.md",
            "processed_md": CONTENT_DIR / "umea.md",
            "fetcher": fetch_html,
            "parser": parse_jobs_umea,
        },
        {
            "name": "Örebro University",
            "url": "https://www.oru.se/english/career/available-positions",
            "html_file": HTML_DIR / "latest_orebro_page.html",
            "raw_md": RAW_DIR / "orebro.md",
            "processed_md": CONTENT_DIR / "orebro.md",
            "fetcher": fetch_html,
            "parser": parse_jobs_orebro,
        },
        {
            "name": "Luleå University",
            "url": "https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies",
            "html_file": HTML_DIR / "latest_lulea_page.html",
            "raw_md": RAW_DIR / "lulea.md",
            "processed_md": CONTENT_DIR / "lulea.md",
            "fetcher": fetch_html,
            "parser": parse_jobs_lulea,
        },
        {
            "name": "Malmö University",
            "url": "https://mau.se/en/about-us/job-offers/current-vacancies/",
            "html_file": HTML_DIR / "latest_malmo_page.html",
            "raw_md": RAW_DIR / "malmo.md",
            "processed_md": CONTENT_DIR / "malmo.md",
            "fetcher": fetch_html,
            "parser": parse_jobs_malmo,
        },
        {
            "name": "Chalmers University of Technology",
            "url": "https://web103.reachmee.com/ext/I003/304/main?site=5&validator=a72aeedd63ec10de71e46f8d91d0d57c&lang=UK&ref=https%3A%2F%2F",
            "html_file": HTML_DIR / "latest_chalmers_page.html",
            "raw_md": RAW_DIR / "chalmers.md",
            "processed_md": CONTENT_DIR / "chalmers.md",
            "fetcher": fetch_html,
            "parser": parse_jobs_chalmers,
        },
        {
            "name": "Swedish University of Agricultural Sciences",
            "url": "https://web103.reachmee.com/ext/I017/1114/main?site=7&validator=87e4b706891e51f731ed44be28da8352&lang=UK&ref=https%3a%2f%2fwww.overleaf.com%2f",
            "html_file": HTML_DIR / "latest_slu_page.html",
            "raw_md": RAW_DIR / "slu.md",
            "processed_md": CONTENT_DIR / "slu.md",
            "fetcher": fetch_html,
            "parser": parse_jobs_slu,
        },
        {
            "name": "Karlstad University",
            "url": "https://kau.varbi.com/en/what:iframe/login:1/buttons:1/subscribe:1/template:default",
            "html_file": HTML_DIR / "latest_karlstad_page.html",
            "raw_md": RAW_DIR / "karlstad.md",
            "processed_md": CONTENT_DIR / "karlstad.md",
            "fetcher": fetch_html,
            "parser": parse_jobs_karlstad,
        },
        {
            "name": "Södertörn University",
            "url": "https://web103.reachmee.com/ext/I007/532/main?site=24&validator=2f5f4343b7f80edb4b210427ef968f34&lang=UK&ref=https%3a%2f%2fwww.overleaf.com%2f",
            "html_file": HTML_DIR / "latest_sodertorn_page.html",
            "raw_md": RAW_DIR / "sodertorn.md",
            "processed_md": CONTENT_DIR / "sodertorn.md",
            "fetcher": fetch_html,
            "parser": parse_jobs_sodertorn,
        },
        {
            "name": "Dalarna University",
            "url": "https://www.du.se/en/about-du/career-opportunities/vacant-positions/",
            "html_file": HTML_DIR / "latest_dalarna_page.html",
            "raw_md": RAW_DIR / "dalarna.md",
            "processed_md": CONTENT_DIR / "dalarna.md",
            "fetcher": fetch_html,
            "parser": parse_jobs_dalarna,
        },
        {
            "name": "Gävle University",
            "url": "https://www.hig.se/engelska/university-of-gavle/about-the-university/work-with-us#Currentvacancies",
            "html_file": HTML_DIR / "latest_gavle_page.html",
            "raw_md": RAW_DIR / "gavle.md",
            "processed_md": CONTENT_DIR / "gavle.md",
            "fetcher": fetch_html,
            "parser": parse_jobs_gavle,
        },
        {
            "name": "Mälardalen University",
            "url": "https://www.mdu.se/en/malardalen-university/about-mdu/work-with-us/job-opportunities",
            "html_file": HTML_DIR / "latest_malardalen_page.html",
            "raw_md": RAW_DIR / "malardalen.md",
            "processed_md": CONTENT_DIR / "malardalen.md",
            "fetcher": fetch_html,
            "parser": parse_jobs_malardalen,
        },
    ]

    for uni in universities:
        print(f"\nScraping jobs for {uni['name']}...")

        # Many of your functions likely expect strings, so convert Path -> str at call boundaries
        uni["fetcher"](uni["url"], save_to=str(uni["html_file"]))

        jobs = uni["parser"](str(uni["html_file"]))

        uni["raw_md"].parent.mkdir(parents=True, exist_ok=True)
        with open(uni["raw_md"], "w", encoding="utf-8") as f:
            f.write(f"# {uni['name']}\n\n")
            for job in jobs:
                f.write(f"### {job['title']}\n")
                f.write(f"- **Link:** [View job posting]({job['url']})\n")
                f.write(f"- **Department:** {job['department']}\n")
                f.write(f"- **Published:** {job['published']}\n")
                f.write(f"- **Deadline:** {job['deadline']}\n\n")

        print(f"Processing jobs for {uni['name']}...")
        convert_md_headings_to_html(str(uni["raw_md"]), str(uni["processed_md"]))
        add_search_and_filter(Path(uni["processed_md"]))  # ok either way
        add_position_count(str(uni["processed_md"]))

    update_index_date(path=str(CONTENT_DIR / "index.md"))
    print("\nAll universities processed successfully!")

    merged_md = RAW_DIR / "current_positions.md"
    merge_job_markdowns(str(RAW_DIR), str(merged_md))
    convert_md_headings_to_html(str(merged_md), str(CONTENT_DIR / "current_positions.md"))
    add_search_and_filter(Path(CONTENT_DIR / "current_positions.md"))
    add_position_count(str(CONTENT_DIR / "current_positions.md"))
    print("\nAll universities merged successfully!")


if __name__ == "__main__":
    main()


# How to find the real URL for some universities
# Right click "Develop Tools" -- "Inspect" -- "Network" -- "Doc"
