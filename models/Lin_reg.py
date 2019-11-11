from sklearn.preprocessing import RobustScaler
import autograd
import autograd.numpy as np2
import numpy as np
from math import e

from features import get_feature_data, get_capacitance, split_data, elementwise_concatenate
from plot import plot as plt

class lin_reg():

    def __init__(self, x_train, x_test, y_train, y_test):
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test

    def fit(self, plot=True):
        x_train = self.x_train
        x_test = self.x_test
        y_train = self.y_train
        y_test = self.y_test

        x_train = np.concatenate(x_train, axis=0)
        x_test = np.concatenate(x_test, axis=0)
        y_train = np.concatenate(y_train, axis=0)
        y_test = np.concatenate(y_test, axis=0)

        scaler = RobustScaler().fit(np.concatenate((x_train, x_test), axis=0))
        x_train = scaler.transform(x_train)
        x_test = scaler.transform(x_test)
   

        eps = 1e-15
        weights = np.zeros(x_train.shape[1])

        def wTx(w, x):
            return np2.dot(x, w)

        def sigmoid(z):
            return 1./(1+(e**(-z)))

        def logistic_predictions(w, x):
            predictions = sigmoid(wTx(w, x))
            return predictions.clip(eps, 1-eps)

        def custom_loss(y, pred_y):
            return np2.mean((pred_y - y) ** 2)
        
        def custom_loss_with_weights(w):
            y_predicted = logistic_predictions(w, x_train)
            return custom_loss(y_train, y_predicted)


        gradient = autograd.grad(custom_loss_with_weights)

        print("[*] Training model")

        for i in range(100000):
            weights -= gradient(weights) * 0.003
            if i % 5000 == 0:
                print('Iterations {} | Loss {}'.format(i, round(custom_loss_with_weights(weights), 5)))
                print(weights)
                print()

        print("[*] Evaluating model")
        train_pred = wTx(weights, x_train)
        test_pred = wTx(weights, x_test)

        print("\n[*] Training complete:")

        print('\nTraining set - predictions')
        print(np.squeeze(y_train))
        print(np.round(train_pred, 2))

        print('\nTesting set - predictions')
        print(np.squeeze(y_test))
        print(np.round(test_pred, 2))

        train_rmse = np.sqrt(np.mean((train_pred - y_train) ** 2))

        test_rmse = np.sqrt(np.mean((test_pred - y_test) ** 2))

        rmse = np.sqrt(np.mean(( \
            np.concatenate((train_pred, test_pred), axis=0) - \
            np.concatenate((y_train, y_test), axis=0)) ** 2))

        print("Estimator evaluation:")
        print("Training set rmse - {}".format(round(train_rmse, 3)))
        print("Test set rmse - {}".format(round(test_rmse, 3)))
        print("RMSE - {}".format(round(rmse, 3)))
        
        input("Press Enter to continue")

        print("[*]Graphing data")

        p = plt()
        for bat in self.y_train[:3]:
            [pred, train_pred] = np.split(train_pred, [len(bat)-1])
            p.plot_one_series(range(len(bat)), bat, '', style='-')
            p.plot_one_series(range(len(pred)), pred, '',  style='--')

        
        p.label_axes('Cycle', 'Capacity (Ahr)', "Predictions vs Actual")
        p.show_plot()
        p.close()

    #TODO
    def predict(self):
        predictions = 0

        # print("\nTrue | Predicted")
        # for t, p in zip(y, predictions):
        #     print(t, "-", p)
               

    def save(self):
        raise NotImplementedError

    def load(self, filename='default'):
        raise NotImplementedError


def get_data():    
    X = get_feature_data()
    Y = get_capacitance()

    return split_data(X, Y)

#Mainly just UI
def run():
    
    x_train, x_test, y_train, y_test = get_data()
    model = lin_reg(x_train, x_test, y_train, y_test)

    print("\nPHM Linear Regression")
    
    while True:
        user = input("1. Train\n2. Predict\n3. Save\n4. Load\n5. Quit\n")
        
        if user == '1':
            model.fit()
        elif user == '2':
            model.predict()
        elif user == '3':
            model.save()
        elif user == '4':
            model.load()
        elif user == '5':
            break

        print("\n--------Linear Regression---------\n")