from shared import df

from datetime import date
from shiny import App, render, ui

# User interface (UI) definition
app_ui = ui.page_fluid(

    ui.panel_title(ui.h2("Neuro Impact Calculator", class_="pt-5")),

    ui.input_numeric("minutes", "Minutes of active scanning", 45), 
    
    ui.input_numeric("year", "Year of the scanning", date.today().year), 

    ui.input_select(
        "country", "Country", choices=["Ecolandia", "Petrolandia"]
    ),

    ui.input_select(
        "entity", "Machine", choices=["Magnito", "GravityGuy"]
    ),

    ui.input_select(
        "modality", "Modality", choices=["MRI"]
    ),

    ui.output_text_verbatim("text"), 

    )


# Server function provides access to client-side input values
def server(input):
    @render.text  
    def text():
        return input.minutes()
    
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()

