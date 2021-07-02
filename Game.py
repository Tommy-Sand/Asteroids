import pygame, math, random

def create_asteroid(surface, object_color, radius, position, velocity):
    asteroid = Asteroid(surface, position, object_color, velocity, radius)
    return(asteroid)

def within_bounds(main_menu):
    if main_menu.get_rect()[0] <= pygame.mouse.get_pos()[0] <= main_menu.get_rect()[1] and main_menu.get_rect()[2] <= pygame.mouse.get_pos()[1] <= main_menu.get_rect()[3]:
        return True
    return False

#This class specifies the creation of a scoreboard
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



#remove and make it a function
class GameOver:
    def __init__(self, surface):
        self.surface = surface
    def render(self):
        text_string1 = "GAME OVER"
        text_color = pygame.Color("white")
        text_font = pygame.font.SysFont('arial MT', 96)
        text_image = text_font.render(text_string1, True, text_color)
        text_pos1 = ((self.surface.get_width()//2) - (text_image.get_width()//2),(self.surface.get_height()//2) - (text_image.get_height()//2))
        self.surface.blit(text_image, text_pos1)

class MainMenu:
    def __init__(self, surface):
        self.surface = surface
    def render(self):
        text_string1 = "ASTEROIDS"
        text_color = pygame.Color('white')
        text_font = pygame.font.SysFont("arial MT", 106)
        text_image = text_font.render(text_string1, True, text_color)
        text_pos1 = ((self.surface.get_width()//2) - (text_image.get_width()//2),(self.surface.get_height()//2) - (text_image.get_height()//2) - 100)
        self.surface.blit(text_image, text_pos1)
        text_string2 = "Play Game"
        text_font = pygame.font.SysFont("arial MT", 70)
        text_image = text_font.render(text_string2, True, text_color)
        text_pos2 = ((self.surface.get_width()//2) - (text_image.get_width()//2),(self.surface.get_height()//2) - (text_image.get_height()//2))
        self.surface.blit(text_image, text_pos2)
        return text_image.get_rect()

    def get_rect(self):
        text_string2 = "Play Game"
        text_font = pygame.font.SysFont("arial MT", 70)
        text_color = pygame.Color('white')
        text_image = text_font.render(text_string2, True, text_color)
        text_pos2 = ((self.surface.get_width()//2) - (text_image.get_width()//2),(self.surface.get_height()//2) - (text_image.get_height()//2))
        return (text_pos2[0], text_pos2[0] + text_image.get_rect().width, text_pos2[1], text_pos2[1] + text_image.get_rect().height)

class Ship(pygame.sprite.Sprite):
        def __init__(self, surface, center, color, lives = 3):
            pygame.sprite.Sprite.__init__(self)
            self.surface = surface
            self.color = color
            self.lives = lives
            self.velocity = [0, 0]
            self.acceleration = [0, 0]
            self.length = [10, 7, 7, 10]
            self.angle = [90, 225, 315]
            self.center = center
            self.size = surface
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

        def velocity_correction(self):
            if self.velocity[0] > abs(math.cos(self.angle[0])):
                self.velocity[0] -= self.velocity[0]/20
            elif self.velocity[0] < -abs(math.cos(self.angle[0])):
                self.velocity[0] += -(self.velocity[0]/20)
            if self.velocity[1] > abs(math.sin(self.angle[0])):
                self.velocity[1] -= self.velocity[1]/20
            elif self.velocity[1] < -abs(math.sin(self.angle[0])):
                self.velocity[1] += -(self.velocity[1]/20)

        def velocity_move(self):
            self.velocity = [self.velocity[0] + self.acceleration[0], self.velocity[1] + self.acceleration[1]]

        def hyperspace(self):
            self.center = (random.randint(0,size[0]), random.randint(0,size[1]))

        def move(self):
            self.center = (self.center[0] + self.velocity[0], self.center[1] + self.velocity[1])
            self.polygon1 = (int(10 + self.length[0]*math.cos(math.pi*self.angle[0]/180)), int(10 - self.length[0]*math.sin(math.pi*self.angle[0]/180)))
            self.polygon2 = (int(10 + self.length[1]*math.cos(math.pi*self.angle[1]/180)), int(10 - self.length[1]*math.sin(math.pi*self.angle[1]/180)))
            self.polygon4 = (int(10 + self.length[2]*math.cos(math.pi*self.angle[2]/180)), int(10 - self.length[2]*math.sin(math.pi*self.angle[2]/180)))
            self.polygon = (self.polygon1, self.polygon2, (10,10), self.polygon4)

        def collision_bullet(self, bullet, scoreboard, ufo):
            offset_bullet = (int(self.center[0] - bullet.position[0]), int(self.center[1] - bullet.position[1]))
            overlap_bullet = self.mask.overlap(bullet.mask, offset_bullet)
            return ship_rebirth(overlap_bullet, self, scoreboard, ufo)

        def collision(self):
            if self.center[1] <= 0:
                self.center = (self.center[0], size[1] - 50)
            if self.center[0] <= 0:
                self.center = (size[0] - 50, self.center[1])
            if self.center[1] >= size[1]:
                self.center = (self.center[0], 0)
            if self.center[0] >= size[0]:
                self.center = (50, self.center[1])

        def shoot(self):
            return Bullet(self.surface, self.angle[0], (self.center[0] + self.polygon1[0], self.center[1] + self.polygon1[1]), self.color, 10)

        def add_life(self):
            self.lives += 1

        def rebirth(self, scoreboard):
            self.__init__(self.surface, (size[0]//2, size[1]//2), pygame.Color("white"), self.lives - 1)
            scoreboard.remove_life(self)
            print(self.lives)

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

class Asteroid(pygame.sprite.Sprite):
    ''' Asteroids movement and collision need to be completely rewritten so velocity is distrivuted non-evenly when broken up and smaller asteroids move faster than bigger asteroids'''
    def __init__(self, surface, position, color, velocity, radius):
        self.surface = surface
        self.position = position
        self.color = color
        self.velocity = velocity
        self.angle = (int(math.atan2(velocity[1], velocity[0]))/math.pi) * 180
        self.radius = radius
        self.width = 1

        pygame.sprite.Sprite.__init__(self)
        self.ASTEROID = pygame.Surface((self.radius*2,self.radius*2),pygame.SRCALPHA)
        pygame.draw.circle(self.ASTEROID, self.color, (self.radius, self.radius), self.radius, self.width)
        self.mask = pygame.mask.from_surface(self.ASTEROID)

    def draw(self):
        self.surface.blit(self.ASTEROID, self.position)

    def move(self):
        self.position = (self.position[0] + self.velocity[0],self.position[1] - self.velocity[1])

    def collision_ship(self, ship, scoreboard, ufo):
        offset_asteroid = (int(ship.center[0] - self.position[0]), int(ship.center[1] - self.position[1]))
        overlap_asteroid = self.mask.overlap(ship.mask, offset_asteroid)
        return ship_rebirth(overlap_asteroid, ship, scoreboard, ufo)

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
            temp.append(create_asteroid(self.surface, self.color, (2*self.radius)//3, self.calculate_position(bullet, direction = -1), self.calculate_velocity(bullet, True)))
            temp.append(create_asteroid(self.surface, self.color, (2*self.radius)//3, self.calculate_position(bullet), self.calculate_velocity(bullet, False)))
            return temp
        elif overlap_asteroid != None and self.radius < 15:
            return []

    def collision_UFO(self, ufo):
        offset_asteroid = (int(ufo.position[0] - self.position[0]), int(ufo.position[1] - self.position[1]))
        overlap_asteroid = self.mask.overlap(ufo.mask, offset_asteroid)
        if overlap_asteroid != None and self.radius > 15:
            temp = []
            temp.append(create_asteroid(self.surface, self.color, (2*self.radius)//3, self.calculate_position(ufo, direction = -1), self.calculate_velocity(ufo, True)))
            temp.append(create_asteroid(self.surface, self.color, (2*self.radius)//3, self.calculate_position(ufo), self.calculate_velocity(ufo, False)))
            return temp
        elif overlap_asteroid != None:
            return []

    def collision(self):
            if self.position[1] <= -30:
                self.position = (self.position[0], size[1] - 15)
            if self.position[0] <= -30:
                self.position = (size[0] - 15, self.position[1])
            if self.position[1] >= size[1] + 30:
                self.position = (self.position[0], -15)
            if self.position[0] >= size[0] + 30:
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

def double_range(size):
    a = []
    b = (random.randint(-50,1), random.randint(0,size[1]))
    c = (random.randint(size[0] + 1, size[0] + 50), random.randint(0,size[1]))
    d = (random.randint(0,size[0]), random.randint(-50,1))
    e = (random.randint(0,size[0]), random.randint(size[1] + 1,size[1] + 50))
    a.append(b)
    a.append(c)
    a.append(d)
    a.append(e)
    return random.choice(a)

def ship_rebirth(overlap, ship, scoreboard, ufo):
    if overlap != None and ship.lives == 0:
        ship.center = (1600,900)
        return True
    elif overlap != None and ship.lives != 0:
        ship.rebirth(scoreboard)
        for i in asteroid_list:
            if math.sqrt((i.position[0] - (size[0]//2)) ** 2 + (i.position[1] - (size[1]//2)) ** 2) < 100:
                i.position = double_range(size)
        if ufo != None and math.sqrt((ufo.position[0] - (size[0]//2)) ** 2 + (ufo.position[1] - (size[1]//2)) ** 2) < 100:
            ufo.position = double_range(size)
    return False



def main():
    pygame.init()
    global size
    size = (1600, 900)
    surface = pygame.display.set_mode(size)
    pygame.display.set_caption("Asteroids")
    width = size[0]
    height = size[1]
    scoreboard = Scoreboard(surface)
    bg_color = pygame.Color('black')
    game_clock = pygame.time.Clock()
    FPS = 120
    timer = 3000
    main_menu_display = True
    continue_game = True
    close_clicked = False
    bullet_exists = False
    bullet_list = []
    ufo_bullet_list = []
    global asteroid_list
    asteroid_list = []
    center = (width//2, height//2)
    object_color = pygame.Color('white')
    ship = Ship(surface, center, object_color)
    ufo = None
    game_over = GameOver(surface)
    main_menu = MainMenu(surface)

    while len(asteroid_list) < 6:
        asteroid_list.append(create_asteroid(surface, object_color, 30, double_range(size), (random.choice((-2,-1, -0.5, 0.5, 1, 2)), random.choice((-2,-1, -0.5, 0.5, 1, 2)))))

    if len(asteroid_list) < 10:
        pygame.time.set_timer(pygame.USEREVENT, timer)

    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
    pygame.time.set_timer(pygame.USEREVENT + 2, 10000)

    while not close_clicked:
        '''Handles Pygame events from keyboard and those that are automatically setup'''
        pygame.key.set_repeat(1)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                close_clicked = True
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                bullet_list.append(ship.shoot())
            if main_menu_display == False:
                if event.type == pygame.KEYUP and event.key == pygame.K_e:
                    ship.hyperspace()
                if event.type == pygame.USEREVENT:
                    asteroid_list.append(Asteroid(surface, double_range(size), pygame.Color("white"), (random.choice((-2,-1, -0.5, 0.5, 1, 2)), random.choice((-2,-1, -0.5, 0.5, 1, 2))), 30))
                if event.type == pygame.USEREVENT + 1 and ufo != None:
                    ufo_bullet_list.append(ufo.shoot())
                if event.type == pygame.USEREVENT + 2 and ufo == None:
                    ufo = UFO(surface, double_range(size), object_color, random.choice((random.randint(-2,-1), random.randint(1,2))))
            if main_menu_display and event.type == pygame.MOUSEBUTTONUP and within_bounds(main_menu):
                main_menu_display = False
        ''' End of handling pygame events '''

        ''' The start of the render portion of the main function '''
        surface.fill(bg_color)

        if main_menu_display:
            rectangle = main_menu.render()
            rect = pygame.Rect(main_menu.get_rect()[0], main_menu.get_rect()[2], rectangle.width, rectangle.height)
            if main_menu_display and main_menu.get_rect()[0] <= pygame.mouse.get_pos()[0] <= main_menu.get_rect()[1] and main_menu.get_rect()[2] <= pygame.mouse.get_pos()[1] <= main_menu.get_rect()[3]:
                pygame.draw.rect(surface, pygame.Color("white"), rect, width = 3)
        elif not main_menu_display:
            scoreboard.render()
            ship.draw()

            if ufo != None:
                ufo.draw()

            for i in bullet_list:
                i.draw()

            for i in ufo_bullet_list:
                i.draw()

            for i in asteroid_list:
                i.draw()

            if not continue_game:
                game_over.render()

        pygame.display.flip()

        ''' The end of the render portion of the main function'''

        if continue_game and main_menu_display == False:

            ship.move()
            ship.acceleration_correction()
            ship.velocity_move()
            ship.collision()
            if ufo != None:
                ufo.move()
                ufo.collision()
            for i in asteroid_list:
                i.collision()
                i.move()

            to_be_removed = []
            #Removes the ship's bullets that leave screen
            for i in bullet_list:
                if -100 < i.position[0] < size[0] + 100 and -100 < i.position[1] < size[1] + 100:
                    i.move()
                else:
                    to_be_removed.append(i)

            #Removes the ufo's bullets that leave the screen
            for i in ufo_bullet_list:
                if -100 < i.position[0] < size[0] + 100 and -100 < i.position[1] < size[1] + 100:
                    i.move()
                else:
                    to_be_removed.append(i)

            asteroid_to_be_removed = []
            #For every bullet checks if the bullet collides with the ufo or with every asteroid
            for i in bullet_list:
                if ufo != None and ufo.collision_bullet(i) != None:
                    ufo = None
                    scoreboard.increment(500, ship)
                for j in asteroid_list:
                    if j.collision_bullet(i) != None:
                        to_be_removed.append(i)
                        asteroid_to_be_removed.append(j)
                        asteroid_list = asteroid_list + j.collision_bullet(i)
                        scoreboard.increment(j.radius * 100, ship)



            #For every ufo bullet check if it hits the ship or if it hits an asteroid
            for i in ufo_bullet_list:
                a = ship.collision_bullet(i, scoreboard, ufo)
                if a:
                    continue_game = not a
                for j in asteroid_list:
                    if j.collision_bullet(i) != None:
                        to_be_removed.append(i)
                        asteroid_to_be_removed.append(j)
                        asteroid_list = asteroid_list + j.collision_bullet(i)

            #For every asteroid checks if it hit and asteroid or a bullet
            for i in asteroid_list:
                if ufo != None and i.collision_UFO(ufo) != None:
                    asteroid_to_be_removed.append(i)
                    asteroid_list = asteroid_list + i.collision_UFO(ufo)

            if ufo != None:
                bool = ufo.collision_ship(ship, scoreboard, ufo)
                if bool:
                    continue_game = False
                else:
                    continue_game = True

            for i in to_be_removed:
                if i in bullet_list:
                    bullet_list.remove(i)

            for i in asteroid_to_be_removed:
                if i in asteroid_list:
                    asteroid_list.remove(i)

            to_be_removed = []
            asteroid_to_be_removed = []

            if len(asteroid_list) >= 10 and timer == 3000:
                timer = 0
                pygame.time.set_timer(pygame.USEREVENT, timer)
            elif len(asteroid_list) < 10 and timer == 0:
                timer = 3000
                pygame.time.set_timer(pygame.USEREVENT, timer)

            for i in asteroid_list:
                c = i.collision_ship(ship, scoreboard, ufo)
                if c:
                    continue_game = not c

            if pygame.key.get_pressed()[119] == 1:
                ship.accelerate(0.03)
            if pygame.key.get_pressed()[97] == 1:
                ship.rotate(3)
                ship.mask_update()
            if pygame.key.get_pressed()[100] == 1:
                ship.rotate(-3)
                ship.mask_update()
        game_clock.tick(FPS)

main()
