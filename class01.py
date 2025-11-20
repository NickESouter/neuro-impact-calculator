#!/bin/python
# Time-stamp: <2025-20-11 monika.utrosa@gmail.com>

import pandas as pd

class acquisition():
    
    def __init__(self, modality, entity, duration, country, year):
        self.modality = modality # MRI
        self.entity   = entity   # anat, func, fmap, perf
        self.duration = duration # active scanning time
        self.country  = country  # user-specified
        self.year     = year     # user-specified

    def _get_consumption(self):

        df_carbon = pd.read_csv("data/carbon-intensity.csv")
        df_energy = pd.read_csv("data/Chodorowski_energy.csv")

        carbon_intensity = df_carbon[df_carbon["Entity"] == country][df_carbon["Year"] == year]["Carbon intensity of electricity - gCO2/kWh"]
        
        kWh_per_minute   = df_energy[df_energy["sequence"] == entity]["kWh_per_minute"]
        consumption = float(self.duration) * kWh_per_minute.iloc[0] * carbon_intensity.iloc[0]

        return consumption


# Example usage
if __name__ == "__main__":

    country  = "Spain"
    year     = 2015
    duration = 35
    entity   = "SE DWIMVb1000s/mm2 2.0mm"

    a = acquisition("MRI", entity, duration, country, year)
    w = a._get_consumption()
    print(w)