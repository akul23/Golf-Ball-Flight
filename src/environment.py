# Module imports
import numpy as np
import requests
import json

# Script imports
from . import UI

# Define global constants
Suther = 120  # Sutherland's constant
u_0 = 0.01724  # Reference viscosity
T_0 = 273.15  # Referenčna temperature
R = 287  # Specific gas constant for air
api_key = "40d40b0b15d847bc93783410231912"


def get_local_weather_data(loc="Ljubljana"):
    loc = UI.city_dropdown.value
    data = json.loads(
        requests.get(
            f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={loc}&aqi=no"
        ).text
    )
    return [
        data["current"]["temp_c"],
        data["current"]["pressure_mb"] / 1000,
        data["current"]["wind_kph"] / 3.6,
        data["current"]["wind_degree"],
    ]


def calculate_viscosity():
    """Calculates viscosity for custum UI values"""
    if UI.local_weather.value:
        data = get_local_weather_data()[0]
    else:
        data = UI.temparature_slider.value  # Calls UI values
    temp = data + T_0  # Extracts temperature value and converts to Kelvin
    viscosity = (  # Sutherlands formula, inaccurate at low pressures
        u_0 * (temp / T_0) ** 1.5 * ((0.555 * T_0 + Suther) / (0.555 * temp + Suther))
    )
    return viscosity / 1000  # Conversion form cP to Pas


def calculate_density():
    """Calculates density for UI values"""
    if UI.user_interface(get_value=True)[12].value:
        data = get_local_weather_data()[:2]
    else:
        data = [
            UI.temparature_slider.value,
            UI.pressure_slider.value,
        ]  # Calls UI values
    temp = data[0] + T_0  # Extracts temperature value and converts to Kelvin
    pressure = data[1] * 100000  # Extracts pressure value and converts to Pa

    return pressure / (R * temp)  # Returns density by the ideal gas law


def prepare_wind_vector():
    """
    Returns vector in form [x_wind_velocity, y_wind_velocity, 0]
    """

    if UI.local_weather.value:
        a = get_local_weather_data()[2:]
    else:
        a = [UI.wind_slider.value, UI.wind_direction_slider.value]  # Calls UI values
    return np.round(
        [a[0] * np.cos(np.radians(a[1])), a[0] * np.sin(np.radians(a[1])), 0], 2
    )
