import globals
from utility import *
from datetime import *
from data_loader import *
from model.Enums import Role
from model.User import User
import seller_functions
import manager_functions
import string
import re
from globals import users, airports, airplanes, flights, departures, tickets, init, current_flight_id, current_ticket_id
from output_handler import *
import calendar
import copy
from sys import exit
local_user = None
customer = ""
self_purchase = False
self_check_in = False


def generate_departure_dates():
    global departures

    start_date = datetime.today() - timedelta(days = 1)
    end_date = datetime.today() + timedelta(days = 35)
    daysOftheWeek = ("ISO Week days start from 1", "mon", "tue", "wed", "thu", "fri", "sat", "sun")

    results = []
    #generate departures from flights
    current_date = start_date
    current_departure_id = int(departures[0].id)


    arrival_date = None
    while current_date <= end_date:
        for flight in flights:
            flight_days = flight.days
            flight_days= flight_days.rstrip().split(" ")
            if daysOftheWeek[current_date.isoweekday()] in flight_days:
                if flight.overnight == "Yes":
                    arrival_date = current_date + timedelta(days = 1)
                else:
                    arrival_date = current_date
                new_departure_id = f"{current_departure_id:04d}"
                departure = Departure(new_departure_id, flight.flight_number, current_date.date().strftime("%d-%m-%Y"),
                                      arrival_date.date().strftime("%d-%m-%Y"), flight, "0")
                results.append(departure)
                current_departure_id += 1

        current_date += timedelta(days=1)
    for departure_in_results, departure_in_departures in zip(results, departures):
        if departure_in_departures.id == departure_in_results.id:
            departure_in_results.seats_taken = departure_in_departures.seats_taken
    departures = results
    save_departures_to_file()
    #print_departure_search_table(results)
        #print(new_departure_id)


# TODO: Print all the date formating examples mm-dd-yyyy


def collect_optional_data(ticket, passenger=""):
    global local_user
    if passenger == "":
        if local_user.passport_number == "":
            while True:
                print("Please enter your passport number.")
                passport_number = input()
                if passport_number.isnumeric() is True and len(passport_number) == 9:
                    local_user.passport_number = passport_number
                    ticket.passport_number = passport_number
                    break
                else:
                    print("Invalid passport number. A valid number contains 9 digitis.")
        else:
            ticket.passport_number = local_user.passport_number

        if local_user.nationality == "":
            while True:
                print("Please enter your nationality")
                nationality = input()
                if nationality.isalpha() is True:
                    local_user.nationality = nationality
                    ticket.nationality = nationality
                    break
                else:
                    print("Nationality can only contain letters.")
        else:
            ticket.nationality = local_user.nationality

        if local_user.gender == "":
            while True:
                print("Please enter your gender (Male, Female, Other)")
                gender = input()
                if gender.lower() == "male" or gender.lower() == "female" or gender.lower() == "other":
                    local_user.gender = gender
                    ticket.gender = gender
                    break
                else:
                    print("Invalid gender.")
        else:
            ticket.gender = local_user.gender



    elif passenger == "Passenger":
        if ticket.passport_number == "":
            while True:
                print("Please enter the passenger's passport number.")
                passport_number = input()
                if passport_number.isnumeric() is True and len(passport_number) == 9:
                    ticket.passport_number = passport_number
                    break
                else:
                    print("Invalid passport number. A valid number contains 9 digitis.")

        if ticket.nationality == "":
            while True:
                print("Please enter the passenger's nationality")
                nationality = input()
                if nationality.isalpha() is True:
                    ticket.nationality = nationality
                    break
                else:
                    print("Nationality can only contain letters.")

        if ticket.gender == "":
            while True:
                print("Please enter the passenger's gender (Male, Female, Other)")
                gender = input()
                if gender.lower() == "male" or gender.lower() == "female" or gender.lower() == "other":
                    ticket.gender = gender
                    break
                else:
                    print("Invalid gender.")


