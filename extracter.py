import numpy as np
from os import listdir

charge_metrics = ["Voltage_measured", "Current_measured", "Temperature_measured", "Current_charge", "Voltage_charge", "Time"]
discharge_metrics = ["Voltage_measured", "Current_measured", "Temperature_measured", "Current_charge", "Voltage_charge", "Time"] #Capacity is scalar
impedance_metrics = ["Sense_current", "Battery_current", "Current_ratio", "Battery_impedance", "Rectified_impedance"] #Re and Rct are scalar
metric_dict = {'charge': charge_metrics, 'discharge': discharge_metrics, 'impedance': impedance_metrics}

charge_scalar = []
discharge_scalar = ['Capacity']
impedance_scalar = ['Re', 'Rct']
measurement_dict = {'charge': charge_scalar, 'discharge': discharge_scalar, 'impedance': impedance_scalar}

measurement_info = ['Ambient_temperature', 'Date']

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


class extract():

    prev_capacities = [0, 0]

    def __init__(self, data):
        self.data = data

    #Searches all data of a given type (charge, discharge) from a battery file
    #and returns it
    def of_type(self, dat_type, metrics='all', num=-1):
        out = []
        counter = 0

        if isinstance(dat_type, str):
            dat_type = [dat_type]

        for measure in self.data:
            if measure[0] in dat_type: #checks if measurement is type of data type
                if metrics == 'all':
                    out.append(measure)
                else:
                    out.append(self.get_metrics_from_measure(measure, metrics=metrics))

                counter += 1

                if counter == num:
                    break

        return out

    def get_measurement_info(self, dat_type='all', metrics='all', num=-1): #TODO
        out = []
            
        if isinstance(metrics, str) and metrics != 'all':
            metrics = [metrics]

        if isinstance(dat_type, str) and dat_type != 'all':
            dat_type = [dat_type] 

        if metrics == 'all':
            metrics = measurement_info

        counter = 0

        for measure in self.data:
            temp = []

            if measure[0] in dat_type: #checks if measurement is type of data type
                
                if 'Date' in metrics:
                    temp.append(measure[2])

                if 'Ambient_temperature' in metrics:
                    temp.append(measure[1])

                out.append(temp)

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

        #pos are the indices in measure that contain the
        #corresponding metrics
        #It probably isn't the most elegant way to do this...
        if metrics == 'all':
            pos = range(0, len(metric_map)-1)
        else:
            pos = [metric_map.index(met) for met in metrics]

        for ind in pos:
            out.append(measure[3][ind])

        return out

    def get_scalar_metrics_from_measure(self, measure, metrics='all'): 
        out = []
        
        if isinstance(metrics, str) and metrics != 'all':
            metrics = [metrics]

        dat_type = measure[0]

        if metrics == 'all':
            metrics = measurement_dict[dat_type]
        
        if dat_type == 'charge':
            return []
           
        if 'Capacity' in metrics: #dat_type is implicitly discharge
            temp = measure[3][6]

            if(isinstance(temp, np.ndarray)):
                return 0
            else: return temp

        if 'Re' in metrics:
            out.append(measure[3][5][0])
        if 'Rct' in metrics:
            out.append(measure[3][6][0])
            
        return out