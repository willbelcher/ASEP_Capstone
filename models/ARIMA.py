from statsmodels.tsa.arima_model import ARIMA
import pickle

from features import *

class ARIMA_model():
    def __init__(self):
        pass

    def fit(self, X_train, Y_train, X_test, Y_test):
        self.model = ARIMA([X_train, Y_train], order=(1,1,1))

        print("[*] Training model")
        self.model.fit(X_train, Y_train)

        print("[*] Evaluating")
        self.predict(X_train, Y_train, X_test, Y_test)


    def predict(self, X_train, Y_train, X_test, Y_test):
        train_pred = self.model.predict(X_train)
        test_pred = self.model.predict(X_test)

        print('\nTraining set - predictions')
        print(Y_train)
        print(np.round(train_pred, 2))

        print('\nTesting set - predictions')
        print(Y_test)
        print(np.round(test_pred, 2))

        train_rmse = np.sqrt(np.mean((train_pred - Y_train) ** 2))

        test_rmse = np.sqrt(np.mean((test_pred - Y_test) ** 2))

        rmse = np.sqrt(np.mean(( \
            np.concatenate((train_pred, test_pred), axis=0) - \
            np.concatenate((Y_train, Y_test), axis=0))** 2))

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
def train(model):    
    
    data = get_feature_data()

    #split data

    model.fit(X_train, Y_train, X_test, Y_test)


def predict(model):
    X, Y = get_feature_data()

    X_train, Y_train , X_test, Y_test = remove_one_plate(X, Y)

    model.predict(X_train, Y_train, X_test, Y_test)


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
    model = ARIMA_model()

    print("\nARIMA")
    
    while True:
        user = input("1. Train\n2. Predict\n3. Save\n4. Load\n5. Quit\n")
        
        if user == '1':
            train(model)
        elif user == '2':
            predict(model)
        elif user == '3':
            save(model)
        elif user == '4':
            load(model)
        elif user == '5':
            break

        print("\n-----------RF------------")