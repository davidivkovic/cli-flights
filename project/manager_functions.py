import seller_functions
from model.Seller import Seller
from model.Flight import Flight
from model.Enums import Role
from utility import *
from globals import current_flight_id
import string


def save_seller_to_file(seller):
    with open("data/sellers", "a") as f:
        f.write("\n" + str(seller.serialize()))


def save_flight_to_file(flight):
    with open("data/flights", "a") as f:
        f.write("\n" + str(flight.serialize()))

    with open("data/current_flight_id", "w") as f:
        f.write(str(current_flight_id))


def save_flights_to_file():
    from main import flights
    with open("data/flights", "w") as f:
        for flight in flights:
            f.write(flight.serialize() + "\n")


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
    users.append(seller)
    save_seller_to_file(seller)
    print("Seller", seller.first_name, seller.last_name, "successfully registered")


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
                return airport
        print("City not found.")

# TODO: check if inputs are empty
def create_new_flight():
    from main import airplanes, validate_datetime, flights, print_flight_search_table
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

    departure_time_obj = datetime.strptime(departure_time, "%H:%M")
    arrival_time_obj = datetime.strptime(arrival_time, "%H:%M")
    if arrival_time_ < departure_time_:
        flight.overnight = "Yes"
    else:
        flight.overnight = "No"


    while True:
        print("Please enter an airline name")
        airline = input()
        if "|" not in airline:
            break
        else:
            print("Airline names cannot contain the character \"|\"")

    days = ""
    while True:
        print("Enter days on which the flight departs separated by spaces. Example 1 2 3")
        print("First day of the week is Monday")
        choices = input()
        elements = choices.split(" ")
        for element in elements:
            if element not in ['1', '2', '3', '4', '5', '6', '7']:
                print("Invalid command")
                break
        if "1" in elements:
            days += "mon "
        if "2" in elements:
            days += "tue "
        if "3" in elements:
            days += "wed "
        if "4" in elements:
            days += "thu "
        if "5" in elements:
            days += "fri "
        if "6" in elements:
            days += "sat "
        if "7" in elements:
            days += "sun "
        break

    current_airplane = None
    while True:
        if current_airplane is not None:
            break
        print("|1| Enter an airplane model")
        print("|2| Show all available airplane models")
        choice = input()

        if choice == "1":
            print("Airplane model:")
            valid = False
            while True:
                current_airplane = input().upper()
                for airplane in airplanes:
                    if current_airplane == airplane.code:
                        current_airplane = airplane
                        valid = True
                        break
                else:
                    current_airplane = None
                    print("Model does not exist")
                    break
                if valid is True:
                    break

        elif choice == "2":
            print("{:30}{:6}".format("Airplane name", "Model"))
            for airplane in airplanes:
                print("{:30}{:6}".format(airplane.name, airplane.code))

        else:
            print("Invalid command")

    while True:
        print("Enter a price in €")
        price = input()
        if price.isnumeric():
            break
        else:
            print("Price can only contain digits")
    global current_flight_id
    alphabet = string.ascii_uppercase
    current_flight_id += 1
    flight_id = f"{current_flight_id:04d}"  # format the string with two leading zeroes, those will be mapped as
    # alphabet[number]
    letter1 = int(flight_id[0])  # contains a number which will be mapped to a letter
    letter2 = int(flight_id[1])  # we will only have 9999 id's
    numbers = flight_id[2:]
    new_flight_id = alphabet[letter1] + alphabet[letter2] + numbers

    flight = Flight(new_flight_id, departure_airport, destination_airport, departure_time, arrival_time, overnight,
                    airline, days, current_airplane, price)
    flights.append(flight)
    save_flight_to_file(flight)
    print("Flight created successfully")
    print_flight_search_table(flight, "Single")


