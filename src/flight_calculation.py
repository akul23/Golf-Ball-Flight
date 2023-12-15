# Module imports
import numpy as np
import sympy as sym
import scipy as sci

# Script imports
from . import ball, environment, UI


def define_constants():
    """
    Defines constants used by functions in this script, requires access to environment.py, ball.py and UI.py
    """
    global A
    global rho
    global mu
    global gravity
    global d
    global w
    global wind
    global m_e

    A = (
        ball.ball_properties.get("diameter") / 2
    ) ** 2 * np.pi  # Projected area of ball
    rho = np.round(environment.calculate_density(), 2)  # Air density
    mu = environment.calculate_viscosity()  # Air viscosity
    gravity = np.array([0, 0, -9.81])  # Gravity vector
    d = ball.ball_properties.get("diameter")  # Ball diameter
    wind = environment.prepare_wind_vector()  # Wind vector
    m_e = magnus_equation()  # Defines numerical magnus function
    
    if UI.user_interface_club_ball(get_value=True)[0]: # Check for use of preset
        w = ball.get_club_data(UI.user_interface_club_ball(get_value=True)[1])[:3] # Spin rate in rad/s
    else:
        w = UI.user_interface_club_ball(get_value=True)[5:]  # Spin rate in rad/s


def magnus_equation():
    """
    Prepares the numerial function for magnus force calculation
    """
    # Define symbols
    rho_s, r_s, r_1_s = sym.symbols("rho, r r_1", positive=True) 
    w_s = sym.Matrix(sym.MatrixSymbol("w", 3, 1))
    v = sym.Matrix(sym.MatrixSymbol("v", 3, 1))
    # Equations
    A_1 = sym.pi * r_1_s**2
    A_k = sym.pi * r_s**2 - A_1
    r_1 = sym.solve(sym.Eq(A_1, A_k), r_1_s, positive=True)
    F = 2 * rho * r_1[0] ** 2 * r_s * sym.pi * w_s.cross(v)
    # Insert flight constants
    F = F.subs({w_s[0]: w[0], w_s[1]: w[1], w_s[2]: w[2], rho_s: rho, r_s: d / 2})
    return sym.lambdify(v, F, "numpy") # returns numerical function for specific flight, taking velocity as a variable


def calculate_reynolds(velocity):
    """
    Calculates reynolds number at given viscosity

    Keyword arguments:
    velocity -- velocity vector at which the ball is travelling, list.shape(3,1)
    """
    return np.round(rho * np.abs(velocity) * d / mu)


def calculate_drag_force(velocity, c_d_function):
    """
    Calculates drag force of the ball at given velocity with the given drag coefficient function

    Keyword arguments:
    velocity -- velocity vector at which the ball is travelling, list.shape(3,1)
    c_d_function -- drag coefficient function, func
    """
    Re = calculate_reynolds(velocity)  # Caluclates reynolds number
    C_d = np.round(c_d_function(Re), 2)  # Gets corresponding drag coefficient
    i = np.sign(velocity)  # Sign mask to reverse drag force when falling

    return np.round(-0.5 * C_d * rho * A * velocity**2 * i, 2)


def calculate_wind_force():
    """
    Calculates force wind applys to ball
    """
    mask = np.sign(wind) # Sign mask, sign gets lost due to squaring

    return np.round(mask * 0.5 * rho * wind**2 * A, 2)


def calculate_magnus_force(velocity):
    """
    Calculates the magnus force

    Keyword arguments:
    velocity -- velocity vector at which the ball is travelling, list.shape(3,1)
    """
    return np.round(np.ravel(m_e(velocity[0], velocity[1], velocity[2])), 2)


def calculate_dynamics(v, t, c_d_function, x):
    """
    Calculate ball flight dynamics, returns [:3] velocity at each time point, [3:] location at each time point

    Keyword arguments:
    v -- veelocity at given time, list.shape(3,1)
    t -- time points, list.shape(0,n)
    c_d_function -- drag coefficient function, func
    x -- dummy, odeit glitch?
    """
    v = v[:3] # Extract velocity slice

    # Calculate forces
    F_w = calculate_wind_force()
    F_d = calculate_drag_force(v, c_d_function)
    F_m = calculate_magnus_force(v)

    # Prepare to return first and second order results in form [ v_x, v_y, v_z, x, y, z]
    out = np.zeros(6)
    out[:3] = (F_w + F_d + F_m) / ball.ball_properties.get("mass") + gravity
    out[3:] = v
    return out


def analize_flight(flight_data, n):
    """
    analizes flight and returns flight details in form [x_distance, max_height, flight_time, curve distance]

    Keyword arguments:
    flight_data -- x, y, z velocity and position values
    n -- time of flight evaluation, int
    """
    #TODO 3D interpolated function
    flight_x_z = sci.interpolate.interp1d(
        flight_data[:, 3], flight_data[:, 5]
    )  # Flight x z function

    flight_x_y = sci.interpolate.interp1d(
        flight_data[:, 3], flight_data[:, 4]
    )  # Flight x y function

    #TODO optimize root search, newton method
    z_0 = sci.optimize.bisect(flight_x_z, 1, flight_data[:, 3][-100])  # X of touchdown

    curve = flight_x_y(z_0)  # Curve amplitude

    z_max = sci.ndimage.maximum(flight_data[:, 5])  # Maximum of flight

    # Flight time
    length_s = np.shape(flight_data[:, 3])[0] / n  # Datapoints per second
    closest_value = min(
        flight_data[:, 3], key=lambda x: abs(z_0 - x)
    )  # Find the closest x value in array to touchdown
    closest_value_index = np.where(
        closest_value == flight_data[:, 3]
    )  # Find the index of the closest value
    f_time = closest_value_index[0][0] / length_s  # Time till touchdown aka flight time

    return np.round(np.array([z_0, z_max, f_time, curve]), 2)


def calculate_trajectory(c_d_function, t_points=np.linspace(0, 6, 1000)):
    """
    Calculate ball flight trajectory

    Keyword arguments:
    c_d_function -- drag coefficient function, func
    t_points -- time points (default np.linspace(0, 8, 1000))
    """
    define_constants() # Prepare constants for specific flight
    v_0 = np.zeros(6)
    v_0[:3] = ball.prepare_ball_initial_velocity_vector()
    v_t = sci.integrate.odeint(
        calculate_dynamics, v_0, t_points, args=(c_d_function, 1)
    ) # Solve system of differential equations
    return v_t
