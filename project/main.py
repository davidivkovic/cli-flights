from utility import *
from datetime import *
from data_loader import *
from model.Enums import Role
from model.User import User
import seller_functions
import manager_functions
import string
import re
import globals

users = load_users()
airports = load_airports()
airplanes = load_airplanes()
flights = load_flights(airports, airplanes)
departures = load_departures(flights, airplanes)
tickets = load_tickets(departures)
current_user = None
customer = ""
self_purchase = False
self_check_in = False

#TODO: Print all the date formating examples m-d-yyyy

def departure_datetime(departure_date, departure_time):
    departure_date_obj = datetime.strptime(departure_date, "%d-%m-%Y").date()
    departure_time_obj = datetime.strptime(departure_time, "%H:%M").time()
    departure_datetime_obj = datetime.combine(departure_date_obj, departure_time_obj)
    return departure_datetime_obj


def collect_optional_data(ticket, passenger = ""):

    global current_user
    if passenger == "":
        if current_user.passport_number == "":
            while True:
                print("Please enter your passport number.")
                passport_number = input()
                if passport_number.isnumeric() is True and len(passport_number) == 9:
                    current_user.passport_number = passport_number
                    ticket.passport_number = passport_number
                    break
                else:
                    print("Invalid passport number. A valid number contains 9 digitis.")
        else:
            ticket.passport_number = current_user.passport_number

        if current_user.nationality == "":
            while True:
                print("Please enter your nationality")
                nationality = input()
                if nationality.isalpha() is True:
                    current_user.nationality = nationality
                    ticket.nationality = nationality
                    break
                else:
                    print("Nationality can only contain letters.")
        else:
            ticket.nationality = current_user.nationality
        
        if current_user.gender == "":
            while True:
                print("Please enter your gender (Male, Female, Other)")
                gender = input()
                if gender.lower() == "male" or gender.lower() == "female" or gender.lower() == "other":
                    current_user.gender = gender
                    ticket.gender = gender
                    break
                else:
                    print("Invalid gender.")
        else:
            ticket.gender = current_user.gender
    
    
    
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
        if current_user.email == ticket.contact_email and ticket.for_deletion == "No":
            candidates.append(ticket)

    for ticket in candidates:
        if (current_user.email == ticket.contact_email
            and current_user.first_name == ticket.first_name
            and current_user.last_name == ticket.last_name
            and ticket.seat != ""):

            self_ticket = ticket
            found = True

        if (found is True
            and current_user.email == ticket.contact_email
            and current_user.first_name == ticket.first_name
            and current_user.last_name == ticket.last_name
            and ticket.departure.flight.departure_airport == self_ticket.departure.flight.destination_airport):

            connected.append(ticket)
    return connected
    #print_ticket(connected, "Multi")


def passenger_flights():

    candidates = []
    passenger_tickets = []
    found = False

    for ticket in tickets:
        if current_user.email == ticket.contact_email and ticket.for_deletion == "No":
            candidates.append(ticket)

    for ticket in candidates:
        if (current_user.email == ticket.contact_email
                and (current_user.first_name != ticket.first_name or current_user.last_name != ticket.last_name)
                and ticket.seat == ""):
            passenger_ticket = ticket
            found = True
        if found is True:
            passenger_tickets.append(passenger_ticket)
    return passenger_tickets


