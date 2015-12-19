# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 15:36:10 2015

@author: Fatma - Geoffroy - Pierre 
"""

""" 
9 designe un vide sur l'interface "batiments"
0 designe une route sur l'interface "batiments"
1 designe une maison sur l'interface "batiments"
2 designe une usine sur l'interface "batiments"
3 designe une mine sur l'interface "batiments"
4 designe un atelier sur l'interface "batiments"
"""

from Constantes import *
import random

# wood = 100 # evolution avec le temps => passÃ© en argument de la map
workers_remaining = 0 # evolution avec le temps


class Building():
    def __init__(self):
        self.type = 9

class Empty(Building):
    def __init__(self):
        self.type = 9

class Road(Building):
    def __init__(self):
        self.type = 0
        self.wood_needed = 1
        self.time = 0

    def check_ressource(self, wood):
        result = False
        if wood >= self.wood_needed:
            result = True
        return(result)
        
class House(Building):
    def __init__(self):
        self.type = 1
        self.hab_max = 5
        self.hab_cond = 5
        self.hab = 0
        self.wood_needed = 5
        self.time = 0
        self.debit = 40

    def check_ressource(self, wood):
        result = False
        if wood >= self.wood_needed:
            result = True
        return(result)
        
    def moving(self, timing):
        if self.hab < self.hab_cond and (timing-self.time)%self.debit == 0:
            self.hab += 1
        if self.hab > self.hab_cond:
            self.hab = self.hab_cond

class Factory(Building):
    def __init__(self):
        self.type = 2
        self.wood_needed = 10
        
        self.hab_max = 10

        self.prod_max = 10
        self.worker = 0
        self.debit = 80
        self.time = 0

    def check_ressource(self, wood):
        result = False
        if wood >= self.wood_needed:
            result = True
        return(result)
    
    def production(self, timing): # La petite fonction de prod tranquilou! Simpliste, mais pour le cas dÃ©gÃ©nÃ©rÃ© on est bons
        wood = 0
        if (timing-self.time)%self.debit == 0:
            wood = int(self.prod_max * self.worker / self.hab_max)
        return(wood)

class Mine(Building):
    def __init__(self):
        self.type = 3
        self.stock = 1000

class Workshop(Building):
    def __init__():
        self.type = 4
        self.wood_needed = 10        

        self.hab_max = 10

        self.prod_max = 10
        self.worker = 0
        self.debit = 80
        self.time = 0

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

        #self.set_mines()
        self.map[2][0] = Road()
        # J'ai rajoute quelques trucs qui seront plus manipulables en tant qu'arguments    
        self.wood = 100
        self.habitants = 0
        self.height = height
        self.width = width
        self.workers = 0

    def set_mines(self):
        ''' Creates random mines. '''
        for i in range(NB_MINES):
            self.map[int(random.random()*NBCOLUMN)][int(random.random()*NBROW)] = Mine()

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
        if i-1 >= 0:
            if self.map[i-1][j].type == 0: # 0 designe une route
                result = True
        if j-1 >= 0:
            if self.map[i][j-1].type == 0: # 0 designe une route
                result = True
        if i+1 <= self.height-1:
            if self.map[i+1][j].type == 0: # 0 designe une route
                result = True 
        if j+1 <= self.width-1:
            if self.map[i][j+1].type == 0: # 0 designe une route
                result = True
        return(result)
        
    def check_junction(self, types, i, j):
        ''' Determines how many buildings of type types near the [i][j] cell. '''
        result = 0
        if i-1 >= 0:
            if self.map[i-1][j].type == types: # 0 designe une route
                result += 1
        if j-1 >= 0:
            if self.map[i][j-1].type == types: # 0 designe une route
                result += 1
        if i+1 <= self.height-1:
            if self.map[i+1][j].type == types: # 0 designe une route
                result += 1
        if j+1 <= self.width-1:
            if self.map[i][j+1].type == types: # 0 designe une route
                result += 1
        return(result)

    def insert(self, building, i, j):
        ''' Inserts a building in cell [i][j]. '''
        if self.check_empty(i, j) and self.check_road_junction(i, j) and building.check_ressource(self.wood):            
            self.map[i][j] = building
            self.wood -= building.wood_needed
            return(True)
        return(False)
        
    def delete(self, i, j):
        ''' Deletes the [i][j] building. '''
        self.map[i][j] = Empty()

    def display(self):
        ''' Displays the matrix in text mode. '''
        types = []
        for i in range(self.height):
            for j in range(self.width):
                types.append(self.map[i][j].type)
            print(types)
            types = []
        print("")
    
    def types(self):
        ''' Returns a matrix with all the types '''
        # on avait dit que c'etait pas joli mais sinon c'est vraiment pas pratique
        types = []
        line = []
        for i in range(self.height):
            for j in range(self.width):
                line.append(self.map[i][j].type)
            types.append(line)
            line = []
        return(types)
      
