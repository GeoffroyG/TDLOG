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

TITLE = "French City Simulator"

# Map width and height in pixels
GAMEWIDTH  = NBCOLUMN_DISP * (GAPSIZE + BOXSIZE) + GAPSIZE 
GAMEHEIGHT = NBROW_DISP    * (GAPSIZE + BOXSIZE) + GAPSIZE 

# Ressource bar width and height in pixels
RESSOURCEBARWIDTH = GAMEWIDTH
RESSOURCEBARHEIGHT = 60

# Menu bar width and height in pixels
MENUBARWIDTH = 180 
MENUBARHEIGHT = RESSOURCEBARHEIGHT + GAPSIZE_MENU + GAMEHEIGHT 

# Total window width and height in pixels
WINDOWWIDTH  = MENUBARWIDTH + 2*GAPSIZE_MENU + GAMEWIDTH + GAPSIZE
WINDOWHEIGHT = MENUBARHEIGHT + GAPSIZE + GAPSIZE_MENU

pygame.font.init()

font_bubble = pygame.font.Font(None, 14)
font = pygame.font.Font(None, 24)
font_title = pygame.font.Font(None, 68)
font_other = pygame.font.Font(None, 40)

menuCoords = [(WINDOWWIDTH - GAPSIZE - MENUBARWIDTH, GAPSIZE), 
              (WINDOWWIDTH - GAPSIZE - MENUBARWIDTH, WINDOWHEIGHT - GAPSIZE), 
              (WINDOWWIDTH - GAPSIZE, WINDOWHEIGHT - GAPSIZE), 
              (WINDOWWIDTH - GAPSIZE, GAPSIZE)]
largermenuCoords = [(WINDOWWIDTH - 3*GAPSIZE - MENUBARWIDTH, GAPSIZE), 
                    (WINDOWWIDTH - 3*GAPSIZE - MENUBARWIDTH, WINDOWHEIGHT \
                    - GAPSIZE), 
                    (WINDOWWIDTH, WINDOWHEIGHT - GAPSIZE), 
                    (WINDOWWIDTH, GAPSIZE)]
headerCoords = [(GAPSIZE, GAPSIZE), 
                (GAPSIZE, RESSOURCEBARHEIGHT), 
                (GAPSIZE + RESSOURCEBARWIDTH, RESSOURCEBARHEIGHT), 
                (GAPSIZE + RESSOURCEBARWIDTH, GAPSIZE)]
boardCoords = [(0, RESSOURCEBARHEIGHT), 
               (0, WINDOWHEIGHT), 
               (WINDOWWIDTH - GAPSIZE - MENUBARWIDTH, WINDOWHEIGHT), 
               (WINDOWWIDTH - GAPSIZE - MENUBARWIDTH, RESSOURCEBARHEIGHT)]
# Initialisation of many variables that are useful later

MINES_DENSITY = 80
NBMINES = int(NBCOLUMN * NBROW / MINES_DENSITY)

FORESTS_DENSITY = 80
NBFORESTS = int(NBCOLUMN * NBROW / FORESTS_DENSITY)

WHITE = (255, 255, 255) # white background
BLACK = (10, 10, 10)
RED = (255, 0, 0)
ORANGE = (139, 69, 19)

PRODSTEP = 15 # Number of steps between two productions

HAPPINESSGAP = 15
HAPPINESSSTEP = 15

time_lost = 5 # Time (sec) you have to improve happiness before you lose

TAXMAX = 10 # Maximum of tax you can impose
TAXMIN = 1 # Minimum of tax you can impose
TAXSTEP = 200 # Number of loops before tax is taken
DROPSTEP = 0.2 # Drop of percentage of happiness if nothing is done

CITIZENSLEVEL = 200