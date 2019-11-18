from sklearn.model_selection import train_test_split
import numpy as np

from extracter import *
from plot import plot


def plot_all_bats(x, label):
    bat_nums = list_bat_nums()

    cap = get_capacitance()
    print()

    for x_bat, cap_bat, bat in zip(x, cap, bat_nums):
        p = plot()

        cap_len = len(cap_bat)
        x_len = len(x_bat)

        #Sometimes there will be more charge measurements than capacity measurements
        #Resizes arrays so they can be plotted
        if x_len == cap_len:
            pass
        elif x_len > cap_len:
            x_bat = x_bat[:cap_len]
        elif x_len < cap_len:
            cap_bat = cap_bat[:x_len]

        p.plot_one_series(cap_bat, x_bat, label='')
        p.label_axes("Capacity (Ah)", label)

        print('Showing Capactity vs. {} : Battery {} : Entries {}'.format(label, bat, len(x_bat)))  
        p.show_plot()
        p.close()


def get_capacitance():
    bat_nums = list_bat_nums()

    data = np.empty(len(bat_nums), dtype=np.object)

    for i, n in enumerate(bat_nums):
        file = load_bat(n, disp=False)
        e = extract(file)

        measures = e.of_type('discharge')
        temp = np.empty(len(measures))

        for i2, measure in enumerate(measures):
            temp[i2] = e.get_scalar_from_measure(measure, 'Capacity')

        data[i] = temp

    return data

def prev_capacitance(x, battery=-1, l=5):

    #There are faster ways to do this loop, creates offset list of capacities
    #I'm trying to turn a time series problem into a supervised one by feeding in previous capacities
    #along with previous battery capacities
    for offset in range(l):

        file = load_bat(battery, disp=False)
        e = extract(file)

        measures = e.of_type('discharge')[offset:]
        temp = np.empty(len(measures), dtype=np.float64)

        for i, measure in enumerate(measures):
            temp[i] = e.get_scalar_from_measure(measure, 'Capacity')

        x.append(temp)

    return x

#Time of min Voltage measured in discharge vs Capacity
def min_discharge_voltage_measured(battery=-1):
    if battery == -1:
        bat_nums = list_bat_nums()
    else:
        bat_nums = [battery]

    data = np.empty(len(bat_nums), dtype=np.object)

    for i, n in enumerate(bat_nums):
        file = load_bat(n, disp=False)
        e = extract(file)

        measures = e.of_type('discharge', ['Voltage_measured', 'Time'])
        temp = np.empty(len(measures))

        for i2, measure in enumerate(measures):
            ind = np.argmin(measure[0])
            temp[i2] = measure[1][ind]

        data[i] = temp

    return data

def min_discharge_voltage_charge(battery=-1):
    if battery == -1:
        bat_nums = list_bat_nums()
    else:
        bat_nums = [battery]

    data = np.empty(len(bat_nums), dtype=np.object)

    for i, n in enumerate(bat_nums):
        file = load_bat(n, disp=False)
        e = extract(file)

        measures = e.of_type('discharge', ['Voltage_charge', 'Time'])
        temp = np.empty(len(measures))

        for i2, measure in enumerate(measures):
            ind = np.argmin(measure[0][1:])
            temp[i2] = measure[1][ind]

        data[i] = temp

    return data

#Absolute max 
def absmax_charge_voltage_charge(battery=-1):
    if battery == -1:
        bat_nums = list_bat_nums()
    else:
        bat_nums = [battery]

    data = np.empty(len(bat_nums), dtype=np.object)

    for i, n in enumerate(bat_nums):
        file = load_bat(n, disp=False)
        e = extract(file)

        measures = e.of_type('charge', ['Voltage_charge', 'Time'])
        temp = np.empty(len(measures))

        for i2, measure in enumerate(measures):
            ind = np.argmax(measure[0][1:])
            temp[i2] = measure[1][ind]

        data[i] = temp

    return data

def timeofmax_discharge_temperature(battery=-1):
    if battery == -1:
        bat_nums = list_bat_nums()
    else:
        bat_nums = [battery]
    data = np.empty(len(bat_nums), dtype=np.object)

    for i, n in enumerate(bat_nums):
        file = load_bat(n, disp=False)
        e = extract(file)

        measures = e.of_type('discharge', ['Temperature_measured', 'Time'])
        temp = np.empty(len(measures))

        for i2, measure in enumerate(measures):
            ind = np.argmax(measure[0])
            temp[i2] = measure[1][ind]

        data[i] = temp

    return data

#Unusable
def timeofmax_charge_temperature(battery=-1):
    if battery == -1:
        bat_nums = list_bat_nums()
    else:
        bat_nums = [battery]

    data = np.empty(len(bat_nums), dtype=np.object)

    for i, n in enumerate(bat_nums):
        file = load_bat(n, disp=False)
        e = extract(file)

        measures = e.of_type('charge', ['Temperature_measured', 'Time'])
        temp = np.empty(len(measures))

        for i2, measure in enumerate(measures):
            ind = np.argmax(measure[0][1:])
            temp[i2] = measure[1][ind]

        data[i] = temp

    return data

