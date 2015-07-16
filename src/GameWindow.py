import pygame
import sys

from GameManager import GameManager

class GameWindow(object):
    WIN_IMAGE = pygame.image.load("res/game_over/win.png")
    LOSE_IMAGE = pygame.image.load("res/game_over/lose.png")
    
    def __init__(self, parent):
        
        # For drawing
        self.screen = parent.screen
        
        # To avoid having to make another button function
        self.button = parent.make_button
        
        # Runs at 60 FPS
        self.clock = pygame.time.Clock()
        
        # Font type of the enemy queue counter
        self.type_font = pygame.font.SysFont("arial", 10)
        
        
    def begin_game(self, level, cheat):
        
        # To avoid the timer from beginning early
        first_time = True
        
        self.game_running = True
        
        # Create the game manager
        self.manager = GameManager(self, level, cheat)
        
        # If we got shut off before we began (level error)
        if not self.game_running:
            return
        
        # Press P to pause
        self.pause = False
        
        while self.game_running:
            
            if first_time:
                actual_tick = 0
                first_time = False
                self.clock.tick(60)
            else:
                actual_tick = self.clock.tick(60)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                
                if event.type == pygame.KEYDOWN:
                   if event.key == 32:
                       self.manager.player_shoot()
                    
                   if event.key in [112, 80]:
                       self.pause = not self.pause
                    
            if not self.pause:
                # Update the logical part
                self.manager.update_elements(actual_tick)
                
                if self.game_running:
                    # And the graphical part
                    self.update_graphics()
                    pygame.display.update()
    
    
    def update_graphics(self):
        # Draw the game area background
        pygame.draw.rect(self.screen, (124, 124, 124), (0, 0, 640, 576))
        
        # The enemy queue counter
        pygame.draw.rect(self.screen, (206, 174, 125), (640, 0, 160, 576))
        
        # And a button to return to the main menu
        self.button("Main menu", (640, 526, 160, 50), ((42, 120, 35), (27, 77, 23)), funcion=self.return_menu)
        
        # We ask the manager for the elements
        elements = self.manager.elements
        
        for block in elements["blocks"]:
            self.screen.blit(block.image, block.rect)
        
        for hole in elements["holes"]:
            self.screen.blit(hole.image, hole.rect)
            
        for enemy in elements["enemies"]:
            self.screen.blit(enemy.image, enemy.rect)
        
        self.screen.blit(elements["player"].image, elements["player"].rect)
        self.screen.blit(elements["heart"].image, elements["heart"].rect)
        
        for explosion in elements["explosions"]:
            self.screen.blit(explosion.image, explosion.rect)
            
        for bala in elements["bullets"]:
            self.screen.blit(bala.image, bala.rect)
                
        self.update_counter()
        
        
    def game_over(self, we_won):
        if we_won:  
            self.screen.blit(self.WIN_IMAGE, (0,0))
        else:
            self.screen.blit(self.LOSE_IMAGE, (0,0))
        
        pygame.display.update()
        
        running = True
        while running:
            for event in pygame.event.get():               
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.return_menu()
                        running = False
                
    def return_menu(self):
        self.game_running = False
    
    
    def update_counter(self):
        self.enemies = self.manager.enemy_count()
        
        self.screen.blit(self.type_font.render("Enemies left on queue", 1, (0,0,0)), (645, 10))
        self.screen.blit(self.type_font.render("Weak: {}".format(self.enemies[0]), 1, (0,0,0)), (650, 30))
        self.screen.blit(self.type_font.render("Med: {}".format(self.enemies[1]), 1, (0,0,0)), (650, 50))
        self.screen.blit(self.type_font.render("Strong: {}".format(self.enemies[2]), 1, (0,0,0)), (650, 70))
   