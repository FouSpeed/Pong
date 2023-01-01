import pygame
import time

class Window:
    def __init__(self, window_size = (1024, 780)):
        self.window_size = window_size
        self.screen = pygame.display.set_mode(window_size)
        self.window_size = self.screen.get_size()
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption("Jeu")

    def renitialiser(self):
        self.screen.fill((255, 255, 255))

    def afficher_objet(self, objet_surface, position):
        self.screen.blit(objet_surface, position)
    
    def afficher_text(self, texte: str, position, font_size = 75 , color = (0,0,0)):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(str(texte), True, color)
        self.screen.blit(text_surface, position)


class Balle(Window):
    def __init__(self, object_window:Window, balle = pygame.image.load("balle.png")):
        self.object_window = object_window 
        self.balle = balle
        self.balle_surface = pygame.Surface(balle.get_size())
        self.position = (self.object_window.window_size[0]/2, self.object_window.window_size[1]/2)
        self.balle_surface.blit(balle, self.position)
        self.object_window.screen.blit(self.balle_surface, self.position)
        self.speed = 5
        self.sens = "right"
        self.add_y = 0.5

    def move_ball(self, joueur:list, direction: list):
        # Création des objets Rect à partir de l'objet Balle et de l'objet joueur
        rect_balle = pygame.Rect(self.position, self.balle.get_size())
        
        # Détection de la collision
        for nbr, i in enumerate(joueur):
            rect_joueur = pygame.Rect(i.position, i.joueur.get_size())
            if rect_balle.colliderect(rect_joueur) and nbr == 1:
                self.sens = "left"
                if direction[nbr] == "up":
                    self.add_y -= 2
            elif rect_balle.colliderect(rect_joueur) and nbr == 0:
                self.sens = "right" 
                if direction[nbr] == "down":
                    self.add_y += 2       
        # Mise à jour de la position de la balle par rapport à x
        
        if self.sens == "left" and (self.position[1] > 0 and self.position[1] < self.object_window.window_size[1]):
            self.position = (self.position[0] - self.speed, self.position[1] + self.add_y)
        elif self.sens == "right" and (self.position[1] > 0 and self.position[1]  < self.object_window.window_size[1]):
            self.position = (self.position[0] + self.speed, self.position[1] + self.add_y)
        elif self.sens == "left" and (self.position[1] <= 0 or self.position[1]  >= self.object_window.window_size[1]-5):
            self.add_y = - self.add_y
            self.position = (self.position[0] - self.speed, self.position[1] + self.add_y)
        elif self.sens == "right" and (self.position[1] <= 0 or self.position[1]  >= self.object_window.window_size[1]-5):
            self.add_y = - self.add_y
            self.position = (self.position[0] + self.speed, self.position[1] + self.add_y)

    def winner(self, joueur: list):
        if self.position[0] <= 0:
            joueur[1].point += 1
        elif self.position[0] >= self.object_window.window_size[0]:
            joueur[0].point += 1
        if self.position[0] <= 0 or self.position[0] >= self.object_window.window_size[0]:
            self.position = (self.object_window.window_size[0]/2, self.object_window.window_size[1]/2)
            self.speed = 0
            self.add_y = 0
            
            return True

    def restart(self, key_pressed):
        x = window.window_size[0]
        y =window.window_size[1]
        self.object_window.afficher_text("Pour relancer une partie appuyer sur r", (x/7, y/2 -50), font_size=55)

        if key_pressed:
            self.speed = 5
            self.add_y = 0.5
            return True

    def afficher(self):
        self.object_window.afficher_objet(self.balle_surface, self.position)

class joueur(Window):
    def __init__(self, object_window, joueur, x):
        self.object_window = object_window 
        self.joueur = joueur
        self.joueur_surface = pygame.Surface(joueur.get_size())
        #self.position = (x, self.object_window.window_size[1]/2)
        self.position = (x, self.object_window.window_size[1]/2)
        self.joueur_surface.blit(joueur, self.position)
        self.object_window.screen.blit(self.joueur_surface, self.position)
        self.point = 0
    
    def move(self, direction):
        dir_value = 0
        if direction == "up" and self.position[1] > 0:
            dir_value = -5
        elif direction == "down" and self.position[1] < self.object_window.window_size[1] - self.joueur_surface.get_height():
            dir_value = 5
        self.position = (self.position[0], self.position[1] + dir_value)
    
    def afficher_point(self, position:tuple):
        font = pygame.font.Font(None, 75)
        text_surface = font.render(str(self.point), True, (0, 0, 0))
        self.object_window.afficher_objet(text_surface, position)

    def afficher(self):
        self.object_window.afficher_objet(self.joueur_surface, self.position)


