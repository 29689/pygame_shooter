import sys, pygame
import random
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

background = (150, 50, 175)

clock = pygame.time.Clock()

frame_rate = 60

gravity = .75

line_color = (255, 0, 0)

exp_group = pygame.sprite.Group()
def draw_background():
    screen.fill(background)
    pygame.draw.line(screen, line_color, (0, 300), (SCREEN_WIDTH, 300))


class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, ammo, char_type, grenades):
        pygame.sprite.Sprite.__init__(self)

        self.grenades = grenades
        self.grenade_group = pygame.sprite.Group()
        self.grenade_thrown = False
        self.grenade = False

        self.direction = 1
        self.speed = speed
        self.flip = False
        self.moving_left = False
        self.moving_right = False
        self.jump = False
        self.velocity_y = 0
        self.in_air = False
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.health = 100
        self.alive = True
        self.shoot = False
        self.bullets = pygame.sprite.Group()
        self.char_type = char_type
        self.animation_list = []
        self.action = 0
        self.frame = 0
        self.update_time = pygame.time.get_ticks()

        animation_types = ['Idle', 'Run', 'Jump', 'Death']

        for animation in animation_types:
            temp_list = []

            num_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))

            for i in range(num_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)

            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_animation(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame += 1
        if self.frame >= len(self.animation_list[self.action])-1:
            if self.action == 3:
                self.frame = 7
            else:
                self.frame = 0

    def update(self):
        self.check_alive()
        self.update_animation()
        if self.shoot_cooldown >0:
            self.shoot_cooldown-=1

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        if self.moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1

        if self.moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.jump == True and self.in_air == False:
            self.velocity_y = -11
            self.jump = False
            self.in_air = True

        self.velocity_y += gravity

        if self.velocity_y > 10:
            self.velocity_y

        dy += self.velocity_y

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def fire(self):
        if self.shoot_cooldown == 0 and self.ammo>0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (.5 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            self.bullets.add(bullet)
            self.ammo -=1

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = pygame.image.load('img/icons/grenade.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction

    def update(self):
        self.vel_y += gravity
        dx = self.direction * self.speed
        dy = self.vel_y

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0

        self.rect.x += dx
        self.rect.y += dy

        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, .5)
            exp_group.add(explosion)

            if abs(self.rect.centerx - player.rect.centerx) < 80 and abs(self.rect.centery - player.rect.centery) < 80:
                player.health -= 50

            if abs(self.rect.centerx - enemy.rect.centerx) < 80 and abs(self.rect.centery - enemy.rect.centery) < 80:
                enemy.health -= 50





class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,6):
            img = pygame.image.load(f'img/explosion/exp{num}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0

    def update(self):
        exp_speed = 4
        self.counter +=1
        if self.counter >= exp_speed:
            self.counter = 0
            self.frame +=1
            if self.frame >= 5:
                self.kill()
            else:
                self.image = self.images[self.frame]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pygame.image.load('img/icons/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed)

        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        if pygame.sprite.spritecollide(player, enemy.bullets, False):
            player.health -= 5
            self.kill()
            print("Player health", player.health)
        if pygame.sprite.spritecollide(enemy, player.bullets, False):
            enemy.health -= 5
            self.kill()
            print("Enemy health", enemy.health)




# player_bullets = pygame.sprite.Group()
# enemy_bullets = pygame.sprite.Group()


player = Soldier(200, 200, 3, 5, 20, 'player', 10)
enemy = Soldier(250, 200, 3, 5, 20, 'enemy', 5)

run = True
while run:
    clock.tick(frame_rate)

    draw_background()

    player.draw()
    enemy.draw()

    player.move(player.moving_left, player.moving_right)
    enemy.move(enemy.moving_left, enemy.moving_right)

    player.update()
    enemy.update()

    player.bullets.update()
    player.bullets.draw(screen)

    enemy.bullets.update()
    enemy.bullets.draw(screen)

    player.grenade_group.update()
    enemy.grenade_group.update()

    player.grenade_group.draw(screen)
    enemy.grenade_group.draw(screen)

    exp_group.update()
    exp_group.draw(screen)

    if player.alive:
        if (player.moving_left or player.moving_right) and not enemy.in_air:
            player.update_action(1)
        elif player.in_air:
            player.update_action(2)
        else:
            player.update_action(0)
        if player.shoot:
            player.fire()

        elif player.grenade and player.grenade_thrown == False and player.grenades >0:
            grenade = Grenade(player.rect.centerx, player.rect.top, player.direction)
            player.grenade_group.add(grenade)
            player.grenades -= 1
            player.grenade_thrown = True

    if enemy.alive:
        if (enemy.moving_left or enemy.moving_right) and not enemy.in_air:
            enemy.update_action(1)
        elif enemy.in_air:
            enemy.update_action(2)
        else:
            enemy.update_action(0)
        if enemy.shoot:
            enemy.fire()
        elif enemy.grenade and enemy.grenade_thrown == False and enemy.grenades >0:
            grenade = Grenade(enemy.rect.centerx, enemy.rect.top, enemy.direction)
            enemy.grenade_group.add(grenade)
            enemy.grenades -= 1
            enemy.grenade_thrown = True

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:


            if player.alive:
                if event.key == pygame.K_d:
                    player.moving_right = True
                if event.key == pygame.K_a:
                    player.moving_left = True

                if event.key == pygame.K_t:
                    player.grenade = True

                if event.key == pygame.K_w:
                    player.jump = True

                if event.key == pygame.K_SPACE:
                    player.shoot = True
            if enemy.alive:
                if event.key == pygame.K_RIGHT:
                    enemy.moving_right = True
                if event.key == pygame.K_LEFT:
                    enemy.moving_left = True

                if event.key == pygame.K_UP:
                    enemy.jump = True

                if event.key == pygame.K_DOWN:
                    enemy.shoot = True

                if event.key == pygame.K_0:
                    enemy.grenade = True


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.moving_right = False
            if event.key == pygame.K_a:
                player.moving_left = False
            if event.key == pygame.K_SPACE:
                player.shoot = False
            if event.key == pygame.K_t:
                player.grenade = False
                player.grenade_thrown = False

            if event.key == pygame.K_RIGHT:
                enemy.moving_right = False
            if event.key == pygame.K_LEFT:
                enemy.moving_left = False
            if event.key == pygame.K_DOWN:
                enemy.shoot = False
            if event.key == pygame.K_0:
                enemy.grenade = False
                enemy.grenade_thrown = False

    pygame.display.update()

pygame.quit()
