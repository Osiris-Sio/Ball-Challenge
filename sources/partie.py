# -*- coding: utf-8 -*-

'''
-> Ball Challenge

Auteur : AMEDRO Louis
''' 

######################################################
### Importation Module :
######################################################

import pygame, attributs, controle, affichage

######################################################
### Classe Jeu :
######################################################

class Partie () :
    
    def __init__(self, les_attributs):
        assert isinstance(les_attributs, attributs.Attributs()), 'Le paramètre doit être de la classe Attributs !'
        
        self.attributs = les_attributs
        
        
    def deroulement(self) :
        pass