def edit_flight(flight):
    from main import print_flight_search_table, validate_datetime, airplanes, save_departures_to_file, flights, print_departure_search_table
    from data_loader import load_departures
    while True:
        print("You are now editing flight")
        print_flight_search_table(flight, "Single")
        print("|0| Return to previous menu")
        print("|1| Change departure airport")
        print("|2| Change destination airport")
        print("|3| Change departure time")
        print("|4| Change arrival time")
        print("|5| Change whether the flight is an overnight one")
        print("|6| Change airline")
        print("|7| Change departure days")
        print("|8| Change airplane model")
        print("|9| Change Price")

        choice = input()
        if choice == "0":
            return
        elif choice == "1":
            while True:
                departure_airport = validate_city("Enter departure city. Example: Belgrade")
                if flight.destination_airport != departure_airport:
                    flight.departure_airport = departure_airport
                    save_flights_to_file()
                    print("Edit successful")
                    break
                else:
                    print("Departure and destination arports cannot be the same")

        elif choice == "2":
            while True:
                destination_airport = validate_city("Enter destination city. Example: London")
                if flight.departure_airport != destination_airport:
                    flight.destination_airport = destination_airport
                    save_flights_to_file()
                    print("Edit successful")
                    break
                else:
                    print("Departure and destination arports cannot be the same")

        elif choice == "3":
            while True:
                print("Enter a departure time in the format of H:M")
                time = input()
                if validate_datetime(time, "Time") is True:
                    flight.departure_time = time
                    save_flights_to_file()
                    print("Edit successful")
                    break

        elif choice == "4":
            while True:
                print("Enter an arrival time in the format of H:M")
                time = input()
                if validate_datetime(time, "Time") is True:
                    flight.arrival_time = time
                    save_flights_to_file()
                    print("Edit successful")
                    break

        elif choice == "5":
            while True:
                print("Is this an overnight flight?")
                print("|1| Yes")
                print("|2| No")
                choice = input()
                if choice == "1":
                    flight.overnight = "Yes"
                    save_flights_to_file()
                    print("Edit successful")
                    break
                elif choice == "2":
                    flight.overnight = "No"
                    save_flights_to_file()
                    print("Edit successful")
                    break
                else:
                    print("Invalid command")

        elif choice == "6":
            while True:
                print("Please enter an airline name")
                airline = input()
                if "|" not in airline:
                    flight.airline = airline
                    save_flights_to_file()
                    print("Edit successful")
                    break
                else:
                    print("Airline names cannot contain the character \"|\"")

        elif choice == "7":
            days = ""
            valid = True
            while True:
                print("Enter days on which the flight departs separated by spaces. Example 1 2 3")
                print("First day of the week is Monday")
                choices = input()
                elements = choices.split(" ")
                for element in elements:
                    if element not in ['1', '2', '3', '4', '5', '6', '7']:
                        valid = False
                        print("Invalid command")
                        break
                if valid is False:
                    continue
                if "1" in elements:
                    days += "mon "
                if "2" in elements:
                    days += "tue "
                if "3" in elements:
                    days += "wed "
                if "4" in elements:
                    days += "thu "
                if "5" in elements:
                    days += "fri "
                if "6" in elements:
                    days += "sat "
                if "7" in elements:
                    days += "sun "
                flight.days = days
                save_flights_to_file()
                print("Edit successful")
                break

        elif choice == "8":
            current_airplane = None
            while True:
                if current_airplane is not None:
                    break
                print("|1| Enter an airplane model")
                print("|2| Show all available airplane models")
                choice = input()

                if choice == "1":
                    print("Airplane model:")
                    valid = False
                    while True:
                        current_airplane = input().upper()
                        for airplane in airplanes:
                            if current_airplane == airplane.code:
                                flight.airplane = airplane
                                save_flights_to_file()
                                # global departures
                                departures = load_departures(flights, airplanes)
                                #save_departures_to_file()
                                # for departure in departures:
                                #     print(departure.id, departure.flight_number, departure.capacity)
                                print("Edit successful")
                                valid = True
                                break
                        else:
                            current_airplane = None
                            print("Model does not exist")
                            break
                        if valid is True:
                            break

                elif choice == "2":
                    print("{:30}{:6}".format("Airplane name", "Model"))
                    for airplane in airplanes:
                        print("{:30}{:6}".format(airplane.name, airplane.code))

                else:
                    print("Invalid command")

        elif choice == "9":
            print("Enter a price in €")
            price = input()
            if price.isnumeric():
                flight.price = price
                save_flights_to_file()
                print("Edit successful")
            else:
                print("Price can only contain digits")
        else:
            print("Invalid command")


