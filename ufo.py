import pygame, math, random

class UFO(pygame.sprite.Sprite):
    def __init__(self, surface, position, color, velocity):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.position = position
        self.color = color
        self.velocity = velocity
        self.angle = random.randint(0,360)
        self.UFO = pygame.Surface((50,50), pygame.SRCALPHA)
        self.ellipsce_rect = pygame.Rect(0, 25, 50, 25)
        self.arc_rect = pygame.Rect(13,12,25,25)
        pygame.draw.ellipse(self.UFO, self.color, self.ellipsce_rect, width = 1)
        pygame.draw.arc(self.UFO, self.color, self.arc_rect, math.pi * (-10/180), math.pi * (190/180), width = 1)
        self.mask = pygame.mask.from_surface(self.UFO)

    def draw(self):
        self.surface.blit(self.UFO, self.position)

    def move(self):
        self.position = (self.position[0] + self.velocity*(math.cos(math.radians(self.angle))), self.position[1] + self.velocity*(math.sin(math.radians(self.angle))))

    def collision_ship(self, ship, scoreboard, ufo):
        offset_ship = (int(self.position[0] - ship.center[0]), int(self.position[1] - ship.center[1]))
        overlap_ship = ship.mask.overlap(self.mask, offset_ship)
        return ship_rebirth(overlap_ship, ship, scoreboard, ufo)

    def collision_bullet(self, bullet):
        offset_asteroid = (int(bullet.position[0] - self.position[0] - 15), int(bullet.position[1] - self.position[1] - 15))
        overlap_asteroid = self.mask.overlap(bullet.mask, offset_asteroid)
        if overlap_asteroid != None:
            return overlap_asteroid

    def collision(self):
            if self.position[1] <= -20:
                self.position = (self.position[0], size[1] - 20)
                self.angle = random.randint(0,360)
            if self.position[0] <= -20:
                self.position = (size[0] - 20, self.position[1])
                self.angle = random.randint(0,360)
            if self.position[1] >= size[1] + 20:
                self.position = (self.position[0], 0)
                self.angle = random.randint(0,360)
            if self.position[0] >= size[0] + 20:
                self.position = (20, self.position[1])
                self.angle = random.randint(0,360)

    def shoot(self):
        return Bullet(self.surface, random.randint(0,360), (self.position[0] + (self.UFO.get_rect().right//2), self.position[1] + 10), self.color, 10)