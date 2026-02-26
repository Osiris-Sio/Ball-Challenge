# -*- coding: utf-8 -*-

'''
Ball Challenge

Studio : Osiris Games
Auteur : AMEDRO Louis (alias Osiris Sio)

licence CC BY SA
''' 

import pyxel, random, time, math

# ==========================================
# CONSTANTES & CONFIGURATION
# ==========================================
ECRAN_L = 200
ECRAN_H = 92
FPS = 60

# Limites du Jeu
LIMITE_MIN_X = 0
LIMITE_MAX_X = ECRAN_L - 8
LIMITE_MIN_Y = 0
LIMITE_MAX_Y = ECRAN_H - 12 

# Couleurs (Palette Pyxel)
COL_NOIR = 0
COL_BLANC = 7
COL_JAUNE = 10
COL_ROUGE = 8
COL_BLEU = 12
COL_GRIS = 13

# Couleurs contrastées pour les contours des balles
COULEURS_CONTRASTE = {
    0: 7,  1: 10, 2: 10, 3: 7,  4: 7,  5: 10, 6: 7,  7: 2,
    8: 7,  9: 7,  10: 12, 11: 8, 12: 10, 13: 7, 14: 1, 15: 1
}

# ==========================================
# UTILITAIRES
# ==========================================

def verifier_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    """
    Détection de collision AABB.
    Retourne Vrai si les rectangles se chevauchent.
    """
    return (x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2)

def dessiner_pilule(x, y, w, h, col_fond, col_mur):
    """Dessine une forme de 'pilule' vide."""
    r = h // 2
    # Corps principal (rectangles)
    pyxel.rect(x + r, y, w - 2*r, h, col_mur)         # Haut/Bas murs
    pyxel.circ(x + r, y + r, r, col_mur)              # Cercle Gauche
    pyxel.circ(x + w - r - 1, y + r, r, col_mur)      # Cercle Droit (ajustement -1 pour symétrie pixel)
    
    # Évidement (pour faire le contour)
    # On dessine la même chose en plus petit en 'gommant' avec col_fond
    # Epaisseur du trait ~ 2px
    t = 2 
    pyxel.circ(x + r, y + r, r - t, col_fond)
    pyxel.circ(x + w - r - 1, y + r, r - t, col_fond)
    pyxel.rect(x + r, y + t, w - 2*r, h - 2*t, col_fond)



# ==========================================
# SYSTÈME DE PARTICULES
# ==========================================

class Particule:
    def __init__(self, x, y, dx, dy, vie, couleur, mode="pixel"):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.vie = vie
        self.vie_max = vie
        self.couleur = couleur
        self.mode = mode # "pixel" ou "ligne"

    def mettre_a_jour(self):
        self.x += self.dx
        self.y += self.dy
        self.vie -= 1

    def dessiner(self):
        if self.mode == "ligne":
            # Dessine une petite traînée
            queue_x = self.x - self.dx 
            queue_y = self.y - self.dy
            pyxel.line(self.x, self.y, queue_x, queue_y, self.couleur)
        else:
            pyxel.pset(self.x, self.y, self.couleur)

