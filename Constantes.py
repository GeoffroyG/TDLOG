# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 15:36:10 2015

@author: Fatma - Geoffroy - Pierre
"""

import pygame
pygame.init()

FPS           = 10 # frames per second, the general speed of the program

BOXSIZE       = 40 # size of box height & width in pixels
GAPSIZE       = 5 # size of gap between boxes in pixels

NBCOLUMN      = 30 # number of columns of icons in the map
NBROW         = 30 # number of rows of icons in the map
NBCOLUMN_DISP = 20 # number of columns displayed in the game windows
NBROW_DISP    = 10 # number of rows displayed in the game windows

GAMEWIDTH  = NBCOLUMN_DISP * (GAPSIZE + BOXSIZE) + GAPSIZE # size of game's width in pixels
GAMEHEIGHT = NBROW_DISP    * (GAPSIZE + BOXSIZE) + GAPSIZE # size of game's height in pixels

RESSOURCEBARWIDTH = GAMEWIDTH # size of the bar indicating the ressources
RESSOURCEBARHEIGHT = 60 # size of the bar indicating the ressources

MENUBARWIDTH = 180 # size of the bar indicating the menu
MENUBARHEIGHT = RESSOURCEBARHEIGHT + GAPSIZE + GAMEHEIGHT # size of the bar indicating the menu

WINDOWWIDTH  = MENUBARWIDTH + 3*GAPSIZE + GAMEWIDTH  # final size of the window in pixels
WINDOWHEIGHT = MENUBARHEIGHT + 2*GAPSIZE # final size of the window in pixels

pygame.font.init()

font_bubble = pygame.font.Font(None, 14)
font = pygame.font.Font(None, 24)
font_title = pygame.font.Font(None, 68)
font_other = pygame.font.Font(None, 40)

menuCoordinates = [(WINDOWWIDTH-GAPSIZE-MENUBARWIDTH,GAPSIZE),(WINDOWWIDTH-GAPSIZE-MENUBARWIDTH,WINDOWHEIGHT-GAPSIZE),(WINDOWWIDTH-GAPSIZE,WINDOWHEIGHT-GAPSIZE),(WINDOWWIDTH-GAPSIZE,GAPSIZE)]
headerCoordinates = [(GAPSIZE,GAPSIZE),(GAPSIZE,RESSOURCEBARHEIGHT),(GAPSIZE+RESSOURCEBARWIDTH,RESSOURCEBARHEIGHT),(GAPSIZE+RESSOURCEBARWIDTH,GAPSIZE)]
boardCoordinates = [(0,RESSOURCEBARHEIGHT),(0,WINDOWHEIGHT),(WINDOWWIDTH-GAPSIZE-MENUBARWIDTH,WINDOWHEIGHT),(WINDOWWIDTH-GAPSIZE-MENUBARWIDTH,RESSOURCEBARHEIGHT)]
# Initialisation of many variables that are useful later

MINES_DENSITY = 80
NBMINES = int(NBCOLUMN * NBROW / MINES_DENSITY)
BGCOLOR = (255, 255, 255) # white background
