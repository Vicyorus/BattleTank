# -*- coding: utf-8 -*-
import pygame, sys, json
from pygame.locals import *
from Tkinter import *
import tkMessageBox
import os

pygame.init()


class LevelBuilder(object):
    
    def __init__(self, screen):
        
        # Access to the main screen
        self.screen = screen.screen
        
        self.button = screen.make_button
        
        # The block we have currently on the mouse
        self.actual_block = None
        
        # The type of block we're currently holding
        self.block_type = None
               
        
        self.enemies = []
        
        # Load the images
        self.wood_image = pygame.image.load("res/blocks/wood.png")
        self.wood_image_valid = pygame.image.load("res/blocks/wood_val.png")
        self.wood_image_invalid = pygame.image.load("res/blocks/wood_inval.png")
        
        self.metal_image = pygame.image.load("res/blocks/metal.png")
        self.metal_image_valid = pygame.image.load("res/blocks/metal_val.png")
        self.metal_image_invalid = pygame.image.load("res/blocks/metal_inval.png")
        
        self.armored_image = pygame.image.load("res/blocks/armored.png")
        self.armored_image_valid = pygame.image.load("res/blocks/armored_val.png")
        self.armored_image_invalid = pygame.image.load("res/blocks/armored_inval.png")
        
        self.hole_image = pygame.image.load("res/blocks/hole.png")
        self.hole_image_valid = pygame.image.load("res/blocks/hole_val.png")
        self.hole_image_invalid = pygame.image.load("res/blocks/hole_inval.png")
        
        self.player_image = pygame.image.load("res/tanks/tank.png")
        self.player_image_valid = pygame.image.load("res/tanks/tank_val.png")
        self.player_image_invalid = pygame.image.load("res/tanks/tank_inval.png")
        
        self.heart_image = pygame.image.load("res/blocks/heart_1.png")
        self.heart_image_valid = pygame.image.load("res/blocks/heart_val.png")
        self.heart_image_invalid = pygame.image.load("res/blocks/heart_inval.png")
        
        
        # Text font
        self.font = pygame.font.SysFont("timesnewroman", 14)
        
        
    def create_level(self):
        
        # Creamos variables que ocupamos cada vez que iniciamos
        self.running = True
        
        self.active_heart = False
        self.active_player = False
        self.actual_block = None
        
        self.active_blocks = []
        self.final_map = []
        
        while self.running:
            
            # Ask for the current position of the mouse
            mouseX, mouseY = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Pressed the mouse
                if event.type == MOUSEBUTTONDOWN:
                    
                    # Over a block image
                    if 641 < mouseX < 673:
                        
                        
                        # Wood
                        if 17 < mouseY < 49:
                            self.actual_block = GenericBlock(
                                self,
                                "wood",
                                self.wood_image,
                                self.wood_image_invalid,
                                self.wood_image_valid,
                                0
                            )
                        
                        # Metal
                        if 49 < mouseY < 81:
                            self.actual_block = GenericBlock(
                                self,
                                "metal",
                                self.metal_image,
                                self.metal_image_invalid,
                                self.metal_image_valid,
                                1
                            )
                        
                        # Armored
                        if 81 < mouseY < 113:
                            self.actual_block = GenericBlock(
                                self,
                                "armored",
                                self.armored_image,
                                self.armored_image_invalid,
                                self.armored_image_valid,
                                2
                            )
                        
                        # Enemy Hole
                        if 113 < mouseY < 145:
                            self.actual_block = GenericBlock(
                                self, 
                                "hole", 
                                self.hole_image, 
                                self.hole_image_invalid, 
                                self.hole_image_valid, 
                                3
                            )
                        
                        # Special conditions for heart and player
                        # Player
                        if 145 < mouseY < 177 and not self.active_player:
                            self.actual_block = GenericBlock(
                                self,
                                "player",
                                self.player_image,
                                self.player_image_invalid,
                                self.player_image_valid,
                                4
                            )
                        
                        # Heart
                        if 177 < mouseY < 209 and not self.active_heart:
                            self.actual_block = GenericBlock(
                                self,
                                "heart",
                                self.heart_image,
                                self.heart_image_invalid,
                                self.heart_image_valid,
                                5
                            )
                    
                    # Check if we have to save the block
                    self.save_block()
                    
                    
            # Draw the game area
            pygame.draw.rect(self.screen, (124, 124, 124), (0, 0, 640, 576))
            
            # The option bar
            pygame.draw.rect(self.screen, (142, 125, 72), (640, 0, 160, 576))
            
            
            # Create the buttons
            self.button("Clear Map", (640, 426, 160, 50), ((42, 120, 35), (27, 77, 23)), funcion=self.reset_map)
            self.button("Save Map", (640, 476, 160, 50), ((42, 120, 35), (27, 77, 23)), funcion=self.save_map)
            self.button("Main Menu", (640, 526, 160, 50), ((42, 120, 35), (27, 77, 23)), funcion=self.return_main)
            
            
            # Draw the images and their texts
            self.screen.blit(self.font.render("Wood", False, (255, 255, 255)), (675, 25))
            self.screen.blit(self.font.render("Metal", False, (255, 255, 255)), (675, 57))
            self.screen.blit(self.font.render("Armored", False, (255, 255, 255)), (675, 89))
            self.screen.blit(self.font.render("Enemy Hole", False, (255, 255, 255)), (675, 121))
            
            self.screen.blit(self.wood_image, (641, 17))
            self.screen.blit(self.metal_image, (641, 49))
            self.screen.blit(self.armored_image, (641, 81))
            self.screen.blit(self.hole_image, (641, 113))
            
            # Check if we have to draw the player and the heart
            if not self.active_player: 
                self.screen.blit(self.font.render("Player", False, (255, 255, 255)), (675, 153))
                self.screen.blit(self.player_image, (641, 145))
                
            if not self.active_heart:
                self.screen.blit(self.font.render("Heart", False, (255, 255, 255)), (675, 185))
                self.screen.blit(self.heart_image, (641, 177))
            
            # Draw all alocated blocks
            for block in self.active_blocks:
                self.screen.blit(block.image, block.rect)
            
            # Update the block
            if self.actual_block != None:
                self.actual_block.update_pos()
                
            # If the block is still there, draw it
            if self.actual_block != None:
                self.screen.blit(self.actual_block.image, self.actual_block.rect)
                
            pygame.display.update()
    

    def return_main(self):
        self.running = False
    
    
    def reset_map(self):
        # Reset the map
        self.active_heart = False
        self.active_player = False
        self.actual_block = None
        
        self.active_blocks = []
        self.final_map = []
    

    def save_map(self):
        if not self.check_map():
            pass
        
        else:
            # Create the info window
            self.info_window = AskInfoWindow(self)
            
            # Y la llamamos
            self.info_window.ask_for_info()
            
            if self.enemies != []:
                # Open the file
                with open("res/levels/{}.txt".format(self.enemies[0]), "w") as f:
                    
                    # Add the enemies
                    self.final_map.append(self.enemies[1])
                    
                    # Convert to JSON
                    self.final_map = json.dumps(self.final_map)
                    
                    f.write(self.final_map)
                    
                    f.close()
        
                    self.reset_map()
        

    # Check if the map has the basics: heart, player and 1 enemy hole
    def check_map(self):
        # Invisible window
        window = Tk()
        window.withdraw()
        
        heart = False
        player = False
        hole = False
        
        if self.final_map == []:
            tkMessageBox.showwarning("Error", "Map can't be empty.")
            window.destroy()
            return False
        for element in self.final_map:
            if element["type"] == "heart":
                heart = True
            
            if element["type"] == "player":
                player = True
            
            if element["type"] == "hole":
                hole = True
        
        if not heart:
            tkMessageBox.showwarning("Error", "Map must contain the heart.")
            window.destroy()
            return False
        if not player:
            tkMessageBox.showwarning("Error", "Map must contain the player.")
            window.destroy()
            return False
        if not hole:
            tkMessageBox.showwarning("Error", "Map must contain at least one enemy hole.")
            window.destroy()
            return False
        
        window.destroy()
        return True
        
        
    def save_block(self):
        
        # Check if there is a block
        if self.actual_block is not None:
            block = self.actual_block

            # Check if the block is inside the game area and is not colliding
            if block.rect.x in range(609) and block.rect.y in range(545) and block.can_save:
                block.image = block.normal_image
                self.active_blocks.append(block)
                self.actual_block = GenericBlock(self, block.name, block.normal_image, block.invalid_image, block.valid_image, block.number)
                
                if block.name == "heart":
                    self.active_heart = True
                    self.actual_block = None
                    
                if block.name == "player":
                    self.active_player = True
                    self.actual_block = None
                
                for blocks in self.final_map:
                    # Check if the block type was already on the list, to add coordinates
                    if blocks["type"] == block.name:
                        blocks["pos"].append((block.rect.x, block.rect.y))
                        break
                else:
                    self.final_map.append(
                        {"type": block.name, 
                        "pos": [(block.rect.x, block.rect.y)]
                        }
                    )
        
        
