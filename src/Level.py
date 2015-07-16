import json
from os import getcwd, path
from Tkinter import Tk
from tkMessageBox import showwarning

from Tank import Player
from Block import Block, Heart
from Timer import Timer
from EnemyHole import EnemyHole

class Level(object):
    def __init__(self, manager):
        self.manager = manager
        pass
    
    def load_level(self, level_name):
        filename = getcwd() + "/res/levels/{}.txt".format(level_name)
        
        # In case the file no longer exists
        if not path.exists(filename):
            window = Tk()
            window.withdraw()
            showwarning("Error", "Looks like the level file is no longer available, we're sorry!")
            window.destroy()
            return False
            
        else:
            # We load all the elements on a dictionary
            element_dict = {
                "player": None,
                "enemy_count": None,
                "heart": None,
                "blocks": [],
                "holes": [],
                "enemies": [],
                "bullets": [],
                "explosions": []
            }
            
            elements = json.loads(open(filename).read())
            
            element_dict["timer"] = Timer()
            
            # Iterate through the file structure
            for element in elements:
                element_type = element["type"]
                if element_type == "player":
                    element_dict["player"] = Player(self.manager, element["pos"][0])
                
                elif element_type in ["wood", "metal", "armored"]:
                    for position in element["pos"]:
                        element_dict["blocks"].append(Block(self.manager, position, element_type))
                
                elif element_type == "hole":
                    for position in element["pos"]:
                        element_dict["holes"].append(EnemyHole(self.manager, position))
                
                elif element_type == "heart":
                    element_dict["heart"] = Heart(self.manager, element["pos"][0])
                
                elif element_type == "enemy_count":
                    element_dict["enemy_count"] = element["cant"]
            
            return element_dict
