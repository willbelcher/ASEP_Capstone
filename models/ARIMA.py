from statsmodels.tsa.arima_model import ARIMA
import numpy as np
import pickle

from features import *
from plot import plot


#Honestly you just need to figure out how this works in terms of inputs and 
#whatever degrees of freedom are
#Also figure out how inputs work here, its gonna be a pain

class ARIMA_model():
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

        #train = np.concatenate(x_train, axis=0)

        ARIMA.endog_names = 'capacity'

        for bat in x_train:
            y = bat[:, 1]
            self.model = ARIMA(y, order=(4, 2, 1))

            print("[*] Training model")
            self.model_fit = self.model.fit()

            print("[*] Evaluating")
            self.predict(y)
   
    def predict(self, y):
        start = 5

        train_pred = self.model_fit.predict(start=start, end=len(y)-1)
       
        print('\nTraining set - predictions')
        print(y)
        print(np.round(train_pred, 2))

        train_rmse = np.sqrt(np.mean((train_pred - y[start:]) ** 2))

        print("Estimator evaluation:")
        print("Training set RMSE - {}".format(round(train_rmse, 3)))
        input("Press Enter to continue") 


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
    y = get_capacitance()
    Y = insert_cycles(y)

    Y, y = remove_outliers(Y, y)

    #split training and test set
    return split_data(Y, y)


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

    model = ARIMA_model(x_train, x_test, y_train, y_test)

    print("\nARIMA")
    
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

        print("\n----------ARIMA-----------")