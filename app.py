# -*- coding: utf-8 -*-

'''
-> Ball Challenge

Auteur : AMEDRO Louis (alias Osiris Sio)
''' 

######################################################
### Importation Module :
######################################################

import pyxel, random, time

######################################################
### Classe Personnage :
######################################################

class Personnage() :
    
    def __init__(self, apparence):
        #Position :
        self.x = 95
        self.y = 20
        #Apparence :
        self.apparence = apparence
        #Collisions :
        self.tab_collisions = [(0, 0), (4, 0), (8, 0), (0, 4), (0, 8), (4, 4), (8, 4), (4, 8), (8, 8)]
        
    ###Accesseur :
    
    def acc_x(self):
        return self.x
    
    def acc_y(self):
        return self.y
    
    def acc_tab_collisions(self):
        return self.tab_collisions
        
    ###Mouvements :
    
    def gauche(self):
        self.x -= 1
        
    def droite(self):
        self.x += 1
        
    def haut(self):
        self.y -= 1
        
    def bas(self):
        self.y += 1
        
    ###Affichage :
    
    def afficher(self):
        dic = {
            0 : pyxel.blt(self.x, self.y, 1, 8, 24, 8, 8, 0)
        }
        dic[self.apparence]
        
######################################################
### Classe Pièce :
######################################################

class Piece() :
    
    def __init__(self, x, y):
        #Position :
        self.x = x
        self.y = y
        
    def collisions(self, x_perso, y_perso, tab_collisions_perso) :
        return x_perso < self.x < x_perso + 8 and y_perso < self.y < y_perso + 8
    
    def afficher(self):
        pyxel.circ(self.x, self.y, 1, 10)
        
######################################################
### Classe Ball :
######################################################

