from utility import *
from datetime import *
from data_loader import *
from model.Enums import Role
import re

users = load_users()
airports = load_airports()
airplanes = load_airplanes()
flights = load_flights(airports)
departures = load_departures(flights, airplanes)
tickets = load_tickets(departures)
current_user = None


def validate_flight_id():

    flight_id = ""
    valid = False
    result = None
    while flight_id == "" and valid is False:
        flight_id = input("Enter flight ID. Enter 0 to return to previous menu\n")
        if flight_id == '0':
            return
        if len(flight_id) == 4 and flight_id.isnumeric():
            for departure in departures:
                if flight_id == departure.id:
                    result = departure
                    valid = True
                    break

        if valid is False:
            print("Invalid flight ID\n")
            flight_id = ""

        if valid is True:
            if result.seats_taken == result.capacity:
                valid = False
                flight_id = ""
                print("Flight is full. Please choose another flight")




    return result


def purchase_ticket(departure, customer = ""):
    #TODO:
    # ticket = Ticket()
    # departure.seats_taken += 1
    # save_departures_to_file()
    pass


def purchase_tickets_menu():

    while True:
        #print("Please enter a flight ID. You can also look it up using search")
        print("|0| Go back to previous menu")
        print("|1| Enter flight ID")
        print("|2| Look up flight IDs by a single criteria")
        print("|3| Look up flight IDs by multiple criteria")
        choice = input()

        if choice == "0":
            return

        elif choice == "1":


            while True:
                departure = validate_flight_id()
                print("Are you purchasing this ticket for yourself?")
                print("|1| Yes, I am purchasing this ticket for myself.")
                print("|2| No, I am purchasing this ticket for somebody else.")
                command = input()
                if command == "1":
                    purchase_ticket(departure)
                    #TODO: Take data from the currently logged in user
                elif command == "2":
                    purchase_ticket(departure, "Other")
                    #TODO: Enter name and last name for the contact person, but take contact info from the logged in user
                else:
                    print("Invalid command. Please enter a valid command.\n")



            #purchase_tickets(flight_id)
            #Check the flight ID
            #length 4 only digits
            #check if it exists
            #
        elif choice == "2":
            flight_search_menu("End")
        elif choice == "3":
            flight_search_menu("End","Multi")
        else:
            print("Invalid input")
            choice = ""

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
    validate_city(search_criteria, "departure_airport", "Please enter a departure city name. Example: Belgrade\n")
    validate_city(search_criteria, "destination_airport", "Please enter a destination city name. Example: London\n")

    departure_date = date_input("Please enter departure date\n")
    departure_days = date_input("Please enter numbers of days for the search window\n", "Day")

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

    arrival_days = date_input("Please enter numbers of days for the search window\n", "Day")

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

    candidates = []
    for departure_date in departure_dates:
        search_criteria["departure_date"] = departure_date
        for arrival_date in arrival_dates:
            search_criteria["arrival_date"] = arrival_date
            candidates.extend(flight_search(departures, search_criteria))

    results = []
    current_date_obj = datetime.today().date()
    current_time_obj = datetime.now().time()

    for departure in candidates:
        departure_date = datetime.strptime(departure.departure_date, "%d-%m-%Y").date()
        departure_time = datetime.strptime(departure.flight.departure_time, "%H:%M").time()

        if departure_date > current_date_obj:
            results.append(departure)
        if departure_date == current_date_obj and departure_time >= current_time_obj:
            results.append(departure)

    print_flight_search_table(results)

def cheapest_flights_menu(amount):   #TODO: Rework this

    search_criteria = create_search_dict()
    validate_city(search_criteria, "departure_airport", "Please enter a departure city name. Example: Belgrade\n")
    validate_city(search_criteria, "destination_airport", "Please enter a destination city name. Example: London\n")
    results = flight_search(departures, search_criteria)

    results.sort(key = lambda departure: departure.flight.price )
    results =  results[:amount]
    results.reverse()
    print_flight_search_table(results)

