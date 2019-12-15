from model.Departure import Departure

class Ticket():
    def __init__(self, id, departure, first_name, last_name, contact_phone, contact_email, purchase_date, seat,
                 for_deletion, sold_by=""):
        self.id = id
        self.departure = departure
        self.first_name = first_name
        self.last_name = last_name
        self.contact_phone = contact_phone
        self.contact_email = contact_email
        self.purchase_date = purchase_date
        self.seat = seat
        self.for_deletion = for_deletion
        self.sold_by = sold_by

    def serialize(self):
        return (str(self.id) + "|" + self.departure.id + "|" + self.first_name + "|" + self.last_name + "|"
                + self.contact_phone + "|" + self.contact_email + "|" + self.purchase_date + "|" + self.seat + "|"
                + self.for_deletion + "|" + self.sold_by)
    # template ticket_id | departure_id | first_name | last_name | contact_phone | contact_email | date_of_purchase |
    # for_deletion | sold_by
