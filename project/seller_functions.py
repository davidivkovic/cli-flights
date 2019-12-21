from model.Ticket import Ticket
from model.Enums import Role
from main import users, departures, tickets, save_ticket_to_file, save_tickets_to_file, save_departures_to_file, \
    departure_search_menu, validate_departure_id, print_ticket, datetime_input, validate_city, \
    departure_datetime, save_customers_to_file, save_customer_to_file, print_departure_search_table, choose_seat
import globals
import re
import string
from utility import *
from datetime import *


# TODO: Also show checked-in tickets in unrealised tickets

# redone
def purchase_ticket(departure, first_name, last_name, phone, email):
    #global current_ticket_id#, current_user
    globals.current_ticket_id += 1
    ticket_id = "AA" + f"{globals.current_ticket_id:04d}"  # takes a number and formats it into 4 digits with leading zeroes 2 --> 0002

    current_date_obj = datetime.today().date()
    current_date_str = current_date_obj.strftime("%#d-%#m-%Y")

    registered_user = None

    # we search whether the user is registered in the system, if yes then we save a reference to him
    for user in users:
        if user.first_name == first_name and user.last_name == last_name and user.email == email:
            registered_user = user
            break

    if registered_user is None:
        ticket = Ticket(ticket_id, departure, first_name.capitalize(), last_name.capitalize(), phone,
                        email, "", "", "", current_date_str, "", "No",
                        globals.current_user.first_name + " " + globals.current_user.last_name)
        # "" -> No seat assigned yet. "No" -> not q'd for deletion
    else:  # the user has not been found as registered in the system
        ticket = Ticket(ticket_id, departure, user.first_name, user.last_name,
                        user.phone, user.email, user.passport_number,
                        user.nationality, user.gender, current_date_str, "", "No",
                        globals.current_user.first_name + " " + globals.current_user.last_name)  # current global user is the seller, we mark his name

    tickets.append(ticket)
    departure.seats_taken += 1
    save_ticket_to_file(ticket)
    save_departures_to_file()

    print("Purchase successful.")
    print_ticket(ticket, "Single")


