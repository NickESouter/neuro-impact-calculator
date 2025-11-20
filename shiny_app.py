# from shared import df

# Prerequisites
from datetime import date
from shiny import App, render, ui
import pandas as pd

<<<<<<< HEAD
from utils.consumptions import mri_consumption, cooling_consumption


=======
# Path to data
>>>>>>> e4687b4e839f2ceda59d8fe3d52607a3d83fd1ea
countryCarbonIntensity_filename = "data/carbon-intensity.csv"
scannerData_filename = "data/Scanner Power - Sheet3.csv"

def get_choices(file_name, category, other = False):

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
    df_models.sort_values(by = ['model_full'], inplace = True)

    # Make sure field strength is a float
    df_models['Field strength'] = df_models['Field strength'].astype(float)

    return df_models


def compute_percents(summary, transport_mode):
    # TODO: implement
    return 0

def get_computing_energy():
    # TODO: implement

    return 0

def convert_g2kg(grams):
    return grams / 1000.0

def get_statement(summary):
    text = (
        f"For the current study, {summary['scan_power']:.2f} kWh was used for MRI scanning, "
        f"and {summary['computing_energy']:.2f} kWh for data processing and analysis. "
        f"In {summary['country']}, with a carbon intensity value of {summary['carbon_intensity']:.2f} grams of carbon dioxide per kWh (gCO2/kWh), "
        f"this amounted to {convert_g2kg(summary['carbon_emissions']):.2f} kilograms of carbon dioxide-equivalent emissions. "
        f"This is equivalent to {compute_percents(summary, 'flight'):.2f}% of a return flight from London to Paris, "
        f"{compute_percents(summary, 'car'):.2f}% miles driven in a passenger car."
    )
    return text

def compute_scan(modality, model, field_strength, scan_duration, country, year, scannerData_filename=scannerData_filename, countryCarbonIntensity_filename=countryCarbonIntensity_filename):
    
    # Country specific data
    df_carbon = pd.read_csv(countryCarbonIntensity_filename)
    mask = (df_carbon["Entity"] == country) & (df_carbon["Year"] == year)

    if not mask.any():
        raise ValueError(f"No carbon intensity data for {country} in {year}") 
    
    else:
        carbon_intensity = df_carbon.loc[mask, "Carbon intensity of electricity - gCO2/kWh"].iloc[0] # TODO: check that

        # Scanner specific data
        df_energy = load_scanner_data(scannerData_filename=scannerData_filename)

        # MACHINE-RELATED CALCULATIONS
        ##############################

        # If the model is in our database
        if model in df_energy["model_full"].values:
            scan_power = df_energy.loc[df_energy["model_full"] == model, "scan_mode"].iloc[0]
            idle_power = df_energy.loc[df_energy["model_full"] == model, "idle_mode"].iloc[0]
        
        # If not, use the average based on our database (by field strength)
        elif model == "Other":
            scan_mode_vals = df_energy.loc[df_energy["Field strength"] == field_strength, "scan_mode"].dropna()
            if scan_mode_vals.empty:
                raise ValueError(f"No scan_mode entries for field strength {field_strength}")
            scan_power = scan_mode_vals.mean()

            idle_mode_vals = df_energy.loc[df_energy["Field strength"] == field_strength, "idle_mode"].dropna()
            if idle_mode_vals.empty:
                raise ValueError(f"No idle_mode entries for field strength {field_strength}")
            idle_power = idle_mode_vals.mean()
        
        # carbon_emissions = duration * scan_power * carbon_intensity
        carbon_emissions = mri_consumption(idle_power, scan_power, duration)

        # COMPUTING-RELATED CALCULATIONS
        ################################

        computing_energy = get_computing_energy() # TODO: decide to keep, and if yes, implement


        # SUMMARY
        #########

        summary = {
            "country": country,
            "year": year,
            "carbon_intensity": carbon_intensity,
            "duration": duration,
            "carbon_emissions": carbon_emissions,
            "scan_power": scan_power,
            "computing_energy": computing_energy
        }

        return summary


# Server function provides access to client-side input values
def server(input):
    @render.text  
    def consumption(scannerData_filename=scannerData_filename, countryCarbonIntensity_filename=countryCarbonIntensity_filename, modality = input.modality, model = input.model, manufacturer = input.manufacturer, field_strength = input.field_strength, scan_duration = input.scan_duration, country = input.country, year = input.year):
        # Read inputs from Shiny input objects
        modality = modality.get()
        model = model.get()
        manufacturer = manufacturer.get()
        field_strength = float(field_strength.get())
        scan_duration = float(scan_duration.get())
        idle_duration = float(idle_duration.get())
        country = country.get()
        year = year.get()

        try:
            return get_statement(compute_scan(modality, model, field_strength, duration, country, year, scannerData_filename=scannerData_filename, countryCarbonIntensity_filename=countryCarbonIntensity_filename))
        except Exception as e:
            # Return an informative error string to the UI instead of raising
            return f"Error: {e}"


if __name__ == "__main__":

    # User interface (UI) definition
    app_ui = ui.page_fluid(

    ui.panel_title(ui.h2("Neuro Impact Calculator", class_="pt-5")),

    ui.input_numeric("scan_duration", "Duration of active scanning (in minutes)", 45), 

    ui.input_numeric("idle_duration", "Duration of idle scanning (in minutes)", 45), 
    
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

    ui.output_text("consumption"),
    )

    app = App(app_ui, server)

    app.run()