def connected_flights():
    candidates = []
    connected = []
    found = False
    for ticket in tickets:
        if local_user.email == ticket.contact_email and ticket.for_deletion == "No":
            candidates.append(ticket)

    for ticket in candidates:
        if (local_user.email == ticket.contact_email
                and local_user.first_name == ticket.first_name
                and local_user.last_name == ticket.last_name
                and ticket.seat != ""):
            self_ticket = ticket
            found = True

        if (found is True
                and local_user.email == ticket.contact_email
                and local_user.first_name == ticket.first_name
                and local_user.last_name == ticket.last_name
                and ticket.departure.flight.departure_airport == self_ticket.departure.flight.destination_airport):
            connected.append(ticket)
    return connected
    # print_ticket(connected, "Multi")


def passenger_flights():
    candidates = []
    passenger_tickets = []
    found = False

    for ticket in tickets:
        if local_user.email == ticket.contact_email and ticket.for_deletion == "No":
            candidates.append(ticket)

    for ticket in candidates:
        if ( (local_user.first_name != ticket.first_name or local_user.last_name != ticket.last_name)
                and ticket.seat == ""):
            passenger_ticket = ticket
            found = True
        if found is True:
            passenger_tickets.append(passenger_ticket)
            found = False
    return passenger_tickets


def choose_seat(current_ticket):
    if current_ticket.seat != "":
        print("Already checked in.")
        return

    rows_cols = current_ticket.departure.flight.airplane.rows_cols
    rows = int(rows_cols.split("/")[0])  # 1,2,3,4...
    cols = int(rows_cols.split("/")[1])  # 1,2,3,4...
    alphabet = string.ascii_uppercase
    seating_table = [[0 for x in range(cols)] for x in range(rows)]
    # each ticket holds a field named seat
    # upon creation of a ticket object, the seat field is empty
    # upon check in this field is assigned a value in the form of 1A
    # to generate a table of available and taken seats for a departure we will extract the seat
    # data from the tickets which all contain the same departure id
    for i in range(rows):
        for j in range(cols):
            seating_table[i][j] = alphabet[j]

    for ticket in tickets:
        if ticket.departure.id == current_ticket.departure.id:
            seat = ticket.seat
            if seat != "":  # 1A
                row = int(seat[:-1])  # 1,2,3...
                col = ord(seat[-1]) - 64  # A -> 1, B -> 2...
                try:
                    seating_table[row - 1][col - 1] = "X"
                except:
                    print("Unexpected error occured")
    for i in range(rows):
        print("Row {:<2}".format(i + 1), ": ", end="")
        for j in range(cols):
            print(seating_table[i][j] + " ", end="")
        print("\n", end="")

    print(
        "Please choose a seat. For example 1A. Seats marked with an X are already taken. Enter 0 to return to previous menu.")
    while True:
        chosen_seat = input()
        if chosen_seat == "0":
            return
        if len(chosen_seat) in [2, 3] and chosen_seat[:-1].isnumeric() and chosen_seat[-1].isalpha():
            chosen_row = int(chosen_seat[:-1])
            chosen_col = chosen_seat[-1].upper()
            chosen_col = ord(chosen_col) - 64
            if chosen_row > rows or chosen_col > cols:
                print("Non-existent seat.")
                continue

            elif seating_table[chosen_row - 1][chosen_col - 1] == "X":
                print("Seat is already taken.")

            else:
                for ticket in tickets:
                    if current_ticket.id == ticket.id:
                        ticket.seat = chosen_seat[:-1] + chosen_seat[-1].upper()
                        save_tickets_to_file()
                        print("Check in successful. Your seat is", ticket.seat)
                        break
                break
        else:
            print("Invalid seat")


