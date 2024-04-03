# -*- coding: utf-8 -*-

'''
-> ???

Auteur : AMEDRO Louis
''' 

######################################################
### Importation Module :
######################################################

import pygame, attributs

######################################################
### Classe Jeu :
######################################################

class Controle () :
    
    def __init__(self, les_attributs) :
        assert isinstance(les_attributs, attributs.Attributs), 'Le paramètre doit être de la classe Attributs !'
        
        self.attributs = les_attributs
        
    ######################################################
    ### Boutons :
    ######################################################
    
    def boutons_options(self) :
        pass
    
    def boutons_menu(self) :
        pass
    
    def boutons_partie(self) :
        pass
    
    
    
    ######################################################
    ### Entrées :
    ######################################################
        
    def quitter(self, evenement) :
        if evenement.type == pygame.QUIT or (evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_ESCAPE) :
            self.attributs.mut_continuer(False)
            return True
        return False
    
    def menu(self, evenement) :
        
        if not self.quitter(evenement) :
            pass
        
        
        
        
    
    def partie(self, evenement) :
        
        if not self.quitter(evenement) :
            pass
        