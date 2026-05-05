class Client:

    def __init__(self,name,id_number):
        self.name = name
        self.id_number=id_number

    def show_info(self):
        print("Name:", self.name)
        print("ID:", self.id_number)





class Service:

    def __init__(self,name, price_per_hour, hours):
        self.name = name
        self.price_per_hour = price_per_hour
        self.hours = hours

    def calculate_cost(self):
        return self.price_per_hour * self.hours
    
    def show_info(self):
        print("Service:", self.name)
        print("Hours:",self.hours)
        print("Total cost:", self.calculate_cost())



