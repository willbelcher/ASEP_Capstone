from extracter import *
from features import *
from plot import *

from models import ARIMA, P_filter, Lin_reg, Poly_reg, SVR


def main():

    print("Model_testing")
    
    while True:
        user = input("1. ARIMA\n2. Particle Filtering\n3. Linear Regression\n4. Polynomial Regression\n5. SVR\n6. Quit\n")
        
        if user == '1':
            ARIMA.run()
        elif user == '2':
            P_filter.run()
        elif user == '3':
            Lin_reg.run()
        elif user == '4':
            Poly_reg.run()
        elif user == '5':
            SVR.run()
        elif user == '6':
            break

        print("\n---------------------")

main()