def check_in(option=""):
    global local_user
    global self_check_in
    candidates = []  # contains only the user's tickets
    connected = []  # contains the users connected flight tickets if the argument option == "Connected"
    passenger = []

    # if option == "": #contains users tickets before check in
    for ticket in tickets:
        if local_user.email == ticket.contact_email and ticket.for_deletion == "No":
            candidates.append(ticket)

    # if check in is for connected flgihts
    if option == "Connected":
        candidates = connected_flights()
        print_ticket(candidates, "Multi")

    elif option == "Passenger":
        candidates = passenger_flights()
        print_ticket(candidates, "Multi")

    while True:

        if option == "":
            print("Please enter a ticket ID. Enter 0 to return to previous menu")

        elif option == "Connected":
            print("Please enter a connected flight ticket ID. Enter 0 to return to previous menu")

        elif option == "Passenger":
            print("Please enter a passenger ticket ID. Enter 0 to return to previous menu")

        ticket_id = input()  # the user enters a ticket for which he wishes to check in

        ticket_is_valid = False

        for ticket in candidates:  # candidates contains the users tickets only
            if ticket_id == "0":  # the user wanted to go back - sentinel value
                return

            if ticket_id.upper() == ticket.id:
                ticket_is_valid = True
                current_ticket = ticket  # save the current ticket for use

                if current_ticket.seat != "":
                    print("Already checked in.")
                    return

                departure_datetime_obj = departure_datetime(ticket.departure.departure_date,
                                                            ticket.departure.flight.departure_time)  # takes the required date and time strings,
                check_in_datetime_obj = departure_datetime_obj - timedelta(hours=48)  # parses them, joins them and returns a datetime object
                current_datetime_obj = datetime.now()

                if current_datetime_obj >= check_in_datetime_obj and current_datetime_obj < departure_datetime_obj:
                    # collect missing data from the user - passport number, nationality and gender
                    # if option in ["","Connected"]:
                    if local_user.first_name == current_ticket.first_name and local_user.last_name == current_ticket.last_name:
                        collect_optional_data(current_ticket)
                        self_check_in = True

                    else:  # if option == "Passenger":
                        collect_optional_data(current_ticket, "Passenger")

                    save_customers_to_file()
                    choose_seat(current_ticket)
                    save_tickets_to_file()
                    return


                elif current_datetime_obj > departure_datetime_obj:
                    print("Sorry, your flight has already departed.")
                    return False

                else:
                    print("Check is not allowed until 48 hours before the departure of a flight")
                    print("You can check in at", check_in_datetime_obj)
                    return False

        if ticket_is_valid is False:
            print("Invalid ticked ID")


def check_in_menu():
    while True:
        print("You can check in 48 hours before your flight. Enter a ticket ID or search for it.")
        print("|0| Return to previous menu")
        print("|1| Enter ticket ID to check in")
        print("|2| View your unrealised tickets")
        choice = input()
        if choice == "0":
            return
        elif choice == "1":
            valid = check_in()  # check-in is valid if flight hasn't departed yet

            # check whether there are tickets purchased for passengers
            passenger_tickets = passenger_flights()

            if len(passenger_tickets) > 0: #and self_check_in is True: #TODO: Left off here
                while True and valid is not False:
                    print("Do you want to check in a passenger?")
                    print("|1| Yes")
                    print("|2| No")
                    command = input()

                    if command == "1":

                        # print_ticket(passenger_tickets, "Multi")
                        check_in("Passenger")
                        break
                    elif command == "2":
                        return
                    else:
                        print("Invalid command.")

            # check whether there are tickets purchased for connected flights
            connected_tickets = connected_flights()

            if len(connected_tickets) > 0 and self_check_in is True:
                while True and valid is not False:
                    print("Do you want to check in for your connected flights?")
                    print("|1| Yes")
                    print("|2| No")
                    command = input()

                    if command == "1":
                        check_in("Connected")
                        break
                    elif command == "2":
                        break
                    else:
                        print("Invalid command.")



        elif choice == "2":
            unrealised_tickets()
        else:
            print("Invalid command.")
    unrealised_tickets()


def unrealised_tickets():
    current_datetime_obj = datetime.now()
    candidates = []
    # user_tickets = []
    for ticket in tickets:
        departure_datetime_obj = departure_datetime(ticket.departure.departure_date,
                                                    ticket.departure.flight.departure_time)

        if (ticket.for_deletion == "No" and local_user.email == ticket.contact_email and departure_datetime_obj > current_datetime_obj):
            candidates.append(ticket)

    # return all the users tickets which havent been checked in and are on his name
    if len(candidates) > 0:
        print_ticket(candidates, "Multi")
    else:
        print("You have not purchased any tickets.")