# redone
def purchase_tickets_menu():
    # This function is a mess, I am totally aware of that...

    def holder_menu():
        first_name, last_name, phone, email = "", "", "", ""


        while True:
            print("Is the customer already registered?")
            print("|1| Yes")
            print("|2| No")
            command = input()

            if command == "1":
                while True:
                    print("Please enter the customer's username")
                    username = input()
                    for user in users:
                        if user.username == username:
                            return user.first_name, user.last_name, user.phone, user.email
                    print("User not found")

            elif command == "2":
                break
                # we continue and ask for the customers first and last name phone and email
            else:
                print("Ivalid command")

        print("Please enter the first and last name of the customer.")

        while first_name == "":
            first_name = input("First name:\n")
            if not first_name.isalpha():
                print("Please enter only letters")
                first_name = ""

        while last_name == "":
            last_name = input("Last name:\n")
            if not last_name.isalpha():
                print("Please enter only letters")

        # for user in users:
        #     if (user.role == Role.Customer
        #             and user.first_name.lower() == first_name.lower()
        #             and user.last_name.lower() == last_name.lower()):
        #         unused = input("Please enter the customer's username")  # TODO: NEW project specification
        #         # registered_user = user #The entered user has been found and saved to extract passport data for later on
        #         return user.first_name, user.last_name, user.phone, user.email

        # if registered_user is None: #if the entered user has not been found we will take his personal data
        while phone == "":
            phone = input("Phone number*: ")
            if '|' in phone:
                print("Phone number cannot contain the character \"|\"")

        while email == "":
            email = input("Email address*: ")
            if not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                print("Please enter a valid email address")
                email = ""

        return first_name, last_name, phone, email

    def confirmation_menu(departure, first_name, last_name, phone, email):
        while True:
            print("Confirm the purchase of this ticket")
            print("|1| Confirm")
            print("|2| Abort purchase")
            confirmation = input()
            if confirmation == "1":

                customer_ticket = purchase_ticket(departure, first_name, last_name, phone, email)  # generate new ticket
                passenger_ticket_menu(departure, phone, email)  # ask seller if the customer wants to buy a ticket for a passenger
                connected_departures_menu(departure, first_name, last_name, phone, email)  # ask seller if the customer wants to but a ticket for connected flights
                return

            elif confirmation == "2":
                return
            else:
                print("Invalid command. Please enter a valid command.")

    def passenger_ticket_menu(departure, phone, email):
        first_name, last_name = "", ""
        while True:
            print("Does the customer wish to purchase tickets for a passenger?")
            print("|1| Yes")
            print("|2| No")

            selection = input()
            if selection == "1":

                customer = "Other"
                print("Please enter the first and last name of the customer's passenger.")

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
                        purchase_ticket(departure, first_name, last_name, phone, email)  # TODO: Look into this
                        return

                    elif confirmation == "2":
                        return
                    else:
                        print("Invalid command. Please enter a valid command.")

            elif selection == "2":
                return
            else:
                print("Invalid command. Please enter a valid command.")

    def connected_departures_menu(departure, first_name, last_name, phone, email):

        arrival_datetime_obj = departure_datetime(departure.arrival_date, departure.flight.arrival_time)
        arrival_datetime_obj_delta = arrival_datetime_obj + timedelta(minutes=120)

        candidates = []
        search_criteria = create_search_dict()
        search_criteria["departure_airport"] = departure.flight.destination_airport.city
        candidates.extend(departure_search(departures, search_criteria))

        results = []

        while True:
            for departure in candidates:
                connected_datetime = departure_datetime(departure.departure_date, departure.flight.departure_time)

                if connected_datetime >= arrival_datetime_obj and connected_datetime <= arrival_datetime_obj_delta:
                    results.append(departure)

            if len(results) > 0:

                print("Does the customer wish to purchase tickets for flights connected to his flight?")
                print("|1| Yes")
                print("|2| No")
                selection = input()
                if selection == "1":
                    print("Flights that depart no more than 120 minutes of the customer's arrival.")
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
                        purchase_ticket(new_departure, first_name, last_name, phone, email)
                        return

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
        print("|1| Enter the departure ID for the ticket you wish to sell")
        print("|2| Look up departure IDs by a single criteria")
        print("|3| Look up departure IDs by multiple criteria")
        choice = input()

        if choice == "0":
            return

        elif choice == "1":

            departure = validate_departure_id()
            if departure is False:
                continue

            print("\nCurrently selling tickets for departure:")
            print_departure_search_table(departure, "Single")
            print()

            first_name, last_name, phone, email = holder_menu()  #
            confirmation_menu(departure, first_name, last_name, phone, email)


        elif choice == "2":
            departure_search_menu("End")
        elif choice == "3":
            departure_search_menu("End", "Multi")
        else:
            print("Invalid input")
            choice = ""


# redone
def collect_optional_data(user, ticket, passenger=""):
    if passenger == "":
        if user.passport_number == "":
            while True:
                print("Please enter your passport number.")
                passport_number = input()
                if passport_number.isnumeric() is True and len(passport_number) == 9:
                    user.passport_number = passport_number
                    ticket.passport_number = passport_number
                    break
                else:
                    print("Invalid passport number. A valid number contains 9 digitis.")
        else:
            ticket.passport_number = user.passport_number

        if user.nationality == "":
            while True:
                print("Please enter your nationality")
                nationality = input()
                if nationality.isalpha() is True:
                    user.nationality = nationality
                    ticket.nationality = nationality
                    break
                else:
                    print("Nationality can only contain letters.")
        else:
            ticket.nationality = user.nationality

        if user.gender == "":
            while True:
                print("Please enter your gender (Male, Female, Other)")
                gender = input()
                if gender.lower() == "male" or gender.lower() == "female" or gender.lower() == "other":
                    cuser.gender = gender
                    ticket.gender = gender
                    break
                else:
                    print("Invalid gender.")
        else:
            ticket.gender = user.gender



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


