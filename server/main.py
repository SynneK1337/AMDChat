#! /usr/bin/env python
import asyncore
import socket
host = 'localhost'
port = 1337
server_name = "AMDChat"

class Server(asyncore.dispatcher):
    clients = []
    nicknames = []

    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        print("[+] Server listening on port %s" % port)

    def handle_accept(self):
        sock, addr = self.accept()
        sock.setblocking(True)
        sock.send(server_name.encode('utf-8'))
        nickname = sock.recv(64)
        while not nickname:
            nickname = sock.recv(64)
        if nickname in self.nicknames:
            print("[!] %s nickname spoofing detected from %s" %
                  (nickname.decode('utf-8'), addr[0]))
            sock.send("Nickname is used already".encode('utf-8'))

        else:
            self.nicknames.append(nickname)
            self.clients.append(EchoHandler(sock))
            print("[i] %s connected from %s" % (nickname.decode('utf-8'), addr[0]))


class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(1024)
        if data:
            print(data.decode('utf-8'))
            for x in Server.clients:
                try:
                    if x != self:
                        x.send(data)
                except Exception as e:
                    print("Server Closing. " + "Error: " + str(e))
                    Server.clients.remove(x)


s = Server()
asyncore.loop()
