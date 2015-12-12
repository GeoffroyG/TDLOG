# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 22:13:40 2015

@author: Pierre
"""

import Classes_Tests, pygame, sys
from pygame.locals import *

pygame.font.init()

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

n = 3 # number of pictures per column in the menu

Graphism = ["Road.png", "House.png", "Factory.png", "None.png", "None.png", "None.png", "None.png", "None.png", "None.png", "Grass.png"]
Buildings = [Classes_Tests.Road(), Classes_Tests.House(), Classes_Tests.Factory(), Classes_Tests.Empty(), Classes_Tests.Empty(), Classes_Tests.Empty(), Classes_Tests.Empty(), Classes_Tests.Empty(), Classes_Tests.Empty(), Classes_Tests.Empty()]
# Graphism and Buildings are to be modified together, one is the buidings list the other the pictures list

mainBoard = Classes_Tests.Map(BOARDHEIGHT,BOARDWIDTH)
font = pygame.font.Font(None, 24)
MenuCoordinates = [(WINDOWWIDTH-GAPSIZE-MENUBARWIDTH,GAPSIZE),(WINDOWWIDTH-GAPSIZE-MENUBARWIDTH,WINDOWHEIGHT-GAPSIZE),(WINDOWWIDTH-GAPSIZE,WINDOWHEIGHT-GAPSIZE),(WINDOWWIDTH-GAPSIZE,GAPSIZE)]
# Initialisation of many variables that are useful later

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    # Initialisation of the clock and the window

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Jeu Test') # name of the game


    BGCOLOR = (255, 255, 255) # white background
    DISPLAYSURF.fill(BGCOLOR)
    
    buildingSelected = False
    building = Classes_Tests.Empty()  # initialisation of the two selection variables   
    
    timing = 0 # set of a timer to manipulate production
    Factories = [] # preparation of a list to store the factories for production

    while True: # main game loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(mainBoard, DISPLAYSURF)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
                
        
        if isInGame(mousex, mousey):
            boxx, boxy = getBoxAtPixelGame(mousex, mousey)
            # If we're in the game, the coordinates represent a box and we have selected a building
            if boxx != None and boxy != None and mouseClicked and buildingSelected:
                mainBoard.insert(building, boxx, boxy)
                # We create that building and reinitialize the parameters used (the tests are already in insert)
                if building.type == 2:
                    # If we are building a factory   
                    building.time = timing-1
                    Factories.append(building)
                buildingSelected = False
                building = Classes_Tests.Empty()
        
        if isInMenu(mousex):
            # Step to select a building in the menu
            if mouseClicked and getBuildingFromMenu(mousex, mousey) != None:
                buildingSelected = True
                building = getBuildingFromMenu(mousex, mousey)
        
        # Reinitialization of the parameters after
        boxx, boxy = None, None
        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        # Use of an auxiliary variable to check on the workers available
        # This is not the most efficient as it focuses more on the first Factories built
        worker_aux = mainBoard.habitants
        if Factories != []:
            i = 0
            while i < len(Factories) and worker_aux > 0:
                worker = min(worker_aux,Factories[i].hab_max)
                mainBoard.wood += Factories[i].production(worker, timing)
                worker_aux -= worker
        # Increase of the timer
        timing += 1
        

def getBoxAtPixelGame(mousex, mousey):
    # Translates the coordinates in the game from pixels to integers
    j = mousex / GAMEWIDTH * BOARDWIDTH
    i = (mousey - RESSOURCEBARHEIGHT) / GAMEHEIGHT * BOARDHEIGHT
    return(int(i),int(j))
    
def getBuildingFromMenu(mousex, mousey):
    # Gives the building from the coordinates in the menu (see drawBoard)
    p = (mousex-WINDOWWIDTH+MENUBARWIDTH)//(GAPSIZE+BOXSIZE)
    q = (mousey-RESSOURCEBARHEIGHT-2*GAPSIZE)//(GAPSIZE+BOXSIZE)
    k = int(p)*n+int(q)
    if k>=0 and k<10:
        return(Buildings[k])
    else:
        return(None)
    

def drawBoard(Map, DISPLAYSURF):
    # First we translate the map matrix into a types matrix
    Matrix = Map.types()
    # Then we display each box with the picture attached to it
    # Check how we can manage to win time by only displaying the changes
    for i in range(BOARDHEIGHT):
        for j in range(BOARDWIDTH):
            p = Matrix[i][j]
            file = Graphism[p]
            dessin = pygame.image.load(file).convert()
            DISPLAYSURF.blit(dessin, (GAPSIZE + (BOXSIZE+GAPSIZE)*j, RESSOURCEBARHEIGHT + GAPSIZE + (BOXSIZE+GAPSIZE)*i))
    # Then we display the ressources
    Ressources = "Wood : "+str(Map.wood)+"   Habitants : "+str(Map.habitants)
    text = font.render(Ressources, 1, (10,10,10))
    textpos = text.get_rect(centerx=RESSOURCEBARWIDTH/2)
    DISPLAYSURF.blit(text, textpos)
    # We draw the background for the menu (I don't know why we have to do this step everytime but else it erases)
    pygame.draw.polygon(DISPLAYSURF, (139,69,19), MenuCoordinates)
    # And finally all the things that are on said menu
    text = font.render("Menu", 1, (10,10,10))
    textpos = text.get_rect(centerx=RESSOURCEBARWIDTH+2*GAPSIZE + MENUBARWIDTH/2)
    DISPLAYSURF.blit(text, textpos)
    # For the pictures of the buildings we can change n to print more buildings in height, I haven't thought of a formula that would depend on the window length
    i=0
    for k in Graphism:
        dessin = pygame.image.load(k).convert()
        # The formula is more understandable in this order, but it's the same than in detBuildingFromMenu actually 
        x = (i//n)*(GAPSIZE+BOXSIZE)+WINDOWWIDTH-MENUBARWIDTH
        y = (i%n)*(GAPSIZE+BOXSIZE)+RESSOURCEBARHEIGHT+2*GAPSIZE
        DISPLAYSURF.blit(dessin,(x,y))
        i+=1

    
    

def isInMenu(mousex):
    # returns True if the mouse is in the menu
    if mousex > WINDOWWIDTH - MENUBARWIDTH:
        return(True)
    else:
        return(False)

def isInGame(mousex, mousey):
    # returns True if the mouse is in the game
    if mousex < GAMEWIDTH + 2*GAPSIZE and mousey > RESSOURCEBARHEIGHT + 2*GAPSIZE:
        return(True)
    else:
        return(False)

    
if __name__ == '__main__':
    main()
