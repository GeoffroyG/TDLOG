# 9 designe un vide sur l'interface "batiments"
# 0 designe une route sur l'interface "batiments"
# 1 designe une maison sur l'interface "batiments"
# 2 designe une  usine sur l'interface "batiments"
# 3 designe un batiment en général sur l'interface "batiments"

batiments=[[9,9,9,9,9,9,9,9],
           [9,9,9,9,9,9,9,9],
           [0,0,0,9,9,9,9,9],
           [9,9,9,9,9,9,9,9]]


taille_hauteur=4  # pour le besoin de l'exercice
taille_largeur=8  # pour le besoin de l'exercice

stock_bois=0 # evolution avec le temps
hab_restant=0 # evolution avec le temps

maison1 = Maison(3,4)

class Batiment():
    def __init__(self, i, j):
        self.type = 3
        self.accept_construction(i, j)

    def check_raccord_route(self, i, j):
        result = False
        if i-1 >= 0:
            if batiments [i-1][j].type == 0: # 0 designe une route
                result = True
        if j-1 >= 0:
            if batiments [i][j-1].type == 0: # 0 designe une route
                result = True
        if i+1 <= taille_hauteur-1:
            if batiments [i+1][j].type == 0: # 0 designe une route
                result = True 
        if j+1 <= taille_largeur-1:
            if batiments [i][j+1].type == 0: # 0 designe une route
                result = True
        return(result)

    def check_emplacement_vide(self, i, j):
        result = True
        if batiments [i][j].type != 9:
            result = False
        return(result)

    def accept_construction(self, i, j):
        result= False
        if (self.check_emplacement_vide(i, j)) And (self.check_raccord_route(i, j)):
            result= True
        return(result) 

#    def affiche_changement(self)

          
class Maison(Batiment):
    def __init__(self):
        super().__init__()
        self.type = 1
        self.hab_par_maison=5
        self.materiaux_requis=3

    def check_ressource(self):
        result = False
        if stock_bois >= self.materiaux_requis:
            result = True
        return(result)

    def creation(self):
        if self.accept_construction() And self.check_ressource():
            batiments[self.i][self.j].type = 1

    def destruction(self):
        batiments[self.i][self.j].type = 9  # destruction variable selon batiment_autres ressources specifiques (incomplet)

class Usine(Batiment):
    def __init__(self):
        super().__init__()
        self.type = 2
        self.hab_requis = 10
        self.hab_affectes = 0
        self.prod_max = 100
        self.stock_bois = 0
        self.materiaux_requis = 10

    def check_ressource(self):
        result= False
        if (stock_bois >= self.materiaux_requis) And (hab_restant >= 1):
            result= True
        return(result)

    def creation(self):
        if self.accept_construction() And self.check_ressource():
            batiments[self.i][self.j].type = 2
 
    def destruction(self):
        batiments[self.i][self.j].type = 9  # destruction variable selon batiment_autres ressources specifiques (incomplet)      

class Route(Batiment):
    def __init__(self):
        super().__init__()
        self.type = 0
        self.materiaux_requis = 1

    def check_ressource(self):
        result= False
        if stock_bois >= self.materiaux_requis:
            result= True
        return(result)

    def creation(self):
        if self.accept_construction() And self.check_ressource():
            batiments[self.i][self.j].type = 0

    def destruction(self):
        batiments[self.i][self.j].type = 9  # destruction variable selon batiment_autres ressources specifiques (incomplet)







     
                 
       
