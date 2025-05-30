import pdfplumber
import csv
import re

# Input and output file paths
input_pdf = "extract.pdf"
output_csv = "extracted_extract.csv"

# List to store extracted transaction data
extracted_data = []

# Regex to detect the start of a line with a date (e.g. 01-01-2024)
date_pattern = re.compile(r"^\d{2}-\d{2}-\d{4}")

# Regex to extract full transaction information
# Format: date, value date, description, optional ID, amount
transaction_pattern = re.compile(
    r"^(\d{2}-\d{2}-\d{4})\s+(\d{2}-\d{2}-\d{4})\s+(.+?)(?:\s+([a-zA-Z0-9]{6,})\s+)?(-?\d{1,3}(?:[.,]\d{2}))",
    re.DOTALL
)

# Buffer to accumulate lines belonging to the same transaction
buffered_line = ""

with pdfplumber.open(input_pdf) as pdf:
    for i, page in enumerate(pdf.pages):
        print(f"\n📄 Page {i + 1}")
        text = page.extract_text()

        if text:
            for line in text.split("\n"):
                print("🔍", line)

                # If the line starts with a date, it likely starts a new transaction
                if date_pattern.match(line):
                    # Try to extract data from the previously accumulated block
                    if buffered_line:
                        block = buffered_line.strip().replace("\n", " ")
                        match = transaction_pattern.search(block)

                        if match:
                            date = match.group(1)
                            description = match.group(3).strip()
                            amount_raw = match.group(5).replace(",", ".")
                            try:
                                amount = abs(float(amount_raw))
                                transaction_type = "SAIDA" if "-" in amount_raw else "ENTRADA"
                                extracted_data.append([date, description, f"{amount:.2f}", transaction_type])
                            except Exception as e:
                                print("❌ Error converting amount:", amount_raw, e)

                    # Start a new block
                    buffered_line = line
                else:
                    # Continue accumulating lines into the same block
                    buffered_line += " " + line.strip()

            # After processing all lines, don't forget the last block
            if buffered_line:
                block = buffered_line.strip().replace("\n", " ")
                match = transaction_pattern.search(block)

                if match:
                    date = match.group(1)
                    description = match.group(3).strip()
                    amount_raw = match.group(5).replace(",", ".")
                    try:
                        amount = abs(float(amount_raw))
                        transaction_type = "SAIDA" if "-" in amount_raw else "ENTRADA"
                        extracted_data.append([date, description, f"{amount:.2f}", transaction_type])
                    except Exception as e:
                        print("❌ Error converting amount:", amount_raw, e)

                buffered_line = ""

# Write extracted data to CSV file
with open(output_csv, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(["Date", "Description", "Amount", "Type"])
    writer.writerows(extracted_data)

print(f"\n✅ {len(extracted_data)} transactions extracted and saved to '{output_csv}'")
