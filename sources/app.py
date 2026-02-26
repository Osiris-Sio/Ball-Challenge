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
        self.seuil_fade = vie // 2
        self.couleur = couleur
        self.mode = mode # "pixel" ou "ligne"

    def mettre_a_jour(self):
        self.x += self.dx
        self.y += self.dy
        self.vie -= 1
        return self.vie > 0

    def dessiner(self):
        # Fade simple selon la vie pour plus de douceur
        col = self.couleur
        if self.vie < self.seuil_fade:
            if col == COL_BLANC: col = COL_GRIS
            
        if self.mode == "ligne":
            pyxel.line(self.x, self.y, self.x - self.dx, self.y - self.dy, col)
        else:
            pyxel.pset(self.x, self.y, col)

class GestionnaireParticules:
    def __init__(self):
        self.particules = []

    def ajouter_effet_air(self, x, y, direction, est_balle=False):
        """
        Génère de petites lignes blanches pour simuler l'air.
        est_balle: Si vrai, effet plus fréquent et petit.
        """
        seuil = 0.8 if est_balle else 0.4 # Augmenté pour les balles
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
        # Mise à jour et filtrage optimisé
        self.particules = [p for p in self.particules if p.mettre_a_jour()]

    def dessiner(self):
        # Mise en cache locale des méthodes pour la rapidité
        for p in self.particules:
            p.dessiner()

# Gestionnaire global (géré dans Jeu)
particules = None 

