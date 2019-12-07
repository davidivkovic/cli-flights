from utility import *

users = load_users()
departures = load_departures()
#flights = load_flights()

def unrealised_departures():
    for departure in departures:
        flight_number = departure.flight_number

    #print (departures)
    #print(users)


def authenticate_user(username, password):
    for user in users:
        if user.username == username and user.password == password:
            return user.role
    return None

def register_handler():
    username, password, first_name, last_name, phone, email = "", "", "", "", "", ""
    list_of_usernames = [user.username for user in users]

    print("Fields marked with an * are required")
    while username == "":
        username = input("Username*: ")
        if username in list_of_usernames:
            print("Username already taken, please enter a different username")
            username = ""

    while password == "":
        password = input("Password*: ")
    while first_name == "":
        first_name = input("First name*: ")
    while last_name == "":
        last_name = input("Last name*: ")
    while phone == "":
        phone = input("Phone number*: ")
    while email == "":
        email = input("Email address*:")

    passport_number = input("Passport number: ")
    citizenship = input("Citizenship: ")
    gender = input("Gender: ")

    register_user(username, password, first_name, last_name, phone, email, passport_number, citizenship, gender)

def register_user(username, password, first_name, last_name, phone, email, passport_number, citizenship, gender):
    user = Customer(username, password, first_name, last_name, phone, email, passport_number , citizenship , gender)
    users.append(user)
    save_user_to_file(user)

def save_user_to_file(user):
    with open("customers","a") as f:
        line = "\n" + str(user.serialize())
        #print(line)
        f.write(line)


def print_default_menu():
    print("|2| Exit application")
    print("|3| Overview of unrealised flights")
    print("|4| Flight search")
    print("|5| Multiple-criteria Flight search")
    print("|6| 10 Cheapest flights from departure to destination")
    print("|7| Flexible departure date")

def input_handler(command):

    if command == '2':
        exit()
    elif command == '3':
        unrealised_departures()
        #TODO: Overview of unrealised flights
        pass
    elif command == '4':
        #TODO: Flight search by one criteria
        pass
    elif command == '5':
        pass
    elif command == '6':
        pass
    elif command == '7':
        pass
    else:
        return False


def customer_menu():

    valid = True
    while True:
        print("|1| Log out")
        print_default_menu()
        print("|8| Buy tickets")
        print("|9| Overview of unrealised tickets")
        print("|10| Check-in for your flight")
        command = input()

        if command == '1':  # LOGOUT
            return

        if command == '8':
            print("buy tickets")
            # TODO: buy tickets
            pass
        elif command == '9':
            # TODO: unrealised flights
            pass
        elif command == '10':
            # TODO: check-in
            pass

        valid = input_handler(command)
        if not valid:
            print("Unknown command, please enter a valid command")


def seller_menu():
    valid = True
    while True:
        print("Welcome, Seller")
        print("|1| Log out")
        print_default_menu()
        print("|8| Sell tickets")
        print("|9| Check-in a passenger for his flight")
        print("|10| Edit a ticket")
        print("|11| Delete a ticket")
        print("|12| Browse sold tickets")

        command = input()

        if command == '1':  # LOGOUT
            return
        elif command == '8':
            pass
        elif command == '9':
            pass
        elif command == '10':
            pass
        elif command == '11':
            pass
        elif command == '12':
            pass

        valid = input_handler(command)
        if not valid:
            print("Unknown command, please enter a valid command")


def manager_menu():

    print("Welcome, Manager")
    while True:
        print("|1| Log out")
        print_default_menu()
        print("|8| Browse sold tickets")
        print("|9| Register a new seller")
        print("|10| Create a new flight") #TODO: proverava se ispravnost unetih podataka
        print("|11| Edit flights") #TODO: Omoguciti izmenu samo zeljenih podataka
        print("|12| Confirm deletion of a ticket")

        command = input()
        if command == '1':  # LOGOUT
            return
        elif command == '8':
            pass
        elif command == '9':
            pass
        elif command == '10':
            pass
        elif command == '11':
            pass
        elif command == '12':
            pass

        valid = input_handler(command)
        if not valid:
            print("Unknown command, please enter a valid command")


def main():

    print("Welcome")
    while True:
        print("|1| Log in")
        print_default_menu()
        print("|8| Register as new user")
        command = input()

        if command == '1':
            username = input("Please enter your username: ")
            password = input("Please enter your password: ")
            role = authenticate_user(username, password)

            if role == None:
                print("\nInvalid credentials, please try logging in again")

            elif role == Role.Customer:
                customer_menu()

            elif role == Role.Seller:
                seller_menu()

            elif role == Role.Manager:
                manager_menu()

        elif command == '8':
            print("Please enter your credentials: ")
            register_handler()

        valid = input_handler(command)
        if not valid and command != '1':
            print("Unknown command, please enter a valid command")

if __name__ == "__main__":
    main()