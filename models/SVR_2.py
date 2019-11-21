import numpy as np

from models.SVR import SVR_model
from process_data import get_data
from features import get_capacitance
from plot import plot

init_rmse = extrap_rmse = 0

def train(init_model, extrap_model):
    global init_rmse, extrap_rmse

    print('Initial SVR')
    init_model.fit(evaluate=False)
    init_rmse = init_model.predict(show_predictions=False)

    print('Second SVR')
    extrap_model.fit(evaluate=False)
    extrap_rmse = extrap_model.predict(show_predictions=False)

    return init_model, extrap_model

    
def predictions(init_model, extrap_model):
    offset = 7
    ix, iy = get_data(features=['min_discharge_voltagem', 'min_discharge_voltagec', 'max_discharge_temp'], caps=offset, split=False)
    ex, ey = get_data(features='previous_capacity', caps=offset, split=False)

    predictions = []
    actual = []

    print("[*]Predicting using both models...")
    for ixs, iys, exs, eys in zip(ix, iy, ex, ey):

        for off, [ixs_s, iys_s] in enumerate(zip(ixs, iys)):
            ip = init_model.model.predict(ixs_s)

            for exs_s, eys_s in zip(exs[off:], eys[off:]):
                predictions.append(extrap_model.model.predict(exs_s+[ip]))
                actual.append(eys_s)

    return actual, predictions
    
    rmse = np.sqrt(np.mean((predictions - actual) ** 2))

    print("Estimator evaluation:")
    print("RMSE - {}".format(round(rmse, 3)))

    input("Press Enter to continue") 

    p = plot()
    for bat in iy[:3]:
        [pred, predictions] = np.split(predictions, [len(bat)-1])
        p.plot_one_series(range(len(bat)), bat, '', style='-')
        p.plot_one_series(range(len(pred)), pred, '',  style='--')

        
        p.label_axes('Cycle', 'Capacity (Ahr)', "Predictions vs Actual")
        p.show_plot()
        p.close()


def save(model):
    while True:
        user = input("Would you like to specify a filename? y/n\n")

        if user == 'y':
            filename = input("Filename:\n")
            break
        elif user == 'n':
            filename = 'default'
            break

    model.save('saves/' + filename + '.sav')

def load(model):
    filename = input('Please enter filename\n')
    model.load('saves/' + filename + '.sav')

def run():
    x_train, x_test, y_train, y_test = get_data(features=['min_discharge_voltagem', 'min_discharge_voltagec', 'max_discharge_temp'])
    init_model = SVR_model(x_train, x_test, y_train, y_test)

    print()

    x_train, x_test, y_train, y_test = get_data(features='previous_capacity', caps=7)
    extrap_model = SVR_model(x_train, x_test, y_train, y_test)

    print("\n\033[4mSVR\033[0m")

    selected = [True] * 2
    while True:
        print('Selected\ninit_model: {}    extrap_model: {}\n'.format(selected[0], selected[1]))
        user = input("1. Train\n2. Predict\n3. Toggle selection\n4. Save\n5. Load\n6. Quit\n")
        
        if user == '1':
            init_model, extrap_model = train(init_model, extrap_model)
        elif user == '2':
            predictions(init_model, extrap_model)
        elif user == '3':
            choice = int(input('\nToggle selection for model (1 or 2)\n'))
            selected[choice-1] = not selected[choice-1]
        elif user == '4':
            if selected[0]: save(init_model)
            if selected[1]: save(extrap_model)
        elif user == '5':
            if selected[0]: load(init_model)
            if selected[1]: load(extrap_model)
        elif user == '6':
            break

        print("\n----------SVR_2-----------")