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
n = (WINDOWHEIGHT-2*GAPSIZE_MENU-2*font_height) // (GAPSIZE_MENU + BOXSIZE) - 1 # number of pictures per column in the menu

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


def drawBoard(Map, DISPLAYSURF, selected, timing, origin, graphism):
    ''' Displays the entire board. '''
    # First we display the background
    pygame.draw.polygon(DISPLAYSURF, BGCOLOR, boardCoordinates)
    # We display each box with the picture attached to it
    for i in range(NBROW_DISP):
        for j in range(NBCOLUMN_DISP):
            p = Map.map[origin[0]+i][origin[1]+j].type
            dessin = graphism[p]
            DISPLAYSURF.blit(dessin, ((BOXSIZE+GAPSIZE)*j + GAPSIZE, RESSOURCEBARHEIGHT + GAPSIZE + (BOXSIZE+GAPSIZE)*i))


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
                    coordinates = [(j*(BOXSIZE+GAPSIZE),RESSOURCEBARHEIGHT+i*(BOXSIZE+GAPSIZE)),(j*(BOXSIZE+GAPSIZE),RESSOURCEBARHEIGHT+i*(BOXSIZE+GAPSIZE)+BOXSIZE+GAPSIZE),(j*(BOXSIZE+GAPSIZE)+BOXSIZE+GAPSIZE,RESSOURCEBARHEIGHT+i*(BOXSIZE+GAPSIZE)+BOXSIZE+GAPSIZE),(j*(BOXSIZE+GAPSIZE)+BOXSIZE+GAPSIZE,RESSOURCEBARHEIGHT+i*(BOXSIZE+GAPSIZE))]
                    pygame.draw.polygon(DISPLAYSURF, (255,255,255), coordinates)
                    DISPLAYSURF.blit(dessin, (GAPSIZE + (BOXSIZE+GAPSIZE)*j, RESSOURCEBARHEIGHT + GAPSIZE + (BOXSIZE+GAPSIZE)*i))


def drawHeader(Map, DISPLAYSURF):
    # Then we display the ressources
    pygame.draw.polygon(DISPLAYSURF, (255,255,255), headerCoordinates)
    ressources = "Money : "+str(Map.money)+"   Wood : "+str(Map.wood)+"   Stone : "+str(Map.stone)+"   Habitants : "+str(Map.habitants)+"   Electricity : "+str(Map.elec)
    text = font.render(ressources, 1, (10,10,10))
    textpos = text.get_rect(centerx=RESSOURCEBARWIDTH/2,centery=GAPSIZE+RESSOURCEBARHEIGHT/2)
    DISPLAYSURF.blit(text, textpos)
    
