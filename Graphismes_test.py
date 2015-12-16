# -*- coding: utf-8 -*-


import Classes_Tests
from Constantes import *
from pygame.locals import *

n = 3 # number of pictures per column in the menu

Buildings = [Classes_Tests.Road(), Classes_Tests.House(), Classes_Tests.Factory(), Classes_Tests.Empty(), Classes_Tests.Empty(), Classes_Tests.Empty(), Classes_Tests.Empty(), Classes_Tests.Empty(), Classes_Tests.Empty(), Classes_Tests.Empty()]
# Graphism and Buildings are to be modified together, one is the buidings list the other the pictures list

mainBoard = Classes_Tests.Map(BOARDHEIGHT,BOARDWIDTH)

def main():
    global FPSCLOCK, DISPLAYSURF, Selected, building
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    # Initialisation of the clock and the window

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Jeu Test') # name of the game
    
    BGCOLOR = (255, 255, 255) # white background
    DISPLAYSURF.fill(BGCOLOR)
    game = False
    Rules = False
    posReturn = pygame.Rect(0,0,0,0)
    
    while not game:
        background = pygame.image.load("2.Images/Backgroundimage.jpg").convert()
        pygame.transform.scale(background, (WINDOWWIDTH, WINDOWHEIGHT))
        DISPLAYSURF.blit(background, (0,0))
        text = font_title.render("Simulation de ville 2D", 1, (255, 0, 0))
        textposTitle = text.get_rect(centerx = WINDOWWIDTH / 2, centery = 50)
        DISPLAYSURF.blit(text, textposTitle)
        if not Rules:
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
                sys.exit() 
        
        
        if textposNewGame.collidepoint(mousex, mousey) and not Rules:
            game = True
        elif textposRules.collidepoint(mousex, mousey) and not Rules:
            Rules = True
        elif posReturn.collidepoint(mousex, mousey) and Rules:
            Rules = False
            
        pygame.display.update()
        FPSCLOCK.tick(FPS)



    Selected = [False, False, False, False, False, False, False, False, False, False]
    building = Classes_Tests.Empty()
    
    buildingSelected = False
    mouseClicked = False
    # initialisation of the selection variables   
    
    timer = 0 # set of a timer in frames
    timing = 0 # set of a timer in seconds to manipulate production
    Factories = [] # preparation of a list to store the factories for production
    Factories_coords = []    
    Houses = [] # same for the houses
    Houses_coords = [] # useful to keep coordinates as hab max depend on the proximity of Factories
    Roads = [Classes_Tests.Road()]
    Roads_coords = [[2,0]]
    build = False


    while True: # main game loop

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(mainBoard, DISPLAYSURF, Selected, timing)
                
                
        for event in pygame.event.get(): # event handling loop        
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()        
        
        
        if isInGame(mousex, mousey):
            boxx, boxy = getBoxAtPixelGame(mousex, mousey)
            # If we're in the game, the coordinates represent a box and we have selected a building
            if boxx != None and boxy != None and mouseClicked and buildingSelected:
                build = mainBoard.insert(building, boxx, boxy)
                if build:
                    if building.type == 0:
                        building = Classes_Tests.Road()
                        building.time = timer - 1
                        Roads.append(building)
                        Roads_coords.append([boxx,boxy])
                        # We create that building and reinitialize the parameters used (the tests are already in insert)
                    if building.type == 1:
                        building = Classes_Tests.House()
                        building.time = timer-1
                        Houses.append(building)
                        Houses_coords.append([boxx,boxy])
                    if building.type == 2:
                        # If we are building a factory
                        building = Classes_Tests.Factory()
                        building.time = timer-1
                        Factories.append(building)
                        Factories_coords.append([boxx,boxy])
                    if building.type == 9:
                        remove([Roads, Roads_coords, Houses, Houses_coords, Factories, Factories_coords], boxx, boxy)
                        mainBoard.delete(boxx, boxy)
                    
                buildingSelected = False
                building = Classes_Tests.Empty()
                Selected = [False, False, False, False, False, False, False, False, False, False]
            if  [boxx,boxy] in  Houses_coords:
                index= Houses_coords.index([boxx,boxy])
                text = font.render("Habitants : "+str(Houses[index].hab), 1, (10,10,10))
                textpos = text.get_rect()
                DISPLAYSURF.blit(text, textpos)
            elif [boxx,boxy] in  Factories_coords:
                index= Factories_coords.index([boxx,boxy])
                text="Employes : "+str(Factories[index].worker)+" \n "+"Production : "+str(int(Factories[index].prod_max * Factories[index].worker / Factories[index].hab_max))
                height = font.get_height()*1.3
                x,y = 0,0
                for line in text.splitlines():
                    img = font.render(line,1,(10,10,10))
                    DISPLAYSURF.blit(img,(x,y))
                    y += height
                #text = font.render("employes : "+str(Factories[index].worker)+" \n "+"production : "+str(int(Factories[index].prod_max * Factories[index].worker / Factories[index].hab_max)), 1, (10,10,10))
                #textpos = text.get_rect()
                #DISPLAYSURF.blit(text, textpos)
    
        if isInMenu(mousex):
            # Step to select a building in the menu
            if mouseClicked and getBuildingFromMenu(mousex, mousey, Selected) != None:
                buildingSelected = True
                building = getBuildingFromMenu(mousex, mousey, Selected)
        
        # Reinitialization of the parameters after
        boxx, boxy = None, None
        mouseClicked = False
        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        # Increase of the newcomers
        habitants_aux = 0
        if Houses != []:
            for i in range(len(Houses)):
                p = mainBoard.check_junction(2,Houses_coords[i][0], Houses_coords[i][1])
                Houses[i].hab_cond = Houses[i].hab_max - p
                Houses[i].moving(timer)
                habitants_aux += Houses[i].hab
        mainBoard.habitants = habitants_aux
        # Use of an auxiliary variable to check on the workers available
        # This is not the most efficient as it focuses more on the first Factories built
        worker_aux = mainBoard.habitants
        if Factories != []:
            i = 0
            while i < len(Factories) and worker_aux > 0:
                Factories[i].worker = min(worker_aux,Factories[i].hab_max)
                mainBoard.wood += Factories[i].production(timer)
                worker_aux -= Factories[i].worker
                i+=1 # increment to go through all factories  
        # Increase of the timer
        timer += 1
        timing = timer // FPS