def validate_departure_id(list=None):
    flight_id = ""
    valid = False
    result = None
    while flight_id == "" and valid is False:
        flight_id = input("Enter a departure ID. Enter 0 to return to previous menu\n")
        if flight_id == '0':
            return False
        if len(flight_id) == 4 and flight_id.isnumeric():
            if list is not None:
                for departure in list:  # we pass the optional parameter LIST if we want to validate flights
                    if flight_id == departure.id:  # only countained in that given list
                        result = departure  # else we will search the list of all departures
                        valid = True
                        break
            else:
                for departure in departures:
                    if flight_id == departure.id:
                        result = departure  # if the departure_id is valid we will get a reference to a departure object
                        valid = True
                        break

        if valid is False:
            print("Invalid departure ID")
            flight_id = ""
            continue

    if valid is True:
        if result.seats_taken >= result.flight.airplane.capacity:
            valid = False
            flight_id = ""
            print("Flight is full. Please choose another flight")
            return False

        current_datetime_obj = datetime.now()
        departure_datetime_obj = departure_datetime(result.departure_date, result.flight.departure_time)

        if current_datetime_obj >= departure_datetime_obj:
            print("Flight has already taken off.")
            return False
    return result


def purchase_ticket(departure, first_name="", last_name=""):
    global current_ticket_id
    current_ticket_id += 1
    ticket_id = "AA" + f"{current_ticket_id:04d}"  # takes a number and formats it into 4 digits with leading zeroes 2 --> 0002

    current_date_obj = datetime.today().date()
    current_date_str = current_date_obj.strftime("%d-%m-%Y")

    if first_name == "" and last_name == "":
        ticket = Ticket(ticket_id, departure, local_user.first_name, local_user.last_name, local_user.phone,
                        local_user.email, local_user.passport_number, local_user.nationality, local_user.gender,
                        current_date_str, "", "No")  # "" -> No seat assigned yet. "No" -> not q'd for deletion
    else:
        ticket = Ticket(ticket_id, departure, first_name.capitalize(), last_name.capitalize(), local_user.phone,
                        local_user.email, "", "", "", current_date_str, "", "No")

    tickets.append(ticket)
    departure.seats_taken += 1
    save_ticket_to_file(ticket)
    save_departures_to_file()

    print("Purchase successful.")
    print_ticket(ticket, "Single")


def purchase_tickets_menu():
    # This function is a mess, I am totally aware of that...
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

                arrival_datetime_obj = departure_datetime(departure.arrival_date, departure.flight.arrival_time)
                arrival_datetime_obj_delta = arrival_datetime_obj + timedelta(minutes=120)

                candidates = []
                search_criteria = create_search_dict()
                search_criteria["departure_airport"] = departure.flight.destination_airport.city
                candidates.extend(departure_search(departures, search_criteria))

                results = []
                for departure in candidates:
                    connected_datetime = departure_datetime(departure.departure_date, departure.flight.departure_time)
                    if connected_datetime >= arrival_datetime_obj and connected_datetime <= arrival_datetime_obj_delta:
                        results.append(departure)

                if len(results) > 0:

                    print("Do you wish to purchase a ticket for flights connected to your flight?")
                    print("|1| Yes")
                    print("|2| No")
                    selection = input()
                    if selection == "1":
                        print("Flights that depart no more than 120 minutes of your arrival,")
                        print_departure_search_table(results)
                        new_departure = validate_departure_id(
                            results)  # new departure will be inputted throught the validate departure function
                        # the function will only look for connected flights (results)

                        if new_departure is False:
                            return
                        print("Confirm the purchase of this ticket")
                        print("|1| Confirm")
                        print("|2| Abort purchase")
                        confirmation = input()
                        if confirmation == "1":
                            purchase_ticket(new_departure, first_name, last_name)
                            return
                            # customer_ticket =  purchase_ticket(new_departure, first_name, last_name)
                            # print_ticket(customer_ticket, "Single")

                        elif confirmation == "2":
                            return
                        else:
                            print("Invalid command. Please enter a valid command.")

                    elif selection == "2":
                        return
                    else:
                        print("Invalid command. Please enter a valid command.")
                else:
                    print("No connected flights to show.")
                    return None

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

            print("\nYou are now purchasing tickets for the following departure:")
            print_departure_search_table(departure, "Single")
            print()

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
        departure_dates.append((date + timedelta(days=i)).strftime("%d-%m-%Y"))  # adds and subtracts wanted number of
        # days from date, converts it into
        # european format and then appends
        # that date to an list
    for i in range(-int(arrival_days), int(arrival_days) + 1):
        date = datetime.strptime(arrival_date, "%d-%m-%Y").date()
        arrival_dates.append((date + timedelta(days=i)).strftime("%d-%m-%Y"))

    candidates = []
    for departure_date in departure_dates:
        search_criteria["departure_date"] = departure_date
        for arrival_date in arrival_dates:
            search_criteria["arrival_date"] = arrival_date
            candidates.extend(departure_search(departures, search_criteria))

    results = []
    current_datetime_obj = datetime.now()

    for departure in candidates:
        departure_datetime_obj = departure_datetime(departure.departure_date, departure.flight.departure_time)

        if departure_datetime_obj > current_datetime_obj:
            results.append(departure)

    print_departure_search_table(results)


