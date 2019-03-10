import random
import socket
import sys
import time
from threading import Thread

from faker import Faker


class Sender(Thread):
    ENCODING = 'utf-8'
    HOST = '127.0.0.1'
    Max_Queue = 10
    def __init__(self, myPort, myName, DRDCPORT, DS):
        Thread.__init__(self)
        self.fake = Faker()
        self.myPort = myPort
        self.myName = myName
        self.DRDCPORT = DRDCPORT
        self.DS = DS

    def generate_fake_data(self):
        data = None
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            try:
                port = int(input("Enter the other node port:\n"))
            except:
                print("Enter a valid port number")
            try:
                s2.connect((self.HOST, self.DRDCPORT))
                data = "request_queue|{}".format(self.myPort)
                s2.sendall(data.encode())
            except:
                print("An error has occured")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            s2.bind((self.HOST, 1))  # FAKE PORT TO LET OTHERS SEND TO ME ON
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
                    s2.connect((self.HOST, port))
                    data = "Receive_From |{}|{}|{}|".format(self.myName, self.myPort, port)
                    data += self.fake.address()
                    s2.sendall(data.encode())
                except:
                    print("Plzz enter a valid port number")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                s2.connect((self.HOST, self.DRDCPORT))
                s2.sendall(data.encode())
        else:
            print("Please resend the message, the queue is full")

    def tell_others(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.HOST, self.DRDCPORT))
            except:
                print("Please, First run the DRDC\nBye-Bye ")
                sys.exit()
            # here we send the connect request to DRDC so it can add to it the users
            data = "connect_request From User: |{}|{}|{}".format(self.myName, self.HOST, self.myPort).encode(
                self.ENCODING)
            s.sendall(data)

    def send_msg(self):
        data = None
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            try:
                port = int(input("Enter the other node port:\n"))
            except:
                print("Enter a valid port number")
            try:
                s2.connect((self.HOST, self.DRDCPORT))
                data = "request_queue|{}".format(self.myPort)
                s2.sendall(data.encode())
            except:
                print("An error has occured")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            s2.bind((self.HOST, 1))  # FAKE PORT TO LET OTHERS SEND TO ME ON
            s2.listen(15)
            conn, addr = s2.accept()
            with conn:
                Queuelength = conn.recv(1024).decode()

        print("QueueLength is "+Queuelength)
        if int(Queuelength)<10:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                    s2.connect((self.HOST, port))
                    data = "Receive_From |{}|{}|{}|".format(self.myName, self.myPort, port)
                    data += input("Msg: \n")
                    s2.sendall(data.encode())
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                    s2.connect((self.HOST, self.DRDCPORT))
                    s2.sendall(data.encode())
            except:print("An error has occured")
        else :
            print("Please resend the message, the queue is full")
    def exit(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            s2.connect((self.HOST, self.DRDCPORT))
            data = "Delete |" + str(self.myPort)
            s2.sendall(data.encode())
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            s2.connect((self.HOST, self.myPort))
            data = "Exit"
            s2.sendall(data.encode())
            sys.exit(0)

    def output_datastore(self):
        with open(self.myName + "_DS.txt", "rb") as f:
            data = f.readlines();
            for line in data:
                print(line)

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
