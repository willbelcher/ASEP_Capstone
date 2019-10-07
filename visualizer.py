from os import listdir

import matplotlib.pyplot as plt
import numpy as np

from extracter import extract

def load_bat(bat_num):
    if not isinstance(bat_num, str):
        bat_num = str(bat_num)

    filename = "B{}.npy".format(bat_num.rjust(4, '0'))
    file = np.load("Dataset_np/" + filename, allow_pickle=True)

    print("[*]Loaded: {} with {} entries".format(filename, len(file)))

    return file

def list_bat_nums(filepath='Dataset_np/'):
    files = listdir(filepath)

    #Ugly as this is, apparently it's the fastest way to strip the battery number
    #from the filename
    out = [int(filename.replace('.npy', '').replace('B0', '').replace('B00', '')) for filename in files]
    out.sort()

    return out


def one_measurement(battery_num, dat_type, metric1, metric2='Time', max_measurements=-1):
    #Support for string and list types
    if isinstance(metric1, str):
        metric1 = [metric1]

    data = load_bat(battery_num)

    extr = extract(data)
    measures = extr.of_type(dat_type, num=max_measurements, metrics='all')

    num_measurements = len(measures)

    for i, measure in enumerate(measures):
        if len(metric1) == 1:
            p = plot()
        else:
            p = plot(one_plot=False, num_plots=len(metric1))

        x = extr.get_metrics_from_measure(measure, metrics=metric2)

        for m in metric1:
            y = extr.get_metrics_from_measure(measure, metrics=m)

            p.plot_one_series(x[0], y[0], '', scale=False, new_subplot=True)
            p.label_axes(metric2, m)

        print("Showing entry {}/{}".format(i+1, num_measurements), end="\r", flush=True) 

        p.show_plot()
        p.close()

    print()

def plot_capacitance(battery_num, metric2='Date', max_measurements=-1): #fix for empty capacitance values
    data = load_bat(battery_num)

    extr = extract(data)
    dates = extr.get_measurement_info('discharge', metrics=metric2)

    measures = extr.of_type('discharge')

    num_measurements = len(measures)

    x = dates
    y = [extr.get_scalar_metrics_from_measure(measure) for measure in measures]

    p = plot()
    p.plot_one_series(x, y, 'Capacity and {}'.format(metric2))
    p.label_axes(metric2, 'Capacity')

    print('Showing Capactity vs. {} : Battery {} : Entries {}'.format(metric2, battery_num, num_measurements))
    p.show_plot()
    p.close()


class plot():

    def __init__(self, one_plot=True, num_plots=1):
        self.fig = plt.figure()
        self.subplot_info = [num_plots, 1, 1]
        if one_plot: self.ax = self.fig.add_subplot(1, 1, 1)

    def plot_one_series(self, x_data, y_data, label, scale=False, new_subplot=False):
        if new_subplot: self.new_subplot()
        if scale: plt.axis([min(x_data),
                            max(x_data),
                            min(y_data) + (min(y_data)/5),
                            max(y_data) + (max(y_data)/5)])

        self.ax.plot(x_data, y_data, label=label)

    def label_axes(self, x_label, y_label, label='none'):
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        if label is not 'none': plt.legend(loc='upper left')

    def new_subplot(self):
        self.ax = self.fig.add_subplot(self.subplot_info[0], self.subplot_info[1], self.subplot_info[2])

        self.subplot_info[2] += 1

    def show_plot(self):       
        plt.show()
    
    def close(self):
        subplot_info = [1,1,1]
        plt.close()