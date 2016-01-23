#!/usr/bin/python2
# -*- coding : utf8 -*-
import select;
import socket;
import sys;

socket_l = socket.socket();
socket_l.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_l.bind((sys.argv[1], int(sys.argv[2])))

socket_l.listen(5)
connection_list = []
connection_list.append(socket_l)

while True:
    read_s, write_s, err_s = select.select(connection_list, [], [])
    for s in read_s:
        if s == socket_l:  # Nouveau client
            socket_c, address_c = socket_l.accept()
            socket_c.setblocking(0)
            connection_list.append(socket_c)
            socket_c.send("Bienvenue, vous etes sur mon serveur" + "\n")
            print("Eh oh, un nouveau client !")
        else:  # On traite le client existant
            message = s.recv(1024)
            if len(message) == 0:
                s.close()
                connection_list.remove(s)  # Pour ne pas retraiter au prochain coup !
                print("Client deconnecte !")
            else:
                s.send("J'ai recu votre message : " + message + "\n")
                print("Un client a parle !")
