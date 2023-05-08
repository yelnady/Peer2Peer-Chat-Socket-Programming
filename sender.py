import random
import socket
import sys
import time
from threading import Thread
from DRDC import DRDC

from faker import Faker

# This class represents a sender which will be executed in a separate thread. 
# It will be used to send messages and connect to other users.
# IMPORTANT: This class inherits from the Thread class --> Therefore we had to call the constructor of the Thread class, and we had to define a run function
class Sender(Thread):
    # Class-level constants and variables
    ENCODING = 'utf-8' # Encoding to be used for encoding data
    HOST_ADDR = DRDC.HOST # Host address, which the IPV4 address of the DRDC.
    DRDCPORT = DRDC.PORT # Port number of DRDC
    Max_Queue = 10 # Maximum length of the messages in queue
    
    def __init__(self, my_port, my_name, DS):
        Thread.__init__(self)
        self.fake = Faker()
        self.my_port = my_port # Port number of the current user
        self.my_name = my_name # Name of the current user
        self.DS = DS

    # The run() method is typically where the main work of the thread is done. 
    # It should contain a loop or other control structure that allows the thread to repeatedly perform its task. Once the run() method returns, the thread will exit and its resources will be released.
    # Once the run() method returns, the thread will exit and its resources will be released.
    def run(self):
        self.tell_others()
        while True:
            print('*' * 100)
            print("1- Send Your Msg     2- Send a Fake Data     3- Output Data Store    4- Exit This Connection")
            # what to be done, I'll send to specific port, telling him what's my name and my port
            try:
                n = int(input("Enter Number:\n"))
            except:
                print("An Error has occured");
                continue
            if n == 1:
                self.send_msg()
            elif n == 2:
                self.generate_fake_data()
            elif n == 3:
                self.output_datastore()
                # will open the file corresponding to my name and printing al7agat lly gwah
            elif n == 4:
                # It will be a msg to there of deletion, can't perform it 3ltol .. l2n ana fat7 kza nos5a mmn albrnamg
                self.exit()
            else:
                print("Plzz choose a correct number")
            time.sleep(random.randint(0, 5))

    
    # We will send a message to the DRDC that starts with connect_request, and it will understand I am a new node, and will notify all available users that I have joined!
    def tell_others(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.HOST_ADDR, self.DRDCPORT))
            except:
                print("Please, First run the DRDC\nBye-Bye ")
                sys.exit(0)
            # here we send the connect request to DRDC so it can add to it the users
            connect_request_string = "connect_request From User: |{}|{}|{}".format(self.my_name, self.HOST_ADDR, self.my_port).encode(self.ENCODING)
            s.sendall(connect_request_string)

    # This function is used to send a message to another user
    def send_msg(self):
        data = None # Initialize the variable data as None
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2: # create a socket object for connection
            try:
                port = int(input("Enter the other node port:\n")) # Prompt user to enter the port number of the other user
                try:
                    s2.connect((self.HOST_ADDR, self.DRDCPORT)) # connect to the DRDC
                    data = "request_queue|{}".format(self.my_port) # form a request queue for the message, it needs to start with the string "request_queue" to be parsed
                    s2.sendall(data.encode(self.ENCODING)) # send the request queue to DRDC
                except:
                    print("An error has occured") # if there is an error then print an error message
            except:
                print("Enter a valid port number") # If the user enters an invalid input, then print an error message
            
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2: # create another socket object for connection
            s2.bind((self.HOST_ADDR, 1)) # bind the fake port to listen to messages from other users
            s2.listen(15) # Start listening for connections from other users
            conn, addr = s2.accept() # accept the connection request and get the address of the connected user
            with conn:
                Queuelength = conn.recv(1024).decode() # receive the length of the queue

        print("QueueLength is "+Queuelength)
        if int(Queuelength)<10:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                    s2.connect((self.HOST_ADDR, port))
                    data = "Receive_From |{}|{}|{}|".format(self.my_name, self.my_port, port)
                    data += input("Msg: \n")
                    s2.sendall(data.encode(self.ENCODING))
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                    s2.connect((self.HOST_ADDR, self.DRDCPORT))
                    s2.sendall(data.encode(self.ENCODING))
            except:print("An error has occured")
        else :
            print("Please resend the message, the queue is full")


    def exit(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            s2.connect((self.HOST_ADDR, self.DRDCPORT))
            data = "delete|" + str(self.my_port)
            s2.sendall(data.encode(self.ENCODING))


        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            s2.connect((self.HOST_ADDR, self.my_port)) # This time I am sending a message to myself (my_port), not to the DRDC
            data = "exit"
            s2.sendall(data.encode(self.ENCODING))
            sys.exit(0)

    def output_datastore(self):
        with open(self.my_name + "_DS.txt", "rb") as f:
            data = f.readlines();
            for line in data:
                print(line)

   


    def generate_fake_data(self):
        data = None

        # Creating a socket for sending data
        # This is a socket object with IPv4 and TCP protocol
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            try:
                port = int(input("Enter the other node port:\n"))
            except:
                print("Enter a valid port number")
            try:
                s2.connect((self.HOST_ADDR, self.DRDCPORT))
                data = "request_queue|{}".format(self.my_port)
                s2.sendall(data.encode(self.ENCODING))
            except:
                print("An error has occured")

        # Creating a new socket for receiving data
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2: 
            s2.bind((self.HOST_ADDR, 1))  # FAKE PORT TO LET OTHERS SEND TO ME ON
            s2.listen(15)
            conn, addr = s2.accept()
            with conn:
                Queuelength = conn.recv(1024).decode()

        print("QueueLength is " + Queuelength)
        if int(Queuelength )< 10:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                try:port = int(input("Enter the other node port:\n"))
                except:print("Enter a valid port number")

                try:
                    s2.connect((self.HOST_ADDR, port))
                    data = "Receive_From |{}|{}|{}|".format(self.my_name, self.my_port, port)
                    data += self.fake.address()
                    s2.sendall(data.encode(self.ENCODING))
                except:
                    print("Plzz enter a valid port number")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                s2.connect((self.HOST_ADDR, self.DRDCPORT))
                s2.sendall(data.encode(self.ENCODING))
        else:
            print("Please resend the message, the queue is full")