def cheapest_flights_menu():

    search_criteria = create_search_dict()
    validate_city(search_criteria, "departure_airport", "Please enter a departure city name. Example: Belgrade\n")
    validate_city(search_criteria, "destination_airport", "Please enter a destination city name. Example: London\n")
    results = flight_search(flights, search_criteria)

    results.sort(key=lambda flight: flight.price)
    results = results[:10]
    results.reverse()

    print_flight_search_table(results)


def unrealised_departures():
    results = []
    current_datetime_obj = datetime.now()

    for departure in departures:
        departure_datetime_obj = departure_datetime(departure.departure_date, departure.flight.departure_time)

        if departure_datetime_obj > current_datetime_obj:
            results.append(departure)

    print_departure_search_table(results)


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

            # actually should be called validate date or time
            # if we pass "Time" into the time parameter it will validate time


def datetime_input(search_criteria, key, text, time=""):  # use this when passing data into a dictionary
    valid = False  # we force the user to enter a correct date or time by validaing it
    while search_criteria[key] == "" and valid == False:
        search_criteria[key] = input(text)
        valid = validate_datetime(search_criteria[key], time)
        if not valid:
            search_criteria[key] = ""
    return search_criteria[key]


def validate_city(search_criteria, key, text):  # dict, key for dict
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
            validate_city(search_criteria, "departure_airport", "Please enter a departure city name. Example: Belgrade\n")

        if '2' in choices:
            validate_city(search_criteria, "destination_airport", "Please enter a destination city name. Example: London\n")

        if '3' in choices:
            datetime_input(search_criteria, "departure_date", "Please enter a departure date in the format of dd-mm-yyyy\n")

        if '4' in choices:
            datetime_input(search_criteria, "arrival_date", "Please enter an arrival date in the format of dd-mm-yyyy\n")

        if '5' in choices:
            datetime_input(search_criteria, "departure_time", "Please enter a departure time in the format of HH:MM\n",
                           "Time")

        if '6' in choices:
            datetime_input(search_criteria, "arrival_time", "Please enter an arrival time in the format of HH:MM\n",
                           "Time")

        if '7' in choices:
            while search_criteria["airline"] == "":
                search_criteria["airline"] = input("Please enter airline\n")
        if valid:
            if end == "Return":
                return departure_search(departures, search_criteria)
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
    list_of_emails = [user.email for user in users if user.role == Role.Customer]

    print("Fields marked with an * are required")
    while username == "":
        username = input("Username*: ")
        if '|' in username:
            print("Username cannot contain the character \"|\"")
            username = ""

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
        elif email in list_of_emails:
            print("Email address already taken, please enter a different email address")
            email = ""

    passport_number = input("(Press enter to skip) Passport number:")
    while passport_number != "":
        if len(passport_number) != 9 or not passport_number.isnumeric():
            print("Passport number can only contain digits and must be 9 digits long")
            passport_number = input("Passport number: ")
        else:
            break

    nationality = input("(Press enter to skip) Nationality: ")
    while nationality != "":
        if not nationality.isalpha():
            print("Please enter only letters")
            nationality = input("nationality: ")
        else:
            break

    gender = input("(Press enter to skip) Gender: ")
    while gender != "":
        if not gender.isalpha():
            print("Please enter only letters")
            gender = input("Nationality: ")
        else:
            break

    register_user(username, password, first_name, last_name, phone, email, passport_number, nationality, gender)


