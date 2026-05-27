# ===================================================================================================
# 9TH-GRADE CHEAT SHEET
# ---------------------------------------------------------------------------------------------------
# * OBJECT: A "thing" in your code that can hold data and do actions. Think of it like a character
#   in a game.
#
# * ATTRIBUTE: A variable that belongs to an object. It describes the object, like its health,
#   speed, or color.
#
# * METHOD: A function that lives inside a class. It is an action that the object knows how to do.
#
# * OBJECT METHOD: When you actually tell a specific object to do one of its actions.
#
# * CORE CONCEPT: A basic coding building block like a variable, a loop, or an if-statement condition.
# ===================================================================================================

import pygame  # [OBJECT] Brings in the pygame module, which is a massive utility object full of game-making tools
import os  # [OBJECT] Brings in the os module, which is a tool object used to read folders and files on your computer

pygame.init()  # [OBJECT METHOD] Starts up all the hidden background engines inside the pygame object so the game can run

SCREEN_WIDTH = 800  # [CORE CONCEPT] Creates a global variable that stores an integer number for how wide the screen is in pixels
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)  # [CORE CONCEPT] Creates a global variable for the screen height by multiplying the width by zero point eight

clock = pygame.time.Clock()  # [OBJECT] Creates a brand new Clock object and names it clock so we can control the game speed
FPS = 60  # [CORE CONCEPT] Creates a global variable holding the number sixty, which is our target frames per second

moving_left = False  # [CORE CONCEPT] Creates a global variable holding a true or false value to track if Player One is moving left
moving_right = False  # [CORE CONCEPT] Creates a global variable holding a true or false value to track if Player One is moving right

ml = False  # [CORE CONCEPT] Creates a global variable holding a true or false value to track if Player Two is moving left
mr = False  # [CORE CONCEPT] Creates a global variable holding a true or false value to track if Player Two is moving right

gravity = 0.75  # [CORE CONCEPT] Creates a global physics variable holding a decimal number to pull characters downward

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # [OBJECT] Creates the main game window surface object and names it screen
pygame.display.set_caption("Diego's Shooter Game")  # [OBJECT METHOD] Tells the pygame display tool to change the text attribute of the window title bar

background_color = (124, 45, 255)  # [CORE CONCEPT] Creates a global tuple variable holding three numbers that mix together to make a purple color


def draw_background():  # [CORE CONCEPT] Groups together a block of code into a custom function object that draws the game backdrop
    screen.fill(background_color)  # [OBJECT METHOD] Tells our screen object to erase everything by flooding itself with our purple color variable
    pygame.draw.line(screen, (255, 0, 0), (0, 300), (SCREEN_WIDTH, 300))  # [OBJECT METHOD] Tells the pygame drawing tool to paint a red line across the screen object canvas


