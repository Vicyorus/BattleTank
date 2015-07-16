from uuid import uuid4

class Timer(object):
    def __init__(self):
        self.actions = []
        pass
    
    def add_action(self, time, function):
        action_dict = {
            "id": uuid4(),
            "time_passed": 0,
            "interval": time,
            "function": function
        }
        
        self.actions.append(action_dict)
        
        return action_dict["id"]
    
    def update(self, time_taken):
        for action in self.actions:
            action["time_passed"] += time_taken
            if action["time_passed"] >= action["interval"]:
                action["time_passed"] -= action["interval"]
                action["function"]()
                
    
    def remove_action(self, iden):
        for action in self.actions:
            if action["id"] == iden:
                self.actions.remove(action)