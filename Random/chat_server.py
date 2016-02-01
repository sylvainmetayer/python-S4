#!/usr/bin/python2
# -*- coding: utf8 -*-

import select
import socket
import sys


# TODO refactor

def getAllUsername():
    message = "Liste des utilisateurs : "
    for user in username:
        message += get_username(username, user) + ", "
    return message;


def get_username(dictionnaire, client):
    """
    Cette fonction retourne le nom d'utilisateur d'une socket.
    :param dictionnaire:
    :param client:
    :return:
    """
    retour = ""
    for key, value in dictionnaire.iteritems():
        if key == client:
            retour = value
    if retour == "":
        retour = "Anoynme"
    return retour

def send_to_all(current, socket_list, message, asAdmin=False):
    """
    Cette fonction permet d'envoyer un message à toute une liste de client, sans prendre en compte le client actuel
    :rtype: object
    :param current: Utilisateur actuel
    :param socket_list: liste de client
    :param message: Le message à envoyer
    :return: None
    """
    for user_tmp in socket_list:
        if user_tmp == current:
            pass
        else:
            utilisateur = get_username(username, current)
            if asAdmin:
                if user_tmp == sys.stdout:
                    print "******** " + message + " ********\r\n"
                else:
                    user_tmp.send("******** " + message + " ********\r\n")
            else:
                if user_tmp == sys.stdout:
                    print utilisateur + ": " + message + '\n'
                else:
                    user_tmp.send(utilisateur + ": " + message + '\n')


if len(sys.argv) != 3:
    print "Syntaxe " + sys.argv[0] + " <adresse> <port>"
    sys.exit(1)

adresse = sys.argv[1]
port = sys.argv[2]

socket_l = socket.socket()
socket_l.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_l.bind((adresse, int(port)))

socket_l.listen(5)
socket_list = []
client_list = []
socket_list.append(socket_l)
socket_list.append(sys.stdin)
client_list.append(sys.stdout)  # la console

username = {}

while True:
    read_s, write_s, err_s = select.select(socket_list, [], [])
    for s in read_s:
        if s == socket_l:  # Nouveau client
            socket_c, address_c = socket_l.accept()
            socket_c.setblocking(0)
            # print address_c
            socket_list.append(socket_c)
            client_list.append(socket_c)
            message = "331 Votre nom d'utilisateur :\n"
            socket_c.send(message)
        elif s == sys.stdin:
            message = sys.stdin.readline()
            message = message.replace("\n", "").replace("\r", "")

            code = message.split(" ")[0]
            if code == "QUIT":
                send_to_all(sys.stdout, client_list, "Arrêt du serveur.", True)
                sys.exit(0)
            else:
                send_to_all(sys.stdout, client_list, "Message du serveur : " + message, True)
        else:
            message = s.recv(1024)
            message = message.replace("\n", "").replace("\r", "")
            if len(message) == 0:
                s.send("221 Au revoir.\r\n")
                user = username.get(s)
                try:
                    s.close()
                    username.__delitem__(s)
                except Exception:
                    pass
                socket_list.remove(s)
                if client_list.__contains__(s):
                    client_list.remove(s)
                    send_to_all("", client_list, user + " s'est deconnecté !", True)
                    #Sinon, pas la peine d'envoyer un message, l'utilisateur n'était pas connecté..
            else:
                code = message.split(" ")[0]
                if code == "USER":
                    user = message[4:]
                    if username.values().__contains__(user):
                        s.send("403 Désolé, ce pseudo est déjà pris !\r\n")
                    else:
                        if username.has_key(s):
                            send_to_all("", client_list, username[s] + " a changé son pseudo en " + str(user))
                            username[s] = user
                        else:
                            username[s] = user
                            send_to_all("", client_list, getAllUsername(), True)
                elif code == "HOW":
                    s.send("Il y a " + str(len(username)) + " utilisateur(s) actif(s) sur le chat.\r\n")
                elif code == "QUIT":
                    s.send("221 Au revoir.\r\n")
                    user = username.get(s)
                    try:
                        s.close()
                        username.__delitem__(s)
                    except Exception:
                        pass
                    socket_list.remove(s)
                    client_list.remove(s)
                    send_to_all("", client_list, user + " s'est deconnecté !", True)
                else:
                    if username.has_key(s):
                        send_to_all(s, client_list, message)
                        s.send("Votre message : \n")
                    else:
                        s.send("Vous devez d'abord définir votre nom d'utilisateur !\r\n")