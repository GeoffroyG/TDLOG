# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 15:36:10 2015

@author: Fatma - Geoffroy - Pierre
"""

import pygame
pygame.init()

FPS           = 30 # frames per second, the general speed of the program

BOXSIZE       = 40 # size of box height & width in pixels
GAPSIZE       = 1 # size of gap between boxes in pixels
GAPSIZE_MENU  = 5

NBCOLUMN      = 50 # number of columns of icons in the map
NBROW         = 45 # number of rows of icons in the map
NBCOLUMN_DISP = 20 # number of columns displayed in the game windows
NBROW_DISP    = 15 # number of rows displayed in the game windows

GAMEWIDTH  = NBCOLUMN_DISP * (GAPSIZE + BOXSIZE) + GAPSIZE # size of game's width in pixels
GAMEHEIGHT = NBROW_DISP    * (GAPSIZE + BOXSIZE) + GAPSIZE # size of game's height in pixels

RESSOURCEBARWIDTH = GAMEWIDTH # size of the bar indicating the ressources
RESSOURCEBARHEIGHT = 60 # size of the bar indicating the ressources

MENUBARWIDTH = 180 # size of the bar indicating the menu
MENUBARHEIGHT = RESSOURCEBARHEIGHT + GAPSIZE_MENU + GAMEHEIGHT # size of the bar indicating the menu

WINDOWWIDTH  = MENUBARWIDTH + 2*GAPSIZE_MENU + GAMEWIDTH + GAPSIZE # final size of the window in pixels
WINDOWHEIGHT = MENUBARHEIGHT + GAPSIZE + GAPSIZE_MENU # final size of the window in pixels

pygame.font.init()

font_bubble = pygame.font.Font(None, 14)
font = pygame.font.Font(None, 24)
font_title = pygame.font.Font(None, 68)
font_other = pygame.font.Font(None, 40)

menuCoordinates = [(WINDOWWIDTH-GAPSIZE-MENUBARWIDTH,GAPSIZE),(WINDOWWIDTH-GAPSIZE-MENUBARWIDTH,WINDOWHEIGHT-GAPSIZE),(WINDOWWIDTH-GAPSIZE,WINDOWHEIGHT-GAPSIZE),(WINDOWWIDTH-GAPSIZE,GAPSIZE)]
largerMenuCoordinates = [(WINDOWWIDTH-GAPSIZE-MENUBARWIDTH-GAPSIZE*2,GAPSIZE),(WINDOWWIDTH-GAPSIZE-MENUBARWIDTH-GAPSIZE*2,WINDOWHEIGHT-GAPSIZE),(WINDOWWIDTH,WINDOWHEIGHT-GAPSIZE),(WINDOWWIDTH,GAPSIZE)]
headerCoordinates = [(GAPSIZE,GAPSIZE),(GAPSIZE,RESSOURCEBARHEIGHT),(GAPSIZE+RESSOURCEBARWIDTH,RESSOURCEBARHEIGHT),(GAPSIZE+RESSOURCEBARWIDTH,GAPSIZE)]
boardCoordinates = [(0,RESSOURCEBARHEIGHT),(0,WINDOWHEIGHT),(WINDOWWIDTH-GAPSIZE-MENUBARWIDTH,WINDOWHEIGHT),(WINDOWWIDTH-GAPSIZE-MENUBARWIDTH,RESSOURCEBARHEIGHT)]
# Initialisation of many variables that are useful later

MINES_DENSITY = 80
NBMINES = int(NBCOLUMN * NBROW / MINES_DENSITY)

FORESTS_DENSITY = 80
NBFORESTS = int(NBCOLUMN * NBROW / FORESTS_DENSITY)

BGCOLOR = (255, 255, 255) # white background
PRODSTEP = 15 # Number of steps between two productions

HAPPINESSGAP = 15
HAPPINESSSTEP = 15

time_lost = 5 # Time (sec) you have to improve you inhabitants' happiness before you lose

TAXMAX = 10 # Maximum of tax you can impose
TAXMIN = 1 # Minimum of tax you can impose
TAXSTEP = 200 # Number of loops before tax is taken
DROPSTEP = 0.2 # Drop of percentage of happiness if nothing is done

HABITANTSLEVEL = 200 # Number of inhabitants you need to win the game
