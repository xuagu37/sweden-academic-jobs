import re
from pathlib import Path
from datetime import date
import re
from pathlib import Path
from html import unescape

def convert_md_headings_to_html(input_path: str, output_path: str, level: int = 2):
    """
    Converts Markdown headings (##, ###, etc.) to HTML <hN> tags in a Markdown file,
    unescapes &amp; in Markdown links, and converts job info blocks into HTML <ul>.

    Handles both individual university .md files and merged all_current_jobs.md.

    Args:
        input_path (str): Path to the input .md file.
        output_path (str): Path to the output .md file.
        level (int): Minimum heading level to convert (default is 2).
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    text = input_path.read_text(encoding="utf-8")

    # --- 1. Convert headings like ## or ### to <h2>, <h3> etc. ---
    heading_pattern = re.compile(r"^(#{%d,}) (.+)$" % level, re.MULTILINE)

    def heading_replacer(match):
        hashes, title = match.groups()
        heading_level = len(hashes)
        return f"<h{heading_level}>{title.strip()}</h{heading_level}>\n"

    text = heading_pattern.sub(heading_replacer, text)

    # --- 2. Convert job bullet blocks into HTML lists ---
    job_block_pattern = re.compile(
        r"""(?P<list>- \*\*Link:\*\* \[([^\]]+)\]\(([^)]+)\)\s*
(?:- \*\*University:\*\* ?(.*)\s*)?
- \*\*Department:\*\* ?(.*)\s*
- \*\*Published:\*\* ?(.*)\s*
- \*\*Deadline:\*\* ?(.*))""",
        re.MULTILINE,
    )

    def job_block_replacer(match):
        _, label, raw_url, uni, dept, pub, deadline = match.groups()
        url = unescape(raw_url)

        # Build <ul> block
        block = [
            "<ul>",
            f'  <li><strong>Link:</strong> <a href="{url}">{label}</a></li>',
        ]

        if uni is not None:
            block.append(f'  <li><strong>University:</strong> {uni.strip()}</li>')

        block.extend([
            f'  <li><strong>Department:</strong> {dept.strip()}</li>',
            f'  <li><strong>Published:</strong> {pub.strip()}</li>',
            f'  <li><strong>Deadline:</strong> {deadline.strip()}</li>',
            "</ul>"
        ])
        return "\n".join(block)

    text = job_block_pattern.sub(job_block_replacer, text)

    output_path.write_text(text, encoding="utf-8")
    print(f"Converted headings and job blocks in {input_path.name}...")
    


def detect_job_type(title: str) -> str:
    title_lower = title.lower()

    if "research engineer" in title_lower:
        return "Research Engineer"
    elif "postdoc" in title_lower or "postdoctoral" in title_lower:
        return "Postdoc/Researcher"
    elif re.search(r'\bphd\b', title_lower) or (
         "doctoral" in title_lower and "postdoctoral" not in title_lower):
        return "PhD"
    elif "researcher" in title_lower:
        return "Postdoc/Researcher"
    elif "lecturer" in title_lower or "professor" in title_lower:
        return "Lecturer/Professor"
    else:
        return "Other"


def add_search_and_filter(md_file: Path):
    content = md_file.read_text(encoding="utf-8")

    # Skip if already processed
    if 'id="filterType"' in content or 'id="jobFilter"' in content:
        print(f"⚠️  Skipping {md_file.name} (already contains search/filter UI)")
        return

    lines = content.strip().splitlines()
    title_line = lines.pop(0) if lines[0].startswith('# ') else ""

    job_blocks = []
    current_block = []
    job_type = None

    for line in lines:
        if line.strip().startswith("<h3>"):
            if current_block:
                job_blocks.append((job_type, current_block))
                current_block = []

            title_text = re.sub(r"<\/?h3>", "", line).strip()
            job_type = detect_job_type(title_text)

        current_block.append(line)

    if current_block:
        job_blocks.append((job_type, current_block))

    # UI: Dropdown + Search Box
    filter_ui = """
<div id="filters" style="margin: 1em 0;">
  <label for="filterType"><strong>Filter by Job Type:</strong></label>
  <select id="filterType" style="margin-right: 1em;">
    <option value="">Show All</option>
    <option value="PhD">PhD</option>
    <option value="Postdoc/Researcher">Postdoc/Researcher</option>
    <option value="Lecturer/Professor">Lecturer/Professor</option>
    <option value="Research Engineer">Research Engineer</option>    
    <option value="Other">Other</option>
  </select>
  <input type="text" id="jobFilter" placeholder="Search jobs..." style="padding: 0.5em; width: 50%;">
</div>