def getBoxAtPixelGame(mousex, mousey):
    # Translates the coordinates in the game from pixels to integers
    j = mousex / GAMEWIDTH * BOARDWIDTH
    i = (mousey - RESSOURCEBARHEIGHT) / GAMEHEIGHT * BOARDHEIGHT
    return(int(i),int(j))
    
def getBuildingFromMenu(mousex, mousey, Selected):
    # Gives the building from the coordinates in the menu (see drawBoard)
    p = (mousex-WINDOWWIDTH+MENUBARWIDTH)//(GAPSIZE+BOXSIZE)
    q = (mousey-RESSOURCEBARHEIGHT-2*GAPSIZE)//(GAPSIZE+BOXSIZE)
    k = int(p)*n+int(q)
    if k>=0 and k<10:
        for i in range(len(Selected)):
            Selected[i] = False
        Selected[k] = True
        return(Buildings[k])
    else:
        return(None)
        
def getType(Map, boxx, boxy):
    Matrix = Map.types()
    return(Matrix[boxx][boxy])
    
def remove(list_types_coords, boxx, boxy):
    # The list is organized this way : [Building A, Building Coords A, Building B...]
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
        

def drawBoard(Map, DISPLAYSURF, Selected, timing):
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
    textpos = text.get_rect(centerx=RESSOURCEBARWIDTH/2,centery=GAPSIZE+RESSOURCEBARHEIGHT/2)
    DISPLAYSURF.blit(text, textpos)
    # We draw the background for the menu (I don't know why we have to do this step everytime but else it erases)
    pygame.draw.polygon(DISPLAYSURF, (139,69,19), MenuCoordinates)
    # And finally all the things that are on said menu
    text = font.render("Menu", 1, (10,10,10))
    textpos = text.get_rect(centerx=RESSOURCEBARWIDTH+2*GAPSIZE + MENUBARWIDTH/2, centery=GAPSIZE+RESSOURCEBARHEIGHT/2)
    DISPLAYSURF.blit(text, textpos)
    text = font.render("Time : "+str(timing), 1, (10,10,10))
    textpos = text.get_rect(centerx=RESSOURCEBARWIDTH+2*GAPSIZE + MENUBARWIDTH/2, centery=WINDOWHEIGHT-GAPSIZE-24/2)
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
    i=0
    for k in Selected:
        if k:
            graph = Graphism_Selected[i]           
            dessin = pygame.image.load(graph).convert()
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

    
