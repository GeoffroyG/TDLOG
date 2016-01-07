# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 21:18:54 2016

@author: Pierre
"""

from Graphismes_test import *


buildings = [Classes_Tests.Road(), Classes_Tests.House(), 
             Classes_Tests.Factory(), Classes_Tests.Workshop(), 
             Classes_Tests.Wind_power_plant(), Classes_Tests.Coal_power_plant(), 
             Classes_Tests.Nuclear_power_plant(), Classes_Tests.Hydraulic_power_plant(), 
             Classes_Tests.Empty(),Classes_Tests.Empty(),
             Classes_Tests.Mine()]
# graphism and buildings are to be modified together, one is the buidings list the other the pictures list

mainBoard = Classes_Tests.Map(NBROW,NBCOLUMN)

def main():
    global FPSCLOCK, DISPLAYSURF, selected, building, graphism, graphism_Selected, toBuild, toBuild_Selected
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    happiness = 1
    # Initialisation of the clock and the window

    toBuild = [pygame.image.load("2.Images/Road.png").convert(),
               pygame.image.load("2.Images/House.png").convert(),
               pygame.image.load("2.Images/Factory.png").convert(),
               pygame.image.load("2.Images/Workshop.png").convert(),
               pygame.image.load("2.Images/Wind.png").convert(), 
               pygame.image.load("2.Images/Coal.png").convert(), 
               pygame.image.load("2.Images/Nuclear.png").convert(), 
               pygame.image.load("2.Images/Hydraulic.png").convert(), 
               pygame.image.load("2.Images/None.png").convert(), 
               pygame.image.load("2.Images/Grass.png").convert()]
            
    toBuild_Selected = [pygame.image.load("2.Images/Road_Selected.png").convert(), 
                        pygame.image.load("2.Images/House_Selected.png").convert(), 
                        pygame.image.load("2.Images/Factory_Selected.png").convert(), 
                        pygame.image.load("2.Images/Workshop_Selected.png").convert(), 
                        pygame.image.load("2.Images/Wind_Selected.png").convert(), 
                        pygame.image.load("2.Images/Coal_Selected.png").convert(), 
                        pygame.image.load("2.Images/Nuclear_Selected.png").convert(), 
                        pygame.image.load("2.Images/Hydraulic_Selected.png").convert(), 
                        pygame.image.load("2.Images/None.png").convert(), 
                        pygame.image.load("2.Images/Grass_Selected.png").convert()]


    graphism = toBuild + [pygame.image.load("2.Images/Mine.png").convert()]
    graphism_Selected = toBuild_Selected + [pygame.image.load("2.Images/Mine_Selected.png").convert()]

    pygame.display.set_caption('Jeu Sim City') # name of the game

    DISPLAYSURF.fill(BGCOLOR)

    
    displayBeginningMenu(DISPLAYSURF, FPSCLOCK, font_title)


    selected = [False, False, False, False, False, False, False, False, False, False]
    building = Classes_Tests.Empty()

    buildingselected = False
    mouseClicked = False
    # initialisation of the selection variables
        
    changes = []
    change_all = False
    
    build = False

    timer = 0 # set of a timer in frames
    timing = 0 # set of a timer in seconds to manipulate production

    origin = [0,0] # coordinates of the top-left cell displayed
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    

    DISPLAYSURF.fill(BGCOLOR) # drawing the window
    drawBoard(mainBoard, DISPLAYSURF, selected, timing, origin, graphism)
    drawHeader(mainBoard, DISPLAYSURF)
    drawMenu(mainBoard, DISPLAYSURF, selected, timing, toBuild, toBuild_Selected)


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
                if build:
                    changes.append([boxx, boxy])
                
            drawInfoBoard(DISPLAYSURF, boxx, boxy, mainBoard)
            


        if isInMenu(mousex):
            
            # Select a building in the menu
            if mouseClicked and getBuildingFromMenu(mousex, mousey, selected, buildings) != None:
                buildingselected = True
                building = getBuildingFromMenu(mousex, mousey, selected, buildings)                                                       
            
            drawInfoMenu(DISPLAYSURF, mousex, mousey, buildings)


        # Reinitialization of the parameters after
        boxx, boxy = None, None
        mouseClicked = False
        # Increase of the newcomers
#        mainBoard.habitants = 0
#        for i in range(NBROW):
#            for j in range(NBCOLUMN):
#                if  getType(mainBoard, i, j) == 1:
#                    mainBoard.map[i][j].hab_cond = mainBoard.map[i][j].hab_max - mainBoard.check_junction(2,i,j)
#                    mainBoard.map[i][j].moving(timer)
#                    mainBoard.habitants += mainBoard.map[i][j].hab
#
#        # This is not the most efficient as it focuses more on the first factories built
#        worker_aux = mainBoard.habitants
#        for i in range(NBROW):
#            for j in range(NBCOLUMN):
#                if  getType(mainBoard, i, j) == 2:
#                    while worker_aux > 0:
#                        mainBoard.map[i][j].worker = min(worker_aux,mainBoard.map[i][j].hab_max)
#                        worker_aux -= mainBoard.map[i][j].worker
#                        mainBoard.wood += mainBoard.map[i][j].production(timer)
#                        mainBoard.money += mainBoard.map[i][j].production(timer) * mainBoard.map[i][j].VA / mainBoard.map[i][j].prod_max                   


        mainBoard.capacity_electricity = 0
        mainBoard.global_demand_elec = 0
        for i in range(NBROW):
            for j in range(NBCOLUMN):
                if  getType(mainBoard, i, j) in [4,5,6,7]:
                    mainBoard.capacity_electricity += mainBoard.map[i][j].capacity
                    
        mainBoard.available_electricity = mainBoard.capacity_electricity
        for i in range(NBROW):
            for j in range(NBCOLUMN):
                if  getType(mainBoard, i, j) in [1,2,3]:
                    mainBoard.global_demand_elec += mainBoard.map[i][j].elec_consumption
                    if mainBoard.map[i][j].elec_consumption <= mainBoard.available_electricity:
                        mainBoard.available_electricity -= mainBoard.map[i][j].elec_consumption
                        mainBoard.map[i][j].real_consumption = mainBoard.map[i][j].elec_consumption
                    
                    
        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        # Increase of the timer
        timer += 1
        timing = timer // FPS

        
        #drawBoard(mainBoard, DISPLAYSURF, selected, timing, origin, graphism)
        drawBoard_changes(mainBoard, DISPLAYSURF, selected, timing, origin, graphism, changes, change_all)
        drawHeader(mainBoard, DISPLAYSURF)
        drawMenu(mainBoard, DISPLAYSURF, selected, timing, toBuild, toBuild_Selected)
        #drawHappiness(DISPLAYSURF,happiness,0,0,BOXSIZE)
        #happiness -= 0.01
        
