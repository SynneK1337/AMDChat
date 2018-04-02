#! /usr/bin/env python
import asyncore
import socket
host = ''
port = 1337

class Server(asyncore.dispatcher):
    clients = []
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        print("[+] Server listening on port %s" % port)

    def handle_accept(self):
        sock, addr = self.accept()
        sock.setblocking(True)
        sock.send("Welcome!".encode('utf-8'))
        nickname = sock.recv(64)
        while not nickname:
            nickname = sock.recv(64)
        print("%s connected from %s" % (nickname.decode('utf-8'), addr[0]))
        self.clients.append((EchoHandler(sock), nickname))

class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(1024)
        if data:
            print(data)
            for x in Server.clients:
                try:
                    if x[0] != self:
                        x[0].send(data)
                except:
                    Server.clients.remove(x)
s = Server(host, port)
asyncore.loop()