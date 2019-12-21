from data_loader import load_current_ticket_id, load_current_flight_id, load_departures, load_users,\
     load_airports,load_airplanes, load_flights, load_departures, load_tickets

print("Loading data", end = "")
def init():
     global current_user
     current_user = None
users = load_users()
airports = load_airports()
airplanes = load_airplanes()
print(".", end = "")
flights = load_flights(airports, airplanes)
print(".", end = "")
departures = load_departures(flights, airplanes)
print(".")
tickets = load_tickets(departures)



current_ticket_id = load_current_ticket_id()
current_flight_id = load_current_flight_id()