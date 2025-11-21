# from shared import df

# Prerequisites
from datetime import date
from shiny import App, render, ui
import pandas as pd
from utils.consumptions import mri_consumption, cooling_consumption, computing_consumption, storage_consumption
from pathlib import Path

# Paths to data
countryCarbonIntensity_filename = "data/carbon-intensity.csv"
scannerData_filename = "data/Scanner Power - Main.csv"
here = Path(__file__).parent


def get_choices(file_name, category, filter_cat=None, filter_val=None, other = False):

    if file_name == scannerData_filename and category == "model_full":
        df_choices = load_scanner_data(scannerData_filename=scannerData_filename)
    else:
        df_choices = pd.read_csv(file_name)

    if filter_cat is not None and filter_val is not None:
        df_choices = df_choices[df_choices[filter_cat] == filter_val]

    choice_list = df_choices[category].unique().tolist()
    if other:
        choice_list.append("Other")

    return choice_list

def load_scanner_data(scannerData_filename=scannerData_filename):
    df_models = pd.read_csv(scannerData_filename)
    df_models['model_full'] = df_models['Manufacturer'] + " " + df_models['Model']
    df_models.sort_values(by = ['model_full'], inplace = True)

    # Make sure field strength is a float
    df_models['Field strength'] = df_models['Field strength'].astype(float)

    return df_models

def compute_transports_comparison(carbon_emissions_g):
    # COMPARISON DATA
    flight_short = 221.8 # kg of co2, london to paris return
    flight_long = 1900 # kg of co2, london to NYC return
    car_ratio_km = 106.4 # g of co2 / km
    car_ratio_mile = 171 # g of co2 / mile

    # carbon emissions in kg
    ce_kg = convert_g2kg(carbon_emissions_g)

    # Transportation comparison summary
    transports_data = {}

    # Compute flight comparison
    if ce_kg / flight_short < 1:
        transports_data['flight_percent'] = (ce_kg / flight_short) * 100
        transports_data['flight_type'] = 'London-Paris return flight'
    else:
        transports_data['flight_percent'] = (ce_kg / flight_long) * 100
        transports_data['flight_type'] = 'London-New York return flight'

    # Compute car comparison
    transports_data['car_dist_km'] = carbon_emissions_g / car_ratio_km
    transports_data['car_dist_mile'] = carbon_emissions_g / car_ratio_mile

    return transports_data

def convert_g2kg(grams):
    return grams / 1000.0

def get_statement(summary):
    parts = []
    if summary["year"] != summary["year_eff"]:
        parts.append(f"<p><em>We don't have data for {summary['year']} yet, so the estimation provided is computed based on the closest year available ({summary['year_eff']}) for the country selected, {summary['country']}.</em></p>")
    if summary["model"] == "Other":
        parts.append(f"<p><em>The value provided below is computed as the median for {summary['field_strength']:.1f}T MRI models in our database.</em></p>")
    else:
        parts.append(f"<p>You have selected the {summary['model']} model.</p>")

    parts.append(f"<p>For the current study, <strong>{summary['scan_power']:.2f} kWh</strong> was used for MRI scanning <strong>{summary['sample_size']}</strong> subjects for a duration of active scanning of <strong>{summary['scan_duration']:.0f} minutes</strong> per subject,<br>"
                 f"and an additional <strong>{summary['idle_power']:.2f} kWh</strong> for idle scanning for a duration of <strong>{summary['idle_duration']:.0f} minutes</strong> per subject,<br>"
                 f"and <strong>{summary['computing_energy']:.2f} kWh</strong> for data processing and analysis.</p>")

    parts.append(f"<p>In <strong>{summary['country']}</strong> in <strong>{summary['year_eff']}</strong>, with a carbon intensity value of <strong>{summary['carbon_intensity']:.2f} grams</strong> of carbon dioxide per kWh (gCO2/kWh),"
                 f"this amounted to <strong>{convert_g2kg(summary['carbon_emissions']):.2f} kilograms</strong> of carbon dioxide-equivalent emissions.</p>")

    parts.append(f"<p>This is equivalent to <strong>{summary['transports_data']['flight_percent']:.2f}%</strong> of a <strong>{summary['transports_data']['flight_type']}</strong>,"
                 f"<strong>{summary['transports_data']['car_dist_km']:.2f} kilometers</strong> or <strong>{summary['transports_data']['car_dist_mile']:.2f} miles</strong> driven in a passenger car.</p>")

    return "\n".join(parts)

