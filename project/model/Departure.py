class Departure():
    def __init__(self, id, flight_number, departure_date, arrival_date, flight, capacity, seats_taken):
        self.id = id
        self.flight_number = flight_number
        self.departure_date = departure_date
        self.arrival_date = arrival_date
        self.flight = flight
        self.capacity = capacity
        self.seats_taken = seats_taken

    def serialize(self):
        return self.id + "|" + self.flight_number + "|" + self.departure_date + "|" + self.arrival_date + "|" + str(self.capacity) + "|" + str(self.seats_taken)