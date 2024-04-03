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

class Jeu () :
    
    def __init__(self) :
        
        #Attributs Fenêtre :
        self.ecran = pygame.display.set_mode((1300, 800))
        self.horloge = pygame.time.Clock()
        
        #Initialisation d'Attributs :
        self.attributs = attributs.Attributs()
        
    def boucle(self) :
        
        while self.attributs.acc_continuer() :

            ### Menu :
            if self.attributs.acc_menu() :
                
                
            
            
            
            
            
            
            
            
            
            
            ### Partie :
            else :
                pass
            
        
        
        
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