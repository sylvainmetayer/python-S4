#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import pygame
import sys
from pygame.locals import *

from PodSixNet.Connection import connection, ConnectionListener

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768


def load_png(name):
    """Load image and return image object"""
    fullname = os.path.join('.', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    return image, image.get_rect()


class Ship(pygame.sprite.Sprite, ConnectionListener):
    """
    Classe représentant le vaisseau côté client.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('Pics/ship.png')
        self.rect.center = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
        self.speed = [3, 3]
        self.pas = 10

    def Network_ship(self, data):
        self.rect.center = data['center']

    def update(self):
        self.Pump()


class Tir(pygame.sprite.Sprite):
    """
    Classe de tir du vaisseau côté client.
    """

    def __init__(self, ship):
        self.image, self.rect = load_png('Pics/shot.png')
        self.speed = [0, -1]
        self.rect.center = ship.rect.center

    def update(self):
        self.Pump()

    def Network_shot(self, data):
        if data['isAlive'] == True:
            self.rect.center = data['center']
        else:
            self.kill()


class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
        self.game_client = False

    def Loop(self):
        connection.Pump()
        self.Pump()

    def Network(self, data):
        print('message de type %s recu' % data['action'])

    ### Network event/message callbacks ###
    def Network_connected(self, data):
        print('connecte au serveur !')

    def Network_connexion_ok(self, data):
        print data["message"]

    def Network_error(self, data):
        print 'error:', data['error'][1]
        connection.Close()

    def Network_disconnected(self, data):
        print 'Server disconnected'
        sys.exit()


class MyShotSprite(pygame.sprite.RenderClear, ConnectionListener):
    def __init__(self):
        pygame.sprite.RenderClear.__init__()
        self.tirs = pygame.sprite.RenderClear()

    def Network_shot_update(self, data):
        for shot in self.tirs:
            shot.update()

    def Network_shot_add(self, data):
        tir = Tir()
        tir.rect.center = data["center"]
        self.tirs.add(tir)

    def Network_shot_remove(self, data):
        self.tirs.remove(data["tir"])

    def Network_shot_update(self, data):
        pass

    def update(self):
        for shot in self.tirs:
            shot.update()


if len(sys.argv) != 3:
    print "Usage:", sys.argv[0], "host port"
else:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    client = Client(sys.argv[1], int(sys.argv[2]))
    ship = Ship()
    pygame.init()
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 1)

    # Objects creation
    background_image, background_rect = load_png('Pics/background.jpg')
    ship = Ship()  # creation d'une instance de Ship
    ship_sprite = pygame.sprite.RenderClear()  # creation d'un groupe de sprite
    ship_sprite.add(ship)  # ajout du sprite au groupe de sprites

    while True:
        clock.tick(60)  # max speed is 60 frames per second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        touches = pygame.key.get_pressed()
        client.Send({"action": "keys", "keys": touches})
        client.Loop()
        ship.update()

        screen.blit(background_image, background_rect)
        ship_sprite.draw(screen)
        pygame.display.flip()
