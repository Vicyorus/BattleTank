import pygame

from Tank import Enemy

class EnemyHole(object):
    
    def __init__(self, manager, position):
        self.manager = manager
        self.image = pygame.image.load("res/blocks/hole.png")
        
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
    
    
    def begin_timer(self):
        self.cronID = self.manager.add_action(5000, self.create_tank)
    
    
    def create_tank(self):
        available_tanks = self.manager.enemy_count()
        
        # In case we want a maximum of tanks in screen
        #if len(self.manager.elements["enemies"]) == 8:
        #    return
        
        # If there is a tank above the hole, no enemy spawns
        for tank in self.manager.elements["enemies"] + [self.manager.elements["player"]]:
            if self.rect.colliderect(tank):
                return
            
        # Create our enemy
        if available_tanks[0] != 0:  # Weak
            new_enemy = Enemy(self.manager, self.rect.x, self.rect.y, "normal", 3)
            self.manager.enemy_count(0)
        
        elif available_tanks[1] != 0:  # Med
            new_enemy = Enemy(self.manager, self.rect.x, self.rect.y, "5k", 2)
            self.manager.enemy_count(1)
        
        elif available_tanks[2] != 0: # Stronk
            new_enemy = Enemy(self.manager, self.rect.x, self.rect.y, "10k", 1)
            self.manager.enemy_count(2)
        
        else:  # No tanks left in the queue
            self.manager.remove_action(self.cronID)
            return
        
        # Add to the enemy list
        self.manager.add_enemy(new_enemy)        
        