class GenericBlock(object):
    def __init__(self, builder, name, normal_image, invalid_image, valid_image, block_number):
        
        self.builder = builder
        self.screen = builder.screen
        self.name = name
        
        self.normal_image = normal_image
        self.invalid_image = invalid_image
        self.valid_image = valid_image
        
        self.image = normal_image
        self.number = block_number
        
        self.update_pos()


    def update_pos(self):
        self.image = self.invalid_image
        
        # All blocks can be saved until the contrary is proven
        self.can_save = True
        
        # Draw a white rectangle around the block's icon
        pygame.draw.rect(self.screen, (255, 255, 255), (641, 17 + (self.number * 32), 32, 32), 1)
        
        # Update the position
        posX, posY = pygame.mouse.get_pos()
        self.rect = self.image.get_rect(center=(posX, posY))
        
        # Avoid getting out of the screen
        if self.rect.x < 0:
            self.rect.x = 0
            
        if self.rect.x > 768:
            self.rect.x = 768
        
        if self.rect.y < 0:
            self.rect.y = 0
        
        if self.rect.y > 544:
            self.rect.y = 544
            
        # Check if we're inside the game area
        if 0 <= self.rect.x <= 608 and 0 <= self.rect.y <= 544:
            self.image = self.valid_image
            
            # Check if we're colliding with someone
            for block in self.builder.active_blocks:
                if self.rect.colliderect(block.rect):
                    
                    # Block colliding against heart/player/hole
                    if block.number in [3, 4, 5] and self.number in [0, 1, 2]:
                        self.can_save = False
                        self.image = self.invalid_image
                    
                    # Player/heart/hole colliding with someone else
                    if self.number in [3, 4, 5]:
                        self.can_save = False
                        self.image = self.invalid_image


