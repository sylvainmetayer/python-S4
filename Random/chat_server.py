#!/usr/bin/python2
# -*- coding: utf8 -*-

import select
import socket
import sys


# TODO refactor + baser user sur le port de connexion et non la socket (split a faire sur le address_c)

def getCoffee():
    coffee = '\n              {               \n'
    coffee += '          }   }   {             \n'
    coffee += '          {   {  }  }           \n'
    coffee += '           }   }{  {            \n'
    coffee += '         _{  }{  }  }_          \n'
    coffee += '        (  }{  }{  {  )         \n'
    coffee += '        |""---------""|         \n'
    coffee += '        |             /""\      \n'
    coffee += '        |            | _  |     \n'
    coffee += '        |             / | |     \n'
    coffee += '       |             |/  |      \n'
    coffee += '       |             /  /       \n'
    coffee += '        |            |  /       \n'
    coffee += '        |            "T"        \n'
    coffee += '        ""---------""           \n'
    return coffee


def getUsername(dictionnaire, client_list, socket_c):
    """
    Cette fonction retourne le nom d'utilisateur d'une socket.
    :param dictionnaire:
    :param client_list:
    :param socket_c:
    :return:
    """
    retour = ""
    for key, value in dictionnaire.iteritems():
        if key == socket_c:
            retour = value
    if retour == "":
        retour = "Anoynme"
    return retour


def sendToAll(current, socket_list, message, asAdmin=False):
    """
    Cette fonction permet d'envoyer un message à toute une liste de client, sans prendre en compte le client actuel
    :param current: Utilisateur actuel
    :param socket_list: liste de client
    :param message: Le message à envoyer
    :return: ""
    """
    for user in socket_list:
        if user == current:
            pass
        else:
            utilisateur = getUsername(username, client_list, current)
            if asAdmin:
                user.send("******** " + message + " ********\r\n")
            else:
                user.send(utilisateur + ": " + message + '\n')


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

username = {}

while True:
    read_s, write_s, err_s = select.select(socket_list, [], [])
    for s in read_s:
        if s == socket_l:  # Nouveau client
            socket_c, address_c = socket_l.accept()
            socket_c.setblocking(0)
            print address_c
            socket_list.append(socket_c)
            client_list.append(socket_c)
            socket_c.send(
                "Bienvenue sur mon serveur de chat :\n'USER <username>' pour définir/modifier votre nom d'utilisateur" + "\n")
        else:
            message = s.recv(1024)
            message = message.replace("\n", "").replace("\r", "")
            if len(message) == 0:
                s.send("Au revoir.\r\n")
                user = username.get(s)
                try:
                    s.close()
                    username.__delitem__(s)
                except Exception:
                    pass
                socket_list.remove(s)
                client_list.remove(s)
                sendToAll("", client_list, user + " s'est deconnecté !", True)
            else:
                code = message.split(" ")[0]
                if code == "USER":
                    user = message.split(" ")[1]
                    if username.values().__contains__(user):
                        s.send("Désolé, ce pseudo est déjà pris !\r\n")
                    else:
                        if username.has_key(s):
                            sendToAll(s, client_list, username[s] + " a changé son pseudo en " + str(user))
                        username[s] = user
                        s.send("Votre pseudo est " + user + "\r\n")
                        sendToAll(s, client_list, username[s] + " a rejoint le chat", True)
                elif code == "COFFEE":
                    if username.has_key(s):
                        sendToAll(s, client_list, "Café de " + username[s] + getCoffee(), True)
                    else:
                        s.send("Vous devez d'abord définir votre nom d'utilisateur !\r\n")
                elif code == "HOW":
                    s.send("Il y a " + str(len(username)) + " utilisateur(s) actif(s) sur le chat.\r\n")
                else:
                    if username.has_key(s):
                        sendToAll(s, client_list, message)
                    else:
                        s.send("Vous devez d'abord définir votre nom d'utilisateur !\r\n")