class GestionnaireParticules:
    def __init__(self):
        self.particules = []

    def ajouter_effet_air(self, x, y, direction, est_balle=False):
        """
        Génère de petites lignes blanches pour simuler l'air.
        est_balle: Si vrai, effet plus petit.
        """
        seuil = 0.5 if est_balle else 0.4
        if random.random() > seuil: return 
        
        # Centre approximatif
        if est_balle:
             # Balle 6x6 -> centre +3
             px, py = x + 3, y + 3
             vie = 4 
        else:
             # Perso 8x8 -> centre +4
             px, py = x + 4, y + 4
             vie = 6
             
        # Offset selon direction
        dx, dy = 0, 0
        if direction == 'gauche':
            dx, dy = random.uniform(0.5, 1.0), random.uniform(-0.3, 0.3)
            # Décalage visuel opposé au mouvement
            start_x = px + (3 if est_balle else 4)
            start_y = py
        elif direction == 'droite':
            dx, dy = random.uniform(-1.0, -0.5), random.uniform(-0.3, 0.3)
            start_x = px - (3 if est_balle else 4)
            start_y = py
        elif direction == 'haut':
            dx, dy = random.uniform(-0.3, 0.3), random.uniform(0.5, 1.0)
            start_x = px
            start_y = py + (3 if est_balle else 4)
        elif direction == 'bas':
             dx, dy = random.uniform(-0.3, 0.3), random.uniform(-1.0, -0.5)
             start_x = px
             start_y = py - (3 if est_balle else 4)
        else:
            start_x, start_y = px, py 

        if est_balle:
             # Réduire vitesse pour balle
             dx *= 0.8
             dy *= 0.8

        self.particules.append(Particule(start_x, start_y, dx, dy, vie, COL_BLANC, "ligne"))

    def ajouter_impact_mur(self, x, y, normal_x, normal_y):
        """Génère une explosion de particules contre un mur."""
        nombre = 8 # Remis un peu plus nombreux
        for _ in range(nombre):
            vitesse = random.uniform(1.0, 2.5) # Vitesse un peu augmentée
            
            # La direction de base reflète la normale du mur
            dx = normal_x * vitesse + random.uniform(-0.8, 0.8)
            dy = normal_y * vitesse + random.uniform(-0.8, 0.8)
            
            # Vie et taille un peu plus grandes comme demandé
            vie = random.randint(8, 15)
            self.particules.append(Particule(x, y, dx, dy, vie, random.choice([COL_BLANC, COL_JAUNE]), "pixel"))

    def ajouter_effet_piece(self, x, y):
        """Effet scintillant lors de la collecte d'une pièce. (Minimisé)"""
        nombre = 6 # Réduit de 12 à 6
        for _ in range(nombre):
            angle = random.uniform(0, math.pi * 2)
            vitesse = random.uniform(0.5, 1.5) # Réduit vitesse
            dx = math.cos(angle) * vitesse
            dy = math.sin(angle) * vitesse
            # Vie réduite (5-10 au lieu de 10-20)
            self.particules.append(Particule(x, y, dx, dy, random.randint(5, 10), COL_JAUNE, "pixel"))


    def mettre_a_jour(self):
        # Mettre à jour et filtrer les particules mortes
        self.particules = [p for p in self.particules if p.vie > 0]
        for p in self.particules:
            p.mettre_a_jour()

    def dessiner(self):
        for p in self.particules:
            p.dessiner()

# Gestionnaire global (géré dans Jeu)
particules = None 

# ==========================================
# CLASSES DU JEU
# ==========================================

class Personnage:
    def __init__(self):
        self.x = 160
        self.y = 37
        self.w = 8
        self.h = 8
        self.apparence = 0
        
    def placer_menu(self):
        self.x, self.y = 160, 37
        
    def placer_partie(self):
        self.x, self.y = 96, 20
        
    def gauche(self, vitesse=1):
        if self.x > 0:
            self.x -= vitesse
            particules.ajouter_effet_air(self.x, self.y, 'gauche')
        
    def droite(self, vitesse=1):
        if self.x < ECRAN_L - self.w:
            self.x += vitesse
            particules.ajouter_effet_air(self.x, self.y, 'droite')
        
    def haut(self, vitesse=1):
        if self.y > 0:
            self.y -= vitesse
            particules.ajouter_effet_air(self.x, self.y, 'haut')
        
    def bas(self, vitesse=1):
        if self.y < 52: 
            self.y += vitesse
            particules.ajouter_effet_air(self.x, self.y, 'bas')

    def changement_apparence(self, val):
        self.apparence = max(0, min(11, self.apparence + val))
        
    def afficher(self):
        pyxel.blt(self.x, self.y, 1, 0, 8 * self.apparence, 8, 8, 0)

class Piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 2 
        self.h = 2
        
    def verifier_collision(self, mk_x, mk_y):
        return verifier_collision(self.x - 1, self.y - 1, 4, 4, mk_x, mk_y, 8, 8)
    
    def faire_reapparaitre(self):
        self.x = random.randint(5, 195)
        self.y = random.randint(5, 55)

    def afficher(self):
        pyxel.circ(self.x, self.y, 1, 10)

