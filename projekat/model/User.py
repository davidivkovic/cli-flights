class User:
    def __init__(self, username, password, first_name, last_name, role):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.role = role

    def __str__(self): #TODO: fix this
        return self.first_name + " " + self.last_name + " " + str(self.role.name)











