from utility import *
from datetime import *
from data_loader import *
from model.Enums import Role

users = load_users()
flights = load_flights()
departures = load_departures(flights)

def date_input(text, day = ""):

    valid = False
    date = ""
    while date == "" and valid == False:
        date = input(text)
        if day == "":
            valid = validate_datetime(date)
        elif day == "Day":
            valid = validate_integer(date)
        if not valid:
            date = ""
    return date

def flexible_schedule_menu():

    search_criteria = create_search_dict()
    airport_input_and_validation(search_criteria, "departure_airport", "Please enter a 3 character departure airport:")
    airport_input_and_validation(search_criteria, "destination_airport", "Please enter a 3 character arrival airport:")

    departure_date = date_input("Please enter departure date: ")
    departure_days = date_input("Please enter numbers of days for the search window: ", "Day")

    departure_date_object = datetime.strptime(departure_date, "%d-%m-%Y").date()

    arrival_date = date_input("Please enter arrival date: ")
    valid = False
    while not valid:
        arrival_date_object = datetime.strptime(arrival_date, "%d-%m-%Y").date()
        if arrival_date_object < departure_date_object:
            print("Cannot travel back in time. ")
            arrival_date = date_input("Please enter arrival date: ")
            continue
        else:
            valid = True

    arrival_days = date_input("Please enter numbers of days for the search window: ", "Day")

    departure_dates = []
    arrival_dates = []

    for i in range(-int(departure_days),int(departure_days) + 1):
        date = datetime.strptime(departure_date, "%d-%m-%Y").date()               #convert string date to datetime object
        departure_dates.append((date + timedelta(days = i)).strftime("%#d-%#m-%Y")) # adds and subtracts wanted number of
                                                                                  # days from date, converts it into
                                                                                  # european format and then appends
                                                                                  # that date to an list
    for i in range(-int(arrival_days),int(arrival_days) + 1):
        date = datetime.strptime(arrival_date, "%d-%m-%Y").date()
        arrival_dates.append((date + timedelta(days = i)).strftime("%#d-%#m-%Y"))

    results = []
    for departure_date in departure_dates:
        search_criteria["departure_date"] = departure_date
        for arrival_date in arrival_dates:
            search_criteria["arrival_date"] = arrival_date
            results.extend(flight_search(departures, search_criteria))

    print_flight_search_table(results)

def cheapest_flights_menu(amount):

    search_criteria = create_search_dict()
    print("Please enter a 3 character airport code. Example: BEG")
    airport_input_and_validation(search_criteria, "departure_airport", "Please enter departure airport:")
    airport_input_and_validation(search_criteria, "destination_airport", "Please enter destination airport:")
    results = flight_search(departures, search_criteria)

    results.sort(reverse = True, key = lambda departure: departure.flight.price )
    results =  results[:amount]
    print_flight_search_table(results)

def unrealised_departures(): #TODO: Rework because of changed model, added pointer to Flight object
                             #TODO: Check current date and time, compare to departures
    print("Unrealised departures: ")
    print("{:6}{:6}{:25}{:25}{:}".format("From", "To", "Departure date and time", "Arrival date and time", "Price"))
    for departure in departures:
        for flight in flights:
            if flight.flight_number == departure.flight_number:
                print("{:6}{:6}{:10} at {:11}{:1} at {:10} {:}€"
                      .format(flight.departure_airport,flight.destination_airport, departure.departure_date,
                              flight.departure_time, departure.arrival_date, flight.arrival_time, flight.price))

def print_flight_search_menu():
    print("|1| Departure airport")
    print("|2| Destination airport")
    print("|3| Departure date")
    print("|4| Arrival date")
    print("|5| Departure time")
    print("|6| Arrival time")
    print("|7| Airline")
    print("|0| Return to previous menu")

def validate_datetime(date_text, time = ""):
    if time == "Time":
        try:
            datetime.strptime(date_text, "%H:%M")
        except:
            print("Incorrect time. Please enter a valid time.") #TODO: Unhardcode this. Move this function into utils, and the prints into main
            return False
        else:
            return True

    else:
        try:
            datetime.strptime(date_text, "%d-%m-%Y")
        except:
            print("Incorrect date. Please enter a valid date.")
            return False
        else:
            return True

def validate_integer(integer):
    try:
        int(integer)
    except:
        print("Incorrect number. Please enter a valid number")
        return False
    else:
        return True