<div id="jobList">
"""

    job_divs = []
    for jt, block in job_blocks:
        joined = "\n".join(block)
        wrapped = f'<div class="job" data-type="{jt}" style="margin-bottom: 1.5em;">\n{joined}\n</div>'
        job_divs.append(wrapped)

    end_div = "</div>\n\n"

    # JS: Combined filter logic (dropdown + search)
    filter_script = """<script>
document.addEventListener("DOMContentLoaded", function () {
  const typeSelect = document.getElementById('filterType');
  const textInput = document.getElementById('jobFilter');
  const jobBlocks = document.querySelectorAll('.job');

  function updateDisplay() {
    const selected = typeSelect.value.toLowerCase();
    const query = textInput.value.toLowerCase();

    jobBlocks.forEach(job => {
      const jobType = (job.dataset.type || "").toLowerCase();
      const matchesType = !selected || jobType === selected;
      const matchesQuery = job.textContent.toLowerCase().includes(query);
      job.style.display = (matchesType && matchesQuery) ? '' : 'none';
    });
  }

  typeSelect.addEventListener('change', updateDisplay);
  textInput.addEventListener('input', updateDisplay);
});
</script>
"""

    final = (
        f"{title_line}\n\n"
        + filter_ui
        + "\n\n".join(job_divs)
        + end_div
        + filter_script
    )

    md_file.write_text(final, encoding="utf-8")
    print(f"Added search and job-type filters to {md_file.name}...")




def update_index_date(path="content/index.md"):
    file_path = Path(path)
    content = file_path.read_text(encoding="utf-8")

    today = date.today().isoformat()
    updated_line = f"_Last updated: {today}_"

    # Replace the line or insert if not found
    if "_Last updated:" in content:
        content = re.sub(r"_Last updated:.*_", updated_line, content)
    else:
        content = content.replace(
            "Welcome! This site presents regularly scraped academic job listings from Swedish universities.",
            f"Welcome! This site presents regularly scraped academic job listings from Swedish universities.\n\n{updated_line}"
        )

    file_path.write_text(content, encoding="utf-8")
    print(f"Updated 'Last updated' in {file_path} to {today}...")
    
    
def add_job_count(file_path: str):
    path = Path(file_path)
    text = path.read_text(encoding="utf-8")

    # Count number of job entries
    matches = re.findall(r'<div class="job"\s', text)
    job_count = len(matches)

    # Never go negative (defensive)
    if job_count < 0:
        job_count = 0

    count_line = f'<p style="font-size: 1.2em; font-weight: bold;">Total jobs: {job_count}</p>'

    updated = re.sub(
        r"^(# .+?)\n",
        rf"\1\n{count_line}\n",
        text,
        count=1,
        flags=re.MULTILINE
    )

    # If you want “replace existing count line”, match the exact HTML we insert
    updated = re.sub(
        r'<p style="font-size: 1\.2em; font-weight: bold;">Total jobs: \d+</p>',
        count_line,
        updated
    )

    path.write_text(updated, encoding="utf-8")
    print(f"Added job count to {file_path}...")

    
    
def merge_job_markdowns(input_dir: str, output_path: str):
    input_dir = Path(input_dir)
    output_path = Path(output_path)

    merged = ["# All Current Jobs\n"]

    SKIP_NAMES = {
        output_path.name,
        "all_current_jobs.md",
    }

    for md_file in sorted(input_dir.glob("*.md")):
        if md_file.name in SKIP_NAMES:
            continue

        text = md_file.read_text(encoding="utf-8").strip()
        if not text:
            continue

        # University name from first H1
        m = re.search(r"^#\s*(.+)$", text, flags=re.MULTILINE)
        university = m.group(1).strip() if m else md_file.stem.replace("-", " ").title()

        # Split into entries by "### "
        # Keep only real job entries that start with "### "
        parts = text.split("\n### ")
        if len(parts) <= 1:
            continue  # no jobs in this file

        # parts[0] is header area; each subsequent part is one job without the leading "### "
        for part in parts[1:]:
            block = "### " + part.strip()

            # Ensure it contains a link line; otherwise skip (filters out weird content)
            if "- **Link:**" not in block:
                continue

            # Inject university line once
            if "**University:**" not in block:
                # Insert after Link line if possible
                lines = block.splitlines()
                new_lines = []
                inserted = False
                for line in lines:
                    new_lines.append(line)
                    if (not inserted) and line.startswith("- **Link:**"):
                        new_lines.append(f"- **University:** {university}")
                        inserted = True
                block = "\n".join(new_lines)

            merged.append(block + "\n")

    output_path.write_text("\n\n".join(merged).strip() + "\n", encoding="utf-8")
    print(f"Merged into {output_path.name}, skipping self-reference.")
    
