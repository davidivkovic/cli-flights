from model.User import *

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

def load_departures():
    with open("departures") as f:
        content = f.readlines()

    departures = []
    for line in content:
        departure_data = line.split('|')
        departure = Departure(departure_data[0],
                              departure_data[1],
                              departure_data[2],
                              departure_data[3])

        departures.append(departure)
    return departures
'''
def load_flights:
    with open("flights") as f:
        content = f.readlines()

    flights = []
    for line in content:
        flight_data = line.split('|')
        flight = Flight(flight_data[0],
                        flight_data[1],
                        flight_data[2],
                        flight_data[3],
                        flight_data[4],
                        flight_data[4],
                        flight_data[4],
                        flight_data[4],
                        flight_data[4],)

        departures.append(departure)
    return departures'''