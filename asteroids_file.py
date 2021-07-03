import pygame, math, random

class Asteroid(pygame.sprite.Sprite):
    ''' Asteroids movement and collision need to be completely rewritten so velocity is distrivuted non-evenly when broken up and smaller asteroids move faster than bigger asteroids'''
    def __init__(self, surface, position, color, velocity, radius, size):
        self.surface = surface
        self.position = position
        self.color = color
        self.velocity = velocity
        self.angle = (int(math.atan2(velocity[1], velocity[0]))/math.pi) * 180
        self.radius = radius
        #self.width = 1
        self.size = size

        pygame.sprite.Sprite.__init__(self)
        self.ASTEROID = pygame.Surface((self.radius*2,self.radius*2),pygame.SRCALPHA)
        pygame.draw.circle(self.ASTEROID, self.color, (self.radius, self.radius), self.radius)
        self.mask = pygame.mask.from_surface(self.ASTEROID)

    def draw(self):
        self.surface.blit(self.ASTEROID, self.position)

    def move(self):
        self.position = (self.position[0] + self.velocity[0],self.position[1] - self.velocity[1])

    def collision_ship(self, ship):
        offset_asteroid = (int(ship.center[0] - self.position[0]), int(ship.center[1] - self.position[1]))
        overlap_asteroid = self.mask.overlap(ship.mask, offset_asteroid)
        return overlap_asteroid

    def calculate_bullet_offset(self, object, offsets_offset):
        return (int(object.position[0] - self.position[0]), int(object.position[1] - self.position[1]))

    def calculate_position(self, object, direction = 1):
        return (self.position[0] + 10*math.cos(math.pi * (object.angle + (direction * 30))/180), self.position[1] - 10*math.sin(math.pi * (object.angle + (direction * 30))/180))

    def collision_bullet(self, bullet):
        if self.radius == 30:
            offset_asteroid = self.calculate_bullet_offset(bullet, 5)
        elif self.radius == 20:
            offset_asteroid = self.calculate_bullet_offset(bullet, 10)
        else:
            offset_asteroid = self.calculate_bullet_offset(bullet, 15)
        overlap_asteroid = self.mask.overlap(bullet.mask, offset_asteroid)
        if overlap_asteroid != None and self.radius > 15:
            temp = []
            temp.append(Asteroid(self.surface, self.calculate_position(bullet, direction = -1), self.color, self.calculate_velocity(bullet, True), (2*self.radius)//3, self.size))
            temp.append(Asteroid(self.surface, self.calculate_position(bullet), self.color, self.calculate_velocity(bullet, False), (2*self.radius)//3, self.size))
            return temp
        elif overlap_asteroid != None and self.radius < 15:
            return []

    def collision_UFO(self, ufo):
        offset_asteroid = (int(ufo.position[0] - self.position[0]), int(ufo.position[1] - self.position[1]))
        overlap_asteroid = self.mask.overlap(ufo.mask, offset_asteroid)
        if overlap_asteroid != None and self.radius > 15:
            temp = []
            temp.append(Asteroid(self.surface, self.calculate_position(ufo, direction = -1), self.color, self.calculate_velocity(ufo, True), (2*self.radius)//3, self.size))
            temp.append(Asteroid(self.surface, self.calculate_position(ufo), self.color, self.calculate_velocity(ufo, False), (2*self.radius)//3, self.size))
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