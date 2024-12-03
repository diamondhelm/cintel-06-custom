import faicons as fa  # For using font awesome in cards
import pandas as pd  # Pandas for data manipulation, required by plotly.express
import plotly.express as px  # Plotly Express for making Plotly plots
from shinywidgets import render_plotly  # For rendering Plotly plots
from shiny import reactive, render, req  # To define reactive calculations
from shiny.express import input, ui  # To define the user interface

exerise_df = px.data.exercise()

# Compute static values
exercise_type_tuple = (min(exercise_df.exercise_type), max(exercise_df.exercise_type))

# Define the Shiny UI Page layout
# Call the ui.page_opts() function to set the page title and make the page fillable
ui.page_opts(title="Exercise and Diet Data", fillable=True)


with ui.sidebar(open="open"):

    ui.h2("Sidebar")

    ui.input_slider(
        "selected_range_exercise_type",
        "Exercise type",
        min=lowfat[0],
        max= nofat[1],
        value=exercise_type_tuple,
        pre="$",
    )

    ui.input_checkbox_group(
        "selected_time_category",
        "Diet Type",
        ["Lowfat", "Nofat"],
        selected=["Lowfat", "Nofat"],
        inline=True,
    )

    ui.input_action_button("reset_event", "Reset filter")
    ui.hr()
    ui.h6("Links:")
    ui.a(
        "GitHub Source",
        href="https://github.com/diamondhelm/cintel-06-custom",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://github.com/diamondhelm/cintel-06-custom/blob/main/dashboard/app.py",
        target="_blank",
    )


# Value boxes
with ui.layout_columns(fill=False):

    with ui.value_box(showcase=ICONS["user"]):
        "Total contestants"

        @render.express
        def total_contestants():
            filtered_data().shape[0]

    with ui.value_box(showcase=ICONS["diets"]):
        "Diets"

        @render.express
        def diet_type():
            d = filtered_data()
           
    with ui.value_box(showcase=ICONS["exercise types"]):
            "Types of exercise"

        @render.express
        def exercise_type():

# Tables and charts
with ui.layout_columns(col_widths=[6, 6, 12]):

    with ui.card(full_screen=True):
        ui.card_header("Exercise data")

        @render.data_frame
        def table():
            return render.DataGrid(filtered_data())

    with ui.card(full_screen=True):
        with ui.card_header(class_="d-flex justify-content-between align-items-center"):
            "Total bill vs tip"
            with ui.popover(title="Add a color variable", placement="top"):
                ICONS["gear"]
                ui.input_radio_buttons(
                    "scatter_color",
                    None,
                    ["none", "Time", "HR", "Type", "ID type"],
                    inline=True,
                )

    with ui.card(full_screen=True):
        with ui.card_header(class_="d-flex justify-content-between align-items-center"):
            "Exercise Graph"
            with ui.popover(title="Add a color variable"):
                ICONS["gear"]
                ui.input_radio_buttons(
                    "type_exercise_y",
                    "Split by:",
                    ["diet", "exercise", "HR", "time"],
                    selected="type",
                    inline=True,
                )

        @render_plotly
        def type_exercise():
            filtered_df = filtered_data()
            filtered_df["percent"] = filtered_df.exercise / filtered_df.total_bill=
            yvar = input.tip_perc_y()

            # Create a violin plot with Plotly
            violin_figure = px.violin(
                filtered_df,
                y="percent",
                color=yvar,  # This will split the violin plot by the selected variable
                box=True,  # Displays a box plot inside the violin
                points="all",  # Shows all points
                hover_data=exercise_df.columns,  # Adds all other data as hover information
                title="Exercise Type with Diets " + yvar.capitalize(),
            )

            violin_figure.update_layout(
                yaxis_title="Exercise",
                legend_title=yvar.capitalize(),
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                ),
            )
            return violin_figure

    isInSelectedTime = exercise_df.time.isin(input.selected_time_category())

    return exercise_df[isTotalExercise & isInSelectedTime]

@reactive.effect
@reactive.event(input.reset_event)
def _():
    ui.update_slider("selected_type_of_exercise", value=type_of_exercise_tuple)

    ui.update_checkbox_group("selected_type_category", selected=["Lowfat", "Nofat"])
