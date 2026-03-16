import re
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def _clean(text):
    if text is None:
        return ""
    return " ".join(text.split()).strip()


def get_linkedin(soup):
    for link in soup.find_all("a", href=True):
        href = link.get("href", "")
        href_lower = href.lower()
        if "linkedin.com/company" in href_lower and "pmsbazaar" not in href_lower and "/admin" not in href_lower:
            return href
    return ""


def _pick_funds_table(soup):
    tables = soup.find_all("table")
    if not tables:
        return None

    keywords = {"fund", "category", "return", "approach", "inception"}

    best_table = None
    best_score = -1

    for table in tables:
        headers = [_clean(th.get_text()) for th in table.find_all("th")]
        header_text = " ".join(h.lower() for h in headers)
        score = sum(1 for k in keywords if k in header_text)

        if score > best_score:
            best_score = score
            best_table = table

    return best_table or tables[0]


def extract_funds(soup, amc_name):
    funds = []

    table = _pick_funds_table(soup)
    if not table:
        return funds

    rows = table.select("tbody tr") or table.find_all("tr")

    for row in rows:
        cols = [_clean(c.get_text()) for c in row.find_all("td")]

        if len(cols) >= 7:
            funds.append([
                amc_name,
                cols[0],
                cols[1],
                cols[2],
                cols[3],
                cols[4],
                cols[5],
                cols[6]
            ])

    return funds


def extract_managers(soup, amc_name):
    managers = []

    name_re = re.compile(r"^(Mr|Ms|Mrs|Dr)\b", re.IGNORECASE)

    for h in soup.find_all(["h2", "h3", "h4"]):
        name = _clean(h.get_text())

        if name_re.match(name):
            designation_tag = h.find_next(["h4", "h5"])
            bio_tag = h.find_next("p")

            designation = _clean(designation_tag.get_text()) if designation_tag else ""
            bio = _clean(bio_tag.get_text()) if bio_tag else ""

            managers.append([
                amc_name,
                name,
                designation,
                bio
            ])

    return managers


def _label_key(label):
    label = label.lower()
    if "aum" in label:
        return "aum"
    if "client" in label:
        return "clients"
    if "approach" in label or "strategy" in label:
        return "approaches"
    if "as on" in label or "as-on" in label or "as on date" in label or "as on" in label:
        return "date"
    return None


def _extract_metrics_from_cards(soup):
    metrics = {
        "aum": "",
        "clients": "",
        "approaches": "",
        "date": ""
    }

    for label_tag in soup.find_all(["h4", "h5", "span", "div", "th"]):
        label = _clean(label_tag.get_text())
        key = _label_key(label)
        if not key:
            continue

        value = ""

        value_tag = label_tag.find_next("b")
        if value_tag:
            value = _clean(value_tag.get_text())

        if not value:
            p_tag = label_tag.find_next("p")
            if p_tag:
                value = _clean(p_tag.get_text())

        if not value:
            parent = label_tag.parent
            if parent:
                bold = parent.find("b")
                if bold:
                    value = _clean(bold.get_text())

        if value and not metrics[key]:
            metrics[key] = value

    return metrics


def _extract_metrics_from_table(soup, metrics):
    tables = soup.find_all("table")
    if not tables:
        return metrics

    for table in tables:
        headers = [_clean(th.get_text()).lower() for th in table.find_all("th")]
        if not headers:
            continue

        header_text = " ".join(headers)
        if "aum" not in header_text and "client" not in header_text and "strategy" not in header_text and "approach" not in header_text:
            continue

        rows = table.find_all("tr")
        if len(rows) < 2:
            continue

        values = [_clean(cell.get_text()) for cell in rows[1].find_all(["td", "th"])]

        for i, header in enumerate(headers):
            if i >= len(values):
                continue

            value = values[i]
            if not value:
                continue

            key = _label_key(header)
            if key and not metrics[key]:
                metrics[key] = value

        break

    return metrics


def extract_metrics(soup):
    metrics = _extract_metrics_from_cards(soup)
    metrics = _extract_metrics_from_table(soup, metrics)
    return metrics


def scrape_amc(html, url):
    soup = BeautifulSoup(html, "lxml")

    name_tag = soup.find("h1")

    name = _clean(name_tag.get_text()) if name_tag else ""

    linkedin = get_linkedin(soup)

    metrics = extract_metrics(soup)

    funds = extract_funds(soup, name)

    managers = extract_managers(soup, name)

    return {
        "amc": [
            name,
            metrics.get("aum", ""),
            metrics.get("clients", ""),
            metrics.get("approaches", ""),
            metrics.get("date", ""),
            linkedin,
            url
        ],
        "funds": funds,
        "managers": managers
    }
