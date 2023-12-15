# Imports
import numpy as np
import pandas as pd
import scipy as sci
import os

from . import UI

ball_properties = {
    "mass": 0.04593,  # Golf ball weight in Kg
    "diameter": 0.0426,  # Golf ball diameter in m
}


def get_club_data(club):
    
    club_data = np.array(  # Opens file and read the desired columns
        pd.read_csv(
            os.getcwd() + "\Data\clubs.csv",
            usecols=["spin_" + club, "velocity_" + club],
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
    re_data = data[:, 0]  # Preparing data
    c_d_data = data[:, 1]

    # Interpolation
    spline = sci.interpolate.InterpolatedUnivariateSpline(
        re_data, c_d_data
    )  

    return spline


def prepare_ball_initial_velocity_vector():
    """
    Returns initial_velocity vector of ball given the launch angle
    """
    if UI.user_interface_club_ball(get_value=True)[0]:
        data = get_club_data(UI.user_interface_club_ball(get_value=True)[1])[3:]
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
        data = UI.user_interface_club_ball(get_value=True)[3:]
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
        

