from . import UI
import numpy as np

Suther = 120  # Sutherland's constant
u_0 = 0.01724  # Reference viscosity
T_0 = 273.15  # Referenčna temperature


def calculate_viscosity():
    """Calculates viscosity for UI values"""
    data = UI.user_interface_environment(get_value=True)  # Calls UI values
    temp = data[2] + T_0  # Extracts temperature value and converts to Kelvin
    viscosity = (  # Sutherlands formula, inaccurate at low pressures
        u_0 * (temp / T_0) ** 1.5 * ((0.555 * T_0 + Suther) / (0.555 * temp + Suther))
    )
    return viscosity / 1000  # Conversion form cP to Pas


def calculate_density():
    """Calculates density for UI values"""
    data = UI.user_interface_environment(get_value=True)  # Calls UI values
    temp = data[2] + T_0  # Extracts temperature value and converts to Kelvin
    pressure = data[3] * 100000  # Extracts pressure value and converts to Pa
    R = 287  # Specific gas constant for air

    return pressure / (R * temp)  # Returns density by the ideal gas law

def prepare_wind_vector():
    a = UI.user_interface_environment(get_value=True)[:2] # Calls UI values
    return np.round([a[0] * np.cos(np.radians(a[1])), a[0] * np.sin(np.radians(a[1])), 0], 2)

