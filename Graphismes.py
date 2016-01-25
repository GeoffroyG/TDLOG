# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 15:36:10 2015

@author: Fatma - Geoffroy - Pierre
"""

import Classes
from Constantes import *
from pygame.locals import *
import os
import math

(font_width, font_height) = font.size("A")

# Number of pictures per column in the menu
n = (WINDOWHEIGHT - 2*GAPSIZE_MENU - 2*font_height) \
    // (GAPSIZE_MENU + BOXSIZE) - 1 

def displayBeginningMenu(DISPLAYSURF, FPSCLOCK, font_title):
    game = False
    rules = False
    credits_game = False
    leaderboard = False
    mousex = 0
    mousey = 0
    posReturn = pygame.Rect(0,0,0,0)
    background = pygame.image.load("2.Images/Backgroundimage.jpg").convert()
    pygame.transform.scale(background, (WINDOWWIDTH, WINDOWHEIGHT))

    while not game:
        DISPLAYSURF.blit(background, (0,0))
        text = font_title.render("City Management 2D", 1, RED)
        textposTitle = text.get_rect(centerx = WINDOWWIDTH / 2, centery = 50)
        DISPLAYSURF.blit(text, textposTitle)
        if not rules and not credits_game and not leaderboard:
            text = font_other.render("New Game", 1, BLACK, WHITE)
            textposNewGame = text.get_rect(centerx = WINDOWWIDTH / 2, 
                                           centery = WINDOWHEIGHT / 2)
            DISPLAYSURF.blit(text, textposNewGame)
            text = font_other.render("Instructions", 1, BLACK, WHITE)
            textposRules = text.get_rect(centerx = WINDOWWIDTH / 2, 
                                         centery = WINDOWHEIGHT / 2 + \
                                                   textposNewGame.height)
            DISPLAYSURF.blit(text, textposRules)
            text = font_other.render("Credits", 1, BLACK, WHITE)
            textposCredits = text.get_rect(centerx = WINDOWWIDTH / 2, 
                                           centery = WINDOWHEIGHT / 2 + \
                                                     textposNewGame.height + \
                                                     textposNewGame.height)
            DISPLAYSURF.blit(text, textposCredits)
        elif rules:
            text = font_other.render("Rules", 1, BLACK, WHITE)
            textpos = text.get_rect(centerx = WINDOWWIDTH / 2, 
                                    centery = WINDOWHEIGHT / 2)
            DISPLAYSURF.blit(text, textpos)
            back = pygame.image.load("2.Images/Return.png").convert()
            DISPLAYSURF.blit(back, (0, 0))
            posReturn = pygame.Rect(0, 0, 40, 40)
        elif credits_game:
            text = font_other.render("Credits for noun Projet and Pygame", 1, 
                                     BLACK, WHITE)
            textpos = text.get_rect(centerx = WINDOWWIDTH / 2, 
                                    centery = WINDOWHEIGHT / 2)
            DISPLAYSURF.blit(text, textpos)
            back = pygame.image.load("2.Images/Return.png").convert()
            DISPLAYSURF.blit(back, (0, 0))
            posReturn = pygame.Rect(0, 0, 40, 40)            

        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            elif event.type == QUIT or (event.type == KEYUP \
                                        and event.key == K_ESCAPE):
                pygame.quit()
                os.sys.exit()


        if textposNewGame.collidepoint(mousex, mousey) \
           and not rules and not credits_game and mouseClicked:
            game = True
        elif textposRules.collidepoint(mousex, mousey) \
             and not rules and not credits_game and mouseClicked:
            rules = True
        elif textposCredits.collidepoint(mousex, mousey) \
             and not credits_game and mouseClicked:
            credits_game = True           
        elif posReturn.collidepoint(mousex, mousey) \
             and rules and mouseClicked:
            rules = False
        elif posReturn.collidepoint(mousex, mousey) \
             and credits_game and mouseClicked:
            credits_game = False

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
    if mousex < GAMEWIDTH + 2*GAPSIZE \
       and mousey > RESSOURCEBARHEIGHT + 2*GAPSIZE:
        return(True)
    else:
        return(False)


def getBoxAtPixelGame(mousex, mousey, origin):
    ''' Translates the coordinates in the game from pixels to integers. '''
    i = origin[0] + ((mousey - RESSOURCEBARHEIGHT) / GAMEHEIGHT * NBROW_DISP)
    j = origin[1] + (mousex / GAMEWIDTH * NBCOLUMN_DISP)
    return(int(i), int(j))

def getBuildingFromMenu(mousex, mousey, selected, buildings, click):
    ''' Returns the building corresponding to coordinates in the menu. '''
    p = (mousex - WINDOWWIDTH + MENUBARWIDTH)//(GAPSIZE_MENU + BOXSIZE)
    q = (mousey - RESSOURCEBARHEIGHT - 2*GAPSIZE_MENU)//(GAPSIZE_MENU \
                                                         + BOXSIZE)
    k = int(p)*n+int(q)
    if k >= 0 and k < 10:
        if click == True:
            old_status = selected[k]
            for i in range(len(selected)):
                selected[i] = False
            selected[k] = (old_status + 1)%2
        return(selected, True, buildings[k])
    else:
        return(selected, False, buildings[9])

def getType(Map, boxx, boxy):
    ''' Returns the type of the object in position (x,y). '''
    matrix = Map.types()
    return(matrix[boxx][boxy])


def drawBoard(Map, DISPLAYSURF, selected, timing, origin, graphism):
    ''' Displays the entire board. '''
    # First we display the background
    pygame.draw.polygon(DISPLAYSURF, WHITE, boardCoords)
    # We display each box with the picture attached to it
    for i in range(NBROW_DISP):
        for j in range(NBCOLUMN_DISP):
            p = Map.map[origin[0]+i][origin[1]+j].type
            dessin = graphism[p]
            DISPLAYSURF.blit(dessin, ((BOXSIZE+GAPSIZE)*j + GAPSIZE, 
                                      RESSOURCEBARHEIGHT + GAPSIZE + \
                                      (BOXSIZE+GAPSIZE)*i))


def drawBoard_changes(Map, DISPLAYSURF, selected, timing, origin, graphism, 
                      changes, change_all):
    ''' Displays the entire board. '''

    if change_all == True:
        drawBoard(Map, DISPLAYSURF, selected, timing, origin, graphism)

    else:
        if len(changes) != 0:
            for k in range(len(changes)):
                if changes[k][0] >= origin[0] \
                   and changes[k][0] < origin[0] + NBROW_DISP \
                   and changes[k][1] >= origin[1] \
                   and changes[k][1] < origin[1] + NBCOLUMN_DISP:
                    i = changes[k][0] - origin[0]
                    j = changes[k][1] - origin[1]
                    a = origin[0]+changes[k][0]
                    b = origin[1]+changes[k][1]
                    p = Map.map[a][b].type
                    dessin = graphism[p]
                    coords = [(j*(BOXSIZE + GAPSIZE),
                               RESSOURCEBARHEIGHT + i*(BOXSIZE + GAPSIZE)),
                              (j*(BOXSIZE + GAPSIZE), 
                               RESSOURCEBARHEIGHT + i*(BOXSIZE + GAPSIZE)\
                               + BOXSIZE + GAPSIZE), 
                              ((j+1)*(BOXSIZE + GAPSIZE), 
                               RESSOURCEBARHEIGHT + (i+1)*(BOXSIZE + GAPSIZE)), 
                              ((j+1)*(BOXSIZE + GAPSIZE), 
                               RESSOURCEBARHEIGHT + i*(BOXSIZE + GAPSIZE))]
                    pygame.draw.polygon(DISPLAYSURF, WHITE, coords)
                    DISPLAYSURF.blit(dessin, (GAPSIZE + (BOXSIZE+GAPSIZE)*j, 
                                              RESSOURCEBARHEIGHT + GAPSIZE + \
                                              (BOXSIZE+GAPSIZE)*i))


def drawHeader(Map, DISPLAYSURF):
    """ Header to display the main variable : ressources, happiness and 
    number of inhabitants. """
    pygame.draw.polygon(DISPLAYSURF, WHITE, headerCoords)
    ressources = "Money : "+str(round(Map.money, 2)) + \
                 "   Wood : "+str(round(Map.wood, 2)) + \
                 "   Stone : "+str(round(Map.stone, 2)) + \
                 "   Habitants : "+str(Map.citizens) + \
                 "   Electricity : "+str(Map.elec)
    text = font.render(ressources, 1, BLACK)
    textpos = text.get_rect(centerx = RESSOURCEBARWIDTH/2, 
                            centery = GAPSIZE + RESSOURCEBARHEIGHT/2)
    DISPLAYSURF.blit(text, textpos)
    
def drawHappiness(DISPLAYSURF, happiness, topleftx, toplefty, size, color_txt):
    '''Draws the happiness level with a percentage and a smiley. '''
    color = (int(255*(1-happiness)), int(255*happiness), 0)
    center = (topleftx + size//2, toplefty + size//2)
    pygame.draw.circle(DISPLAYSURF, BLACK, center, 1 + size//2)
    pygame.draw.circle(DISPLAYSURF, color, center, size//2)
    x = size//6
    y = size//4
    length = size//4
    pygame.draw.line(DISPLAYSURF, BLACK,
                     (topleftx + size//2 - x, toplefty + size//2 - y),
                     (topleftx + size//2 - x, toplefty + size//2 - y + length))
    pygame.draw.line(DISPLAYSURF, BLACK, (topleftx + size//2 + x, 
                                          toplefty + size//2 - y),
                                         (topleftx + size//2 + x, 
                                          toplefty + size//2 - y + length))
    height_max = size // 5
    center_left = [topleftx + size//2 - size//5, toplefty + size//2 + size//5]
    center_right = [topleftx + size//2 + size//5, toplefty + size//2 + size//5]
    height_prop = abs(happiness - 0.5)
    
    if height_prop < 0.2:
        pygame.draw.line(DISPLAYSURF, BLACK, (center_left[0], 
                                              center_left[1]), 
                                              (center_right[0], 
                                               center_right[1]))
    else:
        if height_prop < 0.4:
            height_prop = 0.4
        else:
            height_prop = 0.5
        topleftRect = [center_left[0], center_left[1] \
                                       - int(height_prop*height_max)]
        smileRect = pygame.Rect(topleftRect[0], topleftRect[1], 2*size//5, 
                                int(height_max*height_prop*2))
        if happiness > 0.5:
            a = math.pi
            b = 2*a
        else:
            a = 2*math.pi
            b = 3*math.pi
        pygame.draw.arc(DISPLAYSURF, BLACK, smileRect, a, b)
        
    happ = str(int(100*happiness)) + "%"
    text = font.render(happ, 1, color_txt)
    textpos = text.get_rect(centerx = 3*topleftx + size, 
                            centery = GAPSIZE + RESSOURCEBARHEIGHT/2)
    DISPLAYSURF.blit(text, textpos)   

def drawMenu(Map, DISPLAYSURF, selected, timing, toBuild, toBuild_Selected, 
             color, tax):
    """ Draws the menu on the right side of the game with buildings, 
    priorities and timing. """
    # We first draw a white background to erase traces of Menu Info
    pygame.draw.polygon(DISPLAYSURF, WHITE, largermenuCoords)
    # We draw the background for the menu
    pygame.draw.polygon(DISPLAYSURF, ORANGE, menuCoords)

    # And finally all the things that are on said menu
    text = font.render("Menu", 1, BLACK)
    textpos = text.get_rect(centerx = RESSOURCEBARWIDTH + 2*GAPSIZE_MENU \
                                    + MENUBARWIDTH/2, 
                            centery = GAPSIZE_MENU + RESSOURCEBARHEIGHT/2)
    DISPLAYSURF.blit(text, textpos)
    text = font.render("Time : " + str(timing), 1, color)
    textpos = text.get_rect(centerx = RESSOURCEBARWIDTH + 2*GAPSIZE_MENU \
                                    + MENUBARWIDTH/2, 
                                    centery = WINDOWHEIGHT - GAPSIZE_MENU - 12)
    DISPLAYSURF.blit(text, textpos)

    # For the pictures of the buildings we can change n to print more 
    # buildings in height
    i = 0

    for k in toBuild:
        # The formula is more understandable in this order, but it's 
        # the same than in detBuildingFromMenu actually.
        x = (i//n)*(GAPSIZE_MENU + BOXSIZE) + WINDOWWIDTH - MENUBARWIDTH
        y = (i%n)*(GAPSIZE_MENU + BOXSIZE) + RESSOURCEBARHEIGHT \
            + 2*GAPSIZE_MENU
        DISPLAYSURF.blit(k,(x,y))
        i += 1
    i = 0

    for k in selected:
        if k:
            dessin = toBuild_Selected[i]
            x = (i//n)*(GAPSIZE_MENU + BOXSIZE) + WINDOWWIDTH - MENUBARWIDTH
            y = (i%n)*(GAPSIZE_MENU + BOXSIZE) + RESSOURCEBARHEIGHT \
                + 2*GAPSIZE_MENU
            DISPLAYSURF.blit(dessin,(x,y))
        i += 1 
        
    drawPriorities(Map, DISPLAYSURF, color)
    drawTaxes(Map, DISPLAYSURF, color, tax)
    drawShortcuts(Map, DISPLAYSURF, color, toBuild)

def drawTaxes(Map, DISPLAYSURF, color, tax):    
    """ Displays the current amount of taxes and "+" and "-" buttons. """
    
    text = font.render("Taxes", 1, color)
    x = RESSOURCEBARWIDTH + 2*GAPSIZE_MENU + MENUBARWIDTH/2
    y = WINDOWHEIGHT - GAPSIZE_MENU - 72
    textpos = text.get_rect(centerx = x, centery = y)
    DISPLAYSURF.blit(text, textpos)

    text = font.render("-", 1, color)
    x = RESSOURCEBARWIDTH + 6*GAPSIZE_MENU
    y = WINDOWHEIGHT - GAPSIZE_MENU - 54
    Map.tax_minus_button = text.get_rect(centerx = x, centery = y)
    DISPLAYSURF.blit(text, Map.tax_minus_button)
    
    text = font.render("+", 1, color)
    x = RESSOURCEBARWIDTH + MENUBARWIDTH - 4*GAPSIZE_MENU
    y = WINDOWHEIGHT - GAPSIZE_MENU - 54
    Map.tax_plus_button = text.get_rect(centerx = x, centery = y)
    DISPLAYSURF.blit(text, Map.tax_plus_button)    
    
    text = font.render(str(tax), 1, color)
    x = RESSOURCEBARWIDTH + 2*GAPSIZE_MENU + MENUBARWIDTH/2
    y = WINDOWHEIGHT - GAPSIZE_MENU - 54
    textpos = text.get_rect(centerx = x, centery = y)
    DISPLAYSURF.blit(text, textpos)    
    
def drawPriorities(Map, DISPLAYSURF, color):
    """ Displays priorities for the repartition of inhabitants 
    in production buildings, ans "+" and "-" buttons. """
    
    for k in range(3):
        text = font.render(str(Map.priority.index(k+2) + 1), 1, color)
        x = RESSOURCEBARWIDTH + MENUBARWIDTH - 8*GAPSIZE_MENU
        y = (k+2)*(GAPSIZE_MENU + BOXSIZE) + RESSOURCEBARHEIGHT \
                                           + 2*GAPSIZE_MENU + BOXSIZE/2
        textpos = text.get_rect(centerx = x, centery = y)
        DISPLAYSURF.blit(text, textpos)
    
        text = font.render("-", 1, color)
        x = RESSOURCEBARWIDTH + MENUBARWIDTH - 12*GAPSIZE_MENU
        y = (k+2)*(GAPSIZE_MENU + BOXSIZE) + RESSOURCEBARHEIGHT \
                                           + 2*GAPSIZE_MENU + BOXSIZE/2
        Map.prio_minus[k] = text.get_rect(centerx = x, centery = y)
        DISPLAYSURF.blit(text, Map.prio_minus[k])
        
        text = font.render("+", 1, color)
        
        x = RESSOURCEBARWIDTH + MENUBARWIDTH - 4*GAPSIZE_MENU
        y = (k+2)*(GAPSIZE_MENU + BOXSIZE) + RESSOURCEBARHEIGHT \
                                           + 2*GAPSIZE_MENU + BOXSIZE/2
        Map.prio_plus[k] = text.get_rect(centerx = x, centery = y)
        DISPLAYSURF.blit(text, Map.prio_plus[k])
        
def drawShortcuts(Map, DISPLAYSURF, color, toBuild):
    for k in range(len(toBuild)):
        text = font.render(Map.shortcuts_str[k], 1, color)
        x = RESSOURCEBARWIDTH + BOXSIZE + 6*GAPSIZE_MENU
        y = k*(GAPSIZE_MENU + BOXSIZE) + RESSOURCEBARHEIGHT + 2*GAPSIZE_MENU \
            + BOXSIZE/2
        textpos = text.get_rect(centerx = x, centery = y)
        DISPLAYSURF.blit(text, textpos)

def drawInfoMenu(DISPLAYSURF, mousex, mousey, buildings):
    """ Draws info bubbles for buildings in the menu bar"""
    p = (mousex - WINDOWWIDTH + MENUBARWIDTH)//(GAPSIZE_MENU + BOXSIZE)
    q = (mousey - RESSOURCEBARHEIGHT - 2*GAPSIZE_MENU)// \
        (GAPSIZE_MENU + BOXSIZE)
    k = int(p)*n + int(q)
    if k < len(buildings) - 1 and k >= 0 :
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
            gap = 0
            for line in text.splitlines():
                img = font_bubble.render(line, 1, BLACK, WHITE)
                x = (k//n)*(GAPSIZE_MENU + BOXSIZE) + WINDOWWIDTH \
                    - MENUBARWIDTH + 35
                y = (k%n)*(GAPSIZE_MENU + BOXSIZE) + RESSOURCEBARHEIGHT \
                    + 2*GAPSIZE_MENU + 5 + gap
                textpos = img.get_rect(centerx = x, centery = y)
                DISPLAYSURF.blit(img, textpos)
                gap += height
    

def drawInfoBoard(DISPLAYSURF, boxx, boxy, mainBoard, buildings):
    """ Draws info bubbles for buildings in the main board"""

    building = mainBoard.map[boxx][boxy]
    text = ""
    jump = False
    if building.cit > 0:
        text += "cit. : "+str(building.cit)
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
        img = font_bubble.render(line, 1, BLACK, WHITE)
        x = GAPSIZE + (BOXSIZE + GAPSIZE)*boxy + 15
        y = RESSOURCEBARHEIGHT + GAPSIZE + (BOXSIZE + GAPSIZE)*boxx + gap
        textpos = img.get_rect(centerx = x, centery = y)
        DISPLAYSURF.blit(img, textpos)
        gap += height


def displayLosingMenu(DISPLAYSURF, FPSCLOCK):
    """When the game is over, displays a message to the player. """
    lost = True
    DISPLAYSURF.fill((0,0,0))
    mouseClicked = False
    
    while lost:
        text = font_title.render("YOU LOST : CLICK TO START AGAIN", 1, RED)
        textposTitle = text.get_rect(centerx = WINDOWWIDTH / 2, 
                                     centery = WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(text, textposTitle)
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            elif event.type == QUIT or (event.type == KEYUP \
                                        and event.key == K_ESCAPE):
                pygame.quit()
                os.sys.exit()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
        if mouseClicked:
            lost = False
