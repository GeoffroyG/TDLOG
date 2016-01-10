# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 15:36:10 2015

@author: Fatma - Geoffroy - Pierre
"""

import Classes_Tests
from Constantes import *
from pygame.locals import *
import os
import math

(font_width, font_height) = font.size("A")
n = (WINDOWHEIGHT-2*GAPSIZE-2*font_height) // (GAPSIZE + BOXSIZE) - 1 # number of pictures per column in the menu

def displayBeginningMenu(DISPLAYSURF, FPSCLOCK, font_title):
    game = False
    rules = False
    mousex = 0
    mousey = 0
    posReturn = pygame.Rect(0,0,0,0)
    background = pygame.image.load("2.Images/Backgroundimage.jpg").convert()
    pygame.transform.scale(background, (WINDOWWIDTH, WINDOWHEIGHT))

    while not game:
        DISPLAYSURF.blit(background, (0,0))
        text = font_title.render("Simulation de ville 2D", 1, (255, 0, 0))
        textposTitle = text.get_rect(centerx = WINDOWWIDTH / 2, centery = 50)
        DISPLAYSURF.blit(text, textposTitle)
        if not rules:
            text = font_other.render("Nouveau Jeu", 1, (10,10,10), (255,255,255))
            textposNewGame = text.get_rect(centerx = WINDOWWIDTH / 2, centery = WINDOWHEIGHT / 2)
            DISPLAYSURF.blit(text, textposNewGame)
            text = font_other.render("Regles", 1, (10,10,10), (255,255,255))
            textposRules = text.get_rect(centerx = WINDOWWIDTH / 2, centery = WINDOWHEIGHT / 2 + textposNewGame.height)
            DISPLAYSURF.blit(text, textposRules)
        else:
            text = font_other.render("Ceci sont les regles, ca va etre coton a  tout taper en faisant les sauts de lignes", 1, (10,10,10), (255,255,255))
            textpos = text.get_rect(centerx = WINDOWWIDTH / 2, centery = WINDOWHEIGHT / 2)
            DISPLAYSURF.blit(text, textpos)
            back = pygame.image.load("2.Images/Return.png").convert()
            DISPLAYSURF.blit(back, (0,0))
            posReturn = pygame.Rect(0, 0, 40, 40)


        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            elif event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                os.sys.exit()


        if textposNewGame.collidepoint(mousex, mousey) and not rules and mouseClicked:
            game = True
        elif textposRules.collidepoint(mousex, mousey) and not rules and mouseClicked:
            rules = True
        elif posReturn.collidepoint(mousex, mousey) and rules and mouseClicked:
            rules = False

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        mouseClicked = False

def getBoxAtPixelGame(mousex, mousey, origin):
    ''' Translates the coordinates in the game from pixels to integers. '''
    i = origin[0] + ((mousey - RESSOURCEBARHEIGHT) / GAMEHEIGHT * NBROW_DISP)
    j = origin[1] + (mousex / GAMEWIDTH * NBCOLUMN_DISP)
    return(int(i),int(j))

def getBuildingFromMenu(mousex, mousey, selected, buildings):
    ''' Gives the building from the coordinates in the menu (see drawBoard). '''
    p = (mousex-WINDOWWIDTH+MENUBARWIDTH)//(GAPSIZE+BOXSIZE)
    q = (mousey-RESSOURCEBARHEIGHT-2*GAPSIZE)//(GAPSIZE+BOXSIZE)
    k = int(p)*n+int(q)
    if k >= 0 and k < 10:
        for i in range(len(selected)):
            selected[i] = False
        selected[k] = True
        return(buildings[k])
    else:
        return(None)

def getType(Map, boxx, boxy):
    ''' Returns the type of the object in position (x,y). '''
    matrix = Map.types()
    return(matrix[boxx][boxy])

def remove(list_types_coords, boxx, boxy):
    ''' Deletes a building from the map. The list is organized this way :
    [Building A, Building Coords A, Building B...]. '''
    n = len(list_types_coords)
    n = n//2
    k_final = 0
    i_final = 0
    for k in range(n):
        coords_list = list_types_coords[2*k+1]
        p = len(coords_list)
        for i in range(p):
            if [boxx,boxy] == coords_list[i]:
                k_final = k
                i_final = i
    del list_types_coords[2*k_final][i_final]
    del list_types_coords[2*k_final+1][i_final]


def drawBoard(Map, DISPLAYSURF, selected, timing, origin, graphism):
    ''' Displays the entire board. '''
    # First we display the background
    pygame.draw.polygon(DISPLAYSURF, BGCOLOR, boardCoordinates)
    # We display each box with the picture attached to it
    for i in range(NBROW_DISP):
        for j in range(NBCOLUMN_DISP):
            p = Map.map[origin[0]+i][origin[1]+j].type
            dessin = graphism[p]
            DISPLAYSURF.blit(dessin, (GAPSIZE + (BOXSIZE+GAPSIZE)*j, RESSOURCEBARHEIGHT + GAPSIZE + (BOXSIZE+GAPSIZE)*i))


def drawBoard_changes(Map, DISPLAYSURF, selected, timing, origin, graphism, changes, change_all):
    ''' Displays the entire board. '''

    if change_all == True:
        drawBoard(Map, DISPLAYSURF, selected, timing, origin, graphism)

    else:
        if len(changes) != 0:
            for k in range(len(changes)):
                if changes[k][0] >= origin[0] and changes[k][0] < origin[0] + NBROW_DISP and changes[k][1] >= origin[1] and changes[k][1] < origin[1] + NBCOLUMN_DISP:
                    i = changes[k][0] - origin[0]
                    j = changes[k][1] - origin[1]
                    p = Map.map[origin[0]+changes[k][0]][origin[1]+changes[k][1]].type
                    dessin = graphism[p]
                    coordinates = [(j*(BOXSIZE+GAPSIZE),RESSOURCEBARHEIGHT+i*(BOXSIZE+GAPSIZE)),(j*(BOXSIZE+GAPSIZE),RESSOURCEBARHEIGHT+i*(BOXSIZE+GAPSIZE)+BOXSIZE+2*GAPSIZE),(j*(BOXSIZE+GAPSIZE)+BOXSIZE+2*GAPSIZE,RESSOURCEBARHEIGHT+i*(BOXSIZE+GAPSIZE)+BOXSIZE+2*GAPSIZE),(j*(BOXSIZE+GAPSIZE)+BOXSIZE+2*GAPSIZE,RESSOURCEBARHEIGHT+i*(BOXSIZE+GAPSIZE))]
                    pygame.draw.polygon(DISPLAYSURF, (255,255,255), coordinates)
                    DISPLAYSURF.blit(dessin, (GAPSIZE + (BOXSIZE+GAPSIZE)*j, RESSOURCEBARHEIGHT + GAPSIZE + (BOXSIZE+GAPSIZE)*i))


def drawHeader(Map, DISPLAYSURF):
    # Then we display the ressources
    pygame.draw.polygon(DISPLAYSURF, (255,255,255), headerCoordinates)
    ressources = "Money : "+str(Map.money)+"   Wood : "+str(Map.wood)+"   Stone : "+str(Map.stone)+"   Habitants : "+str(Map.habitants)+"   NRJ : "+str(Map.elec)
    text = font.render(ressources, 1, (10,10,10))
    textpos = text.get_rect(centerx=RESSOURCEBARWIDTH/2,centery=GAPSIZE+RESSOURCEBARHEIGHT/2)
    DISPLAYSURF.blit(text, textpos)

def drawMenu(Map, DISPLAYSURF, selected, timing, toBuild, toBuild_Selected):
    # We draw the background for the menu (I don't know why we have to do this step everytime but else it erases)
    pygame.draw.polygon(DISPLAYSURF, (139,69,19), menuCoordinates)

    # And finally all the things that are on said menu
    text = font.render("Menu", 1, (10,10,10))
    textpos = text.get_rect(centerx=RESSOURCEBARWIDTH+2*GAPSIZE + MENUBARWIDTH/2, centery=GAPSIZE+RESSOURCEBARHEIGHT/2)
    DISPLAYSURF.blit(text, textpos)
    text = font.render("Time : "+str(timing), 1, (10,10,10))
    textpos = text.get_rect(centerx=RESSOURCEBARWIDTH+2*GAPSIZE + MENUBARWIDTH/2, centery=WINDOWHEIGHT-GAPSIZE-24/2)
    DISPLAYSURF.blit(text, textpos)

    # For the pictures of the buildings we can change n to print more buildings in height, I haven't thought of a formula that would depend on the window length
    i=0

    for k in toBuild:
        # The formula is more understandable in this order, but it's the same than in detBuildingFromMenu actually
        x = (i//n)*(GAPSIZE+BOXSIZE)+WINDOWWIDTH-MENUBARWIDTH
        y = (i%n)*(GAPSIZE+BOXSIZE)+RESSOURCEBARHEIGHT+2*GAPSIZE
        DISPLAYSURF.blit(k,(x,y))
        i+=1
    i=0

    for k in selected:
        if k:
            dessin = toBuild_Selected[i]
            x = (i//n)*(GAPSIZE+BOXSIZE)+WINDOWWIDTH-MENUBARWIDTH
            y = (i%n)*(GAPSIZE+BOXSIZE)+RESSOURCEBARHEIGHT+2*GAPSIZE
            DISPLAYSURF.blit(dessin,(x,y))
        i+=1


def isInMenu(mousex):
    ''' Returns True if the mouse is in the menu. '''
    if mousex > WINDOWWIDTH - MENUBARWIDTH:
        return(True)
    else:
        return(False)

def isInGame(mousex, mousey):
    ''' Returns True if the mouse is in the game. '''
    if mousex < GAMEWIDTH + 2*GAPSIZE and mousey > RESSOURCEBARHEIGHT + 2*GAPSIZE:
        return(True)
    else:
        return(False)

def drawHappiness(DISPLAYSURF, happiness, topleftx, toplefty, size):
    '''Draws the happiness level'''
    color = (int(255*(1-happiness)),int(255*happiness),0)
    center = (topleftx+size//2,toplefty+size//2)
    pygame.draw.circle(DISPLAYSURF,(0,0,0),center,size//2+1)
    pygame.draw.circle(DISPLAYSURF,color,center,size//2)
    x = size//6
    y = size//4
    length = size//4
    pygame.draw.line(DISPLAYSURF,(0,0,0),(topleftx+size//2-x,toplefty+size//2-y),(topleftx+size//2-x,toplefty+size//2-y+length))
    pygame.draw.line(DISPLAYSURF,(0,0,0),(topleftx+size//2+x,toplefty+size//2-y),(topleftx+size//2+x,toplefty+size//2-y+length))
    height_max = size // 5
    if happiness > 0.5:
        topleftRect = [topleftx+size//2-size//4, toplefty+size//2+size//8-int(height_max*happiness)]
        smileRect = pygame.Rect(topleftRect[0],topleftRect[1],size//2,int(height_max*happiness))
        pygame.draw.arc(DISPLAYSURF,(0,0,0),smileRect,math.pi,2*math.pi)
    if happiness == 0.5:
        pygame.draw.line(DISPLAYSURF,(0,0,0),(topleftx+size//2-size//5, toplefty+size//2+size//8),(topleftx+size//2+size//5, toplefty+size//2+size//8))
    if happiness < 0.5:
        topleftRect = [topleftx+size//2-size//4, toplefty+size//2+size//8]
        smileRect = pygame.Rect(topleftRect[0],topleftRect[1],size//2,int(height_max*happiness))
        pygame.draw.arc(DISPLAYSURF,(0,0,0),smileRect,0,math.pi)

def drawInfoMenu(DISPLAYSURF, mousex, mousey, buildings):
    p = (mousex-WINDOWWIDTH+MENUBARWIDTH)//(GAPSIZE+BOXSIZE)
    q = (mousey-RESSOURCEBARHEIGHT-2*GAPSIZE)//(GAPSIZE+BOXSIZE)
    k = int(p)*n+int(q)
    #print(k)
    if k < len(buildings)-2 and k >= 0 :
        if buildings[k].wood_needed != 0 and buildings[k].stone_needed != 0 and buildings[k].money_needed != 0 and buildings[k].elec_needed != 0:
            text = "Bois requis : "+str(buildings[k].wood_needed)+" \n "+"Pierre requis : "+str(buildings[k].stone_needed)+" \n "+"Cout : "+str(buildings[k].money_needed)+" \n "+"NRJ : "+str(buildings[k].elec_needed)
        elif buildings[k].wood_needed == 0 and buildings[k].stone_needed != 0 and buildings[k].money_needed != 0 and buildings[k].elec_needed != 0:
            text = "Pierre requis : "+str(buildings[k].stone_needed)+" \n "+"Cout : "+str(buildings[k].money_needed)+" \n "+"NRJ : "+str(buildings[k].elec_needed)    
        elif buildings[k].wood_needed == 0 and buildings[k].stone_needed != 0 and buildings[k].money_needed != 0 and buildings[k].elec_needed == 0:
            text = "Pierre requis : "+str(buildings[k].stone_needed)+" \n "+"Cout : "+str(buildings[k].money_needed)   
        elif buildings[k].type == 9 :
            text =""
        height = font_bubble.get_height()*1
        gap=0
        for line in text.splitlines():
            img = font_bubble.render(line,1,(10,10,10),(255,255,255))
            textpos = img.get_rect(centerx=(k//n)*(GAPSIZE+BOXSIZE)+WINDOWWIDTH-MENUBARWIDTH+35, centery=(k%n)*(GAPSIZE+BOXSIZE)+RESSOURCEBARHEIGHT+2*GAPSIZE+5+gap)
            DISPLAYSURF.blit(img,textpos)
            gap += height
        

def drawInfoBoard(DISPLAYSURF, boxx, boxy, mainBoard):
    # Display House data
    if  getType(mainBoard, boxx, boxy) == 1:
        text = "Habs : "+str(mainBoard.map[boxx][boxy].hab)+" \n "+"NRJ : "+str(mainBoard.map[boxx][boxy].elec_needed)
        height = font_bubble.get_height()*1
        gap=0
        for line in text.splitlines():
            img = font_bubble.render(line,1,(10,10,10),(255,255,255))
            textpos = img.get_rect(centerx=GAPSIZE + (BOXSIZE+GAPSIZE)*boxy+15, centery=RESSOURCEBARHEIGHT + GAPSIZE + (BOXSIZE+GAPSIZE)*boxx+gap)
            DISPLAYSURF.blit(img,textpos)
            gap += height

#        textpos = text.get_rect(centerx=GAPSIZE + (BOXSIZE+GAPSIZE)*boxy+15, centery=RESSOURCEBARHEIGHT + GAPSIZE + (BOXSIZE+GAPSIZE)*boxx)
#        DISPLAYSURF.blit(text, textpos)

    # Display Factory or workshop data
    elif getType(mainBoard, boxx, boxy) in [2,3]:
        text="Empl : "+str(mainBoard.map[boxx][boxy].worker)+" \n "+"Prod : "+str(int(mainBoard.map[boxx][boxy].prod_max * mainBoard.map[boxx][boxy].worker / mainBoard.map[boxx][boxy].hab_max))+" \n "+"NRJ : "+str(mainBoard.map[boxx][boxy].elec_needed)
        height = font_bubble.get_height()*1
        gap=0
        for line in text.splitlines():
            img = font_bubble.render(line,1,(10,10,10),(255,255,255))
            textpos = img.get_rect(centerx=GAPSIZE + (BOXSIZE+GAPSIZE)*boxy+15, centery=RESSOURCEBARHEIGHT + GAPSIZE + (BOXSIZE+GAPSIZE)*boxx+gap)
            DISPLAYSURF.blit(img,textpos)
            gap += height

    # Display NRJ data
    if  getType(mainBoard, boxx, boxy) in [4,5,6,7]:
        text = font_bubble.render("NRJ : "+str(mainBoard.map[boxx][boxy].elec_needed),1,(10,10,10),(255,255,255))
        textpos = text.get_rect(centerx=GAPSIZE + (BOXSIZE+GAPSIZE)*boxy+15, centery=RESSOURCEBARHEIGHT + GAPSIZE + (BOXSIZE+GAPSIZE)*boxx)
        DISPLAYSURF.blit(text,textpos)
        
