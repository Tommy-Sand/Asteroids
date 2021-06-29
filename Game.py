import pygame, math, random

#This class specifies the creation of a scoreboard
class Scoreboard:
    def __init__(self, surface):
        self.surface = surface
        self.score = 0
    #This method increments the scoreboard by one
    def increment(self, asteroid):
        self.score += asteroid.radius * 100
    #This method renders the scoreboard on the surface
    def render(self):
        text_string1 = str(self.score)
        text_color = pygame.Color('white')
        text_font = pygame.font.SysFont('Arial MT', 48)
        text_image = text_font.render(text_string1, True, text_color)
        text_pos1 = (0, 0)
        self.surface.blit(text_image, text_pos1)

#remove and make it a function
class GameOver:
    def __init__(self, surface):
        self.surface = surface
    def render(self):
        text_string1 = "GAME OVER"
        text_color = pygame.Color("white")
        text_font = pygame.font.SysFont('arial MT', 96)
        text_image = text_font.render(text_string1, True, text_color)
        text_pos1 = (250,250)
        self.surface.blit(text_image, text_pos1)

class MainMenu:
    def __init__(self, surface):
        self.surface = surface 
    def render(self):
        text_string1 = "ASTEROIDS"
        text_color = pygame.Color('white')
        text_font = pygame.font.SysFont("arial MT", 106)
        text_image = text_font.render(text_string1, True, text_color)
        text_pos1 = (200,200)
        self.surface.blit(text_image, text_pos1)
        text_string2 = "Play Game"
        text_font = pygame.font.SysFont("arial MT", 70)
        text_image = text_font.render(text_string2, True, text_color)
        text_pos2 = (250,400)
        self.surface.blit(text_image, text_pos2)
        return text_image.get_rect()
    def get_rect(self):
        text_string2 = "Play Game"
        text_font = pygame.font.SysFont("arial MT", 70)
        text_color = pygame.Color('white')
        text_image = text_font.render(text_string2, True, text_color)
        return text_image.get_rect()

class Ship(pygame.sprite.Sprite):
        def __init__(self, surface, center, color):
            pygame.sprite.Sprite.__init__(self)

            self.surface = surface
            self.color = color
            self.velocity = [0, 0]
            self.acceleration = [0, 0]
            self.length = [10, 7, 7]
            self.angle = [90, 225, 315]
            self.center = center
            self.size = surface

            self.polygon1 = (int(10 + self.length[0]*math.cos(math.pi*self.angle[0]/180)), int(10 - self.length[0]*math.sin(math.pi*self.angle[0]/180)))
            self.polygon2 = (int(10 + self.length[1]*math.cos(math.pi*self.angle[1]/180)), int(10 - self.length[1]*math.sin(math.pi*self.angle[1]/180)))
            self.polygon4 = (int(10 + self.length[2]*math.cos(math.pi*self.angle[2]/180)), int(10 - self.length[2]*math.sin(math.pi*self.angle[2]/180)))
            self.polygon = (self.polygon1, self.polygon2, (10,10), self.polygon4)
            self.SHIP = pygame.Surface((30,30), pygame.SRCALPHA)
            pygame.draw.polygon(self.SHIP, self.color, self.polygon)
            self.mask = pygame.mask.from_surface(self.SHIP)

            #self.image = pygame.image.load("ship.jpg")

        def rotate(self, angle):
            for i in range(0, 3):
                self.angle[i] += angle
            self.mask_update()

        def mask_update(self):
            self.SHIP = pygame.Surface((30,30), pygame.SRCALPHA)
            self.mask.clear()
            pygame.draw.polygon(self.SHIP,self.color, self.polygon)
            self.mask = pygame.mask.from_surface(self.SHIP)

        def draw(self):
            self.surface.blit(self.SHIP,(int(self.center[0]), int(self.center[1])))
            #self.surface.blit(self.image,(0,0))
            
        def accelerate(self, acceleration):
            self.acceleration = [self.acceleration[0] + acceleration*math.cos(math.pi*(self.angle[0]/180)), self.acceleration[1] - acceleration*math.sin(math.pi*(self.angle[0]/180))]
            
        def acceleration_correction(self):
            if self.acceleration[0] > 0:
                self.acceleration[0] -= self.acceleration[0]/5
            elif self.acceleration[0] < 0:
                self.acceleration[0] += -(self.acceleration[0]/5)
            if self.acceleration[1] > 0:
                self.acceleration[1] -= self.acceleration[1]/5
            elif self.acceleration[1] < 0:
                self.acceleration[1] += -(self.acceleration[1]/5)
            self.velocity_correction()
            
        def velocity_correction(self):
            if self.velocity[0] > 0:
                self.velocity[0] -= self.velocity[0]/20
            elif self.velocity[0] < 0:
                self.velocity[0] += -(self.velocity[0]/20)
            if self.velocity[1] > 0:
                self.velocity[1] -= self.velocity[1]/20
            elif self.velocity[1] < 0:
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
            
        def collision_bullet(self, bullet):
            offset_asteroid = (int(self.center[0] - bullet.start_point[0]), int(self.center[1] - bullet.start_point[1]))
            overlap_asteroid = self.mask.overlap(bullet.mask, offset_asteroid)
            if overlap_asteroid != None:
                self.center = (1600,900)
                return True
            return False

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

