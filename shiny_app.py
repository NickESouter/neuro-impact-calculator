# from shared import df

from datetime import date
from shiny import App, render, ui
import pandas as pd

# User interface (UI) definition
app_ui = ui.page_fluid(

    ui.panel_title(ui.h2("Neuro Impact Calculator", class_="pt-5")),

    ui.input_numeric("minutes", "Minutes of active scanning", 45), 
    
    ui.input_numeric("year", "Year of the scanning", date.today().year), 

    ui.input_select(
        "country", "Country", choices=["Spain", "Ecolandia", "Petrolandia"]
    ),

    ui.input_select(
        "entity", "Machine", choices=["SE DWIMVb1000s/mm2 2.0mm", "Magnito", "GravityGuy"] 
    ),

    ui.input_select(
        "modality", "Modality", choices=["MRI"]
    ),

    ui.output_text_verbatim("consumption"), 

    )


# Server function provides access to client-side input values
def server(input):
    @render.text  
    def consumption(modality = input.modality, entity = input.entity, duration = input.minutes, country = input.country, year = input.year):


        modality = modality.get()
        entity = entity.get()
        duration = duration.get()
        country = country.get()
        year= year.get()

        df_carbon = pd.read_csv("data/carbon-intensity.csv")
        df_energy = pd.read_csv("data/Chodorowski_energy.csv")

        mask = (df_carbon["Entity"] == country) & (df_carbon["Year"] == year)
        carbon_intensity = df_carbon.loc[mask, "Carbon intensity of electricity - gCO2/kWh"]

        kWh_per_minute   = df_energy[df_energy["sequence"] == entity]["kWh_per_minute"]
        consumption = float(duration) * kWh_per_minute.iloc[0] * carbon_intensity.iloc[0]

        return consumption 
 
 
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()

