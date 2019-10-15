import matplotlib.pyplot as plt


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