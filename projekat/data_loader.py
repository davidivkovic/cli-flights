from model.Customer import Customer
from model.Seller import Seller
from model.Manager import Manager
from model.Flight import Flight
from model.Departure import Departure

def load_customers():
    with open("data/customers") as f:
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
    with open("data/sellers") as f:
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
    with open("data/managers") as f:
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
    with open("data/flights") as f:
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
    with open("data/departures") as f:
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
