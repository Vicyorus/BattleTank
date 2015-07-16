import pygame

class Explosion(object):
    
    BLOCK_IMAGE = pygame.image.load("res/explosions/block_explosion.png")
    BULLET_IMAGE = pygame.image.load("res/explosions/bullet_explosion.png")
    
    BULLET_SOUND = pygame.mixer.Sound("res/sounds/bullet_explosion.wav")
    BLOCK_SOUND = pygame.mixer.Sound("res/sounds/block_explosion.wav")
    
    def __init__(self, manager, rect):
        self.rect = rect
        self.manager = manager
        
        if self.rect.width == 8:  # Bullet
            self.image = self.BULLET_IMAGE
            self.sound = self.BULLET_SOUND
        else:
            self.image = self.BLOCK_IMAGE
            self.sound = self.BLOCK_SOUND
            
        # We add ourselves to the explosion list
        self.manager.add_explosion(self)
        
        # We create an action to stay on screen for 1/10 of a second
        self.ID = self.manager.add_action(100, self.destroy)
        self.manager.reproduce_sound(self.sound)
        
    def destroy(self):
        self.manager.remove_action(self.ID)
        self.manager.remove_explosion(self)