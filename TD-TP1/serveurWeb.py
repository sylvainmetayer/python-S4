#!/usr/bin/python2
# -*- coding : utf8 -*-
import os
import socket
import sys


def agent(socket_c):
    reponse = ""
    message = socket_c.recv(1024);

    if message[0:4] != "GET ":
        print("La demande n'est pas au format GET")
        print message
        socket_c.send("Merci de communiquer via GET")
        socket_c.close()
        sys.exit(1)

    finHeader = "\r\n\r\n"

    header = "HTTP/1.0 200 OK\r\nContent-type: text/html\r\n"
    headerErreur = "HTTP/1.0 400 KO\r\nContent-type: text/html\r\n"

    sizeContent = "Content-length: "

    tab = message.split("HTTP")
    resu = tab[0].split(" ")
    demande = resu[1]
    demande = "." + demande  # Current directory

    try:
        f = open(demande, 'r')
    except IOError:
        if verbose:
            print "Fichier inconnu, envoi de la page d'erreur"
        f = open("./site/404.html")
        content = f.read()
        size = content.__sizeof__()
        sizeContent = sizeContent + str(size) + "\r\n"
        response = headerErreur + sizeContent + finHeader + content
    else:
        content = f.read()
        size = content.__sizeof__()
        sizeContent = sizeContent + str(size) + "\r\n"
        response = header + sizeContent + finHeader + content
    finally:
        f.close()

    if verbose:
        print "Reponse envoyee au client, fermeture de la connexion"
    # print response
    socket_c.send(response)


# End agent


def main():
    socket_c, address_c = socket_l.accept()

    pid = os.fork()
    if pid == 0:  # Nouvelle connexion
        if verbose:
            print "Un agent demarre"
        socket_l.close()
        agent(socket_c)
        if verbose:
            print "Un agent se termine"
        sys.exit(0)
    else:
        socket_c.close()


# end main


if (len(sys.argv) != 4):
    print "Syntaxe <adresse> <port> <verbose (o/n)>"
    sys.exit(1)

address = sys.argv[1]
port = int(sys.argv[2])
verbose_s = sys.argv[3]
verbose = True if verbose_s == "o" else False

socket_l = socket.socket();
socket_l.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_l.bind((address, port))

socket_l.listen(5)

if verbose:
    print("Le serveur web demarre")

while True:
    main()
