from pathlib import Path
import csv
import matplotlib.pyplot as plt
import numpy as np

SUBSAMPLE_LEVEL = 0
# This script iterates through folders in a folder
# Open each folder and find the csv file ending with "event_tagged"
# Make a list of tuples, each tuple corresponding to: relative time, f0, event name, step number
# List covers only MOF deposition steps

# Two plotting options are available: versus relative time or versus deposition step no

path = Path(r"M:\deposition monitoring\ngela-025")

data = {} # example: {folder_name: {file_name: {relative time : [], f0: [], event name: [], step number: [],
                                    # step_range: int, f0_length_each_step: {step_number: int}}}}

for folder in path.iterdir():
    if folder.is_dir():
        print(f"Processing folder: {folder.stem}")
        data[folder.name] = {}
        for file in folder.iterdir():
            if file.suffix == ".csv" and file.stem.endswith("event_tagged"):
                file_dict = {'relative_time': [],
                             'f0': [],
                             'event_name': [],
                             'step_number': [],
                             'step_range': 0,
                             'f0_length_each_step': {}}
                #Identify start and finish of MOF deposition
                with open(file, newline="") as f:
                    reader = csv.reader(f)
                    # Read until the first "Cu Withdraw" row
                    for row in reader:
                        if row[5] != "Cu Withdraw":
                            continue
                        break
                    # Keep reading the rest of the file
                    subsample_counter = 0
                    current_step_number = 0
                    step_length = 0
                    for row in reader:
                        if row[6] == 0:
                            break # Stop loading data when we reach the final step
                        if subsample_counter >= SUBSAMPLE_LEVEL:
                            file_dict['relative_time'].append(float(row[1]))
                            file_dict['f0'].append(float(row[3]))
                            file_dict['event_name'].append(row[5])
                            file_dict['step_number'].append(int(row[6]))
                            # Count the length of each step
                            current_step_number = int(row[6])
                            if current_step_number in file_dict['f0_length_each_step']:
                                file_dict['f0_length_each_step'][current_step_number] += 1
                            else:
                                file_dict['f0_length_each_step'][current_step_number] = 1

                            subsample_counter = 0
                        subsample_counter += 1
                    file_dict['step_range'] = current_step_number # Add final step no as the step range

                data[folder.name][file.name] = file_dict

#print(data)


# Plot experiments vs relative time
plt.figure()
plt.xlabel("Time (h)")
plt.ylabel("f0 (Hz)")
plt.title("Comparison of experiments vs time")
plt.grid(True)

for folder in data.keys():
    for file in data[folder].keys():
        x = [i/(60*60) for i in data[folder][file]["relative_time"]]
        y = data[folder][file]["f0"]
        label = folder
        plt.plot(x, y, label=label)


# Plot experiments vs step size time
plt.figure()
plt.xlabel("Step number")
plt.ylabel("f0 (Hz)")
plt.title("Comparison of experiments vs MOF deposition step")
plt.grid(True)

for folder in data.keys():
    for file in data[folder].keys():
        x = []
        y = data[folder][file]["f0"]
        print(len(y))
        # Generate the x-axis data points
        # Go through the step_number in each row
        # If it is identical to the previous step_no continue
        # If it is higher divide using np.linspace
        last_step_number = 0
        for step_number in data[folder][file]['step_number']:
            step_length = data[folder][file]['f0_length_each_step'][step_number]
            if step_number != 0 and step_number > last_step_number:
                print(f"{last_step_number=}")
                print(f"{step_number=}")
                last_step_number = step_number
                x.extend(np.linspace(step_number - 1, step_number, step_length))

        label = folder
        print(len(x))
        print(len(y))
        plt.plot(x, y, label=label)

# Add legend, grid, and display
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

