# Neuro Impact Calculator

The actions we take as neuroimaging researchers, including conference travel, data collection, and even data preprocessing and storage, have a carbon footprint and therefore contribute to the climate crisis. Increasingly, funding bodies expect researchers to estimate the environmental impacts of proposed projects, and to take steps where possible to reduce them. There is an absence of tools which allow researchers to estimate their footprint across an entire project. Given that it frequently requires substantial energy to collect data, and results in large datasets and computationally expensive pipelines, human neuroimaging is an ideal discipline for such a tool.

This online calculator is intended to provide an estimate of carbon dioxide (CO2) emissions for MRI scanning. Based on provided input information (see below), it generates an 'Environmental impact statement' which can be pasted into grant applications (rephrased to be prospective) or into a publication after the completion of a study. The tool can be accessed through the following URL (<LINK>). In short, the tool requires the following information as input:

* **Duration of active scanning (in minutes)** - The time spent actively collecting MRI data, with a participant in the scanner. Here, include the cumulative length of all scans run. Set at a default of 60 minutes
* **Duration of idle scanning (in minutes)** - The time during your allocated slot during which the scanner was not actively collecting data (e.g., setting up for scanning, putting the participant in the scanner). Set at a default of 15 minutes
* **Year of the scanning** - The year in which data was collected. In some cases, carbon intensity data for the respective combination of year and country may not be available. In such a case, the carbon intensity value for the nearest available year will be used
* **Country** - The country in which scanning was performed
* **Modality** - The neuroimaging modality used. At present, this is limited to MRI scanning. Future iterations may be expanded to include other modalities (EEG, MEG, CT)
* **Field strength** - The field strength of MRI scanning, currently includes 1.5T, 3T, and 7T
* **Model** - The model of the MRI scanner used, including both the manufacturer and the specific model

The components used for this tool are explained in turn below.

## data

This folder contains input data for running the tool.

### carbon_intensity.csv

This file contains carbon intensity conversion factors for countries and overseas territories across the world. Columns include:

* **Entity** - The resepctive country/territory
* **Code** - A shortened code for the respective entity
* **Year** - The year for which carbon intensity is reported
* **Carbon intensity of electricity - gCO2/kWh** - Carbon intensity conversion factor

This data was accessed via Our World in Data [https://ourworldindata.org/grapher/carbon-intensity-electricity]:

Source: Ember (2025), Energy Institute - Statistical Review of World Energy (2025) – with major processing by Our World In Data.

It was edited such that carbon intensity factors for entities larger than countries (e.g., Asia, Africa, the EU) were removed.

This data allows for country-specific carbon footprint estimates, whereby energy usage in kWh can be multiplied by the respective conversion factor to produce an estimate of carbon emissions

### Scanner Power - Sheet3.csv

This file contains power consumption factors for varying models of MRI field strengths and model types. This includes:

* **Manufacturer** - The manufacturer of the MRI scanner used (Siemens, GE, Philips, and Canon)
* **Field strength** - The field strength of the MRI scanner used (1.5T, 3T, 7T)
* **Model** - The specific model of scanner used
* **Off mode (kW)** - The power consumer by the scanner when in 'off' mode. Currently not used in calculations
* **Standby (no scan) mode (kW)** - Reported kW while the scanner is in standby mode
* **Ready-to-scan mode (kW)** - Reported kW while the scanner is in a ready to scan state, not actively collecting data
* **idle_mode** - A kW value for the scanner while not actively collecting data. A separate column has been made for this given that manufacturers variably provide data for the two above fields, and the real term difference between them is not always clear. When one value is provided, this is taken to be idle scanning power. When values are provided for both of the above fields, they are averaged to produce this estimate
* **Scan mode (kW)** - Reported kW during active MRI scanning of patients
* **scan_mode** - As the field above, but adjusted as needed. This is only relevant when a range of values have been provided by the manufacturer. In such cases, the average of the minimum and maximum value is taken.
* **Source** - A URL reflecting where this information has been extracted

Currently, the data in this file has been taken from environmental declarations and poduct specifications provided for the respective model by manufacturers.

### MRI_energy.csv

This file contains energy usage (kWh) per minute metrics for MRI scanning, as taken from multiple papers. The aim of this resource was to allow for flexible estimations of energy usage based on the specific scanner in use, in light of data provided across studies. Note, however, that this resource is largely incomplete. Papers discussing the energy usage of MRI rarely provide sufficient data, including (a) duraiton of MRI scanning and (b) energy usage for a given scan (kWh). Additionally, several of the papers listed here are not open access, meaning metrics cannot be extracted. Ultimately, it may be wise to disregard this file and instead use the csv file discussed below.

That said, this file contains the following columns:

* **kWh_per_minute** - kWh needed for active MRI scanning per minute
* **paper** - Name of the paper from which this metric has been taken
* **url** - DOI links for each paper referenced
* **scanner** - The specific MRI scanner used to derive the metric
* **notes** - Context on how the estimated was derived from the respective paper, or comments on why this metric could not be accessed.

### Chodorowski_energy.csv

Chodorowski et al. (2024) [https://doi.org/10.1016/j.neurad.2023.12.001] provides a useful resource with which to estimate energy usage of MRI scanning. For scanning on a a 3T Philips MR7700 scanner, this paper provides (a) duration of scanning and (b) energy usage (kWh) per scan for both and fMRI EPI sequence and several variants of DWI sequences. From this, hourly energy usage of MRI scanning can be inferred. This may therefore be an ideal resource with which to estimate the energy usage of MRI scanning, although it lacks comparable data for structural scanning (T1/T2). This file contains the following columns:

* **sequence** - The scanning sequence for which energy usage was measured.
* **duration_seconds** - The duration of the respective scan, in seconds as provided in the paper
* **duration_minutes** - This same duration metric converted to minutes
* **kWh** - The energy usage in kWh of the respective scanning sequence
* **kWh_per_minute** - The equivilant energy usage value for a minute of scanning

### Souter_energy.csv

Souter et al. (2025) [https://doi.org/10.1162/IMAG.a.36] estimated the energy usage of fMRI data processing in software pipelines FSL, SPM, and fMRIPrep. This file contains data from this paper, including:

* **software** - The software for which the estimate is provided
* **stage** - Either preprocessing or analysis
* **duration_seconds** - The duration of computing in seconds
* **duration_minutes** - The same duration metric converted to minutes
* **kWh** - The energy needed for this computing
* **kWh_per_minute** - The equivilant energy usage value for a minute of computing

While this provides a good starting point, it would be preferable to be able to use an existing carbon tracking tool, like the Green Algorithms calculator [https://calculator.green-algorithms.org/], which provides flexibility on things like the specific processor used, and the power use effectiveness of the data centre. The benchmark data provided by Souter al. (2025) assumes the use of an Intel® Xeon® Processor E5-2640 v3, and a power use effectiveness value of 1.28. The data processed for this paper was approximatley 6 minutes of task fMRI data, at 2mm resolution.



## Running 
### Requirements

pip install shiny

\>\>\>  python shiny_app.py   

Link to access: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
