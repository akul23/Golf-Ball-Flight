# Module imports
import numpy as np
import sympy as sym
from scipy import interpolate, optimize, integrate
import matplotlib.pyplot as plt

# Script imports
from . import ball, environment, UI


def define_constants():
    """Defines constants used by functions in this script, requires access to environment.py, ball.py and UI.py"""
    global A
    global rho
    global mu
    global gravity
    global d
    global w
    global wind
    global m_e
    global c_d_function

    A = (
        ball.ball_properties.get("diameter") / 2
    ) ** 2 * np.pi  # Projected area of ball
    rho = np.round(environment.calculate_density(), 2)  # Air density
    mu = environment.calculate_viscosity()  # Air viscosity
    gravity = np.array([0, 0, -9.81])  # Gravity vector
    d = ball.ball_properties.get("diameter")  # Ball diameter
    wind = environment.prepare_wind_vector()  # Wind vector

    if UI.toggle.value:  # Check for use of preset
        w = -ball.get_club_data(UI.club_dropdown.value)[:3]  # Spin rate in rad/s
    else:
        w = [
            UI.spin_x_slider.value,
            UI.spin_y_slider.value,
            UI.spin_z_slider.value,
        ]  # Spin rate in rad/s

    c_d_function = ball.c_d_re_interpolation(UI.ball_dropdown.value)

    m_e = magnus_equation()  # Defines numerical magnus function


def magnus_equation():
    """Prepares the numerial function for magnus force calculation

    Returns:
        np.func: numerical function for magnus force
    """
    # Define symbols
    rho_s, r_s, r_1_s = sym.symbols("rho, r r_1", positive=True)
    w_s = sym.Matrix(sym.MatrixSymbol("w", 3, 1))
    v = sym.Matrix(sym.MatrixSymbol("v", 3, 1))
    # Equations
    A_1 = sym.pi * r_1_s**2
    A_k = sym.pi * r_s**2 - A_1
    r_1 = sym.solve(sym.Eq(A_1, A_k), r_1_s, positive=True)
    F =  rho * r_1[0] ** 2 * r_s * sym.pi * w_s.cross(v)
    # Insert flight constants
    F = F.subs({w_s[0]: w[0], w_s[1]: w[1], w_s[2]: w[2], rho_s: rho, r_s: d / 2})
    return sym.lambdify(
        v, F, "numpy"
    )  # returns numerical function for specific flight, taking velocity as a variable


def calculate_reynolds(velocity):
    """Calculates reynolds number at given viscosity

    Args:
        velocity (list): in form [v_x, v_y, v_z]

    Returns:
        list: in form [Re_x, Re_y, Re_z]
    """
    return np.round(rho * np.abs(velocity) * d / mu)


def calculate_drag_force(velocity):
    """Calculates drag force of the ball at given velocity with the given drag coefficient function

    Args:
        velocity (list): in form [v_x, v_y, v_z]

    Returns:
        list: in form [F_x, F_y, F_z]
    """
    Re = calculate_reynolds(velocity)  # Caluclates reynolds number
    C_d = np.round(c_d_function(Re), 2)  # Gets corresponding drag coefficient
    i = np.sign(velocity)
    return np.round(-0.5 * C_d * rho * A * velocity**2 * i, 2)


def calculate_wind_force():
    """Calculates force wind applys to ball

    Returns:
        list: in form [F_x, F_y, F_z]
    """
    mask = np.sign(wind)  # Sign mask, sign gets lost due to squaring

    return np.round(mask * 0.5 * rho * wind**2 * A, 2)


def calculate_magnus_force(velocity):
    """Calculates the magnus force

    Args:
        velocity (list): in form [v_x, v_y, v_z]

    Returns:
        list: in form [F_x, F_y, F_z]
    """
    slip_factor = 1  # Slip factor, 1 -> not used
    return np.round(
        np.ravel(m_e(velocity[0], velocity[1], velocity[2]) * slip_factor), 2
    )