class Soldier(pygame.sprite.Sprite):  # [CORE CONCEPT] Creates a blueprint class object used to build individual player and enemy characters
    def __init__(self, x, y, scale, speed, char_type, ammo, health):  # [METHOD] The setup function that runs automatically every time a new character object is built
        pygame.sprite.Sprite.__init__(self)  # [OBJECT METHOD] Runs the setup code of the built in sprite utility to register this new object correctly
        self.char_type = char_type  # [ATTRIBUTE] Stores a text description on this character to remember if they are a player or an enemy
        self.animation_list = []  # [ATTRIBUTE] Creates an empty list on this character that will hold all their different animation pictures
        self.frame_index = 0  # [ATTRIBUTE] Creates a number variable on this character to track which picture frame they are currently showing
        self.update_time = pygame.time.get_ticks()  # [ATTRIBUTE] Stores a timestamp on this character tracking the exact millisecond they were built
        self.action = 0  # [ATTRIBUTE] Stores a state number on this character where zero means idle, one means run, and two means jump
        self.jump = False  # [ATTRIBUTE] Stores a true or false flag on this character to track if the player just pressed the jump button
        self.in_air = False  # [ATTRIBUTE] Stores a true or false flag on this character to know if they are floating off the ground
        self.ammo = ammo  # [ATTRIBUTE] Stores a number on this character to keep track of how many bullets they have left to shoot
        self.shoot_cooldown = 0  # [ATTRIBUTE] Stores a countdown timer number on this character to prevent them from shooting too fast

        animation_types = ['Idle', 'Run', 'Jump', 'Death']  # [CORE CONCEPT] Creates a temporary local list holding the text names of our four asset folders
        for animation in animation_types:  # [LOOP] Starts a loop that repeats exactly four times to look inside each animation folder name
            temp_list = []  # [CORE CONCEPT] Creates a temporary empty list that resets on every loop to hold pictures for the current folder
            num_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))  # [CORE CONCEPT] Uses the os folder tool to count exactly how many pictures are in the folder

            for i in range(num_frames):  # [NESTED LOOP] Starts a sub loop inside our main loop that repeats once for every picture found in the folder
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png')  # [OBJECT] Loads a single picture file from your computer disk as a new picture surface object
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))  # [OBJECT METHOD] Changes the size of our new image object by reading its width and height attributes
                temp_list.append(img)  # [CORE CONCEPT] Puts the newly resized image object into our temporary list collection variable

            self.animation_list.append(temp_list)  # [ATTRIBUTE] Saves the group of images from the temporary list into the character permanent list attribute

        self.image = self.animation_list[self.action][self.frame_index]  # [ATTRIBUTE] Chooses one picture surface object from our list and sets it as the character active look

        self.rect = self.image.get_rect()  # [ATTRIBUTE] Generates an invisible hitbox rectangle object and saves it as an attribute on this character
        self.rect.center = (x, y)  # [ATTRIBUTE] Changes the center X and Y coordinate attributes inside our hitbox rectangle object to position the character
        self.direction = 1  # [ATTRIBUTE] Creates a number attribute where one means facing right and negative one means facing left
        self.flip = False  # [ATTRIBUTE] Creates a true or false flag attribute that tells the game whether to flip the character image backwards
        self.speed = speed  # [ATTRIBUTE] Creates a number attribute that sets how many pixels this character can walk in a single frame
        self.velocity_y = 0  # [ATTRIBUTE] Creates a physics speed attribute tracking how fast the character is moving up or down
        self.health = health  # [ATTRIBUTE] Creates a health pool attribute that tracks how much damage this character can take before dying
        self.alive = True  # [ATTRIBUTE] Creates a status flag attribute that stays true while the character is active and alive
        self.bullet_group = pygame.sprite.Group()  # [ATTRIBUTE] Creates a special container group object that will hold all the bullets fired by this character

    def draw(self):  # [METHOD] A function built into the class that lets this character object draw its picture onto the screen
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)  # [OBJECT METHOD] Draws the character image attribute onto the screen object while checking the flip attribute

    def move(self, moving_left, moving_right):  # [METHOD] A function built into the class that handles moving the character hitbox coordinates
        dx = 0  # [CORE CONCEPT] Creates a temporary local variable to track horizontal movement for just this single frame
        dy = 0  # [CORE CONCEPT] Creates a temporary local variable to track vertical movement for just this single frame

        if moving_left:  # [CONDITION] Checks if the incoming moving left variable is true because the player is holding the key down
            dx = -self.speed  # [CORE CONCEPT] Subtracts the character speed attribute from our local movement variable to slide them left
            self.flip = True  # [ATTRIBUTE] Changes the character flip attribute to true so the artwork faces left
            self.direction = -1  # [ATTRIBUTE] Sets the character direction attribute to negative one to track that they face left

        if moving_right:  # [CONDITION] Checks if the incoming moving right variable is true because the player is holding the key down
            dx = self.speed  # [CORE CONCEPT] Adds the character speed attribute to our local movement variable to slide them right
            self.flip = False  # [ATTRIBUTE] Changes the character flip attribute to false so the artwork faces right standard
            self.direction = 1  # [ATTRIBUTE] Sets the character direction attribute to positive one to track that they face right

        if self.jump == True and self.in_air == False:  # [CONDITION] Checks if the character jump attribute is true and their in air attribute is false
            self.jump = False  # [ATTRIBUTE] Resets the character jump attribute to false so they do not keep jumping forever
            self.in_air = True  # [ATTRIBUTE] Sets the character in air attribute to true so they cannot jump again while floating
            self.velocity_y = -14  # [ATTRIBUTE] Gives the character velocity attribute a negative number to shoot them upward into the sky

        self.velocity_y += gravity  # [ATTRIBUTE] Constantly increases the character velocity attribute by adding the global gravity number
        if self.velocity_y > 10:  # [CONDITION] Checks if the character falling speed attribute has become faster than terminal velocity
            self.velocity_y = 10  # [ATTRIBUTE] Caps the character velocity attribute so they do not fall through the floor too fast

        dy += self.velocity_y  # [CORE CONCEPT] Adds the character vertical velocity attribute value to our local frame movement variable

        if self.rect.bottom + dy > 300:  # [CONDITION] Checks if the bottom attribute of our hitbox rectangle goes past the red floor line
            dy = 300 - self.rect.bottom  # [CORE CONCEPT] Recalculates our local dy variable so the character stops exactly on top of the floor line
            self.in_air = False  # [ATTRIBUTE] Changes the character in air attribute to false because they are standing on solid ground

        self.rect.x += dx  # [ATTRIBUTE] Changes the horizontal X position attribute inside our character rect hitbox object
        self.rect.y += dy  # [ATTRIBUTE] Changes the vertical Y position attribute inside our character rect hitbox object

    def update_animation(self):  # [METHOD] A function built into the class that handles animation timers and switching pictures
        cooldown = 100  # [CORE CONCEPT] Creates a local variable setting the speed of the animation to one hundred milliseconds per frame
        self.image = self.animation_list[self.action][self.frame_index]  # [ATTRIBUTE] Swaps the character image attribute to show the current animation frame

        if pygame.time.get_ticks() - self.update_time > cooldown:  # [CONDITION] Checks if enough time has passed on the clock to change the picture
            self.update_time = pygame.time.get_ticks()  # [ATTRIBUTE] Resets the character update time attribute to the current clock time
            self.frame_index += 1  # [ATTRIBUTE] Adds one to the character frame index attribute to move to the next picture frame

        if self.frame_index >= len(self.animation_list[self.action]):  # [CONDITION] Checks if our frame index attribute has reached the end of the picture list
            if self.action == 3:  # [CONDITION] Checks if the character action attribute is currently set to three, which means Death
                self.frame_index = len(self.animation_list[self.action]) - 1  # [ATTRIBUTE] Freezes the frame index attribute on the final picture so the corpse stays flat
            else:  # [CORE CONCEPT] Runs if the character is doing any normal action like walking or idling
                self.frame_index = 0  # [ATTRIBUTE] Resets the character frame index attribute back to zero to loop the animation from the start

    def update(self):  # [METHOD] A general manager function inside the class that runs every frame to maintain the character status
        self.update_animation()  # [OBJECT METHOD] Tells this specific character object to run its internal animation update function
        if self.shoot_cooldown > 0:  # [CONDITION] Checks if the character weapon cooldown timer attribute is currently above zero
            self.shoot_cooldown -= 1  # [ATTRIBUTE] Subtracts one from the character shoot cooldown attribute frame counter

    def update_action(self, new_action):  # [METHOD] A function inside the class that changes the character current behavior state
        if new_action != self.action:  # [CONDITION] Checks if the new incoming action number is different from our current action attribute
            self.action = new_action  # [ATTRIBUTE] Overwrites the character action attribute with the new action state number
            self.frame_index = 0  # [ATTRIBUTE] Resets the frame index attribute to zero so the new animation starts at the beginning
            self.update_time = pygame.time.get_ticks()  # [ATTRIBUTE] Resets the update time attribute to sync the animation clock accurately

    def shoot(self):  # [METHOD] A function inside the class that lets a character spawn and shoot a bullet object
        if self.ammo > 0 and self.shoot_cooldown == 0:  # [CONDITION] Checks if the character ammo attribute is above zero and their cooldown attribute is zero
            self.shoot_cooldown = 20  # [ATTRIBUTE] Sets the character shoot cooldown attribute to twenty frames to make them wait before firing again
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)  # [OBJECT] Spawns a brand new Bullet object using character attributes as starting coordinates
            self.bullet_group.add(bullet)  # [OBJECT METHOD] Adds our new bullet object into this character bullet group container attribute
            self.ammo -= 1  # [ATTRIBUTE] Subtracts one bullet from the character ammo attribute stock pool

    def check_alive(self):  # [METHOD] A function inside the class that monitors the character health points pool
        if self.health <= 0:  # [CONDITION] Checks if the character health attribute has dropped down to dead levels
            self.alive = False  # [ATTRIBUTE] Flips the character alive attribute to false to turn off their controls
            self.speed = 0  # [ATTRIBUTE] Sets the character speed attribute to zero so they instantly stop sliding across the screen
            self.update_action(3)  # [OBJECT METHOD] Tells this character object to switch its action attribute to three to play the death scene


