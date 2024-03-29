import pygame, random, math
import bullet_file

class UFO(pygame.sprite.Sprite):
    def __init__(self, surface, position, color, velocity, size):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.position = position
        self.color = color
        self.velocity = velocity
        self.size = size
        self.angle = random.randint(0,360)
        self.UFO = pygame.Surface((50,50), pygame.SRCALPHA)
        self.ellipsce_rect = pygame.Rect(0, 25, 50, 25)
        pygame.draw.ellipse(self.UFO, self.color, self.ellipsce_rect,)
        pygame.draw.circle(self.UFO, self.color, (25,25), 13)
        self.mask = pygame.mask.from_surface(self.UFO)

    def draw(self):
        self.surface.blit(self.UFO, self.position)

    def move(self):
        self.position = (self.position[0] + self.velocity*(math.cos(math.radians(self.angle))), self.position[1] + self.velocity*(math.sin(math.radians(self.angle))))

    def collision_ship(self, ship):
        offset_ship = (int(self.position[0] - ship.center[0]), int(self.position[1] - ship.center[1]))
        overlap_ship = ship.mask.overlap(self.mask, offset_ship)
        return overlap_ship

    def collision_bullet(self, bullet):
        offset_asteroid = (int(bullet.position[0] - self.position[0] - 15), int(bullet.position[1] - self.position[1] - 15))
        overlap_asteroid = self.mask.overlap(bullet.mask, offset_asteroid)
        if overlap_asteroid != None:
            return overlap_asteroid

    def collision(self):
            if self.position[1] <= -20:
                self.position = (self.position[0], self.size[1] - 20)
                self.angle = random.randint(0,360)
            if self.position[0] <= -20:
                self.position = (self.size[0] - 20, self.position[1])
                self.angle = random.randint(0,360)
            if self.position[1] >= self.size[1] + 20:
                self.position = (self.position[0], 0)
                self.angle = random.randint(0,360)
            if self.position[0] >= self.size[0] + 20:
                self.position = (20, self.position[1])
                self.angle = random.randint(0,360)

    def shoot(self):
        return bullet_file.Bullet(self.surface, random.randint(0,360), (self.position[0] + (self.UFO.get_rect().right//2), self.position[1] + 10), self.color, 4)

class small_UFO(UFO):
    def __init__(self, surface, position, color, velocity, size):
        UFO.__init__(self, surface, position, color, velocity, size)
        self.UFO = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.ellipsce_rect = pygame.Rect(0, 17, 30, 17)
        pygame.draw.ellipse(self.UFO, self.color, self.ellipsce_rect)
        pygame.draw.circle(self.UFO, self.color, (15,16), 7)
        self.mask = pygame.mask.from_surface(self.UFO)