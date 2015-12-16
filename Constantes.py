# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 15:36:10 2015

@author: Fatma - Geoffroy - Pierre 
"""

import pygame

FPS = 30 # frames per second, the general speed of the program
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 5 # size of gap between boxes in pixels
BOARDWIDTH = 10 # number of columns of icons
BOARDHEIGHT = 10 # number of rows of icons
GAMEWIDTH = BOARDWIDTH * (GAPSIZE + BOXSIZE) + GAPSIZE # size of game's width in pixels
GAMEHEIGHT = BOARDHEIGHT * (GAPSIZE + BOXSIZE) + GAPSIZE # size of game' height in pixels
RESSOURCEBARWIDTH = GAMEWIDTH # size of the bar indicating the ressources
RESSOURCEBARHEIGHT = 60 # size of the bar indicating the ressources
MENUBARWIDTH = 180 # size of the bar indicating the menu
MENUBARHEIGHT = RESSOURCEBARHEIGHT + GAPSIZE + GAMEHEIGHT # size of the bar indicating the menu
WINDOWWIDTH = MENUBARWIDTH + 3*GAPSIZE + GAMEWIDTH  # final size of the window in pixels
WINDOWHEIGHT = MENUBARHEIGHT + 2*GAPSIZE # final size of the window in pixels

Graphism = ["2.Images/Road.png", "2.Images/House.png", "2.Images/Factory.png", "2.Images/None.png", "2.Images/None.png", "2.Images/None.png", "2.Images/None.png", "2.Images/None.png", "2.Images/None.png", "2.Images/Grass.png"]
Graphism_Selected = ["2.Images/Road_Selected.png", "2.Images/House_Selected.png", "2.Images/Factory_Selected.png", "2.Images/None.png", "2.Images/None.png", "2.Images/None.png", "2.Images/None.png", "2.Images/None.png", "2.Images/None.png", "2.Images/Grass_Selected.png"]

pygame.font.init()

font = pygame.font.Font(None, 24)
font_title = pygame.font.Font(None, 68)
font_other = pygame.font.Font(None, 40)

MenuCoordinates = [(WINDOWWIDTH-GAPSIZE-MENUBARWIDTH,GAPSIZE),(WINDOWWIDTH-GAPSIZE-MENUBARWIDTH,WINDOWHEIGHT-GAPSIZE),(WINDOWWIDTH-GAPSIZE,WINDOWHEIGHT-GAPSIZE),(WINDOWWIDTH-GAPSIZE,GAPSIZE)]
# Initialisation of many variables that are useful later