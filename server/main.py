#! /usr/bin/env python
import asyncore
import socket
import config_parse
from help_parse import help_msg


class Commands():
    def exit(self):
        Server.clients.pop(self.nickname)
        self.close()
        self.disc_msg = "{} disconnected.".format(self.nickname)
        print(disc_msg)
        for x in Server.clients.values():
            x.send(disc_msg.encode('utf-8'))

    def help(self):
        self.send(help_msg().encode('utf-8'))

    def list_clients(self):
        for x in Server.clients.values():
            x.send(" ".join(Server.clients.keys).encode('utf-8'))


class Server(asyncore.dispatcher):
    port = config_parse.port
    name = config_parse.name
    clients = {}
    def accept(self):
        self.clients[nickname] = EchoHandler(sock)
        EchoHandler.nickname = nickname
        print("[i] {} connected from {}".format(nickname, addr[0]))

    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', self.port))
        self.listen(0)
        print("[+] Server listening on port {}.".format(self.port))

    def handle_accept(self):
        sock, addr = self.accept()
        sock.setblocking(True)
        sock.send(self.name.encode('utf-8'))
        nickname = sock.recv(16).decode('utf-8', errors='ignore')
        if nickname in self.clients:
            try:
                self.clients[nickname].send(" ".encode('utf-8'))

            except:
                self.accept()
            
            else:
                print(
                    "[!] {} nickname spoofing detected from {}".format(
                        nickname, addr))
                sock.send("Nickname is already in use.".encode('utf-8'))

        else:
            self.accept()


class EchoHandler(asyncore.dispatcher_with_send):
    nickname = str

    def handle_read(self):
        data = self.recv(1024).decode('utf-8', errors='ignore')
        if data.startswith("/"):
            if data.lower() == "/exit" or data.lower() == "/quit":
                Commands.exit(self)
                print("{} disconnected.".format(self.nickname))
            elif data.lower() == "/help":
                Commands.help(self)

            elif data.lower() == "/list":
                Commands.list_clients(self)
        else:
            print("{}~$ {}".format(self.nickname, data))
            for x in Server.clients.values():
                try:
                    if x != self:
                        x.send(data.encode('utf-8'))
                except BaseException:
                    Commands.exit()


s = Server()
asyncore.loop()
