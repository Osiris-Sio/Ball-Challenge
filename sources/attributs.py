# -*- coding: utf-8 -*-

'''
-> ???

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
        
        #Boucle :
        self.continuer = True
        
        #Menu :
        self.menu = True
        
    ######################################################
    ### Accesseurs :
    ######################################################
    
    def acc_continuer(self):
        return self.continuer
    
    def acc_menu(self):
        return self.menu
    
    ######################################################
    ### Mutateurs :
    ######################################################
    
    def mut_continuer(self, valeur):
        assert isinstance(valeur, bool), 'Le paramètre doit être un booléen !'
        self.continuer = valeur 
        
    def mut_menu(self, valeur):
        assert isinstance(valeur, bool), 'Le paramètre doit être un booléen !'
        self.menu = valeur