bullet_img = pygame.image.load('img/icons/bullet.png')  # [OBJECT] Loads the bullet artwork from your computer disk as a shared global surface object


class Bullet(pygame.sprite.Sprite):  # [CORE CONCEPT] Creates a blueprint class object used to build individual flying bullet projectile objects
    def __init__(self, x, y, direction):  # [METHOD] The setup function that runs automatically every time a new bullet object is spawned
        pygame.sprite.Sprite.__init__(self)  # [OBJECT METHOD] Runs the setup code of the built in sprite utility to register this bullet instance
        self.speed = 10  # [ATTRIBUTE] Creates a speed attribute on this bullet determining how many pixels it flies across the screen per frame
        self.image = bullet_img  # [ATTRIBUTE] Links our shared bullet artwork surface object directly to this bullet image attribute
        self.rect = self.image.get_rect()  # [ATTRIBUTE] Generates an invisible hitbox rectangle object and saves it as an attribute on this bullet
        self.rect.center = (x, y)  # [ATTRIBUTE] Centers our bullet rect hitbox attribute coordinates directly on top of the gun muzzle position
        self.direction = direction  # [ATTRIBUTE] Stores the character facing direction number onto this bullet direction attribute

    def update(self):  # [METHOD] A function inside the class that handles moving the bullet and tracking target impacts
        self.rect.x += self.direction * self.speed  # [ATTRIBUTE] Changes the horizontal X position attribute of our bullet rect hitbox to fly it forward

        if pygame.sprite.spritecollide(player, player2.bullet_group, False):  # [OBJECT METHOD] Uses a collision tool to check if the player object overlaps player2's bullet group attribute
            player.health -= 5  # [ATTRIBUTE] Directly subtracts five points from the player object health attribute pool
            self.kill()  # [OBJECT METHOD] Tells this specific bullet object to destroy itself and disappear from the game entirely

        if pygame.sprite.spritecollide(player2, player.bullet_group, False):  # [OBJECT METHOD] Uses a collision tool to check if the player2 object overlaps player's bullet group attribute
            player2.health -= 5  # [ATTRIBUTE] Directly subtracts five points from the player2 object health attribute pool
            self.kill()  # [OBJECT METHOD] Tells this specific bullet object to destroy itself and disappear from the game entirely


