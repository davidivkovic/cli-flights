from model.User import *
from datetime import *

def load_customers():
    with open("customers") as f:
        content = f.readlines()

    customers = []
    for line in content:
        customer_data = line.split('|')
        customer = Customer(customer_data[0],   #username
                            customer_data[1],   #password
                            customer_data[2],   #first name
                            customer_data[3],   #last name
                            customer_data[4],   #phone
                            customer_data[5],   #email
                            customer_data[6],   #passport number
                            customer_data[7],   #citizenship
                            customer_data[8])   #gender
        customers.append(customer)
    return customers


def load_sellers():
    with open("sellers") as f:
        content = f.readlines()

    sellers = []
    for line in content:
        seller_data = line.split('|')
        seller = Seller(seller_data[0],    #username
                        seller_data[1],    #password
                        seller_data[2],    #first name
                        seller_data[3])    #last name

        sellers.append(seller)
    return sellers


def load_managers():
    with open("managers") as f:
        content = f.readlines()

    managers = []
    for line in content:
        manager_data = line.split('|')
        seller = Manager(manager_data[0],    #username
                         manager_data[1],    #password
                         manager_data[2],    #first name
                         manager_data[3])    #last name

        managers.append(seller)
    return managers

def load_users():
    users = []
    users.extend(load_customers())
    users.extend(load_sellers())
    users.extend(load_managers())

    return users

def load_flights():
    with open("flights") as f:
        content = f.readlines()

    flights = []
    for line in content:
        flight_data = line.strip().split('|')
        flight = Flight(flight_data[0],
                        flight_data[1],
                        flight_data[2],
                        flight_data[3],
                        flight_data[4],
                        flight_data[5],
                        flight_data[6],
                        flight_data[7],
                        flight_data[8],
                        flight_data[9])

        flights.append(flight)
    return flights

def load_departures(flights):
    with open("departures") as f:
        content = f.readlines()

    departures = []
    for line in content:
        departure_data = line.strip().split('|')
        f = [flight for flight in flights if flight.flight_number == departure_data[1]][0]
        departure = Departure(departure_data[0],
                              departure_data[1],
                              departure_data[2],
                              departure_data[3],
                              f)

        departures.append(departure)
    return departures

def create_search_dict():
    search_criteria = dict()
    search_criteria["departure_airport"] = ""
    search_criteria["destination_airport"] = ""
    search_criteria["departure_date"] = ""
    search_criteria["arrival_date"] = ""
    search_criteria["departure_time"] = ""
    search_criteria["arrival_time"] = ""
    search_criteria["airline"] = ""
    return search_criteria

def flight_search(departures, search_criteria):

    candidates = departures[:]
    for departure in candidates:
        if search_criteria["departure_airport"] != "":
            candidates[:] = [departure for departure in candidates if search_criteria["departure_airport"] == departure.flight.departure_airport]
        if search_criteria["destination_airport"] !="":
            candidates[:] = [departure for departure in candidates if search_criteria["destination_airport"] == departure.flight.destination_airport]
        if search_criteria["departure_date"] != "":
            candidates[:] = [departure for departure in candidates if search_criteria["departure_date"] == departure.departure_date]
        if search_criteria["arrival_date"] != "":
            candidates[:] = [departure for departure in candidates if search_criteria['arrival_date'] == departure.arrival_date]
        if search_criteria["departure_time"] != "":
            candidates[:] = [departure for departure in candidates if search_criteria['departure_time'] == departure.flight.departure_time]
        if search_criteria["arrival_time"] != "":
            candidates[:] = [departure for departure in candidates if search_criteria['arrival_time'] == departure.flight.arrival_time]
        if search_criteria["airline"] != "":
            candidates[:] = [departure for departure in candidates if search_criteria['airline'] == departure.flight.airline]
    return candidates