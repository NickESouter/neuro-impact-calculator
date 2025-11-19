#!/bin/python
# Time-stamp: <2025-19-11 monika.utrosa@gmail.com>

class acquisition():
    
    def __init__(self, duration, carbon_intensity, kWh_per_minute): 
        self.duration 		  = duration  		  # What was the duration of the acquisition?
        self.kWh_per_minute   = kWh_per_minute    # What is the energy consuption of your acqusition?
        self.carbon_intensity = carbon_intensity  # What is the carbon intensity of your data collection site?
    
    def get_consumption(self):
    	consumption = self.duration * self.kWh_per_minute * self.carbon_intensity
    	
    	return consumption


# TEST
# Angloa 200 for 5 min of scanning with EPI DWIb1000s/mm2 3.0mm 
# Chodorowski


a = acquisition(5, 1.463414634, 256.94443)
c = a.get_consumption()
print(c)