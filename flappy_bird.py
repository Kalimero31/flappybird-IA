import pygame
import random
import numpy as np

pygame.init()

win_height = 800
win_width  = 600
win = pygame.display.set_mode((win_width,win_height))

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0

    def draw(self, win):
        pygame.draw.circle(win, (255,0,0), (self.x, self.y), 20)

    def get_rect(self):
        return pygame.Rect(self.x - 20,
                           self.y - 20, 20, 20)  # x, y, largeur, hauteur

class Pipe:
    def __init__(self, x):
        self.x = x
        self.w = 70
        self.height = random.randint(200, 400)
        self.gap = 140  # Espace entre les tuyaux du haut et du bas
        self.color = (0,255,0)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, 0, self.w, self.height))
        pygame.draw.rect(win, self.color, (self.x, self.height + self.gap, self.w, win_height-self.height))
        # pygame.draw.rect()

    def move(self):
        self.x -= 8

    def get_upper_rect(self):
        return pygame.Rect(self.x, 0, self.w, self.height)
    
    def get_lower_rect(self):
        return pygame.Rect(self.x, self.height + self.gap, self.w, win_height - self.height)

class Game():

    def __init__(self) -> None:

        # initialisation de Pygame et gestion de la fenetre
        pygame.init()
        self.win_height = 800
        self.win_width  = 600
        self.win = pygame.display.set_mode((win_width,win_height))

        # event tick ?
        self.clock = pygame.time.Clock()

        self.reset()

    def reset(self):
        self.bird = Bird(50, 400)
        self.run = True
        self.pipes = [Pipe(self.win_width)]
        # Initial state can be more elaborate
        return self.get_state()
    
    def get_state(self):
        # Exemple: retourne la position en y de l'oiseau et la position en x du prochain tuyau
        return np.array([int(self.bird.y), 
                         int(self.pipes[0].x), 
                         int(self.pipes[0].height)])
    
    def step(self, action):
        self.clock.tick(30)
        if action == 1:  # Supposons que 1 signifie sauter
            self.bird.vel = -10
        self.bird.y += self.bird.vel
        self.bird.vel += 1.5

        self.check_pipes_position()
        done = self.check_collisions()

        next_state = self.get_state()
        reward = 1
        
        # if self.bird.y < 200 or self.bird.y > 600:
        #     reward = -5  # Exemple: 1 point pour la survie, tu pourras ajuster

        # Provisoire : donner une récompoense qui grandit qd on est sur l'axe du tuyau.
        if done == True:
            reward = -100
        return next_state, reward, done


    def render(self):
        self.win.fill((0,0,0))  # Remplit l'écran de noir
        self.bird.draw(self.win)
        for pipe in self.pipes:
            if pipe==self.pipes[0]:
                pipe.color=(0,0,255)
            pipe.draw(self.win)
        
        pygame.display.update()


    # Vérifie les collisions entre oiseau/tuyau
    def check_collisions(self):
            # collision avec les tuyaux.
            for pipe in self.pipes:
                if self.bird.get_rect().colliderect(pipe.get_upper_rect()) or self.bird.get_rect().colliderect(pipe.get_lower_rect()):
                    return True
            # collision avec le sol
            if self.bird.y > self.win_height:
                return True
            # collision avec le plafond
            if self.bird.y < 0:
                return True
            
            return False
                

    # Gère les tuyaux : On les supprime quand ils dépassent à gauche 
    # Et on en fait spawn un nouveau à droite
    def check_pipes_position(self):
        for pipe in self.pipes:
            pipe.move()
            if pipe.x < -40:
                self.pipes.remove(pipe)
        if len(self.pipes) == 0 or self.pipes[-1].x < win_width - 400:  # 300 est la distance entre les tuyaux
            self.pipes.append(Pipe(win_width))


if __name__=='__main__':
    testGame = Game()

    



