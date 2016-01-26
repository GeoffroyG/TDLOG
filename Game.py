# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 21:18:54 2016

@author: Fatma - Geoffroy - Pierre
"""

from Graphismes import *

def main():
    """ Main game loop. """
    global FPSCLOCK, DISPLAYSURF, selected, building, graphism, \
    graphism_Selected, toBuild, toBuild_Selected, timer, tax
    pygame.init()

    # Initialisation of the clock and the window
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    init_buildings()

    pygame.display.set_caption('Jeu Sim City') # name of the game

    DISPLAYSURF.fill(WHITE)

    while True:

        # Display of a beginning menu and wait for the player to start the game
        displayBeginningMenu(DISPLAYSURF, FPSCLOCK, font_title)

        # Initialization of main board
        mainBoard = Classes.Map(NBROW, NBCOLUMN)

        tax = TAXMIN
        timer_aux = 0
        color = (0,0,0)

        selected = [False, False, False, False, False, False, False, False,
                    False, False]
        building = Classes.Empty()

        shortcuts = [K_r, K_h, K_f, K_a, K_s, K_z, K_c, K_p, K_e, K_g]

        # Initialisation of the selection variables
        buildingselected = False
        mouseClicked = False

        # Initialisation of game variables
        changes = []
        change_all = True
        game = True
        danger = False

        timer = 0 # timer in FPS
        timing = timer // FPS # timer in seconds

        origin = [0,0] # coordinates of the top-left cell displayed
        mousex = 0 # used to store x coordinate of mouse event
        mousey = 0 # used to store y coordinate of mouse event

        # Draw the main window for the first time
        DISPLAYSURF.fill(WHITE)
        drawBoard(mainBoard, DISPLAYSURF, selected, timing, origin, graphism)
        drawHeader(mainBoard, DISPLAYSURF)
        drawMenu(mainBoard, DISPLAYSURF, selected, timing, toBuild,
                 toBuild_Selected, color, tax)

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
                elif event.type == QUIT \
                     or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    os.sys.exit()

                if event.type == KEYUP and event.key in shortcuts:
                    selected, buildingselected, building = \
                    shortcuts_manager(shortcuts.index(event.key), selected,
                                      buildingselected, building)

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
                if boxx != None and boxy != None and mouseClicked \
                                and buildingselected:
                    build = mainBoard.insert(building, boxx, boxy)
                    if build:
                        changes.append([boxx, boxy])
                if boxx != None and boxy != None and not(mouseClicked) \
                                and buildingselected and build:
                    buildingselected = False
                    building = Classes.Empty()
                    selected = [False, False, False, False, False, False,
                                False, False, False, False]

                drawInfoBoard(DISPLAYSURF, boxx, boxy, mainBoard, buildings)

            if isInMenu(mousex) \
                and getBuildingFromMenu(mousex, mousey, selected,
                                        buildings, False) != None:
                drawInfoMenu(DISPLAYSURF, mousex, mousey, buildings)

            if isInMenu(mousex) and mouseClicked:

                # Selection of a building in the menu
                selected, buildingselected, building = \
                getBuildingFromMenu(mousex, mousey, selected,
                                    buildings, mouseClicked)

                # Modification of tax level
                if mainBoard.tax_plus_button.collidepoint(mousex, mousey):
                    tax = increase_taxes(tax)

                if mainBoard.tax_minus_button.collidepoint(mousex, mousey):
                    tax = decrease_taxes(tax)

                if mainBoard.prio_plus[0].collidepoint(mousex, mousey):
                    priorize(mainBoard, 2, -1)

                if mainBoard.prio_minus[0].collidepoint(mousex, mousey):
                    priorize(mainBoard, 2, 1)

                if mainBoard.prio_plus[1].collidepoint(mousex, mousey):
                    priorize(mainBoard, 3, -1)

                if mainBoard.prio_minus[1].collidepoint(mousex, mousey):
                    priorize(mainBoard, 3, 1)

                if mainBoard.prio_plus[2].collidepoint(mousex, mousey):
                    priorize(mainBoard, 4, -1)

                if mainBoard.prio_minus[2].collidepoint(mousex, mousey):
                    priorize(mainBoard, 4, 1)

                drawMenu(mainBoard, DISPLAYSURF, selected, timing, toBuild,
                         toBuild_Selected, color, tax)

            # Reinitialization of the parameters after each loop
            boxx, boxy = None, None
            mouseClicked = False
            # Increase of the newcomers
            for k in mainBoard.built:
                if len(k) > 0:
                    i, j = k[0], k[1]
                    if  getType(mainBoard, i, j) == 1:
                        mainBoard.citizens += mainBoard.map[i][j].moving(timer)

            if timer % PRODSTEP == 0:
                production(mainBoard, buildings)

            if timer % TAXSTEP == 0:
                mainBoard.money += mainBoard.citizens * tax

            if timer % HAPPINESSSTEP == 0:
                happiness_calc(mainBoard, tax, timing)
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

            drawBoard_changes(mainBoard, DISPLAYSURF, selected, timing, origin,
                              graphism, changes, change_all)
            drawHeader(mainBoard, DISPLAYSURF)
            drawMenu(mainBoard, DISPLAYSURF, selected, timing, toBuild,
                     toBuild_Selected, color, tax)
            drawHappiness(DISPLAYSURF, mainBoard.happiness, HAPPINESSGAP,
                          HAPPINESSGAP, BOXSIZE, color)

            if timing_aux >= time_lost:
                game = False
                displayLosingMenu(DISPLAYSURF, FPSCLOCK)

def init_buildings():
    global buildings, toBuild, toBuild_Selected, graphism, graphism_Selected

    buildings = [Classes.Road(),                Classes.House(),
                 Classes.Factory(),             Classes.Quarry(),
                 Classes.Sawmill(),             Classes.Wind_power_plant(),
                 Classes.Coal_power_plant(),    Classes.Park(),
                 Classes.ENPC(),                Classes.Empty(),
                 Classes.Mine(),                Classes.Forest()]
    # toBuild and buildings are to be modified together :
    # one is the buidings list the other the pictures list

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

    toBuild_Selected = [pygame.image.load("2.Images/Road_S.png").convert(),
                        pygame.image.load("2.Images/House_S.png").convert(),
                        pygame.image.load("2.Images/Factory_S.png").convert(),
                        pygame.image.load("2.Images/Quarry_S.png").convert(),
                        pygame.image.load("2.Images/Sawmill_S.png").convert(),
                        pygame.image.load("2.Images/Wind_S.png").convert(),
                        pygame.image.load("2.Images/Coal_S.png").convert(),
                        pygame.image.load("2.Images/Park_S.png").convert(),
                        pygame.image.load("2.Images/ENPC_S.png").convert(),
                        pygame.image.load("2.Images/Grass_S.png").convert()]

    # "Graphism" is the extension of "toBuild" with things that cant be built.
    # This distinction will be useful in the display of the menu.
    graphism = toBuild + [pygame.image.load("2.Images/Mine.png").convert()] \
                       + [pygame.image.load("2.Images/Forest.png").convert()]

    graphism_Selected = toBuild_Selected \
    + [pygame.image.load("2.Images/Mine_S.png").convert()] \
    + [pygame.image.load("2.Images/Forest_S.png").convert()]


def production(mainBoard, buildings):
    """ Function computing the production of each building depending on the
    inputs required. """
    workers_needed = [0 for i in range(len(mainBoard.priority))]
    wood_needed = [0 for i in range(len(mainBoard.priority))]
    number = [0 for i in range(len(mainBoard.priority))]

    # Aggregation of the requirements of every building in the map
    for i in range(NBROW):
        for j in range(NBCOLUMN):
            bat = mainBoard.map[i][j]
            if bat.type in mainBoard.priority:
                workers_needed[mainBoard.priority.index(bat.type)] += \
                bat.cit_max

                wood_needed[mainBoard.priority.index(bat.type)] += \
                bat.wood_input

                number[mainBoard.priority.index(bat.type)] += 1
    workers_remaining = mainBoard.citizens
    k = 0

    # Assign workers to building types depending on priorization
    while k < len(mainBoard.priority) and workers_remaining > 0:

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

        mainBoard.wood += buildings[mainBoard.priority[k]].wood_output * \
                          min(proportion_worker,proportion_wood) * \
                          mainBoard.sawmill_coeff * number[k]
        mainBoard.money += buildings[mainBoard.priority[k]].money_output * \
                           min(proportion_worker,proportion_wood) * number[k]
        mainBoard.stone += buildings[mainBoard.priority[k]].stone_output * \
                           min(proportion_worker,proportion_wood) * \
                           mainBoard.quarry_coeff * number[k]
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

def priorize(mainBoard, building, order):
    index = mainBoard.priority.index(building)
    if index + order >= 0 and index + order < len(mainBoard.priority):
        mainBoard.priority.remove(building)
        mainBoard.priority.insert(index + order, building)
        print(mainBoard.priority)

def happiness_calc(mainBoard, tax, timing):
    """ Calculates the happiness based on the number of inhabitants
    and taxes. """
    if mainBoard.citizens == 0:
        mainBoard.happiness = 1
    else:
        drop_tax = (tax - TAXMIN) / TAXMAX * DROPSTEP
        drop_citizens = mainBoard.citizens / CITIZENSLEVEL * DROPSTEP
        drop_timing = timing / TIMINGLEVEL * DROPSTEP
        if mainBoard.elec < 0:
            drop_supp = 20
        else:
            drop_supp = 0
        drop_happ = 0
        for k in mainBoard.built:
            if len(k) > 0:
                i, j = k[0], k[1]
                drop_happ += mainBoard.map[i][j].happiness_output
        drop = drop_tax + drop_citizens + drop_supp + drop_timing - drop_happ
        if drop > mainBoard.happiness:
            mainBoard.happiness = 0
        elif mainBoard.happiness - drop >= 1:
            mainBoard.happiness = 1
        else:
            mainBoard.happiness -= drop


def shortcuts_manager(shortcut_index, selected, buildingselected, building):
    """ Selection of buildings with keyboards shortcuts. """
    if selected[shortcut_index] == False:
        buildingselected = True
        building = buildings[shortcut_index]
        selected = [False, False, False, False, False, False, False, False,
                    False, False]
        selected[shortcut_index] = True
    else:
        buildingselected = False
        building = Classes.Empty()
        selected = [False, False, False, False, False, False, False, False,
                    False, False]
    return selected, buildingselected, building



def read_leaderboard(filename):
    scores = []
    with open(filename, 'r', encoding='utf-8') as infile:
        for line in infile:
            data = line.split()
            scores.append([data[0], data[1], data[3], data[5]])
    print(scores)


def write_leaderboard(filename, playername, minutes, seconds, date):
    score = playername + " " + str(minutes) + " min " + str(seconds) + " sec " + date + "\n"
    with open(filename, 'a', encoding='utf-8') as infile:
        infile.write(score)

def convert_time(timer):
    minutes = times // 60
    seconds = timer - minutes * 60
    return minutes, seconds



read_leaderboard(LEADERBOARDFILE)
write_leaderboard(LEADERBOARDFILE, "Geoffroy", 12, 14, "26/01/2015")
read_leaderboard(LEADERBOARDFILE)
