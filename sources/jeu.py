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
        self.ecran = pygame. display.set_mode((1024, 768))
        self.horloge = pygame.time.Clock()
        
        #Initialisation d'Attributs :
        self.attributs = attributs.Attributs()
        self.controle = controle.Controle(self.attributs)
        self.affichage = affichage.Affichage(self.ecran, self.attributs)
        
        self.partie = None
        
    ######################################################
    ### Accesseurs :
    ######################################################
    
    def acc_ecran(self) :
        return self.ecran
    
    
    ######################################################
    ### Boucle :
    ######################################################
        
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
                
                
                
            pygame.display.flip()
            self.horloge.tick(60)
        
        
        pygame.quit()

    ######################################################
    ### Initialisation du Jeu et de la fenêtre :
    ######################################################
        
    def jouer(self) :
        pygame.init()
        pygame.display.set_caption('Ball Challenge')
        #pygame.mouse.set_visible(False)
        #pygame.display.set_icon(pygame.image.load('medias/.png'))
        self.boucle()