# redone
def connected_flights(user):
    candidates = []
    connected = []
    found = False
    for ticket in tickets:
        if user.email == ticket.contact_email and ticket.for_deletion == "No":
            candidates.append(ticket)

    for ticket in candidates:
        if (user.first_name == ticket.first_name
                and user.last_name == ticket.last_name
                and ticket.seat != ""):
            self_ticket = ticket
            found = True

        if (
                found is True and ticket.departure.flight.departure_airport == self_ticket.departure.flight.destination_airport):
            connected.append(ticket)
    # print_ticket(connected, "Multi")
    return connected


# redone
def passenger_flights(user):
    candidates = []
    passenger_tickets = []
    found = False
    departure_id = ""

    # find the tickets that the user has already checked in for
    for ticket in tickets:
        if user.email == ticket.contact_email and ticket.seat != "" and ticket.for_deletion == "No":
            departure_id = ticket.departure.id
            break

    for ticket in tickets:
        if (user.email == ticket.contact_email and ticket.seat == ""
                and ticket.departure.id == departure_id and ticket.for_deletion == "No"):
            candidates.append(ticket)

    return candidates


def check_in(option="", user_obj=None):
    candidates = []  # contains only the user's tickets
    connected = []  # contains the users connected flight tickets if the argument option == "Connected"
    passenger = []

    # if check-in is for connected flgihts
    if option == "":
        candidates = [ticket for ticket in tickets if ticket.for_deletion == "No"]

    if option == "Connected":
        candidates = connected_flights(user_obj)
        print_ticket(candidates, "Multi")
    #
    elif option == "Passenger":
        candidates = passenger_flights(user_obj)
        print_ticket(candidates, "Multi")

    while True:

        if option == "":
            print("Please enter a ticket ID. Enter 0 to return to previous menu")

        elif option == "Connected":
            print("Please enter a connected flight ticket ID. Enter 0 to return to previous menu")

        elif option == "Passenger":
            print("Please enter a passenger ticket ID. Enter 0 to return to previous menu")

        ticket_id = input()

        ticket_is_valid = False

        for ticket in candidates:
            if ticket_id == "0":  # user wanted to go back - sentinel value
                return
            if ticket_id.upper() == ticket.id:
                ticket_is_valid = True
                current_ticket = ticket  # save the current ticket for use

                if current_ticket.seat != "":
                    print("Already checked in.")
                    return

                departure_datetime_obj = departure_datetime(ticket.departure.departure_date,
                                                            ticket.departure.flight.departure_time)
                check_in_datetime_obj = departure_datetime_obj - timedelta(hours=48)
                current_datetime_obj = datetime.now()

                if current_datetime_obj >= check_in_datetime_obj and current_datetime_obj < departure_datetime_obj:  # We check if flight has departed yet
                    # collect missing data from the user - passport number, nationality and gender
                    customers = [user for user in users if user.role == Role.Customer]
                    for user in customers:
                        if user.first_name == current_ticket.first_name and user.last_name == current_ticket.last_name and user.email == current_ticket.contact_email:
                            collect_optional_data(user, current_ticket)
                            break

                    for user in customers:
                        if (
                                user.first_name != current_ticket.first_name or user.last_name != current_ticket.last_name) and user.email == current_ticket.contact_email:
                            collect_optional_data(user, current_ticket, "Passenger")
                            break

                    save_customers_to_file()
                    choose_seat(ticket)
                    save_tickets_to_file()
                    return user


                elif current_datetime_obj > departure_datetime_obj:
                    print("Sorry, the flight has already departed.")
                    return False

                else:
                    print("Check is not allowed until 48 hours before the departure of a flight")
                    print("You can check the customer in at", check_in_datetime_obj)
                    return False

        if ticket_is_valid is False:
            print("Invalid ticked ID")