class Bullet(pygame.sprite.Sprite):
    def __init__(self, surface, angle, position, color, length):
        pygame.sprite.Sprite.__init__(self)

        self.surface = surface
        self.angle = angle
        self.start_point = position
        self.color = color
        self.length = length
        self.velocity = 15
        self.end_point = (20 + (self.length * math.cos(math.pi * (self.angle/180))), 20 - (self.length * math.sin(math.pi * (self.angle/180))))

        self.BULLET = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.line(self.BULLET, self.color, (20, 20), self.end_point)
        self.mask = pygame.mask.from_surface(self.BULLET)

    def draw(self):
        self.surface.blit(self.BULLET, (self.start_point[0] - 20, self.start_point[1] - 20))
        #self.bulletrect = self.BULLET.get_rect(center = self.start_point)
        #pygame.draw.rect(self.surface, pygame.Color('white'), self.bulletrect, width = 2)

    def move(self):
        self.start_point = (self.start_point[0] + (self.velocity * math.cos(math.pi * (self.angle/180))), self.start_point[1] - (self.velocity * math.sin(math.pi * (self.angle/180))))
        self.end_point = ((self.velocity * math.cos(math.pi * (self.angle/180))), -(self.velocity * math.sin(math.pi * (self.angle/180))))
     
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, surface, position, color, velocity, radius):
        self.surface = surface
        self.position = position
        self.color = color
        self.velocity = velocity
        self.angle = self.angle = (int(math.atan2(velocity[1], velocity[0]))/math.pi) * 180
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

    def collision_ship(self, ship):
        self.rect = self.ASTEROID.get_rect()
        self.ship_rect = ship.SHIP.get_rect()
        if self.radius == 30:
            offset_asteroid = (int(self.position[0] - ship.center[0] + self.radius + (self.radius/3)), int(self.position[1] - ship.center[1] + self.radius + (self.radius/3)))
        else:
            offset_asteroid = (int(self.position[0] - ship.center[0] + self.radius), int(self.position[1] - ship.center[1] + self.radius))
        overlap_asteroid = self.mask.overlap(ship.mask, offset_asteroid)
        if overlap_asteroid != None:
            ship.center = (1600,900)
            return True
        return False


    def collision_bullet(self, bullet):
        if self.radius == 30:
            offset_asteroid = (int(self.position[0] - bullet.start_point[0] + self.radius + (self.radius/3)), int(self.position[1] - bullet.start_point[1] + self.radius + (self.radius/3)))
        else:
            offset_asteroid = (int(self.position[0] - bullet.start_point[0] + self.radius), int(self.position[1] - bullet.start_point[1] + self.radius))
        overlap_asteroid = self.mask.overlap(bullet.mask, offset_asteroid)
        if overlap_asteroid != None and self.radius > 15:
            asteroid1 = Asteroid(self.surface, (self.position[0] + 10*math.cos(math.pi * (bullet.angle - 90)/180), self.position[1] - 10*math.sin(math.pi * (bullet.angle - 90)/180)), self.color, self.calculate_velocity(bullet, True), self.radius//2)
            asteroid2 = Asteroid(self.surface, (self.position[0] + 10*math.cos(math.pi * (bullet.angle + 90)/180), self.position[1] - 10*math.sin(math.pi * (bullet.angle + 90)/180)), self.color, self.calculate_velocity(bullet, False), self.radius//2)
            return [asteroid1, asteroid2]
        elif overlap_asteroid != None and self.radius == 15:
            asteroid1 = Asteroid(self.surface, (self.position[0] + 10*math.cos(math.pi * (bullet.angle - 90)/180), self.position[1] - 10*math.sin(math.pi * (bullet.angle - 90)/180)), self.color, self.calculate_velocity(bullet, True), 10)
            asteroid2 = Asteroid(self.surface, (self.position[0] + 10*math.cos(math.pi * (bullet.angle + 90)/180), self.position[1] - 10*math.sin(math.pi * (bullet.angle + 90)/180)), self.color, self.calculate_velocity(bullet, False), 10)
            return [asteroid1, asteroid2]
        elif overlap_asteroid != None and self.radius < 15:
            return []

    def collision_UFO(self, ufo):
        offset_asteroid = (int(self.position[0] - ufo.position[0] + 10), int(self.position[1] - ufo.position[1]))
        overlap_asteroid = self.mask.overlap(ufo.mask, offset_asteroid)
        if overlap_asteroid != None and self.radius > 15:
            asteroid1 = Asteroid(self.surface, (self.position[0] + 10*math.cos(math.pi * (ufo.angle - 90)/180), self.position[1] - 10*math.sin(math.pi * (ufo.angle - 90)/180)), self.color, self.calculate_velocity(ufo, True), self.radius//2)
            asteroid2 = Asteroid(self.surface, (self.position[0] + 10*math.cos(math.pi * (ufo.angle + 90)/180), self.position[1] - 10*math.sin(math.pi * (ufo.angle + 90)/180)), self.color, self.calculate_velocity(ufo, False), self.radius//2)
            return [asteroid1, asteroid2]
        elif overlap_asteroid != None and self.radius == 15:
            return []

    def collision(self):
            if self.position[1] <= -50:
                self.position = (self.position[0], size[1] - 50)
            if self.position[0] <= -50:
                self.position = (size[0] - 50, self.position[1])
            if self.position[1] >= size[1] + 50:
                self.position = (self.position[0], 0)
            if self.position[0] >= size[0] + 50:
                self.position = (50, self.position[1])
    
    def calculate_velocity(self, bullet, ninety):
        total_velocity = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        if ninety:
            angle = bullet.angle - 90
        elif not ninety:
            angle = bullet.angle + 90
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
        self.angle = (int(math.atan2(velocity[1], velocity[0]))/math.pi) * 180
        self.UFO = pygame.Surface((50,50), pygame.SRCALPHA)
        self.ellipsce_rect = pygame.Rect(0, 25, 50, 25)
        self.arc_rect = pygame.Rect(13,12,25,25)
        pygame.draw.ellipse(self.UFO, self.color, self.ellipsce_rect, width = 3)
        pygame.draw.arc(self.UFO, self.color, self.arc_rect, math.pi * (-10/180), math.pi * (190/180), width = 3)
        self.mask = pygame.mask.from_surface(self.UFO)

    def draw(self):
        self.surface.blit(self.UFO, self.position)

    def move(self):
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])


    def collision_ship(self, ship):
        self.rect = self.UFO.get_rect()
        self.ship_rect = ship.SHIP.get_rect()
        offset_asteroid = (int(self.position[0] - ship.center[0] + (self.UFO.get_rect().right//2)), int(self.position[1] - ship.center[1] + (self.UFO.get_rect().bottom)))
        overlap_asteroid = self.mask.overlap(ship.mask, offset_asteroid)
        if overlap_asteroid != None:
            ship.center = (1600,900)
            return True
        return False

    def collision_bullet(self, bullet):
        offset_asteroid = (int(self.position[0] - bullet.start_point[0] + (self.UFO.get_rect().right//2)), int(self.position[1] - bullet.start_point[1] + (self.UFO.get_rect().bottom)))
        overlap_asteroid = self.mask.overlap(bullet.mask, offset_asteroid)
        if overlap_asteroid != None:
            return overlap_asteroid

    def collision(self):
            if self.position[1] <= -50:
                self.position = (self.position[0], size[1] - 50)
            if self.position[0] <= -50:
                self.position = (size[0] - 50, self.position[1])
            if self.position[1] >= size[1] + 50:
                self.position = (self.position[0], 0)
            if self.position[0] >= size[0] + 50:
                self.position = (50, self.position[1])

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

def main():
    pygame.init()
    global size
    size = (800, 800)
    surface = pygame.display.set_mode(size)
    pygame.display.set_caption("Asteroids")
    width = surface.get_rect().bottom
    height = surface.get_rect().right
    scoreboard = Scoreboard(surface)
    bg_color = pygame.Color('black')
    game_clock = pygame.time.Clock()
    FPS = 60
    timer = 3000
    main_menu_display = True
    continue_game = True
    close_clicked = False
    size = size 
    bullet_exists = False
    bullet_list = []
    ufo_bullet_list = []
    asteroid_list = []
    center = (width//2, height//2)
    object_color = pygame.Color('white')
    ship = Ship(surface, center, object_color)
    ufo = None
    game_over = GameOver(surface)
    main_menu = MainMenu(surface)

    while len(asteroid_list) < 6:
        asteroid = Asteroid(surface, double_range(size), object_color, (random.randint(-2,2), random.randint(-2,2)), 30)
        asteroid_list.append(asteroid)

    if len(asteroid_list) < 10:
        pygame.time.set_timer(pygame.USEREVENT, timer)

    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
    pygame.time.set_timer(pygame.USEREVENT + 2, 10000)

    while not close_clicked:
        pygame.key.set_repeat(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_clicked = True
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                bullet_list.append(ship.shoot())
            if main_menu_display == False and event.type == pygame.KEYUP and event.key == pygame.K_e:
                ship.hyperspace()
            if main_menu_display == False and event.type == pygame.USEREVENT:
                asteroid_list.append(Asteroid(surface, double_range(size), pygame.Color("white"), (random.randint(-2,2), random.randint(-2,2)), 30))
            if main_menu_display == False and event.type == pygame.USEREVENT + 1 and ufo != None:
                ufo_bullet_list.append(ufo.shoot())
            if main_menu_display == False and event.type == pygame.USEREVENT + 2 and ufo == None:
                ufo = UFO(surface, double_range(size), object_color, (random.randint(-2,2), random.randint(-2,2)))
            if main_menu_display and 250 <= pygame.mouse.get_pos()[0] <= 250 + main_menu.get_rect().right and 400 <= pygame.mouse.get_pos()[1] <= 400 + main_menu.get_rect().bottom and event.type == pygame.MOUSEBUTTONUP:
                main_menu_display = False
        
        
        surface.fill(bg_color)

        if main_menu_display:
            rectangle = main_menu.render()
            rectangle.topleft = (250, 400)
            if main_menu_display and 250 <= pygame.mouse.get_pos()[0] <= 250 + main_menu.get_rect().right and 400 <= pygame.mouse.get_pos()[1] <= 400 + main_menu.get_rect().bottom:
                pygame.draw.rect(surface, pygame.Color("white"), rectangle, width = 3)

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

            for i in bullet_list:
                for j in asteroid_list:
                    if j.collision_bullet(i) != None:
                        to_be_removed.append(i)
                        asteroid_to_be_removed.append(j)
                        asteroid_list = asteroid_list + j.collision_bullet(i)
                        scoreboard.increment(j)

            if not continue_game:
                game_over.render()

        pygame.display.flip()


        if continue_game:
            if main_menu_display == False:
                scoreboard.render()
                ship.move()
                ship.acceleration_correction()
                ship.velocity_move()
                ship.collision()
                if ufo != None:
                    ufo.move()
                    ufo.collision_ship(ship)
                    ufo.collision()
                for i in asteroid_list:
                    i.collision()
                    i.move()

                to_be_removed = []
                #Removes the ship's bullets that leave screen
                for i in bullet_list:
                    if -100 < i.start_point[0] < size[0] + 100 and -100 < i.start_point[1] < size[1] + 100:
                        i.move()
                    else:
                        to_be_removed.append(i)

                #Removes the ufo's bullets that leave the screen
                for i in ufo_bullet_list:
                    if -100 < i.start_point[0] < size[0] + 100 and -100 < i.start_point[1] < size[1] + 100:
                        i.move()
                    else:
                        to_be_removed.append(i)

                asteroid_to_be_removed = []
                #For every bullet checks if the bullet collides with the ufo or with every asteroid
                for i in bullet_list:
                    if ufo != None and ufo.collision_bullet(i) != None:
                        ufo = None
                        scoreboard.score += 500
                    for j in asteroid_list:
                        if j.collision_bullet(i) != None:
                            to_be_removed.append(i)
                            asteroid_to_be_removed.append(j)
                            asteroid_list = asteroid_list + j.collision_bullet(i)
                            scoreboard.increment(j)

                #For every ufo bullet check if it hits the ship or if it hits an asteroid 
                for i in ufo_bullet_list:
                    a = ship.collision_bullet(i)
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
                    bool = ufo.collision_ship(ship)
                if ufo != None and bool:
                    continue_game = not ufo.collision_ship(ship)

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
                    c = i.collision_ship(ship)
                    if c:
                        continue_game = not c

                if pygame.key.get_pressed()[119] == 1:
                    ship.accelerate(0.15)
                if pygame.key.get_pressed()[97] == 1:
                    ship.rotate(6)
                    ship.mask_update()
                if pygame.key.get_pressed()[100] == 1:
                    ship.rotate(-6)
                    ship.mask_update()
        game_clock.tick(FPS)
main()