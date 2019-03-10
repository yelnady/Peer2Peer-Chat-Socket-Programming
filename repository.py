class DataStore:
    def __init__(self):
        self.queue = []
        self.repo = []
        self.old = open("DRDC_DS.txt", "w+")
        self.repo_len = 2
    def add_to_queue(self, msg):
        self.queue.append(msg)

    def add_to_datastore(self, msg):
        self.repo.append(msg)

    def get_queue_length(self):
        return len(self.queue)

    def free_the_datastore(self):
        self.repo = []

    def free_the_queue(self):
        self.queue = []

    def get_data_store(self):
        return self.repo

    def get_queue(self):
        return self.queue


class User:
    def __init__(self, name, host, port):
        self.name = name;
        self.host = host;
        self.port = int(port)
