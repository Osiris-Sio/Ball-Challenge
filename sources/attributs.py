# -*- coding: utf-8 -*-

'''
-> Ball Challenge

Auteur : AMEDRO Louis
''' 

######################################################
### Importation Module :
######################################################

import pygame

######################################################
### Classe Attributs :
######################################################

class Attributs () :
    
    def __init__(self) :
        
        self.continuer = True
        self.menu = True
        self.options = False
        
    ######################################################
    ### Accesseurs :
    ######################################################
    
    def acc_continuer(self):
        return self.continuer
    
    def acc_menu(self):
        return self.menu
    
    def acc_options(self):
        return self.options
    
    ######################################################
    ### Mutateurs :
    ######################################################
    
    def mut_continuer(self, valeur):
        assert isinstance(valeur, bool), 'Le paramètre doit être un booléen !'
        self.continuer = valeur 
        
    def mut_menu(self, valeur):
        assert isinstance(valeur, bool), 'Le paramètre doit être un booléen !'
        self.menu = valeur
        
    def mut_options(self, valeur):
        assert isinstance(valeur, bool), 'Le paramètre doit être un booléen !'
        self.options = valeur