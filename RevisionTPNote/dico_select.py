#!/usr/bin/python2
# -*- coding:utf-8 -*-

import select
import socket
import sys

dico = ['alpha', 'beta', 'gamma', 'epsilon']

if len(sys.argv) != 3:
    print "Syntaxe : " + sys.argv[0] + " <adresse> <port>"
    sys.exit(1)

socket_l = socket.socket()

adresse = sys.argv[1]
port = sys.argv[2]

socket_l.bind((adresse, int(port)))
socket_l.listen(5)

listeConnections = []
listeConnections.append(socket_l)

print "En attente d'un client.."
while True:
    read_s, write_s, err_s = select.select(listeConnections, [], [])
    for s in listeConnections:
        if s in read_s:  # Nouveau client
            socket_c, adresse_c = socket_l.accept()
            listeConnections.append(socket_c)
            print "Client connecte !"
        else:
            message = s.recv(1024)
            if len(message) == 0:
                s.close()
                print "Client deconnecte"
                listeConnections.remove(s)
            else:
                if message in dico:
                    s.send("Mot trouve ! \r\n")
                else:
                    s.send("Mot inconnu ! \r\n")
