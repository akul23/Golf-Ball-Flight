# Module imports
import numpy as np

# Script imports
from . import UI

# Define global constants
Suther = 120  # Sutherland's constant
u_0 = 0.01724  # Reference viscosity
T_0 = 273.15  # Referenčna temperature
R = 287  # Specific gas constant for air


def calculate_viscosity():
    """Calculates viscosity for custum UI values"""
    data = UI.user_interface(get_value=True)[10]  # Calls UI values
    temp = data + T_0  # Extracts temperature value and converts to Kelvin
    viscosity = (  # Sutherlands formula, inaccurate at low pressures
        u_0 * (temp / T_0) ** 1.5 * ((0.555 * T_0 + Suther) / (0.555 * temp + Suther))
    )
    return viscosity / 1000  # Conversion form cP to Pas


def calculate_density():
    """Calculates density for UI values"""
    data = UI.user_interface(get_value=True)  # Calls UI values
    temp = data[10] + T_0  # Extracts temperature value and converts to Kelvin
    pressure = data[11] * 100000  # Extracts pressure value and converts to Pa

    return pressure / (R * temp)  # Returns density by the ideal gas law

def prepare_wind_vector():
    """
    Returns vector in form [x_wind_velocity, y_wind_velocity, 0]
    """
    a = UI.user_interface(get_value=True)[8:10] # Calls UI values
    return np.round([a[0] * np.cos(np.radians(a[1])), a[0] * np.sin(np.radians(a[1])), 0], 2)

