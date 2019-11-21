from models import ARIMA, Lin_reg, Poly_reg, SVR, SVR_2, RF


def main():

    print("Model_testing")
    
    while True:
        user = input("1. ARIMA\n2. Linear Regression\n3. Polynomial Regression\n4. SVR\n5. SVR_2\n6. Random Forest\n7. Quit\n")
        
        if user == '1':
            ARIMA.run()
        elif user == '2':
            Lin_reg.run()
        elif user == '3':
            Poly_reg.run()
        elif user == '4':
            SVR.run()
        elif user == '5':
            SVR_2.run()
        elif user == '6':
            RF.run()
        elif user == '7':
            break

        print("\n----------MAIN-----------\n")

main()