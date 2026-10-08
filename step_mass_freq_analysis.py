from pathlib import Path
import pandas as pd
import math


# Parameters for S equation for mass calculation from freq change
f_0 = 10000000 # in Hz
area = 0.09 # in cm2
shear_modulus = 2.947*(10**11) # in g cm-1 s-2
density = 2.648 # in g cm-3

def freq_to_mass(delta_freq):
    delta_mass_g = (delta_freq * area * math.sqrt(shear_modulus*density))/(2*(f_0**2))
    delta_mass_mcg = delta_mass_g * (10**6)
    return round(delta_mass_mcg, 2)

def generate_changes_table(df, event_name, total_cycle):
    changes = {}
    for cycle_no in range(1,total_cycle+1):
        result = df[
            (df["Process"] == event_name) &
            (df["Number"] == cycle_no)
        ]

        first_frequency = result["Resonance_frequency"].iloc[0]
        last_frequency = result["Resonance_frequency"].iloc[-1]

        frequency_change = last_frequency - first_frequency
        mass_change = freq_to_mass(-frequency_change)

        changes[cycle_no] = [int(frequency_change), round(mass_change, 2)]

    table = pd.DataFrame.from_dict(
    changes,
    orient="index",
    columns=["Frequency change", "Mass change"]
    ).reset_index()

    table.columns = ["Cycle", "Frequency change", "Mass change"]

    print(f"Event: {event_name}")
    print(table.to_string(index=False))

# Define the file name below to analyze the frequency and mass change observed in each Cu or linker deposition step
if __name__ == "__main__":

    folder = Path(r"M:\deposition monitoring\ngela-025")
    tagged_data_file = folder / "1-2026-Aug-24_15-06-19_fundamental_event_tagged.csv"

    df = pd.read_csv(tagged_data_file, encoding="cp1252")
    event_name = "Cu Infuse" # Cu infuse, Linker infuse
    total_cycle = 10

    generate_changes_table(df, event_name, total_cycle)