import math, pygame, random
import bullet_file

class Ship(pygame.sprite.Sprite):
    def __init__(self, surface, center, color, size, lives = 3):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.color = color
        self.lives = lives
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.length = [10, 7, 7, 10]
        self.angle = [90, 225, 315]
        self.size = size
        self.center = center
        self.thruster = False
        self.polygon1 = (int(10 + self.length[0]*math.cos(math.pi*self.angle[0]/180)), int(10 - self.length[0]*math.sin(math.pi*self.angle[0]/180)))
        self.polygon2 = (int(10 + self.length[1]*math.cos(math.pi*self.angle[1]/180)), int(10 - self.length[1]*math.sin(math.pi*self.angle[1]/180)))
        self.polygon4 = (int(10 + self.length[2]*math.cos(math.pi*self.angle[2]/180)), int(10 - self.length[2]*math.sin(math.pi*self.angle[2]/180)))
        self.polygon = (self.polygon1, self.polygon2, (10,10), self.polygon4)
        self.SHIP = pygame.Surface((30,30), pygame.SRCALPHA)
        pygame.draw.line(self.SHIP, self.color, self.polygon1, self.polygon2, 1)
        pygame.draw.line(self.SHIP, self.color, self.polygon2, self.polygon4, 1)
        pygame.draw.line(self.SHIP, self.color, self.polygon4, self.polygon1, 1)
        self.mask = pygame.mask.from_surface(self.SHIP)

    def rotate(self, angle):
        for i in range(0, 3):
            self.angle[i] += angle
        self.mask_update()

    def mask_update(self):
        self.SHIP = pygame.Surface((30,30), pygame.SRCALPHA)
        self.mask.clear()
        pygame.draw.line(self.SHIP, self.color, self.polygon1, self.polygon2, 1)
        pygame.draw.line(self.SHIP, self.color, self.polygon2, self.polygon4, 1)
        pygame.draw.line(self.SHIP, self.color, self.polygon4, self.polygon1, 1)
        self.mask = pygame.mask.from_surface(self.SHIP)

    def draw(self):
        self.surface.blit(self.SHIP,(int(self.center[0]), int(self.center[1])))

    def accelerate(self, acceleration):
        self.acceleration = [self.acceleration[0] + acceleration*math.cos(math.pi*(self.angle[0]/180)), self.acceleration[1] - acceleration*math.sin(math.pi*(self.angle[0]/180))]

    def acceleration_correction(self):
        if self.acceleration[0] > 0:
            self.acceleration[0] -= self.acceleration[0]/8
        elif self.acceleration[0] < 0:
            self.acceleration[0] += -(self.acceleration[0]/8)
        if self.acceleration[1] > 0:
            self.acceleration[1] -= self.acceleration[1]/8
        elif self.acceleration[1] < 0:
            self.acceleration[1] += -(self.acceleration[1]/8)
        self.velocity_correction()

#Add another variable so that it stores the angle of the last acceleration for angle calculations


    def velocity_correction(self):
        if self.velocity[0] > abs(math.cos(math.pi*self.angle[0]/180)):
            self.velocity[0] -= self.velocity[0]/20
        elif self.velocity[0] < -abs(math.cos(math.pi*self.angle[0]/180)):
            self.velocity[0] += -(self.velocity[0]/20)
        if self.velocity[1] > abs(math.sin(math.pi*self.angle[0]/180)):
            self.velocity[1] -= self.velocity[1]/20
        elif self.velocity[1] < -abs(math.sin(math.pi*self.angle[0]/180)):
            self.velocity[1] += -(self.velocity[1]/20)

    def velocity_move(self):
        self.velocity = [self.velocity[0] + self.acceleration[0], self.velocity[1] + self.acceleration[1]]

    def hyperspace(self):
        self.center = (random.randint(0,self.size[0]), random.randint(0,self.size[1]))

    def move(self):
        self.center = (self.center[0] + self.velocity[0], self.center[1] + self.velocity[1])
        self.polygon1 = (int(10 + self.length[0]*math.cos(math.pi*self.angle[0]/180)), int(10 - self.length[0]*math.sin(math.pi*self.angle[0]/180)))
        self.polygon2 = (int(10 + self.length[1]*math.cos(math.pi*self.angle[1]/180)), int(10 - self.length[1]*math.sin(math.pi*self.angle[1]/180)))
        self.polygon4 = (int(10 + self.length[2]*math.cos(math.pi*self.angle[2]/180)), int(10 - self.length[2]*math.sin(math.pi*self.angle[2]/180)))
        self.polygon = (self.polygon1, self.polygon2, (10,10), self.polygon4)

    def collision_bullet(self, bullet):
        offset_bullet = (int(self.center[0] - bullet.position[0]), int(self.center[1] - bullet.position[1]))
        overlap_bullet = self.mask.overlap(bullet.mask, offset_bullet)
        return overlap_bullet

    def collision(self):
        if self.center[1] <= 0:
            self.center = (self.center[0], self.size[1] - 50)
        if self.center[0] <= 0:
            self.center = (self.size[0] - 50, self.center[1])
        if self.center[1] >= self.size[1]:
            self.center = (self.center[0], 0)
        if self.center[0] >= self.size[0]:
            self.center = (50, self.center[1])

    def shoot(self):
        return bullet_file.Bullet(self.surface, self.angle[0], (self.center[0] + self.polygon1[0], self.center[1] + self.polygon1[1]), self.color, 4)

    def add_life(self):
        self.lives += 1

    def rebirth(self, scoreboard):
        self.__init__(self.surface, (self.size[0]//2, self.size[1]//2), pygame.Color("white"), self.size, self.lives - 1)
        scoreboard.remove_life(self)
        print(self.lives)