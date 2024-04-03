# -*- coding: utf-8 -*-

'''
-> Ball Challenge

Auteur : AMEDRO Louis
''' 

######################################################
### Importation Module :
######################################################

import pygame, attributs, controle

######################################################
### Classe Jeu :
######################################################

class Affichage () :
    
    def __init__(self, les_attributs) :
        assert isinstance(les_attributs, attributs.Attributs()), 'Le paramètre doit être de la classe Attributs !'
        
        self.attributs = les_attributs
    
    
    def fond_menu(self) :
        pass
    
    
    
    
    
    
    def menu(self) :
        self.fond_menu()
    
    
    
    def partie(self) :
        pass