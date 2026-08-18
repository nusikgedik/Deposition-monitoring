from pathlib import Path
import csv
import datetime

folder = Path(r"")

logs = {}

for file in folder.iterdir():
    if file.suffix != ".log":
        print(f"Skipping '{file.name}', it is not a .log file")
        continue

    with open(file, 'r') as fp:
        print(f"Parsing file '{file.name}'")
        events = []

        while True:
            values_sorted = {}

            line = fp.readline()

            if line == "":
                break

            values = line[:-1].split(" - ")

            if len(values) != 6:
                continue

            if values[1] != "INFO":
                continue

            values_sorted["datetime"]= datetime.datetime.strptime(values[0], "%Y-%m-%d %H:%M:%S")
            values_sorted["process"] = values[2]
            values_sorted["number"]= values[3]
            values_sorted["volume"] = values[4]
            values_sorted["rate"] = values[5]

            events.append(values_sorted)

        print(f"{events=}")
        print(len(events))
        # events = [
        #     {datetime: ..., process: ..., number: ...},
        #     {datetime: ..., process: ..., number: ...},
        #     ...
        # ]

for file in folder.iterdir():
    if file.suffix != ".csv":
        print(f"Skipping '{file.name}', it is not a .csv file")
        continue

    data_file = file
    with open(file, newline='') as csvfile:
        print(f"Parsing file '{file.name}'")
        qcm_data_reader = csv.reader(csvfile, delimiter=',')
        qcm_data_file_content = []
        for number,row in enumerate(qcm_data_reader):
            if number == 0:
                continue

            row[0] = row[0]+ " " + row[1]

            row[0] = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")

            del(row[1])
            qcm_data_file_content.append(row)

    print(qcm_data_file_content[:5])

current_event_i = 0
current_event = events[0]
for row in qcm_data_file_content:
    data_date_time = row[0]

    while current_event_i < len(events)-1:
        next_event = events[current_event_i+1]
        if data_date_time >= next_event['datetime']:
            current_event = next_event
            current_event_i += 1
        else:
            break

    row += [current_event['process'], current_event['number'], current_event['volume'], current_event['rate']]

save_data_file = data_file.name[:-4] + "_event_tagged.csv"

with open(save_data_file, newline='', mode='w+') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    csv_headers = ["Datetime", "Relative_time", "Temperature", "Resonance_frequency", "Dissipation",
                   "Process", "Number", "Volume", "Rate"]
    writer.writerow(csv_headers)
    writer.writerows(qcm_data_file_content)


