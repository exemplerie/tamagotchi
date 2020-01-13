import pygame
import sys
import os

# я обрезала картинки и добавиа временный цикл, чтоб проверить работают ли классы
# вроде пока все нормально и комнаты даже перелистываются, но спрайты как-то странны обрезаются
# я не добавила кнопку снизу экрана и не трогала спрайт яйца(display который), мне кажется фон лучше сразу весь рисовать

pygame.init()
size = width, height = 455, 565
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()


def load_image(name, colorkey=None):  # загрузка изображения
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():  # выход из программы
    pygame.quit()
    sys.exit()


tile_images = {'arrow_left': load_image('arrow_left.jpg'), 'arrow_right': load_image('arrow_right.jpg'),
               'display': load_image('display.png')}
fon_images = {'kitchen': load_image('kitchen.png'),
              'bathroom': load_image('bathroom.png'), 'bedroom': load_image('bedroom.jpg'),
              'hall': load_image('hall.png'), 'gameroom': load_image('gameroom.png')}
player_image = {'one_level': load_image('baby.jpg'), 'two_level': load_image('baby_2.jpg'),
                'three_level': load_image('baby_2.jpg')}
#  порядок комнат: игровая, спальня, холл, кухня, ванная
rooms = ['gameroom', 'bedroom', 'hall', 'kitchen', 'bathroom']
room = 'hall'
age = 'one_level'

# группы спрайтов
player_group = pygame.sprite.Group()
fon_group = pygame.sprite.Group()
right_button_group = pygame.sprite.Group()
left_button_group = pygame.sprite.Group()


class Fon(pygame.sprite.Sprite):
    def __init__(self, fon_type):
        super().__init__(fon_group)
        self.image = fon_images[fon_type]
        self.rect = self.image.get_rect().move(0, 190)
        self.add(fon_group)


class Player(pygame.sprite.Sprite):
    def __init__(self, age):
        super().__init__(player_group)
        self.image = player_image[age]
        self.rect = self.image.get_rect().move(180, 300)
        self.add(player_group)


class LeftButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(left_button_group)
        self.image = tile_images['arrow_left']
        self.rect = self.image.get_rect().move(40, 500)
        self.add(left_button_group)


class RightButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(right_button_group)
        self.image = tile_images['arrow_right']
        self.rect = self.image.get_rect().move(365, 500)
        self.add(right_button_group)


def draw(room, age):
    RightButton()
    LeftButton()
    Player(age)
    Fon(room)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for sprite in right_button_group:
                if sprite.rect.collidepoint(event.pos):
                    room = rooms[(rooms.index(room) + 1) % len(rooms)]
            for sprite in left_button_group:
                if sprite.rect.collidepoint(event.pos):
                    room = rooms[(rooms.index(room) - 1) % len(rooms)]
    player_group.empty()
    left_button_group.empty()
    right_button_group.empty()
    fon_group.empty()
    draw(room, age)

    screen.fill((0, 0, 0))
    fon_group.draw(screen)
    left_button_group.draw(screen)
    right_button_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
terminate()