player = Soldier(200, 200, 3, 5, "player", 10, 100)  # [OBJECT] Creates a unique Soldier object named player to act as our Player One character
player2 = Soldier(400, 200, 3, 5, "enemy", 10, 100)  # [OBJECT] Creates a second unique Soldier object named player2 to act as our Player Two character

player_shoot = False  # [CORE CONCEPT] Creates a global tracking variable holding a true or false value for Player One shooting status
player2_shoot = False  # [CORE CONCEPT] Creates a global tracking variable holding a boolean true or false value for Player Two shooting status

run = True  # [CORE CONCEPT] Creates a loop control variable that keeps our game running as long as it holds a true value
while run:  # [LOOP] Starts the main game loop that loops over and over on repeat to refresh the game world
    clock.tick(FPS)  # [OBJECT METHOD] Tells our clock object to slow down the loop execution speed so it locks at sixty frames per second
    draw_background()  # [CORE CONCEPT] Runs our custom global function object to wipe the screen clean with background colors

    player.check_alive()  # [OBJECT METHOD] Tells our player object to run its internal function to verify if its health attribute is above zero
    player2.check_alive()  # [OBJECT METHOD] Tells our player2 object to run its internal function to verify if its health attribute is above zero

    if player.alive:  # [CONDITION] Reads the alive attribute of our player object to make sure they can still move
        player.move(moving_left, moving_right)  # [OBJECT METHOD] Tells our player object to run its move function using Player One global input variables
        if player_shoot:  # [CONDITION] Checks if the global player shoot control variable is currently set to true
            player.shoot()  # [OBJECT METHOD] Tells our player object to execute its internal shoot weapon method function
        if player.health <= 0:  # [CONDITION] Checks if the player object health attribute has dropped down to dead levels
            player.update_action(3)  # [OBJECT METHOD] Tells the player object to switch its action attribute to three to trigger death artwork
        elif player.in_air:  # [CONDITION] Checks if the player object in air physics attribute flag is currently set to true
            player.update_action(2)  # [OBJECT METHOD] Tells the player object to switch its action attribute to two to trigger jumping artwork
        elif moving_left or moving_right:  # [CONDITION] Checks if either Player One keyboard movement input variable is holding a true state
            player.update_action(1)  # [OBJECT METHOD] Tells the player object to switch its action attribute to one to trigger running artwork
        else:  # [CORE CONCEPT] Runs as a fallback if Player One is alive but standing completely still
            player.update_action(0)  # [OBJECT METHOD] Tells the player object to switch its action attribute to zero to trigger idling artwork

    if player2.alive:  # [CONDITION] Reads the alive attribute of our player2 object to make sure they can still move
        player2.move(ml, mr)  # [OBJECT METHOD] Tells our player2 object to run its move function using Player Two global input variables
        if player2_shoot:  # [CONDITION] Checks if the global player2 shoot control variable is currently set to true
            player2.shoot()  # [OBJECT METHOD] Tells our player2 object to execute its internal shoot weapon method function
        if player2.health <= 0:  # [CONDITION] Checks if the player2 object health attribute has dropped down to dead levels
            player2.update_action(3)  # [OBJECT METHOD] Tells the player2 object to switch its action attribute to three to trigger death artwork
        elif player2.in_air:  # [CONDITION] Checks if the player2 object in air physics attribute flag is currently set to true
            player2.update_action(2)  # [OBJECT METHOD] Tells the player2 object to switch its action attribute to two to trigger jumping artwork
        elif ml or mr:  # [CONDITION] Checks if either Player Two keyboard movement input variable is holding a true state
            player2.update_action(1)  # [OBJECT METHOD] Tells the player2 object to switch its action attribute to one to trigger running artwork
        else:  # [CORE CONCEPT] Runs as a fallback if Player Two is alive but standing completely still
            player2.update_action(0)  # [OBJECT METHOD] Tells the player2 object to switch its action attribute to zero to trigger idling artwork

    player.update()  # [OBJECT METHOD] Tells our player object to refresh its internal animation counters and cooldown attributes
    player2.update()  # [OBJECT METHOD] Tells our player2 object to refresh its internal animation counters and cooldown attributes

    player.draw()  # [OBJECT METHOD] Tells our player object to read its look attributes and blit itself onto the monitor screen
    player2.draw()  # [OBJECT METHOD] Tells our player2 object to read its look attributes and blit itself onto the monitor screen

    player.bullet_group.update()  # [OBJECT METHOD] Tells the player bullet group collection attribute to update every single active bullet object inside it
    player.bullet_group.draw(screen)  # [OBJECT METHOD] Paints all active player bullet objects onto our main screen display surface object

    player2.bullet_group.update()  # [OBJECT METHOD] Tells the player2 bullet group collection attribute to update every single active bullet object inside it
    player2.bullet_group.draw(screen)  # [OBJECT METHOD] Paints all active player2 bullet objects onto our main screen display surface object

    for event in pygame.event.get():  # [LOOP] Starts an event loop that checks a list of hardware action objects sent by your computer mouse and keyboard
        if event.type == pygame.QUIT:  # [CONDITION] Checks the type attribute of the current event object to see if the user clicked the window close button
            run = False  # [CORE CONCEPT] Flips our global run variable to false which will stop our primary while loop and exit the game

        if event.type == pygame.KEYDOWN:  # [CONDITION] Checks if the event object type attribute represents a keyboard button being pressed down
            if event.key == pygame.K_w:  # [CONDITION] Checks if the key code map attribute of our event object matches the W key on your keyboard
                player.jump = True  # [ATTRIBUTE] Changes the jump state attribute inside our player object directly to a true value
            if event.key == pygame.K_a:  # [CONDITION] Checks if the key code map attribute of our event object matches the A key on your keyboard
                moving_left = True  # [CORE CONCEPT] Changes our global moving left variable to true to tell the player object to walk left
            if event.key == pygame.K_d:  # [CONDITION] Checks if the key code map attribute of our event object matches the D key on your keyboard
                moving_right = True  # [CORE CONCEPT] Changes our global moving right variable to true to tell the player object to walk right
            if event.key == pygame.K_s:  # [CONDITION] Checks if the key code map attribute of our event object matches the S key on your keyboard
                player_shoot = True  # [CORE CONCEPT] Changes our global player shoot variable to true to activate the player weapon firing loop
            if event.key == pygame.K_r and player.ammo <= 0:  # [CONDITION] Checks if the R key is pressed while the player object ammo attribute is empty
                player.ammo = 10  # [ATTRIBUTE] Refills the ammo tracking attribute inside the player object directly back up to ten units

            if event.key == pygame.K_UP:  # [CONDITION] Checks if the key code map attribute of our event object matches the Up arrow key on your keyboard
                player2.jump = True  # [ATTRIBUTE] Changes the jump state attribute inside our player2 object directly to a true value
            if event.key == pygame.K_LEFT:  # [CONDITION] Checks if the key code map attribute of our event object matches the Left arrow key on your keyboard
                ml = True  # [CORE CONCEPT] Changes our global ml variable to true to tell the player2 object to walk left
            if event.key == pygame.K_RIGHT:  # [CONDITION] Checks if the key code map attribute of our event object matches the Right arrow key on your keyboard
                mr = True  # [CORE CONCEPT] Changes our global mr variable to true to tell the player2 object to walk right
            if event.key == pygame.K_DOWN:  # [CONDITION] Checks if the key code map attribute of our event object matches the Down arrow key on your keyboard
                player2_shoot = True  # [CORE CONCEPT] Changes our global player2 shoot variable to true to activate the player2 weapon firing loop
            if event.key == pygame.K_SPACE and player2.ammo <= 0:  # [CONDITION] Checks if the Spacebar is pressed while the player2 object ammo attribute is empty
                player2.ammo = 10  # [ATTRIBUTE] Refills the ammo tracking attribute inside the player2 object directly back up to ten units

        if event.type == pygame.KEYUP:  # [CONDITION] Checks if the event object type attribute represents a keyboard button being released
            if event.key == pygame.K_a:  # [CONDITION] Checks if the key code map attribute of our event object matches the A key on your keyboard
                moving_left = False  # [CORE CONCEPT] Changes our global moving left variable to false to make the player object stop walking left
            if event.key == pygame.K_d:  # [CONDITION] Checks if the key code map attribute of our event object matches the D key on your keyboard
                moving_right = False  # [CORE CONCEPT] Changes our global moving right variable to false to make the player object stop walking right
            if event.key == pygame.K_LEFT:  # [CONDITION] Checks if the key code map attribute of our event object matches the Left arrow key on your keyboard
                ml = False  # [CORE CONCEPT] Changes our global ml variable to false to make the player2 object stop walking left
            if event.key == pygame.K_RIGHT:  # [CONDITION] Checks if the key code map attribute of our event object matches the Right arrow key on your keyboard
                mr = False  # [CORE CONCEPT] Changes our global mr variable to false to make the player2 object stop walking right
            if event.key == pygame.K_s:  # [CONDITION] Checks if the key code map attribute of our event object matches the S key on your keyboard
                player_shoot = False  # [CORE CONCEPT] Changes our global player shoot variable to false to stop the player weapon firing loop
            if event.key == pygame.K_DOWN:  # [CONDITION] Checks if the key code map attribute of our event object matches the Down arrow key on your keyboard
                player2_shoot = False  # [CORE CONCEPT] Changes our global player2 shoot variable to false to stop the player2 weapon firing loop

    pygame.display.update()  # [OBJECT METHOD] Tells the pygame display engine object to swap our finished drawing frame onto your physical monitor screen

pygame.quit()  # [OBJECT METHOD] Runs a closing cleaning function on the master pygame object to disconnect hardware memory safely as the window shuts down
