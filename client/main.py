import asyncore
import socket
import threading

hostname = input("Server: ")
nickname = input("Nickname: ")

class Client(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.socket.setblocking(True)
        try:
            self.connect((hostname, 1337))
            self.send(nickname.encode('utf-8'))
        except Exception as e:
            print("Connection failed " + "Error: " + str(e))
        else:
            print("Connected successful")
        self.server_name = self.recv(64).decode('utf-8')

    def receiving(self):
        while 1:
            data = self.recv(1024)
            if data:
                print("\n" + data.decode('utf-8'))

    def sending(self):
        while 1:
            msg = input("{}@{}$ ".format(nickname, self.server_name))
            self.send(("{}@{}$ ".format(nickname, self.server_name) + msg).encode('utf-8'))

c = Client()
t1 = threading.Thread(target=c.receiving)
t2 = threading.Thread(target=c.sending)
t1.start()
t2.start()
asyncore.loop()