class Balle:
    def __init__(self, vitesse, dx, dy, apparence):
        self.x = 100
        self.y = 50
        self.w = 6 
        self.h = 6 
        self.vitesse = vitesse
        self.dx = dx * self.vitesse
        self.dy = dy * self.vitesse
        self.apparence = apparence
        
    def deplacer(self):
        self.x += self.dx
        self.y += self.dy
    
    def verifier_collision(self, mk_x, mk_y):
        return verifier_collision(self.x - 3, self.y - 3, 6, 6, mk_x, mk_y, 8, 8)

    def remplacer(self, tuple_dx_dy):
        self.dx = tuple_dx_dy[0] * self.vitesse
        self.dy = tuple_dx_dy[1] * self.vitesse
        pyxel.play(1, 1)

    def rebonds(self):
        touche = False
        # Mur Gauche
        if self.x - 3 < 0:
            self.remplacer(random.choice([(1, -1), (2, 0), (1, 1)]))
            particules.ajouter_impact_mur(0, self.y, 1, 0)
            touche = True
        
        # Mur Droit
        elif self.x + 3 > ECRAN_L:
            self.remplacer(random.choice([(-1, -1), (-2, 0), (1, 1)]))
            particules.ajouter_impact_mur(ECRAN_L, self.y, -1, 0)
            touche = True
            
        # Mur Haut
        if self.y - 3 < 0:
            self.remplacer(random.choice([(-1, 1), (0, 1), (1, 1)]))
            particules.ajouter_impact_mur(self.x, 0, 0, 1)
            touche = True
            
        # Mur Bas (Limite zone de jeu ~60)
        elif self.y + 3 > 60:
            self.remplacer(random.choice([(-1, -1), (0, -1), (1, -1)]))
            particules.ajouter_impact_mur(self.x, 60, 0, -1)
            touche = True
            
    def afficher(self):
        # Couleur contour
        col_contour = COULEURS_CONTRASTE.get(self.apparence, 7)
        # Cercle plein (contour)
        pyxel.circ(self.x, self.y, 3, col_contour)
        # Cercle interieur (couleur balle, plus petit de 1px)
        pyxel.circ(self.x, self.y, 2, self.apparence)

# ==========================================
# CLASSE PRINCIPALE JEU
# ==========================================

