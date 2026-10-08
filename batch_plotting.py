from pathlib import Path
import csv
import datetime

# This script iterates through folders in a folder
# Open each folder and find the csv file ending with "event_tagged"
# Make a list of tuples, each tuple corresponding to: relative time, f0, event name, step number
# List covers only MOF deposition steps

# Two plotting options are available: versus relative time or versus deposition step no

path = Path(r"M:\deposition monitoring")

data = {} # example: {ngela-019: [relative time, f0, event name, step number] * 50...]

for folder in path.iterdir():
    if folder.is_dir():
        data[folder.name] = []
        for file in folder.iterdir():
            if file.suffix == ".csv" and file.stem.endswith("event_tagged"):
                data[folder.name].append(file.name)
                #Identify start and finish of MOF deposition
                with open(file, newline="") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        print(row[5])

print(data)