def edit_flights_menu():
    from main import flights, print_flight_search_table
    search_criteria = create_search_dict()
    valid_results = None

    while True:
        print("|0| Return to previous menu")
        print("|1| Edit a flight by entering its number")
        print("|2| Search for flights")
        choice = input()

        if choice == "0":
            return

        elif choice == "1":
            end = False
            while True:
                print("Please enter a flight number")
                flight_input = input()
                for flight in flights:
                    if flight_input.lower() == flight.flight_number.lower():
                        edit_flight(flight)
                        end = True
                if end is True:
                    break
                print("Invalid flight number")

        elif choice == "2":
            departure_airport = validate_city("Enter departure city. Example: Belgrade")
            destination_airport = validate_city("Enter destination city. Example: London")
            search_criteria["departure_airport"] = departure_airport.city
            search_criteria["destination_airport"] = destination_airport.city
            results = flight_search(flights, search_criteria)
            print_flight_search_table(results)
        else:
            print("Invalid command")


def delete_tickets_menu():
    from main import tickets, print_ticket, save_tickets_to_file

    while True:
        candidates = []
        for ticket in tickets:
            if ticket.for_deletion == "Yes":
                candidates.append(ticket)

        if len(candidates) > 0:
            print("Tickets marked for deletion:")
            print_ticket(candidates, "Multi")
        else:
            print("No tickets marked for deletion")

        print("|0| Return to previous menu")
        print("|1| Permanently delete all of the tickets marked for deletion")
        print("|2| Permanently delete one or more selected tickets")
        print("|3| Unmark one or more tickets that have been marked for deletion")
        choice = input()

        if choice == "0":
            return

        elif choice == "1":
            for ticket in reversed(tickets):
                if ticket.for_deletion == "Yes":
                    tickets.remove(ticket)
                    candidates.clear()
            save_tickets_to_file()
            print("Succesfully deleted tickets\n")

        elif choice in ["2", "3"]:
            while True:
                valid = True
                print("Please enter one or more ticket IDs separated by spaces. Example AA0000 AA0001")
                entry = input()
                for_deletion = entry.split(" ")
                for_deletion[:] = [ticket_id.upper() for ticket_id in for_deletion]
                for ticket_id in for_deletion:
                    if ticket_id not in [ticket.id for ticket in candidates]:
                        print("Please enter only tickets shown in the table above")
                        valid = False
                        break

                if choice == "2":
                    if valid is True:
                        for ticket in reversed(tickets):
                            if ticket.id in for_deletion:
                                tickets.remove(ticket)
                        save_tickets_to_file()
                        print("Succesfully deleted tickets\n")
                        break

                elif choice == "3":
                    if valid is True:
                        for ticket in reversed(tickets):
                            if ticket.id in for_deletion:
                                ticket.for_deletion = "No"
                        save_tickets_to_file()
                        print("Succesfully unmarked tickets\n")
                        break

            else:
                print("Invalid command")


