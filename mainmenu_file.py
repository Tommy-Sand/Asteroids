import pygame

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