def compute_scan(modality, model, field_strength, scan_duration, idle_duration, country, year, sample_size, scannerData_filename=scannerData_filename, countryCarbonIntensity_filename=countryCarbonIntensity_filename):
    
    # Country specific data
    df_carbon = pd.read_csv(countryCarbonIntensity_filename)

    # If the year selected is not in the data we have for the selected country, take closest available year
    if year not in df_carbon[df_carbon["Entity"] == country]["Year"].values:
        # available_years = sorted(df_carbon[df_carbon["Entity"] == country]["Year"].unique())
        # year_eff = available_years[-1] # (abs(available_years - year)).argmin()
        available_years = df_carbon[df_carbon["Entity"] == country]["Year"].unique()
        year_eff = available_years[(abs(available_years - year)).argmin()]
    else:
        year_eff = year

    mask = (df_carbon["Entity"] == country) & (df_carbon["Year"] == year_eff)

    if not mask.any():
        raise ValueError(f"No carbon intensity data for {country} in {year_eff}") # TODO: We won't have such a case now
    
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
            scan_power = scan_mode_vals.median() # More robust than the mean given observed data 

            idle_mode_vals = df_energy.loc[df_energy["Field strength"] == field_strength, "idle_mode"].dropna()
            if idle_mode_vals.empty:
                raise ValueError(f"No idle_mode entries for field strength {field_strength}")
            idle_power = idle_mode_vals.median() # More robust than the mean given observed data
        
        # Total active scan and idle duration times
        scan_duration_tot = scan_duration * sample_size
        idle_duration_tot = idle_duration * sample_size

        # Calculate carbon emissions
        carbon_emissions = carbon_intensity * mri_consumption(idle_power, scan_power, scan_duration_tot, idle_duration_tot)

        # COMPUTING-RELATED CALCULATIONS
        ################################

        computing_energy = computing_consumption(cpu_hours=2, ram_gb=32, gpu_hours=0, pue_hpc = 1.56)

        # COMPUTE PERCENTAGES
        #####################
        transports_data = compute_transports_comparison(carbon_emissions)


        # SUMMARY
        #########

        summary = {
            "sample_size": sample_size,
            "country": country,
            "year": year,
            "year_eff": year_eff,
            "model": model,
            "field_strength": field_strength,
            "carbon_intensity": carbon_intensity,
            "scan_duration": scan_duration,
            "idle_duration": idle_duration,
            "carbon_emissions": carbon_emissions,
            "scan_power": scan_power,
            "idle_power": idle_power,
            "computing_energy": computing_energy,
            "transports_data": transports_data
        }

        return summary


# Server function provides access to client-side input values
def server(input, output, session):
    @render.ui
    def model_ui():
        field_strength = input.field_strength.get()
        if field_strength is None or field_strength == "":
            choices = get_choices(scannerData_filename, "model_full", other=True)
        else:
            choices = get_choices(scannerData_filename, "model_full", filter_cat="Field strength", filter_val=float(field_strength), other=True)
        return ui.input_select("model", "Model", choices=choices)

    @render.image
    def logo():
        img_path = Path(__file__).parent / "V34.svg"
        return {"src": str(img_path), "width": "300px"}


    @render.ui
    def consumption(scannerData_filename=scannerData_filename, 
                    countryCarbonIntensity_filename=countryCarbonIntensity_filename,
                    input=input):
        # Read inputs from Shiny input objects
        modality = input.modality.get()
        model = input.model.get()
        sample_size = input.sample_size.get()
        field_strength = float(input.field_strength.get())
        scan_duration = float(input.scan_duration.get())
        idle_duration = float(input.idle_duration.get())
        country = input.country.get()
        year = input.year.get()

        try:
            html_text = get_statement(compute_scan(modality, model, field_strength, scan_duration, idle_duration, country, year, sample_size, scannerData_filename=scannerData_filename, countryCarbonIntensity_filename=countryCarbonIntensity_filename))
            return ui.HTML(html_text)
        except Exception as e:
            return ui.HTML(f"<em>Error: {e}</em>")

if __name__ == "__main__":

    # User interface (UI) definition
    app_ui = ui.page_fluid(
        ui.panel_title(ui.h2("Neuro Impact Calculator", class_="pt-5")),
        
        ui.tags.div(
            ui.output_image("logo"),
            style="position: absolute; bottom: 10px; right: 20px; z-index: 1000;"
         ),
        
        ui.layout_columns(
            # Sidebar (left panel) for inputs
            ui.card(
                ui.input_numeric("sample_size", "Number of subjects scanned", 1, min=1),
                ui.input_numeric("scan_duration", "Duration of active scanning per subject (in minutes)", 60), 
                ui.input_numeric("idle_duration", "Duration of idle scanning per subject (in minutes)", 15), 
                ui.input_select(
                    "country", "Country", choices=get_choices("data/carbon-intensity.csv", "Entity")
                ),
                ui.input_numeric("year", "Year of the scanning", date.today().year-1, max=date.today().year, min=2000), 
                ui.input_select(
                    "modality", "Modality", choices=["MRI"]
                ),
                ui.input_select(
                    "field_strength", "Field strength", choices=get_choices(scannerData_filename, "Field strength")
                ),
                ui.output_ui("model_ui"),
            ),

            # Main panel (right) for output
            ui.card(
                ui.HTML(ui.output_ui("consumption"), ),
                position="right"
            ),

            col_widths = (3, 9),
        )
    )

    app = App(app_ui, server)
    app.run()
