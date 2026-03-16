import csv
import json
import logging
import os
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from tqdm import tqdm

from directory_scraper import get_amc_links
from amc_scraper import scrape_amc, HEADERS


OUTPUT_DIR = "output"
RESUME_FILE = os.path.join(OUTPUT_DIR, "processed.txt")
LOG_FILE = os.path.join(OUTPUT_DIR, "scrape.log")

MAX_WORKERS = 16
REQUEST_TIMEOUT = 20
REQUEST_DELAY_RANGE = (0.0, 0.3)
RETRIES = 3
BACKOFF = 0.5
JSON_EXPORT = False


_log_lock = threading.Lock()


def setup_logging():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )


def log_event(event, **fields):
    payload = {"event": event}
    payload.update(fields)
    with _log_lock:
        logging.info(json.dumps(payload, ensure_ascii=False))


_thread_local = threading.local()


def build_session():
    session = requests.Session()

    retry = Retry(
        total=RETRIES,
        backoff_factor=BACKOFF,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    adapter = HTTPAdapter(max_retries=retry, pool_connections=MAX_WORKERS, pool_maxsize=MAX_WORKERS)

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    session.headers.update(HEADERS)

    return session


def get_session():
    if not hasattr(_thread_local, "session"):
        _thread_local.session = build_session()
    return _thread_local.session


def load_processed():
    if not os.path.exists(RESUME_FILE):
        return set()

    with open(RESUME_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def mark_processed(url):
    with _log_lock:
        with open(RESUME_FILE, "a", encoding="utf-8") as f:
            f.write(url + "\n")


def dedup_rows(rows):
    seen = set()
    unique = []

    for row in rows:
        key = tuple(row)
        if key not in seen:
            seen.add(key)
            unique.append(row)

    return unique


def fetch_and_parse(url):
    delay = random.uniform(*REQUEST_DELAY_RANGE)
    if delay > 0:
        time.sleep(delay)

    session = get_session()

    r = session.get(url, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()

    if not r.encoding:
        r.encoding = "utf-8"
    else:
        r.encoding = r.apparent_encoding

    return scrape_amc(r.text, url)


def write_csv(path, headers, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def write_json(path, headers, rows):
    data = [dict(zip(headers, row)) for row in rows]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    setup_logging()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    session = build_session()
    links = get_amc_links(session=session, timeout=REQUEST_TIMEOUT)

    log_event("links_fetched", count=len(links))
    print("Total AMCs found:", len(links))

    processed = load_processed()
    pending = [link for link in links if link not in processed]

    if not pending:
        log_event("resume_skip", message="All links already processed")
        print("All links already processed.")
        return

    amc_rows = []
    fund_rows = []
    manager_rows = []

    failures = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_map = {executor.submit(fetch_and_parse, link): link for link in pending}

        for future in tqdm(as_completed(future_map), total=len(future_map)):
            link = future_map[future]
            try:
                data = future.result()
            except Exception as exc:
                failures.append(link)
                log_event("scrape_failed", url=link, error=str(exc))
                continue

            amc_rows.append(data["amc"])
            fund_rows.extend(data["funds"])
            manager_rows.extend(data["managers"])

            mark_processed(link)
            log_event("scrape_ok", url=link)

    amc_rows = dedup_rows(amc_rows)
    fund_rows = dedup_rows(fund_rows)
    manager_rows = dedup_rows(manager_rows)

    write_csv(os.path.join(OUTPUT_DIR, "amc.csv"), [
        "amc_name",
        "aum",
        "clients",
        "approaches",
        "date",
        "linkedin",
        "url"
    ], amc_rows)

    write_csv(os.path.join(OUTPUT_DIR, "funds.csv"), [
        "amc_name",
        "fund_name",
        "category",
        "1yr",
        "2yr",
        "3yr",
        "5yr",
        "inception"
    ], fund_rows)

    write_csv(os.path.join(OUTPUT_DIR, "managers.csv"), [
        "amc_name",
        "manager_name",
        "designation",
        "bio"
    ], manager_rows)

    if JSON_EXPORT:
        write_json(os.path.join(OUTPUT_DIR, "amc.json"), [
            "amc_name",
            "aum",
            "clients",
            "approaches",
            "date",
            "linkedin",
            "url"
        ], amc_rows)

        write_json(os.path.join(OUTPUT_DIR, "funds.json"), [
            "amc_name",
            "fund_name",
            "category",
            "1yr",
            "2yr",
            "3yr",
            "5yr",
            "inception"
        ], fund_rows)

        write_json(os.path.join(OUTPUT_DIR, "managers.json"), [
            "amc_name",
            "manager_name",
            "designation",
            "bio"
        ], manager_rows)

    if failures:
        log_event("scrape_done", success=len(amc_rows), failures=len(failures))
        print("Failed pages:", len(failures))
    else:
        log_event("scrape_done", success=len(amc_rows), failures=0)


if __name__ == "__main__":
    main()
