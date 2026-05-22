import pygame
import os

# Initialize the Pygame library
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8) # The height is 80% of the width

# Set up the clock for FPS control
clock = pygame.time.Clock()
FPS = 60 # Frames per second

# Variables to track movement
moving_left = False
moving_right = False

# Movement for player 2
ml = False
mr = False

# Gravity constant for character movement
gravity = .75

# Create the display screen and set the caption
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Diego\'s Shooter Game')

# Background color and function to draw the background
background_color = (124, 45, 255)

def draw_background():
    screen.fill(background_color) # Fill the screen with the background color
    pygame.draw.line(screen, (255, 0, 0), (0, 300), (SCREEN_WIDTH, 300)) # Draw a red line to separate sections

# Soldier class representing the player or enemy character
class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, char_type, ammo, health):
        pygame.sprite.Sprite.__init__(self) # Initialize the sprite class
        self.char_type = char_type # Character type (player or enemy)
        self.animation_list = [] # List to store character animations
        self.frame_index = 0 # Current animation frame
        self.update_time = pygame.time.get_ticks() # Timer to control animation speed
        self.action = 0 # Current action (Idle, Run, etc.)
        self.jump = False # Whether the character is jumping
        self.in_air = False # Whether the character is in the air (not grounded)
        self.ammo = ammo # Starting ammo count
        self.shoot_cooldown = 0 # Cooldown for shooting

        # Animation types (Idle, Run, etc.)
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            temp_list = []
            num_frames = len(os.listdir(f'img/{self.char_type}/{animation}')) # Get number of frames for each animation

            # Load each frame of animation
            for i in range(num_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale))) # Scale the image
                temp_list.append(img) # Add to the animation list

            self.animation_list.append(temp_list) # Append the animation list to the character's animations
        self.image = self.animation_list[self.action][self.frame_index] # Set initial image/frame

        # Create a rectangle around the image for positioning
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) # Position the character
        self.direction = 1 # Character's facing direction (1 = right, -1 = left)
        self.flip = False # Whether the character is flipped horizontally
        self.speed = speed # Character's movement speed
        self.velocity_y = 0 # Vertical velocity (used for jump and gravity)
        self.health = health # Character's health
        self.alive = True # Whether the character is alive
        self.bullet_group = pygame.sprite.Group() # Group to hold the bullets fired by this character

    def draw(self):
        # Draw the current frame of the character's animation to the screen
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        # Handle left and right movement
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1 # Face left

        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1 # Face right

        # Handle jumping
        if self.jump == True and self.in_air == False:
            self.jump = False
            self.in_air = True
            self.velocity_y = -14 # Initial jump velocity

        self.velocity_y += gravity # Apply gravity
        if self.velocity_y > 10: # Terminal velocity limit
            self.velocity_y = 10

        dy += self.velocity_y # Update vertical position

        # Prevent falling below the ground
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False # Stop falling when the character hits the ground

        self.rect.x += dx # Update horizontal position
        self.rect.y += dy # Update vertical position

    def update_animation(self):
        cooldown = 100 # Animation frame change time
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if it's time to update the frame
        if pygame.time.get_ticks() - self.update_time > cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3: # Death animation doesn't loop
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0 # Loop other animations

    def update(self):
        self.update_animation()
        # Decrease shoot cooldown if it's greater than 0
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def update_action(self, new_action):
        # Change the character's action (Idle, Run, Jump, Death)
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def shoot(self):
        # Shoot a bullet if there is ammo and the cooldown is 0
        if self.ammo > 0 and self.shoot_cooldown == 0:
            self.shoot_cooldown = 20 # Set cooldown for shooting
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
            self.bullet_group.add(bullet) # Add bullet to the bullet group
            self.ammo -= 1 # Decrease ammo by 1

    def check_alive(self):
        # Check if the character is still alive (health <= 0)
        if self.health <= 0:
            self.alive = False
            self.speed = 0 # Stop movement
            self.update_action(3) # Change to death animation

# Bullet class to represent a bullet shot by the player or enemy
bullet_img = pygame.image.load('img/icons/bullet.png')

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10 # Bullet speed
        self.image = bullet_img # Bullet image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) # Position the bullet
        self.direction = direction # Direction of the bullet

    def update(self):
        # Update bullet position based on direction
        self.rect.x += self.direction * self.speed

        # Check for collision with player or enemy and decrease health
        if pygame.sprite.spritecollide(player, player2.bullet_group, False):
            player.health -= 5
            self.kill() # Destroy the bullet

        if pygame.sprite.spritecollide(player2, player.bullet_group, False):
            player2.health -= 5
            self.kill() # Destroy the bullet

# Initialize players (Soldiers)
player = Soldier(200, 200, 3, 5, "player", 10, 100)
player2 = Soldier(400, 200, 3, 5, "enemy", 10, 100)

# Shooting flags
player_shoot = False
player2_shoot = False

# Main game loop
run = True
while run:
    clock.tick(FPS) # Maintain FPS
    draw_background() # Draw background

    # Check if players are alive
    player.check_alive()
    player2.check_alive()

    # Player movement and actions
    if player.alive:
        player.move(moving_left, moving_right)
        if player_shoot:
            player.shoot()
        if player.health <= 0:
            player.update_action(3) # Death animation
        elif player.in_air:
            player.update_action(2) # Jump animation
        elif moving_left or moving_right:
            player.update_action(1) # Run animation
        else:
            player.update_action(0) # Idle animation

    # Player 2 movement and actions
    if player2.alive:
        player2.move(ml, mr)
        if player2_shoot:
            player2.shoot()
        if player2.health <= 0:
            player2.update_action(3) # Death animation
        elif player2.in_air:
            player2.update_action(2) # Jump animation
        elif ml or mr:
            player2.update_action(1) # Run animation
        else:
            player2.update_action(0) # Idle animation

    player.update() # Update player state
    player2.update() # Update player 2 state

    player.draw() # Draw player
    player2.draw() # Draw player 2

    # Update and draw bullets for both players
    player.bullet_group.update()
    player.bullet_group.draw(screen)

    player2.bullet_group.update()
    player2.bullet_group.draw(screen)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False # Exit the game if the window is closed

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.jump = True # Player jump
            if event.key == pygame.K_a:
                moving_left = True # Player move left
            if event.key == pygame.K_d:
                moving_right = True # Player move right
            if event.key == pygame.K_s:
                player_shoot = True # Player shoot
            if event.key == pygame.K_r and player.ammo <= 0:
                player.ammo = 10 # Refill player ammo

            if event.key == pygame.K_UP:
                player2.jump = True # Player 2 jump
            if event.key == pygame.K_LEFT:
                ml = True # Player 2 move left
            if event.key == pygame.K_RIGHT:
                mr = True # Player 2 move right
            if event.key == pygame.K_DOWN:
                player2_shoot = True # Player 2 shoot
            if event.key == pygame.K_SPACE and player2.ammo <= 0:
                player2.ammo = 10 # Refill player 2 ammo

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False # Stop moving left
            if event.key == pygame.K_d:
                moving_right = False # Stop moving right
            if event.key == pygame.K_LEFT:
                ml = False # Stop moving left for player 2
            if event.key == pygame.K_RIGHT:
                mr = False # Stop moving right for player 2
            if event.key == pygame.K_s:
                player_shoot = False # Stop shooting for player
            if event.key == pygame.K_DOWN:
                player2_shoot = False # Stop shooting for player 2

    pygame.display.update() # Update the screen

# Quit Pygame after the game loop ends
pygame.quit()