import pygame
from random import randint

from Bullet import Bullet
from Explosion import Explosion

class Tank(object):
    
    def __init__(self, manager, posX, posY, max_bullets=1, tank_type=1, level="normal"):
        
        # According to tank_type, the name of the image changes
        if tank_type:
            image_name = "tank"
        else:
            image_name = "enemy_tank"
            
        self.max_bullets = max_bullets
        self.active_bullets = 0
        
        self.tank_level = level
        self.bullet_speed = 3
        
        # Player or enemy?
        self.side = tank_type
        
        # 4 diferent images: normal, 5 kills, 10 kills, 15 kills
        # 4 diferent positions, depending where the tank is looking
        self.images = self.load_images(image_name)
        
        # By default, the tank looks up
        self.image = self.images["normal"]
        self.manager = manager
        
        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY
        
        self.movement_sound = pygame.mixer.Sound("res/sounds/movement_sound.wav")
        self.shoot_sound = pygame.mixer.Sound("res/sounds/shoot_sound.wav")
        
        self.wait_period = False
        
        
    def load_images(self, image_name):
        
        # Load the base images
        images_dict = {
            "normal": pygame.image.load("res/tanks/{}.png".format(image_name)),
            "5k": pygame.image.load("res/tanks/{}_2.png".format(image_name)),
            "10k": pygame.image.load("res/tanks/{}_3.png".format(image_name)),
        }
        
        if self.side:  # The player has 4 images, so we add it
            images_dict["15k"] = pygame.image.load("res/tanks/{}_4.png".format(image_name))
        
        return images_dict
    
    
    def update_position(self, posX, posY, blocks):
        
        # Update the X and Y coordinate
        self.rect.x += posX
        self.rect.y += posY
        
        crashed = False
        
        # Check if we get out of the map
        if self.rect.x < 0:
            self.rect.x = 0
            crashed = True
        
        elif self.rect.x > 608:
            self.rect.x = 608
            crashed = True
            
        if self.rect.y < 0:
            self.rect.y = 0
            crashed = True
        
        elif self.rect.y > 544:
            self.rect.y = 544
            crashed = True
        
        # Check if we hit a block
        for block in blocks:
            
            if block == self:
                pass
            
            elif self.rect.colliderect(block):
                if posX > 0:  # Left side crash
                    self.rect.right = block.rect.left
                if posX < 0:  # Right side crash
                    self.rect.left = block.rect.right
                if posY > 0:  # Upper side crash
                    self.rect.bottom = block.rect.top
                if posY < 0:  # Lower crash side
                    self.rect.top = block.rect.bottom
                
                # For the enemy tanks to change direction
                crashed = True
        
        return crashed
        
    
    def update_image(self):
        degrees = (0, 180, 90, 270)
        self.image = pygame.transform.rotate(self.images[self.tank_level], degrees[self.position])
        
    
    def shoot(self):
        if self.side:  # If it's the player, check max_bullets
            
            if self.active_bullets == self.max_bullets:
                pass
            
            elif not self.wait_period:
                self.manager.add_bullet(
                    Bullet(self.manager, self.side, (self.rect.x, self.rect.y), self.position, self.bullet_speed)
                )
                self.active_bullets += 1
                self.shoot_sound.play(0)
                
                self.wait_period = True
                self.ID = self.manager.add_action(500, self.load_bullet)
       
        else:
            self.manager.add_bullet(
                    Bullet(self.manager, self.side, (self.rect.x, self.rect.y), self.position, self.bullet_speed)
            )
            self.shoot_sound.play(0)
            
    
    def load_bullet(self):
        # We wait for half a second, to avoid glitching
        # and having more than 1 bullet for the player
        self.wait_period = False
        self.manager.remove_action(self.ID)
        

    def destroy(self):
        # As the enemies don't check the kill count, we can do this
        if self.tank_level == "15k":  # Only the player checks this
            self.tank_level = "10k"
            self.kill_number = 10
            self.speed = 4
            self.bullet_speed = 6
            self.update_image()
        
        elif self.tank_level == "10k":
            self.kill_number = 5
            self.tank_level = "5k"
            if self.side:
                self.speed = 2
                self.bullet_speed = 6 
        
        elif self.tank_level == "5k":
            self.kill_number = 0
            self.tank_level = "normal"
            if self.side:
                self.speed = 2
                self.bullet_speed = 3
        
        else:  # Last shot
            if self.side:  # Player, you just lost the game
                self.manager.game_lost()
                return True
            
            else:
                # If it's an enemy, stop shooting bullets
                self.update_shoot_time(True)
                
                # Load the explosion
                Explosion(self.manager, self.rect)
                
                # And eliminate ourselves
                self.manager.remove_enemy(self)
                return True
        
        self.update_shoot_time()
    
    
    def update_shoot_time(self):
        # This is just the basic function declaration
        # Only the Enemy uses this function, which is overwritten on its class
        pass
    
class Player(Tank):

    def __init__(self, screen, position):
        
        Tank.__init__(self, screen, position[0], position[1])
        
        # 2px por presion de tecla (inicial)
        self.speed = 2
        self.position = 0
        self.kill_number = 0
        self.active_bullet = False
    
    
    def update(self, blocks):
        # Check if we have to move
        keys = pygame.key.get_pressed()
    
        # Move the tank upwards
        if keys[pygame.K_UP]:
            self.update_position(0, -self.speed, blocks)
            self.position = 0
            
        # Move the tank downwards
        elif keys[pygame.K_DOWN]:
            self.update_position(0, self.speed, blocks)
            self.position = 1
            
        # Move the tank to the left
        elif keys[pygame.K_LEFT]:
            self.update_position(-self.speed, 0, blocks)
            self.position = 2
        
        # Move the tank to the right
        elif keys[pygame.K_RIGHT]:
            self.update_position(self.speed, 0, blocks)
            self.position = 3
            
        # Check if we have to update the tank and its image, according to the kills
        self.update_tank()
        self.update_image()
    
    
    def update_tank(self):
        if self.kill_number == 5:
            self.tank_level = "5k"
            self.bullet_speed = 6
        
        elif self.kill_number == 10:
            self.tank_level = "10k"
            self.speed = 4
        
        elif self.kill_number == 15:
            self.tank_level = "15k"
            self.bullet_speed = 9
            self.speed = 6
    


class Enemy(Tank):

    def __init__(self, manager, posX, posY, level, time):
        Tank.__init__(self, manager, posX, posY, tank_type=0, level=level)
        self.speed = 2
        self.position = 0
        self.keep_going = False
        self.shoot_time = time
        self.action_id = self.manager.add_action(time * 1000, self.shoot)
    

    def update(self, blocks):
        
        if not self.keep_going:
            action = randint(0, 4)
            self.keep_going = True
        else:
            action = self.position
        
        # Upwards
        if action == 0:
            if self.update_position(0, -self.speed, blocks):
                self.keep_going = False
            self.position = 0
            
        # Downwards
        if action == 1:
            if self.update_position(0, self.speed, blocks):
                self.keep_going = False
            self.position = 1
            
        # Left
        if action == 2:
            if self.update_position(-self.speed, 0, blocks):
                self.keep_going = False
            self.position = 2
        
        # Right
        if action == 3:
            if self.update_position(self.speed, 0, blocks):
                self.keep_going = False
            self.position = 3
        
        self.update_image()
    
    
    def update_shoot_time(self, destroy=False):
        
        self.manager.remove_action(self.action_id)
        
        if not destroy:
            self.shoot_time += 1
            self.action_id = self.manager.add_action(self.shoot_time * 1000, self.shoot)