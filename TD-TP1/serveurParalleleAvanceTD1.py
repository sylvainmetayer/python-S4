#!/usr/bin/python2
# -*- coding : utf8 -*-
import os
import socket
import subprocess
import sys


def agent(socket_c):
    socket_c.send("Bonjour !")
    print "Nouveau client !"

    while True:
        reponse = ""
        message = socket_c.recv(1024);
        if len(message) == 0:
            print("Le client est parti !")
            socket_c.close()
            sys.exit(0)
        print "Le client a demande " + message
        if message == "TIME\n":
            p = subprocess.Popen(['date'], stdout=subprocess.PIPE)
            reponse = p.communicate()[0]
        elif message == "SYS\n":
            p = subprocess.Popen(['cat', '/etc/issue'], stdout=subprocess.PIPE)
            reponse = p.communicate()[0]
        elif message == "DISK\n":
            p = subprocess.Popen(['df', '-h'], stdout=subprocess.PIPE)
            reponse = p.communicate()[0]
        elif message == "QUIT\n":
            reponse = "Au revoir\n"

        if reponse == "":
            reponse = "Commande inconnue"

        print reponse
        socket_c.send(reponse);


socket_l = socket.socket();
socket_l.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_l.bind((sys.argv[1], int(sys.argv[2])))

socket_l.listen(5)
print("Le serveur demarre")

while True:
    socket_c, address_c = socket_l.accept()

    pid = os.fork()
    if pid == 0:  # Nouvelle connexion
        socket_l.close()
        agent(socket_c)
        print "Tu ne passe pas la !"
        sys.exit(0)
    else:
        socket_c.close()
