from model.User import User
from model.Enums import Role

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

        #TODO: Fix this
    def __str__(self):
        return super().__str__() + " " + str(self.passport_number)

    def serialize(self):
        return (self.username + "|" + self.password +  "|" + self.first_name +  "|" + self.last_name +  "|" + self.phone
        +  "|" + self.email +  "|" + self.passport_number +  "|" + self.citizenship + "|" + str(self.gender))