from model.Customer import Customer
from model.Seller import Seller
from model.Manager import Manager
from model.Flight import Flight
from model.Airport import Airport
from model.Departure import Departure
from model.Airplane import Airplane
from model.Ticket import Ticket

def load_customers():
    with open("data/customers") as f:
        content = f.readlines()

    customers = []
    for line in content:
        customer_data = line.strip().split('|')
        customer = Customer(customer_data[0],  # username
                            customer_data[1],  # password
                            customer_data[2],  # first name
                            customer_data[3],  # last name
                            customer_data[4],  # phone
                            customer_data[5],  # email
                            customer_data[6],  # passport number
                            customer_data[7],  # citizenship
                            customer_data[8])  # gender
        customers.append(customer)
    return customers


def load_sellers():
    with open("data/sellers") as f:
        content = f.readlines()

    sellers = []
    for line in content:
        seller_data = line.strip().split('|')
        seller = Seller(seller_data[0],  # username
                        seller_data[1],  # password
                        seller_data[2],  # first name
                        seller_data[3])  # last name

        sellers.append(seller)
    return sellers


def load_managers():
    with open("data/managers") as f:
        content = f.readlines()

    managers = []
    for line in content:
        manager_data = line.strip().split('|')
        seller = Manager(manager_data[0],  # username
                         manager_data[1],  # password
                         manager_data[2],  # first name
                         manager_data[3])  # last name

        managers.append(seller)
    return managers


def load_users():
    users = []
    users.extend(load_customers())
    users.extend(load_sellers())
    users.extend(load_managers())

    return users


def load_airplanes():
    with open("data/airplanes") as f:
        content = f.readlines()

    airplanes = []
    for line in content:
        airplane_data = line.strip().split('|')
        airplane = Airplane(airplane_data[0],  # code
                            airplane_data[1],  # name
                            airplane_data[2])  # rows_cols
        airplanes.append(airplane)
    return airplanes


def load_flights(airports, airplanes):
    with open("data/flights") as f:
        content = f.readlines()

    flights = []
    for line in content:
        flight_data = line.strip().split('|')

        departure_airport_pointer = [airport for airport in airports if airport.code == flight_data[1]][0]
        destination_airport_pointer = [airport for airport in airports if airport.code == flight_data[2]][0]
        airplane_pointer = [airplane for airplane in airplanes if airplane.code == flight_data[8]][0]

        flight = Flight(flight_data[0],  # flight_number
                        departure_airport_pointer,  # departure airport
                        destination_airport_pointer,  # destination airport
                        flight_data[3],  # departure_time
                        flight_data[4],  # arrival time
                        flight_data[5],  # overnight
                        flight_data[6],  # airline
                        flight_data[7],  # days
                        airplane_pointer,  # airplane
                        flight_data[9])  # price

        flights.append(flight)
    return flights


def load_departures(flights, airplanes):
    with open("data/departures") as f:
        content = f.readlines()

    departures = []
    for line in content:
        departure_data = line.strip().split('|')

        flight_pointer = [flight for flight in flights if flight.flight_number == departure_data[1]][0]
        flight_rows_cols = [airplane.rows_cols for airplane in airplanes if airplane.code == flight_pointer.airplane.code][0]
        flight_capacity = [airplane.capacity for airplane in airplanes if airplane.code == flight_pointer.airplane.code][0]

        #flight_capacity = int(flight_rows_cols.strip().split('/')[0]) * int(flight_rows_cols.strip().split('/')[1])

        departure = Departure(departure_data[0],  # id
                              departure_data[1],  # flight_number
                              departure_data[2],  # departure_date
                              departure_data[3],  # arrival_date
                              flight_pointer,  # flight_object_pointer
                              int(departure_data[4]))  # seats_taken

        departures.append(departure)
    return departures


def load_airports():
    with open("data/airports", encoding="utf8") as f:
        content = f.readlines()

    airports = []
    for line in content:
        airport_data = line.strip().split('|')
        airport = Airport(airport_data[0],  # code
                          airport_data[1],  # name
                          airport_data[2],  # city
                          airport_data[3], )  # country
        airports.append(airport)
    return airports


def load_tickets(departures):
    with open("data/tickets") as f:
        content = f.readlines()

    tickets = []
    for line in content:
        ticket_data = line.strip().split('|')



        departure_pointer = [departure for departure in departures if departure.id == ticket_data[1]][0]

        ticket = Ticket(ticket_data[0],  # ticket_id
                        departure_pointer,  # departure_id
                        ticket_data[2],  # first_name
                        ticket_data[3],  # last_name
                        ticket_data[4],  # contact_phone
                        ticket_data[5],  # contact_email
                        ticket_data[6],  # passport number
                        ticket_data[7],  # nationality
                        ticket_data[8],  # gender
                        ticket_data[9],  # purchase_date
                        ticket_data[10],  # seat
                        ticket_data[11],  # delete
                        ticket_data[12])  # sold_by
        tickets.append(ticket)
    return tickets


def load_current_ticket_id():
    with open("data/current_ticket_id") as f:
        content = f.readlines()
    return int(content[0])

def load_current_flight_id():
    with open("data/current_flight_id") as f:
        content = f.readlines()
    return int(content[0])
