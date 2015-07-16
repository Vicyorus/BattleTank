import pygame
from Level import Level

pygame.mixer.init()

class GameManager(object):
    
    WIN_SOUND = pygame.mixer.Sound("res/sounds/won.wav")
    LOSE_SOUND = pygame.mixer.Sound("res/sounds/lose.wav")
    
    def __init__(self, game_window, level, cheats):
        self.game_window = game_window
        
        # Load the level
        self.elements = Level(self).load_level(level)
        
        if self.elements is False:  # Uh oh
            self.game_window.return_menu()
            return 
        
        if cheats:  # If cheats are on, the heart is indestructible
            self.elements["heart"].possible_hits = -1
                
        # Begin the timers for all the enemy holes
        for hole in self.elements["holes"]:
            hole.begin_timer()
        
        self.audio_channels = [pygame.mixer.Channel(i) for i in range(8)]
            
    
    def game_lost(self):
        # You just lost the game
        pygame.mixer.stop()
        
        self.reproduce_sound(self.LOSE_SOUND)
        
        self.game_window.game_over(0)
        
        
    def game_won(self):
        pygame.mixer.stop()
        
        self.reproduce_sound(self.WIN_SOUND)
        
        self.game_window.game_over(1)
    
    
    def player_shoot(self):
        self.elements["player"].shoot()
    
    
    def update_elements(self, tick):
        # Check if the enemy tanks were destroyed
        tanks = self.elements["enemy_count"]
        if tanks[0] == tanks[1] == tanks[2] == 0:
            if self.elements["enemies"] == []:
                self.game_won()
        
        # Update the player
        self.elements["player"].update(self.elements["blocks"] + self.elements["enemies"] + [self.elements["heart"]])
        
        # Update the bullets
        for bullet in self.elements["bullets"]:
            bullet.update(
                self.elements["bullets"] + self.elements["blocks"] + self.elements["enemies"] + [self.elements["player"], self.elements["heart"]]
            )
            
        # Update the enemies
        for enemy in self.elements["enemies"]:
            enemy.update(self.elements["blocks"] + [self.elements["player"], self.elements["heart"]] + self.elements["enemies"])
        
        # Update the timer
        self.elements["timer"].update(tick)
    
    
    def bullet_explode(self):
        pass
    
    
    def destroy_element(self, element):
        return element.destroy()
        
    
    def add_bullet(self, bullet):
        self.elements["bullets"].append(bullet)
        
    
    def remove_bullet(self, bullet):
        if bullet in self.elements["bullets"]:
            self.elements["bullets"].remove(bullet)
    
    
    def remove_player_bullet(self):
        # Indicate the player his bullet is no longer active
        self.elements["player"].active_bullets -= 1
    
    
    def increment_kills(self):
        self.elements["player"].kill_number += 1
        
        
    def remove_block(self, block):
        if block in self.elements["blocks"]:
            self.elements["blocks"].remove(block)
    
    
    def add_enemy(self, enemy):
        self.elements["enemies"].append(enemy)
        
    
    def remove_enemy(self, enemy):
        if enemy in self.elements["enemies"]:
            self.elements["enemies"].remove(enemy)
    
    
    def add_action(self, time, function):
        # Adds an action to the timer
        return self.elements["timer"].add_action(time, function)
        
    
    def remove_action(self, iden):
        # Removes an action from the timer
        self.elements["timer"].remove_action(iden)
    
    
    def add_explosion(self, explosion):
        self.elements["explosions"].append(explosion)
        
        
    def remove_explosion(self, explosion):
        # As explosions remove themselves, we know
        # they must be in the list (in theory)
        self.elements["explosions"].remove(explosion)
    
    
    def enemy_count(self, param=None):
        # According to the param, we either return the amount of enemies or
        # we remove one enemy from the given param
        
        if param == None:
            return self.elements["enemy_count"]
        else:
            self.elements["enemy_count"][param] -= 1
    
    
    def reproduce_sound(self, sound):
        
        # Find an empty channel and play on it
        for channel in self.audio_channels:
            if not channel.get_busy():
                channel.play(sound)