def unrealised_departures(): #TODO: Rework because of changed model, added pointer to Flight object
                             #TODO: Check current date and time, compare to departures

    results = []

    current_date_obj = datetime.today().date()
    current_time_obj = datetime.now().time()

    for departure in departures:
        departure_date = datetime.strptime(departure.departure_date, "%d-%m-%Y").date()
        departure_time = datetime.strptime(departure.flight.departure_time, "%H:%M").time()

        if departure_date > current_date_obj:
            results.append(departure)
        if departure_date == current_date_obj and departure_time >= current_time_obj:
            results.append(departure)

    print_flight_search_table(results)

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

    #if id == "Flight_ID":
    if len(results) > 0:
        print(
            "{:12}{:16}{:16}{:25}{:25}{:10}{:}".format("Flight ID","From", "To", "Departure date and time", "Arrival date and time",
                                                  "Price", "Airline"))
        for departure in results:
            print("{:12}{:16}{:16}{:10} at {:11}{:10} at {:11}{:10}{:}".format(departure.id,
                                                                        departure.flight.departure_airport.city,
                                                                        departure.flight.destination_airport.city,
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

def validate_city(search_criteria, key, text):

    valid = False
    while search_criteria[key] == "" and valid == False:
        var = search_criteria[key] = input(text)
        if var.isalpha():
            for airport in airports:
                if airport.city.lower() == var.lower():
                    search_criteria[key] = airport.city
                    valid = True
                    break
            if valid is False:
                print("Invalid city. ", end = "")
                search_criteria[key] = ""
            #TODO: Iata
            #search_criteria[key] = ""

        else:
            print("Invalid city. ", end = "")
            valid = False
            search_criteria[key] = ""

def flight_search_menu(end = "", mode = "Single"): #Other argument is "Multi"

    while True:
        choices = []
        valid = True
        if mode == "Single":
            print("Please select a criteria to search flights by")
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
            validate_city(search_criteria, "departure_airport", "Please enter a departure city name. Example: Belgrade\n")

        if '2' in  choices:
            validate_city(search_criteria, "destination_airport", "Please enter a destination city name. Example: London\n")

        if '3' in choices:
            datetime_input(search_criteria, "departure_date", "Please enter a departure date in the format of d-m-yyyy\n")

        if '4' in choices:
            datetime_input(search_criteria, "arrival_date", "Please enter an arrival date in the format of d-m-yyyy\n")

        if '5' in choices:
            datetime_input(search_criteria, "departure_time", "Please enter a departure time in the format of H:M\n", "Time")

        if '6' in choices:
            datetime_input(search_criteria, "arrival_time", "Please enter an arrival time in the format of H:M\n", "Time")

        if '7' in choices:
            while search_criteria["airline"] == "":
                search_criteria["airline"] = input("Please enter airline\n")
        if valid:
            if end == "End":
                print_flight_search(search_criteria)
                break
            else:
                print_flight_search(search_criteria)

def authenticate_user(username, password):

    for user in users:
        if user.username == username and user.password == password:
            return user
    return None

def register_handler(): 
    username, password, first_name, last_name, phone, email = "", "", "", "", "", ""
    list_of_usernames = [user.username for user in users]

    print("Fields marked with an * are required")
    while username == "":
        username = input("Username*: ")
        if '|' in username:
            print("Username cannot contain the character \"|\"")

        if username in list_of_usernames:
            print("Username already taken, please enter a different username")
            username = ""

    while password == "":
        password = input("Password*: ")
        if '|' in password:
            print("Password cannot contain the character \"|\"")
            password = ""

    while first_name == "":
        first_name = input("First name*: ")
        if not first_name.isalpha():
            print("Please enter only letters")
            first_name = ""

    while last_name == "":
        last_name = input("Last name*: ")
        if not last_name.isalpha():
            print("Please enter only letters")

    while phone == "":
       phone = input("Phone number*: ")

    while email == "" :
        email = input("Email address*: ")
        if  not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",email):
            print("Please enter a valid email address")
            email = ""
            continue

    passport_number = input("Passport number: ")
    while passport_number != "":
        if len(passport_number) != 9 or not passport_number.isnumeric():
            print("Passport number can only contain digits and must be 9 digits long")
            passport_number = input("Passport number: ")
        else:
            break

    citizenship = input("Citizenship: ")
    while citizenship != "":
        if not citizenship.isalpha():
            print("Please enter only letters")
            citizenship = input("Citizenship: ")
        else:
            break

    gender = input("Gender: ")
    while gender != "":
        if not gender.isalpha():
            print("Please enter only letters")
            gender = input("Citizenship: ")
        else:
            break

    register_user(username, password, first_name, last_name, phone, email, passport_number, citizenship, gender)

def register_user(username, password, first_name, last_name, phone, email, passport_number, citizenship, gender):
    user = Customer(username, password, first_name, last_name, phone, email, passport_number , citizenship , gender)
    users.append(user)
    save_user_to_file(user)

def save_user_to_file(user):
    with open("data/customers","a") as f:
        line = "\n" + str(user.serialize())
        #print(line)
        f.write(line)

def save_departures_to_file():
    with open("data/departures","w") as f:
        for departure in departures:
            #print(departure.serialize())
            f.write(departure.serialize() + "\n")
        #line = "\n" + str(user.serialize())
        #print(line)
        #f.write(line)

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
        #TODO: Save departures to file
        save_departures_to_file()
    elif command == '3':
        unrealised_departures()
        #TODO: Overview of unrealised flights
    elif command == '4':
        # for departure in departures:
        #     if departure.id == "0001" and departure.capacity > departure.seats_taken:
        #         departure.seats_taken += 1
        #     print(departure.serialize())
        flight_search_menu("")
        #TODO: Flight search by one criteria
    elif command == '5':
        flight_search_menu("","Multi")
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
            purchase_tickets_menu()
            #print("buy tickets")
            # TODO: buy tickets
        elif command == '9':
            # TODO: unrealised flights
            pass
        elif command == '10':
            # TODO: check-in
            pass

        valid = default_menu(command)
        if not valid and command not in ['1','8','9','10']:
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
            user = authenticate_user(username, password)


            if user == None:
                print("Invalid credentials, please try logging in again")

            elif user.role == Role.Customer:
                customer_menu()

            elif user.role == Role.Seller:
                seller_menu()

            elif user.role == Role.Manager:
                manager_menu()

            current_user = user

        elif command == '8':
            print("Please enter your credentials: ")
            register_handler()

        valid = default_menu(command)
        if not valid and command not in ['1','8']:
            print("Unknown command, please enter a valid command")

if __name__ == "__main__":
    main()