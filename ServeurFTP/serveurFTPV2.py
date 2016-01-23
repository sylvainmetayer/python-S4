#!/usr/bin/python2
# -*- coding: utf8 -*-
import os
import socket
import subprocess
import sys


def agent(socket_c):
    """
    Fonction qui traite un client du début à la fin ce qui inclut la phase d'authentification, et la deconnexion du client.
    Les opérations supportées sont : pwd, ls, authentification, put, get.
    Cette fonction n'est pas censée se terminer. Si jamais cela arrive, elle doit être tuée par l'appelant.
    :rtype: object
    :param socket_c: La socket client
    :return: null
    """

    # TODO gérer user/pwd autrement (dictionnaire ?)
    user = "reseau"

    user_u = ""
    pwd_u = ""

    socket_data = ""
    fileToRename = ""
    portData = int(2020)  # Car 20 demmande root

    message = ""
    isConnected = False

    socket_c.send("220 Votre nom d'utilisateur : \r\n")
    while True:
        if verbose:
            print "------------------\n"  # Plus propre en console

        try:
            message = socket_c.recv(1024)
        except Exception:
            pass

        if len(message) == 0:  # Client KO
            socket_c.shutdown(0)
            socket_c.close()
            if verbose:
                print("Client deconnecte !")
            sys.exit(0)
        else:
            message = message.replace("\n", "").replace("\r", "")  # On clean la chaine
            commande = message[0:4]  # On isole la commande client

            if verbose:
                print "L'utilisateur est connecté" if isConnected else "L'utilisateur n'est pas connecté"
                print "Message recu : " + message
                print "Code = " + commande + "."

            if commande == "USER":
                user_u = message.split(" ")[1]
                socket_c.send("331 Votre mot de passe svp : \r\n")
                if verbose:
                    print "Je demande le mot de passe a l'utilisateur"

            elif commande == "PASS":
                pwd_u = message.split(" ")[1]
                if pwd_u == user and user_u == user:
                    socket_c.send("230 Login OK ! :) \r\n")
                    isConnected = True
                    if verbose:
                        print "Le login de l'utilisateur est correct"

                else:
                    if verbose:
                        print "Le login de l'utilisateur est incorrect"

                    socket_c.send("430 Login KO ! :( \r\n")

            elif isConnected and commande == "SYST":
                if verbose:
                    print "Je donne la version du systeme à l'utilisateur"

                socket_c.send("215 Debian 8 Jessie. \r\n")

            elif commande == "QUIT":
                if verbose:
                    print "Le client s'en va"
                socket_c.send("221 A bientot ! \r\n")
                sys.exit(0)  # Plus besoin de l'agent.

            elif isConnected and commande == "TYPE":
                if verbose:
                    print "Le client a demandé TYPE"

                socket_c.send("200 Resultat TYPE OK ! \r\n")

            elif isConnected and (commande == "XPWD" or commande in "PWD" or commande == "PWD"):
                if verbose:
                    print "Le client a demande le repertoire courant"

                pwd = subprocess.Popen(['pwd'], stdout=subprocess.PIPE)
                reponse = pwd.communicate()[0]
                socket_c.send("257 " + reponse + "\r\n")

            elif isConnected and commande == "PORT":
                if verbose:
                    print "Je recupere le port temporaire du client"

                ip = message.split(" ")[1]
                socket_data = socket.socket()
                socket_data.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                socket_data.bind((address, int(portData)))
                ip = ip.split(",")
                ipUser = ip[0] + "." + ip[1] + "." + ip[2] + "." + ip[3]
                portUser = int(ip[4]) * 256 + int(ip[5])
                socket_c.send("200 Tout va bien ! \r\n")

            elif isConnected and commande == "LIST":
                if verbose:
                    print "Je fais le ls et l'envoie au client"

                ls = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE)
                data = ls.communicate()[0]
                socket_c.send("150 Je t'envoie des donnees ! \r\n")
                socket_data.connect((ipUser, int(portUser)))
                socket_data.send(data)
                socket_data.shutdown(0)
                socket_data.close()
                socket_c.send("226 J'ai fini de t'envoyer des donnees ! \r\n")

            elif isConnected and commande == "RETR":
                if verbose:
                    print "J'envoie un fichier au client"

                askFor = message.split(" ")[1]
                cat = subprocess.Popen(['cat', askFor], stdout=subprocess.PIPE)
                data = cat.communicate()[0]
                socket_c.send("150 Je t'envoie des donnees ! \r\n")
                socket_data.connect((ipUser, int(portUser)))
                socket_data.send(data)
                socket_data.shutdown(0)
                socket_data.close()
                socket_c.send("226 J'ai fini de t'envoyer des donnees ! \r\n")

            elif isConnected and commande == "STOR":
                if verbose:
                    print "Je m'occupe de gerer l'upload d'un fichier"
                filename = message.split(" ")[1]
                socket_c.send("150 Je viens recuperer le fichier ! \r\n")
                socket_data.connect((ipUser, int(portUser)))
                data = socket_data.recv(8192)
                socket_data.shutdown(0)
                socket_data.close()
                try:
                    handle = open(filename, "w+")
                    handle.write(data)
                    handle.close()
                except IOError:
                    if verbose:
                        print "Une erreur est survenue lors de l'ecriture du fichier"
                socket_c.send("226 Transfert termine ! \r\n")

            else:
                if verbose:
                    print "Le code n'a pas ete reconnu"
                socket_c.send("500 Commande inconnue ! :( \r\n")


# End agent

def loop():
    """
    Cette fonction est la boucle infinie dans laquelle on traite les nouveaux clients et on les redirige vers agent()
    :return: null
    """
    while True:
        socket_c, address_c = socket_l.accept()

        pid = os.fork()
        if pid == 0:  # Nouvelle connexion
            if verbose:
                print("Une nouvelle connexion ! ")
            socket_l.close()
            agent(socket_c)
            if verbose:
                print("Quelque chose de mal est arrive, je tue l'agent !")
            sys.exit(0)
        else:
            socket_c.close()


# end loop

# Check arguments, déclaration variables & initialisation socket
if (len(sys.argv) != 4):
    print "Syntaxe <adresse> <port> <verbose> (o/?)"
    sys.exit(1)

address = sys.argv[1]
port = int(sys.argv[2])
verbose_s = sys.argv[3]
verbose = True if verbose_s == "o" else False

socket_l = socket.socket()
socket_l.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_l.bind((address, port))

socket_l.listen(5)

if verbose:
    print("Le serveur ftp demarre")

loop()
