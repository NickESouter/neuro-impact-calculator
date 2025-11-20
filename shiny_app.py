# from shared import df

from datetime import date
from shiny import App, render, ui
import pandas as pd



countryCarbonIntensity_filename = "data/carbon-intensity.csv"
scannerData_filename = "data/Scanner Power - Sheet3.csv"


def get_choices(file_name, category, other=False):
    if file_name == scannerData_filename and category == "model_full":
        df_choices = load_scanner_data(scannerData_filename=scannerData_filename)
    else:
        df_choices = pd.read_csv(file_name)
    choice_list = df_choices[category].unique().tolist()
    if other:
        choice_list.append("Other")
    return choice_list


def load_scanner_data(scannerData_filename=scannerData_filename):
    df_models = pd.read_csv(scannerData_filename)
    df_models['model_full'] = df_models['Manufacturer'] + ", " + df_models['Model']
    df_models.sort_values(by=['model_full'], inplace=True)

    # Make sure field strength is a float
    df_models['Field strength'] = df_models['Field strength'].astype(float)

    return df_models


def get_consumption(modality, model, field_strength, duration, country, year, scannerData_filename=scannerData_filename, countryCarbonIntensity_filename=countryCarbonIntensity_filename):

    # Country specific data
    df_carbon = pd.read_csv(countryCarbonIntensity_filename)
    mask = (df_carbon["Entity"] == country) & (df_carbon["Year"] == year)

    if not mask.any():
        raise ValueError(f"No carbon intensity data for {country} in {year}") 
    
    else:
        carbon_intensity = df_carbon.loc[mask, "Carbon intensity of electricity - gCO2/kWh"].iloc[0] # TODO: check that

        # Scanner specific data
        df_energy = load_scanner_data(scannerData_filename=scannerData_filename)

        # IF MODEL IS PART OF OUR LIST
        if model in df_energy["model_full"].values:
            scan_energy = df_energy.loc[df_energy["model_full"] == model, "scan_mode"].iloc[0] # TODO: check here too
        
        # IF NOT, USE THE AVERAGE BASED ON OUR DATABASE (by field strength)
        elif model == "Other":
            matching = df_energy.loc[df_energy["Field strength"] == field_strength, "scan_mode"].dropna()
            if matching.empty:
                raise ValueError(f"No scan_mode entries for field strength {field_strength}")
            scan_energy = matching.mean()

        return duration * scan_energy * carbon_intensity


# Server function provides access to client-side input values
def server(input):
    @render.text  
    def consumption(scannerData_filename=scannerData_filename, countryCarbonIntensity_filename=countryCarbonIntensity_filename, modality = input.modality, model = input.model, manufacturer = input.manufacturer, field_strength = input.field_strength, duration = input.minutes, country = input.country, year = input.year):
        # Read inputs from Shiny input objects
        modality = modality.get()
        model = model.get()
        field_strength = float(field_strength.get())
        duration = float(duration.get())
        country = country.get()
        year = year.get()

        try:
            return get_consumption(modality, model, field_strength, duration, country, year, scannerData_filename=scannerData_filename, countryCarbonIntensity_filename=countryCarbonIntensity_filename)
        except Exception as e:
            # Return an informative error string to the UI instead of raising
            return f"Error calculating consumption: {e}"
 
if __name__ == "__main__":

    # User interface (UI) definition
    app_ui = ui.page_fluid(

    ui.panel_title(ui.h2("Neuro Impact Calculator", class_="pt-5")),

    ui.input_numeric("minutes", "Minutes of active scanning", 45), 
    
    ui.input_numeric("year", "Year of the scanning", date.today().year), 

    ui.input_select(
        "country", "Country", choices=get_choices("data/carbon-intensity.csv", "Entity")
    ),

    ui.input_select(
        "modality", "Modality", choices=["MRI"]
    ),

    ui.input_select(
        "field_strength", "Field strength", choices=get_choices(scannerData_filename, "Field strength")
    ),

    
    ui.input_select(
        "model", "Model", choices=get_choices(scannerData_filename, "model_full", other=True)
    ),

    ui.output_text_verbatim("consumption"), 

    )

    app = App(app_ui, server)

    app.run()

