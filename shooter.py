import sys
import pygame
import random
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

clock = pygame.time.Clock()

FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Diego's Shooter Game")

class Soldier(pygame.sprite.Sprite):

    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.update_time = pygame.time.get_ticks()
        self.img = pygame.image.load(f'img/player/Idle/0.png')
        self.img = pygame.transform.scale(self.img, (int(self.img.get_width() * scale), int(self.img.get_height() * scale)))
        self.rect = self.img.get_rect()
        self.rect.center = (x,y)
        self.flip = False
        self.direction = 1
        self.speed = speed

    def draw(self):
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)

    def move(self, movingLeft, movingRight):
        dx = 0
        dy = 0

        if movingLeft:
            dx = -self.speed
            self.flip = True
            self.direction = -1

        if movingRight:
            dx = self.speed
            self.flip = False
            self.direction = 1

        self.rect.x += dx
        self.rect.y += dy


player = Soldier(200, 200, 3, 4)
run = True
movingLeft = False
movingRight = False

while run:
    screen.fill((125, 50, 255))

    player.draw()
    player.move(movingLeft, movingRight)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                movingLeft = True
            if event.key == pygame.K_d:
                movingRight = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                movingLeft = False
            if event.key == pygame.K_d:
                movingRight = False




pygame.quit()

##        animation_types = ['Idle', 'Run', 'Jump', 'Death']
##
##        for animation in animation_types:
##            temp_list = []
##
##            num_frames = len(os.listdir(f'H:/PyGame_Shooter/img/{self.char_type}/{animation}'))
##
##            for i in range(num_frames):
##                img = pygame.image.load(f'H:/PyGame_Shooter/img/{self.char_type}/{animation}/{i}.png')
##                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
##                temp_list.append(img)
##
##
##            self.animation_list.append(temp_list)
##
##        self.image = self.animation_list[self.action][self.frame]
##        self.rect = self.image.get_rect()