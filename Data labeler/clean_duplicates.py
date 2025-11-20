"""
Verwijder alle image_paths die meer dan 1 keer voorkomen uit labels.csv
Houdt alleen unieke paths over.
"""

import csv
from pathlib import Path
from collections import Counter

CSV_PATH = Path("labels 2.csv")

# alle rijen inladen
rows = []
with open(CSV_PATH, "r") as f:
    reader = csv.reader(f)
    header = next(reader)  # lees header
    for row in reader:
        rows.append(row)

# tellen hoe vaak elk image_path voorkomt
path_counts = Counter(row[0] for row in rows)

# alleen houdt rijen met unieke image_paths
unique_rows = [row for row in rows if path_counts[row[0]] == 1]

print(f"Origineel: {len(rows)} rijen")
print(f"Duplicaten verwijderd: {len(rows) - len(unique_rows)} rijen")
print(f"Unieke paths: {len(unique_rows)} rijen")

# terugschrijven --> CSV
with open(CSV_PATH, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(unique_rows)

print(f"Opgeslagen in {CSV_PATH}")
