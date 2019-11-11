from sklearn.svm import SVR

import numpy as np
import pickle

from features import *
from plot import plot

'''
I didn't store feature information along with previous models so change line in get_data accordingly
get_feature_data([features])

SVR1.sav: ['min_discharge_voltagem', 'min_discharge_voltagec', 'max_discharge_temp', 'previous_capacity']
SVR2.sav: ['min_discharge_voltagem', 'min_discharge_voltagec', 'max_discharge_temp'] //best

'''

class SVR_model():
    def __init__(self, x_train, x_test, y_train, y_test):
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test

    def fit(self):
        x_train = self.x_train
        x_test = self.x_test
        y_train = self.y_train
        y_test = self.y_test

        x_train = np.concatenate(x_train, axis=0)
        x_test = np.concatenate(x_test, axis=0)
        y_train = np.concatenate(y_train, axis=0)
        y_test = np.concatenate(y_test, axis=0)

        
        self.model = SVR(kernel='rbf', degree=5, gamma='scale')

        print("[*] Training model")
        self.model.fit(x_train, y_train)

        print("[*] Evaluating")
        self.predict()


    def predict(self):
        x_train = self.x_train
        x_test = self.x_test
        y_train = self.y_train
        y_test = self.y_test

        x_train = np.concatenate(x_train, axis=0)
        x_test = np.concatenate(x_test, axis=0)
        y_train = np.concatenate(y_train, axis=0)
        y_test = np.concatenate(y_test, axis=0)

        train_pred = self.model.predict(x_train)
        test_pred = self.model.predict(x_test)

        print('\nTraining set - predictions')
        print(y_train)
        print(np.round(train_pred, 2))

        print('\nTesting set - predictions')
        print(y_test)
        print(np.round(test_pred, 2))

        train_rmse = np.sqrt(np.mean((train_pred - y_train) ** 2))

        test_rmse = np.sqrt(np.mean((test_pred - y_test) ** 2))

        rmse = np.sqrt(np.mean(( \
            np.concatenate((train_pred, test_pred), axis=0) - \
            np.concatenate((y_train, y_test), axis=0))** 2))

        print("Estimator evaluation:")
        print("Training set RMSE - {}".format(round(train_rmse, 3)))
        print("Test set RMSE - {}".format(round(test_rmse, 3)))
        print("RMSE - {}".format(round(rmse, 3)))
        input("Press Enter to continue") 

        p = plot()
        for bat in self.y_train[:3]:
            [pred, train_pred] = np.split(train_pred, [len(bat)-1])
            p.plot_one_series(range(len(bat)), bat, '', style='-')
            p.plot_one_series(range(len(pred)), pred, '',  style='--')

        
        p.label_axes('Cycle', 'Capacity (Ahr)', "Predictions vs Actual")
        p.show_plot()
        p.close()


    def save(self, filename):
        print('[*] Saving model to {}'.format(filename))
        pickle.dump(self.model, open(filename, 'wb'))
        print('[*] Model saved')

    def load(self, filename='default'):
        print('[*] Loading model from {}'.format(filename))
        self.model = pickle.load(open(filename, 'rb'))
        print('[*] Model loaded')


#Handles training the model, allows for changing metrics 'easily'
def get_data():    
    X = get_feature_data(['min_discharge_voltagem', 'min_discharge_voltagec', 'max_discharge_temp'])
    Y = get_capacitance()
    

    X, Y = remove_outliers(X, Y)

    #split training and test set
    return split_data(X, Y)


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


#Mainly just UI
def run():
    x_train, x_test, y_train, y_test = get_data()

    model = SVR_model(x_train, x_test, y_train, y_test)

    print("\nSVR")
    
    while True:
        user = input("1. Train\n2. Predict\n3. Save\n4. Load\n5. Quit\n")
        
        if user == '1':
            model.fit()
        elif user == '2':
            model.predict()
        elif user == '3':
            save(model)
        elif user == '4':
            load(model)
        elif user == '5':
            break

        print("\n-----------SVR------------")