
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
            candidates[:] = [departure for departure in candidates if search_criteria['airline'].lower() == departure.flight.airline.lower()]
    return candidates

def flight_search_flexible(departures, search_criteria):
    candidates = departures[:]
    for departure in candidates:
        if search_criteria["departure_airport"] != "":
            candidates[:] = [departure for departure in candidates if search_criteria["departure_airport"] == departure.flight.departure_airport]
        if search_criteria["destination_airport"] != "":
            candidates[:] = [departure for departure in candidates if search_criteria["destination_airport"] == departure.flight.destination_airport]