def choose_seat(current_ticket):

    if current_ticket.seat !="":
        print("Already checked in.")
        return

    rows_cols = current_ticket.departure.flight.airplane.rows_cols
    rows = int(rows_cols.split("/")[0])  #1,2,3,4...
    cols = int(rows_cols.split("/")[1])  #1,2,3,4...
    alphabet = string.ascii_uppercase
    seating_table = [[0 for x in range(cols)] for x in range(rows)]
    #each ticket holds a field named seat
    #upon creation of a ticket object, the seat field is empty
    #upon check in this field is assigned a value in the form of 1A
    #to generate a table of available and taken seats for a departure we will extract the seat
    #data from the tickets which all contain the same departure id
    for i in range(rows):
        for j in range(cols):
            seating_table[i][j] = alphabet[j]


    for ticket in tickets:
        if ticket.departure.id == current_ticket.departure.id:
            seat = ticket.seat
            if seat != "":               #1A
                row = int(seat[:-1])       # 1,2,3...
                col = ord(seat[-1]) - 64  # A -> 1, B -> 2...
                seating_table[row-1][col-1] = "X"

    for i in range(rows):
        print("Row {:<2}".format(i + 1), ": ", end = "")
        for j in range(cols):
            print(seating_table[i][j] + " ", end = "")
        print("\n", end = "")

    print("Please choose a seat. For example 1A. Seats marked with an X are already taken. Enter 0 to return to previous menu.")
    while True:
        chosen_seat = input()
        if chosen_seat == "0":
            return
        if len(chosen_seat) in [2,3] and chosen_seat[:-1].isnumeric() and chosen_seat[-1].isalpha():
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
        else:
            print("Invalid seat")


def check_in(option = ""):

    global current_user
    global self_check_in
    candidates = []  # contains only the user's tickets
    connected = []  #contains the users connected flight tickets if the argument option == "Connected"
    passenger = []

    #if option == "": #contains users tickets before check in
    for ticket in tickets:
        if current_user.email == ticket.contact_email and ticket.for_deletion == "No":
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

        ticket_id = input()             # the user enters a ticket for which he wishes to check in

        ticket_is_valid = False

        for ticket in candidates:       #candidates contains the users tickets only
            if ticket_id == "0":        #the user wanted to go back - sentinel value
                return

            if ticket_id.upper() == ticket.id:
                ticket_is_valid = True
                current_ticket = ticket #save the current ticket for use

                if current_ticket.seat != "":
                    print("Already checked in.")
                    return

                departure_datetime_obj = departure_datetime(ticket.departure.departure_date, ticket.departure.flight.departure_time) # takes the required date and time strings,
                check_in_datetime_obj = departure_datetime_obj - timedelta(hours = 48)                                               # parses them, joins them and returns a datetime object
                current_datetime_obj = datetime.now()

                if current_datetime_obj >= check_in_datetime_obj and current_datetime_obj < departure_datetime_obj:
                    #collect missing data from the user - passport number, nationality and gender
                    #if option in ["","Connected"]:
                    if current_user.first_name == current_ticket.first_name and current_user.last_name == current_ticket.last_name:
                        collect_optional_data(current_ticket)
                        self_check_in = True

                    else: #if option == "Passenger":
                        collect_optional_data(current_ticket, "Passenger")

                    save_customers_to_file()
                    choose_seat(ticket)
                    save_tickets_to_file()
                    return


                elif current_datetime_obj > departure_datetime_obj:
                    print("Sorry, your flight has already departed.")
                    return False

                else:
                    print("Check is not allowed until 48 hours before the departure of a flight")
                    print("You can check in at",  check_in_datetime_obj)
                    return False



        if ticket_is_valid is False:
            print("Invalid ticked ID")

#TODO: If he tries to check in for a passenger first no not take data from the current user - DONE
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
            valid = check_in() #check-in is valid if flight hasn't departed yet

            #check whether there are tickets purchased for connected flights
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

            # check whether there are tickets purchased for passengers
            passenger_tickets = passenger_flights()

            if len(passenger_tickets) > 0 and self_check_in is True:
                while True and valid is not False:
                    print("Do you want to check in a passenger?")
                    print("|1| Yes")
                    print("|2| No")
                    command = input()

                    if command == "1":

                        #print_ticket(passenger_tickets, "Multi")
                        check_in("Passenger")
                        break
                    elif command == "2":
                        return
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
    #user_tickets = []
    for ticket in tickets:
        departure_datetime_obj = departure_datetime(ticket.departure.departure_date, ticket.departure.flight.departure_time)

        if (ticket.for_deletion == "No" and current_user.email == ticket.contact_email
            and departure_datetime_obj > current_datetime_obj):
            candidates.append(ticket)

    #return all the users tickets which havent been checked in and are on his name
    if len(candidates) > 0:
        print_ticket(candidates, "Multi")
    else:
        print("You have not purchased any tickets.")