# TODO: If he tries to check in for a passenger first no not take data from the current user - DONE
def check_in_menu():
    while True:
        print("You can check a customer in 48 hours before his flight. Enter a ticket ID or search for it.")
        print("|0| Return to previous menu")
        print("|1| Enter ticket ID to check a customer in")
        print("|2| Search tickets")
        choice = input()
        if choice == "0":
            return
        elif choice == "1":

            user = check_in()  # check-in is valid if flight hasn't departed yet and will return the user that checked in
            # else user is False - it should be None though
            # check whether there are tickets purchased for connected flights
            if user is not False:
                connected_tickets = connected_flights(user)

                if len(connected_tickets) > 0:
                    while True and user is not False:
                        print("Do you want to check in for your connected flights?")
                        print("|1| Yes")
                        print("|2| No")
                        command = input()

                        if command == "1":
                            check_in("Connected", user)
                            break
                        elif command == "2":
                            break
                        else:
                            print("Invalid command.")

                # check whether there are tickets purchased for passengers
                passenger_tickets = passenger_flights(user)

                if len(passenger_tickets) > 0:
                    while True and user is not False:
                        print("Do you want to check in a passenger?")
                        print("|1| Yes")
                        print("|2| No")
                        command = input()

                        if command == "1":

                            # print_ticket(passenger_tickets, "Multi")
                            check_in("Passenger", user)
                            break
                        elif command == "2":
                            return
                        else:
                            print("Invalid command.")

        elif choice == "2":
            ticket_search_menu()
        else:
            print("Invalid command.")


def ticket_search_menu():
    search_criteria = create_search_dict_ticket()

    validate_city(search_criteria, "departure_airport", "Please enter a departure city name. Example: Belgrade\n")
    validate_city(search_criteria, "destination_airport", "Please enter a destination city name. Example: London\n")

    departure_date = datetime_input(search_criteria, "departure_date", "Please enter a departure date\n")
    arrival_date = datetime_input(search_criteria, "arrival_date", "Please enter an arrival date\n")

    first_name, last_name = "", ""

    while first_name == "":
        first_name = input("First name:\n")
        if not first_name.isalpha():
            print("Please enter only letters")
            first_name = ""
    search_criteria["first_name"] = first_name.capitalize()

    while last_name == "":
        last_name = input("Last name:\n")
        if not last_name.isalpha():
            print("Please enter only letters")
    search_criteria["last_name"] = last_name.capitalize()

    # for user in users: #TODO: this crap still isn't working properly
    #     if user.first_name.lower() == first_name.lower() and user.last_name.lower() == last_name.lower():
    #         search_criteria["email"] = user.email
    #         break

    results = ticket_search(tickets, search_criteria)
    results = [ticket for ticket in results if ticket.for_deletion == "No"]
    if len(results) > 0:
        print_ticket(results, "Multi")
    else:
        print("No matching results")


