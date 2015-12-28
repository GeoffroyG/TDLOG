# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 15:36:10 2015

@author: Fatma - Geoffroy - Pierre
"""

import Classes_Tests
from Constantes import *
from pygame.locals import *
import os

n = 3 # number of pictures per column in the menu

buildings = [Classes_Tests.Road(), Classes_Tests.House(), 
             Classes_Tests.Factory(), Classes_Tests.Workshop(), 
             Classes_Tests.Empty(), Classes_Tests.Empty(), 
             Classes_Tests.Empty(), Classes_Tests.Empty(), 
             Classes_Tests.Empty(),Classes_Tests.Empty(),
             Classes_Tests.Mine()]
# graphism and buildings are to be modified together, one is the buidings list the other the pictures list

mainBoard = Classes_Tests.Map(NBROW,NBCOLUMN)

def main():
    global FPSCLOCK, DISPLAYSURF, selected, building, graphism, graphism_Selected, toBuild, toBuild_Selected
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    # Initialisation of the clock and the window

    toBuild = [pygame.image.load("2.Images/Road.png").convert(),
               pygame.image.load("2.Images/House.png").convert(),
               pygame.image.load("2.Images/Factory.png").convert(),
               pygame.image.load("2.Images/Workshop.png").convert(),
               pygame.image.load("2.Images/None.png").convert(), 
               pygame.image.load("2.Images/None.png").convert(), 
               pygame.image.load("2.Images/None.png").convert(), 
               pygame.image.load("2.Images/None.png").convert(), 
               pygame.image.load("2.Images/None.png").convert(), 
               pygame.image.load("2.Images/Grass.png").convert()]
            
    toBuild_Selected = [pygame.image.load("2.Images/Road_Selected.png").convert(), 
                        pygame.image.load("2.Images/House_Selected.png").convert(), 
                        pygame.image.load("2.Images/Factory_Selected.png").convert(), 
                        pygame.image.load("2.Images/Workshop_Selected.png").convert(), 
                        pygame.image.load("2.Images/None.png").convert(), 
                        pygame.image.load("2.Images/None.png").convert(), 
                        pygame.image.load("2.Images/None.png").convert(), 
                        pygame.image.load("2.Images/None.png").convert(), 
                        pygame.image.load("2.Images/None.png").convert(), 
                        pygame.image.load("2.Images/Grass_Selected.png").convert()]

    graphism = toBuild + [pygame.image.load("2.Images/Mine.png").convert()]
    graphism_Selected = toBuild_Selected + [pygame.image.load("2.Images/Mine_Selected.png").convert()]

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Jeu Sim City') # name of the game

    origin = [0,0] # coordinates of the top-left cell displayed

    BGCOLOR = (255, 255, 255) # white background
    DISPLAYSURF.fill(BGCOLOR)
    game = False
    rules = False
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
            text = font_other.render("Règles", 1, (10,10,10), (255,255,255))
            textposRules = text.get_rect(centerx = WINDOWWIDTH / 2, centery = WINDOWHEIGHT / 2 + textposNewGame.height)
            DISPLAYSURF.blit(text, textposRules)
        else:
            text = font_other.render("Ceci sont les règles, ça va être coton à tout taper en faisant les sauts de lignes", 1, (10,10,10), (255,255,255))
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


        if textposNewGame.collidepoint(mousex, mousey) and not rules:
            game = True
        elif textposRules.collidepoint(mousex, mousey) and not rules:
            rules = True
        elif posReturn.collidepoint(mousex, mousey) and rules:
            rules = False

        pygame.display.update()
        FPSCLOCK.tick(FPS)


    selected = [False, False, False, False, False, False, False, False, False, False]
    building = Classes_Tests.Empty()

    buildingselected = False
    mouseClicked = False
    # initialisation of the selection variables

    timer = 0 # set of a timer in frames
    timing = 0 # set of a timer in seconds to manipulate production

    roads = [Classes_Tests.Road()]
    roads_coords = [[2,0]]
    
    changes = []
    change_all = False
    
    build = False

    DISPLAYSURF.fill(BGCOLOR) # drawing the window
    drawBoard(mainBoard, DISPLAYSURF, selected, timing, origin)
    drawHeader(mainBoard, DISPLAYSURF)
    drawMenu(mainBoard, DISPLAYSURF, selected, timing)


    while True: # main game loop
    
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            # Shifts on the map
            if event.type == KEYUP and event.key == K_LEFT:
                if origin[1] > 0:
                    origin[1] -= 1
                    change_all = True
            if event.type == KEYUP and event.key == K_RIGHT:
                if origin[1] < NBCOLUMN - NBCOLUMN_DISP:
                    origin[1] += 1
                    change_all = True
            if event.type == KEYUP and event.key == K_UP:
                if origin[0] > 0:
                    origin[0] -= 1
                    change_all = True
            if event.type == KEYUP and event.key == K_DOWN:
                if origin[0] < NBROW - NBROW_DISP:
                    origin[0] += 1
                    change_all = True

        if isInGame(mousex, mousey):
            boxx, boxy = getBoxAtPixelGame(mousex, mousey, origin)

            # Build a new building            
            if boxx != None and boxy != None and mouseClicked and buildingselected:
                build = mainBoard.insert(building, boxx, boxy)

                buildingselected = False
                building = Classes_Tests.Empty()
                selected = [False, False, False, False, False, False, False, False, False, False]
                
                changes.append([boxx, boxy])

            # Display House data
            if  getType(mainBoard, boxx, boxy) == 1:
                text = font_bubble.render("Habitants : "+str(mainBoard.map[boxx][boxy].hab), 1, (10,10,10),(255,255,255))
                textpos = text.get_rect(centerx=GAPSIZE + (BOXSIZE+GAPSIZE)*boxy+30, centery=RESSOURCEBARHEIGHT + GAPSIZE + (BOXSIZE+GAPSIZE)*boxx)
                DISPLAYSURF.blit(text, textpos)

                
            # Display Factory data
            elif getType(mainBoard, boxx, boxy) == 2:
                text="Employes : "+str(mainBoard.map[boxx][boxy].worker)+" \n "+"Production : "+str(int(mainBoard.map[boxx][boxy].prod_max * mainBoard.map[boxx][boxy].worker / mainBoard.map[boxx][boxy].hab_max))
                height = font_bubble.get_height()*1
                gap=0
                for line in text.splitlines():
                    img = font_bubble.render(line,1,(10,10,10),(255,255,255))
                    textpos = img.get_rect(centerx=GAPSIZE + (BOXSIZE+GAPSIZE)*boxy+30, centery=RESSOURCEBARHEIGHT + GAPSIZE + (BOXSIZE+GAPSIZE)*boxx+gap)
                    DISPLAYSURF.blit(img,textpos)
                    gap += height
            


        if isInMenu(mousex):
            # Select a building in the menu
            if mouseClicked and getBuildingFromMenu(mousex, mousey, selected) != None:
                buildingselected = True
                building = getBuildingFromMenu(mousex, mousey, selected)

        # Reinitialization of the parameters after
        boxx, boxy = None, None
        mouseClicked = False
        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        # Increase of the newcomers
        mainBoard.habitants = 0
        for i in range(NBROW):
            for j in range(NBCOLUMN):
                if  getType(mainBoard, i, j) == 1:
                    mainBoard.map[i][j].hab_cond = mainBoard.map[i][j].hab_max - mainBoard.check_junction(2,i,j)
                    mainBoard.map[i][j].moving(timer)
                    mainBoard.habitants += mainBoard.map[i][j].hab

        # This is not the most efficient as it focuses more on the first factories built
        worker_aux = mainBoard.habitants
        for i in range(NBROW):
            for j in range(NBCOLUMN):
                if  getType(mainBoard, i, j) == 2:
                    while worker_aux > 0:
                        mainBoard.map[i][j].worker = min(worker_aux,mainBoard.map[i][j].hab_max)
                        worker_aux -= mainBoard.map[i][j].worker
                        mainBoard.wood += mainBoard.map[i][j].production(timer)

        # Increase of the timer
        timer += 1
        timing = timer // FPS

        drawBoard_changes(mainBoard, DISPLAYSURF, selected, timing, origin, changes, change_all)
        drawHeader(mainBoard, DISPLAYSURF)
        drawMenu(mainBoard, DISPLAYSURF, selected, timing)


def getBoxAtPixelGame(mousex, mousey, origin):
    ''' Translates the coordinates in the game from pixels to integers. '''
    i = origin[0] + ((mousey - RESSOURCEBARHEIGHT) / GAMEHEIGHT * NBROW_DISP)
    j = origin[1] + (mousex / GAMEWIDTH * NBCOLUMN_DISP)
    return(int(i),int(j))

def getBuildingFromMenu(mousex, mousey, selected):
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


def drawBoard(Map, DISPLAYSURF, selected, timing, origin):
    ''' Displays the entire board. '''

    # We display each box with the picture attached to it
    for i in range(NBROW_DISP):
        for j in range(NBCOLUMN_DISP):
            p = Map.map[origin[0]+i][origin[1]+j].type
            dessin = graphism[p]
            DISPLAYSURF.blit(dessin, (GAPSIZE + (BOXSIZE+GAPSIZE)*j, RESSOURCEBARHEIGHT + GAPSIZE + (BOXSIZE+GAPSIZE)*i))


def drawBoard_changes(Map, DISPLAYSURF, selected, timing, origin, changes, change_all):
    ''' Displays the entire board. '''
 
    if change_all == True:
        drawBoard(Map, DISPLAYSURF, selected, timing, origin)
    
    else:
        if len(changes) != 0:
            for k in range(len(changes)):
                if changes[k][0] >= origin[0] and changes[k][0] < origin[0] + NBROW_DISP and changes[k][1] >= origin[1] and changes[k][1] < origin[1] + NBCOLUMN_DISP:
                    i = changes[k][0] - origin[0]
                    j = changes[k][1] - origin[1]                    
                    p = Map.map[origin[0]+changes[k][0]][origin[1]+changes[k][1]].type
                    dessin = graphism[p]
                    DISPLAYSURF.blit(dessin, (GAPSIZE + (BOXSIZE+GAPSIZE)*j, RESSOURCEBARHEIGHT + GAPSIZE + (BOXSIZE+GAPSIZE)*i))


def drawHeader(Map, DISPLAYSURF):
    # Then we display the ressources
    ressources = "Wood : "+str(Map.wood)+"   Habitants : "+str(Map.habitants)
    text = font.render(ressources, 1, (10,10,10))
    textpos = text.get_rect(centerx=RESSOURCEBARWIDTH/2,centery=GAPSIZE+RESSOURCEBARHEIGHT/2)
    DISPLAYSURF.blit(text, textpos)

def drawMenu(Map, DISPLAYSURF, selected, timing):
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

