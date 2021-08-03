import pygame, math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, surface, angle, position, color, length):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.angle = angle
        self.position = position
        self.color = color
        self.length = length
        self.velocity = 10
        self.x_coeff = math.cos(math.pi * (self.angle/180))
        self.y_coeff = math.sin(math.pi * (self.angle/180))
        self.radius = 5
        self.BULLET = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.BULLET, self.color, (0, 0), self.radius)
        self.mask = pygame.mask.from_surface(self.BULLET)

    def draw(self):
        self.surface.blit(self.BULLET, self.position)

    def move(self):
        self.position = (self.position[0] + (self.velocity * self.x_coeff), self.position[1] - (self.velocity * self.y_coeff))