def edit_ticket(ticket_id):
    departure_candidates = []
    ticket_is_valid = False
    for ticket in tickets:
        if ticket_id.upper() == ticket.id and ticket.for_deletion == "No":
            ticket_is_valid = True
            current_ticket = ticket  # save the current ticket for use
            break
    if ticket_is_valid is False:
        print("Invalid ticket ID")
        return

    while True:
        print("You are now editing ticket:")
        print_ticket(current_ticket, "Single")
        print("|0| Return to previous menu")
        print("|1| Change flight")
        print("|2| Change departure date")
        print("|3| Change seat")
        choice = input()

        if choice == "0":
            return

        if choice in ["1", "2"]:
            if choice == "1":
                departure_candidates = []
                candidates = departure_search_menu("Return", "Multi")  # returns the resulsts, does not print them

                for departure in candidates:
                    departure_datetime_obj = departure_datetime(departure.departure_date,
                                                                departure.flight.departure_time)
                    departure_date_obj = departure_datetime_obj.date()
                    current_datetime_obj = datetime.now()
                    # filter the candidates
                    # if a departure hasnt taken off yet and its id is different from the current departure then we add it into candidates
                    if departure_datetime_obj > current_datetime_obj and current_ticket.departure.flight_number != departure.flight_number:
                        departure_candidates.append(departure)

            elif choice == "2":
                departure_candidates = []
                for departure in departures:
                    if departure.flight_number == current_ticket.departure.flight_number:
                        departure_datetime_obj = departure_datetime(departure.departure_date,
                                                                    departure.flight.departure_time)
                        departure_date_obj = departure_datetime_obj.date()
                        current_datetime_obj = datetime.now()

                        # if a departure hasnt taken off yet and its id is different from the current departure then we add it into candidates
                        if departure_datetime_obj > current_datetime_obj and current_ticket.departure.id != departure.id:
                            departure_candidates.append(departure)

            print("Available departures")
            print_departure_search_table(departure_candidates)

            departure = validate_departure_id(departure_candidates)

            if departure is not False:
                current_ticket.seat = ""
                current_ticket.departure.seats_taken -= 1
                save_tickets_to_file()
                save_departures_to_file()
                current_ticket.departure = departure  # we swap the departure reference of the ticket object with a reference to a new departure
                current_ticket.departure.seats_taken += 1
                save_tickets_to_file()
                save_departures_to_file()

                if choice == "1":
                    print("Flight change successful.")
                else:
                    print("Date change successful.")


        elif choice == "3":
            if current_ticket.seat == "":
                print("You can only change seats if a ticket has been checked in for")
                continue

            current_ticket.seat = ""
            ticket.departure.seats_taken -= 1
            save_tickets_to_file()  # we have modified the ticket so we must save it in order for chose_seat to account for the freed seat
            save_departures_to_file()
            choose_seat(current_ticket)
            # delete the seat from the ticket and check in the user again, dont allow passenger and connected check ins
        else:
            print("Invalid command")
    # let, datum polaska,  sediste


# TODO: Print on ticket if customer has checked in or not
def edit_ticket_menu():
    while True:
        print("|0| Return to previous menu")
        print("|1| Edit a ticket by entering its ID")
        print("|2| Search for sold tickets")
        command = input()
        if command == "0":
            return
        elif command == "1":
            while True:
                ticket_id = input(
                    "Please enter a ticket ID. Enter 0 to return to previous menu\n")  # TODO: Validate the ticket id, only allow this if the ticket is checked in
                if ticket_id == "0":
                    break
                edit_ticket(ticket_id)
        elif command == "2":
            ticket_search_menu()
        else:
            print("Invalid command")


def delete_ticket(ticket_id):
    # validate ticket id
    for ticket in tickets:
        if ticket_id.upper() == ticket.id:
            print_ticket(ticket)
            print("Confirm the deletion of this ticket?")
            print("|1| Yes")
            print("|2| No")
            command = input()
            if command == "1":
                print("Ticket succesfully deleted")
                ticket.for_deletion = "Yes"  # change the ticket atribute marked for deletion from no to yes
                ticket.seat = ""  # check the passenger out
                ticket.departure.seats_taken -= 1  # empty a place on the departure
                save_tickets_to_file()  # after that save all the tickets into our file
                save_departures_to_file()  # because we changed seats taken we also have to save all the deparures
                return
            elif command == "2":
                return
            else:
                print("Invalid command")

    # if we don't find a valid ticket id
    print("Invalid ticket ID")
    return


def delete_ticket_menu():
    while True:
        print("|0| Return to previous menu")
        print("|1| Delete a ticket by entering its ID")
        print("|2| Search for sold tickets")
        command = input()
        if command == "0":
            return
        elif command == "1":
            print("Please enter a ticket ID")
            ticket_id = input()
            delete_ticket(ticket_id)
        elif command == "2":
            ticket_search_menu()
        else:
            print("Invalid command")
