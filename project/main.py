from utility import *
from datetime import *
from data_loader import *
from model.Enums import Role
from model.User import User
import string
import re

users = load_users()
airports = load_airports()
airplanes = load_airplanes()
flights = load_flights(airports, airplanes)
departures = load_departures(flights, airplanes)
tickets = load_tickets(departures)
current_ticket_id = load_current_ticket_id()
current_user = None
customer = ""
self_purchase = False

def choose_seat(current_ticket):
    rows_cols = current_ticket.departure.flight.airplane.rows_cols
    rows = int(rows_cols.split("/")[0])  #1,2,3,4...
    cols = int(rows_cols.split("/")[1])  #1,2,3,4...
    alphabet = string.ascii_uppercase
    seating_table = [[0] * cols] * rows  #TODO: Fix this, only creates references to a single list, changes element in every list...
    #each ticket hold a filed named seat
    #upon creation of a ticket object the seat field is empty
    #upon check in this field is assigned a value in the form of 1A
    #to generate a table of available and taken seats for a departure we will extract the seat
    #data from the tickets which contain the same departure id
    for i in range(rows):
        for j in range(cols):
            seating_table[i][j] = alphabet[j]


    for ticket in tickets:
        if ticket.departure.id == current_ticket.departure.id:
            seat = ticket.seat
            if seat != "":               #1A
                row = int(seat[0])       # 1,2,3...
                col = ord(seat[1]) - 64  # A -> 1, B -> 2...
                seating_table[row-1][col-1] = "X"

    print(seating_table)
    #for i in range(rows):
        #print(seating_table[i])



def check_in():

    global current_user

    candidates = [] #contains only the user's tickets
    for ticket in tickets:
        if current_user.email == ticket.contact_email:
            candidates.append(ticket)

    while True:

        print("Please enter a ticket ID")
        ticket_id = input()

        ticket_is_valid = False
        for ticket in candidates:
            if ticket_id.upper() == ticket.id:
                ticket_is_valid = True
                current_ticket = ticket #save the current ticket for use

                departure_date_obj = datetime.strptime(ticket.departure.departure_date, "%d-%m-%Y").date()
                departure_time_obj = datetime.strptime(ticket.departure.flight.departure_time, "%H:%M").time()
                print(departure_date_obj, departure_time_obj)
                departure_datetime_obj = datetime.combine(departure_date_obj, departure_time_obj)
                check_in_datetime_obj = departure_datetime_obj - timedelta(hours = 48)
                current_datetime_obj = datetime.now()

                if current_datetime_obj >= check_in_datetime_obj:
                    #collect missing data from the user - passport number, nationality and gender

                    if current_user.passport_number == "":
                        while True:
                            print("Please enter your passport number.")
                            passport_number = input()
                            if passport_number.isnumeric() is True and len(passport_number) == 9:
                                current_user.passport_number = passport_number
                                break
                            else:
                                print("Invalid passport number. A valid number contains 9 digitis.")

                    if current_user.citizenship == "":
                        while True:
                            print("Please etner your citizenship")
                            citizenship = input()
                            if citizenship.isalpha() is True:
                                current_user.citizenship = citizenship
                                break
                            else:
                                print("Citizenship can only contain letters.")

                    if current_user.gender == "":
                        while True:
                            print("Please enter your gender (Male, Female, Other)")
                            gender = input()
                            if  gender.lower() == "male" or gender.lower() == "female" or gender.lower() == "other":
                                current_user.gender = gender
                                break
                            else:
                                print("Invalid gender.")

                    choose_seat(ticket)
                    #TODO: Continue from here

                elif current_datetime_obj > departure_datetime_obj:
                    print("Sorry, your flight has already departed.")
                    return

                else:
                    print("Check is not allowed until 48 hours before the departure of a flight")
                    print("You can check in at",  check_in_datetime_obj)
                    return



        if ticket_is_valid is False:
            print("Invalid ticked ID")


