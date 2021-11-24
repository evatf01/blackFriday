import random
from threading import Thread, Lock
from time import sleep
from random import uniform

NUMBER_OF_CUSTOMERS = 8


class Till():
    """Simula el uso de la caja de la tienda para las ofertas disponibles"""

    available_products = 5

    @classmethod
    def hasProducts(cls):
        """Indica si quedan productos en oferta"""
        return cls.available_products > 0

    def __init__(self):
        self.myLock = Lock()
        print('[CAJA] Caja abierta. Productos disponibles: ' + str(Till.available_products))

    def pay(self, customer):
        """Permite al cliente pagar el producto en oferta, lo que hace que quede una unidad menos"""

        if Till.hasProducts():
            if Till.available_products == 0:
                print("No hay productos disponibles")
                exit(0)

            print('[CAJA] Cliente (' + customer + ') va a a pagar...')
            if self.myLock.locked():
                print(customer + " esta esperando")

            self.myLock.acquire()
            print("\nCaja ocupada por cliente " + customer)
            sleep(uniform(1, Customer.MAX_TIME))
            print("Caja libre")
            self.myLock.release()
            Till.available_products = Till.available_products - 1
            print("\nprodutos disponibles: " + str(Till.available_products))


class Customer(Thread):
    """Simula el comportamiento de los clientes del centro comercial"""

    MAX_TIME = 10

    sharedTill = Till()

    @classmethod
    def setTill(cls, till):
        cls.sharedTill = till

    def __init__(self, number):
        Thread.__init__(self)
        self.name = str(number)

    def getName(self):
        return self.name

    def walk(self):
        """Se da un paseíllo por ahí durante un rato"""
        print('[CLIENTE ' + self.name + '] Me doy una vuelta...')
        sleep(uniform(1, Customer.MAX_TIME))

    def hasToBuy(self):
        """Decide si va a comprar el producto"""
        return random.choice([True, False])

    def run(self):
        self.walk()
        if self.hasToBuy():
            Customer.sharedTill.pay(self.name)
        else:
            print("El cliente " + self.name + " no va comprar")
            print("adios")
        # Completar...


if __name__ == '__main__':
    myTill = Till()
    Customer.setTill(myTill)

    for i in range(NUMBER_OF_CUSTOMERS):
        cli = Customer(i)
        cli.start()

    # Completar (crear hilos y lanzarlos)
