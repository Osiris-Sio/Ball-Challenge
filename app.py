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
    
    def __init__(self):
        #Position :
        self.x = 160
        self.y = 37
        #Apparence :
        self.apparence = 0
        
    ###Accesseur :
    
    def acc_x(self):
        return self.x
    
    def acc_y(self):
        return self.y
    
    def acc_apparence(self):
        return self.apparence
    
    ###Changement apparence :
    
    def changement_apparence(self, valeur) :
        self.apparence += valeur
    
    ###Placement :
    
    def placer_menu(self):
        self.x = 160
        self.y = 37
        
    def placer_partie(self):
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
        
    ###Accesseur :
    
    def acc_x(self):
        return self.x
    
    def acc_y(self):
        return self.y
        
    ###Déplacement :
    
    def deplacer(self):
        self.x += self.dx
        self.y += self.dy
    
    ###Rebonds :
    
    def collisions(self, x_elt, y_elt) :
        tab_collisions_ball = [(-3, -3), (0, -3), (1, -3), (-3, 0), (0, 0), (3, 0), (-3, 3), (0, 3), (3, 3)]
        i = 0
        constat = False
        while i < len(tab_collisions_ball) and not constat :
            if x_elt < self.x + tab_collisions_ball[i][0] < x_elt + 8 and y_elt < self.y + tab_collisions_ball[i][1] < y_elt + 8:
                constat = True
            i += 1
        return constat
    
    def remplacer(self, tuple_dx_dy):
        self.dx = tuple_dx_dy[0] * self.vitesse
        self.dy = tuple_dx_dy[1] * self.vitesse
        pyxel.play(1, 1)
        
    def rebonds(self):
        if self.x - 4 < 0 :
            self.remplacer(random.choice([(1, -1), (2, 0), (1, 1)]))
        if self.x + 4 > 200 :
            self.remplacer(random.choice([(-1, -1), (-2, 0), (1, 1)]))
        if self.y - 4 < 0 :
            self.remplacer(random.choice([(-1, 1), (0, 1), (1, 1)]))
        if self.y + 4 > 60 :
            self.remplacer(random.choice([(-1, -1), (0, -1), (1, -1)]))
            
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
        
        #Apparence :
        self.ball_apparence = 1
        
        #Personnage :
        self.personnage = Personnage()
        
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
                self.personnage.placer_partie()
                self.tab_balls = [Ball(0.3, -1, 0, self.ball_apparence), Ball(0.3, 1, 0, self.ball_apparence)]
                self.piece = Piece(100, 35)
            
            #Plateforme :
            elif 179 <= pyxel.mouse_x <= 195 and 5 <= pyxel.mouse_y <= 21 :
                self.clavier = not self.clavier
                pyxel.mouse(self.clavier)
                
            #Zones Flèches :
            elif 55 <= pyxel.mouse_y <= 63 :
                
                #Gauche Ball :
                if 18 <= pyxel.mouse_x <= 26 and 1 < self.ball_apparence :
                    self.ball_apparence -= 1
                
                #Droite Ball :
                elif 34 <= pyxel.mouse_x <= 42 and self.ball_apparence < 15 :
                    self.ball_apparence += 1
                                    
                #Gauche Personnage :
                elif 152 <= pyxel.mouse_x <= 160 and 0 < self.personnage.acc_apparence() :
                    self.personnage.changement_apparence(-1)
                
                #Droite Personnage :
                elif 168 <= pyxel.mouse_x <= 176 and self.personnage.acc_apparence() < 7 :
                    self.personnage.changement_apparence(1)
    
    def bouton_retour(self):
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) :
            if 10 <= pyxel.mouse_x <= 58 and 69 <= pyxel.mouse_y <= 85 :
                self.tab_balls = []
                self.personnage.placer_menu()
                self.score = 0
                self.menu = True
                self.fin_partie = False
                    
    ###Contrôles :
                    
    def controle_clavier_manette(self):
        if (pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)) and self.personnage.acc_x() > 0:
            self.personnage.gauche()
        if (pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)) and self.personnage.acc_x() < 192 :
            self.personnage.droite()
        if (pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)) and self.personnage.acc_y() > 0:
            self.personnage.haut()
        if (pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)) and self.personnage.acc_y() < 52 :
            self.personnage.bas()
        
    def controle_tactile(self):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) :
            #Gauche :
            if 136 <= pyxel.mouse_x <= 152 and 76 <= pyxel.mouse_y <= 92 and self.personnage.acc_x() > 0:
                self.personnage.gauche()
            #Droite :
            if 168 <= pyxel.mouse_x <= 184 and 76 <= pyxel.mouse_y <= 92 and self.personnage.acc_x() < 192:
                self.personnage.droite()
            #Haut :
            if 152 <= pyxel.mouse_x <= 168 and 60 <= pyxel.mouse_y <= 76 and self.personnage.acc_y() > 0:
                self.personnage.haut()
            #Bas :
            if 152 <= pyxel.mouse_x <= 168 and 76 <= pyxel.mouse_y <= 92 and self.personnage.acc_y() < 52:
                self.personnage.bas()
    
    def controle_personnage(self):
        if self.clavier :
            self.controle_clavier_manette()
        else :
            self.controle_tactile()
         
    ###Balls :
            
    def actions_balls(self):
        for ball in self.tab_balls :
            ball.deplacer()
            ball.rebonds()
            
    ###Pièces :
            
    def prendre_piece(self):
        if self.piece.collisions(self.personnage.acc_x(), self.personnage.acc_y()) :
            pyxel.play(0, 2)
            self.piece = Piece(random.randint(5, 195), random.randint(5, 55))
            self.score += 1
            if self.score % 1 == 0 and self.score != 0:
                for ball in self.tab_balls:
                    ball.vitesse += 0.02
            
    ###Fin de partie :
        
    def est_fini(self):
        i = 0
        while i < len(self.tab_balls) and not self.fin_partie :
            if self.tab_balls[i].collisions(self.personnage.acc_x(), self.personnage.acc_y()) :
                self.fin_partie = True
                pyxel.play(0, 3)
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
            self.bouton_retour()
            
    ######################################################
    ### Affichages :
    ######################################################
    
    def afficher_intro(self) :
        pyxel.blt(84, 38, 0, 0, 56, 32, 16)
        pyxel.text(100, 55, 'Games', 7)
    
    def afficher_menu(self):
        #Version :
        pyxel.text(2, 85, '0.0.3', 7)
        
        #Titre :
        pyxel.rect(71, 18, 59, 9, 5)
        pyxel.rectb(71, 18, 59, 9, 7)
        pyxel.text(73, 20, 'Ball Challenge', 7)
        
        #Ball :
        pyxel.circ(30, 40, 3, self.ball_apparence)
        
        ###Boutons Ball :
        #Gauche :
        if 1 < self.ball_apparence :
            pyxel.blt(18, 55, 0, 0, 48, 8, 8)
        else :
            pyxel.blt(18, 55, 0, 16, 48, 8, 8)
        
        #Droite Ball :
        if self.ball_apparence < 15 :
            pyxel.blt(34, 55, 0, 8, 48, 8, 8)
        else :
            pyxel.blt(34, 55, 0, 24, 48, 8, 8)
        
        ###Boutons Personnage :
        #Gauche :
        if 0 < self.personnage.acc_apparence() :
            pyxel.blt(152, 55, 0, 0, 48, 8, 8)
        else :
            pyxel.blt(152, 55, 0, 16, 48, 8, 8)
        
        #Droite :
        if self.personnage.acc_apparence() < 7 :
            pyxel.blt(168, 55, 0, 8, 48, 8, 8)
        else :
            pyxel.blt(168, 55, 0, 24, 48, 8, 8)
        
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
        pyxel.rect(0, 60, 200, 33, 5)
        pyxel.rectb(0, 60, 200, 33, 7)
        pyxel.text(80, 80, 'Temps : ' + str(self.temps), 7)
        pyxel.text(80, 70, 'Score : ' + str(self.score), 7)
        
        #Bouton Retour :
        pyxel.blt(10, 69, 0, 0, 32, 48, 16)
        
        #Touche :
        if self.clavier :
            pyxel.blt(136, 60, 0, 0, 104, 48, 32, 0)
        else :
            pyxel.blt(136, 60, 0, 0, 72, 48, 32, 0)
          
    def afficher_balls(self):
        for ball in self.tab_balls :
            ball.afficher()
                
    def afficher_fin(self):
        pyxel.text(78, 18, 'Partie\n  Terminee', 7)
        
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