def register_user(username, password, first_name, last_name, phone, email, passport_number, nationality, gender):
    user = Customer(username, password, first_name.capitalize(), last_name.capitalize(), phone, email, passport_number, nationality, gender)
    users.append(user)
    save_customer_to_file(user)
    print("Successfully registered! You may now log in")


def save_customer_to_file(user):
    with open("data/customers", "a") as f:
        f.write(str(user.serialize()) + "\n")


def save_customers_to_file():
    with open("data/customers", "w") as f:
        for user in users:
            if user.role == Role.Customer:
                f.write(str(user.serialize()) + "\n")


def save_departures_to_file():
    with open("data/departures", "w") as f:
        for departure in departures:
            f.write(departure.serialize() + "\n")


def save_ticket_to_file(ticket):
    with open("data/tickets", "a") as f:
        f.write(str(ticket.serialize()) + "\n")

    with open("data/current_ticket_id", "w") as f:
        f.write(str(current_ticket_id))


def save_tickets_to_file():
    with open("data/tickets", "w") as f:
        for ticket in tickets:
            f.write(ticket.serialize() + "\n")


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
            cheapest_flights_menu()
        else:
            command_dict[command]()
        return True
    return False


def customer_menu():
    command_dict = {
        "8": purchase_tickets_menu,
        "9": unrealised_tickets,
        "10": check_in_menu,
    }

    print("Currently logged in as", local_user.first_name, local_user.last_name)
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
        "8": seller_functions.purchase_tickets_menu,
        "9": seller_functions.check_in_menu,
        "10": seller_functions.edit_ticket_menu,
        "11": seller_functions.delete_ticket_menu,
        "12": seller_functions.ticket_search_menu,
    }

    print("Currently logged in as", globals.current_user.first_name, globals.current_user.last_name)
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
        "8": seller_functions.ticket_search_menu,
        "9": manager_functions.register_seller,
        "10": manager_functions.create_new_flight,
        "11": manager_functions.edit_flights_menu,
        "12": manager_functions.delete_tickets_menu,
        "13": manager_functions.generate_reports
    }

    print("Currently logged in as", globals.current_user.first_name, globals.current_user.last_name)
    while True:
        print("|1| Log out")
        print_default_menu()
        print("|8| Browse sold tickets")
        print("|9| Register a new seller")
        print("|10| Create a new flight")
        print("|11| Edit flights")
        print("|12| Confirm deletion of a ticket")
        print("|13| Reports menu")

        command = input()
        if command == "1":  # LOGOUT
            return

        elif command in command_dict:
            command_dict[command]()

        valid = default_menu(command)
        if not valid and command not in command_dict:
            print("Unknown command, please enter a valid command")


def main():

    init()
    print("Welcome!")
    print("Current date and time:", datetime.now().replace(microsecond=0))
    generate_departure_dates()
    #test1()
    while True:

        print("|1| Log in")
        print_default_menu()
        print("|8| Register as new user")

        command = input()

        if command == '1':

            username = input("Please enter your username: ")
            password = input("Please enter your password: ")
            user = authenticate_user(username, password)

            #global current_user
            if user == None:
                print("Invalid credentials, please try logging in again")
            elif user.role == Role.Customer:
                global local_user
                local_user = user
                customer_menu()

            elif user.role == Role.Seller:
                globals.current_user = user     # log the user in as a seller
                seller_menu()           # let him use the seller's menus
            elif user.role == Role.Manager:
                globals.current_user = user     # log the user in as a manager
                manager_menu()          # let him use the manager's menus

        # when he is done log him out
        globals.current_user = None

        if command == '8':
            print("Please enter your credentials: ")
            register_handler()

        valid = default_menu(command)
        if not valid and command not in ['1', '8', '9']:
            print("Unknown command, please enter a valid command")


if __name__ == "__main__":
    main()
