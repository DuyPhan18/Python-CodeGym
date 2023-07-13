class Person:
    def __init__(self, full_name, phone_number):
        self.full_name = full_name
        self.phone_number = phone_number
    def __str__(self):
         return f"Name: {self.full_name}, phone_number: {self.phone_number}"
class Customers(Person):
    def __init__(self, full_name, phone_number):
        super().__init__(full_name, phone_number)
    def __str__(self):
         return f"Name: {self.full_name}, phone_number: {self.phone_number}"
class Admins(Person):
    def __init__(self, full_name, phone_number, username, password):
        super().__init__(full_name, phone_number)
        self.username = username
        self.password = password
    def __str__(self):
         return f'''Name: {self.full_name}, phone_number: {self.phone_number}, 
                    Username: {self.username}, Password: {self.password}'''
class Products:
    def __init__(self, product_name, quantity, price, category ):
        self.product_name = product_name
        self.quantity = quantity
        self.price = price
        self.category = category
    def __str__(self):
         return f"Name: {self.product_name}, quantity: {self.quantity}, price: {self.price}, category:{self.category}"
class Orders:
    def __init__(self, item, quantity, datetime, total):
        self.item = item
        self.quantity = quantity
        self.datetime = datetime
        self.total = total
    def __str__(self):
        return f"item: {self.item}, quantity: {self.quantity}, datetime: {self.datetime}, total: {self.total}"
        