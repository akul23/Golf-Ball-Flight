# Module import
import numpy as np
import pandas as pd
import scipy as sci
import os

# Script imports
from . import UI

ball_properties = {
    "mass": 0.04593,  # Golf ball weight in Kg
    "diameter": 0.0426,  # Golf ball diameter in m
}


def get_club_data(club):
    """
    Returns vector in form [x_spin, y_spin, z_spin, abs_velocity, launch angle]

    Keyword arguments:
    club -- club name, " " replaced with "_", str
    """
    club_data = np.array(  # Opens file and read the desired columns
        pd.read_csv(
            os.getcwd() + "\Data\clubs.csv",
            usecols=[ "velocity_" + club, "spin_" + club]
        )
    )
    
    return club_data.flatten("F")


def read_ball_data(ball_type="Calloway"):
    """
    Reads golf ball drag data from Data\{balltype}

    Keyword arguments:
    ball_type -- select which ball data to return (default "Calloway"), str
    """
    C_d_Re_data = np.array(  # Opens file and read the desired columns
        pd.read_csv(
            os.getcwd() + "\Data\C_d-Re.csv",
            usecols=["Re_" + ball_type, "C_d_" + ball_type],
        )
    )
    return C_d_Re_data


def c_d_re_interpolation(ball_type="generic"):
    """
    Interpolates drag data for selected ball

    Keyword arguments:
    ball_type -- select which ball data to return (default "Calloway"), str
    """
    data = read_ball_data(ball_type)  # Calls for ball data
    
    # Preparing data
    re_data = data[:, 0]  
    c_d_data = data[:, 1]

    # Interpolation
    spline = sci.interpolate.InterpolatedUnivariateSpline(
        re_data, c_d_data
    )  

    return spline


def prepare_ball_initial_velocity_vector():
    """
    Returns initial_velocity vector of ball given the launch angle, assuming no sideway (y) velocity
    """
    if UI.user_interface(get_value=True)[0]: # Check for use of preset
        data = get_club_data(UI.user_interface(get_value=True)[1])[3:5] # [abs_velocity, launch angle], from club data
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
        data = UI.user_interface(get_value=True)[3:5] # [abs_velocity, launch angle], from custom value user interface
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
        

