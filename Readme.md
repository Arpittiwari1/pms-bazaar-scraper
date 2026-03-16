```markdown
# PMS Bazaar Data Scraper

A Python-based web scraping tool that extracts Portfolio Management Service (PMS) data from https://pmsbazaar.com and converts it into structured datasets.

The scraper automatically collects information about **Asset Management Companies (AMCs), Funds, and Portfolio Managers** and exports the data into CSV files for analysis.


## Project Highlights

- Scraped **300+ Asset Management Companies**
- Extracted **fund performance metrics**
- Collected **portfolio manager profiles**
- Structured financial data into clean CSV datasets
- Built using a modular scraping architecture

---

## Dataset Overview

The scraper generates the following datasets:

### 1. AMC Dataset (`amc.csv`)

| Field      | Description |
|------------|-------------|
| amc_name   | Name of Asset Management Company |
| aum        | Assets Under Management |
| clients    | Number of clients |
| approaches | Investment strategy |
| date       | Data update date |
| linkedin   | LinkedIn profile |
| url        | Company webpage |

---

### 2. Funds Dataset (`funds.csv`)

| Field     | Description |
|-----------|-------------|
| amc_name  | Asset Management Company |
| fund_name | Fund name |
| category  | Investment category |
| 1yr       | 1 year return |
| 2yr       | 2 year return |
| 3yr       | 3 year return |
| 5yr       | 5 year return |
| inception | Return since inception |

---

### 3. Managers Dataset (`managers.csv`)

| Field       | Description |
|-------------|-------------|
| amc_name    | Asset Management Company |
| manager_name| Portfolio manager name |
| designation | Job title |
| bio         | Manager profile description |

---

## Project Structure

```

pms-bazaar-scraper
│
├── final
|     ├── amc_scraper.py
|     ├── directory_scraper.py
|     ├── main.py
│
├── output
│   ├── amc.csv
│   ├── funds.csv
│   └── managers.csv
│
├── requirements.txt
└── README.md

```
## Missing Data Handling

Some records may contain "-" values.  
This indicates that the data was not available on the source website at the time of scraping.
---

## Scraper Workflow

```

 PMS Bazaar Website
       │
       ▼
 Directory Scraper
 (Collects AMC Links)
       │
       ▼
   AMC Scraper
(Extracts AMC, Funds, Managers Data)
      │
      ▼
 Data Processing
      │
      ▼
CSV Dataset Export

````

---

## Technologies Used

- Python
- BeautifulSoup
- Requests

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/pms-bazaar-scraper.git
cd pms-bazaar-scraper
````

Install required libraries:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the scraper:

```bash
python main.py
```

The script will scrape PMS Bazaar and store the extracted datasets in the **output/** directory.

---

## Sample Output

Example from `amc.csv`:

| amc_name          | aum      | clients | approach |
| ----------------- | -------- | ------- | -------- |
| Example Capital   | ₹1200 Cr | 1500    | Growth   |
| Alpha Investments | ₹850 Cr  | 900     | Value    |

---

## Learning Outcomes

This project helped me gain practical experience in:

* Web scraping pipelines
* Parsing HTML with BeautifulSoup
* Data extraction and structuring
* Building modular Python scripts
* Exporting datasets for analysis

---
**dataset count**:
```
Total AMCs scraped: 300+
Total Funds records: 550+
Total Managers: 470+
``

## Disclaimer

This project is built for **educational and research purposes only**.

All data is collected from publicly available sources and belongs to their respective owners.
```
---

```
## Author

**Arpit tiwari**

If you found this project useful, feel free to ⭐ the repository.
---
```

