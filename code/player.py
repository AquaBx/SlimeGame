import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, w, h, obstacle_sprites):
        super().__init__(groups)
        self.image = (pygame.transform.scale(pygame.image.load("Assets/GreenSlime/Grn_Idle1.png"), (w, h))).convert_alpha()
        self.position = pygame.Vector2(pos[0],pos[1])
        self.taille = pygame.Vector2(w,h)
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.Vector2()
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites
    
    def input(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_z]:
            self.direction.y = -1
        elif keys_pressed[pygame.K_s]:
            self.direction.y = 1
        else :
            self.direction.y = 0

        if keys_pressed[pygame.K_d]:
            self.direction.x = 1
        elif keys_pressed[pygame.K_q]:
            self.direction.x = -1
        else :
            self.direction.x = 0
        
    
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.rect.x += self.direction.x * speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * speed
        self.collision('vertical')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
        
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom


    def update(self):
        self.input()
        self.move(self.speed)



    