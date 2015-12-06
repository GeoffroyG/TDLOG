# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 10:39:00 2015

@author: Geoffroy

Variables globales à initialiser : 
- nb_tours le compteur du nombre de tours
- hab_par_maison la capacité d'accueil de chaque maison
- stock_bois le bois stocké
- condition_victoire le nombre de maisons nécessaires pour gagner le jeu

Fonctions à définir : 
- fermer_jeu() la fonction qui affiche un message "gagné" et ferme proprement le jeu

"""




def fin_de_tour():
    hab = 0
    prod_bois= 0
    
    # On compte le nombre d'habitants totaux de la ville
    for i in range(taille_plateau):
        if batiments[i] == 1: # 1 représente la maison
            hab += hab_par_maison

    hab_restant = hab # le nombre d'habitants restant à affecter en usines est égal au nombre d'habitants de la ville

    # On affecte les habitants aux usines et les usines produisent
    for i in range(taille_plateau):
        if batiments[i] == 2: # 2 représente l'usine
            batiments[i].hab_affectes = min(batiments[i].hab_requis, hab_restant)
            hab_restant -= batiments[i].hab_affectes
            stock_bois += int(batiments[i].prod_max * batiments[i].hab_affectes / batiments[i].hab_requis)
            
    nb_tours += 1
    
    if fin_de_jeu():
        fermer_jeu()

def fin_de_jeu():
    nb_maisons = 0
    for i in range(taille_plateau):
        if batiments[i] == 1: # 1 représente la maison
            nb_maisons += 1
            
    gagne = False

    if nb_maisons >= condition_victoire:
        gagne = True
    return gagne
    
    