# here is where we check if the departure is full or not
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
                for departure in list:                 # we pass the optional parameter LIST if we want to validate flights
                    if flight_id == departure.id:      # only countained in that given list
                        result = departure             # else we will search the list of all departures
                        valid = True
                        break
            else:
                for departure in departures:
                    if flight_id == departure.id:
                        result = departure            #if the departure_id is valid we will get a reference to a departure object
                        valid = True
                        break

    if valid is False:
        print("Invalid departure ID")
        flight_id = ""

    elif valid is True:
        if result.seats_taken == result.capacity:
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

# Takes a single ticket and prints it if mode is "Single"
# Takes a list of tickets and prints them all if mode is "Multi"
def print_ticket(ticket, mode):

    # print the default table header
    print("{:12}{:14}{:16}{:16}{:22}{:22}{:24}{:20}{:30}{:20}{:20}".format("Ticket ID", "Departure ID", "From", "To",
                                                                           "Departure date", "Arrival date",
                                                                           "Ticket holder",
                                                                           "Contact phone",
                                                                           "Contact email", "Date of purchase", "Seat"))
    if mode == "Single":    # we pass one single ticket - a non iterable
        if ticket.seat == "":
            seat = "Not checked in"
        else:
            seat = ticket.seat
        print("{:12}{:14}{:16}{:16}{:22}{:22}{:24}{:20}{:30}{:20}{:20}".format(ticket.id, ticket.departure.id,
                                                                          ticket.departure.flight.departure_airport.city,
                                                                          ticket.departure.flight.destination_airport.city,
                                                                          ticket.departure.departure_date + " at " +
                                                                          ticket.departure.flight.departure_time,
                                                                          ticket.departure.arrival_date + " at " +
                                                                          ticket.departure.flight.arrival_time,
                                                                          ticket.first_name + " " + ticket.last_name,
                                                                          ticket.contact_phone,
                                                                          ticket.contact_email,
                                                                          ticket.purchase_date,
                                                                          seat))
    elif mode == "Multi":  # we pass a list of tickets to print - iterable
        tickets = ticket   # so in order to overload we declare a list called tickets and assign it the paramter's list
        for ticket in tickets:
            if ticket.seat == "":
                seat = "Not checked in"
            else:
                seat = ticket.seat
            print("{:12}{:14}{:16}{:16}{:22}{:22}{:24}{:20}{:30}{:20}{:20}".format(ticket.id, ticket.departure.id,
                                                                              ticket.departure.flight.departure_airport.city,
                                                                              ticket.departure.flight.destination_airport.city,
                                                                              ticket.departure.departure_date + " at " +
                                                                              ticket.departure.flight.departure_time,
                                                                              ticket.departure.arrival_date + " at " +
                                                                              ticket.departure.flight.arrival_time,
                                                                              ticket.first_name + " " + ticket.last_name,
                                                                              ticket.contact_phone,
                                                                              ticket.contact_email,
                                                                              ticket.purchase_date,
                                                                              seat))


