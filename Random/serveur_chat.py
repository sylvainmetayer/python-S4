#!/usr/bin/python2
# -*- coding: utf8 -*-

import select
import socket
import sys


def sendToAll(current, socket_list, message):
    """
    Cette fonction permet d'envoyer un message à toute une liste de client, en évitant d'envoyer ce message à l'utilisateur actuel.
    :param current: Utilisateur actuel
    :param socket_list: liste de client
    :param message: Le message à envoyer
    :return: ""
    """
    for user in socket_list:
        if user == current:
            pass
        else:
            user.send(message + '\n')


if len(sys.argv) != 3:
    print "Syntaxe " + sys.argv[0] + " <adresse> <port>"
    sys.exit(1)

adresse = sys.argv[1]
port = sys.argv[2]

socket_l = socket.socket();
socket_l.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_l.bind((adresse, int(port)))

socket_l.listen(5)
socket_list = []
client_list = []
socket_list.append(socket_l)

while True:
    read_s, write_s, err_s = select.select(socket_list, [], [])
    for s in read_s:
        if s == socket_l:  # Nouveau client
            socket_c, address_c = socket_l.accept()
            socket_c.setblocking(0)
            socket_list.append(socket_c)
            client_list.append(socket_c)
            socket_c.send("Bienvenue sur le serveur de chat :" + "\n")
            sendToAll(socket_c, client_list, "Un client vient de se connecter !\n")
        else:
            message = s.recv(1024)
            message = message.replace("\n", "").replace("\r", "")
            if len(message) == 0:
                s.close()
                socket_list.remove(s)
                client_list.remove(s)
                sendToAll("", client_list, "Un client s'est deconnecte !\n")
            else:
                sendToAll(s, client_list, message)