class Mur(Window):
    def __init__(self, window, mur_image, xy = (10,0)):
        self.object_window = window
        self.mur_image = mur_image
        self.position = xy
        self.mur_surface = pygame.Surface(self.mur_image.get_size())
        self.mur_surface.blit(mur_image, self.position)
        self.object_window.screen.blit(self.mur_surface, self.position)

    def afficher(self):
        self.object_window.afficher_objet(self.mur_surface, self.position)

#initialisation de la fenêtre
pygame.init()
window = Window()


#charger les images

mur_image = pygame.image.load("mur3.png")
mur_image = pygame.transform.scale(mur_image, (window.window_size[1], 10))
mur_image = pygame.transform.rotate(mur_image, 90)
mur1 = Mur(window, mur_image)
mur2 = Mur(window, mur_image, xy = (window.window_size[0]-20, 0))
balle = Balle(window)
joueur1_image = pygame.image.load("joueur1.png")
joueur1_image = pygame.transform.scale(joueur1_image,(int(joueur1_image.get_width() * 0.25), int(joueur1_image.get_height()*0.75)))
joueur2_image = pygame.image.load("joueur2.png")
joueur2_image = pygame.transform.scale(joueur2_image,(int(joueur2_image.get_width() * 0.25), int(joueur2_image.get_height()*0.75)))
joueur1 = joueur(window, joueur1_image, x = 50)
joueur2  = joueur(window, joueur2_image, x = window.window_size[0]-50)

direction1, direction2 = "", ""
key_down_pressed, key_up_pressed, key_a_pressed, key_q_pressed, key_r_pressed = False, False, False, False, False
win = False

while True:
    # Mettre à jour l'affichage
    window.renitialiser()
    #déplacement joueur 1
    events1 = pygame.event.get()
    for event in events1:
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_UP:
                key_up_pressed = True
            if event.key == pygame.K_DOWN:
                key_down_pressed = True
            
            if event.key == pygame.K_a:
                key_a_pressed = True
            if event.key == pygame.K_q:
                key_q_pressed = True
            if event.key == pygame .K_r:
                key_r_pressed = True
            
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_UP:
                key_up_pressed = False
            if event.key == pygame.K_DOWN:
                key_down_pressed = False
            
            if event.key == pygame.K_a:
                key_a_pressed = False
            if event.key == pygame.K_q:
                key_q_pressed = False
            if event.key == pygame .K_r:
                key_r_pressed = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
    if key_up_pressed and not key_down_pressed:
        direction1 = "up"
    if key_down_pressed and not key_up_pressed:
        direction1 = "down"
    if key_up_pressed and key_down_pressed:
        direction1 = ""
    if not key_up_pressed and not key_down_pressed:
        direction1 = ""

    if key_a_pressed and not key_q_pressed:
        direction2 = "up"
    if key_q_pressed and not key_a_pressed:
        direction2 = "down"
    if key_q_pressed and key_a_pressed:
        direction2 = ""
    if not key_a_pressed and not key_q_pressed:
        direction2 = "" 
         
    joueur1.move(direction2)
    joueur2.move(direction1)
    balle.move_ball([joueur1, joueur2], [direction2, direction1])
    x = window.window_size[0]
    y =window.window_size[1]
    if balle.winner([joueur1, joueur2]):
        win = True        
    if win:
        if balle.restart(key_r_pressed):
            win = False
    mur1.afficher()
    mur2.afficher()
    balle.afficher()
    joueur1.afficher()
    joueur2.afficher()

    joueur1.afficher_point((x/8,y/8))
    joueur2.afficher_point(( x - (x / 8),y / 8))
    pygame.display.update()
    time.sleep(0.01)