def purchase_ticket(departure, first_name="", last_name=""):

    globals.current_ticket_id += 1
    ticket_id = "AA" + f"{globals.current_ticket_id:04d}"  # takes a number and formats it into 4 digits with leading zeroes 2 --> 0002

    current_date_obj = datetime.today().date()
    current_date_str = current_date_obj.strftime("%#d-%#m-%Y")
    print(current_date_str)
    # validate_ticket_id()

    if first_name == "" and last_name == "":
        ticket = Ticket(ticket_id, departure, current_user.first_name, current_user.last_name, current_user.phone,
                        current_user.email, current_user.passport_number, current_user.nationality, current_user.gender,
                        current_date_str, "" ,"No")     # "" -> No seat assigned yet. "No" -> not q'd for deletion
    else:
        ticket = Ticket(ticket_id, departure, first_name.capitalize(), last_name.capitalize(), current_user.phone,
                        current_user.email, "", "", "", current_date_str, "", "No")

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
                        new_departure = validate_departure_id(results)   #new departure will be inputted throught the validate departure function
                                                                         #the function will only look for connected flights (results)

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
    current_datetime_obj = datetime.now()

    for departure in candidates:
        departure_datetime_obj = departure_datetime(departure.departure_date, departure.flight.departure_time)

        if departure_datetime_obj > current_datetime_obj:
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
    current_datetime_obj = datetime.now()

    for departure in departures:
        departure_datetime_obj = departure_datetime(departure.departure_date, departure.flight.departure_time)

        if departure_datetime_obj > current_datetime_obj:
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
            print("Incorrect time. Please enter a valid time.")  # TODO: Unhardcode this. Move this function into utils, and the prints into main
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

                                                            # actually should be called validate date or time
                                                            # if we pass "Time" into the time parameter it will validate time


def datetime_input(search_criteria, key, text, time=""):    # use this when passing data into a dictionary
    valid = False                                           # we force the user to enter a correct date or time by validaing it
    while search_criteria[key] == "" and valid == False:
        search_criteria[key] = input(text)
        valid = validate_datetime(search_criteria[key], time)
        if not valid:
            search_criteria[key] = ""
    return search_criteria[key]


def validate_city(search_criteria, key, text):          # dict, key for dict
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
            if end == "Return":
                return departure_search(departures, search_criteria)
            print_departure_search_table(departure_search(departures, search_criteria))
            if end == "End":
                break



def authenticate_user(username, password, ):
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

    nationality = input("Nationality: ")
    while nationality != "":
        if not nationality.isalpha():
            print("Please enter only letters")
            nationality = input("nationality: ")
        else:
            break

    gender = input("Gender: ")
    while gender != "":
        if not gender.isalpha():
            print("Please enter only letters")
            gender = input("Nationality: ")
        else:
            break

    register_user(username, password, first_name, last_name, phone, email, passport_number, nationality, gender)


def register_user(username, password, first_name, last_name, phone, email, passport_number, nationality, gender):
    user = Customer(username, password, first_name, last_name, phone, email, passport_number, nationality, gender)
    users.append(user)
    save_customer_to_file(user)


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
        f.write(str(globals.current_ticket_id))


def save_tickets_to_file():
    with open("data/tickets", "w") as f:
        for ticket in tickets:
            f.write(ticket.serialize() + "\n")


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
        "11": departure_search_menu,  # TODO:
        "12": departure_search_menu,  # TODO:
    }

    print("Currently logged in as", globals.current_user.first_name, globals.current_user.last_name)
    while True:
        print("|1| Log out")
        print_default_menu()
        print("|8| Browse sold tickets")
        print("|9| Register a new seller")
        print("|10| Create a new flight")  # TODO: proverava se ispravnost unetih podataka
        print("|11| Edit flights")  # TODO: Omoguciti izmenu samo zeljenih podataka
        print("|12| Confirm deletion of a ticket")
        print("|13| Reports menu")

        command = input()
        if command == "1":  # LOGOUT
            return

        elif command == "9":
            seller = manager_functions.register_seller()
            users.append(seller)
            continue

        elif command == "10":
            #flight = \
            manager_functions.create_new_flight()
            #flights.append(flight)
            continue

        elif command in command_dict:
            command_dict[command]()

        valid = default_menu(command)
        if not valid and command not in command_dict:
            print("Unknown command, please enter a valid command")


def main():

    print("Welcome")
    print("Current date and time:", datetime.now().replace(microsecond=0))
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
                globals.current_user = current_user
                seller_menu()
                globals.current_user = None
            elif current_user.role == Role.Manager:
                globals.current_user = current_user
                manager_menu()
                globals.current_user = None

        current_user = None

        if command == '8':
            print("Please enter your credentials: ")
            register_handler()

        valid = default_menu(command)
        if not valid and command not in ['1', '8']:
            print("Unknown command, please enter a valid command")


if __name__ == "__main__":
    main()
