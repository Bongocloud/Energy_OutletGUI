
class Order:

    def __init__(self, customer_name, brand, drink, price):
        self.customer_name = customer_name
        self.brand = brand
        self.drink = drink
        self.price = price

    # -------- Setters --------

    def set_customer_name(self, customer_name):
        self.customer_name = customer_name

    def set_brand(self, brand):
        self.brand = brand

    def set_drink(self, drink):
        self.drink = drink

    def set_price(self, price):
        self.price = price

    # -------- Getters --------

    def get_customer_name(self):
        return self.customer_name

    def get_brand(self):
        return self.brand

    def get_drink(self):
        return self.drink

    def get_price(self):
        return self.price

    # -------- Summary --------

    def summary(self):
        return (
            f"{self.customer_name} ordered "
            f"{self.drink} from {self.brand} "
            f"for ${self.price:.2f}"
        )