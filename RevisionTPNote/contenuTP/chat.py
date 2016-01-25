#!/usr/bin/python2
# -*- coding: utf8

import os
import socket
import sys

socket_l = socket.socket()
socket_l.bind((sys.argv[1], int(sys.argv[2])))
socket_l.listen(5)


def agent(socket_c):
    socket_c.send("Votre username : ")
    user = socket_c.recv(1024)
    user = user.replace("\r", "").replace("\n", "")
    print user + " a rejoint la conversation !"

    socket_c.send("Votre nom: " + user + "\nMessage : \r\n")
    message = socket_c.recv(1024)
    while len(message) != 0:
        print "[" + user + "]: " + message
        socket_c.send("Votre message : " + message + "\r\n")
        message = socket_c.recv(1024)

    print user + " a quitte la conversation !"
    socket_c.close()
    sys.exit(0)


while True:
    socket_c, adresse_c = socket_l.accept()

    pid = os.fork()
    if pid == 0:
        socket_l.close()
        agent(socket_c)
        print "Oups !"
    else:
        socket_c.close()
