"""
Reflection Questions:
1. You've now completed a full ETL pipeline: read a CSV, transform the data, write a new CSV. 
   How does this compare to doing the same task in Excel? What can Python do that Excel can't do easily, and vice versa?
   Python automates repetitive ETL pipelines reliably across thousands of files, whereas Excel requires manual point-and-click or fragile VBA macros. 
   Excel excels at quick exploratory visual formatting and ad-hoc charting, while Python shines in scalability, version control integration, and programmatic robustness.

2. Exercise 8 showed you append mode. Think of a real business process that would benefit from an append-mode log file — describe it and explain why append mode is the right tool.
   An e-commerce order processing system benefits from an append-mode transaction log to record every incoming purchase securely over time without overwriting history. 
   Append mode is the right tool because it ensures audit trails grow chronologically and safely without risking data loss from truncation.
"""

import csv
from datetime import datetime
import os

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

print("--- EXERCISE 1 & 2: Read and print raw rows ---")
# Exercise 1 & 2: Read and print raw rows using csv.reader
with open("data/sales.csv", mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

print("\n--- EXERCISE 3: Skip the header ---")
# Exercise 3: Skip the header, store it, and print data rows separately
with open("data/sales.csv", mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)
    print(f"Header: {header}")
    print("Data rows:")
    for row in reader:
        print(row)

print("\n--- EXERCISE 4: Compute totals ---")
# Exercise 4: Compute totals per row and overall total revenue
total_revenue = 0.0
with open("data/sales.csv", mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # skip header
    for row in reader:
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        total_revenue += line_total
        print(
            f"{product}: {quantity} units × ${price:.2f} = ${line_total:.2f}"
        )
print(f"Overall Total Revenue: ${total_revenue:.2f}")

print("\n--- EXERCISE 5: Filter and write ---")
# Exercise 5: Filter orders with total > $100 and write to data/cleaned.csv
original_count = 0
written_count = 0

with open(
    "data/sales.csv", mode="r", encoding="utf-8"
) as infile, open(
    "data/cleaned.csv", mode="w", newline="", encoding="utf-8"
) as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Write new header
    writer.writerow(["Product", "Price", "Qty", "Total"])
    next(reader)  # skip original header

    for row in reader:
        original_count += 1
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity

        if line_total > 100:
            writer.writerow([product, f"{price:.2f}", quantity, f"{line_total:.2f}"])
            written_count += 1

print(
    f"Original rows: {original_count}, Cleaned/written rows (> $100): {written_count}"
)

print("\n--- EXERCISE 6: csv.DictReader ---")
# Exercise 6: Re-read using DictReader and compare totals
# Comment comparison: csv.reader accesses columns by integer index (e.g., row[0]), making code brittle if column order changes.
# csv.DictReader maps columns to dictionary keys (e.g., row['product']), making code more readable and robust against column reordering.
dict_total_revenue = 0.0
with open("data/sales.csv", mode="r", encoding="utf-8") as file:
    dict_reader = csv.DictReader(file)
    for row in dict_reader:
        price = float(row["price"])
        quantity = int(row["quantity"])
        dict_total_revenue += price * quantity
print(f"DictReader Total Revenue: ${dict_total_revenue:.2f}")

print("\n--- EXERCISE 7: Sales summary by product ---")
# Exercise 7: Build a summary dictionary {product_name: total_revenue} and print sorted by product name
product_summary = {}
with open("data/sales.csv", mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        product_summary[product] = product_summary.get(product, 0.0) + line_total

print("Product Summary (Sorted):")
for prod in sorted(product_summary.keys()):
    print(f"{prod}: ${product_summary[prod]:.2f}")

print("\n--- EXERCISE 8: Append mode log ---")
# Exercise 8: Append timestamp and total revenue to data/run_log.txt
os.makedirs("data", exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_entry = f"{timestamp} - Total Revenue: ${total_revenue:.2f}\n"

with open("data/run_log.txt", mode="a", encoding="utf-8") as log_file:
    log_file.write(log_entry)

print(f"Logged run: {log_entry.strip()}")