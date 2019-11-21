from copy import deepcopy
import numpy as np

from features import *

features_dict = {
            'min_discharge_voltagem': min_discharge_voltage_measured,
            'min_discharge_voltagec': min_discharge_voltage_charge,
            'max_charge_temp': timeofmax_charge_temperature,
            'max_discharge_temp': timeofmax_discharge_temperature,
            'previous_capacity': prev_capacitance}

def get_data(features=['min_discharge_voltagem', 'min_discharge_voltagec', 'max_discharge_temp', 'previous_capacity'], caps=1, split=True):    
    print('[*]Loading feature data')
    X = get_feature_data(features, caps)

    print('[*]Loading target data')
    Y = get_capacitance()

    Y = [y[caps-1:] for y in Y]

    print('[*]Removing outliers')
    X, Y = remove_outliers(X, Y)

    print("X samples:", len(np.concatenate(X, axis=0)))
    print("Y samples:", len(np.concatenate(Y, axis=0)))

    #split training and test set
    if split: return split_data(X, Y)
    else: return X, Y

def get_feature_data(features, caps=1):
    if isinstance(features, str): features = [features]

    if features == ['all']: features = features_dict.values()
    else: features = [features_dict[f] for f in features]

    x = []

    for bat in list_bat_nums():
        temp = []
        for f in features:
            if f == prev_capacitance: f(temp, battery=bat, l=caps)
            else: temp.append(f(battery=bat)[0][caps-1:])

        #Overly complicated matrix initialization
        bat = [x[:] for x in [[0] * (len(temp))] * min([len(t) for t in temp])]

        for i, t in enumerate(temp):
            for i2, t2 in enumerate(t):
                if i2 > len(bat)-1: break
                else: bat[i2][i] = round(t2, 5)

        x.append(np.array(bat, np.float64))

    return np.array(x, dtype=object)

def insert_cycles(X, pos=0):
    new_X = []

    for bat in X:
        temp = []
        cycles = range(len(bat)-1)

        for x, c in zip(bat, cycles):
            if not isinstance(x, (list, np.ndarray)): x = [x]

            temp.append(np.insert(x, pos, c))

        new_X.append(np.array(temp))

    return new_X


def split_data(X, Y, test_size=0.2):
    return train_test_split(X, Y, test_size=test_size)

def elementwise_concatenate(x, y):
    out = []

    for x1, y1 in zip(x, y):
        temp = []
        for x2, y2 in zip(x1, y1):
            if not isinstance(x2, (list, np.ndarray)): x2 = [x2]
            if not isinstance(y2, (list, np.ndarray)): y2 = [y2]

            temp = x2 + y2
        out.append(temp)

    return np.array(out)


def remove_outliers(X, Y):
    new_X = deepcopy(X)
    new_Y = deepcopy(Y)
    
    for i, batx, baty in zip(range(len(X)), X, Y):
        offset = 0

        q1 = np.percentile(baty, 25)
        q3 = np.percentile(baty, 75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        for i2, y in enumerate(baty):
            if (y < lower_bound or y > upper_bound):
                new_X[i] = np.delete(new_X[i], [i2 - offset], axis=0)
                new_Y[i] = np.delete(new_Y[i], [i2 - offset], axis=0)
                offset += 1
                
    return new_X, new_Y
    