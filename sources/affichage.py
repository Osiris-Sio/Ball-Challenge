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
        
        #Fond :
        self.fond = pygame.image.load("ressources/menu/test.png")
    
    
    def fond_menu(self) :
        self.ecran.blit(self.fond, (0, 0))
    
    
    
    
    
    
    def menu(self) :
        self.fond_menu()
    
    
    
    def partie(self) :
        pass