def drawHappiness(DISPLAYSURF, happiness, topleftx, toplefty, size, color_text):
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
    center_left = [topleftx+size//2-size//5, toplefty+size//2+size//5]
    center_right = [topleftx+size//2+size//5, toplefty+size//2+size//5]
    height_prop = abs(happiness-0.5)
    if height_prop < 0.2:
        pygame.draw.line(DISPLAYSURF,(0,0,0),(center_left[0], center_left[1]),(center_right[0], center_right[1]))
    else:
        if height_prop < 0.4:
            height_prop = 0.4
        else:
            height_prop = 0.5
        topleftRect = [center_left[0], center_left[1]-int(height_prop*height_max)]
        smileRect = pygame.Rect(topleftRect[0],topleftRect[1],2*size//5,int(height_max*height_prop*2))
        if happiness > 0.5:
            a = math.pi
            b = 2*a
        else:
            a = 2*math.pi
            b = 3*math.pi
        pygame.draw.arc(DISPLAYSURF,(0,0,0),smileRect,a,b)
    happ = str(int(100*happiness))+"%"
    text = font.render(happ, 1, color_text)
    textpos = text.get_rect(centerx=3*topleftx+size,centery=GAPSIZE+RESSOURCEBARHEIGHT/2)
    DISPLAYSURF.blit(text, textpos)   

def drawMenu(Map, DISPLAYSURF, selected, timing, toBuild, toBuild_Selected,color):
    """ Draws the menu on the right side of the game with buildings, priorities and timing"""
    # We first draw a white background to erase traces of Menu Info
    pygame.draw.polygon(DISPLAYSURF, (255,255,255), largerMenuCoordinates)
    # We draw the background for the menu (I don't know why we have to do this step everytime but else it erases)
    pygame.draw.polygon(DISPLAYSURF, (139,69,19), menuCoordinates)

    # And finally all the things that are on said menu
    text = font.render("Menu", 1, (10,10,10))
    textpos = text.get_rect(centerx=RESSOURCEBARWIDTH+2*GAPSIZE_MENU + MENUBARWIDTH/2, centery=GAPSIZE_MENU+RESSOURCEBARHEIGHT/2)
    DISPLAYSURF.blit(text, textpos)
    text = font.render("Time : "+str(timing), 1, color)
    textpos = text.get_rect(centerx=RESSOURCEBARWIDTH+2*GAPSIZE_MENU + MENUBARWIDTH/2, centery=WINDOWHEIGHT-GAPSIZE_MENU-24/2)
    DISPLAYSURF.blit(text, textpos)

    # For the pictures of the buildings we can change n to print more buildings in height, I haven't thought of a formula that would depend on the window length
    i=0

    for k in toBuild:
        # The formula is more understandable in this order, but it's the same than in detBuildingFromMenu actually
        x = (i//n)*(GAPSIZE_MENU+BOXSIZE)+WINDOWWIDTH-MENUBARWIDTH
        y = (i%n)*(GAPSIZE_MENU+BOXSIZE)+RESSOURCEBARHEIGHT+2*GAPSIZE_MENU
        DISPLAYSURF.blit(k,(x,y))
        i+=1
    i=0

    for k in selected:
        if k:
            dessin = toBuild_Selected[i]
            x = (i//n)*(GAPSIZE_MENU+BOXSIZE)+WINDOWWIDTH-MENUBARWIDTH
            y = (i%n)*(GAPSIZE_MENU+BOXSIZE)+RESSOURCEBARHEIGHT+2*GAPSIZE_MENU
            DISPLAYSURF.blit(dessin,(x,y))
        i+=1 

def drawInfoMenu(DISPLAYSURF, mousex, mousey, buildings):
    """ Draws info bubbles for buildings in the menu bar"""
    p = (mousex-WINDOWWIDTH+MENUBARWIDTH)//(GAPSIZE_MENU+BOXSIZE)
    q = (mousey-RESSOURCEBARHEIGHT-2*GAPSIZE_MENU)//(GAPSIZE_MENU+BOXSIZE)
    k = int(p)*n+int(q)
    if k < len(buildings)-1 and k >= 0 :
        text = ""
        money_needed = buildings[k].money_needed
        wood_needed = buildings[k].wood_needed
        stone_needed = buildings[k].stone_needed
        elec_needed = buildings[k].elec_needed
        jump = False
        if money_needed > 0:
            text += "Money needed : "+str(money_needed)
            jump = True
        if wood_needed > 0:
            if jump:
                text += " \n "
            text += "Wood needed : "+str(wood_needed)
            jump = True
        if stone_needed > 0:
            if jump:
                text += " \n "
            text += "Stone needed : "+str(stone_needed)
            jump = True
        if elec_needed > 0:
            if jump:
                text += " \n "
            text += "Elec. needed : "+str(elec_needed)
            jump = True
        if elec_needed < 0:
            if jump:
                text += " \n "
            text += "Gains Elec. : +"+str(-elec_needed)
            jump = True
        if buildings[k].type == 9:
            text = "Erases buildings"
        else:
            height = font_bubble.get_height()*1
            gap=0
            for line in text.splitlines():
                img = font_bubble.render(line,1,(10,10,10),(255,255,255))
                textpos = img.get_rect(centerx=(k//n)*(GAPSIZE_MENU+BOXSIZE)+WINDOWWIDTH-MENUBARWIDTH+35, centery=(k%n)*(GAPSIZE_MENU+BOXSIZE)+RESSOURCEBARHEIGHT+2*GAPSIZE_MENU+5+gap)
                DISPLAYSURF.blit(img,textpos)
                gap += height
    
        

def drawInfoBoard(DISPLAYSURF, boxx, boxy, mainBoard, buildings):
    """ Draws info bubbles for buildings in the main board"""
    # Display House data
    building = mainBoard.map[boxx][boxy]
    text = ""
    jump = False
    if building.hab > 0:
        text += "Hab. : "+str(building.hab)
        jump = True
    if building.elec_needed > 0:
        if jump:
            text += " \n "
        text += "Elec. : -"+str(building.elec_needed)
        jump = True
    if building.elec_needed < 0:
        if jump:
            text += " \n "
        text += "Elec. : +"+str(-building.elec_needed)
        jump = True
    if building.wood_input > 0:
        if jump:
            text += " \n "
        text += "Wood In. : "+str(building.wood_input)
        jump = True
    if building.stone_input > 0:
        if jump:
            text += " \n "
        text += "Stone In. : "+str(building.stone_input)
        jump = True
    if building.money_input > 0:
        if jump:
            text += " \n "
        text += "Money In. : "+str(building.money_input)
        jump = True
    if building.money_output > 0:
        if jump:
            text += " \n "
        text += "Money Out. : "+str(building.money_output)
        jump = True
    if building.wood_output > 0:
        if jump:
            text += " \n "
        text += "Wood Out. : "+str(building.wood_output)
        jump = True
    if building.stone_output > 0:
        if jump:
            text += " \n "
        text += "Stone Out. : "+str(building.stone_output)
        jump = True
    if building.happiness_output > 0:
        if jump:
            text += " \n "
        text += "Hap. Out. : "+str(int(100*building.happiness_output))+"%"
        jump = True
    if text == "":
        return(1)
        
    height = font_bubble.get_height()*1
    gap=0
    for line in text.splitlines():
        img = font_bubble.render(line,1,(10,10,10),(255,255,255))
        textpos = img.get_rect(centerx=GAPSIZE + (BOXSIZE+GAPSIZE)*boxy+15, centery=RESSOURCEBARHEIGHT + GAPSIZE + (BOXSIZE+GAPSIZE)*boxx+gap)
        DISPLAYSURF.blit(img,textpos)
        gap += height

        
def displayLosingMenu(DISPLAYSURF, FPSCLOCK):
    """When the game is over, displays a message to the player"""
    lost = True
    DISPLAYSURF.fill((0,0,0))
    mouseClicked = False
    
    while lost:
        text = font_title.render("YOU LOST : CLICK TO START AGAIN", 1, (255, 0, 0))
        textposTitle = text.get_rect(centerx = WINDOWWIDTH / 2, centery = WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(text, textposTitle)
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            elif event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                os.sys.exit()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
        if mouseClicked:
            lost = False
