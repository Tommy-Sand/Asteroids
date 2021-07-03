import pygame

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