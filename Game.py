import pygame, math, random
import asteroids_file
import gameover_file, scoreboard_file, mainmenu_file, ship_file, ufo_file

def create_asteroid(surface, scale, position, velocity):
    image_name = random.choice(["image/1.png", "image/2.png", "image/3.png"])
    asteroid = asteroids_file.Asteroid(surface, position, image_name, velocity, scale, size)
    return(asteroid)

def within_bounds(main_menu):
    if main_menu.get_rect()[0] <= pygame.mouse.get_pos()[0] <= main_menu.get_rect()[1] and main_menu.get_rect()[2] <= pygame.mouse.get_pos()[1] <= main_menu.get_rect()[3]:
        return True
    return False

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
    if overlap!= None and ship.lives == 0:
        ship.center = (1600,900)
        return True
    elif overlap!= None and ship.lives != 0:
        ship.rebirth(scoreboard)
        for i in asteroid_list:
            if math.sqrt((i.position[0] - (size[0]//2)) ** 2 + (i.position[1] - (size[1]//2)) ** 2) < 100:
                i.position = double_range(size)
        if ufo != None and math.sqrt((ufo.position[0] - (size[0]//2)) ** 2 + (ufo.position[1] - (size[1]//2)) ** 2) < 100:
            ufo.position = double_range(size)
    return False

def main():
    #Initialization section
    pygame.init()
    global size
    size = (1600, 900)
    surface = pygame.display.set_mode(size)
    pygame.display.set_caption("Asteroids")
    width = size[0]
    height = size[1]
    scoreboard = scoreboard_file.Scoreboard(surface)
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
    ship = ship_file.Ship(surface, center, object_color, size)
    ufo = None
    game_over = gameover_file.GameOver(surface)
    main_menu = mainmenu_file.MainMenu(surface)

    while len(asteroid_list) < 6:
        asteroid_list.append(create_asteroid(surface, 1, double_range(size), (random.choice((-2,-1, -0.5, 0.5, 1, 2)), random.choice((-2,-1, -0.5, 0.5, 1, 2)))))

    if len(asteroid_list) < 10:
        pygame.time.set_timer(pygame.USEREVENT, timer)

    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
    pygame.time.set_timer(pygame.USEREVENT + 2, 10000)
    #End of initialization section
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
                    asteroid_list.append(create_asteroid(surface, 1, double_range(size), (random.choice((-2,-1, -0.5, 0.5, 1, 2)), random.choice((-2,-1, -0.5, 0.5, 1, 2)))))
                if event.type == pygame.USEREVENT + 1 and ufo != None:
                    ufo_bullet_list.append(ufo.shoot())
                if event.type == pygame.USEREVENT + 2 and ufo == None:
                    choice = random.randint(0,1) 
                    if (choice == 1):
                        ufo = ufo_file.UFO(surface, double_range(size), object_color, random.choice((random.randint(-2,-1), random.randint(1,2))), size)
                    else:
                        ufo = ufo_file.small_UFO(surface, double_range(size), object_color, random.choice((random.randint(-2,-1), random.randint(1,2))), size)
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
                    if type(ufo) is ufo_file.UFO:
                        scoreboard.increment(500,ship)
                    else:
                        scoreboard.increment(1000, ship)
                for j in asteroid_list:
                    if j.collision_bullet(i) != None:
                        to_be_removed.append(i)
                        asteroid_to_be_removed.append(j)
                        asteroid_list = asteroid_list + j.collision_bullet(i)
                        scoreboard.increment(int((1/j.scale) * 300), ship)



            #For every ufo bullet check if it hits the ship or if it hits an asteroid
            for i in ufo_bullet_list:
                a = ship_rebirth(ship.collision_bullet(i), ship, scoreboard, ufo)
                if a:  
                    continue_game = False
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
                a = ship_rebirth(ufo.collision_ship(ship), ship, scoreboard, ufo)
                if a:
                    continue_game = False

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
                end_game = ship_rebirth(i.collision_ship(ship), ship, scoreboard, ufo)
                if end_game:
                    continue_game = not end_game

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
