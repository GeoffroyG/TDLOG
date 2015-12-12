# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 09:41:27 2015
Principales classes du jeu et tests de fonctionnement de base.
@author: Geoffroy Gallier
"""

""" 
9 designe un vide sur l'interface "batiments"
0 designe une route sur l'interface "batiments"
1 designe une maison sur l'interface "batiments"
2 designe une  usine sur l'interface "batiments"
"""



# wood = 100 # evolution avec le temps => passé en argument de la map
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

    def check_ressource(self, wood):
        result = False
        if wood >= self.wood_needed:
            result = True
        return(result)
        
class House(Building):
    def __init__(self):
        self.type = 1
        self.hab_max = 5
        self.wood_needed = 5

    def check_ressource(self, wood):
        result = False
        if wood >= self.wood_needed:
            result = True
        return(result)

class Factory(Building):
    def __init__(self):
        self.type = 2
        self.wood_needed = 10
        
        self.hab_max = 10

        self.prod_max = 10
        
        self.debit = 80
        self.time = 0

    def check_ressource(self, wood):
        result = False
        if wood >= self.wood_needed:
            result = True
        return(result)
    
    def production(self, worker, timing): # La petite fonction de prod tranquilou! Simpliste, mais pour le cas dégénéré on est bons
        wood = 0
        if (timing-self.time)%self.debit == 0:
            wood = int(self.prod_max * worker / self.hab_max)
        return(wood)


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
        self.map[2][0] = Road()

        # J'ai rajouté quelques trucs qui seront plus manipulables en tant qu'arguments    
        self.wood = 100
        self.habitants = 0
        self.height = height
        self.width = width
        self.workers = 0

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

    def insert(self, building, i, j):
        ''' Inserts a building in cell [i][j]. '''
        if self.check_empty(i, j) and self.check_road_junction(i, j) and building.check_ressource(self.wood):
            self.map[i][j] = building
            self.wood -= building.wood_needed
            if building.type == 1:
                self.habitants += building.hab_max
        
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
        # on avait dit que c'était pas joli mais sinon c'est vraiment pas pratique
        types = []
        line = []
        for i in range(self.height):
            for j in range(self.width):
                line.append(self.map[i][j].type)
            types.append(line)
            line = []
        return(types)
      