def check_in_menu():
    while True:
        print("You can check in 48 hours before your flight. Enter a ticket ID or search for it.")
        print("|0| Return to previous menu")
        print("|1| Enter ticket ID to check in")
        print("|2| View your purchased tickets")
        choice = input()
        if choice == "0":
            return
        elif choice == "1":
            check_in()
        elif choice == "2":
            unrealised_tickets()
        else:
            print("Invalid command.")
    unrealised_tickets()

def unrealised_tickets():
    candidates = []
    for ticket in tickets:
        if current_user.email == ticket.contact_email:
            candidates.append(ticket)
    print_ticket(candidates, "Multi")


def validate_departure_id(list=None):
    flight_id = ""
    valid = False
    result = None
    while flight_id == "" and valid is False:
        flight_id = input("Enter flight ID. Enter 0 to return to previous menu\n")
        if flight_id == '0':
            return False
        if len(flight_id) == 4 and flight_id.isnumeric():
            if list is not None:
                for departure in list:
                    if flight_id == departure.id:
                        result = departure
                        valid = True
                        break
            else:
                for departure in departures:
                    if flight_id == departure.id:
                        result = departure
                        valid = True
                        break

        if valid is False:
            print("Invalid flight ID")
            flight_id = ""

        elif valid is True:
            if result.seats_taken == result.capacity:
                valid = False
                flight_id = ""
                print("Flight is full. Please choose another flight")

    return result


def print_ticket(ticket, mode):
    if mode == "Single":
        print("{:12}{:14}{:16}{:16}{:22}{:22}{:24}{:20}{:30}{:20}".format("Ticket ID", "Departure ID", "From", "To",
                                                                          "Departure date", "Arrival date",
                                                                          "Ticket holder",
                                                                          "Contact phone",
                                                                          "Contact email", "Date of purchase"))

        print("{:12}{:14}{:16}{:16}{:22}{:22}{:24}{:20}{:30}{:20}".format(ticket.id, ticket.departure.id,
                                                                          ticket.departure.flight.departure_airport.city,
                                                                          ticket.departure.flight.destination_airport.city,
                                                                          ticket.departure.departure_date + " at " +
                                                                          ticket.departure.flight.departure_time,
                                                                          ticket.departure.arrival_date + " at " +
                                                                          ticket.departure.flight.arrival_time,
                                                                          ticket.first_name + " " + ticket.last_name,
                                                                          ticket.contact_phone,
                                                                          ticket.contact_email,
                                                                          ticket.purchase_date))
    elif mode == "Multi":
        tickets = ticket
        print("{:12}{:14}{:16}{:16}{:22}{:22}{:24}{:20}{:30}{:20}".format("Ticket ID", "Departure ID", "From", "To",
                                                                          "Departure date", "Arrival date",
                                                                          "Ticket holder",
                                                                          "Contact phone",
                                                                          "Contact email", "Date of purchase"))
        for ticket in tickets:
            print("{:12}{:14}{:16}{:16}{:22}{:22}{:24}{:20}{:30}{:20}".format(ticket.id, ticket.departure.id,
                                                                              ticket.departure.flight.departure_airport.city,
                                                                              ticket.departure.flight.destination_airport.city,
                                                                              ticket.departure.departure_date + " at " +
                                                                              ticket.departure.flight.departure_time,
                                                                              ticket.departure.arrival_date + " at " +
                                                                              ticket.departure.flight.arrival_time,
                                                                              ticket.first_name + " " + ticket.last_name,
                                                                              ticket.contact_phone,
                                                                              ticket.contact_email,
                                                                              ticket.purchase_date))


def purchase_ticket(departure, first_name="", last_name=""):
    global current_ticket_id
    current_ticket_id += 1
    ticket_id = "AA" + f"{current_ticket_id:04d}"  # takes a number and formats it into 4 digits with leading zeroes 2 --> 0002

    current_date_obj = datetime.today().date()
    current_date_str = current_date_obj.strftime("%#d-%#m-%Y")
    print(current_date_str)
    # validate_ticket_id()

    if first_name == "" and last_name == "":
        ticket = Ticket(ticket_id, departure, current_user.first_name, current_user.last_name, current_user.phone,
                        current_user.email, current_date_str, "" ,"No")     # "" -> No seat assigned yet. "No" -> not q'd for deletion
    else:
        ticket = Ticket(ticket_id, departure, first_name, last_name, current_user.phone,
                        current_user.email, current_date_str, "", "No")

    tickets.append(ticket)
    departure.seats_taken += 1
    save_ticket_to_file(ticket)
    save_departures_to_file()

    print("Purchase successful.")
    print_ticket(ticket, "Single")


