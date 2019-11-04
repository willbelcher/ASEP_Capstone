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
        file = load_bat(n)
        e = extract(file)

        measures = e.of_type('discharge')
        temp = np.empty(len(measures))

        for i2, measure in enumerate(measures):
            temp[i2] = e.get_scalar_metrics_from_measure(measure, 'Capacity')

        data[i] = temp

    return data


#Time of min Voltage measured in discharge vs Capacity
def min_discharge_voltage_measured(battery=-1):
    if battery == -1:
        bat_nums = list_bat_nums()
    else:
        bat_nums = [battery]

    data = np.empty(len(bat_nums), dtype=np.object)

    for i, n in enumerate(bat_nums):
        file = load_bat(n)
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
        file = load_bat(n)
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
        file = load_bat(n)
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
        file = load_bat(n)
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
        file = load_bat(n)
        e = extract(file)

        measures = e.of_type('charge', ['Temperature_measured', 'Time'])
        temp = np.empty(len(measures))

        for i2, measure in enumerate(measures):
            ind = np.argmax(measure[0][1:])
            temp[i2] = measure[1][ind]

        data[i] = temp

    return data


features_dict = {
            'min_discharge_voltagem': min_discharge_voltage_measured,
            'min_discharge_voltagec': min_discharge_voltage_charge,
            'max_charge_temp': timeofmax_charge_temperature,
            'max_discharge_temp': timeofmax_discharge_temperature}

def get_feature_data(features=['min_discharge_voltagem', 'min_discharge_voltagec', 'max_charge_temp']):
    if isinstance(features, str): features = [features]

    if features == ['all']: features = features_dict.values()
    else: features = [features_dict[f] for f in features]

    x = []

    for bat in list_bat_nums():
        temp = []
        for f in features:
            temp.append(f(battery=bat))

        #Overly complicated matrix initialization
        bat = [x[:] for x in [[0] * len(features)] * min([len(t[0]) for t in temp])]

        for i, t in enumerate(temp):
            for i2, t2 in enumerate(t[0]):
                if i2 > len(bat)-1: break
                else: bat[i2][i] = round(t2, 2)

        x.append(bat)

    return x


def split_data(X, Y, test_size=0.2):
    return train_test_split(X, Y, test_size=test_size)

    
        