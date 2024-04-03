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

class Jeu () :
    
    def __init__(self) :
        
        #Attributs Fenêtre :
        self.ecran = pygame.display.set_mode((1300, 800))
        self.horloge = pygame.time.Clock()
        
        #Initialisation d'Attributs :
        self.attributs = attributs.Attributs()
        self.controle = controle.Controle(self.attributs)
        self.affichage = affichage.Affichage(self.attributs)
        
        self.partie = None
        
    def boucle(self) :
        
        while self.attributs.acc_continuer() :

            ### Menu :
            if self.attributs.acc_menu() :
                
                for evenement in pygame.event.get() :
                    self.controle.menu(evenement)
            
            
                self.affichage.menu()
            
            
            
            
            
            
            
            ### Partie :
            else :
                
                for evenement in pygame.event.get() :
                    self.controle.partie(evenement)
            
                self.affichage.partie()
        
        
        pygame.quit()

    ######################################################
    ### Initialisation du Jeu et de la fenêtre :
    ######################################################
        
    def jouer(self) :
        pygame.init()
        pygame.display.set_caption('???') 
        pygame.mouse.set_visible(False)
        #pygame.display.set_icon(pygame.image.load('medias/.png'))
        self.boucle()