import pygame

from Explosion import Explosion

class Block(object):
    def __init__(self, manager, position, block_type):
        self.manager = manager
        
        self.image = pygame.image.load("res/blocks/{}.png".format(block_type))
        
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        
        self.block_type = block_type
        
        if block_type == "wood":
            self.possible_hits = 0
        elif block_type == "metal":
            self.possible_hits = 1
        elif block_type == "heart_1":
            self.possible_hits = 3
        else:  # Armored
            self.possible_hits = -1
            
        
    def destroy(self):
        # As the hit number for the armored block is -1, it won't destroy
        if self.possible_hits == 0:
            
            # Check if the 
            if self.block_type == "metal" and not self.can_shoot:
                return False
            
            # Cargamos la explosion
            Explosion(self.manager, self.rect)
            
            self.manager.remove_block(self)
            return True
        
        else:
            
            self.possible_hits -= 1
            if self.block_type == "metal":
                self.can_shoot = True
                self.ID = self.manager.add_action(3000, self.reset_timer)
        
        return False
    
    
    def reset_timer(self):
        # Only used by the metal block
        self.manager.remove_action(self.ID)
        self.possible_hits = 1
        self.can_shoot = False
    
    
class Heart(Block):
    def __init__(self, manager, position):
        Block.__init__(self, manager, position, "heart_1")
        self.images = self.load_images()
        self.image = self.images[4]
    
    
    def load_images(self):
        images_dict = {
            4: pygame.image.load("res/blocks/heart_1.png"),
            3: pygame.image.load("res/blocks/heart_2.png"),
            2: pygame.image.load("res/blocks/heart_3.png"),
            1: pygame.image.load("res/blocks/heart_4.png"),
        }
        return images_dict
        
        
    def destroy(self):
        if self.possible_hits == 3:  # First hit
            self.possible_hits -= 1
            self.image = self.images[3]
        elif self.possible_hits == 2:  # Second hit
            self.possible_hits -= 1
            self.image = self.images[2]
        
        elif self.possible_hits == 1:  # Third hit
            self.possible_hits -= 1
            self.image = self.images[1]
        
        elif self.possible_hits == 0:  # You lose
            self.manager.game_lost()
        
        return False