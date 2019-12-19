import seller_functions
from model.Seller import Seller
from model.Flight import Flight
from utility import *

def save_seller_to_file(seller):
    with open("data/sellers", "a") as f:
        f.write("\n" + str(seller.serialize()))

def register_seller():

    from main import users

    print("Please enter the data of the new seller")

    username, password, first_name, last_name = "", "", "", ""
    list_of_usernames = [user.username for user in users]
    while username == "":
        username = input("Username: ")
        if '|' in username:
            print("Username cannot contain the character \"|\"")

        elif username in list_of_usernames:
            print("Username already taken, please enter a different username")
            username = ""

    while password == "":
        password = input("Password: ")
        if '|' in password:
            print("Password cannot contain the character \"|\"")
            password = ""

    while first_name == "":
        first_name = input("First name: ")
        if not first_name.isalpha():
            print("Please enter only letters")
            first_name = ""

    while last_name == "":
        last_name = input("Last name: ")
        if not last_name.isalpha():
            print("Please enter only letters")
            last_name = ""

    seller = Seller(username, password, first_name, last_name)
    save_seller_to_file(seller)
    print("Seller", seller.first_name, seller.last_name,"successfully registered")
    return seller

def validate_city(text):

    from main import airports
    while True:
        print(text)
        city = input()
        if city.isalpha() is False:
            print("Please enter only letters")
            continue

        for airport in airports:
            if airport.city.lower() == city.lower():
                return airport.code
        print("City not found.")
        return None


def create_new_flight():
    from main import  airplanes, validate_datetime
    departure_airport = validate_city("Enter departure city. Example: Belgrade")
    destination_airport = validate_city("Enter destination city. Example: London")

    while True:
        print("Enter a departure time in the format of H:M")
        time = input()
        if validate_datetime(time, "Time") is True:
            departure_time = time
            break

    while True:
        print("Enter an arrival time in the format of H:M")
        time = input()
        if validate_datetime(time, "Time") is True:
            arrival_time = time
            break


    print(departure_airport, destination_airport)
    print(departure_time, arrival_time)

    # all working so far

    #   AA11 | NYO | BEG | 22: 30 | 23:30 | No | Wizz Air | mon, wed | A333 | 140
    #flight = Flight(,departure_airport, destination_airport, )

