#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Very simple game with Pygame
"""

import os
import pygame
import random
import sys
from pygame.locals import *

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768


# FUNCTIONS
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


# CLASSES
class Ship(pygame.sprite.Sprite):
    """Class for the player's ship"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('Pics/ship.png')
        self.rect.center = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
        self.speed = [3, 3]
        self.pas = 10

    def up(self):
        if self.rect.top <= 0:
            self.rect = self.rect.move([0, 0])
        else:
            self.rect = self.rect.move([0, -self.pas])

    def down(self):
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect = self.rect.move([0, 0])
        else:
            self.rect = self.rect.move([0, self.pas])
            # self.speed[1] += 1

    def left(self):
        if self.rect.left <= 0:
            self.rect = self.rect.move([0, 0])
        else:
            self.rect = self.rect.move([-self.pas, 0])
            # self.speed[0] -= 1

    def right(self):
        if self.rect.right >= SCREEN_WIDTH:
            self.rect = self.rect.move([0, 0])
        else:
            self.rect = self.rect.move([self.pas, 0])
            # self.speed[0] += 1

    def update(self):
        if self.speed[0] >= 5 or self.speed[0] >= -5:
            self.speed[0] = 0
        if self.speed[1] >= 5 or self.speed[1] >= -5:
            self.speed[1] = 0
        self.rect = self.rect.move(self.speed)


class Tir(pygame.sprite.Sprite):
    """
    Classe de tir du vaisseau
    """

    def __init__(self, ship):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('Pics/shot.png')
        self.speed = [0, -1]
        self.rect.center = ship.rect.center

    def update(self):
        self.rect = self.rect.move([0, -10])
        if self.rect.top <= -20:
            self.kill()


class Ennemi(pygame.sprite.Sprite):
    """
    Classe d'ennemi
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('Pics/ship_red.png')
        self.speed = [0, -1]
        self.rect.center = [random.randint(0, SCREEN_HEIGHT), 0]

    def update(self):
        self.rect = self.rect.move([0, 5])
        if self.rect.bottom >= SCREEN_HEIGHT + 10:
            print "Game Over"
            #sys.exit(0)
            self.kill()



# MAIN

def main_function():
    """Main function of the game"""
    # Initialization
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 1)

    # Objects creation
    background_image, background_rect = load_png('Pics/background.jpg')
    ship = Ship()  # creation d'une instance de Ship
    ship_sprite = pygame.sprite.RenderClear()  # creation d'un groupe de sprite
    ship_sprite.add(ship)  # ajout du sprite au groupe de sprites

    # Gestion des tirs
    tir_sprite = pygame.sprite.RenderClear()
    shotAllowed = True
    compteurTir = 15
    tmp = 1

    # Gestion des ennemis
    goEnnemi = True
    timeEnnemi = 50
    tmpEnnemi = 1

    # Gestion des ennemis
    mechant_sprite = pygame.sprite.RenderClear()

    # MAIN LOOP
    while True:
        clock.tick(60)  # max speed is 60 frames per second

        # Events handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # closing the window exits the program

        touches = pygame.key.get_pressed()
        if (touches[K_UP]):
            ship.up()
        if (touches[K_q]):
            return  # exit the program
        if touches[K_DOWN]:
            ship.down()
        if touches[K_RIGHT]:
            ship.right()
        if touches[K_LEFT]:
            ship.left()
        if touches[K_SPACE]:
            if shotAllowed:
                shotAllowed = False
                tmp = compteurTir
                tir = Tir(ship)
                tir_sprite.add(tir)

        # updates
        ship_sprite.update()
        tir_sprite.update()
        mechant_sprite.update()

        if goEnnemi:
            goEnnemi = False
            tmpEnnemi = timeEnnemi
            bad_guy = Ennemi()
            mechant_sprite.add(bad_guy)

        tmpEnnemi = tmpEnnemi - 1
        if tmpEnnemi < 0:
            goEnnemi = True

        test = pygame.sprite.groupcollide(mechant_sprite, tir_sprite, True, True,
                                          pygame.sprite.collide_circle_ratio(0.7))
        print str(test)

        # Gestion tir
        tmp = tmp - 1
        if tmp <= 0:
            shotAllowed = True

        # drawings
        screen.blit(background_image, background_rect)
        ship_sprite.draw(screen)
        tir_sprite.draw(screen)
        mechant_sprite.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main_function()
    sys.exit(0)