class Ball() :
    
    def __init__(self, vitesse, dx, dy, apparence):
        #Position :
        self.x = 95
        self.y = 50
        #Vitesse multiplicateur:
        self.vitesse = vitesse
        #Directions :
        self.dx = dx * self.vitesse
        self.dy = dy * self.vitesse
        #Apparence :
        self.apparence = apparence
        
    ###Déplacement :
    
    def deplacer(self):
        self.x += self.dx
        self.y += self.dy
    
    ###Rebonds :
    
    def remplacer(self, tuple_dx_dy):
        self.dx = tuple_dx_dy[0] * self.vitesse
        self.dy = tuple_dx_dy[1] * self.vitesse
        
    def rebonds_ball(self):
        pass
        
    def rebonds(self):
        if self.x - 4 < 0 :
            self.remplacer(random.choice([(1, -1), (2, 0), (1, 1)]))
        if self.x + 4 > 200 :
            self.remplacer(random.choice([(-1, -1), (-2, 0), (1, 1)]))
        if self.y - 4 < 0 :
            self.remplacer(random.choice([(-1, 1), (0, 1), (1, 1)]))
        if self.y + 4 > 60 :
            self.remplacer(random.choice([(-1, -1), (0, -1), (1, -1)]))
        self.rebonds_ball()
        
    def collisions(self, x_perso, y_perso, tab_collisions_perso) :
        constat = False
        i = 0
        while i < len(tab_collisions_perso) and not constat :
            if self.x - 3 < x_perso + tab_collisions_perso[i][0] < self.x + 3 and self.y - 3 < y_perso + tab_collisions_perso[i][0] < self.y + 3 :
                constat = True
            i += 1
        return constat
    
    def afficher(self):
        pyxel.circ(self.x, self.y, 3, self.apparence)

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
        self.ball_apparence = 9
        
        #Partie :
        self.temps = 0
        self.score = 0
        self.tab_balls = []
        self.fin_partie = False
        
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
                    self.temps_commence = time.time()
                    self.personnage = Personnage(self.personnage_apparence)
                    self.piece = Piece(95, 35)
                    self.tab_balls = [Ball(0.3, -1, 0, self.ball_apparence), Ball(0.3, 1, 0, self.ball_apparence)]
            #Bouton Plateforme :
            if 179 <= pyxel.mouse_x <= 195 and 5 <= pyxel.mouse_y <= 21 :
                self.clavier = not self.clavier
                #pyxel.mouse(self.clavier)
                    
    ###Contrôles :
                    
    def controle_clavier(self):
        if pyxel.btn(pyxel.KEY_Q) and self.personnage.acc_x() > 0:
            self.personnage.gauche()
        if pyxel.btn(pyxel.KEY_D) and self.personnage.acc_x() < 192 :
            self.personnage.droite()
        if pyxel.btn(pyxel.KEY_Z) and self.personnage.acc_y() > 0:
            self.personnage.haut()
        if pyxel.btn(pyxel.KEY_S) and self.personnage.acc_y() < 52 :
            self.personnage.bas()
        
    def controle_tactile(self):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) :
            #Gauche :
            if 168 <= pyxel.mouse_x <= 180 and 60 <= pyxel.mouse_y <= 92:
                self.personnage.gauche()
            #Droite :
            if 188 <= pyxel.mouse_x <= 200 and 60 <= pyxel.mouse_y <= 92:
                self.personnage.droite()
            #Haut :
            if 168 <= pyxel.mouse_x <= 200 and 60 <= pyxel.mouse_y <= 72:
                self.personnage.haut()
            #Bas :
            if 168 <= pyxel.mouse_x <= 200 and 78 <= pyxel.mouse_y <= 92  and self.personnage.acc_y() < 52:
                self.personnage.bas()
    
    def controle_personnage(self):
        if self.clavier :
            self.controle_clavier()
        else :
            self.controle_tactile()
            
    def actions_balls(self):
        for ball in self.tab_balls :
            ball.deplacer()
            ball.rebonds()
            
    def prendre_piece(self):
        if self.piece.collisions(self.personnage.acc_x(), self.personnage.acc_y(), self.personnage.acc_tab_collisions()) :
            self.piece = Piece(random.randint(5, 195), random.randint(5, 55))
            self.score += 1
            if self.score % 1 == 0 and self.score != 0:
                for ball in self.tab_balls:
                    ball.vitesse += 0.02
            
    def est_fini(self):
        i = 0
        while i < len(self.tab_balls) and not self.fin_partie :
            if self.tab_balls[i].collisions(self.personnage.acc_x(), self.personnage.acc_y(), self.personnage.acc_tab_collisions()) :
                self.fin_partie = True
            i += 1
        return self.fin_partie
    
    ###Calculs :
       
    def calculs(self) :
        
        ### Menu :
        if self.menu :
            self.boutons_menu()
        
        ### Partie :
        else :
            if not self.est_fini() :
                self.controle_personnage()
                self.actions_balls()
                self.prendre_piece()
                self.temps = int(time.time() - self.temps_commence)
            
    ######################################################
    ### Affichages :
    ### blt(x, y, img, u, v, w, h, [colkey])
    ### text(x, y, s, col)
    ######################################################
    
    def afficher_menu(self):
        #Textes :
        pyxel.rect(72, 18, 59, 9, 12)
        pyxel.rectb(72, 18, 59, 9, 5)
        pyxel.text(74, 20, 'Ball Challenge', 0)
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
        #Information :
        pyxel.rect(0, 60, 200, 33, 12)
        pyxel.rectb(0, 60, 200, 33, 5)
        pyxel.text(80, 80, 'Temps : ' + str(self.temps), 0)
        pyxel.text(80, 70, 'Score : ' + str(self.score), 0)
        
        #Tactile :
        if not self.clavier :
            pyxel.blt(168, 60, 0, 0, 48, 32, 32, 0)
            if 168 <= pyxel.mouse_x <= 200 and 60 <= pyxel.mouse_y <= 92 :
                pyxel.blt(pyxel.mouse_x - 2, pyxel.mouse_y - 2, 0, 32, 48, 8, 8, 0)
            else :
                pyxel.blt(180, 72, 0, 32, 48, 8, 8, 0)
            
    def afficher_balls(self):
        for ball in self.tab_balls :
            ball.afficher()
                
    def afficher_fin(self):
        pyxel.text(78, 18, 'Partie\n  Terminee', self.ball_apparence)
        
    def affichages(self):
        #Fond Noir :
        pyxel.cls(0)
        
        ### Menu :
        if self.menu :
            self.afficher_menu()
        
        ### Partie :
        else :
            self.afficher_partie()
            if not self.fin_partie :
                self.piece.afficher()
                self.personnage.afficher()
                self.afficher_balls()
            else :
                self.afficher_fin()
                
Jeu()