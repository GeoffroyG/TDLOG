# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 21:18:54 2016

@author: Pierre
"""

from Graphismes_test import *


buildings = [Classes_Tests.Road(), Classes_Tests.House(),
             Classes_Tests.Factory(), Classes_Tests.Quarry(),
             Classes_Tests.Wind_power_plant(), Classes_Tests.Coal_power_plant(),
             Classes_Tests.Nuclear_power_plant(), Classes_Tests.Hydraulic_power_plant(),
             Classes_Tests.Sawmill(),Classes_Tests.Empty(),
             Classes_Tests.Mine(), Classes_Tests.Forest()]
# graphism and buildings are to be modified together, one is the buidings list the other the pictures list

mainBoard = Classes_Tests.Map(NBROW,NBCOLUMN)

def main():
    global FPSCLOCK, DISPLAYSURF, selected, building, graphism, graphism_Selected, toBuild, toBuild_Selected, timer,graph_priority
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    happiness = 1
    # Initialisation of the clock and the window

    toBuild = [pygame.image.load("2.Images/Road.png").convert(),
               pygame.image.load("2.Images/House.png").convert(),
               pygame.image.load("2.Images/Factory.png").convert(),
               pygame.image.load("2.Images/Quarry.png").convert(),
               pygame.image.load("2.Images/Wind.png").convert(),
               pygame.image.load("2.Images/Coal.png").convert(),
               pygame.image.load("2.Images/Nuclear.png").convert(),
               pygame.image.load("2.Images/Hydraulic.png").convert(),
               pygame.image.load("2.Images/Sawmill.png").convert(),
               pygame.image.load("2.Images/Grass.png").convert()]
               
    toBuild_Selected = [pygame.image.load("2.Images/Road_Selected.png").convert(),
                        pygame.image.load("2.Images/House_Selected.png").convert(),
                        pygame.image.load("2.Images/Factory_Selected.png").convert(),
                        pygame.image.load("2.Images/Quarry_Selected.png").convert(),
                        pygame.image.load("2.Images/Wind_Selected.png").convert(),
                        pygame.image.load("2.Images/Coal_Selected.png").convert(),
                        pygame.image.load("2.Images/Nuclear_Selected.png").convert(),
                        pygame.image.load("2.Images/Hydraulic_Selected.png").convert(),
                        pygame.image.load("2.Images/Sawmill_Selected.png").convert(),
                        pygame.image.load("2.Images/Grass_Selected.png").convert()]
                        
    graph_priority = [pygame.image.load("2.Images/plus.png").convert(),
                      pygame.image.load("2.Images/plus.png").convert(),
                      pygame.image.load("2.Images/plus.png").convert(),
                      pygame.image.load("2.Images/1.png").convert(),
                      pygame.image.load("2.Images/2.png").convert(),
                      pygame.image.load("2.Images/3.png").convert(),
                      pygame.image.load("2.Images/moins.png").convert(),
                      pygame.image.load("2.Images/moins.png").convert(),
                      pygame.image.load("2.Images/moins.png").convert()]
               
    graphism = toBuild + [pygame.image.load("2.Images/Mine.png").convert()] + [pygame.image.load("2.Images/Forest.png").convert()]
    graphism_Selected = toBuild_Selected + [pygame.image.load("2.Images/Mine_Selected.png").convert()] + [pygame.image.load("2.Images/Forest_Selected.png").convert()]

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
    
    priority = [2,3,8]


    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                os.sys.exit()

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
                build = mainBoard.insert(building, boxx, boxy, timer)
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
        for k in mainBoard.built:
            if len(k) > 0:
                i, j = k[0], k[1]
                if  getType(mainBoard, i, j) == 1:
                    mainBoard.habitants += mainBoard.map[i][j].moving(timer)
        
        if timer % PRODSTEP == 0:
            production(mainBoard, priority, buildings)

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
        drawHappiness(DISPLAYSURF,happiness,0,0,BOXSIZE)
        #happiness -= 0.01
        
def production(mainBoard, priority, buildings):
    workers_needed = [0 for i in range(len(priority))]
    wood_needed = [0 for i in range(len(priority))]
    number = [0 for i in range(len(priority))]
    for i in range(NBROW):
        for j in range(NBCOLUMN):
            bat = mainBoard.map[i][j] 
            if bat.type in priority:
                workers_needed[priority.index(bat.type)] += bat.hab_max
                wood_needed[priority.index(bat.type)] += bat.wood_input
                number[priority.index(bat.type)] += 1
    workers_remaining = mainBoard.habitants
    k = 0
    while k < len(priority) and workers_remaining > 0:
        
        workers_assigned = min(workers_needed[k],workers_remaining)
        if workers_needed[k] == 0:
            proportion_worker = 1
        else:
            proportion_worker = workers_assigned / workers_needed[k]
            
        wood_used = min(wood_needed[k],mainBoard.wood)
        if wood_needed[k] == 0:
            proportion_wood = 1
        else:
            proportion_wood = wood_used / wood_needed[k]
        
        mainBoard.wood += buildings[priority[k]].wood_output * min(proportion_worker,proportion_wood) * number[k]
        mainBoard.money += buildings[priority[k]].money_output * min(proportion_worker,proportion_wood) * number[k] 
        mainBoard.stone += buildings[priority[k]].stone_output * min(proportion_worker,proportion_wood) * number[k] 
        mainBoard.wood -= wood_used
        
        workers_remaining -= workers_assigned
        k += 1
        
                

