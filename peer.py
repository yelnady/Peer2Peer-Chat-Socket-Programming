from repository import *
from sender import Sender
from reciever import Receiver

class Peer:
    def __init__(self):
        self.DS = DataStore()
        # IMPORTANT: start() is a method of the Thread class in Python. When called, it starts a new thread and calls the run() method of the Thread class in that new thread.
        self.r = Sender(my_port, my_name, self.DS).start()  # Send to DRDC that I'm a new user, add me plz
        # switch to see if any one has send me a msg
        self.s = Receiver(my_port, self).start()


# On Unix-based systems like macOS, only the root user is allowed to bind to ports lower than 1024.
my_name = input("Name: ")
my_port = int(input("Port: "))
p = Peer()
