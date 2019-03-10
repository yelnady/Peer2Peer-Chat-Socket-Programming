from repository import *
from Send import Sender
from Recieve import Receiver

HOST = '127.0.0.1'
DRDCPORT = 65432


class Peer:
    def __init__(self):
        self.DS = DataStore()
        self.r = Sender(myPort, myName, DRDCPORT, self.DS).start()  # Send to DRDC that I'm a new user, add me plz
        # switch to see if any one has send me a msg
        self.s = Receiver(myPort, self).start()


myName = input("Name: ")
myPort = int(input("Port: "))
p = Peer()
