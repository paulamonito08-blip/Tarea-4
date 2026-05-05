class Client:

    def __init__(self,name,id_number):
        if not name:
            raise ValueError("Name cannot be empty")
        if not id_number:
            raise ValueError("ID cannot be empty")
        self.name = name
        self.id_number=id_number

    def show_info(self):
        print("Name:", self.name)
        print("ID:", self.id_number)

class Service:           
    def __init__(self,name,price_per_hour, hours):
        if hours <= 0:
            raise ValueError("Hours must be greater than 0")
        
        self.name = name
        self.price_per_hour = price_per_hour
        self.hours = hours

    def calculate_cost(self):
        return self.price_per_hour * self.hours
    
    def show_info(self):
        print("Service:", self.name)
        print("Hours:",self.hours)
        print("Total cost:", self.calculate_cost())

class InvalidServiceError(Exception):
    pass
        
class RoomService(Service):

    def __init__(self,hours):
        if hours <= 0:
            raise InvalidServiceError("Hours must be greater than 0")
        
        super().__init__("Room Service", 50, hours)

    
class EquipmentService (Service):
    def __init__ (self,days):
        if days <= 0:
            raise InvalidServiceError("Days must be greater than 0")
        
        super().__init__("Equipment Service", 30, days)

    
class AdvisoryService (Service):
    def __init__(self,hours):
        if hours <= 0:
            raise InvalidServiceError("Hours must be greater than 0")
        
        super().__init__("Advisory Service", 100, hours)

class Reservation:

    def __init__(self,client,service):
        if not isinstance(client,Client):
            raise TypeError("Invalid client")
        if not isinstance(service,Service):
            raise TypeError("Invalid service")
        
        self.client = client
        self.service = service
        self.status = "Pending"

    def confirm(self):
        cost = self.service.calculate_cost()
        self.status ="Confirmed"
        print("Reservation confirmed")
        print("Client:", self.client.name)
        print("Service:", self.service.name)
        print("Total cost:", cost)

    def cancel(self):
        self.status = "Cancelled"
        print("Reservation cancelled")

def log_error(e):
    """Función auxiliar para simular logging de errores"""
    print(f"[LOG] Error: {e}")



#TEST

client1 = Client("Paula", "123")
client1.show_info()

print("-----")

service1 = Service("Room", 50, 2)
service1.show_info()

print("-----RESERVATION-----")

reservation1 = Reservation(client1, service1)
reservation1.confirm()

#---TEST ERRORS----

print("\n---TEST ERRORS---")

try:
    bad_client =Client("","")
except Exception as e:
    print("Error:", e)

try:
    bad_service = Service("Room", 50,-2)
except Exception as e:
    print("Error:",e)

print("\n====SIMULATIONS====")

#Cliente válido
try:
    c1 = Client("Ana","121")
    print("CLient created")
except Exception as e:
    print("Error:", e)
    log_error(e)

#Cliente inválido
try:
    c2 = Client("","")
except Exception as e:
    print("Error:", e)
    log_error(e)

#RoomService válido
try:
    s1 = RoomService(2)
    print("Room service created")
    s1.show_info()
except Exception as e:
    print("Error:", e)
    log_error(e)

#RoomService inválido
try:
    s2 = RoomService(-1)
except Exception as e:
    print("Error:", e)
    log_error(e)

#EquipmentService válido 
try:
    s3 = EquipmentService(3)
    print("Equipment service created")
    s3.show_info()
except Exception as e:
    print("Error:", e)
    log_error(e)

#AdvisoryService inválido
try:
    s4 =AdvisoryService(0)
except Exception as e:
    print("Error:", e)
    log_error(e)

#AdvisorService válido
try:
    s5 = AdvisoryService(2)
    print("AdvisoryService created")
    s5.show_info()
except Exception as e:
    print("Error:", e)
    log_error(e)


#Reserva válida
try:
    if 'c1' in locals() and's1' in locals():
        r1 = Reservation(c1, s1)
        r1.confirm()
except Exception as e:
    print("Error:", e)
    log_error(e)

#Reserva inválida
try:
    r2= Reservation("fake_client", s1)
except Exception as e:
    print("Error:", e)
    log_error(e)

#Reserva con servicio inválido
try:
    r3 = Reservation(c1, "fake_service")
except Exception as e:
    print("Error:", e)
    log_error(e)

#Cncelación de reserva
try:
    if 'r1' in locals():
        r1.cancel()
except Exception as e:
    print("Error:", e)
    log_error(e)