def calculate_dynamics(t, v):
    """Calculate ball flight dynamics

    Args:
        t (tuple): in form (t_min, t_max), observation range
        v (list): in form [v_x, v_y, v_z, x, y, z]

    Returns:
        list: [v_x, v_y, v_z, x, y, z]
    """
    v = v[:3]  # Extract velocity slice

    # Calculate forces
    F_w = calculate_wind_force()
    F_d = calculate_drag_force(v)
    F_m = calculate_magnus_force(v)

    # Prepare to return first and second order results in form [ v_x, v_y, v_z, x, y, z]
    out = np.zeros(6)
    out[:3] = (F_w + F_d + F_m) / ball.ball_properties.get("mass") + gravity
    out[3:] = v
    return out


def create_coord_functions(data, n, t):
    """Creates interpolated functions of x, y and z coordinates with respect to time

    Args:
        data (list): flight data as returned by "calculate trajectory"
        n (int): size of observation range
        t (int): amount of time points

    Returns:
        tuple: tuple of functions in form (t_x, t_y, t_z)
    """
    t_int = np.linspace(0, n, t)

    t_x = interpolate.interp1d(t_int, data[0])
    t_y = interpolate.interp1d(t_int, data[1])
    t_z = interpolate.interp1d(t_int, data[2])

    return t_x, t_y, t_z


def path_length(data, n, t_d, t):
    """Calculates path length of balls arc

    Args:
        data (list): flight data as returned by "calculate trajectory"
        n (int): size of observation range
        t_d (int): time of flight
        t (int): amount of time points

    Returns:
        _type_: _description_
    """
    v_x, v_y, v_z = create_coord_functions(data, n, t)
    t_int = np.linspace(0, t_d, t)
    mag = (v_x(t_int) ** 2 + v_y(t_int) ** 2 + v_z(t_int) ** 2) ** 0.5

    return integrate.simpson(mag, t_int, even="avg")


def analize_flight(flight_data, n):
    """Analizes flight and returns flight details in form [x_distance, max_height, flight_time, curve distance]

    Args:
        flight_data (list): flight data as returned by "calculate trajectory"
        n (int): end of observation interval

    Returns:
        list: in form [x_distance, y_distance, apex, flight_path_length, flight_time, t_point_z_0]
    """
    t = len(flight_data[0])

    t_x, t_y, t_z = create_coord_functions(flight_data[3:], n, t)

    try:
        flight_time = optimize.newton(t_z, n - 1)
    except:
        raise ("Check observation range, does the ball reach the ground?")

    x_distance = np.round(t_x(flight_time), 2)
    y_distance = np.round(t_y(flight_time), 2)
    apex = np.round(np.max(flight_data[5]), 2)
    flight_path_length = np.round(
        path_length(flight_data[:3], n, int(np.ceil(flight_time)), t), 2
    )
    t_point_z_0 = np.abs(flight_data[3] - x_distance).argmin()

    return [x_distance, y_distance, apex, flight_path_length, flight_time, t_point_z_0]


def calculate_trajectory(n=15, res=50, plot_graph=False):
    """Calculate ball flight trajectory

    Args:
        n (int, optional):time interval for which to solve. Defaults to 15.
        res (int, optional): time points per second. Defaults to 50.
        plot_graph (bool, optional): plot position graph insted of return values. Defaults to False.

    Returns:
        list: velocity_x, velocity_y, velocity_z, position_x, position_y, position_z
    """
    define_constants()  # Prepare constants for specific flight
    v_0 = np.zeros(6)
    v_0[:3] = ball.prepare_ball_initial_velocity_vector()
    t_points = np.linspace(0, n, n * res)

    v_t = integrate.solve_ivp(calculate_dynamics, (0, n), v_0, t_eval=t_points)

    if plot_graph:
        data = analize_flight(v_t.y, n)

        fig, axs = plt.subplots(1, 2, figsize=(12, 4))
        axs[0].plot(v_t.y[3], v_t.y[5], "g")
        axs[0].set_xlabel(f"dolžina leta {data[0]}m")
        axs[0].set_ylabel(f"višina leta {data[2]}m")
        axs[0].set_xlim(0, data[0] + 20)
        axs[0].set_ylim(0, data[2] + 20)

        axs[1].plot(v_t.y[3], v_t.y[4], "r")
        axs[1].set_xlabel(f"dolžina leta {data[0]}m")
        axs[1].set_ylabel(f"zavoj leta {data[1]}m")
        axs[1].set_xlim(0, data[0])
        axs[1].set_ylim(-data[1] - 1, data[1] + 1)
    else:
        return v_t.y
