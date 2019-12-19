from model.User import User
from model.Enums import Role


class Customer(User):
    def __init__(self, username, password, first_name, last_name, phone, email, passport_number="", nationality="",
                 gender=None):

        super().__init__(username, password, first_name, last_name, Role.Customer)
        self.phone = phone
        self.email = email
        self.passport_number = passport_number
        self.nationality = nationality
        self.gender = gender

    def serialize(self):
        return (self.username + "|" + self.password + "|" + self.first_name + "|" + self.last_name + "|" + self.phone
                + "|" + self.email + "|" + self.passport_number + "|" + self.nationality + "|" + str(self.gender))
