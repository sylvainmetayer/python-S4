#!/usr/bin/python2
# -r -coding : utf8
import socket;
import sys;

maSocket = socket.socket();

adresse = sys.argv[1];
port = int(sys.argv[2]);


def menu():
    print("1- Heure")
    print("2- Version OS")
    print("3- Espace Disque")
    print("4- Quitter")


maSocket.connect((adresse, port));
chaine = maSocket.recv(1024);
print(chaine);
texte = 0

while texte != 4:
    noSend = False
    menu()
    texte = input("Votre choix :");
    if (texte == 1):
        maSocket.send("TIME\n");
    elif (texte == 2):
        maSocket.send("SYS\n");
    elif (texte == 3):
        maSocket.send("DISK\n");
    elif (texte == 4):
        maSocket.send("QUIT\n");
        print("Le serveur s'est arrete")
    else:
        print("Erreur de saisie.");
        noSend = True;

    if noSend == False:
        chaine = maSocket.recv(1024);
        print(chaine);

maSocket.shutdown(0);
maSocket.close();
