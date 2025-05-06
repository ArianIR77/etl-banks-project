# ETL Project: Acquiring and Processing Information on the World's Largest Banks

## Project Overview

This project implements a complete ETL (Extract, Transform, Load) pipeline to gather data on the **top 10 largest banks in the world** by market capitalization, convert the values into different currencies, and store the results locally as both a CSV file and an SQLite database table.

The script is designed to run every financial quarter for consistent and up-to-date reporting.

---

## Table of Contents

- [Project Scenario](#project-scenario)
- [Technologies Used](#technologies-used)
- [ETL Pipeline Steps](#etl-pipeline-steps)
- [How to Run](#how-to-run)
- [Output](#output)
- [Author](#author)

---

## Project Scenario

A research organization requires a data engineer to compile the top 10 banks globally by market cap (in USD), convert these values into GBP, EUR, and INR using exchange rate data, and then store and log the process for future use.

---

## Technologies Used

- Python 3
- pandas
- numpy
- BeautifulSoup (bs4)
- requests
- sqlite3
- datetime

---

## ETL Pipeline Steps

### 1. **Extract**
- Scrapes the Wikipedia archive page for a table of banks by market capitalization.
- Retrieves only the top 10 rows.

### 2. **Transform**
- Converts the market cap from USD to GBP, EUR, and INR using exchange rate data from a CSV file.

### 3. **Load**
- Saves the final transformed data into:
  - A CSV file (`Largest_banks_data.csv`)
  - A SQLite database table (`Banks.db`, table name: `Largest_banks`)

### 4. **Logging**
- Logs progress to `code_log.txt` at every key stage of the ETL process.

---

## How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/etl-largest-banks.git
cd etl-largest-banks
````

### 2. Install Required Libraries

```bash
pip install pandas numpy beautifulsoup4 requests
```

### 3. Run the Script

```bash
python banks_project.py
```

> ⚠️ The script will download and process live data from the archived Wikipedia page and exchange rates CSV URL.

---

## Output

* `Largest_banks_data.csv` – Transformed data saved locally as CSV
* `Banks.db` – SQLite database file with one table: `Largest_banks`
* `code_log.txt` – Logs of each ETL stage
* Console Output – Query results from the database