def generate_reports():
    from main import datetime_input, tickets, print_ticket, users
    while True:
        print("|0| Return to previous menu")
        print("|1| List of sold tickets by date od sale")
        print("|2| List of sold tickets by departure date")
        print("|3| List of sold tickets by date of sale for a given seller")
        print("|4| Total number and price of tickets sold on a given date")
        print("|5| Total number and price of tickets sold for a given departure date")
        print("|6| Total number and price of tickets sold on a given date for a chosen seller")
        print("|7| Total number and price of tickets sold in the last 30 days for each seller")
        choice = input()

        if choice == "0":
            return
        elif choice == "1":
            search_criteria = create_search_dict_ticket()
            datetime_input(search_criteria, "purchase_date", "Please enter a date of sale in the format of m-d-yyyy\n")
            results = ticket_search(tickets, search_criteria)
            print_ticket(results, "Multi")

        elif choice == "2":
            search_criteria = create_search_dict_ticket()
            datetime_input(search_criteria, "departure_date",
                           "Please enter a departure date in the format of m-d-yyyy\n")
            results = ticket_search(tickets, search_criteria)
            print_ticket(results, "Multi")

        elif choice == "3":
            search_criteria = create_search_dict_ticket()
            datetime_input(search_criteria, "purchase_date", "Please enter a date of sale in the format of m-d-yyyy\n")

            first_name, last_name = "", ""

            while True:
                print("Please enter the seller's first name")
                first_name = input()
                if first_name.isalpha() is True:
                    break
                else:
                    print("Please enter only letters")

            while True:
                print("Please enter the seller's last name")
                last_name = input()
                if last_name.isalpha() is True:
                    break
                else:
                    print("Please enter only letters")

            search_criteria["sold_by"] = first_name.capitalize() + " " + last_name.capitalize()

            results = ticket_search(tickets, search_criteria)
            print_ticket(results, "Multi")

        elif choice == "4":
            total_price = 0
            search_criteria = create_search_dict_ticket()
            datetime_input(search_criteria, "purchase_date", "Please enter a date of sale in the format of m-d-yyyy\n")
            results = ticket_search(tickets, search_criteria)

            for ticket in results:
                total_price += int(ticket.departure.flight.price)
            number_of_tickets = len(results)

            print("\nNumber of tickets sold on", search_criteria["purchase_date"], "is", number_of_tickets)
            print("Total price of tickets sold on", search_criteria["purchase_date"], "is", str(total_price) + "€\n")

        elif choice == "5":
            total_price = 0
            search_criteria = create_search_dict_ticket()
            datetime_input(search_criteria, "departure_date",
                           "Please enter a departure date in the format of m-d-yyyy\n")
            results = ticket_search(tickets, search_criteria)

            for ticket in results:
                total_price += int(ticket.departure.flight.price)
            number_of_tickets = len(results)

            print("\nNumber of tickets sold for flights that depart on", search_criteria["departure_date"], "is",
                  number_of_tickets)
            print("Total price of tickets sold for flights that depart on", search_criteria["departure_date"], "is",
                  str(total_price) + "€\n")

        elif choice == "6":
            total_price = 0
            search_criteria = create_search_dict_ticket()
            datetime_input(search_criteria, "purchase_date", "Please enter a date of sale in the format of m-d-yyyy\n")

            first_name, last_name = "", ""
            while True:
                print("Please enter the seller's first name")
                first_name = input()
                if first_name.isalpha() is True:
                    break
                else:
                    print("Please enter only letters")

            while True:
                print("Please enter the seller's last name")
                last_name = input()
                if last_name.isalpha() is True:
                    break
                else:
                    print("Please enter only letters")

            search_criteria["sold_by"] = first_name.capitalize() + " " + last_name.capitalize()

            results = ticket_search(tickets, search_criteria)

            for ticket in results:
                total_price += int(ticket.departure.flight.price)
            number_of_tickets = len(results)

            print("\nNumber of tickets sold by", search_criteria["sold_by"], "on", search_criteria["purchase_date"],
                  "is", number_of_tickets)
            print("Total price of tickets sold by", search_criteria["sold_by"], "on", search_criteria["purchase_date"],
                  "is", str(total_price) + "€\n")

        elif choice == "7":

            candidates = []
            one_month_back_obj = datetime.now() - timedelta(days=30)
            for ticket in tickets:
                ticket_date_obj = datetime.strptime(ticket.purchase_date, "%d-%m-%Y")
                if ticket_date_obj >= one_month_back_obj:  # find only the tickets that have been sold in the last 30 days
                    candidates.append(ticket)

            sellers = []
            for user in users:
                if user.role == Role.Seller:  # extract all sellers from users so we can use their names as keys for a dict
                    sellers.append(user)

            report = dict()
            for seller in sellers:  # for every seller create a dict value of [0,0] with the key being his name
                report[seller.first_name + " " + seller.last_name] = [0,
                                                                      0]  # first element is number of tickets sold, second is price

            for ticket in candidates:
                if ticket.sold_by != "":  # go through all the candidates and take the ones that have been sold by a seller
                    report[ticket.sold_by][0] += 1  # increment the sellers ticket sell count
                    report[ticket.sold_by][1] += int(
                        ticket.departure.flight.price)  # add the sold ticket price to his price tally

            print("\n{:22}{:25}{:}".format("Seller", "Number of tickets sold", "Total price of tickets sold"))
            for key in list(report.keys()):
                print("{:22}{:<25}{:}".format(key, report[key][0], str(report[key][1]) + "€"))
            print()
