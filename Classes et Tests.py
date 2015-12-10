# 9 designe un vide sur l'interface "batiments"
# 0 designe une route sur l'interface "batiments"
# 1 designe une maison sur l'interface "batiments"
# 2 designe une  usine sur l'interface "batiments"
# 3 designe un batiment en général sur l'interface "batiments"

height=4  # pour le besoin de l'exercice
width=8  # pour le besoin de l'exercice

wood=0 # evolution avec le temps
workers_remaining=0 # evolution avec le temps


class Building():
    def __init__(self):
        self.type = 3

class Empty(Building):
    def __init__(self):
        self.type = 9
        
class House(Building):
    def __init__(self):
        self.type = 1
        self.capacity=5
        self.wood_needed=3

    def check_ressource(self):
        result= False
        if wood >= self.wood_needed:
            result= True
        return(result)

class Factory(Building):
    def __init__(self):
        super().__init__(i, j)
        self.type = 2
        self.hab_required = 10
        self.hab_used = 0
        self.prod_max = 10
        self.wood_needed = 10

    def check_ressource(self):
        result= False
        if wood >= self.wood_needed:
            result= True
        return(result)

    def creation(self):
        if self.accept_construction() and self.check_ressource():
            batiments[self.i][self.j].type = 2
 
    def destruction(self):
        batiments[self.i][self.j].type = 9  # destruction variable selon batiment_autres ressources specifiques (incomplet)      

class Route(Batiment):
    def __init__(self, i, j):
        super().__init__(i, j)
        self.type = 0
        self.materiaux_requis = 1

    def check_ressource(self):
        result= False
        if stock_bois >= self.materiaux_requis:
            result= True
        return(result)

    def creation(self):
        if self.accept_construction() and self.check_ressource():
            batiments[self.i][self.j].type = 0

    def destruction(self):
        batiments[self.i][self.j].type = 9  # destruction variable selon batiment_autres ressources specifiques (incomplet)


class Map():
    def __init__(self, height, width):
        empty = Empty()
        line = [empty] * width
        self.map = line * height

    def check_empty(self, i, j):
        if self.map[i][j].type != 9:
            result = False
        else: 
            result = True
        return(result)

    def check_road_junction(self, i, j):
        result = False
        if i-1 >= 0:
            if self.map[i-1][j].type == 0: # 0 designe une route
                result = True
        if j-1 >= 0:
            if self.map[i][j-1].type == 0: # 0 designe une route
                result = True
        if i+1 <= taille_hauteur-1:
            if self.map[i+1][j].type == 0: # 0 designe une route
                result = True 
        if j+1 <= taille_largeur-1:
            if self.map[i][j+1].type == 0: # 0 designe une route
                result = True
        return(result)

    def insert(building, i, j):
        if self.check_empty(i, j) and self.check_road_junction(i, j) and building.check_ressources():
            self.map[i][j] = building
        
    def delete(i, j):
        empty = Empty()
        self.map[i][j] = empty



maison1 = Maison(3,4)


terrainvide = Vide()
route0 = Route(2, 0)
route1 = Route(2, 1)
route2 = Route(2, 2)

batiments=[[terrainvide,terrainvide,terrainvide,terrainvide,terrainvide,terrainvide,terrainvide,terrainvide],
           [terrainvide,terrainvide,terrainvide,terrainvide,terrainvide,terrainvide,terrainvide,terrainvide],
           [route0,route1,route2,terrainvide,terrainvide,terrainvide,terrainvide,terrainvide],
           [terrainvide,terrainvide,terrainvide,terrainvide,terrainvide,terrainvide,terrainvide,terrainvide]]

     
                 
       
