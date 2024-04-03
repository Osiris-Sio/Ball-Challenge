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
    
    def __init__(self, ecran, les_attributs, le_controle) :
        assert isinstance(les_attributs, attributs.Attributs), 'Le paramètre doit être de la classe Attributs !'
        assert isinstance(le_controle, controle.Controle), 'Le paramètre doit être de la classe Controle !'
        
        self.ecran = ecran
        self.attributs = les_attributs
        self.controle = le_controle
        
        #Curseurs :
        self.curseurs = [
            pygame.image.load("ressources/curseur0.png"),
            pygame.image.load("ressources/curseur1.png")
        ]
        
        #Fonds :
        self.fonds = {
            'menu' : pygame.image.load("ressources/menu/fond.png"),
            'par_defaut' : pygame.image.load("ressources/fond_partie.png")
        }
        
        self.barre_partie = pygame.image.load("ressources/barre_partie.png")
        self.zone = pygame.image.load("ressources/zone.png")
        
        self.boutons = {
            'jouer' : pygame.image.load("ressources/menu/jouer.png") ,
            'options' : pygame.image.load("ressources/menu/options.png"),
            'quitter' : pygame.image.load("ressources/menu/quitter.png")
        }
        
        self.personnage = pygame.image.load("ressources/personnage.png")
    
    ### Curseur :
    
    def curseur(self) :
        if self.controle.acc_appuye() :
            self.ecran.blit(self.curseurs[1], self.controle.acc_position_curseur())
        else :
            self.ecran.blit(self.curseurs[0], self.controle.acc_position_curseur())
    
    ### Fonds :
    
    def fond_menu(self) :
        self.ecran.blit(self.fonds['menu'], (0, 0))
    
    def fond_partie(self) :
        self.ecran.blit(self.fonds['par_defaut'], (0, 0))
        self.ecran.blit(self.barre_partie, (0, 668))
        self.ecran.blit(self.zone, (100, 50))
        
    ### Boutons :
        
    def boutons_menu(self) :
        self.ecran.blit(self.boutons['jouer'], (410, 400))
        self.ecran.blit(self.boutons['options'], (410, 500))
        self.ecran.blit(self.boutons['quitter'], (410, 600))
        
    ### Personnage :
    
    def perso(self):
        self.ecran.blit(self.personnage, (10, 10))
        
        
    ### Menu et Partie :
    
    def menu(self) :
        self.fond_menu()
        self.boutons_menu()
        
        
        self.curseur()
        
        
    
    
    def partie(self) :
        self.fond_partie()
        self.perso()
        
        
        self.curseur()
    