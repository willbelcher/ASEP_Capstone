from models import ARIMA, Lin_reg, Poly_reg, SVR, RF


def main():

    print("Model_testing")
    
    while True:
        user = input("1. ARIMA\n2. Linear Regression\n3. Polynomial Regression\n4. SVR\n5. Random Forest\n6. Quit\n")
        
        if user == '1':
            ARIMA.run()
        elif user == '2':
            Lin_reg.run()
        elif user == '3':
            Poly_reg.run()
        elif user == '4':
            SVR.run()
        elif user == '5':
            RF.run()
        elif user == '6':
            break

        print("\n----------MAIN-----------\n")

main()