def purchase_tickets_menu():
    #This function is a mess, I am totally aware of that...
    def holder_menu():
        global customer
        global self_purchase

        first_name, last_name = "", ""
        while True:

            print("Are you purchasing this ticket for yourself?")
            print("|1| Yes, I am purchasing this ticket for myself.")
            print("|2| No, I am purchasing this ticket for somebody else.")
            command = input()

            if command == "1":
                customer = "Self"
                break

            elif command == "2":
                customer = "Other"
                print("Please enter the first and last name of the person you are purchasing the ticket for")

                while first_name == "":
                    first_name = input("First name:\n")
                    if not first_name.isalpha():
                        print("Please enter only letters")
                        first_name = ""

                while last_name == "":
                    last_name = input("Last name:\n")
                    if not last_name.isalpha():
                        print("Please enter only letters")
                break

            else:
                print("Invalid command. Please enter a valid command.")
                continue

        return first_name, last_name

    def confirmation_menu(departure, first_name, last_name):
        global customer
        global self_purchase
        while True:
            global customer
            global self_purchase

            print("Confirm the purchase of this ticket")
            print("|1| Confirm")
            print("|2| Abort purchase")
            confirmation = input()
            if confirmation == "1":
                if customer == "Self":
                    self_purchase = True

                customer_ticket = purchase_ticket(departure, first_name, last_name)  # generate new ticket
                passenger_ticket_menu(departure)  # ask customer if he wants to buy a ticket for a passenger
                connected_departures_menu(departure)  # ask customer if he wants to but a ticket for connected flights
                return

            elif confirmation == "2":
                return
            else:
                print("Invalid command. Please enter a valid command.")

    def passenger_ticket_menu(departure):
        first_name, last_name = "", ""
        while True:
            print("Do you wish to purchase tickets for a passenger?")
            print("|1| Yes")
            print("|2| No")
            # print("Do you wish to purchase tickets for flights connected to your flight?")
            # print("|1| Yes")
            # print("|2| No")
            selection = input()
            if selection == "1":

                customer = "Other"
                print("Please enter the first and last name of the person you are purchasing the ticket for")

                while first_name == "":
                    first_name = input("First name:\n")
                    if not first_name.isalpha():
                        print("Please enter only letters")
                        first_name = ""

                while last_name == "":
                    last_name = input("Last name:\n")
                    if not last_name.isalpha():
                        print("Please enter only letters")

                while True:
                    print("Confirm the purchase of this ticket")
                    print("|1| Confirm")
                    print("|2| Abort purchase")
                    confirmation = input()
                    if confirmation == "1":
                        purchase_ticket(departure, first_name, last_name)
                        return

                    elif confirmation == "2":
                        return
                    else:
                        print("Invalid command. Please enter a valid command.")

            elif selection == "2":
                return
            else:
                print("Invalid command. Please enter a valid command.")

    def connected_departures_menu(departure):
        first_name, last_name = "", ""
        if self_purchase is True:
            while True:
                print("Do you wish to purchase a ticket for flights connected to your flight?")
                print("|1| Yes")
                print("|2| No")
                selection = input()
                if selection == "1":

                    arrival_date_obj = datetime.strptime(departure.arrival_date, "%d-%m-%Y").date()
                    arrival_time_obj = datetime.strptime(departure.flight.arrival_time, "%H:%M").time()

                    arrival_datetime_obj = datetime.combine(arrival_date_obj, arrival_time_obj)
                    arrival_datetime_obj_delta = arrival_datetime_obj + timedelta(minutes=120)

                    candidates = []
                    search_criteria = create_search_dict()
                    search_criteria["departure_airport"] = departure.flight.destination_airport.city
                    candidates.extend(departure_search(departures, search_criteria))

                    results = []
                    for departure in candidates:
                        connected_date = datetime.strptime(departure.departure_date, "%d-%m-%Y").date()
                        connected_time = datetime.strptime(departure.flight.departure_time, "%H:%M").time()
                        connected_datetime = datetime.combine(connected_date, connected_time)

                        if connected_datetime >= arrival_datetime_obj and connected_datetime <= arrival_datetime_obj_delta:
                            results.append(departure)

                    print_departure_search_table(results)

                    new_departure = validate_departure_id(results)

                    if new_departure is False:
                        return
                    print("Confirm the purchase of this ticket")
                    print("|1| Confirm")
                    print("|2| Abort purchase")
                    confirmation = input()
                    if confirmation == "1":
                        customer_ticket = purchase_ticket(new_departure, first_name, last_name)
                        print_ticket(customer_ticket, "Single")

                    elif confirmation == "2":
                        return
                    else:
                        print("Invalid command. Please enter a valid command.")

                elif selection == "2":
                    return
                else:
                    print("Invalid command. Please enter a valid command.")

    while True:
        print("|0| Return to previous menu")
        print("|1| Enter the departure ID for the ticket you wish to purchase ")
        print("|2| Look up departure IDs by a single criteria")
        print("|3| Look up departure IDs by multiple criteria")
        choice = input()

        if choice == "0":
            return

        elif choice == "1":

            departure = validate_departure_id()
            if departure is False:
                continue

            first_name, last_name = holder_menu()  # empty for self pruchase, first and last name when purchasing for other person

            confirmation_menu(departure, first_name, last_name)

            global customer, self_purchase  # reset global variables to their initial state

            customer = ""
            self_purchase = False

        elif choice == "2":
            departure_search_menu("End")
        elif choice == "3":
            departure_search_menu("End", "Multi")
        else:
            print("Invalid input")
            choice = ""