class Personnage:
    def __init__(self):
        self.x = 160
        self.y = 37
        self.w = 8
        self.h = 8
        self.apparence = 0
        self.bouclier = False
        self.magnetisme = 0 # Timer
        self.invincible = 0 # Timer
        
    def placer_menu(self):
        self.x, self.y = 160, 37
        self.bouclier = False
        self.magnetisme = 0
        self.invincible = 0
        
    def placer_partie(self):
        self.x, self.y = 96, 20
        self.bouclier = False
        self.magnetisme = 0
        self.invincible = 0
        
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
        # Effet d'invincibilité (clignotement)
        if self.invincible > 0:
            if (pyxel.frame_count // 2) % 2 == 0: return
            
        pyxel.blt(self.x, self.y, 1, 0, 8 * self.apparence, 8, 8, 0)
        # Aura du bouclier
        if self.bouclier:
            t = pyxel.frame_count
            pyxel.circb(self.x + 4, self.y + 4, 6 + math.sin(t*0.2)*1, 12)
        # Effet magnétisme
        if self.magnetisme > 0:
            if (pyxel.frame_count // 10) % 2 == 0:
                pyxel.circb(self.x + 4, self.y + 4, 8, 10)

class Piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 2 
        self.h = 2
        
    def verifier_collision(self, mk_x, mk_y):
        return verifier_collision(self.x - 1, self.y - 1, 4, 4, mk_x, mk_y, 8, 8)
    
    def faire_reapparaitre(self):
        self.x = random.randint(10, 190)
        self.y = random.randint(10, 50)

    def afficher(self):
        pyxel.circ(self.x, self.y, 1, 10)

class Bonus:
    def __init__(self, x, y, type_bonus):
        self.x = x
        self.y = y
        self.type = type_bonus # "BOUCLIER" ou "AIMANT"
        self.vie = 300 # 5 secondes à 60fps
        self.clignotement = 0
        
    def verifier_collision(self, mk_x, mk_y):
        return verifier_collision(self.x - 2, self.y - 2, 5, 5, mk_x, mk_y, 8, 8)
        
    def mettre_a_jour(self):
        self.vie -= 1
        self.clignotement = (self.clignotement + 1) % 10
        return self.vie > 0
        
    def afficher(self):
        if self.vie < 60 and self.clignotement < 5: return
        # Coordonnées fournies : Bouclier (0, 136), Aimant (0, 144)
        v = 136 if self.type == "BOUCLIER" else 144
        pyxel.blt(self.x - 4, self.y - 4, 0, 0, v, 8, 8, 0)

class Balle:
    def __init__(self, vitesse, dx, dy, apparence, snipe_auto=False):
        self.x = 100
        self.y = 50
        self.w = 6 
        self.h = 6 
        self.vitesse = vitesse
        self.dx = dx * self.vitesse
        self.dy = dy * self.vitesse
        self.apparence = apparence
        self.col_contour = COULEURS_CONTRASTE.get(apparence, 7)
        # Système de traînée pour la fluidité visuelle
        self.trainee = [] 
        self.max_trainee = 5
        
        # Mode Sniper
        self.mode = "NORMAL"
        self.timer_snipe = random.randint(300, 600) if snipe_auto else 0
        self.snipe_auto = snipe_auto
        self.target_dx = 0
        self.target_dy = 0
        
    def deplacer(self, target_x=None, target_y=None):
        if self.mode == "NORMAL" and self.snipe_auto:
            self.timer_snipe -= 1
            if self.timer_snipe <= 0:
                self.forcer_snipe()
        
        if self.mode == "STOP":
            self.timer_snipe -= 1
            if self.timer_snipe <= 0:
                # Calcul direction vers CENTRE de la cible
                if target_x is not None:
                    dx = (target_x + 4) - self.x
                    dy = (target_y + 4) - self.y
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist > 0:
                        self.mode = "SNIPE"
                        # Fonce 4.5x plus vite (plus équilibré)
                        v = self.vitesse * 4.5
                        self.target_dx = (dx / dist) * v
                        self.target_dy = (dy / dist) * v
                else:
                    self.mode = "NORMAL"
                    if self.snipe_auto: self.timer_snipe = 600
                    
        if self.mode == "SNIPE":
            # Traînée spécifique plus longue
            self.trainee.insert(0, (self.x, self.y))
            if len(self.trainee) > 10: self.trainee.pop()
            self.x += self.target_dx
            self.y += self.target_dy
        else:
            # Mode NORMAL ou STOP
            self.trainee.insert(0, (self.x, self.y))
            if len(self.trainee) > self.max_trainee:
                self.trainee.pop()
                
            if self.mode == "NORMAL":
                self.x += self.dx
                self.y += self.dy

    def forcer_snipe(self):
        if self.mode == "NORMAL":
            self.mode = "STOP"
            self.timer_snipe = 60 # S'arrête 1 sec
    
    def verifier_collision(self, mk_x, mk_y):
        return verifier_collision(self.x - 3, self.y - 3, 6, 6, mk_x, mk_y, 8, 8)

    def remplacer(self, tuple_dx_dy):
        v = self.vitesse
        self.dx = tuple_dx_dy[0] * v
        self.dy = tuple_dx_dy[1] * v
        pyxel.play(1, 1)

    def rebonds(self):
        old_mode = self.mode
        touche = False
        # Mur Gauche
        x, y = self.x, self.y
        if x < 3:
            self.remplacer(random.choice([(1, -1), (2, 0), (1, 1)]))
            particules.ajouter_impact_mur(0, y, 1, 0)
            touche = True
        elif x > ECRAN_L - 3:
            self.remplacer(random.choice([(-1, -1), (-2, 0), (1, 1)]))
            particules.ajouter_impact_mur(ECRAN_L, y, -1, 0)
            touche = True
        
        if y < 3:
            self.remplacer(random.choice([(-1, 1), (0, 1), (1, 1)]))
            particules.ajouter_impact_mur(x, 0, 0, 1)
            touche = True
        elif y > 57:
            self.remplacer(random.choice([(-1, -1), (0, -1), (1, -1)]))
            particules.ajouter_impact_mur(x, 60, 0, -1)
            touche = True
            
        if old_mode == "SNIPE" and touche:
            self.mode = "NORMAL"
            if self.snipe_auto:
                self.timer_snipe = random.randint(300, 600)

    def afficher(self):
        circ = pyxel.circ
        if self.mode == "STOP":
            col = 9 if (pyxel.frame_count // 4) % 2 == 0 else self.apparence
            circ(self.x, self.y, 3, 7)
            circ(self.x, self.y, 2, col)
        elif self.mode == "SNIPE":
            for i, pos in enumerate(self.trainee):
                pyxel.pset(pos[0], pos[1], 8 if i % 2 == 0 else 7)
            circ(self.x, self.y, 3, 8)
            circ(self.x, self.y, 2, 7)
        else:
            # Rendu classique
            col_app = self.apparence
            col_cur = self.col_contour
            for i, pos in enumerate(self.trainee):
                rayon = 2 if i < 2 else 1
                circ(pos[0], pos[1], rayon, COL_GRIS if i > 1 else col_app)
            circ(self.x, self.y, 3, col_cur)
            circ(self.x, self.y, 2, col_app)

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
        self.frame_debut_intro = pyxel.frame_count
        self.frame_debut_avertissement = 0
        
        # Config
        self.clavier = True
        self.balle_apparence = 1
        self.nombre_balles = 2
        
        # Entités
        self.personnage = Personnage()
        self.piece = Piece(100, 35)
        self.tab_balles = []
        self.tab_bonus = []
        
        # Données Jeu
        self.score = 0
        self.frame_debut_jeu = 0
        self.temps_actuel = 0
        self.timer_bonus = 600 # 10 secondes
        self.timer_snipe_event = 180 # 3 sec avant premier event
        
        # Audio
        pyxel.playm(0) 
        
        pyxel.run(self.mettre_a_jour, self.dessiner)
        
    # --------------------------------------
    # LOGIQUE
    # --------------------------------------
    
    def lancer_partie(self):
        self.etat = "JEU"
        self.personnage.placer_partie()
        self.frame_debut_jeu = pyxel.frame_count
        self.score = 0
        
        # Création balles (jusqu'à 5)
        # La première balle est TOUJOURS un sniper automatique
        balles_base = [
            Balle(0.3, -1, 0, self.balle_apparence, snipe_auto=True),
            Balle(0.3, 1, 0, self.balle_apparence),
            Balle(0.35, 0, 1, self.balle_apparence),
            Balle(0.35, -1, -1, self.balle_apparence),
            Balle(0.32, 1, 1, self.balle_apparence)
        ]
        self.tab_balles = balles_base[:self.nombre_balles]
        self.piece = Piece(100, 35)
        self.tab_bonus = []
        self.timer_snipe_event = random.randint(180, 400)

    def retour_menu(self):
        self.etat = "MENU"
        self.personnage.placer_menu()
        self.tab_balles = []
        
    def gestion_intro(self):
        if pyxel.frame_count - self.frame_debut_intro >= 120: # 2 secondes
            self.etat = "AVERTISSEMENT"
            self.frame_debut_avertissement = pyxel.frame_count

    def gestion_avertissement(self):
        if pyxel.frame_count - self.frame_debut_avertissement >= 300: # 5 secondes
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
                elif 34 <= mx <= 42 and self.nombre_balles < 5:
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
        # Mise à jour des timers perso
        if self.personnage.invincible > 0: self.personnage.invincible -= 1
        px, py = self.personnage.x, self.personnage.y
        # Balles et Événement Snipe Aléatoire
        self.timer_snipe_event -= 1
        if self.timer_snipe_event <= 0:
            if self.tab_balles:
                # On choisit une balle au hasard pour viser le joueur
                random.choice(self.tab_balles).forcer_snipe()
                self.timer_snipe_event = random.randint(180, 500) # Min 3 sec

        for balle in self.tab_balles:
            balle.deplacer(px, py)
            balle.rebonds() 
            if self.personnage.invincible <= 0 and balle.verifier_collision(px, py):
                if self.personnage.bouclier:
                    # Le bouclier sauve !
                    self.personnage.bouclier = False
                    self.personnage.invincible = 120 # 2 sec d'immunité
                    # Effet d'éclatement bleu
                    for _ in range(10): 
                        particules.particules.append(Particule(px+4, py+4, random.uniform(-2,2), random.uniform(-2,2), 15, 12))
                    # On fait rebondir la balle pour ne pas mourir
                    balle.remplacer((random.uniform(-1,1), random.uniform(-1,1)))
                    pyxel.play(1, 2)
                else:
                    self.etat = "FIN"
                    pyxel.play(0, 3)
                    break # Arrêt immédiat de la boucle

        # Pièce
        if self.personnage.magnetisme > 0:
            self.personnage.magnetisme -= 1
            # Optimisation : Distance au carré pour éviter sqrt inutile
            dx = px - self.piece.x
            dy = py - self.piece.y
            dist_sq = dx*dx + dy*dy
            if dist_sq < 1225: # 35 * 35
                dist = math.sqrt(dist_sq)
                if dist > 0:
                    self.piece.x += (dx / dist) * 1.2
                    self.piece.y += (dy / dist) * 1.2

        if self.piece.verifier_collision(px, py):
            particules.ajouter_effet_piece(self.piece.x, self.piece.y)
            pyxel.play(0, 2)
            self.piece.faire_reapparaitre()
            self.score += 1
            for b in self.tab_balles: b.vitesse += 0.02
        
        # Gestion du Spawn Temporel des Bonus
        # Condition : pas de bouclier, pas d'aimant actif, et pas de bonus sur le terrain
        if not self.personnage.bouclier and self.personnage.magnetisme <= 0 and not self.tab_bonus:
            self.timer_bonus -= 1
            if self.timer_bonus <= 0:
                t = "BOUCLIER" if random.random() < 0.6 else "AIMANT"
                self.tab_bonus.append(Bonus(random.randint(10, 190), random.randint(10, 50), t))
                self.timer_bonus = 600 # Reset 10 sec
        else:
            # On ne reset pas le timer, mais on ne le décompte pas non plus
            pass

        # Bonus
        self.tab_bonus = [b for b in self.tab_bonus if b.mettre_a_jour()]
        for b in self.tab_bonus:
            if b.verifier_collision(px, py):
                if b.type == "BOUCLIER":
                    self.personnage.bouclier = True
                else:
                    self.personnage.magnetisme = 300 # 5 sec
                b.vie = 0 # Désactiver
                pyxel.play(1, 2)

        # Chrono stable
        self.temps_actuel = (pyxel.frame_count - self.frame_debut_jeu) // 60
        
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
        pyxel.blt(34, 45, 0, (8 if self.nombre_balles < 5 else 24), 48, 8, 8)
        
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
        e = self.etat
        
        if e == "INTRO":
            self.dessiner_intro()
        elif e == "AVERTISSEMENT":
            self.dessiner_avertissement()
        elif e == "MENU":
            self.dessiner_menu()
        elif e == "JEU":
            self.piece.afficher()
            for b_bonus in self.tab_bonus: b_bonus.afficher()
            self.personnage.afficher()
            for b in self.tab_balles: b.afficher()
            particules.dessiner() 
            self.dessiner_hud()
        elif e == "FIN":
            self.piece.afficher()
            for b_bonus in self.tab_bonus: b_bonus.afficher()
            self.personnage.afficher()
            for b in self.tab_balles: b.afficher()
            particules.dessiner()
            self.dessiner_hud()
            pyxel.text(78, 18, 'Partie\n  Terminee', 7)

# Lancement
Jeu()