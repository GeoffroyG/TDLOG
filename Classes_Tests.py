# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 15:36:10 2015

@author: Fatma - Geoffroy - Pierre
"""

"""
0 = Road
1 = House
2 = Factory
3 = Quarry
4 = Sawmill
5 = Wind power plant
6 = Coal power plant
7 = Hydraulic power plant
8 = ENPC

9 = Empty
10 = Mine
11 = Forest
"""

from Constantes import *
import random
import math


class Building():
    """ Parent class for every building in the game. """
    def __init__(self):
        self.type = 9
        self.hab = 0
        self.wood_needed = 0
        self.stone_needed = 0
        self.elec_needed = 0
        self.money_needed = 0
        self.coeff = 1
        self.time = 0

        self.wood_input = 0
        self.money_input = 0
        self.stone_input = 0
        self.wood_output = 0
        self.money_output = 0
        self.stone_output = 0
        self.happiness_output = 0

    def check_ressource(self, wood, stone, money, elec):
        """ Check if enough ressources are available to build this building. """
        result = False
        if wood >= self.wood_needed and stone >= self.stone_needed and money >= self.money_needed and elec >= self.elec_needed :
            result = True
        return(result)


class Empty(Building):
    def __init__(self):
        Building.__init__(self)
        self.type = 9


class Road(Building):
    def __init__(self):
        Building.__init__(self)
        self.type = 0
        self.stone_needed = 1
        self.time = 0
        self.money_needed= 100


class House(Building):
    def __init__(self):
        Building.__init__(self)
        self.type = 1
        self.hab_max = 5
        self.factories = 0
        self.hab = 0
        self.wood_needed = 5
        self.stone_needed = 5
        self.debit = 40
        self.money_needed= 200
        self.elec_needed = 5 # in MW

    def moving(self, timer):
        """ Evolution of the number of inhabitants in a house. """
        # If the amount of habs is superior to the number allowed
        if self.hab > self.hab_max - self.factories:
            diff = self.hab_max - self.factories - self.hab

        # If the number of habs is correct but its time to host a new citizen
        else:
            if (timer-self.time)%self.debit == 0:
                diff = 1
            else:
                diff= 0

        self.hab += diff
        return diff


class Factory(Building):
    def __init__(self):
        Building.__init__(self)
        self.type = 2
        self.stone_needed = 10
        self.money_needed= 300
        self.elec_needed = 10 # in MW

        self.hab_max = 10
        self.wood_input = 10
        self.money_output = 50


class Quarry(Building):
    def __init__(self):
        Building.__init__(self)
        self.type = 3
        self.wood_needed = 10
        self.stone_needed = 10
        self.hab_max = 10
        self.money_needed= 200
        self.prod_max = 10
        self.coeff = 0
        self.worker = 0
        self.debit = 80
        self.time = 0
        self.elec_needed = 5
        self.stone_output = 5


class Sawmill(Building):
    def __init__(self):
        Building.__init__(self)
        self.type = 4
        self.wood_needed = 10
        self.stone_needed = 10
        self.hab_max = 10
        self.money_needed= 200
        self.prod_max = 10
        self.coeff = 0
        self.worker = 0
        self.debit = 80
        self.time = 0
        self.elec_needed = 5
        self.wood_output = 5


class Wind_power_plant(Building):
    def __init__(self):
        Building.__init__(self)
        self.type = 5
        self.money_needed= 8000
        self.wood_needed = 10
        self.stone_needed = 10
        self.time = 0
        self.elec_needed = -20

class Coal_power_plant(Building):
    def __init__(self):
        Building.__init__(self)
        self.type = 6
        self.money_needed= 8000
        self.wood_needed = 10
        self.stone_needed = 10
        self.time = 0
        self.elec_needed = -20

class Park(Building):
    def __init__(self):
        Building.__init__(self)
        self.type = 7
        self.money_needed= 10000
        self.wood_needed = 15
        self.stone_needed = 0
        self.time = 0
        self.elec_needed = 2
        self.happiness_output = 0.03


class ENPC(Building):
    def __init__(self):
        Building.__init__(self)
        self.type = 8
        self.money_needed= 50000
        self.wood_needed = 80
        self.stone_needed = 150
        self.time = 0
        self.elec_needed = 50
        self.happiness_output = 0.2


class Mine(Building):
    def __init__(self):
        Building.__init__(self)
        self.type = 10


class Forest(Building):
    def __init__(self):
        Building.__init__(self)
        self.type = 11


class Map():
    def __init__(self, height, width):
        empty = Empty()
        line = []
        self.map = []
        for i in range(height):
            for j in range(width):
                line.append(empty)
            self.map.append(line)
            line = []

        self.set_mines()
        self.set_forests()
        self.map[2][0] = Road()

        self.wood = 100
        self.stone = 100
        self.money = 30000
        self.elec = 0
        self.happiness = 1

        self.habitants = 0
        self.workers = 0

        self.height = height
        self.width = width

        self.built = []

        self.tax_plus_button = []
        self.tax_minus_button = []

        self.quarry_coeff = 0
        self.quarry_nb = 0
        self.sawmill_coeff = 0
        self.sawmill_nb = 0
        
        self.priority = [2,3,4]
        
        self.prio_plus = [0, 0, 0]
        self.prio_minus= [0, 0, 0]
        

        self.shortcuts_str = ["R", "H", "F", "Q", "S", "W", "C", "P", "E", "G"]

    def set_mines(self):
        ''' Creates random mines. '''
        for i in range(NBMINES):
            self.map[int(random.random()*NBROW)][int(random.random()*NBCOLUMN)] = Mine()

    def set_forests(self):
        ''' Creates random mines. '''
        for i in range(NBFORESTS):
            self.map[int(random.random()*NBROW)][int(random.random()*NBCOLUMN)] = Forest()

    def distance_ressource(self, i, j, building_type, delete = 1):
        """ Creates a coefficient reflecting the number of natural ressources nearby. """
        coeff = 0
        for p in range(self.height):
            for q in range(self.width):
                if self.map[p][q].type == building_type:
                    coeff += 1/(1+math.fabs(p-i) + math.fabs(q-j))
        if building_type == 10:
            self.quarry_coeff = round((self.quarry_coeff * self.quarry_nb + delete * coeff) / (self.quarry_nb + delete), 2)
            self.quarry_nb += delete
        if building_type == 11:
            self.sawmill_coeff = round((self.sawmill_coeff * self.sawmill_nb + delete * coeff) / (self.sawmill_nb + delete), 2)
            self.sawmill_nb += delete

    def check_empty(self, i, j):
        ''' Checks if there is no building in cell [i][j]. '''
        if self.map[i][j].type != 9:
            result = False
        else:
            result = True
        return(result)

    def check_road_junction(self, i, j):
        ''' Determines if there is a road near the [i][j] cell. '''
        result = False
        # Type 0 is a road
        if i-1 >= 0:
            if self.map[i-1][j].type == 0:
                result = True
        if j-1 >= 0:
            if self.map[i][j-1].type == 0:
                result = True
        if i+1 <= self.height-1:
            if self.map[i+1][j].type == 0:
                result = True
        if j+1 <= self.width-1:
            if self.map[i][j+1].type == 0:
                result = True
        return(result)

    def check_junction(self, types, i, j):
        ''' Determines how many buildings of type 'types' near the [i][j] cell. '''
        result = 0
        # Type 0 is a road
        if i-1 >= 0:
            if self.map[i-1][j].type == types:
                result += 1
        if j-1 >= 0:
            if self.map[i][j-1].type == types:
                result += 1
        if i+1 <= self.height-1:
            if self.map[i+1][j].type == types:
                result += 1
        if j+1 <= self.width-1:
            if self.map[i][j+1].type == types:
                result += 1
        return(result)

    def factory_impact(self, i, j, delete = 1):
        """ Determines the impact of a factory created on houses nearby. """
        # Type 0 is a road
        if i-1 >= 0:
            if self.map[i-1][j].type == 1:
                self.map[i-1][j].factories += 1 * delete
        if j-1 >= 0:
            if self.map[i][j-1].type == 1:
                self.map[i][j-1].factories += 1 * delete
        if i+1 <= self.height-1:
            if self.map[i+1][j].type == 1:
                self.map[i+1][j].factories += 1 * delete
        if j+1 <= self.width-1:
            if self.map[i][j+1].type == 1:
                self.map[i][j+1].factories += 1 * delete

        return 0

    def insert(self, building_given, i, j):
        ''' Inserts a building in cell [i][j]. '''

        # Check is conditions are met to build the new building
        if self.check_empty(i, j) and self.check_road_junction(i, j) and (building_given.check_ressource(self.wood,self.stone,self.money,self.elec)):
            # Each house is unique for they all contains a certain amount of inhabitants, whereas variable for other buildings are all macro
            if building_given.type == 1:
                building = House()
            else:
                building = building_given

            # The building is created with the ressources
            self.map[i][j] = building
            self.wood -= building.wood_needed
            self.stone -= building.stone_needed
            self.money -= building.money_needed
            self.elec -= building.elec_needed

            # The impact of the new building on happiness is computed
            if self.happiness + building.happiness_output <= 1:
                self.happiness += building.happiness_output
            else:
                self.happiness = 1

            # Built is used to store the buildings and only inspect them at each loop
            if building.type != 0:
                self.built.append([i,j])

            # If it is a factory, look for houses to reduce the number of inhabitants
            if building.type == 2:
                self.factory_impact(i, j)

            # If it is a quarry, look for mines
            if building.type == 3:
                self.distance_ressource(i, j, 10)

            # If it is a sawmill, look for forests
            if building.type == 4:
                self.distance_ressource(i, j, 11)

            return(True)

        # Delete buildings
        if building_given.type == 9:
            former_building = self.map[i][j]
            # If it is a road, we check potential road junction issues
            if self.map[i][j].type == 0 and not(self.delete_road(i, j)):
                return(False)
            # Else, half of the initial ressources are given back
            elif former_building.type < 9:
                self.wood += former_building.wood_needed // 2
                self.stone += former_building.stone_needed // 2
                self.money += former_building.money_needed // 2
                self.elec += former_building.elec_needed
                self.map[i][j] = building_given

                # Inhabitants of a house have to leave the city
                if former_building.type == 1:
                    self.habitants -= former_building.hab

                if former_building.type == 3:
                    self.distance_ressource(i, j, 10, -1)

                if former_building.type == 4:
                    self.distance_ressource(i, j, 11, -1)

                return(True)

        return(False)

    def delete_road(self, i, j):
        """ It is possible to delete a road if it is only attached to 1 road and if no building is directly linked to this road. """
        if i == 2 and j == 0:
            delete = False
        else:
            roads_near = (self.map[i-1][j].type == 0) + (self.map[i+1][j].type == 0) + (self.map[i][j-1].type == 0) + (self.map[i][j+1].type == 0)
            buildings_near = (self.map[i-1][j].type > 0 and self.map[i-1][j].type < 9) + (self.map[i+1][j].type > 0 and self.map[i+1][j].type < 9) + (self.map[i][j-1].type > 0 and self.map[i][j-1].type < 9) + (self.map[i][j+1].type > 0 and self.map[i][j+1].type < 9)

            if roads_near < 2 and buildings_near == 0:
                delete = True
            else:
                delete = False
        return delete

    def display(self):
        ''' Displays the matrix in text mode. '''
        types = []
        for i in range(self.height):
            for j in range(self.width):
                types.append(self.map[i][j].type)
        #    print(types)
            types = []
        #print("")

    def types(self):
        ''' Returns a matrix with all the types '''
        types = []
        line = []
        for i in range(self.height):
            for j in range(self.width):
                line.append(self.map[i][j].type)
            types.append(line)
            line = []
        return(types)

