# -*- coding: utf-8 -*-

'''
-> Ball Challenge

Auteur : AMEDRO Louis
''' 

######################################################
### Importation Module :
######################################################

import pygame, attributs, controle, jeu

######################################################
### Classe Jeu :
######################################################

class Affichage () :
    
    def __init__(self, ecran, les_attributs) :
        assert isinstance(les_attributs, attributs.Attributs), 'Le paramètre doit être de la classe Attributs !'
        
        self.ecran = ecran
        self.attributs = les_attributs
        
        #Fonds :
        self.fonds = {
            'menu' : pygame.image.load("ressources/menu/fond.png"),
            'par_defaut' : pygame.image.load("ressources/fond_partie.png")
        }
        
        self.boutons = {
            'jouer' : pygame.image.load("ressources/menu/jouer.png") 
        }
    
    
    def fond_menu(self) :
        self.ecran.blit(self.fonds['menu'], (0, 0))
    
    def boutons_menu(self) :
        self.ecran.blit(self.boutons['jouer'], (400, 400))
    
    def fond_partie(self) :
        self.ecran.blit(self.fonds['par_defaut'], (0, 0))
    
    
    def menu(self) :
        self.fond_menu()
        self.boutons_menu()
    
    
    
    def partie(self) :
        self.fond_partie()
    