def print_flight_search_table(results):
    if len(results) > 0:
        print("{:6}{:6}{:25}{:25}{:10}{:}".format("From", "To", "Departure date and time", "Arrival date and time",
                                                  "Price", "Airline"))
        for departure in results:
            print("{:6}{:6}{:10} at {:11}{:10} at {:11}{:10}{:}".format(departure.flight.departure_airport,
                                                                        departure.flight.destination_airport,
                                                                        departure.departure_date,
                                                                        departure.flight.departure_time,
                                                                        departure.arrival_date,
                                                                        departure.flight.arrival_time,
                                                                        departure.flight.price + " €",
                                                                        departure.flight.airline))
    else:
        print("No matching results found")

def print_flight_search(search_criteria):

        results = flight_search(departures, search_criteria)
        print_flight_search_table(results)

def datetime_input(search_criteria, key, text, time = ""):

    valid = False
    while search_criteria[key] == "" and valid == False:
        search_criteria[key] = input(text)
        valid = validate_datetime(search_criteria[key], time)
        if not valid:
            search_criteria[key] = ""
    return search_criteria[key]

def airport_input_and_validation(search_criteria, key, text):
    valid = False
    while search_criteria[key] == "" and valid == False:
        search_criteria[key] = input(text).upper()
        if len(search_criteria[key]) != 3:
            search_criteria[key] = ""
        else:
            valid = True

def flight_search_menu(mode = "Single"): #Other argument is "Multi"
    while True:

        choices = []
        valid = True
        if mode == "Single":
            print("Please select a criteria to search flight by")
            print_flight_search_menu()
            choices = input()
            if len(choices) > 1:
                print("Invalid command. Please enter a valid.")
                continue

        elif mode == "Multi":
            print("Search flights by multiple criteria, please select one or more separated by spaces. Example 1 2")
            print_flight_search_menu()
            commands = input()
            choices = commands.split(" ")

        search_criteria = create_search_dict()

        valid = True
        for element in choices:
            if element not in ['0','1','2','3','4','5','6','7']:
                print("Invalid command. Please enter valid commands.")
                valid = False
                break

        if not valid:
            continue

        if '0' in choices:
            return

        if '1' in  choices:
            print("Please enter a 3 character airport code. Example: BEG")
            airport_input_and_validation(search_criteria, "departure_airport", "Please enter departure airport:")

        if '2' in  choices:
            print("Please enter a 3 character airport code. Example: CRL")
            airport_input_and_validation(search_criteria, "destination_airport", "Please enter destination airport:")

        if '3' in choices:
            print("Please enter a date in the format of d-m-yyyy")
            datetime_input(search_criteria, "departure_date", "Please enter departure date:")

        if '4' in choices:
            print("Please enter a date in the format of d-m-yyyy")
            datetime_input(search_criteria, "arrival_date", "Please enter arrival date:")

        if '5' in choices:
            print("Please enter a time in the format of H:M")
            datetime_input(search_criteria, "departure_time", "Please enter departure time:", "Time")

        if '6' in choices:
            print("Please enter a time in the format of H:M")
            datetime_input(search_criteria, "arrival_time", "Please enter arrival time:", "Time")

        if '7' in choices:
            while search_criteria["airline"] == "":
                search_criteria["airline"] = input("Please enter airline:")
        if valid:
            print_flight_search(search_criteria)

def authenticate_user(username, password):

    for user in users:
        if user.username == username and user.password == password:
            return user.role
    return None

def register_handler(): #TODO: User should not be able to enter file delimiter character "|" into any fields except for password. Store password at the end of each line
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
    print("|2| Exit application")
    print("|3| Overview of unrealised flights")
    print("|4| Flight search")
    print("|5| Multiple-criteria Flight search")
    print("|6| 10 Cheapest flights from departure to destination")
    print("|7| Flexible departure date")

def default_menu(command):

    if command == '2':
        exit()
    elif command == '3':
        unrealised_departures()
        #TODO: Overview of unrealised flights
    elif command == '4':
        flight_search_menu()
        #TODO: Flight search by one criteria
    elif command == '5':
        flight_search_menu("Multi")
    elif command == '6':
        cheapest_flights_menu(10)
    elif command == '7':
        flexible_schedule_menu()
    else:
        return False
    return True


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

        valid = default_menu(command)
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

        valid = default_menu(command)
        if not valid:
            print("Unknown command, please enter a valid command")


def manager_menu():

    print("Logged in as Manager")
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

        valid = default_menu(command)
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

        valid = default_menu(command)
        if not valid and command != '1':
            print("Unknown command, please enter a valid command")

if __name__ == "__main__":
    main()