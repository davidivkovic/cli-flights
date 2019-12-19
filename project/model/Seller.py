from model.User import User
from model.Enums import Role

class Seller(User):
    def __init__(self, username, password, first_name, last_name):
        super().__init__(username, password, first_name, last_name, Role.Seller)

    def serialize(self):
        return self.username + "|" + self.password + "|" + self.first_name + "|" + self.last_name