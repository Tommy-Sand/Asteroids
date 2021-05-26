import pygame, math


#

def main():
    # initialize pygame -- this is required for rendering fonts
    pygame.init()
    
    # create the window and set its size to 500 width and 400 height
    size = (800, 800)
    surface = pygame.display.set_mode(size)
    
    # set the title of the window
    pygame.display.set_caption("Pong")
    
    game = Game(surface, size)
    game.play()

# This class is where the games classes are brought together and the game is created

class Game:

    # initializes instance attributes
    def __init__(self, game_surface, size):
        # --- attributes that are general to all games
        self.surface = game_surface
        self.bg_color = pygame.Color('black')
        self.game_clock = pygame.time.Clock()
        self.FPS = 30
        self.continue_game = True
        self.close_clicked = False
        self.size = size 
        self.bullet_exists = False
        self.bullet_list = []
        
        self.asteroid = Asteroid(self.surface, (200,200), pygame.Color('white'), 7, 300)
        #self.scoreboard = Scoreboard(self.surface, self.small_ball, self.size)
        
        self.ship = Ship(self.surface, (10, 10), pygame.Color('white'))
        
    #This method is where other methods are called so the game can run
    def play(self):
        # Play the game until the player presses the close box.
        while not self.close_clicked:
            self.handle_events()
            self.draw()
            if self.continue_game:
                self.update()
            self.game_clock.tick(self.FPS)
    #This method handles the exist condition 
    def handle_events(self):
        pygame.key.set_repeat(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.bullet_list.append(self.ship.shoot())
            
    #This method draws all the constituent parts of the game
    def draw(self):     
        self.surface.fill(self.bg_color)
        #self.scoreboard.render()
        # draw our dot to surface
        self.ship.draw()
        for i in self.bullet_list:
            i.draw()
        self.asteroid.draw()
        # render all drawn objects to the surface
        pygame.display.flip()
    #This method updates the surface 
    def update(self):
        # Update all of our game's objects
        #self.scoreboard.increment()
        #self.scoreboard.render()
        self.ship.move()
        self.ship.acceleration_correction()
        self.ship.velocity_move()
        self.ship.collision()
        self.asteroid.move()
        for i in self.bullet_list:
            i.move()

        if pygame.key.get_pressed()[119] == 1:
            self.ship.accelerate(0.5)
        if pygame.key.get_pressed()[97] == 1:
           self.ship.rotate(5)
        if pygame.key.get_pressed()[100] == 1:
            self.ship.rotate(-5)
        
     
#This class specifies the creation of a scoreboard
class Scoreboard:
    
    def __init__(self, surface, ball, size):
        self.surface = surface
        self.ball = ball
        self.size = size
        self.leftscore = 0
        self.rightscore = 0
    #This method increments the scoreboard by one
    def increment(self):
        if self.ball.center[0] - self.ball.radius <= 0:
            self.rightscore += 1
            print("Rightscore" , self.rightscore)
        if self.ball.center[0] + self.ball.radius >= 500:
            self.leftscore += 1
            print("Leftscore", self.leftscore)
    #This method renders the scoreboard on the surface
    def render(self):
        text_string1 = str(self.leftscore)
        text_color = pygame.Color('white')
        text_font = pygame.font.SysFont('Times New Roman', 48)
        text_image = text_font.render(text_string1, True, text_color)
        text_pos1 = (0, 0)
        self.surface.blit(text_image, text_pos1)
        text_string2 = str(self.rightscore)
        text_font = pygame.font.SysFont('Times New Roman', 48)
        text_image = text_font.render(text_string2, True, text_color)
        text_pos2 = (450, 0)
        self.surface.blit(text_image, text_pos2)


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

            # self.polygon1 = (self.center[0] + self.length[0]*math.cos(math.pi*self.angle[0]/180), self.center[1] - self.length[0]*math.sin(math.pi*self.angle[0]/180))
            # self.polygon2 = (self.center[0] + self.length[1]*math.cos(math.pi*self.angle[1]/180), self.center[1] - self.length[1]*math.sin(math.pi*self.angle[1]/180))
            # self.polygon4 = (self.center[0] + self.length[2]*math.cos(math.pi*self.angle[2]/180), self.center[1] - self.length[2]*math.sin(math.pi*self.angle[2]/180))
            # self.polygon = (self.polygon1, self.polygon2, self.center, self.polygon4)

            self.polygon1 = (10 + self.length[0]*math.cos(math.pi*self.angle[0]/180), 10 - self.length[0]*math.sin(math.pi*self.angle[0]/180))
            self.polygon2 = (10 + self.length[1]*math.cos(math.pi*self.angle[1]/180), 10 - self.length[1]*math.sin(math.pi*self.angle[1]/180))
            self.polygon4 = (10 + self.length[2]*math.cos(math.pi*self.angle[2]/180), 10 - self.length[2]*math.sin(math.pi*self.angle[2]/180))
            self.polygon = (self.polygon1, self.polygon2, (10,10), self.polygon4)

            self.SHIP = pygame.Surface((30,30), pygame.SRCALPHA)
            pygame.draw.polygon(self.SHIP, self.color, self.polygon)
            self.mask = pygame.mask.from_surface(self.SHIP)


        def rotate(self, angle):
            for i in range(0, 3):
                self.angle[i] += angle
            self.mask_update()

        def mask_update(self):
            self.SHIP.fill(pygame.Color("black"))
            pygame.draw.polygon(self.SHIP,self.color, self.polygon)
            self.mask = pygame.mask.from_surface(self.SHIP)

        def draw(self):
            
            self.surface.blit(self.SHIP,(int(self.center[0]), int(self.center[1])))
            
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
            if round(self.acceleration[0],4) or round(self.acceleration[1],4):
                self.velocity_correction()
            
        def velocity_correction(self):
            if self.velocity[0] > 0:
                self.velocity[0] -= self.velocity[0]/5
            elif self.velocity[0] < 0:
                self.velocity[0] += -(self.velocity[0]/5)
            if self.velocity[1] > 0:
                self.velocity[1] -= self.velocity[1]/5
            elif self.velocity[1] < 0:
                self.velocity[1] += -(self.velocity[1]/5)

        def velocity_move(self):
            self.velocity = [self.velocity[0] + self.acceleration[0], self.velocity[1] + self.acceleration[1]]

        def move(self):
            self.center = (self.center[0] + self.velocity[0], self.center[1] + self.velocity[1])
            self.polygon1 = (10 + self.length[0]*math.cos(math.pi*self.angle[0]/180), 10 - self.length[0]*math.sin(math.pi*self.angle[0]/180))
            self.polygon2 = (10 + self.length[1]*math.cos(math.pi*self.angle[1]/180), 10 - self.length[1]*math.sin(math.pi*self.angle[1]/180))
            self.polygon4 = (10 + self.length[2]*math.cos(math.pi*self.angle[2]/180), 10 - self.length[2]*math.sin(math.pi*self.angle[2]/180))
            self.polygon = (self.polygon1, self.polygon2, (10,10), self.polygon4)
    
        def collision(self):
            if self.center[1] <= 0:
                self.center = (self.center[0], 750)
            if self.center[0] <= 0:
                self.center = (750, self.center[1])
            if self.center[1] >= 800:
                self.center = (self.center[0], 0)
            if self.center[0] >= 800:
                self.center = (50, self.center[1])

        def shoot(self):
            return Bullet(self.surface, self.angle[0], (self.center[0] + self.polygon1[0], self.center[1] + self.polygon1[1]), self.color, 5)


class Bullet:
    def __init__(self, surface, angle, position, color, length):
        self.surface = surface
        self.angle = angle
        self.start_point = position
        self.color = color
        self.length = length
        self.velocity = 15
        self.end_point = (self.start_point[0] + (self.length * math.cos(math.pi * (self.angle/180))), self.start_point[1] - (self.length * math.sin(math.pi * (self.angle/180))))

    def draw(self):
        pygame.draw.line(self.surface, self.color, self.start_point, self.end_point)

    def move(self):
        self.start_point = (self.start_point[0] + (self.velocity * math.cos(math.pi * (self.angle/180))), self.start_point[1] - (self.velocity * math.sin(math.pi * (self.angle/180))))
        self.end_point = (self.end_point[0] + (self.velocity * math.cos(math.pi * (self.angle/180))), self.end_point[1] - (self.velocity * math.sin(math.pi * (self.angle/180))))
   
    
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, surface, position, color, velocity, angle):
        self.surface = surface
        self.position = position
        self.color = color
        self.velocity = velocity
        self.angle = angle

        pygame.sprite.Sprite.__init__(self)
        self.ASTEROID = pygame.Surface((60,60),pygame.SRCALPHA)
        pygame.draw.circle(self.ASTEROID, self.color, (30,30), 30, 2)
        self.mask = pygame.mask.from_surface(self.ASTEROID)

    def draw(self):
        pygame.draw.circle(self.surface, self.color, self.position, 30, 2)

    def move(self):
        self.position = (self.position[0] + (self.velocity * math.cos(math.pi * (self.angle/180))),self.position[1] + (self.velocity * math.cos(math.pi * (self.angle/180))))
    
    def collision_ship(self, ship):
        pass
        
main()