def date_input(text, day=""):
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

    for i in range(-int(departure_days), int(departure_days) + 1):
        date = datetime.strptime(departure_date, "%d-%m-%Y").date()  # convert string date to datetime object
        departure_dates.append((date + timedelta(days=i)).strftime("%#d-%#m-%Y"))  # adds and subtracts wanted number of
        # days from date, converts it into
        # european format and then appends
        # that date to an list
    for i in range(-int(arrival_days), int(arrival_days) + 1):
        date = datetime.strptime(arrival_date, "%d-%m-%Y").date()
        arrival_dates.append((date + timedelta(days=i)).strftime("%#d-%#m-%Y"))

    candidates = []
    for departure_date in departure_dates:
        search_criteria["departure_date"] = departure_date
        for arrival_date in arrival_dates:
            search_criteria["arrival_date"] = arrival_date
            candidates.extend(departure_search(departures, search_criteria))

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

    print_departure_search_table(results)


def cheapest_flights_menu(amount):  # TODO: Rework this

    search_criteria = create_search_dict()
    validate_city(search_criteria, "departure_airport", "Please enter a departure city name. Example: Belgrade\n")
    validate_city(search_criteria, "destination_airport", "Please enter a destination city name. Example: London\n")
    results = flight_search(flights, search_criteria)

    results.sort(key=lambda flight: flight.price)
    results = results[:amount]
    results.reverse()

    print_flight_search_table(results)


def unrealised_departures():
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

    print_departure_search_table(results)


def print_departure_search_menu():
    print("|1| Departure airport")
    print("|2| Destination airport")
    print("|3| Departure date")
    print("|4| Arrival date")
    print("|5| Departure time")
    print("|6| Arrival time")
    print("|7| Airline")
    print("|0| Return to previous menu")


def validate_datetime(date_text, time=""):
    if time == "Time":
        try:
            datetime.strptime(date_text, "%H:%M")
        except:
            print(
                "Incorrect time. Please enter a valid time.")  # TODO: Unhardcode this. Move this function into utils, and the prints into main
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


