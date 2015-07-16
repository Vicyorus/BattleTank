import pygame

from Explosion import Explosion

class Bullet(object):
    PLAYER, ENEMY = 1, 0
    
    def __init__(self, manager, parent, init_pos, direction, speed=3):
        self.manager = manager
        self.parent = parent
        
        self.image = pygame.image.load("res/tanks/bullet.png")
        self.explosion = pygame.image.load("res/explosions/bullet_explosion.png")
        
        self.rect = self.calculate_init_point(direction, init_pos)
        
        self.speed = self.calculate_speed(direction, speed)
     
     
    def calculate_speed(self, direction, speed):
        if direction == 0:  # Up
            return (0, -speed)
        if direction == 1:  # Down
            self.image = pygame.transform.rotate(self.image, 180)
            return (0, speed)
        if direction == 2:  # Left
            self.image = pygame.transform.rotate(self.image, 90)
            return (-speed, 0)
        if direction == 3:  # Right
            self.image = pygame.transform.rotate(self.image, -90)
            return (speed, 0)
        
        
    def calculate_init_point(self, direction, init_pos):
        rect = self.image.get_rect()
        
        posX = init_pos[0]
        posY = init_pos[1]
        
        if direction == 0:
            rect.x = posX + 12
            rect.y = posY - 14
        
        if direction == 1:
            rect.x = posX + 12
            rect.y = posY + 32
            
        if direction == 2:
            rect.x = posX - 14
            rect.y = posY + 12
        
        if direction == 3:
            rect.x = posX + 32
            rect.y = posY + 12
            
        return rect
    
    
    def update(self, blocks):
        posX = self.speed[0]
        posY = self.speed[1]
        
        self.rect.x += posX
        self.rect.y += posY
        
        # Si nos vamos a salir del mundo, explotamos
        if self.rect.x < 0:
            self.rect.x = 0
            self.explode()
            
        if self.rect.x > 632:
            self.rect.x = 632
            self.explode()
        
        if self.rect.y < 0:
            self.rect.y = 0
            self.explode()
        
        if self.rect.y > 568:
            self.rect.y = 568
            self.explode()
        
        crashed = False
        
        # Check if we crashed with another block
        for block in blocks:
            
            # We can't crash with ourselves... can we?
            if block == self:
                pass
                        
            # If we do crash, we tell the manager to destroy said block
            elif self.rect.colliderect(block):
                
                # Right after we check if we can destroy said block
                block_name = type(block).__name__
                
                if block_name in ["Block", "Heart", "Bullet"]:
                    self.impact_side(block)
                    if self.manager.destroy_element(block):  # Block tells us if it destroyed
                        crashed = True
                    else:  # Else, we explode
                        self.explode()
                
                elif block_name == "Enemy" and self.parent:  # Player bullet against enemy
                    self.impact_side(block)
                    
                    # If enemy tells us it destroyed, it's a kill
                    if self.manager.destroy_element(block):
                        self.manager.increment_kills()
                        crashed = True
                    else:  # Else, we explode
                        self.explode()
                
                elif block_name == "Enemy" and not self.parent:  # Enemy bullet hitting enemy
                    crashed = True
                    
                
                elif block_name == "Jugador" and not self.parent:  # Enemy bullet hitting the player
                    self.impact_side(block)
                    # If the player destroys, we destroy
                    if self.manager.destroy_element(block):
                        crashed = True
                    else:  # Else, we explode
                        self.explode()
                else:
                    pass
        
        if crashed:  # If we crashed, we destroy ourselves
            self.destroy()
    
    def destroy(self):
        if self.parent == self.PLAYER:
            self.manager.remove_player_bullet()
            
        self.manager.remove_bullet(self)
        return True

    
    def explode(self):
        if self.parent == self.PLAYER:
            self.manager.remove_player_bullet()
        
        # Create the explosion
        Explosion(self.manager, self.rect)
        
        self.manager.remove_bullet(self)
        return True
    
    
    def impact_side(self, block):
        posX = self.speed[0]
        posY = self.speed[1]
        
        if posX > 0:  # Left side
            self.rect.right = block.rect.left
        if posX < 0:  # Right side
            self.rect.left = block.rect.right
        if posY > 0:  # Upper side
            self.rect.bottom = block.rect.top
        if posY < 0:  # Lower side
            self.rect.top = block.rect.bottom