import random
import socket
import sys
import time
from threading import Thread


class Receiver(Thread):
    HOST = '127.0.0.1'

    def __init__(self, myPort, p):
        Thread.__init__(self)
        self.myPort = myPort
        self.mine = p

    def receive(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            try:
                s2.bind((self.HOST, self.myPort))  # FAKE PORT TO LET OTHERS SEND TO ME ON
                s2.listen(15)
                while 1:
                    conn, addr = s2.accept()
                    with conn:
                        data = conn.recv(1024).decode()
                        if not data: break
                        if "Receive_From" in data:
                            arr = data.split('|')
                            if len(arr) == 5:  # ignoring the first one ahu arr[0]
                                sender_name = arr[1];
                                sender_port = arr[2];
                                reciever_port = arr[3];
                                data = arr[4];
                                print("Msg_from {}|{}|{}: {}".format(sender_name, Receiver.HOST, sender_port, data))
                        elif "new_user_has_connected" in data:
                            print(data)
                        elif "exit" in data:
                            sys.exit(0)
                        time.sleep(random.randint(0, 5))
            except:
                sys.exit()

    def run(self):  # need to take constructor , so need also to call the constructor of the thread
        self.receive()
