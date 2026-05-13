from abc import ABC, abstractmethod
from datetime import datetime


# ============================================================
# ARCHIVO DE LOGS
# ============================================================

LOG_FILE = "log.txt"


def log_error(e):
    """Registra errores en un archivo de texto."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{fecha}] ERROR: {str(e)}\n")


def log_event(message):
    """Registra eventos importantes del sistema."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{fecha}] EVENT: {message}\n")


# ============================================================
# EXCEPCIONES PERSONALIZADAS
# ============================================================

class SystemErrorBase(Exception):
    """Excepcion base del sistema."""
    pass


class InvalidClientError(SystemErrorBase):
    """Error para datos invalidos del cliente."""
    pass


class InvalidServiceError(SystemErrorBase):
    """Error para datos invalidos del servicio."""
    pass


class InvalidReservationError(SystemErrorBase):
    """Error para reservas invalidas."""
    pass


class ServiceUnavailableError(SystemErrorBase):
    """Error cuando un servicio no esta disponible."""
    pass


class OperationNotAllowedError(SystemErrorBase):
    """Error cuando una operacion no es permitida."""
    pass


# ============================================================
# CLASE ABSTRACTA GENERAL
# ============================================================

class SystemEntity(ABC):
    """Clase abstracta general para entidades del sistema."""

    def __init__(self, code):
        if not str(code).strip():
            raise ValueError("Code cannot be empty")
        self._code = str(code).strip()

    @property
    def code(self):
        return self._code

    @abstractmethod
    def show_info(self):
        pass


# ============================================================
# CLIENTE
# ============================================================

class Client(SystemEntity):

    def __init__(self, name, id_number, email="cliente@softwarefj.com"):
        try:
            super().__init__(id_number)

            if not name.strip():
                raise InvalidClientError("Name cannot be empty")

            if not id_number.strip():
                raise InvalidClientError("ID cannot be empty")

            if "@" not in email or "." not in email:
                raise InvalidClientError("Email is not valid")

            self._name = name.strip()
            self._id_number = id_number.strip()
            self._email = email.strip()

        except AttributeError as e:
            raise InvalidClientError("Client data must be text") from e

    @property
    def name(self):
        return self._name

    @property
    def id_number(self):
        return self._id_number

    @property
    def email(self):
        return self._email

    def show_info(self):
        print("Name:", self._name)
        print("ID:", self._id_number)
        print("Email:", self._email)


# ============================================================
# SERVICIO ABSTRACTO
# ============================================================

class Service(SystemEntity, ABC):

    def __init__(self, name, price_per_hour, hours, available=True):
        try:
            super().__init__(name)

            if not str(name).strip():
                raise InvalidServiceError("Service name cannot be empty")

            if not isinstance(price_per_hour, (int, float)):
                raise InvalidServiceError("Price must be numeric")

            if price_per_hour <= 0:
                raise InvalidServiceError("Price must be greater than 0")

            if not isinstance(hours, (int, float)):
                raise TypeError("Hours must be numeric")

            if hours <= 0:
                raise InvalidServiceError("Hours must be greater than 0")

            self._name = name
            self._price_per_hour = price_per_hour
            self._hours = hours
            self._available = available

        except TypeError as e:
            raise InvalidServiceError("Invalid service numeric data") from e

    @property
    def name(self):
        return self._name

    @property
    def price_per_hour(self):
        return self._price_per_hour

    @property
    def hours(self):
        return self._hours

    @property
    def available(self):
        return self._available

    def set_available(self, available):
        self._available = bool(available)
        log_event(f"Service availability changed: {self.name} -> {self.available}")

    def validate_availability(self):
        if not self._available:
            raise ServiceUnavailableError(f"Service not available: {self.name}")

    @abstractmethod
    def calculate_cost(self, tax=0, discount=0):
        pass

    @abstractmethod
    def describe_service(self):
        pass

    def show_info(self):
        print("Service:", self._name)
        print("Hours:", self._hours)
        print("Description:", self.describe_service())
        print("Total cost:", self.calculate_cost())


# ============================================================
# SERVICIOS ESPECIALIZADOS
# ============================================================

class RoomService(Service):

    def __init__(self, hours, available=True):
        super().__init__("Room Service", 50, hours, available)

    def calculate_cost(self, tax=0, discount=0):
        total = self.price_per_hour * self.hours
        total += total * tax
        total -= discount

        if total < 0:
            raise InvalidServiceError("Total cost cannot be negative")

        return total

    def describe_service(self):
        return "Room reservation service for meetings or work sessions"


class EquipmentService(Service):

    def __init__(self, days, available=True):
        super().__init__("Equipment Service", 30, days, available)

    def calculate_cost(self, tax=0, discount=0):
        total = self.price_per_hour * self.hours
        total += total * tax
        total -= discount

        if total < 0:
            raise InvalidServiceError("Total cost cannot be negative")

        return total

    def describe_service(self):
        return "Equipment rental service charged by day"


class AdvisoryService(Service):

    def __init__(self, hours, available=True):
        super().__init__("Advisory Service", 100, hours, available)

    def calculate_cost(self, tax=0, discount=0):
        total = self.price_per_hour * self.hours
        total += total * tax
        total -= discount

        if total < 0:
            raise InvalidServiceError("Total cost cannot be negative")

        return total

    def describe_service(self):
        return "Specialized advisory service charged by hour"


# ============================================================
# RESERVA
# ============================================================

