import pygame, math, random

from pygame.transform import scale

class Asteroid(pygame.sprite.Sprite):
    ''' Asteroids movement and collision need to be completely rewritten so velocity is distrivuted non-evenly when broken up and smaller asteroids move faster than bigger asteroids'''
    def __init__(self, surface, position, image_name, velocity, scale, size):
        self.surface = surface
        self.position = position
        self.velocity = velocity
        self.image_name = image_name
        self.angle = (int(math.atan2(velocity[1], velocity[0]))/math.pi) * 180
        self.scale = scale
        self.size = size

        pygame.sprite.Sprite.__init__(self)
        self.ASTEROID = pygame.image.load(self.image_name)
        self.ASTEROID = pygame.transform.scale(self.ASTEROID,(int(self.scale*self.ASTEROID.get_width()), int(self.scale*self.ASTEROID.get_height())))
        self.mask = pygame.mask.from_surface(self.ASTEROID)

    def draw(self):
        self.surface.blit(self.ASTEROID, self.position)

    def move(self):
        self.position = (self.position[0] + self.velocity[0],self.position[1] - self.velocity[1])

    def collision_ship(self, ship):
        offset_asteroid = (int(ship.center[0] - self.position[0]), int(ship.center[1] - self.position[1]))
        overlap_asteroid = self.mask.overlap(ship.mask, offset_asteroid)
        return overlap_asteroid

    def calculate_bullet_offset(self, object):
        return (int(object.position[0] - self.position[0]), int(object.position[1] - self.position[1]))

    def calculate_position(self, object, direction = 1):
        return (self.position[0] + 10*math.cos(math.pi * (object.angle + (direction * 30))/180), self.position[1] - 10*math.sin(math.pi * (object.angle + (direction * 30))/180))

    def collision_bullet(self, bullet):
        offset_asteroid = self.calculate_bullet_offset(bullet)
        overlap_asteroid = self.mask.overlap(bullet.mask, offset_asteroid)
        if overlap_asteroid != None and self.scale > 16/25:
            temp = []
            temp.append(Asteroid(self.surface, self.calculate_position(bullet, direction = -1), self.image_name, self.calculate_velocity(bullet, True), (4*self.scale)/5, self.size))
            temp.append(Asteroid(self.surface, self.calculate_position(bullet), self.image_name, self.calculate_velocity(bullet, False), (4*self.scale)/5, self.size))
            return temp
        elif overlap_asteroid != None and self.scale <= 16/25:
            return []

    def collision_UFO(self, ufo):
        offset_asteroid = (int(ufo.position[0] - self.position[0]), int(ufo.position[1] - self.position[1]))
        overlap_asteroid = self.mask.overlap(ufo.mask, offset_asteroid)
        if overlap_asteroid != None and self.scale > 16/25:
            temp = []
            temp.append(Asteroid(self.surface, self.calculate_position(ufo, direction = -1), self.image_name, self.calculate_velocity(ufo, True), (4*self.scale)/5, self.size))
            temp.append(Asteroid(self.surface, self.calculate_position(ufo), self.image_name, self.calculate_velocity(ufo, False), (4*self.scale)/5, self.size))
            return temp
        elif overlap_asteroid != None:
            return []

    def collision(self):
            if self.position[1] <= -30:
                self.position = (self.position[0], self.size[1] - 15)
            if self.position[0] <= -30:
                self.position = (self.size[0] - 15, self.position[1])
            if self.position[1] >= self.size[1] + 30:
                self.position = (self.position[0], -15)
            if self.position[0] >= self.size[0] + 30:
                self.position = (-15, self.position[1])

    def calculate_velocity(self, bullet, thirty):
        total_velocity = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        if thirty:
            angle = self.angle - 30
        elif not thirty:
            angle = self.angle + 30
        a = total_velocity * math.cos(math.pi * (angle/180))
        b = total_velocity * math.sin(math.pi * (angle/180))
        return (a, b)