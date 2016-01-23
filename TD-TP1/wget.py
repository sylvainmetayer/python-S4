#!/usr/bin/python2
# -*- coding: utf8 -*-
import socket;
import sys;

maSocket = socket.socket();


def getMessageSize(header):
    # On recupère la longueur du header
    tab = header.split("\r\n\n")
    # print(tab[0])

    numDebut = tab[0].find("Content-Length:")
    numFin = tab[0].find("Vary")
    headerSpecialLigne = tab[0][numDebut:numFin];  # On récupère la ligne Content Lenght : xxx

    try:
        longueurMessage = headerSpecialLigne.split(":")[1].split(" ")[1]
        print("Longueur du header : " + longueurMessage)
        # On récupère la longueur du message
    except IndexError:
        print("Erreur lors du calcul. TODO")

    "A RETENIR : numDebut:numFin : on recupere de numDebut a numFin exclus"


if len(sys.argv) != 4:
    print "Syntaxe : wget.py <adresse> <port> <demande>"
    sys.exit(1)

adresse = sys.argv[1];
port = int(sys.argv[2])
demande = sys.argv[3]

message = "GET " + demande + " HTTP/1.0\nHost:" + adresse + "\n\r\n"

maSocket.connect((adresse, port));  # NB : Sous forme de tuple !
maSocket.send(message);

texte = ""
chaine = maSocket.recv(1024);

while len(chaine) == 1024:
    print(chaine);
    texte += chaine
    chaine = maSocket.recv(1024);

getMessageSize(texte)
maSocket.shutdown(0);
maSocket.close();
