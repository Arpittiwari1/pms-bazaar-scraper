import requests
from bs4 import BeautifulSoup

BASE = "https://pmsbazaar.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def _normalize_url(href):
    if not href:
        return None
    if href.startswith("http://") or href.startswith("https://"):
        return href
    if href.startswith("/"):
        return BASE + href
    return BASE + "/" + href


def get_amc_links(session=None, timeout=15):
    url = f"{BASE}/amc"

    client = session or requests
    r = client.get(url, headers=HEADERS, timeout=timeout)

    soup = BeautifulSoup(r.text, "lxml")

    links = []

    for a in soup.find_all("a", href=True):
        href = a.get("href", "")
        if "/AMC/" in href:
            full = _normalize_url(href)
            if full:
                links.append(full)

    return sorted(set(links))