def print_departure_search_table(results):
    if len(results) > 0:
        print(
            "{:16}{:20}{:20}{:25}{:25}{:10}{:}".format("Departure ID", "From", "To", "Departure date and time",
                                                       "Arrival date and time",
                                                       "Price", "Airline"))
        for departure in results:
            print("{:16}{:20}{:20}{:10} at {:11}{:10} at {:11}{:10}{:}".format(departure.id,
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


def print_flight_search_table(results):
    if len(results) > 0:
        print(
            "{:16}{:30}{:30}{:30}{:24}{:10}{:}".format("Flight number", "From", "To", "Departure dates",
                                                       "Overnight flight?",
                                                       "Price", "Airline"))
        for flight in results:
            print("{:16}{:30}{:30}{:30}{:24}{:10}{:}".format(flight.flight_number,
                                                             flight.departure_airport.city,
                                                             flight.destination_airport.city,
                                                             flight.days + " at " + flight.departure_time,
                                                             flight.overnight + " - Arrives at " + flight.arrival_time,
                                                             flight.price + " €",
                                                             flight.airline))
    else:
        print("No matching results found")


def datetime_input(search_criteria, key, text, time=""):
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
                print("Invalid city. ", end="")
                search_criteria[key] = ""

        else:
            print("Invalid city. ", end="")
            valid = False
            search_criteria[key] = ""


def departure_search_menu(end="", mode="Single"):  # Other argument is "Multi"

    while True:
        choices = []
        valid = True
        if mode == "Single":
            print("Please select a criteria to search flights by")
            print_departure_search_menu()
            choices = input()
            if len(choices) > 1:
                print("Invalid command. Please enter a valid.")
                continue

        elif mode == "Multi":
            print("Search flights by multiple criteria, please select one or more separated by spaces. Example 1 2")
            print_departure_search_menu()
            commands = input()
            choices = commands.split(" ")

        search_criteria = create_search_dict()

        valid = True
        for element in choices:
            if element not in ['0', '1', '2', '3', '4', '5', '6', '7']:
                print("Invalid command. Please enter valid commands.")
                valid = False
                break

        if not valid:
            continue

        if '0' in choices:
            return

        if '1' in choices:
            validate_city(search_criteria, "departure_airport",
                          "Please enter a departure city name. Example: Belgrade\n")

        if '2' in choices:
            validate_city(search_criteria, "destination_airport",
                          "Please enter a destination city name. Example: London\n")

        if '3' in choices:
            datetime_input(search_criteria, "departure_date",
                           "Please enter a departure date in the format of d-m-yyyy\n")

        if '4' in choices:
            datetime_input(search_criteria, "arrival_date", "Please enter an arrival date in the format of d-m-yyyy\n")

        if '5' in choices:
            datetime_input(search_criteria, "departure_time", "Please enter a departure time in the format of H:M\n",
                           "Time")

        if '6' in choices:
            datetime_input(search_criteria, "arrival_time", "Please enter an arrival time in the format of H:M\n",
                           "Time")

        if '7' in choices:
            while search_criteria["airline"] == "":
                search_criteria["airline"] = input("Please enter airline\n")
        if valid:
            print_departure_search_table(departure_search(departures, search_criteria))
            if end == "End":
                break


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

        elif username in list_of_usernames:
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
            last_name = ""

    while phone == "":
        phone = input("Phone number*: ")
        if '|' in phone:
            print("Phone number cannot contain the character \"|\"")

    while email == "":
        email = input("Email address*: ")
        if not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            print("Please enter a valid email address")
            email = ""

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
    user = Customer(username, password, first_name, last_name, phone, email, passport_number, citizenship, gender)
    users.append(user)
    save_user_to_file(user)


def save_user_to_file(user):
    with open("data/customers", "a") as f:
        line = "\n" + str(user.serialize())
        f.write(line)


def save_departures_to_file():
    with open("data/departures", "w") as f:
        for departure in departures:
            # print(departure.serialize())
            f.write(departure.serialize() + "\n")
        # line = "\n" + str(user.serialize())
        # print(line)
        # f.write(line)


def save_ticket_to_file(ticket):
    with open("data/tickets", "a") as f:
        line = "\n" + str(ticket.serialize())
        f.write(line)

    with open("data/current_ticket_id", "w") as f:
        f.write(str(current_ticket_id))


def print_default_menu():
    print("|2| Exit application")
    print("|3| Overview of unrealised flights")
    print("|4| Flight search")
    print("|5| Multiple-criteria Flight search")
    print("|6| 10 Cheapest flights from departure to destination")
    print("|7| Flexible departure date")


def default_menu(command):
    command_dict = {
        "2": exit,
        "3": unrealised_departures,
        "4": departure_search_menu,
        "5": departure_search_menu,
        "6": cheapest_flights_menu,
        "7": flexible_schedule_menu
    }
    if command in command_dict:
        if command == "4":
            departure_search_menu("")
        elif command == "5":
            departure_search_menu("", "Multi")
        elif command == "6":
            cheapest_flights_menu(10)
        else:
            command_dict[command]()
        return True
    return False

def customer_menu():
    command_dict = {
        "8": purchase_tickets_menu,
        "9": unrealised_tickets,
        "10": check_in_menu,  # TODO: check-in
    }

    print("Currently logged in as", current_user.first_name, current_user.last_name)
    while True:
        print("|1| Log out")
        print_default_menu()
        print("|8| Buy tickets")
        print("|9| Overview of unrealised tickets")
        print("|10| Check-in for your flight")
        command = input()

        if command == "1":
            return

        elif command in command_dict:
            command_dict[command]()

        valid = default_menu(command)
        if not valid and command not in command_dict:
            print("Unknown command, please enter a valid command")


def seller_menu():
    command_dict = {
        "8": purchase_tickets_menu,  # TODO:
        "9": departure_search_menu,  # TODO:
        "10": departure_search_menu,  # TODO:
        "11": departure_search_menu,  # TODO:
        "12": departure_search_menu,  # TODO:
    }

    print("Currently logged in as", current_user.first_name, current_user.last_name)
    while True:
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
        elif command in command_dict:
            command_dict[command]()

        valid = default_menu(command)
        if not valid and command not in command_dict:
            print("Unknown command, please enter a valid command")


def manager_menu():
    command_dict = {
        "8": purchase_tickets_menu,  # TODO:
        "9": departure_search_menu,  # TODO:
        "10": departure_search_menu,  # TODO:
        "11": departure_search_menu,  # TODO:
        "12": departure_search_menu,  # TODO:
    }

    print("Currently logged in as", current_user.first_name, current_user.last_name)
    while True:
        print("|1| Log out")
        print_default_menu()
        print("|8| Browse sold tickets")
        print("|9| Register a new seller")
        print("|10| Create a new flight")  # TODO: proverava se ispravnost unetih podataka
        print("|11| Edit flights")  # TODO: Omoguciti izmenu samo zeljenih podataka
        print("|12| Confirm deletion of a ticket")

        command = input()
        if command == '1':  # LOGOUT
            return
        elif command in command_dict:
            command_dict[command]

        valid = default_menu(command)
        if not valid and command not in command_dict:
            print("Unknown command, please enter a valid command")


def main():

    print("Welcome")
    print(datetime.now())
    while True:

        print("|1| Log in")
        print_default_menu()
        print("|8| Register as new user")
        command = input()

        if command == '1':

            global current_user
            username = input("Please enter your username: ")
            password = input("Please enter your password: ")
            current_user = authenticate_user(username, password)

            if current_user == None:
                print("Invalid credentials, please try logging in again")
            elif current_user.role == Role.Customer:
                customer_menu()
            elif current_user.role == Role.Seller:
                seller_menu()
            elif current_user.role == Role.Manager:
                manager_menu()

        current_user = None

        if command == '8':
            print("Please enter your credentials: ")
            register_handler()

        valid = default_menu(command)
        if not valid and command not in ['1', '8']:
            print("Unknown command, please enter a valid command")


if __name__ == "__main__":
    main()
