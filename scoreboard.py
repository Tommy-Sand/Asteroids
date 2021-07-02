import pygame, math

class Scoreboard:
    def __init__(self, surface):
        self.surface = surface
        self.score = 0
        self.lives_score = 0
        self.number_of_ships = 3
        self.start = (1600,0)
        self.create_lives()

    #This method increments the scoreboard by the amount
    def increment(self, amount, ship):
        self.score += amount
        self.lives_score += amount
        self.add_life(ship)

    #This method renders the scoreboard on the surface
    def render(self):
        text_string1 = str(self.score)
        text_color = pygame.Color('white')
        text_font = pygame.font.SysFont('Arial MT', 48)
        text_image = text_font.render(text_string1, True, text_color)
        text_pos1 = (0, 0)
        self.surface.blit(text_image, text_pos1)
        self.render_lives()

    def create_lives(self):
        polygon1 = (int(10 + 10*math.cos(math.pi*90/180)), int(10 - 10*math.sin(math.pi*90/180)))
        polygon2 = (int(10 + 7*math.cos(math.pi*225/180)), int(10 - 7*math.sin(math.pi*225/180)))
        polygon4 = (int(10 + 7*math.cos(math.pi*315/180)), int(10 - 7*math.sin(math.pi*315/180)))
        polygon = (polygon1, polygon2, (10,10), polygon4)
        color = pygame.Color("white")
        self.SHIP = pygame.Surface((30,30), pygame.SRCALPHA)
        pygame.draw.line(self.SHIP, color, polygon1, polygon2, 1)
        pygame.draw.line(self.SHIP, color, polygon2, polygon4, 1)
        pygame.draw.line(self.SHIP, color, polygon4, polygon1, 1)

    def render_lives(self):
        for i in range(1, self.number_of_ships + 1):
            self.surface.blit(self.SHIP, (self.start[0] - (self.SHIP.get_width() * i) , self.start[1]))

    def add_life(self, ship):
        if self.lives_score/10000  > 1:
            ship.add_life()
            self.number_of_ships += 1
            self.lives_score -= 10000

    def remove_life(self, ship):
        self.number_of_ships -= 1