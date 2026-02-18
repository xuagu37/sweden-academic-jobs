from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urljoin
from html import unescape

def parse_jobs_lund(filepath: str):
    """
    Parses job listings from a saved HTML file using known class markers.

    Args:
        filepath (str): Path to the saved HTML file.

    Returns:
        List[Dict]: Parsed job entries with title, URL, department, published date, and deadline.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    # Look for all <h2> tags with the title class
    for title_h2 in soup.find_all("h2", class_="vacancies-list__job--title"):
        a_tag = title_h2.find("a")
        if not a_tag:
            continue

        title = a_tag.get_text(strip=True)
        url = a_tag.get("href")
        if not url.startswith("http"):
            url = "https://www.lunduniversity.lu.se" + url

        # Look around the same <td> block
        td_parent = title_h2.find_parent("td")

        # Department
        dept_p = td_parent.find("p", class_="vacancies-list__job--dept")
        department = dept_p.get_text(strip=True) if dept_p else "N/A"

        # Date published
        published_p = td_parent.find("p", class_="vacancies-list__job--date")
        published = "N/A"
        if published_p:
            text = published_p.get_text(strip=True)
            published = text.replace("Date published:", "").strip()

        # Last application date is in the next <td>
        next_td = td_parent.find_next_sibling("td")
        deadline = "N/A"
        if next_td:
            deadline_p = next_td.find("p")
            if deadline_p:
                deadline_text = deadline_p.get_text(strip=True)
                deadline = deadline_text.replace("Last application date:", "").strip()

        jobs.append({
            "title": title,
            "url": url,
            "department": department,
            "published": published,
            "deadline": deadline
        })

    return jobs

def parse_jobs_uppsala(filepath: str):
    """
    Parses job listings from Uppsala University's job page HTML structure.

    Args:
        filepath (str): Path to the saved HTML file.

    Returns:
        List[Dict]: Parsed job entries with title, URL, department, and deadline.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    containers = soup.find_all("div", class_="search-result-hit-text-container")

    for container in containers:
        title_tag = container.find("span", class_="list-group-item-action-title")
        link = title_tag.find("a") if title_tag else None
        department_tag = container.find("p", class_="mb-2")
        deadline_tag = container.find("div", class_="search-result-hit-details")

        if link:
            title = link.get_text(strip=True)
            relative_url = link.get("href")
            url = f"https://www.uu.se{relative_url}" if relative_url else "N/A"
            department = department_tag.get_text(strip=True) if department_tag else "N/A"
            deadline_text = deadline_tag.get_text(strip=True) if deadline_tag else "N/A"

            # Extract only the date from text like "Last application date: 14 May 2025"
            if "Last application date:" in deadline_text:
                deadline = deadline_text.split(":", 1)[-1].strip()
            else:
                deadline = deadline_text

            jobs.append({
                "title": title,
                "url": url,
                "department": department,
                "published": "",  # Published date not available
                "deadline": deadline
            })

    return jobs

def parse_jobs_stockholm(filepath: str):
    """
    Parses job listings from Stockholm University's Varbi page HTML.

    Args:
        filepath (str): Path to the saved HTML file.

    Returns:
        List[Dict]: Parsed job entries with title, URL, department, and deadline.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    jobs = []
    base_url = "https://su.varbi.com"

    for row in soup.find_all("tr"):
        title_td = row.find("td", class_="pos-title")
        dept_tds = row.find_all("td", class_="pos-desc")
        deadline_td = row.find("td", class_="pos-ends")

        if not title_td or not deadline_td or len(dept_tds) < 2:
            continue

        a_tag = title_td.find("a")
        if not a_tag:
            continue

        title = a_tag.get_text(strip=True)
        relative_url = a_tag.get("href", "")
        url = base_url + relative_url if relative_url.startswith("/") else relative_url

        department = dept_tds[1].get_text(strip=True)
        deadline = deadline_td.get_text(strip=True)

        jobs.append({
            "title": title,
            "url": url,
            "department": department,
            "published": "",  # No published date available
            "deadline": deadline
        })

    return jobs


def convert_reachmee_url(raw_url: str) -> str:
    """
    Convert a ReachMee 'main' style job URL to the working 'job' style URL.
    """
    decoded_url = unescape(raw_url)
    parsed = urlparse(decoded_url)
    query = parse_qs(parsed.query)

    if parsed.path.endswith("/main") and "rmjob" in query and "rmpage" in query and query["rmpage"][0] == "job":
        try:
            new_query = {
                "site": query["site"][0],
                "lang": query["lang"][0],
                "validator": query["validator"][0],
                "job_id": query["rmjob"][0]
            }
            return f"{parsed.scheme}://{parsed.netloc}/ext/I005/1035/job?{urlencode(new_query)}"
        except KeyError as e:
            print(f"Missing required parameter: {e}")
            return raw_url
    return raw_url


def parse_jobs_gothenburg(filepath: str):
    """
    Parses job listings from a Stockholm University ReachMee job HTML page.

    Args:
        filepath (str): Path to the saved HTML file.

    Returns:
        List[Dict]: Parsed job entries with title, URL, department, published, and deadline.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    for row in soup.find_all("tr"):
        a_tag = row.find("a", class_="link--xlarge")
        if not a_tag:
            continue

        title = a_tag.get_text(" ", strip=True)
        raw_url = a_tag.get("href", "")
        url = convert_reachmee_url(raw_url)

        # Find deadline by looking for the cell with label 'Application deadline'
        deadline = "N/A"
        for td in row.find_all("td"):
            label_div = td.find("div", class_="label")
            if label_div and "Application deadline" in label_div.get_text(strip=True):
                deadline_div = td.find("div", class_="description")
                if deadline_div:
                    deadline = deadline_div.get_text(strip=True)
                break

        jobs.append({
            "title": title,
            "url": url,
            "department": "",  # Can improve if dept is given
            "published": "",  # No published info in source
            "deadline": deadline
        })

    return jobs