class Reservation(SystemEntity):

    counter = 1

    def __init__(self, client, service):
        super().__init__(f"RES-{Reservation.counter}")
        Reservation.counter += 1

        if not isinstance(client, Client):
            raise InvalidReservationError("Invalid client")

        if not isinstance(service, Service):
            raise InvalidReservationError("Invalid service")

        self.client = client
        self.service = service
        self.status = "Pending"

    def confirm(self):
        try:
            if self.status != "Pending":
                raise OperationNotAllowedError("Only pending reservations can be confirmed")

            self.service.validate_availability()
            cost = self.service.calculate_cost()
            self.status = "Confirmed"

        except SystemErrorBase as e:
            log_error(e)
            print("Reservation could not be confirmed:", e)

        else:
            print("Reservation confirmed")
            print("Client:", self.client.name)
            print("Service:", self.service.name)
            print("Total cost:", cost)
            log_event(f"Reservation confirmed: {self.code}")

        finally:
            print("Confirmation process finished")

    def cancel(self):
        try:
            if self.status == "Cancelled":
                raise OperationNotAllowedError("Reservation is already cancelled")

            self.status = "Cancelled"

        except OperationNotAllowedError as e:
            log_error(e)
            print("Reservation could not be cancelled:", e)

        else:
            print("Reservation cancelled")
            log_event(f"Reservation cancelled: {self.code}")

        finally:
            print("Cancellation process finished")

    def process(self):
        try:
            if self.status != "Confirmed":
                raise OperationNotAllowedError("Only confirmed reservations can be processed")

        except OperationNotAllowedError as e:
            log_error(e)
            print("Reservation could not be processed:", e)

        else:
            print("Reservation processed successfully")
            log_event(f"Reservation processed: {self.code}")

        finally:
            print("Processing process finished")

    def show_info(self):
        print("Reservation:", self.code)
        print("Client:", self.client.name)
        print("Service:", self.service.name)
        print("Status:", self.status)


# ============================================================
# ADMINISTRADOR DEL SISTEMA
# ============================================================

class SystemManager:
    def __init__(self):
        self.clients = []
        self.services = []
        self.reservations = []

    def add_client(self, client):
        try:
            if not isinstance(client, Client):
                raise InvalidClientError("Invalid client type")

        except SystemErrorBase as e:
            print("Error adding client")
            log_error(e)

        else:
            self.clients.append(client)
            print("Client added successfully")
            log_event(f"Client added: {client.name}")

        finally:
            print("Client process finished\n")

    def add_service(self, service):
        try:
            if not isinstance(service, Service):
                raise InvalidServiceError("Invalid service type")

        except SystemErrorBase as e:
            print("Error adding service")
            log_error(e)

        else:
            self.services.append(service)
            print("Service added successfully")
            log_event(f"Service added: {service.name}")

        finally:
            print("Service process finished\n")

    def make_reservation(self, client, service):
        try:
            reservation = Reservation(client, service)

        except SystemErrorBase as e:
            print("Error creating reservation")
            log_error(e)

        else:
            self.reservations.append(reservation)
            reservation.confirm()
            log_event(f"Reservation created: {reservation.code}")
            return reservation

        finally:
            print("Reservation process finished\n")


# ============================================================
# SIMULACIONES DEL SISTEMA
# ============================================================

if __name__ == "__main__":

    print("===== SISTEMA INTEGRAL SOFTWARE FJ =====\n")

    system = SystemManager()

    # 1 Cliente valido
    try:
        c1 = Client("Carlos", "999", "carlos@email.com")
        system.add_client(c1)
    except Exception as e:
        print("Error:", e)
        log_error(e)

    # 2 Cliente valido
    try:
        c2 = Client("Ana", "121", "ana@email.com")
        system.add_client(c2)
    except Exception as e:
        print("Error:", e)
        log_error(e)

    # 3 Cliente invalido
    try:
        c3 = Client("", "", "correo_invalido")
        system.add_client(c3)
    except Exception as e:
        print("Error:", e)
        log_error(e)

    # 4 Servicio de sala valido
    try:
        s1 = RoomService(2)
        system.add_service(s1)
    except Exception as e:
        print("Error:", e)
        log_error(e)

    # 5 Servicio de equipos valido
    try:
        s2 = EquipmentService(3)
        system.add_service(s2)
    except Exception as e:
        print("Error:", e)
        log_error(e)

    # 6 Servicio de asesoria valido
    try:
        s3 = AdvisoryService(2)
        system.add_service(s3)
    except Exception as e:
        print("Error:", e)
        log_error(e)

    # 7 Servicio invalido
    try:
        s4 = RoomService(-1)
        system.add_service(s4)
    except Exception as e:
        print("Error:", e)
        log_error(e)

    # 8 Reserva valida
    r1 = system.make_reservation(c1, s1)

    # 9 Reserva invalida por cliente falso
    system.make_reservation("fake_client", s1)

    # 10 Reserva invalida por servicio falso
    system.make_reservation(c1, "fake_service")

    # 11 Reserva con servicio no disponible
    try:
        s2.set_available(False)
        r2 = system.make_reservation(c2, s2)
    except Exception as e:
        print("Error:", e)
        log_error(e)

    # 12 Cancelacion de reserva valida
    try:
        if r1:
            r1.cancel()
    except Exception as e:
        print("Error:", e)
        log_error(e)

    # 13 Procesamiento incorrecto de reserva cancelada
    try:
        if r1:
            r1.process()
    except Exception as e:
        print("Error:", e)
        log_error(e)

    # 14 Demostracion de calculo con impuesto y descuento
    try:
        print("\nCosto con impuesto y descuento:")
        print("Servicio:", s3.name)
        print("Costo:", s3.calculate_cost(tax=0.19, discount=20))
    except Exception as e:
        print("Error:", e)
        log_error(e)

    print("\n===== FIN DE LAS SIMULACIONES =====")
    print("Revise el archivo log.txt para ver eventos y errores registrados.")
