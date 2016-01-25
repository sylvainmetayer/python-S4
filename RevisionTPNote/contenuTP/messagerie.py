#!/usr/bin/python2
# -*- coding: utf8 -*-

import socket
import sys

socket_l = socket.socket()
socket_l.bind((sys.argv[1], int(sys.argv[2])))
socket_l.listen(5)

socket_c, adress = socket_l.accept()
socket_l.close()

socket_c.send("Expediteur (EXP): \r\n")
expediteur = socket_c.recv(1024)
expediteur = expediteur.replace("\r", "").replace("\n", "")

socket_c.send("Destinataire (DST): \r\n")
destinataire = socket_c.recv(1024)
destinataire = destinataire.replace("\r", "").replace("\n", "")

socket_c.send("Mail (MAIL et se termine par \\n.):\r\n")

message = socket_c.recv(1024)
while (message.find("\n.") == -1):
    message += socket_c.recv(1024)

socket_c.shutdown(0)
socket_c.close()
print expediteur
print destinataire
print message
