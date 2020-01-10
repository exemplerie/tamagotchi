import pygame
import sys
import os

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    colorkey = image.get_at((0, 0))
    image.set_colorkey(colorkey)
    return image


def terminate():  # выход из программы
    pygame.quit()
    sys.exit()


tile_images = {'arrow_left': load_image('arrow_left.jpg'), 'arrow_right': load_image('arrow_right.jpg'),
               'display': load_image('имя дисплея'), 'kitchen': load_image('имя кухни'),
               'bathroom': load_image('имя ванной'), 'bedroom': load_image('имя спальни'),
               'hall': load_image('имя зала')}
player_image = {'one_level': load_image('первый возраст'), 'two_level': load_image('второй возраст'),
                'three_level': load_image('третий возраст')}