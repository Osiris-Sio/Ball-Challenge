# -*- coding: utf-8 -*-

'''
-> Ball Challenge

Auteur : AMEDRO Louis (alias Osiris Sio)
''' 

######################################################
### Importation Module :
######################################################

import pyxel

######################################################
### Classe Terrain :
######################################################

class Terrain() :
    
    def __init__(self, apparence):
        #Position :
        self.x = 30
        self.y = 5
        #Largeur/Hauteur :
        self.largeur = 140
        self.hauteur = 57
        #Apparence :
        self.apparence = apparence
        
    def par_defaut(self) :
        if self.x == 30 :
            self.x += 2
        if self.y == 5 :
            self.y += 2
        if self.largeur == 140:
            pass
        if self.hauteur == 57:
            pass
         
    def reduire():
        pass

    def afficher(self):
        pyxel.rectb(self.x, self.y, self.largeur, self.hauteur, 5)

######################################################
### Classe Personnage :
######################################################

class Personnage() :
    
    def __init__(self, apparence):
        #Position :
        self.x = 50
        self.y = 50
        #Apparence :
        self.apparence = apparence
        
    ###Mouvements :
    
    def gauche(self):
        self.x -= 0.5
        
    def droite(self):
        self.x += 0.5
        
    def haut(self):
        self.y -= 0.5
        
    def bas(self):
        self.y += 0.5
        
    ###Affichage :
    
    def afficher(self):
        dic = {
            0 : pyxel.blt(self.x, self.y, 1, 8, 24, 8, 8, 0)
        }
        dic[self.apparence]
        
######################################################
### Classe Ball :
######################################################

class Ball() :
    
    def __init__(self, apparence):
        #Position :
        self.x = 70
        self.y = 100
        #Apparence :
        self.apparence = apparence
        
    def collisions(self) :
        pass
    
    def afficher(self):
        pass

######################################################
### Classe Jeu :
######################################################

class Jeu() :
    
    def __init__(self) :
        #Menu :
        self.menu = True
        self.clavier = True
        
        #Casier :
        self.personnage_apparence = 0
        self.terrain_apparence = 0
        
        #Partie :
        self.score = 0
        
        #Initialisation de la fenêtre Pyxel 41, 23 /:
        pyxel.init(200, 92, title='Ball Challenge', fps=60, capture_scale=3, capture_sec=0)
        pyxel.mouse(True)
        pyxel.load('res.pyxres')
        pyxel.run(self.calculs, self.affichages)
    
    ######################################################
    ### Calculs :
    ######################################################
    
    ###Boutons :
    
    def boutons_menu(self):
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) :
            #Zone des boutons Jouer/Casier :
            if 65 <= pyxel.mouse_y <= 81 :
                #Casier :
                if 25 <= pyxel.mouse_x <= 73 :
                    print('casier ouvert')
                #Jouer :
                elif 125 <= pyxel.mouse_x <= 173 :
                    self.menu = False
                    self.terrain = Terrain(self.terrain_apparence)
                    self.personnage = Personnage(self.personnage_apparence)
            #Bouton Plateforme :
            if 179 <= pyxel.mouse_x <= 195 and 5 <= pyxel.mouse_y <= 21 :
                self.clavier = not self.clavier
                #pyxel.mouse(self.clavier)
                    
    ###Contrôles :
                    
    def controle_clavier(self):
        if pyxel.btn(pyxel.KEY_LEFT) :
            self.personnage.gauche()
        if pyxel.btn(pyxel.KEY_RIGHT) :
            self.personnage.droite()
        if pyxel.btn(pyxel.KEY_UP) :
            self.personnage.haut()
        if pyxel.btn(pyxel.KEY_DOWN) :
            self.personnage.bas()
        
    def controle_tactile(self):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) :
            #Gauche :
            if 168 <= pyxel.mouse_x <= 180 and 60 <= pyxel.mouse_y <= 92 :
                self.personnage.gauche()
            #Droite :
            if 188 <= pyxel.mouse_x <= 200 and 60 <= pyxel.mouse_y <= 92 :
                self.personnage.droite()
            #Haut :
            if 168 <= pyxel.mouse_x <= 200 and 60 <= pyxel.mouse_y <= 72 :
                self.personnage.haut()
            #Bas :
            if 168 <= pyxel.mouse_x <= 200 and 78 <= pyxel.mouse_y <= 92 :
                self.personnage.bas()
    
    def controle_personnage(self):
        if self.clavier :
            self.controle_clavier()
        else :
            self.controle_tactile()
    
    ###Calculs :
       
    def calculs(self) :
        
        ### Menu :
        if self.menu :
            self.boutons_menu()
        
        ### Partie :
        else :
            self.controle_personnage()
    
    ######################################################
    ### Affichages :
    ### blt(x, y, img, u, v, w, h, [colkey])
    ### text(x, y, s, col)
    ######################################################
    
    def afficher_menu(self):
        #Textes :
        pyxel.text(72, 18, 'Ball Challenge', 5)
        pyxel.text(74, 20, 'Ball Challenge', 12)
        #Boutons Jouer/Casier:
        pyxel.blt(25, 65, 0, 0, 16, 48, 16)
        pyxel.blt(125, 65, 0, 0, 0, 48, 16)
        #Bouton Plateforme :
        dic = {
            True : 0,
            False : 16
        }
        pyxel.blt(179, 5, 0, dic[self.clavier], 32, 16, 16)
        
    def afficher_partie(self):
        #Score :
        pyxel.rect(0, 82, 200, 40, 12)
        pyxel.rectb(0, 82, 200, 40, 5)
        pyxel.text(77, 85, 'Score : ' + str(self.score), 0)
        
        #Tactile :
        if not self.clavier :
            pyxel.blt(168, 60, 0, 0, 48, 32, 32, 0)
            if 168 <= pyxel.mouse_x <= 200 and 60 <= pyxel.mouse_y <= 92 :
                pyxel.blt(pyxel.mouse_x - 2, pyxel.mouse_y - 2, 0, 32, 48, 8, 8, 0)
            else :
                pyxel.blt(180, 72, 0, 32, 48, 8, 8, 0)
        
          
    def affichages(self):
        #Fond Noir :
        pyxel.cls(0)
        
        ### Menu :
        if self.menu :
            self.afficher_menu()
        
        ### Partie :
        else :
            self.afficher_partie()
            self.terrain.afficher()
            self.personnage.afficher()
        
Jeu()