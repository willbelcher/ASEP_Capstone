from statsmodels.tsa.arima_model import ARIMA
import numpy as np
import pickle

from features import get_feature_data, get_capacitance, split_data


#Honestly you just need to figure out how this works in terms of inputs and 
#whatever degrees of freedom are
class ARIMA_model():
    def __init__(self, x_train, x_test, y_train, y_test):
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test

    def fit(self):
        self.model = ARIMA([self.x_train, self.y_train], order=(5,1,1))

        print("[*] Training model")
        self.model.fit()

        print("[*] Evaluating")
        self.predict(self.x_train, self.y_train, self.x_test, self.y_test)


    def predict(self):
        x_train = self.x_train
        x_test = self.x_test
        y_train = self.y_train
        y_test = self.y_test

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
    X = get_feature_data()
    Y = get_capacitance()

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

        print("\n-----------RF------------")