class AskInfoWindow(object):
    def __init__(self, builder):
        self.builder = builder
        self.window = Tk()
        
        self.window.title("Enemies")
        self.window.geometry ("300x200+300+100")
        self.window.resizable(height=False,width=False)
        
        icono = PhotoImage(file=os.getcwd() + '/res/logo/logo.gif')
        self.window.tk.call("wm", "iconphoto", self.window._w, icono)
        
        # Add the background image
        image = PhotoImage(file=os.getcwd() + "/res/backgrounds/tank2.gif")
        image_paste = Label(self.window, image=image)
        image_paste.image = image
        image_paste.place(x=0, y=0)
        
        self.save_button = Button(self.window, text="Save", command=self.save_info).place(x=215,y=100)
        
        level_label = Label(self.window, text="Level name:").place(x=10, y=30)
        weak_label = Label(self.window, text="Weak Enemy:").place(x=10, y=80)
        med_label = Label(self.window, text="Medium Enemy:").place(x=10, y=130)
        _label = Label(self.window, text="Strong Enemy:").place(x=10, y=170)
        
        # Vars
        self.weak_count = IntVar()
        self.med_count = IntVar()
        self._count = IntVar()
        self.level_name = StringVar()
        
        #Línea de texto
        self.name_entry = Entry(self.window, textvariable=self.level_name, width=10).place(x=120,y=30)
        self.weak_entry = Entry(self.window, textvariable=self.weak_count, width=10).place(x=120,y=80)
        self.med_entry = Entry(self.window, textvariable=self.med_count, width=10).place(x=120,y=130)
        self._entry = Entry(self.window, textvariable=self._count, width=10).place(x=120,y=170)
        
    
    def check_info(self):
        name = self.level_name.get()
        
        try:
            weak = self.weak_count.get()
            med = self.med_count.get()
            strong = self._count.get()
        except ValueError:
            tkMessageBox.showwarning("Error", "All quantities of enemies must be numbers.")
            return False
        
        # Check the level has a name
        if name == "":
            tkMessageBox.showwarning("Error", "Map name can't be empty.")
            return False
        
        # Check there's at least 1 enemy
        if weak == med == strong == 0:
            tkMessageBox.showwarning("Error", "There has to be at least 1 enemy on this level.")
            return False
        
        if weak < 0:
            tkMessageBox.showwarning("Error", "You can't have a negative count of weak enemies.")
            return False
        
        elif med < 0:
            tkMessageBox.showwarning("Error", "You can't have a negative count of medium enemies.")
            return False
        
        elif strong < 0:
            tkMessageBox.showwarning("Error", "You can't have a negative count of strong enemies.")
            return False
        
        if len(name) > 15:
            tkMessageBox.showwarning("Error", "Level name must be under 15 characters.")
            return False
        
        return [name, {"type": "enemy_count", "cant": [weak, med, strong]}]
    
    
    def save_info(self):
        info = self.check_info()
        if info is not False:
            tkMessageBox.showinfo("Success", "Map saved successfully!")
            self.builder.enemies = info
            self.window.destroy()
            return
    
    
    def ask_for_info(self):
        self.window.mainloop()
