# Module import
import numpy as np
import pandas as pd
from scipy import interpolate
import os

# Script imports
from . import UI

ball_properties = {
    "mass": 0.04593,  # Golf ball weight in Kg
    "diameter": 0.0426,  # Golf ball diameter in m
}


def get_club_data(club):
    """Reads club data from /Data/clubs.csv

    Args:
        club (str): club name, " " replaced with "_"

    Returns:
        list: in form [x_spin, y_spin, z_spin, abs_velocity, launch angle]
    """
    club_data = np.array(  # Opens file and read the desired columns
        pd.read_csv(
            os.getcwd() + "\Data\clubs.csv",
            usecols=["velocity_" + club, "spin_" + club],
        )
    )

    return club_data.flatten("F")


def read_ball_data(ball_type="Calloway"):
    """_Reads golf ball drag data from Data\C_d-Re.csv

    Args:
        ball_type (str, optional): ball name. Defaults to "Calloway".

    Returns:
        list: in form [[Re, C_d]]
    """
    C_d_Re_data = np.array(  # Opens file and read the desired columns
        pd.read_csv(
            os.getcwd() + "\Data\C_d-Re.csv",
            usecols=["Re_" + ball_type, "C_d_" + ball_type],
        )
    )
    return C_d_Re_data


def c_d_re_interpolation(ball_type="Calloway"):
    """Interpolates drag data for selected ball

    Args:
        ball_type (str, optional): _description_. Defaults to "Calloway".

    Returns:
        func: scipy.function
    """
    data = read_ball_data(ball_type)  # Calls for ball data

    # Preparing data
    re_data = data[:, 0]
    c_d_data = data[:, 1]

    # Interpolation
    spline = interpolate.InterpolatedUnivariateSpline(re_data, c_d_data)

    return spline


def prepare_ball_initial_velocity_vector():
    """initial_velocity vector of ball given the launch angle, assuming no sideway (y) velocity

    Returns:
        list: in form [v_x, v_y, v_z]
    """
    if UI.toggle.value:  # Check for use of preset
        data = get_club_data(UI.club_dropdown.value)[
            3:5
        ]  # [abs_velocity, launch angle], from club data
        return np.round(
            np.array(
                [
                    data[0] * np.cos(np.radians(data[1])),
                    0,
                    data[0] * np.sin(np.radians(data[1])),
                ]
            ),
            2,
        )
    else:
        data = [
            UI.club_speed_slider.value,
            UI.launch_angle_slider.value,
        ]  # [abs_velocity, launch angle], from custom value user interface
        return np.round(
            np.array(
                [
                    data[0] * np.cos(np.radians(data[1])),
                    0,
                    data[0] * np.sin(np.radians(data[1])),
                ]
            ),
            2,
        )