class Jeu:
    def __init__(self):
        global particules
        particules = GestionnaireParticules()

        # Moteur
        pyxel.init(ECRAN_L, ECRAN_H, title='Ball Challenge', fps=FPS, capture_scale=3, capture_sec=0)
        pyxel.mouse(True)
        try:
            pyxel.load('ressources.pyxres')
        except:
            pass 

        # États
        self.etat = "INTRO" # INTRO, AVERTISSEMENT, MENU, JEU, FIN
        self.temps_debut_intro = time.time()
        self.temps_debut_avertissement = 0
        
        # Config
        self.clavier = True
        self.balle_apparence = 1
        self.nombre_balles = 2
        
        # Entités
        self.personnage = Personnage()
        self.piece = Piece(100, 35)
        self.tab_balles = []
        
        # Données Jeu
        self.score = 0
        self.temps_debut = 0
        self.temps_actuel = 0
        
        # Audio
        pyxel.playm(0) 
        
        pyxel.run(self.mettre_a_jour, self.dessiner)
        
    # --------------------------------------
    # LOGIQUE
    # --------------------------------------
    
    def lancer_partie(self):
        self.etat = "JEU"
        self.personnage.placer_partie()
        self.temps_debut = time.time()
        self.score = 0
        
        # Création balles
        balles_base = [
            Balle(0.3, -1, 0, self.balle_apparence),
            Balle(0.3, 1, 0, self.balle_apparence),
            Balle(0.3, 0, 1, self.balle_apparence)
        ]
        self.tab_balles = balles_base[:self.nombre_balles]
        self.piece = Piece(100, 35)

    def retour_menu(self):
        self.etat = "MENU"
        self.personnage.placer_menu()
        self.tab_balles = []
        
    def gestion_intro(self):
        if time.time() - self.temps_debut_intro >= 2: 
            self.etat = "AVERTISSEMENT"
            self.temps_debut_avertissement = time.time()

    def gestion_avertissement(self):
        if time.time() - self.temps_debut_avertissement >= 5:
            self.retour_menu()

    def gestion_menu(self):
        # Souris
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            
            # Bouton JOUER
            if 76 <= mx <= 124 and 65 <= my <= 81:
                self.lancer_partie()
                
            # Switch Clavier/Souris
            elif 179 <= mx <= 195 and 5 <= my <= 21:
                self.clavier = not self.clavier
                pyxel.mouse(self.clavier)
            
            # Ligne Paramètres
            elif 55 <= my <= 63:
                # Apparence Balle
                if 18 <= mx <= 26 and self.balle_apparence > 1:
                    self.balle_apparence -= 1
                elif 34 <= mx <= 42 and self.balle_apparence < 15:
                    self.balle_apparence += 1
                # Apparence Perso
                elif 152 <= mx <= 160: 
                    self.personnage.changement_apparence(-1)
                elif 168 <= mx <= 176:
                    self.personnage.changement_apparence(1)
            
            # Ligne Nombre Balles
            elif 45 <= my <= 53:
                if 18 <= mx <= 26 and self.nombre_balles > 1:
                    self.nombre_balles -= 1
                elif 34 <= mx <= 42 and self.nombre_balles < 3:
                     self.nombre_balles += 1

    def gestion_jeu(self):
        # Contrôles
        if self.clavier:
            if (pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)): self.personnage.gauche()
            if (pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)): self.personnage.droite()
            if (pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)): self.personnage.haut()
            if (pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)): self.personnage.bas()
        else:
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                 if 136 <= mx <= 152 and 76 <= my <= 92: self.personnage.gauche()
                 if 168 <= mx <= 184 and 76 <= my <= 92: self.personnage.droite()
                 if 152 <= mx <= 168 and 60 <= my <= 76: self.personnage.haut()
                 if 152 <= mx <= 168 and 76 <= my <= 92: self.personnage.bas()

        # Balles
        for balle in self.tab_balles:
            balle.deplacer()
            balle.rebonds()
            if balle.verifier_collision(self.personnage.x, self.personnage.y):
                self.etat = "FIN"
                pyxel.play(0, 3)

        # Pièce
        if self.piece.verifier_collision(self.personnage.x, self.personnage.y):
            particules.ajouter_effet_piece(self.piece.x, self.piece.y)
            pyxel.play(0, 2)
            self.piece.faire_reapparaitre()
            self.score += 1
            if self.score > 0 and self.score % 1 == 0:
                for b in self.tab_balles: b.vitesse += 0.02

        # Chrono
        self.temps_actuel = int(time.time() - self.temps_debut)
        
        # Boutons Retour/Rejouer en jeu
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
             if 69 <= pyxel.mouse_y <= 85:
                 if 10 <= pyxel.mouse_x <= 26: self.retour_menu()
                 elif 32 <= pyxel.mouse_x <= 48: 
                     self.retour_menu()
                     self.lancer_partie()

    def gestion_fin(self):
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
             if 69 <= pyxel.mouse_y <= 85:
                 if 10 <= pyxel.mouse_x <= 26: self.retour_menu()
                 elif 32 <= pyxel.mouse_x <= 48: 
                     self.retour_menu()
                     self.lancer_partie()

    def mettre_a_jour(self):
        particules.mettre_a_jour()

        if self.etat == "INTRO":
            self.gestion_intro()
        elif self.etat == "AVERTISSEMENT":
            self.gestion_avertissement()
        elif self.etat == "MENU":
            self.gestion_menu()
        elif self.etat == "JEU":
            self.gestion_jeu()
        elif self.etat == "FIN":
            self.gestion_fin() 

    # --------------------------------------
    # AFFICHAGE
    # --------------------------------------

    def dessiner_intro(self):
        # Logo
        # Centre
        cx, cy = ECRAN_L // 2, ECRAN_H // 2
        
        # On dessine la "pilule" grise
        # Largeur ~70, Hauteur ~20
        largeur_pilule = 74
        hauteur_pilule = 18
        px = cx - largeur_pilule // 2
        py = cy - hauteur_pilule // 2
        
        dessiner_pilule(px, py, largeur_pilule, hauteur_pilule, COL_NOIR, COL_BLANC)
        
        # Texte "Osiris Games"
        texte = "Osiris Games"
        # Centrage approximatif (4px par lettre)
        # Mais on veut un style un peu classe, utilisons la font par defaut
        tx = cx - (len(texte) * 2) # *2 car font width 4 approx, /2 pour radius
        ty = cy - 2
        
        pyxel.text(tx, ty, texte, COL_JAUNE)

    def dessiner_avertissement(self):
        # Centrage du texte
        def centrer(y, txt, col):
            largeur = len(txt) * 4
            x = (ECRAN_L - largeur) // 2
            pyxel.text(x, y, txt, col)
            
        centrer(5, 'Remarque :', 7)
        centrer(35, "Veuillez lire attentivement le Guide", 7)
        centrer(42, "du Jeu avant de jouer.", 7)
        centrer(65, "Ce guide se trouve dans", 7)
        centrer(72, "la description.", 7)

    def dessiner_menu(self):
        # Version mise à jour
        pyxel.text(2, 85, '1.0.0', 7)
        
        # Titre
        pyxel.rect(71, 18, 59, 9, 5)
        pyxel.rectb(71, 18, 59, 9, 7)
        pyxel.text(73, 20, 'Ball Challenge', 7)        
        
        # Param Balle
        # Couleur contour
        col_contour = COULEURS_CONTRASTE.get(self.balle_apparence, 7)
        pyxel.circ(30, 38, 3, col_contour)
        pyxel.circ(30, 38, 2, self.balle_apparence)
        
        # Flèche G
        pyxel.blt(18, 55, 0, (0 if self.balle_apparence > 1 else 16), 48, 8, 8)
        # Flèche D
        pyxel.blt(34, 55, 0, (8 if self.balle_apparence < 15 else 24), 48, 8, 8)
            
        # Param Nombre
        pyxel.text(29, 47, str(self.nombre_balles), 7)   
        # Flèche G
        pyxel.blt(18, 45, 0, (0 if self.nombre_balles > 1 else 16), 48, 8, 8)
        # Flèche D
        pyxel.blt(34, 45, 0, (8 if self.nombre_balles < 3 else 24), 48, 8, 8)
        
        # Param Perso
        if self.personnage.apparence > 0:
            pyxel.blt(152, 55, 0, 0, 48, 8, 8)
        else:
            pyxel.blt(152, 55, 0, 16, 48, 8, 8)
        
        if self.personnage.apparence < 11:
            pyxel.blt(168, 55, 0, 8, 48, 8, 8)
        else:
             pyxel.blt(168, 55, 0, 24, 48, 8, 8)
        
        # Bouton Jouer
        pyxel.blt(76, 65, 0, 0, 0, 48, 16)
        
        # Bouton Clavier/Souris
        sprite_x = 0 if self.clavier else 16
        pyxel.blt(179, 5, 0, sprite_x, 16, 16, 16)

        self.personnage.afficher()

    def dessiner_hud(self):
        # HUD Bas
        pyxel.rect(0, 60, 200, 33, 5)
        pyxel.rectb(0, 60, 200, 33, 7)
        pyxel.text(80, 73, f'Score : {self.score}', 7)
        pyxel.text(80, 83, f'Temps : {self.temps_actuel}', 7)
        
        # Infos configuration actuelle
        # Balle avec contour dans HUD
        col_contour = COULEURS_CONTRASTE.get(self.balle_apparence, 7)
        pyxel.circ(93, 66, 3, col_contour)
        pyxel.circ(93, 66, 2, self.balle_apparence)

        pyxel.text(80, 63, f'{self.nombre_balles}x', 7)
        
        # Boutons
        pyxel.blt(10, 69, 0, 0, 32, 16, 16) # Retour
        pyxel.blt(32, 69, 0, 16, 32, 16, 16) # Rejouer
        
        # Aide Contrôles
        if self.clavier:
            pyxel.blt(136, 60, 0, 0, 104, 48, 32, 0)
        else:
            pyxel.blt(136, 60, 0, 0, 72, 48, 32, 0)

    def dessiner(self):
        pyxel.cls(0)
        
        if self.etat == "INTRO":
            self.dessiner_intro()
        elif self.etat == "AVERTISSEMENT":
            self.dessiner_avertissement()
        elif self.etat == "MENU":
            self.dessiner_menu()
            
        elif self.etat == "JEU":
            self.piece.afficher()
            self.personnage.afficher()
            for b in self.tab_balles: b.afficher()
            particules.dessiner() 
            self.dessiner_hud()
            
        elif self.etat == "FIN":
            # Fond gelé
            self.piece.afficher()
            self.personnage.afficher()
            for b in self.tab_balles: b.afficher()
            particules.dessiner()
            self.dessiner_hud()
            
            # Message fin
            pyxel.text(78, 18, 'Partie\n  Terminee', 7)

# Lancement
Jeu()