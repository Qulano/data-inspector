# 🔍 Data Pre-flight Inspector

A lightweight, robust command-line utility for pre-flight data quality auditing and automated sanitization of CSV datasets.

Designed for Data Analysts, BI Specialists, and Data Engineers to validate data integrity before loading into databases and ETL pipelines.

---

## ⚡ Key Features

- **6-Dimension Data Quality Checks:**
  - 📐 **Schema Consistency:** Detects missing or unexpected column counts.
  - 👤 **Name Validation:** Flags invalid names containing numeric digits.
  - 📧 **Email Syntax:** Validates email format (checks for `@` and domain extensions).
  - 🎂 **Type Integrity:** Detects non-numeric alphabetical characters in age fields.
  - 🕳 **Completeness:** Flags empty strings and null values (`,,`).
  - 👥 **Uniqueness:** Tracks and reports duplicate records by Primary ID.
- **Automated Surgeon Mode (`--clean`):** Surgically filters out all corrupted rows and outputs a clean dataset ready for database ingestion.
- **Data Purity Index:** Mathematically computes the overall quality percentage of the dataset.
- **Cyberpunk Terminal UI:** Beautiful color-coded diagnostic panels and status reporting powered by `Rich`.
- **Memory Efficient:** Processes data via line streaming without overloading RAM.

---

## 🚀 Quick Start

### 1. Clone the repository & enter the folder
```bash
git clone https://github.com/Qulano/data-inspector.git
cd data-inspector
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Diagnostics
```bash
# Run on sample demo data:
py inspector.py dirty_data.csv

# Diagnostic + Auto-clean mode:
py inspector.py dirty_data.csv --clean

# Run on YOUR OWN dataset:
py inspector.py path/to/your_file.csv --clean
```

---

## 📊 Diagnostic Dashboard Preview

- **Dirty Dataset (Requires Sanitization):**
  - Identifies row-level defects with exact line numbers.
  - Flags corrupted schema and duplicate records.
  - Displays dynamic warning panel with calculated Purity Index.

- **Clean Dataset (Verified):**
  - Confirms zero defects (`100.0% Purity Index`).
  - Safe for production database loading (`[OK]`).

---

## 🛠 Tech Stack

- **Language:** Python 3.10+
- **CLI & Styling:** `Rich`
- **Architecture:** Zero external dependencies for core data validation algorithms (pure Python Core).

---

## 📄 License

This project is licensed under the MIT License.
