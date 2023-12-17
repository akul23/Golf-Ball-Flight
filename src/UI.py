from ipywidgets import Checkbox, VBox, Dropdown, FloatSlider, Layout, IntSlider

width = "400px"  # Slider width
description_width = "200px"  # Label width

#############ENVIRONMENT WIDGETS##############
wind_slider = IntSlider(
    value=0,
    min=0,
    max=20,
    step=1,
    description="Hitrost vetra [m/s]",
    readout=True,
    style={"description_width": "initial", "description_width": description_width},
    layout=Layout(width=width),
)
wind_direction_slider = IntSlider(
    value=0,
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

#############/ENVIRONMENT WIDGETS##############
#############CLUB BALL WIDGETS##############
club_dropdown = Dropdown(options=["driver", "3_wood", "5_wood", "3_iron", "4_iron", "5_iron", "6_iron", "7_iron", "8_iron", "9_iron", "PW"])

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
    min=-400,
    max=400,
    step=1,
    description="Vrtljaji okoli x osi [RPM]",
    readout=True,
    style={"description_width": "initial", "description_width": description_width},
    layout=Layout(width=width),
)
spin_y_slider = IntSlider(
    value=-200,
    min=-200,
    max=200,
    step=1,
    description="Vrtljaji okoli y osi [RPM]",
    readout=True,
    style={"description_width": "initial", "description_width": description_width},
    layout=Layout(width=width),
)
spin_z_slider = IntSlider(
    value=0,
    min=-200,
    max=200,
    step=1,
    description="Vrtljaji okoli z osi [RPM]",
    readout=True,
    style={"description_width": "initial", "description_width": description_width},
    layout=Layout(width=width),
)
toggle = Checkbox(
        value=True,
        description="Uporabi Pre-set parametre"
    )  # Checkbox for preset hide/show
#############/CLUB BALL WIDGETS##############


def user_interface_club_ball(get_value=False):
    """
    User interface for club/ball data

    Keyword arguments:
    get_data -- return data or display UI (default False)
    """
    preset = VBox(children=[club_dropdown, ball_dropdown])  # VBox for the preset option

    def custom_preset(x):
        """Adjusts VBox to preset/custom inputs"""
        if x.get("new"):
            preset.children = [club_dropdown, ball_dropdown]  # Preset inputs
        else:
            preset.children = [  # Custom inputs
                ball_dropdown,
                club_speed_slider,
                launch_angle_slider,
                spin_x_slider,
                spin_y_slider,
                spin_z_slider,
            ]

    toggle.observe(
        custom_preset, names="value"
    )  # Calls custom_preset(toggle.value) when value changes

    # Only returns values of the selected menu (preset/custom), first element is for identifying which menu the function returns
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
        ]
    # displays VBox and preset/custom checkbox
    else:
        display(toggle)
        display(preset)


def user_interface_environment(get_value=False):
    """
    User interface for environmental data

    Keyword arguments:
    get_value -- return data or display UI (default False), bool
    """
    if get_value:
        return [
            wind_slider.value,
            wind_direction_slider.value,
            temparature_slider.value,
            pressure_slider.value,
        ]
    else:
        display(temparature_slider, pressure_slider, wind_slider, wind_direction_slider)
