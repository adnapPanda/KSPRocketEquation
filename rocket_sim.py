import math
import matplotlib.pyplot as plt

mass_at_launch = 6.6 * 1000
mass_after_burn = 2.6 * 1000
burn_time = 51
asl_thrust = 205.53 * 1000
vac_thrust = 211 * 1000
launch_pad_y = 75

diameter = 1.3
rocket_radius = diameter / 2

fuel_mass = mass_at_launch - mass_after_burn  # weight of fuel
mass_loss = fuel_mass / burn_time  # mass loss rate

pos_y_list = []
drag_force_list = []
accel_list = []
velocity_list = []

dt = 1/1000
drag_coeff = 0.07

# Air density constants
sea_level_pressure = 101325  # sea level standard atmospheric pressure measured in Pa
sea_level_temp = 288.15  # sea level standard temp measure in K
grav_accel = 9.8  # earth surface gravitaional accel measured in m/s
temp_lapse_rate = 0.0065  # measure in K/m
gas_constant = 8.31447  # ideal universal gas constant measured in J/(mol K)
molar_mass_air = 0.0289654  # molar mass of dry air measured in kg/mol
cross_section = math.pi * rocket_radius**2
iterations = int((10 * (burn_time / dt)) + 1)
kerbin_atm_cutoff = 44000

planet_gravity = 9.8  # TODO param


def get_air_density_old(current_height):
    if current_height < kerbin_atm_cutoff:
        temp_at_alt = sea_level_temp - temp_lapse_rate*current_height  # calcs temp at altitude
        pressure_at_alt = sea_level_pressure*(1 - (temp_lapse_rate*current_height)/sea_level_temp)**((grav_accel*molar_mass_air)/(gas_constant*temp_lapse_rate)) #calcs pressure at altitude
        return (pressure_at_alt*molar_mass_air) / (gas_constant*temp_at_alt)
    else:
        return 0


def get_thrust(asl_t, vac_t, h):
    return min(vac_t, ((h / kerbin_atm_cutoff) * (vac_t - asl_t)) + asl_t)


# TODO turn to class at some point?
def velocity_of_rocket():
    pos_y = launch_pad_y
    velocity = 0

    pos_y_list.append(pos_y)
    drag_force_list.append(0)
    velocity_list.append(velocity)

    mass = mass_at_launch
    thrust = get_thrust(asl_thrust, vac_thrust, pos_y)

    for i in range(iterations):
        drag_force = 0.5 * get_air_density_old(pos_y) * velocity**2 * drag_coeff * cross_section

        if velocity >= 0:
            resultant_force = thrust - ((mass * planet_gravity) + drag_force)
        else:
            resultant_force = drag_force - (mass * planet_gravity)

        accel = resultant_force / mass

        velocity = velocity + (accel * dt)
        pos_y = pos_y + (velocity * dt)

        if i >= (burn_time / dt):
            thrust = 0
            mass = mass_after_burn
        else:
            thrust = get_thrust(asl_thrust, vac_thrust, pos_y)
            mass = mass - (mass_loss * dt)

        pos_y_list.append(pos_y)
        drag_force_list.append(drag_force)
        accel_list.append(accel)
        velocity_list.append(velocity)


def earth():  # calculation for earth
    velocity_of_rocket()
    #print(pos_y_list)  # TODO fix! global var?
    plt.plot(range(iterations + 1), pos_y_list)
    #plt.plot(range(iterations), accel_list)
    #plt.plot(range(iterations + 1), velocity_list)
    #plt.plot(range(iterations + 1), drag_force_list)
    plt.show()

earth()
