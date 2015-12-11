# 9 designe un vide sur l'interface "batiments"
# 0 designe une route sur l'interface "batiments"
# 1 designe une maison sur l'interface "batiments"
# 2 designe une  usine sur l'interface "batiments"

height = 4  # pour le besoin de l'exercice
width = 8  # pour le besoin de l'exercice

wood = 100 # evolution avec le temps
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

    def check_ressource(self):
        result = False
        if wood >= self.wood_needed:
            result = True
        return(result)
        
class House(Building):
    def __init__(self):
        self.type = 1
        self.hab_max = 5
        self.wood_needed = 5

    def check_ressource(self):
        result = False
        if wood >= self.wood_needed:
            result = True
        return(result)

class Factory(Building):
    def __init__(self):
        self.type = 2
        self.wood_needed = 10
        
        self.hab_max = 10
        self.hab_real = 0

        self.prod_max = 10
        self.prod_real = 0

    def check_ressource(self):
        result = False
        if wood >= self.wood_needed:
            result = True
        return(result)


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
        if i+1 <= height-1:
            if self.map[i+1][j].type == 0: # 0 designe une route
                result = True 
        if j+1 <= width-1:
            if self.map[i][j+1].type == 0: # 0 designe une route
                result = True
        return(result)

    def insert(self, building, i, j):
        ''' Inserts a building in cell [i][j]. '''
        if self.check_empty(i, j) and self.check_road_junction(i, j) and building.check_ressource():
            self.map[i][j] = building
        
    def delete(self, i, j):
        ''' Deletes the [i][j] building. '''
        self.map[i][j] = Empty()

    def display(self):
        ''' Displays the matrix in text mode. '''
        types = []
        for i in range(height):
            for j in range(width):
                types.append(self.map[i][j].type)
            print(types)
            types = []
        print("")

mymap = Map(height, width)
mymap.display()

mymap.insert(Road(), 2, 0)
mymap.insert(Road(), 2, 1)
mymap.insert(Road(), 2, 2)
mymap.insert(House(), 1, 2)
mymap.insert(Factory(), 3, 2)

mymap.display()

