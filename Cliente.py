from abc import ABC, abstractmethod

class Client:

    def __init__(self, name, id_number):

        if not name.strip():
            raise ValueError("Name cannot be empty")

        if not id_number.strip():
            raise ValueError("ID cannot be empty")

        self._name = name
        self._id_number = id_number

    @property
    def name(self):
        return self._name

    @property
    def id_number(self):
        return self._id_number

    def show_info(self):
        print("Name:", self._name)
        print("ID:", self._id_number)

class Service(ABC):

    def __init__(self, name, price_per_hour, hours):

        if not isinstance(hours, (int, float)):
            raise TypeError("Hours must be numeric")

        if hours <= 0:
            raise ValueError("Hours must be greater than 0")

        self._name = name
        self._price_per_hour = price_per_hour
        self._hours = hours

    @property
    def name(self):
        return self._name

    @property
    def price_per_hour(self):
        return self._price_per_hour

    @property
    def hours(self):
        return self._hours

    @abstractmethod
    def calculate_cost(self, tax=0, discount=0):
        pass

    def show_info(self):
        print("Service:", self._name)
        print("Hours:", self._hours)
        print("Total cost:", self.calculate_cost())

class InvalidServiceError(Exception):
    pass
        
class RoomService(Service):

    def __init__(self, hours):
        super().__init__("Room Service", 50, hours)

    def calculate_cost(self, tax=0, discount=0):

        total = self.price_per_hour * self.hours

        total += total * tax
        total -= discount

        return total

    
class EquipmentService(Service):

    def __init__(self, days):
        super().__init__("Equipment Service", 30, days)

    def calculate_cost(self, tax=0, discount=0):

        total = self.price_per_hour * self.hours

        total += total * tax
        total -= discount

        return total

    
class AdvisoryService(Service):

    def __init__(self, hours):
        super().__init__("Advisory Service", 100, hours)

    def calculate_cost(self, tax=0, discount=0):

        total = self.price_per_hour * self.hours

        total += total * tax
        total -= discount

        return total

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
    with open("log.txt", "a") as f:
        f.write(f"Error: {str(e)}\n")


class SystemManager:
    def __init__(self):
        self.clients = []
        self.services = []
        self.reservations = []

    def add_client(self, client):
        try:
            if not isinstance(client, Client):
                raise TypeError("Invalid client type")
        except Exception as e:
            print("Error adding client")
            log_error(e)
        else:
            self.clients.append(client)
            print("Client added successfully")
        finally:
            print("Client process finished\n")

    def add_service(self, service):
        try:
            if not isinstance(service, Service):
                raise TypeError("Invalid service type")
        except Exception as e:
            print("Error adding service")
            log_error(e)
        else:
            self.services.append(service)
            print("Service added successfully")
        finally:
            print("Service process finished\n")

    def make_reservation(self, client, service):
        try:
            reservation = Reservation(client, service)
        except Exception as e:
            print("Error creating reservation")
            log_error(e)
        else:
            self.reservations.append(reservation)
            reservation.confirm()
        finally:
            print("Reservation process finished\n")


#TEST

client1 = Client("Paula", "123")
client1.show_info()

print("-----")

service1 = RoomService(2)
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
    bad_service = RoomService(-2)
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

print("\n===== SYSTEM TEST (STUDENT CONTRIBUTION) =====\n")

system = SystemManager()

# 1 Cliente válido
try:
    c1 = Client("Carlos", "999")
    system.add_client(c1)
except Exception as e:
    log_error(e)

# 2 Cliente inválido
try:
    c2 = Client("", "")
    system.add_client(c2)
except Exception as e:
    log_error(e)

# 3 Servicio válido
try:
    s1 = RoomService(2)
    system.add_service(s1)
except Exception as e:
    log_error(e)

# 4 Servicio inválido
try:
    s2 = RoomService(-1)
    system.add_service(s2)
except Exception as e:
    log_error(e)

# 5 Servicio válido
try:
    s3 = EquipmentService(3)
    system.add_service(s3)
except Exception as e:
    log_error(e)

# 6 Servicio inválido
try:
    s4 = AdvisoryService(0)
    system.add_service(s4)
except Exception as e:
    log_error(e)

# 7 Reserva válida
system.make_reservation(c1, s1)

# 8 Reserva inválida (cliente falso)
system.make_reservation("fake_client", s1)

# 9 Reserva inválida (servicio falso)
system.make_reservation(c1, "fake_service")

# 10 Reserva válida adicional
try:
    s5 = AdvisoryService(2)
    system.add_service(s5)
    system.make_reservation(c1, s5)
except Exception as e:
    log_error(e)
