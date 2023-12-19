from ipywidgets import (
    Checkbox,
    VBox,
    Dropdown,
    FloatSlider,
    Layout,
    IntSlider,
    interactive_output,
    HBox,
)
from IPython.display import display
from . import flight_calculation

width = "300px"  # Slider width
description_width = "100px"  # Label width

# WIDGETS
wind_slider = IntSlider(
    value=5,
    min=0,
    max=10,
    step=1,
    description="Hitrost vetra [m/s]",
    readout=True,
    style={"description_width": "initial", "description_width": description_width},
    layout=Layout(width=width),
)
wind_direction_slider = IntSlider(
    value=90,
    min=0,
    max=360,
    step=1,
    description="Smer vetra [°]",
    readout=True,
    style={"description_width": "initial", "description_width": description_width},
    layout=Layout(width=width),
)

temparature_slider = IntSlider(
    value=25,
    min=-10,
    max=40,
    step=1,
    description="Temperatura okolice [°C]",
    readout=True,
    style={"description_width": "initial", "description_width": description_width},
    layout=Layout(width=width),
)

pressure_slider = FloatSlider(
    value=1.01,
    min=0,
    max=1.5,
    step=0.01,
    description="Tlak okolice [Bar]",
    readout=True,
    style={"description_width": "initial", "description_width": description_width},
    layout=Layout(width=width),
)

club_dropdown = Dropdown(
    options=[
        "driver",
        "3_wood",
        "5_wood",
        "3_iron",
        "4_iron",
        "5_iron",
        "6_iron",
        "7_iron",
        "8_iron",
        "9_iron",
        "PW",
    ]
)

ball_dropdown = Dropdown(options=["Titleist", "Calloway", "TaylorMade"])

club_speed_slider = FloatSlider(
    value=72,
    min=10,
    max=80,
    step=0.1,
    description="Hitrost palice ob udarcu [m/s]",
    readout=True,
    style={"description_width": "initial", "description_width": description_width},
    layout=Layout(width=width),
)
launch_angle_slider = FloatSlider(
    value=15,
    min=6,
    max=70,
    step=0.1,
    description="Naklon udarca [°]",
    readout=True,
    style={"description_width": "initial", "description_width": description_width},
    layout=Layout(width=width),
)
spin_x_slider = IntSlider(
    value=0,
    min=-100,
    max=100,
    step=1,
    description="Vrtljaji okoli x osi [RPM]",
    readout=True,
    style={"description_width": "initial", "description_width": description_width},
    layout=Layout(width=width),
)
spin_y_slider = IntSlider(
    value=-200,
    min=-300,
    max=300,
    step=1,
    description="Vrtljaji okoli y osi [RPM]",
    readout=True,
    style={"description_width": "initial", "description_width": description_width},
    layout=Layout(width=width),
)
spin_z_slider = IntSlider(
    value=0,
    min=-100,
    max=100,
    step=1,
    description="Vrtljaji okoli z osi [RPM]",
    readout=True,
    style={"description_width": "initial", "description_width": description_width},
    layout=Layout(width=width),
)
toggle = Checkbox(
    value=True, description="Uporabi Pre-set parametre"
)  # Checkbox for preset hide/show
local_weather = Checkbox(
    value=False, description="Uporabi lokalno vreme"
)  # Checkbox for preset hide/show
city_dropdown = Dropdown(
    options=[
        "Ljubljana",
        "London",
        "New York",
        "Paris",
        "Madrid",
        "Tokyo",
    ],
    disabled=True,
)
# \WIDGETS


def user_interface(get_value=False):
    """
    User interface for club/ball data

    Keyword arguments:
    get_data -- return data or display UI (default False)
    """

    # Calls custom_preset(toggle.value) when value changes

    # Only returns values of the selected menu (preset/custom), first element is for identifying which menu the function returns

    preset = VBox(
        children=[
            toggle,
            club_dropdown,
            ball_dropdown,
        ]
    )  # VBox for the preset option
    weather_box = VBox(
        [
            local_weather,
            temparature_slider,
            pressure_slider,
            wind_slider,
            wind_direction_slider,
        ]
    )

    if get_value:
        return [
            toggle.value,
            club_dropdown.value,
            ball_dropdown.value,
            club_speed_slider.value,
            launch_angle_slider.value,
            spin_x_slider.value,
            spin_y_slider.value,
            spin_z_slider.value,
            wind_slider.value,
            wind_direction_slider.value,
            temparature_slider.value,
            pressure_slider.value,
            local_weather,
        ]
    # displays VBox and preset/custom checkbox

    else:
        return (
            toggle,
            club_dropdown,
            ball_dropdown,
            club_speed_slider,
            launch_angle_slider,
            spin_x_slider,
            spin_y_slider,
            spin_z_slider,
            temparature_slider,
            pressure_slider,
            wind_slider,
            wind_direction_slider,
            local_weather,
        )


def live_plot():
    sliders = VBox(
        [
            toggle,
            club_dropdown,
            ball_dropdown,
            local_weather,
            city_dropdown,
            temparature_slider,
            pressure_slider,
            wind_slider,
            wind_direction_slider,
        ]
    )

    def update_graph(**args):
        flight_calculation.calculate_trajectory(plot_graph=True)

    def custom_preset(x):
        """Adjusts VBox to preset/custom inputs"""
        if x.get("new"):
            sliders.children = [
                toggle,
                club_dropdown,
                ball_dropdown,
                local_weather,
                city_dropdown,
                temparature_slider,
                pressure_slider,
                wind_slider,
                wind_direction_slider,
            ]  # Preset inputs
        else:
            sliders.children = [  # Custom inputs
                toggle,
                ball_dropdown,
                club_speed_slider,
                launch_angle_slider,
                spin_x_slider,
                spin_y_slider,
                spin_z_slider,
                local_weather,
                city_dropdown,
                temparature_slider,
                pressure_slider,
                wind_slider,
                wind_direction_slider,
            ]

    def loc_weather(x):
        if x.get("new"):
            city_dropdown.disabled = False
            temparature_slider.disabled = True
            pressure_slider.disabled = True
            wind_slider.disabled = True
            wind_direction_slider.disabled = True
        else:
            city_dropdown.disabled = True
            temparature_slider.disabled = False
            pressure_slider.disabled = False
            wind_slider.disabled = False
            wind_direction_slider.disabled = False

    toggle.observe(custom_preset, names="value")
    local_weather.observe(loc_weather, names="value")

    graph_output = interactive_output(
        update_graph,
        {
            "toggle_value": toggle,
            "club": club_dropdown,
            "ball": ball_dropdown,
            "speed": club_speed_slider,
            "angle": launch_angle_slider,
            "spin_x": spin_x_slider,
            "spin_y": spin_y_slider,
            "spin_z": spin_z_slider,
            "wind_speed": wind_slider,
            "wind_direction": wind_direction_slider,
            "temperature": temparature_slider,
            "pressure": pressure_slider,
            "local_weather": local_weather,
            "city_dropdown": city_dropdown,
        },
    )

    inputs = VBox([sliders])
    x_z_plot = VBox([graph_output])
    display(HBox([inputs, x_z_plot]))
