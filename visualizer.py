from os import listdir

import matplotlib.pyplot as plt
import numpy as np


charge_metrics = ["Voltage_measured", "Current_measured", "Temperature_measured", "Current_charge", "Voltage_charge", "Time"]
discharge_metrics = ["Voltage_measured", "Current_measured", "Temperature_measured", "Current_charge", "Voltage_charge", "Time"] #Capacity is scalar
impedance_metrics = ["Sense_current", "Battery_current", "Current_ratio", "Battery_impedance", "Rectified_impedance", "Re", "Rct"]
metric_dict = {'charge': charge_metrics, 'discharge': discharge_metrics, 'impedance': impedance_metrics}

measurment_metrics = {''}

def load_bat(bat_num):
    if not isinstance(bat_num, str):
        bat_num = str(bat_num)

    filename = "B{}.npy".format(bat_num.rjust(4, '0'))
    file = np.load("Dataset_np/" + filename, allow_pickle=True)

    print("[*]Loaded: {} with {} entries".format(filename, len(file)))

    return file

def one_measurement(battery_num, dat_type, metric1, metric2='Time', max_measurements=-1):
    #Support for single and list types
    if isinstance(metric1, str):
        metric1 = [metric1]

    data = load_bat(battery_num)

    extr = extracter(data)
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

    def capacitance(battery_num):
        data = load_bat(battery_num)

        extr = extracter(data)


        
class extracter():

    def __init__(self, data):
        self.data = data

    #Searches all data of a given type (charge, discharge) from a battery file
    #and returns it
    def of_type(self, dat_type, num=-1, metrics='all'):
        out = []
        counter = 0

        if isinstance(dat_type, str):
            dat_type = [dat_type]

        for measure in self.data:
            if measure[0] in dat_type:
                if metrics == 'all':
                    out.append(measure)
                else:
                    out.append(self.get_metrics_from_measure(measure, metrics=metrics))

                counter += 1

                if counter == num:
                    break

        return out

    #Takes in one measurement and returns a list of the corresponding
    #metrics, eg. [Voltage measured, time]
    def get_metrics_from_measure(self, measure, metrics='all'):
        out = []
        
        if isinstance(metrics, str) and metrics != 'all':
            metrics = [metrics]

        dat_type = measure[0]
        metric_map = metric_dict[dat_type]

        #pos are the indecies in measure that contain the
        #corresponding metrics
        #It probably isn't the most elegant way to do this...
        if metrics == 'all':
            pos = range(0, len(metric_map)-1)
        else:
            pos = [metric_map.index(met) for met in metrics]

        for ind in pos:
            out.append(measure[3][ind])

        return out

    def get_measurement_info(self, dat_type, metrics='all', num=-1):
        out = []
            
        if isinstance(metrics, str) and metrics != 'all':
            metrics = [metrics]

        
    

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