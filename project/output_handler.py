def print_default_menu():
    print("|2| Exit application")
    print("|3| Overview of unrealised flights")
    print("|4| Flight search")
    print("|5| Multiple-criteria Flight search")
    print("|6| 10 Cheapest flights from departure to destination")
    print("|7| Flexible departure date")

def print_departure_search_menu():
    print("|1| Departure airport")
    print("|2| Destination airport")
    print("|3| Departure date")
    print("|4| Arrival date")
    print("|5| Departure time")
    print("|6| Arrival time")
    print("|7| Airline")
    print("|0| Return to previous menu")

def print_departure_search_table(results, mode = ""):
    if mode == "Single":
        departure = results
        print("{:16}{:20}{:20}{:25}{:25}{:10}{:}".format("Departure ID", "From", "To", "Departure date and time",
                                                         "Arrival date and time",
                                                         "Price", "Airline"))
        print("{:16}{:20}{:20}{:10} at {:11}{:10} at {:11}{:10}{:}".format(departure.id,
                                                                           departure.flight.departure_airport.city,
                                                                           departure.flight.destination_airport.city,
                                                                           departure.departure_date,
                                                                           departure.flight.departure_time,
                                                                           departure.arrival_date,
                                                                           departure.flight.arrival_time,
                                                                           departure.flight.price + " €",
                                                                           departure.flight.airline))

    elif len(results) > 0:
        if mode == "":
            print("{:16}{:20}{:20}{:25}{:25}{:10}{:}".format("Departure ID", "From", "To", "Departure date and time",
                                                           "Arrival date and time",
                                                           "Price", "Airline"))
            for departure, number in zip(results, range(1001)):
                print("{:16}{:20}{:20}{:10} at {:11}{:10} at {:11}{:10}{:}".format(departure.id,
                                                                                   departure.flight.departure_airport.city,
                                                                                   departure.flight.destination_airport.city,
                                                                                   departure.departure_date,
                                                                                   departure.flight.departure_time,
                                                                                   departure.arrival_date,
                                                                                   departure.flight.arrival_time,
                                                                                   departure.flight.price + " €",
                                                                                   departure.flight.airline))
                if(number == 1000):
                    print("Search results have been omitted. Showing first 1000 results")
                    return
        elif mode == "Duration":
            print("{:16}{:20}{:20}{:25}{:25}{:15}{:10}{:}".format("Departure ID", "From", "To", "Departure date and time",
                                                             "Arrival date and time", "Duration",
                                                             "Price", "Airline"))
            for departure in results:
                departure_datetime_obj = departure_datetime(departure.departure_date, departure.flight.departure_time)
                arrival_datetime_obj = departure_datetime(departure.arrival_date, departure.flight.arrival_time)
                duration_obj = arrival_datetime_obj - departure_datetime_obj
                distance = int(duration_obj.total_seconds() / 60)
                print("{:16}{:20}{:20}{:10} at {:11}{:10} at {:11}{:15}{:10}{:}".format(departure.id,
                                                                                   departure.flight.departure_airport.city,
                                                                                   departure.flight.destination_airport.city,
                                                                                   departure.departure_date,
                                                                                   departure.flight.departure_time,
                                                                                   departure.arrival_date,
                                                                                   departure.flight.arrival_time,
                                                                                   str(distance) + " Minutes" ,
                                                                                   departure.flight.price + " €",
                                                                                   departure.flight.airline))

    else:
        print("No matching results found")


def print_flight_search_table(results, single=""):
    if single == "Single":
        print("{:16}{:22}{:22}{:30}{:24}{:10}{:30}{:}".format("Flight number", "From", "To", "Departure dates",
                                                              "Overnight flight?", "Price", "Airplane Model", "Airline"))
        flight = results
        print("{:16}{:22}{:22}{:30}{:24}{:10}{:30}{:}".format(flight.flight_number,
                                                              flight.departure_airport.city,
                                                              flight.destination_airport.city,
                                                              flight.days + " at " + flight.departure_time,
                                                              flight.overnight + " - Arrives at " + flight.arrival_time,
                                                              flight.price + " €",
                                                              flight.airplane.name,
                                                              flight.airline))
    else:
        if len(results) > 0:
            print(
                "{:16}{:22}{:22}{:30}{:24}{:10}{:30}{:}".format("Flight number", "From", "To", "Departure dates",
                                                                "Overnight flight?",
                                                                "Price", "Airplane Model", "Airline"))
            for flight in results:
                print("{:16}{:22}{:22}{:30}{:24}{:10}{:30}{:}".format(flight.flight_number,
                                                                      flight.departure_airport.city,
                                                                      flight.destination_airport.city,
                                                                      flight.days + " at " + flight.departure_time,
                                                                      flight.overnight + " - Arrives at " + flight.arrival_time,
                                                                      flight.price + " €",
                                                                      flight.airplane.name,
                                                                      flight.airline))
        else:
            print("No matching results found")

# Takes a single ticket and prints it if mode is "Single"
# Takes a list of tickets and prints them all if mode is "Multi"
def print_ticket(ticket, mode):
    # print the default table header
    print("{:12}{:14}{:16}{:16}{:22}{:22}{:24}{:20}{:30}{:20}{:20}".format("Ticket ID", "Departure ID", "From", "To",
                                                                           "Departure date", "Arrival date",
                                                                           "Ticket holder",
                                                                           "Contact phone",
                                                                           "Contact email", "Date of purchase", "Seat"))
    if mode == "Single":  # we pass one single ticket - a non iterable
        if ticket.seat == "":
            seat = "Not checked in"
        else:
            seat = ticket.seat
        print("{:12}{:14}{:16}{:16}{:22}{:22}{:24}{:20}{:30}{:20}{:20}".format(ticket.id, ticket.departure.id,
                                                                               ticket.departure.flight.departure_airport.city,
                                                                               ticket.departure.flight.destination_airport.city,
                                                                               ticket.departure.departure_date + " at " +
                                                                               ticket.departure.flight.departure_time,
                                                                               ticket.departure.arrival_date + " at " +
                                                                               ticket.departure.flight.arrival_time,
                                                                               ticket.first_name + " " + ticket.last_name,
                                                                               ticket.contact_phone,
                                                                               ticket.contact_email,
                                                                               ticket.purchase_date,
                                                                               seat))
    elif mode == "Multi":  # we pass a list of tickets to print - iterable
        tickets = ticket  # so in order to overload we declare a list called tickets and assign it the paramter's list
        for ticket in tickets:
            if ticket.seat == "":
                seat = "Not checked in"
            else:
                seat = ticket.seat
            print("{:12}{:14}{:16}{:16}{:22}{:22}{:24}{:20}{:30}{:20}{:20}".format(ticket.id, ticket.departure.id,
                                                                                   ticket.departure.flight.departure_airport.city,
                                                                                   ticket.departure.flight.destination_airport.city,
                                                                                   ticket.departure.departure_date + " at " +
                                                                                   ticket.departure.flight.departure_time,
                                                                                   ticket.departure.arrival_date + " at " +
                                                                                   ticket.departure.flight.arrival_time,
                                                                                   ticket.first_name + " " + ticket.last_name,
                                                                                   ticket.contact_phone,
                                                                                   ticket.contact_email,
                                                                                   ticket.purchase_date,
                                                                                   seat))
