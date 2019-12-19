from datetime import *

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

def create_search_dict_ticket():
    search_criteria = dict()
    search_criteria["departure_airport"] = ""
    search_criteria["destination_airport"] = ""
    search_criteria["departure_date"] = ""
    search_criteria["arrival_date"] = ""
    search_criteria["first_name"] = ""
    search_criteria["last_name"] = ""
    search_criteria["email"] = ""
    return search_criteria

def ticket_search(tickets, search_criteria):
    candidates = tickets[:]
    for ticket in candidates:
        if search_criteria["departure_airport"] != "":
            candidates[:] = [ticket for ticket in candidates if search_criteria["departure_airport"].lower() == ticket.departure.flight.departure_airport.city.lower()]
        if search_criteria["destination_airport"] != "":
            candidates[:] = [ticket for ticket in candidates if search_criteria["destination_airport"].lower() == ticket.departure.flight.destination_airport.city.lower()]
        if search_criteria["departure_date"] != "":
            candidates[:] = [ticket for ticket in candidates if search_criteria["departure_date"] == ticket.departure.departure_date]
        if search_criteria["arrival_date"] != "":
            candidates[:] = [ticket for ticket in candidates if search_criteria['arrival_date'] == ticket.departure.arrival_date]
        if search_criteria["first_name"] != "":
             candidates[:] = [ticket for ticket in candidates if search_criteria['first_name'] == ticket.first_name]
        if search_criteria["last_name"] != "":
             candidates[:] = [ticket for ticket in candidates if search_criteria['last_name'] == ticket.last_name]
        if search_criteria["email"] != "":
            candidates[:] = [ticket for ticket in candidates if search_criteria["email"] == ticket.contact_email]
    return candidates


def flight_search(flights, search_criteria):
    candidates = flights[:]
    for flight in candidates:
        if search_criteria["departure_airport"] != "":
            candidates[:] = [flight for flight in candidates if search_criteria["departure_airport"].lower() == flight.departure_airport.city.lower()]
        if search_criteria["destination_airport"] !="":
            candidates[:] = [flight for flight in candidates if search_criteria["destination_airport"].lower() == flight.destination_airport.city.lower()]
    return candidates

def departure_search(departures, search_criteria):

    candidates = departures[:]
    for departure in candidates:
        if search_criteria["departure_airport"] != "":
            candidates[:] = [departure for departure in candidates if search_criteria["departure_airport"].lower() == departure.flight.departure_airport.city.lower()]
        if search_criteria["destination_airport"] !="":
            candidates[:] = [departure for departure in candidates if search_criteria["destination_airport"].lower() == departure.flight.destination_airport.city.lower()]
        if search_criteria["departure_date"] != "":
            candidates[:] = [departure for departure in candidates if search_criteria["departure_date"] == departure.departure_date]
        if search_criteria["arrival_date"] != "":
            candidates[:] = [departure for departure in candidates if search_criteria['arrival_date'] == departure.arrival_date]
        if search_criteria["departure_time"] != "":
            candidates[:] = [departure for departure in candidates if search_criteria['departure_time'] == departure.flight.departure_time]
        if search_criteria["arrival_time"] != "":
            candidates[:] = [departure for departure in candidates if search_criteria['arrival_time'] == departure.flight.arrival_time]
        if search_criteria["airline"] != "":
            candidates[:] = [departure for departure in candidates if search_criteria['airline'].lower() == departure.flight.airline.lower()]

    results = []

    current_date_obj = datetime.today().date()
    current_time_obj = datetime.now().time()

    for departure in candidates:
        departure_date = datetime.strptime(departure.departure_date, "%d-%m-%Y").date()
        departure_time = datetime.strptime(departure.flight.departure_time, "%H:%M").time()

        if departure_date > current_date_obj:
            results.append(departure)
        if departure_date == current_date_obj and departure_time >= current_time_obj:
            results.append(departure)

    return results

def flight_search_flexible(departures, search_criteria):
    candidates = departures[:]
    for departure in candidates:
        if search_criteria["departure_airport"] != "":
            candidates[:] = [departure for departure in candidates if search_criteria["departure_airport"] == departure.flight.departure_airport]
        if search_criteria["destination_airport"] != "":
            candidates[:] = [departure for departure in candidates if search_criteria["destination_airport"] == departure.flight.destination_airport]
