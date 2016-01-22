# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 21:18:54 2016

@author: Fatma - Geoffroy - Pierre
"""

from Graphismes_test import *


buildings = [Classes_Tests.Road(), Classes_Tests.House(),
             Classes_Tests.Factory(), Classes_Tests.Quarry(),
             Classes_Tests.Sawmill(), Classes_Tests.Wind_power_plant(),
             Classes_Tests.Coal_power_plant(), Classes_Tests.Park(),
             Classes_Tests.ENPC(),Classes_Tests.Empty(),
             Classes_Tests.Mine(), Classes_Tests.Forest()]
# graphism and buildings are to be modified together, one is the buidings list the other the pictures list


def main():
    global FPSCLOCK, DISPLAYSURF, selected, building, graphism, graphism_Selected, toBuild, toBuild_Selected, timer, tax
    pygame.init()

    # Initialisation of the clock and the window
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    # Load images
    toBuild = [pygame.image.load("2.Images/Road.png").convert(),
               pygame.image.load("2.Images/House.png").convert(),
               pygame.image.load("2.Images/Factory.png").convert(),
               pygame.image.load("2.Images/Quarry.png").convert(),
               pygame.image.load("2.Images/Sawmill.png").convert(),
               pygame.image.load("2.Images/Wind.png").convert(),
               pygame.image.load("2.Images/Coal.png").convert(),
               pygame.image.load("2.Images/Park.png").convert(),
               pygame.image.load("2.Images/ENPC.png").convert(),
               pygame.image.load("2.Images/Grass.png").convert()]

    toBuild_Selected = [pygame.image.load("2.Images/Road_Selected.png").convert(),
                        pygame.image.load("2.Images/House_Selected.png").convert(),
                        pygame.image.load("2.Images/Factory_Selected.png").convert(),
                        pygame.image.load("2.Images/Quarry_Selected.png").convert(),
                        pygame.image.load("2.Images/Sawmill_Selected.png").convert(),
                        pygame.image.load("2.Images/Wind_Selected.png").convert(),
                        pygame.image.load("2.Images/Coal_Selected.png").convert(),
                        pygame.image.load("2.Images/Park_Selected.png").convert(),
                        pygame.image.load("2.Images/ENPC_Selected.png").convert(),
                        pygame.image.load("2.Images/Grass_Selected.png").convert()]

    # "Graphism" is the extension of "toBuild" with elements that can not be built.
    # This distinction will be useful in the display of the menu.
    graphism = toBuild + [pygame.image.load("2.Images/Mine.png").convert()] + [pygame.image.load("2.Images/Forest.png").convert()]
    graphism_Selected = toBuild_Selected + [pygame.image.load("2.Images/Mine_Selected.png").convert()] + [pygame.image.load("2.Images/Forest_Selected.png").convert()]

    pygame.display.set_caption('Jeu Sim City') # name of the game

    DISPLAYSURF.fill(BGCOLOR)

    while True:

        # Display of a beginning menu and wait for the player to start the game
        displayBeginningMenu(DISPLAYSURF, FPSCLOCK, font_title)

        # Initialization of main board
        mainBoard = Classes_Tests.Map(NBROW,NBCOLUMN)

        tax = TAXMIN
        timer_aux = 0
        color = (0,0,0)

        selected = [False, False, False, False, False, False, False, False, False, False]
        building = Classes_Tests.Empty()

        # Initialisation of the selection variables
        buildingselected = False
        mouseClicked = False

        # Initialisation of game variables
        changes = []
        change_all = True
        build = False
        game = True
        danger = False

        timer = 0 # timer in FPS
        timing = timer // FPS # timer in seconds

        origin = [0,0] # coordinates of the top-left cell displayed
        mousex = 0 # used to store x coordinate of mouse event
        mousey = 0 # used to store y coordinate of mouse event

        # Draw the main window for the first time
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard, DISPLAYSURF, selected, timing, origin, graphism)
        drawHeader(mainBoard, DISPLAYSURF)
        drawMenu(mainBoard, DISPLAYSURF, selected, timing, toBuild, toBuild_Selected, color, tax)

        # Initial priorities for worker repartition into buildings        
        priority = [2,3,4]

        # Main game loop
        while game:
            build = False
            # Event handling loop
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mousex, mousey = event.pos
                    mouseClicked = True
                elif event.type == MOUSEBUTTONUP and event.button == 1:
                    mousex, mousey = event.pos
                    mouseClicked = False
                elif event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
                    if event.buttons[0] == 1:
                        mouseClicked = True
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
                    build = mainBoard.insert(building, boxx, boxy)
                    if build:
                        changes.append([boxx, boxy])
                if boxx != None and boxy != None and not(mouseClicked) and buildingselected and build:
                    buildingselected = False
                    building = Classes_Tests.Empty()
                    selected = [False, False, False, False, False, False, False, False, False, False]

                drawInfoBoard(DISPLAYSURF, boxx, boxy, mainBoard, buildings)



            if isInMenu(mousex):

                # Select a building in the menu
                if mouseClicked and getBuildingFromMenu(mousex, mousey, selected, buildings) != None:
                    buildingselected = True
                    building = getBuildingFromMenu(mousex, mousey, selected, buildings)

                drawInfoMenu(DISPLAYSURF, mousex, mousey, buildings)

                if mouseClicked and mainBoard.tax_plus_button.collidepoint(mousex, mousey):
                    tax = increase_taxes(tax)
                    drawMenu(mainBoard, DISPLAYSURF, selected, timing, toBuild, toBuild_Selected, color, tax)
                
                if mouseClicked and mainBoard.tax_minus_button.collidepoint(mousex, mousey):
                    tax = decrease_taxes(tax)
                    drawMenu(mainBoard, DISPLAYSURF, selected, timing, toBuild, toBuild_Selected, color, tax)

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

            if timer % HAPPINESSSTEP == 0:
                happiness_calc(mainBoard, tax)
                if mainBoard.happiness > 0.4:
                    danger = False
                else:
                    danger = True

            # Redraw the screen and wait a clock tick.
            pygame.display.update()
            FPSCLOCK.tick(FPS)

            # Increase of the timer
            timer += 1
            timing = timer // FPS

            # Time remaining before defeat
            if danger:
                color = (255,0,0)
                timer_aux += 1
                timing_aux = timer_aux // FPS
            else:
                color = (0,0,0)
                timer_aux = 0
                timing_aux = timer_aux // FPS

            #drawBoard(mainBoard, DISPLAYSURF, selected, timing, origin, graphism)
            drawBoard_changes(mainBoard, DISPLAYSURF, selected, timing, origin, graphism, changes, change_all)
            drawHeader(mainBoard, DISPLAYSURF)
            drawMenu(mainBoard, DISPLAYSURF, selected, timing, toBuild, toBuild_Selected, color, tax)
            drawHappiness(DISPLAYSURF, mainBoard.happiness, HAPPINESSGAP, HAPPINESSGAP, BOXSIZE, color)

            if timing_aux >= time_lost:
                game = False
                displayLosingMenu(DISPLAYSURF, FPSCLOCK)


def production(mainBoard, priority, buildings):
    """ Function computing the production of each building depending on the inputs required. """
    workers_needed = [0 for i in range(len(priority))]
    wood_needed = [0 for i in range(len(priority))]
    number = [0 for i in range(len(priority))]

    # Aggregation of the requirements of every building in the map
    for i in range(NBROW):
        for j in range(NBCOLUMN):
            bat = mainBoard.map[i][j]
            if bat.type in priority:
                workers_needed[priority.index(bat.type)] += bat.hab_max
                wood_needed[priority.index(bat.type)] += bat.wood_input
                number[priority.index(bat.type)] += 1
    workers_remaining = mainBoard.habitants
    k = 0

    # Assign workers to building types depending on priorization
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

def increase_taxes(tax):
    if tax < TAXMAX:
        tax += 1
    return tax

def decrease_taxes(tax):
    if tax > TAXMIN:
        tax -= 1
    return tax

def happiness_calc(mainBoard, tax):
    if mainBoard.habitants == 0:
        mainBoard.happiness = 1
    else:
        drop_tax = (tax - TAXMIN) / TAXMAX * DROPSTEP
        drop_habitants = mainBoard.habitants / HABITANTSLEVEL * DROPSTEP
        if mainBoard.elec < 0:
            drop_supp = 20
        else:
            drop_supp = 0
        for k in mainBoard.built:
            if len(k) > 0:
                i, j = k[0], k[1]
                if  getType(mainBoard, i, j) == 1:
                    mainBoard.habitants += mainBoard.map[i][j].moving(timer)
        drop = drop_tax + drop_habitants + drop_supp
        if drop > mainBoard.happiness:
            mainBoard.happiness = 0
        else:
            mainBoard.happiness -= drop

