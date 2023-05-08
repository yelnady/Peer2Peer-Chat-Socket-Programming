import socket,time,os
from _thread import *

from repository import *

class DRDC:
    # Class-level constants and variables
    HOST = '127.0.0.1' # the local IP address of the host
    PORT = 65432 # the port number for communication
    users = [] # a list to store User objects
    DS = DataStore() # an instance of DataStore class
    conn = None # a variable to hold the connection object
    name = "DRDC" # a string to hold the name of the DRDC
    
    @staticmethod # A static method to print the list of users
    def print_users():
        for i, user in enumerate(DRDC.users):
            print("User{} : {}|{}|{}".format(i, user.name, user.host, user.port))
     
    @staticmethod # A static method to delete a user from the list of users
    def delUser(port):
        for user in DRDC.users:
            if str(user.port) == str(port):
                print("User {}|{}|{} has been terminated".format(user.name, user.host, user.port))
                DRDC.users.remove(user)
        DRDC.print_users()


    # Each message we want to send comes to the broadcast message first, then it decides what option should be taken on this message
    # Either first time joining, so it's connect_request to (notify a new user), OR 
    @staticmethod 
    def broadcast(conn): 
        while 1:
            # The 1024 parameter specifies the maximum amount of data that can be received at once.
            # In this case, the server will receive up to 1024 bytes of data at a time. 
            # If there is more data to be received, it will need to be done in subsequent calls to recv().
            data = conn.recv(1024).decode()
            # The data consists always of "command|param1|param2|...|paramN"

            # func: tell_others()
            if "connect_request" in data:
                print("connect request received")
                arr = data.split("|")
                if len(arr) == 4:  # ignoring the first one cuz it's the command
                    user_name = arr[1];
                    user_host = arr[2];
                    user_port = arr[3];
                    print(data)  # connect_request From User: |joe|127.0.0.1|123
                    for u in DRDC.users:
                        port = int(u.port);
                        name = u.name;
                        # if name of current user not same as one comes from, and my port not the DRDC
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as temp:
                            temp.connect((DRDC.HOST, port))
                            temp.send(
                                "New_user_has_connected : {}|{}|{}| ".format(user_name, user_host, user_port).encode())
                    DRDC.users.append(User(user_name, user_host, user_port))
                    DRDC.print_users()
                    
            # func: exit()
            elif "delete" in data:
                data = data.split('|')
                DRDC.delUser(data[1])
            # func: send_msg()
            elif "Receive_From" in data:  # if any one sends a msg in general , this one should know that there's a msg has been received
                DRDC.DS.add_to_queue(data)
            # func: send_msg()
            elif "request_queue" in data:
                data = data.split('|')
                current_port = int(data[1])
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as temp:
                    temp.connect((DRDC.HOST, 1))
                    msg = str(DRDC.DS.get_queue_length())
                    temp.send(msg.encode())

    @staticmethod
    def synchronize():
        # move from repo to file
        # copy this file as many names as other peers
        # copy from queue to repo
        time.sleep(20)

        while 1:
            print("Time to synchronize")
            print("queue is " + str(DRDC.DS.get_queue()))
            print("Datastore is " + str(DRDC.DS.get_data_store()))
            datastore = DRDC.DS.get_data_store()
            queue = DRDC.DS.get_queue()
            if datastore:
                with open(DRDC.name + "_DS.txt", "ab") as f:
                    for msg in datastore:
                        msg += '\n'
                        f.write(msg.encode())
                    DRDC.DS.free_the_datastore()
            for u in DRDC.users:
                os.popen('copy DRDC_DS.txt ' + u.name + "_DS.txt")
            if queue:
                for msg in queue:
                    DRDC.DS.add_to_datastore(msg)
                DRDC.DS.free_the_queue()
            time.sleep(15)

    @staticmethod
    def start():
        print("Welcome to The Decentralized Replicated Data Store")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((DRDC.HOST, DRDC.PORT))
            s.listen(15)
            start_new_thread(DRDC.synchronize, ())  # you can accept from anyone at any time

            while 1:
                conn, addr = s.accept()
                start_new_thread(DRDC.broadcast, (conn,))  # you can accept from anyone at any time





# The if __name__ == '__main__' block is used to ensure that the code inside it is only executed if the module is run as the main program, rather than being imported as a module into another program. 
# This is a common practice in Python, as it allows you to write code that can be both used as a module and run as a standalone program.
if __name__ == '__main__':
    DRDC.start()