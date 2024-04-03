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
    ### Accesseurs :
    ######################################################
    
    def acc_position_curseur(self):
        return pygame.mouse.get_pos()
        
    ######################################################
    ### Boutons :
    ######################################################
    
    def boutons_options(self) :
        pass
    
    def boutons_menu(self) :
        curseur = self.acc_position_curseur()
        
        #Jouer :
        if 400 <= curseur[0] <= 600 and 400 <= curseur[1] <= 460 :
            self.attributs.mut_menu(False)
    
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
            
            if evenement.type == pygame.MOUSEBUTTONDOWN :
                
                if evenement.button == 1 :
                    self.boutons_menu()
        
        
        
        
    
    def partie(self, evenement) :
        
        if not self.quitter(evenement) :
            pass
        