def parse_jobs_ki(filepath: str):
    """
    Parses job listings from Karolinska Institutet's Varbi-powered HTML page.

    Args:
        filepath (str): Path to the saved HTML file.

    Returns:
        List[Dict]: Parsed job entries with title, URL, department, and deadline.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    rows = soup.select("table tbody tr")
    for row in rows:
        title_td = row.find("td", class_="views-field-title")
        dept_td = row.find("td", class_="views-field-field-vacancy-department")
        deadline_td = row.find("td", class_="views-field-field-last-application")

        if not title_td or not dept_td or not deadline_td:
            continue

        a_tag = title_td.find("a")
        if not a_tag:
            continue

        title = a_tag.get_text(" ", strip=True)
        url = a_tag.get("href", "").strip()
        department = dept_td.get_text(" ", strip=True)
        deadline_tag = deadline_td.find("time")
        deadline = deadline_tag.get_text(" ", strip=True) if deadline_tag else "N/A"

        jobs.append({
            "title": title,
            "url": url,
            "department": department,
            "published": "",
            "deadline": deadline
        })

    return jobs

def parse_jobs_kth(filepath: str):
    """
    Parses job listings from KTH's HTML page.
    """
    base_url = "https://www.kth.se"
    jobs = []

    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # KTH page table typically has no special class
    for row in soup.select("table tbody tr"):
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        title_link = cols[0].find("a")
        if not title_link or not title_link.get("href"):
            continue

        title = title_link.get_text(strip=True)
        url = title_link["href"]
        if not url.startswith("http"):
            url = base_url + url

        department = cols[2].get_text(strip=True)
        deadline = cols[3].get_text(strip=True)

        jobs.append({
            "title": title,
            "url": url,
            "department": department,
            "published": "",
            "deadline": deadline,
        })

    return jobs


def parse_jobs_linkoping(html_path: str) -> list[dict]:
    """
    Parse job postings from Linköping University's job vacancies HTML.

    Args:
        html_path (str): Path to the saved HTML file.

    Returns:
        List[Dict]: List of job postings with title, url, department, published, and deadline.
    """
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    jobs = []
    base_url = "https://liu.se"
    
    rows = soup.select("table tbody tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue

        title_col = cols[0]
        link_tag = title_col.find("a")
        if not link_tag:
            continue

        title = link_tag.text.strip()
        relative_url = link_tag.get("href")
        full_url = relative_url if relative_url.startswith("http") else base_url + relative_url

        deadline = cols[1].text.strip()

        jobs.append({
            "title": title,
            "url": full_url,
            "department": "",       # Not included in the listing table
            "published": "",        # Not available in this HTML view
            "deadline": deadline,
        })

    return jobs


def parse_jobs_umea(html_path: str) -> list[dict]:
    """
    Parses job postings from Umeå University's vacancies page.

    Args:
        html_path (str): Path to the saved HTML file.

    Returns:
        List[Dict]: List of jobs with title, url, department, published (empty), and deadline.
    """
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    jobs = []
    base_url = "https://www.umu.se"

    for job_card in soup.select("a.jobbTitle"):
        title = job_card.get_text(strip=True)
        relative_url = job_card.get("href")
        full_url = base_url + relative_url if relative_url else ""

        # Find the parent <div> of the job card to scope the search
        parent = job_card.find_parent()
        deadline_tag = parent.find_next("p", class_="applybydate")
        deadline = deadline_tag.text.strip() if deadline_tag else ""

        # Search department nearby
        info_div = parent.find_next("div", class_="info")
        department = ""
        if info_div:
            dept_span = info_div.find("span", string=lambda s: s and "Department" in s)
            if dept_span:
                department = dept_span.find_next_sibling("span").text.strip() if dept_span.find_next_sibling("span") else ""

            # fallback: search for any span after "Department of"
            for li in info_div.find_all("li"):
                span = li.find("span")
                if span and "Department of" in span.text:
                    department = span.text.strip()
                    break

        jobs.append({
            "title": title,
            "url": full_url,
            "department": department,
            "published": "",  # Not available
            "deadline": deadline,
        })

    return jobs


def parse_jobs_orebro(html_path: str) -> list[dict]:
    """
    Parses job postings from Örebro University's vacancies page.

    Args:
        html_path (str): Path to the saved HTML file.

    Returns:
        List[Dict]: List of jobs with title, url, department (N/A), published (N/A), and deadline.
    """
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    jobs = []
    base_url = "https://www.oru.se"

    for a_tag in soup.select("li > a[title]"):
        relative_url = a_tag.get("href", "")
        if "/available-positions/job/" not in relative_url:
            continue  # Skip non-job links

        title = a_tag.get("title", "").strip()
        full_url = urljoin(base_url, relative_url)

        # Find the <time> tag inside the <a> tag
        time_tag = a_tag.find("time")
        deadline = time_tag.get("datetime") if time_tag else ""

        jobs.append({
            "title": title,
            "url": full_url,
            "department": "",      # Not clearly available
            "published": "",       # Not available
            "deadline": deadline,
        })

    return jobs


def parse_jobs_lulea(html_path: str) -> list[dict]:
    """
    Parses job postings from Luleå University of Technology's vacancies page.

    Returns:
        List of dicts with title, url, department, published, deadline.
    """

    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    base_url = (
        "https://www.ltu.se/en/about-the-university/work-with-us/job-vacancies"
    )

    jobs = []

    for a in soup.select("a[href^='#item-']"):
        title = a.get_text(strip=True).removeprefix("Job:").strip()
        anchor = a.get("href")  # e.g. "#item-9742"

        # Extract numeric ID from anchor
        job_id = anchor.replace("#item-", "").strip()

        # Correct full URL format
        full_url = f"{base_url}?rmjob={job_id}{anchor}"

        deadline = ""

        # Look inside the same <li> for deadline paragraph
        parent_li = a.find_parent("li")
        if parent_li:
            for p in parent_li.find_all("p"):
                text = p.get_text(strip=True)
                if "Last day to apply" in text:
                    deadline = text.replace("Last day to apply:", "").strip()
                    break

        jobs.append({
            "title": title,
            "url": full_url,
            "department": "",
            "published": "",
            "deadline": deadline,
        })

    return jobs




def convert_reachmee_url_malmo(raw_url: str) -> str:
    """
    Convert a ReachMee 'main' style job URL to the working 'job' style URL.
    """
    decoded_url = unescape(raw_url)
    parsed = urlparse(decoded_url)
    query = parse_qs(parsed.query)

    if parsed.path.endswith("/main") and "rmjob" in query and "rmpage" in query and query["rmpage"][0] == "job":
        try:
            new_query = {
                "site": query["site"][0],
                "lang": query["lang"][0],
                "validator": query["validator"][0],
                "job_id": query["rmjob"][0]
            }
            return f"{parsed.scheme}://{parsed.netloc}/ext/I005/1015/job?{urlencode(new_query)}"
        except KeyError:
            return decoded_url
    return decoded_url

def parse_jobs_malmo(html_path: str) -> list[dict]:
    """
    Parses job postings from Malmö University's vacancies page.

    Args:
        html_path (str): Path to the saved HTML file.

    Returns:
        List[Dict]: List of jobs with title, url, department, published, and deadline.
    """
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    jobs = []

    for li in soup.select("li.list__item"):
        a_tag = li.find("a", class_="list__link")
        if not a_tag:
            continue

        raw_url = a_tag.get("href")
        url = convert_reachmee_url_malmo(raw_url)

        title_tag = li.find("h3", class_="list__list-title")
        title = title_tag.get_text(strip=True) if title_tag else ""

        # Department info
        dept_span = li.find("svg", {"class": "icon"})
        department = ""
        if dept_span:
            dept_text = dept_span.find_parent("span")
            if dept_text:
                department = dept_text.get_text(strip=True).rstrip(" /.").strip()

        # Find published and deadline
        published = ""
        deadline = ""
        spans = li.select("p span")
        for span in spans:
            text = span.get_text(strip=True)
            if "Last day to apply:" in text:
                deadline = text.replace("Last day to apply:", "").strip()
            elif "Published:" in text:
                published = text.replace("Published:", "").strip()

        jobs.append({
            "title": title,
            "url": url,
            "department": department,
            "published": published,
            "deadline": deadline,
        })

    return jobs


from bs4 import BeautifulSoup

def parse_jobs_chalmers(html_path: str) -> list[dict]:
    """
    Parses job postings from Chalmers University's ReachMee vacancies page.

    Args:
        html_path (str): Path to the saved HTML file.

    Returns:
        List[Dict]: List of jobs with title, url, department, published, and deadline.
    """
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    jobs = []

    for row in soup.select("tr"):
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        ref_no = cols[0].get_text(strip=True)
        a_tag = cols[1].find("a")
        if not a_tag:
            continue

        title = a_tag.get_text(strip=True)
        url = a_tag.get("href")
        if not url.startswith("http"):
            url = "https://web103.reachmee.com" + url

        # Extract hidden ISO-format deadline from <span data-order="1" style="display:none">
        deadline_tag = cols[2].find("span", attrs={"data-order": "1"})
        deadline = deadline_tag.get_text(strip=True) if deadline_tag else ""

        jobs.append({
            "title": title,
            "url": url,
            "department": "",      # Not available
            "published": "",       # Not available
            "deadline": deadline,  # Now in YYYY-MM-DD format
        })

    return jobs

from bs4 import BeautifulSoup

def parse_jobs_slu(html_path: str) -> list[dict]:
    """
    Parses job postings from SLU's ReachMee vacancies page.
    """
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    jobs: list[dict] = []

    # SLU job list is a table with id="jobsTable"
    for row in soup.select("#jobsTable tbody tr"):
        tds = row.find_all("td")
        if len(tds) < 4:
            continue

        # Title + URL
        a = tds[0].find("a", href=True)
        if not a:
            continue

        title = a.get_text(strip=True)
        url = a["href"].strip()
        if url.startswith("/"):
            url = "https://web103.reachmee.com" + url

        # Department
        department = tds[1].get_text(strip=True)

        # Deadline (shown as "Published to" on page)
        # Hidden ISO date exists in: <span data-order="1" style="display:none">YYYY-MM-DD</span>
        deadline = ""
        hidden = tds[3].find("span", attrs={"data-order": "1"})
        if hidden:
            deadline = hidden.get_text(strip=True)
        else:
            # fallback: parse visible dd/mm/yyyy text
            deadline = tds[3].get_text(" ", strip=True).replace("Published to:", "").strip()

        jobs.append({
            "title": title,
            "url": url,
            "department": department,
            "published": "",
            "deadline": deadline,
        })

    return jobs



from bs4 import BeautifulSoup

def parse_jobs_karlstad(html_path: str) -> list[dict]:
    """
    Parses job postings from Karlstad University's Varbi-powered vacancies page.

    Args:
        html_path (str): Path to the saved HTML file.

    Returns:
        List[Dict]: List of jobs with title, url, department, published, and deadline.
    """
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    jobs = []

    # Each job is a row (<tr>), assuming multiple <td> elements inside
    for row in soup.select("tr"):
        tds = row.find_all("td")
        if len(tds) < 3:
            continue

        # Title and URL
        a_tag = tds[0].find("a")
        if not a_tag:
            continue

        title = a_tag.get_text(strip=True)
        url = a_tag.get("href")
        if not url.startswith("http"):
            url = "https://kau.varbi.com" + url

        # Department is not explicitly listed — leave blank
        department = ""

        # Deadline
        deadline = tds[2].get_text(strip=True)

        jobs.append({
            "title": title,
            "url": url,
            "department": department,
            "published": "",       # Not available
            "deadline": deadline,
        })

    return jobs


def parse_jobs_sodertorn(html_path: str) -> list[dict]:
    """
    Parses job postings from Södertörn University's ReachMee-powered vacancies page.

    Args:
        html_path (str): Path to the saved HTML file.

    Returns:
        List[Dict]: List of jobs with title, url, department, published, and deadline.
    """
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    jobs = []

    # Each job appears across two <td>s in a <tr>
    for row in soup.select("tr"):
        tds = row.find_all("td")
        if len(tds) < 2:
            continue

        # Title and link
        a_tag = tds[0].find("a")
        if not a_tag:
            continue

        title = a_tag.get_text(strip=True)
        url = a_tag.get("href")
        if not url.startswith("http"):
            url = "https://web103.reachmee.com" + url

        # Deadline in hidden <span>
        deadline_tag = tds[1].find("span", attrs={"data-order": "1"})
        deadline = deadline_tag.get_text(strip=True) if deadline_tag else ""

        jobs.append({
            "title": title,
            "url": url,
            "department": "",     # Not present in HTML
            "published": "",      # Not present in HTML
            "deadline": deadline,
        })

    return jobs


def parse_jobs_dalarna(html_path: str) -> list[dict]:
    """
    Parses job postings from Dalarna University's vacancies page.

    Args:
        html_path (str): Path to the saved HTML file.

    Returns:
        List[Dict]: List of jobs with title, url, department, published, and deadline.
    """
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    jobs = []

    for job_div in soup.select("div.vacantpositions-item"):
        a_tag = job_div.find("a")
        if not a_tag:
            continue

        title = a_tag.get_text(strip=True)
        raw_url = a_tag.get("href", "")
        url = raw_url if raw_url.startswith("http") else f"https://www.du.se{raw_url}"

        deadline_tag = job_div.find("time")
        deadline = deadline_tag.get("datetime", "").split(" ")[0] if deadline_tag else ""

        jobs.append({
            "title": title,
            "url": url,
            "department": "",   # Not provided in the structure
            "published": "",    # Not provided
            "deadline": deadline,
        })

    return jobs


def parse_jobs_gavle(html_path: str) -> list[dict]:
    """
    Parses job postings from University of Gävle's Varbi-powered vacancies page.

    Args:
        html_path (str): Path to the saved HTML file.

    Returns:
        List[Dict]: List of jobs with title, url, department, published, and deadline.
    """
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    jobs = []

    for row in soup.select("li.hiq-varbi-jobs__row"):
        a_tag = row.find("a", class_="hiq-varbi-jobs__cell--title")
        if not a_tag:
            continue  # skip header row

        title = a_tag.get_text(strip=True)
        url = a_tag.get("href")
        if not url.startswith("http"):
            url = "https://hogskolanigavle.varbi.com" + url

        deadline = row.find("p", class_="hiq-varbi-jobs__cell--deadline")
        published = row.find("p", class_="hiq-varbi-jobs__cell--published")

        jobs.append({
            "title": title,
            "url": url,
            "department": "",  # Not explicitly provided
            "published": published.get_text(strip=True) if published else "",
            "deadline": deadline.get_text(strip=True) if deadline else "",
        })

    return jobs


def parse_jobs_malardalen(html_path: str) -> list[dict]:
    """
    Parses job postings from Mälardalen University's ReachMee-powered vacancies page.

    Args:
        html_path (str): Path to the saved HTML file.

    Returns:
        List[Dict]: List of jobs with title, url, department, published, and deadline.
    """
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    jobs = []

    for job_div in soup.select("div.mdh-archive-item__content"):
        title_tag = job_div.select_one("div.mdh-available-positions__item-title a")
        deadline_tag = job_div.select_one("div.mdh-available-positions__item-info")

        if not title_tag or not deadline_tag:
            continue

        title = title_tag.get_text(strip=True)
        raw_url = title_tag.get("href", "")
        url = unescape(raw_url) if raw_url.startswith("http") else f"https://www.mdu.se{unescape(raw_url)}"

        # Extract date part from "Apply by 2025-05-13"
        deadline_match = deadline_tag.get_text(strip=True).replace("Apply by", "").strip()

        jobs.append({
            "title": title,
            "url": url,
            "department": "",
            "published": "",
            "deadline": deadline_match,
        })

    return jobs


def parse_jobs_miun(html_path: str) -> list[dict]:
    """
    Parses job postings from Mid Sweden University's vacancies page.

    Args:
        html_path (str): Path to the saved HTML file.

    Returns:
        List[Dict]: List of jobs with title, url, and deadline.
    """
    from bs4 import BeautifulSoup
    from html import unescape

    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    jobs = []

    # Target the vacancies table
    rows = soup.select("div.link-table table tbody tr")

    for row in rows:
        title_tag = row.select_one('td[data-header="Position"] a')
        deadline_tag = row.select_one('td[data-header="Apply before"]')

        if not title_tag or not deadline_tag:
            continue

        title = title_tag.get_text(strip=True)

        raw_url = title_tag.get("href", "")
        url = (
            f"https://www.miun.se{unescape(raw_url)}"
            if raw_url.startswith("/")
            else unescape(raw_url)
        )

        deadline = deadline_tag.get_text(strip=True)

        jobs.append({
            "title": title,
            "url": url,
            "deadline": deadline,
        })

    return jobs
