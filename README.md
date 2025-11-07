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

This data was accessed via Our World in Data:

Source: Ember (2025), Energy Institute - Statistical Review of World Energy (2025) – with major processing by Our World In Data.

It was edited such that carbon intensity factors for entities larger than countries (e.g., Asia, Africa, the EU) were removed.

This data allows for country-specific carbon footprint estimates, whereby energy usage in kWh can be multiplied by the respective conversion factor.
