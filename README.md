# 💳 PDF Bank Statement Extractor

This project extracts transaction data from a bank statement in PDF format and exports it to a CSV file.

## 📄 What It Does

The script processes a PDF file (`extract.pdf`) containing a bank statement and outputs a CSV file (`extract.csv`) with the following structured fields for each transaction:

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

Ideal for personal finance tracking or integrating with budgeting tools where your bank only provides statements in PDF format.

## ✅ Output Example

| Date       | Description           | Amount   | Type    |
|------------|------------------------|----------|---------|
| 01-01-2024 | Grocery Store Purchase | 45.00    | SAIDA   |
| 03-01-2024 | Salary Deposit         | 1500.00  | ENTRADA |

---

Feel free to contribute or suggest improvements!