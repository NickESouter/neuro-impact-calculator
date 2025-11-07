# Neuro Impact Calculator

This repository will form the basis for an upcoming Brainhack Donostia 2025 project.

The actions we take as neuroimaging researchers, including conference travel, data collection, and even data preprocessing and storage, have a carbon footprint and therefore contribute to the climate crisis. Increasingly, funding bodies expect researchers to estimate the environmental impacts of proposed projects, and to take steps where possible to reduce them. There is an absence of tools which allow researchers to estimate their footprint across an entire project. Given that it frequently requires substantial energy to collect data, and results in large datasets and computationally expensive pipelines, human neuroimaging is an ideal discipline for such a tool.

This project will focus on workshopping, building, and disseminating a single platform which will allow neuroimaging researchers to estimate the environmental impact of their research, based on factors including imaging modality, length of data collection, and analysis software choice. Such a tool could be used prospectively during grant writing, or retrospectively during manuscript writing to provide a ‘sustainability statement’.

This tool will at the very least allow estimation of the carbon footprint of MRI scanning, and fMRI data analysis. Project members will be encouraged to bring insight from their own experience and data to allow expansion of the tool to other modalities, such as EEG, MEG, or PET. Ultimately, this will result in a ready to use open-source tool, in the form of either a Python package or a webpage with an online calculator. This tool will generate a paragraph of text for users which can then be inserted as an environmental impact statement into a grant application or manuscript.

## Data

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

This data allows for country-specific carbon footprint estimates, whereby energy usage in kWh can be multiplied by the respective conversion factor.

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
