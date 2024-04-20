# -*- coding: utf-8 -*-

'''
-> Ball Challenge

Studio : I.V.L Games (Innovation, Vision and Liberty Games)
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
        self.x = 150
        self.y = 30
        #Apparence :
        self.apparence = apparence
        
    ###Accesseur :
    
    def acc_x(self):
        return self.x
    
    def acc_y(self):
        return self.y
    
    ###Placement de la partie :
    
    def placer_correctement(self):
        self.x = 96
        self.y = 20
        
    ###Mouvements :
    
    def gauche(self, vitesse = 1):
        self.x -= vitesse
        
    def droite(self, vitesse = 1):
        self.x += vitesse
        
    def haut(self, vitesse = 1):
        self.y -= vitesse
        
    def bas(self, vitesse = 1):
        self.y += vitesse
        
    ###Affichage :
    
    def afficher(self):
        pyxel.blt(self.x, self.y, 1, 0, 8 * self.apparence, 8, 8, 0)
        
######################################################
### Classe Pièce :
######################################################

class Piece() :
    
    def __init__(self, x, y):
        #Position :
        self.x = x
        self.y = y
        
    def collisions(self, x_perso, y_perso) :
        tab_collisions_piece = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        i = 0
        constat = False
        while i < len(tab_collisions_piece) and not constat :
            if x_perso < self.x + tab_collisions_piece[i][0] < x_perso + 8 and y_perso < self.y + tab_collisions_piece[i][1] < y_perso + 8:
                constat = True
            i += 1
        return constat
    
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
        
    def collisions(self, x_perso, y_perso) :
        tab_collisions_ball = [(-3, -3), (0, -3), (1, -3), (-3, 0), (0, 0), (3, 0), (-3, 3), (0, 3), (3, 3)]
        i = 0
        constat = False
        while i < len(tab_collisions_ball) and not constat :
            if x_perso < self.x + tab_collisions_ball[i][0] < x_perso + 8 and y_perso < self.y + tab_collisions_ball[i][1] < y_perso + 8:
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
        
        #Intro :
        self.intro = True
        self.temps_commence_intro = time.time()
        
        #Menu :
        self.menu = False
        self.clavier = True
        
        #Apparences :
        self.personnage_apparence = 4
        self.ball_apparence = 7
        
        #Personnage :
        self.personnage = Personnage(self.personnage_apparence)
        
        #Partie :
        self.temps = 0
        self.score = 0
        self.fin_partie = False
        
        #Initialisation de la fenêtre Pyxel 41, 23 /:
        pyxel.init(200, 92, title='Ball Challenge', fps=60, capture_scale=3, capture_sec=0)
        pyxel.mouse(True)
        pyxel.load('ressources.pyxres')
        pyxel.playm(0)
        pyxel.run(self.calculs, self.affichages)
    
    ######################################################
    ### Calculs :
    ######################################################
    
    ###Intro :
    
    def finir_intro(self):
        if time.time() - self.temps_commence_intro >= 2 :
            self.intro = False
            self.menu = True
    
    ###Boutons :
    
    def boutons_menu(self):
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) :
            
            #Jouer :
            if 76 <= pyxel.mouse_x <= 124 and 65 <= pyxel.mouse_y <= 81:
                self.menu = False
                self.temps_commence = time.time()
                self.personnage.placer_correctement()
                self.tab_balls = [Ball(0.3, -1, 0, self.ball_apparence), Ball(0.3, 1, 0, self.ball_apparence)]
                self.piece = Piece(95, 35)
            
            #Plateforme :
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
            if 170 <= pyxel.mouse_x <= 180 and 72 <= pyxel.mouse_y <= 80 and self.personnage.acc_x() > 0:
                self.personnage.gauche()
            #Droite :
            if 188 <= pyxel.mouse_x <= 198 and 72 <= pyxel.mouse_y <= 80 and self.personnage.acc_x() < 192:
                self.personnage.droite()
            #Haut :
            if 180 <= pyxel.mouse_x <= 188 and 62 <= pyxel.mouse_y <= 72 and self.personnage.acc_y() > 0:
                self.personnage.haut()
            #Bas :
            if 180 <= pyxel.mouse_x <= 188 and 80 <= pyxel.mouse_y <= 90 and self.personnage.acc_y() < 52:
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
        if self.piece.collisions(self.personnage.acc_x(), self.personnage.acc_y()) :
            self.piece = Piece(random.randint(5, 195), random.randint(5, 55))
            self.score += 1
            if self.score % 1 == 0 and self.score != 0:
                for ball in self.tab_balls:
                    ball.vitesse += 0.02
            
    def est_fini(self):
        i = 0
        while i < len(self.tab_balls) and not self.fin_partie :
            if self.tab_balls[i].collisions(self.personnage.acc_x(), self.personnage.acc_y()) :
                self.fin_partie = True
            i += 1
        return self.fin_partie
    
    ###Calculs :
       
    def calculs(self) :
        
        ### Intro :
        if self.intro :
            self.finir_intro()
        
        ### Menu :
        elif self.menu :
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
    
    def afficher_intro(self) :
        pyxel.blt(84, 38, 0, 0, 56, 32, 16)
        pyxel.text(100, 55, 'Studio', 7)
    
    def afficher_menu(self):
        #Textes :
        pyxel.rect(71, 18, 59, 9, 5)
        pyxel.rectb(71, 18, 59, 9, 7)
        pyxel.text(73, 20, 'Ball Challenge', 7)
        
        #Ball :
        pyxel.circ(30, 30, 3, self.ball_apparence)
        
        #Boutons Jouer:
        pyxel.blt(76, 65, 0, 0, 0, 48, 16)
        
        #Bouton Plateforme :
        dic = {
            True : 0,
            False : 16
        }
        pyxel.blt(179, 5, 0, dic[self.clavier], 16, 16, 16)
        
    def afficher_partie(self):      
        #Information :
        pyxel.rect(0, 60, 200, 33, 12)
        pyxel.rectb(0, 60, 200, 33, 5)
        pyxel.text(80, 80, 'Temps : ' + str(self.temps), 0)
        pyxel.text(80, 70, 'Score : ' + str(self.score), 0)
        
        #Tactile :
        if not self.clavier :
            pyxel.blt(172, 64, 0, 0, 32, 24, 24, 0)
            
    def afficher_balls(self):
        for ball in self.tab_balls :
            ball.afficher()
                
    def afficher_fin(self):
        pyxel.text(78, 18, 'Partie\n  Terminee', self.ball_apparence)
        
    def affichages(self):
        #Fond Noir :
        pyxel.cls(0)
        
        if self.intro :
            self.afficher_intro()
        
        ### Menu :
        elif self.menu :
            self.afficher_menu()
            self.personnage.afficher()
        
        ### Partie :
        else :
            self.afficher_partie()
            if not self.fin_partie :
                self.piece.afficher()
                self.personnage.afficher()
                self.afficher_balls()
            else :
                self.afficher_fin()
                
Jeu() #Lancement du jeu automatiquement