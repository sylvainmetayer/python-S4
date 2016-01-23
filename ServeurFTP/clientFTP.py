#!/usr/bin/python2
# -*- coding : utf8 -*-
import random
import socket
import sys


def getRandomPort():
    resultat = []
    resultat.append(random.randrange(5, 10))
    resultat.append(random.randrange(150, 500))
    return resultat


def getPortCalc(ports):
    port = int(ports[0]) * 256 + int(ports[1])
    return port


def writeFile(data, filename):
    if len(data) == 0:
        print "Aucune donnee a ecrire, ce fichier n'existe pas sur le serveur !"
    else:
        try:
            handle = open(filename + ".copy", "w+")
            handle.write(data)
            handle.close()
        except IOError:
            print "Une erreur est survenue lors de l'ecriture du fichier"


def menu(socketMenu):
    printMenu = "1- Afficher le repertoire courant (pwd)" + "\n2- Lister le contenu du repertoire courant (ls)" + "\n3- Recuperer un fichier" + "\n4- Quitter"
    nombreItems = printMenu.split("\n").__len__()
    print printMenu
    try:
        choix = input("Votre choix : ")
    except Exception:
        print "Erreur lors de la saisie, nous allons vous deconnecter.."
        traitementMenu(int(nombreItems), socketMenu)
    else:
        if choix not in range(1, nombreItems + 1):
            print "Option inconnue.."
            menu(socketMenu)
        else:
            traitementMenu(choix, socketMenu)


def traitementMenu(choix, socketClient):
    if int(choix) == 1:  # pwd
        socketClient.send("XPWD\r\n")

    elif int(choix) == 2:  # ls
        portRandom = getRandomPort()
        socketClient.send("PORT 127,0,0,1," + str(portRandom[0]) + "," + str(portRandom[1]) + "\r\n")
        portData = getPortCalc(portRandom)
        socketData = socket.socket()
        socketData.bind(("127.0.0.1", int(portData)))
        socketData.listen(2)
        messageServeur = socketClient.recv(1024)
        print messageServeur
        socketClient.send("LIST\r\n")
        messageServeur = socketClient.recv(1024)
        print messageServeur  # Je t'envoie des donnees
        socketTmp, addressTmp = socketData.accept()
        ls = socketTmp.recv(1024)
        print ls
        messageServeur = socketClient.recv(1024)  # Fin du transfert
        print messageServeur
        socketTmp.close()
        socketData.close()

        menu(socketClient)
    elif int(choix) == 3:
        """
        A fix
        """
        fichier = raw_input("Nom du fichier a recuperer : ")
        portRandom = getRandomPort()
        socketClient.send("PORT 127,0,0,1," + str(portRandom[0]) + "," + str(portRandom[1]) + "\r\n")
        portData = getPortCalc(portRandom)
        socketClient.send("RETR " + fichier)  # Je dis quel fichier recuperer sur le serveur

        socketData = socket.socket()
        socketData.bind(("127.0.0.1", int(portData)))
        socketData.listen(2)
        socketData, addressTmp = socketData.accept()
        print socketClient.recv(1024)  # Je t'envoie des donnees

        dataFile = ""
        tmp = socketData.recv(4096)  # Je recois les data
        while len(tmp) > 0:
            print "Passage dans la recuperation de data"
            dataFile += tmp
            tmp = socketData.recv(4096)  # Je recois les data
        socketData.shutdown(0)
        socketData.close()
        print socketClient.recv(2014)  # Fin du transfert
        writeFile(dataFile, fichier)

        menu(socketClient)

    elif int(choix) == 4:
        socketClient.send("QUIT\r\n")
    else:
        socketClient.send(str(choix) + "\r\n")  # On envoie le code du client, ce qui retournera une erreur 500


def main():
    if (len(sys.argv) != 3):
        print "Syntaxe <adresse> <port> "
        sys.exit(1)

    address = sys.argv[1]
    port = int(sys.argv[2])
    portClient = getPortCalc(getRandomPort())

    socketClient = socket.socket();
    socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socketClient.bind((address, int(portClient)))

    socketClient.connect((address, int(port)))  # On se connecte au serveur

    while True:
        dataFromServeur = socketClient.recv(1024)  # On recoit le message du serveur
        code = dataFromServeur.split(" ")[0]  # Contient le code retour.

        # Switch case like
        if int(code) == 220:  # Accueil + demande login
            message = dataFromServeur[4:]
            login = raw_input(message)
            socketClient.send("USER " + login + "\r\n")
        elif int(code) == 331:  # Ask pwd
            message = dataFromServeur[4:]
            pwd = raw_input(message)
            socketClient.send("PASS " + pwd + "\r\n")
        elif int(code) == 230:  # Login OK
            message = dataFromServeur[4:]
            print message
            socketClient.send("SYST\r\n")
        elif int(code) == 430:  # Login KO
            message = dataFromServeur[4:]
            print message
            login = raw_input("Votre nom d'utilisateur : ")
            socketClient.send("USER " + login + "\r\n")  # On repart sur une phase de login/pwd
        elif int(code) == 215:  # SYST
            message = dataFromServeur[4:]
            print message
            menu(socketClient)
        elif int(code) == 221:  # Bye
            message = dataFromServeur[4:]
            print message
            socketClient.shutdown(0)
            socketClient.close()
            print "Fermeture du client FTP en cours..."
            sys.exit(0)
        elif int(code) == 200:  # OK
            message = dataFromServeur[4:]
            print message
        elif int(code) == 257:  # Reponse pwd
            message = dataFromServeur[4:]
            print message
            menu(socketClient)
        elif int(code) == 500:  # Erreur
            message = dataFromServeur[4:]
            print message
            menu(socketClient)
        else:
            print "Erreur critique............"


main()
