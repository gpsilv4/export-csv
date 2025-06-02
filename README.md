# 💳 Bank Statement & Coverflex Extractor

This project extracts transaction data from two sources:

- **Banco CTT**: Extracts transactions from a bank statement in PDF format.
- **Coverflex**: Extracts transactions from the Coverflex platform (Meal and Benefits categories).

All extracted data is exported to CSV files for easy analysis and integration.

## 📦 Features

### BANCO CTT

- **CSV Export for Banco CTT**: Extracts and exports the bank account statement from Banco CTT for a specific month to CSV format.

### COVERFLEX

- **Meal & Benefits Export**: Extracts all transactions from the Meal and Benefits categories.
- **Login Options**: Supports both manual and automatic login (with 2FA pause).
- **Month Selection**: Allows you to select all months or a specific month for export.
- **CSV Output**: Exports the extracted data to CSV files for easy integration with other tools.

## 📄 What It Does

The script processes a PDF file (`extract.pdf`) containing a Banco CTT bank statement and/or extracts transactions from the Coverflex platform. All data is exported to CSV files (`extract.csv`, `coverflex_meal.csv`, `coverflex_benefits.csv`) with the following structured fields for each transaction:

- `Date`: The transaction date  
- `Description`: The transaction description  
- `Amount`: The monetary value (positive or negative)  
- `Type`: Indicates whether the transaction is an `ENTRADA` (inflow) or `SAIDA` (outflow)  

It uses regular expressions to detect and parse each transaction line, even when transaction details span multiple lines.

## ⚙️ How It Works

- **PDF Parsing**: Uses [pdfplumber](https://github.com/jsvine/pdfplumber) to extract text from each page of the input PDF.
- **Line Grouping**: Accumulates and groups lines that belong to the same transaction block.
- **Regex Matching**: Applies pattern matching to extract date, description, and amount.
- **CSV Export**: Writes the cleaned data into a UTF-8 encoded CSV file with headers.

## 🧪 Example Use Case

Ideal for personal finance tracking or integrating with budgeting tools where your bank only provides statements in PDF format, or for exporting your Coverflex transactions.

## ✅ Output Example

| Date       | Description           | Amount   | Type    |
|------------|------------------------|----------|---------|
| 01-01-2024 | Grocery Store Purchase | 45.00    | SAIDA   |
| 03-01-2024 | Salary Deposit         | 1500.00  | ENTRADA |

---

Feel free to contribute or suggest improvements!