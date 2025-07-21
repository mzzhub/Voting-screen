import csv
from collections import defaultdict

# Step 1: Read CSV and count votes
vote_counts = defaultdict(lambda: defaultdict(int))

with open('votes.csv', 'r') as f:
    reader = csv.reader(f)
    for position, candidate in reader:
        vote_counts[position][candidate] += 1

# Step 2: Sort candidates by vote count for each position
sorted_candidates = {}
max_rows = 0

for position, candidates in vote_counts.items():
    sorted_list = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
    sorted_candidates[position] = sorted_list
    max_rows = max(max_rows, len(sorted_list))

# Step 3: Build table column-wise
positions = sorted(sorted_candidates.keys())
headers = [""] + positions
rows = []

for i in range(max_rows):
    row = []
    for pos in positions:
        if i < len(sorted_candidates[pos]):
            name, count = sorted_candidates[pos][i]
            row.append(f"{name} ({count})")
        else:
            row.append("-")
    rows.append(row)

# Step 4: Print the table
col_widths = [max(len(cell) for cell in col) for col in zip(*([positions] + rows))]

def format_row(row):
    return "| " + " | ".join(cell.ljust(width) for cell, width in zip(row, col_widths)) + " |"

# Print header
print("+" + "+".join("-" * (width + 2) for width in col_widths) + "+")
print("| " + " | ".join(pos.ljust(width) for pos, width in zip(positions, col_widths)) + " |")
print("+" + "+".join("-" * (width + 2) for width in col_widths) + "+")

# Print rows
for row in rows:
    print(format_row(row))
