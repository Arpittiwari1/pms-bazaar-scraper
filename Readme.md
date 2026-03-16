```markdown
# PMS Bazaar Web Scraper

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Web Scraping](https://img.shields.io/badge/Web%20Scraping-BeautifulSoup-green)
![Status](https://img.shields.io/badge/Project-Active-success)

A **Python-based web scraping tool** that extracts Portfolio Management Service (PMS) data from [PMS Bazaar](https://pmsbazaar.com) and exports it into structured CSV datasets.

The scraper collects information about **Asset Management Companies (AMCs), Funds, and Portfolio Managers** and handles missing data gracefully.
```
---

## 🚀 Project Highlights

- Scraped **300+ Asset Management Companies**
- Extracted **fund performance metrics**
- Collected **portfolio manager profiles**
- Structured financial data into **clean CSV datasets**
- Modular scraper architecture for scalability
- Handles missing data (`-`) when fields are unavailable

---

## 📊 Dataset Overview
```
### 1️⃣ AMC Dataset (`amc.csv`)

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

### 2️⃣ Funds Dataset (`funds.csv`)

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

### 3️⃣ Managers Dataset (`managers.csv`)

| Field       | Description |
|-------------|-------------|
| amc_name    | Asset Management Company |
| manager_name| Portfolio manager name |
| designation | Job title |
| bio         | Manager profile description |

---
```
## 🗂 Project Structure
```

pms-bazaar-scraper/  
│  
├── final/  
│   ├── amc_scraper.py  
│   ├── directory_scraper.py  
│   └── main.py  
│
├── output/  
│   ├── amc.csv  
│   ├── funds.csv  
│   └── managers.csv  
│
|── requirements.txt  
└── README.md  

```

---

##  Missing Data Handling

Some records may contain `"-"` values.  
This indicates that the data was **not available** on the source website at the time of scraping.

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

---
```

## 🛠 Technologies Used

- Python 3.13.11
- BeautifulSoup
- Requests
- lxml
- tqdm
- python-dotenv
- numpy

---

## ⚡ Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/pms-bazaar-scraper.git
cd pms-bazaar-scraper
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the scraper:

```bash
python final/main.py
```

The extracted datasets will be saved inside the **output/** folder.

---

## 📈 Dataset Counts

```
Total AMCs scraped: 300+
Total Funds records: 550+
Total Managers: 470+
```

---

## 🧠 Learning Outcomes

* Built a **modular web scraping pipeline**
* Handled **missing data** effectively
* Parsed HTML content using **BeautifulSoup**
* Exported structured datasets to **CSV**
* Organized a Python project professionally

---

## ⚖️ Disclaimer
```
This project is for **educational and research purposes only**.
All data is publicly available and belongs to the respective owners.
```
---

## 👤 Author
```
**Arpit Tiwari**

If you found this project useful, feel free to ⭐ the repository!
```