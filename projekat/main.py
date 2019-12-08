from utility import *

users = load_users()
flights = load_flights()
departures = load_departures(flights)


def unrealised_departures():

    print("Unrealised departures: ")
    print("{:6}{:6}{:25}{:25}{:}".format("From", "To", "Departure date and time", "Arrival date and time", "Price"))
    for departure in departures:
        for flight in flights:
            if flight.flight_number == departure.flight_number:
                print("{:6}{:6}{:10} at {:11}{:1} at {:10} {:}€"
                      .format(flight.departure_airport,flight.destination_airport, departure.departure_date,
                              flight.departure_time, departure.arrival_date, flight.arrival_time, flight.price))

def print_flight_search_menu():
    print("    |1| Departure airport")
    print("    |2| Destination airport")
    print("    |3| Departure date")
    print("    |4| Arrival date")
    print("    |5| Departure time")
    print("    |6| Arrival time")
    print("    |7| Airline")
    print("    |0| Return to previous menu")


def print_flight_search(search_criteria):

        results = flight_search(departures, search_criteria)
        print("{:6}{:6}{:25}{:25}{:}".format("From", "To", "Departure date and time", "Arrival date and time", "Airline"))
        for departure in results:
            print("{:6}{:6}{:10} at {:11}{:1} at {:10} {:}" .format(departure.flight.departure_airport,
                                                                     departure.flight.destination_airport,
                                                                     departure.departure_date,
                                                                     departure.flight.departure_time,
                                                                     departure.arrival_date,
                                                                     departure.flight.arrival_time,
                                                                     departure.flight.airline))

def flight_search_menu_multi():
    while True:
        print("Search flights by multiple criteria, please select one or more separated by spaces. Example 1 3")
        print_flight_search_menu()
        search_criteria = create_search_dict()
        commands = input()
        choices = commands.split(" ")

        valid = True
        for element in choices:
            if element not in ['0','1','2','3','4','5','6','7']:
                print("Invalid commands. Please enter valid commands.")
                valid = False
                break
        if not valid:
            pass
        if '0' in choices:
            return
        if '1' in  choices:
            while search_criteria['departure_airport'] == "":
                print("Please enter a capitalized 3 character airport code. Example: BEG")
                search_criteria['departure_airport'] = input("Please enter departure airport:")
        if '2' in  choices:
            while search_criteria['destination_airport'] == "":
                print("Please enter a capitalized 3 character airport code. Example: CRL")
                search_criteria['destination_airport'] = input("Please enter destination airport:")
        if '3' in choices:
            while search_criteria['departure_date'] == "":
                search_criteria['departure_date'] = input("Please enter departure date:")
        if '4' in choices:
            while search_criteria['arrival_date'] == "":
                search_criteria['arrival_date'] = input("Please enter arrival date:")
        if '5' in choices:
            while search_criteria['departure_time'] == "":
                search_criteria['departure_time'] = input("Please enter departure time:")
        if '6' in choices:
            while search_criteria['arrival_time'] == "":
                search_criteria['arrival_time'] = input("Please enter arrival time:")
        if '7' in choices:
            while search_criteria['airline'] == "":
                search_criteria['airline'] = input("Please enter airline:")

        print_flight_search(search_criteria)

def flight_search_menu_single():
    while True:
        print("Please select one option. Search flights by:")
        print_flight_search_menu()
        search_criteria = create_search_dict()
        command = input()
        if command == '0':
            return
        elif command == '1':
            while search_criteria['departure_airport'] == "":
                print("Please enter a capitalized 3 character airport code. Example: BEG")
                search_criteria['departure_airport'] = input("Please enter departure airport:")
        elif command == '2':
            while search_criteria['destination_airport'] == "":
                print("Please enter a capitalized 3 character airport code. Example: CRL")
                search_criteria['destination_airport'] = input("Please enter destination airport:")
        elif command == '3':
            while search_criteria['departure_date'] == "":
                search_criteria['departure_date'] = input("Please enter departure date:")
        elif command == '4':
            while search_criteria['arrival_date'] == "":
                search_criteria['arrival_date'] = input("Please enter arrival date:")
        elif command == '5':
            while search_criteria['departure_time'] == "":
                search_criteria['departure_time'] = input("Please enter departure time:")
        elif command == '6':
            while search_criteria['arrival_time'] == "":
                search_criteria['arrival_time'] = input("Please enter arrival time:")
        elif command == '7':
            while search_criteria['airline'] == "":
                search_criteria['airline'] = input("Please enter airline:")
        else:
            print("Unknown command, please enter a valid command")

        print_flight_search(search_criteria)

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
        email = input("Email address*: ")

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
    print("    |2| Exit application")
    print("    |3| Overview of unrealised flights")
    print("    |4| Flight search")
    print("    |5| Multiple-criteria Flight search")
    print("    |6| 10 Cheapest flights from departure to destination")
    print("    |7| Flexible departure date")

def dafault_menu(command):

    if command == '2':
        exit()
    elif command == '3':
        unrealised_departures()
        #TODO: Overview of unrealised flights
    elif command == '4':
        flight_search_menu_single()
        #TODO: Flight search by one criteria
        pass
    elif command == '5':
        flight_search_menu_multi()
        pass
    elif command == '6':
        pass
    elif command == '7':
        pass
    else:
        return False
    return True


def customer_menu():

    valid = True
    while True:
        print("    |1| Log out")
        print_default_menu()
        print("    |8| Buy tickets")
        print("    |9| Overview of unrealised tickets")
        print("    |10| Check-in for your flight")
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

        valid = dafault_menu(command)
        if not valid:
            print("Unknown command, please enter a valid command")


def seller_menu():
    valid = True
    while True:
        print("Welcome, Seller")
        print("    |1| Log out")
        print_default_menu()
        print("    |8| Sell tickets")
        print("    |9| Check-in a passenger for his flight")
        print("    |10| Edit a ticket")
        print("    |11| Delete a ticket")
        print("    |12| Browse sold tickets")

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

        valid = dafault_menu(command)
        if not valid:
            print("Unknown command, please enter a valid command")


def manager_menu():

    print("Logged in as Manager")
    while True:
        print("    |1| Log out")
        print_default_menu()
        print("    |8| Browse sold tickets")
        print("    |9| Register a new seller")
        print("    |10| Create a new flight") #TODO: proverava se ispravnost unetih podataka
        print("    |11| Edit flights") #TODO: Omoguciti izmenu samo zeljenih podataka
        print("    |12| Confirm deletion of a ticket")

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

        valid = dafault_menu(command)
        if not valid:
            print("Unknown command, please enter a valid command")


def main():

    print("Welcome")
    while True:
        print("    |1| Log in")
        print_default_menu()
        print("    |8| Register as new user")
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

        valid = dafault_menu(command)
        if not valid and command != '1':
            print("Unknown command, please enter a valid command")

if __name__ == "__main__":
    main()