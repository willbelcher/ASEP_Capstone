from extracter import *
from plot import plot


def one_measurement(battery_num, dat_type, metric1, metric2='Time', num=-1):
    #Support for string and list types
    if isinstance(metric1, str):
        metric1 = [metric1]

    data = load_bat(battery_num)
    extr = extract(data)
    measures = extr.of_type(dat_type, num=num, metrics='all')

    num_measurements = len(measures)

    for i, measure in enumerate(measures):
        if len(metric1) == 1:
            p = plot()
        else:
            p = plot(one_plot=False, num_plots=len(metric1))

        x = extr.get_metrics_from_measure(measure, metrics=metric2)[0]
        y = extr.get_metrics_from_measure(measure, metrics=metric1)

        for sub_y, m in zip(y, metric1):

            if dat_type == 'impedance':
                x = range(len(sub_y))
            
            p.plot_one_series(x, sub_y, '', scale=False, new_subplot=True)
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

    if metric2 == 'Cycles':
        x = range(num_measurements)
    elif metric2 == 'Date':
        x = dates
    else:
        print('[-]Pick Cycles or Date for metric2')
        return 

    y = [extr.get_scalar_metrics_from_measure(measure) for measure in measures]

    p = plot()
    p.plot_one_series(x, y, 'Capacity and {}'.format(metric2))
    p.label_axes(metric2, 'Capacity')

    print('Showing Capactity vs. {} : Battery {} : Entries {}'.format(metric2, battery_num, num_measurements))
    p.show_plot()
    p.close()
