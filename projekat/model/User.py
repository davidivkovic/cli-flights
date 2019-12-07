from enum import Enum

class Role(Enum):
    Customer = 1
    Seller = 2
    Manager = 3

class Gender(Enum):
    Male = 1
    Female = 2

class Days(Enum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7

class User:
    def __init__(self, username, password, first_name, last_name, role):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
    def __str__(self):
        return self.first_name + " " + self.last_name + " " + str(self.role.name)

class Customer(User):
    def __init__(self, username, password, first_name, last_name, phone, email, passport_number = "", citizenship = "", gender = None):
        #if gender != None and not isinstance(gender, Gender):
            #raise ValueError("Unesi dobar pol")

        super().__init__(username, password, first_name, last_name, Role.Customer)
        self.phone = phone
        self.email = email
        self.passport_number = passport_number
        self.citizenship = citizenship
        self.gender = gender
    def __str__(self):

        return super().__str__() + " " + str(self.passport_number)

    def serialize(self):
        return (self.username + "|" + self.password +  "|" + self.first_name +  "|" + self.last_name +  "|" + self.phone
        +  "|" + self.email +  "|" + self.passport_number +  "|" + self.citizenship + "|" + str(self.gender))

class Seller(User):
    def __init__(self, username, password, first_name, last_name):
        super().__init__(username, password, first_name, last_name, Role.Seller)

class Manager(User):
    def __init__(self, username, password, first_name, last_name):
        super().__init__(username, password, first_name, last_name, Role.Manager)

class Airport:
    def __init__(self, code, name, city, country):
        self.code = code
        self.name = name
        self.city = city
        self.country = country

class Airplane:
    def __init__(self, name, rows, columns):
        self.name = name
        self.rows = rows
        self.columns = columns

class Flight:
    def __init__(self, flight_number, departure_airport, destination_airport, departure_time, arrival_time, overnight,
                 airline, days, airplane_model, price):
        self.flight_number = flight_number
        self.departure_airport = departure_airport
        self.destination_airport = destination_airport
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.overnight = overnight
        self.airline = airline
        self.days = days
        self.airplane_model = airplane_model
        self.price = price
    #def print_basic_data:

class Departure:
    def __init__(self, id, flight_number, departure_date, arrival_date):
        self.id = id
        self.flight_number = flight_number
        self.departure_date = departure_date
        self.arrival_date = arrival_date

