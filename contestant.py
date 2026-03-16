# contestant.py
# Each contestant's data and popularity formula

class Contestant:
    def __init__(self, name, intelligence, communication, physical, adaptability):
        self.name          = name
        self.intelligence  = intelligence
        self.communication = communication
        self.physical      = physical
        self.adaptability  = adaptability
        self.popularity    = 0
        self.game_score    = 0
        self.alive         = True
        self.is_wildcard   = False

    def calculate_popularity(self):
        attr = (self.intelligence  * 0.30 +
                self.communication * 0.35 +
                self.physical      * 0.20 +
                self.adaptability  * 0.15)
        self.popularity = round(attr * 0.6 + self.game_score * 0.4)

    def __repr__(self):
        return (f"{self.name:12s} | Pop:{self.popularity:3d} | "
                f"I:{self.intelligence} C:{self.communication} "
                f"P:{self.physical} A:{self.adaptability}")
