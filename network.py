import socket


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #for this to work on global conection need to put my public ip address google search: hat is my public ip adress
        self.host = "192.168.1.3" # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
                                    # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
                                    # ipv4 address. This feild will be the same for all your clients.
        # public ip 5.55.39.88 188.4.37.46
        self.port = 5555
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        print("Conected!")
        return self.client.recv(1024).decode()

    def send_config(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(33554432).decode()
            return reply
        except socket.error as e:
            return str(e)
    
    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(1024).decode()
            return reply
        except socket.error as e:
            return str(e)
