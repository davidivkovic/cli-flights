class Flight:
    def __init__(self, flight_number, departure_airport, destination_airport, departure_time, arrival_time, overnight,
                 airline, days, airplane, price):
        self.flight_number = flight_number
        self.departure_airport = departure_airport
        self.destination_airport = destination_airport
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.overnight = overnight
        self.airline = airline
        self.days = days
        self.airplane = airplane
        self.price = price
