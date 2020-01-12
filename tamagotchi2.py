import pygame
import sys
import os

# Привела в порядок код, кое-где поменяла названия и разграничила классы с функциями и сам цикл игры.
# Если вам такой вариант покажется удобным, оставим, если нет, то говорите сразу, поменяем
# + сделала нормальную вроде обработку пнг и поменяла стрелочки (они потом будут подходить к желтку,
# когда перекрасим его). Зациклила комнаты, ввела общий класс для кнопок, но функционал в принципе тот же.

SIZE = WIDTH, HEIGHT = 455, 565
FPS = 60
LEVELS = ['Baby', 'Teen', 'Adult', 'Elder']  # пока не знаю, пригодятся ли, но можно выводить как названия


class Display(pygame.sprite.Sprite):  # дисплей (яйцо)
    def __init__(self):
        super().__init__(dis, all_sprites)
        self.image = system_details_images['display']
        self.rect = self.image.get_rect().move(0, 0)


class Buttons(pygame.sprite.Sprite):  # все кнопки (для каждой - отдельный экземпляр)
    def __init__(self, detail, side):
        super().__init__(buttons_group, all_sprites)
        self.image = system_details_images[detail]
        if side == 'right':
            self.rect = self.image.get_rect().move(260, 450)
        elif side == 'left':
            self.rect = self.image.get_rect().move(100, 450)


class Room(pygame.sprite.Sprite):  # комнаты пусть пока останутся так, пока не ввели интерактива
    def __init__(self, room_type):
        super().__init__(room_group, all_sprites)
        self.image = room_images[room_type]
        self.rect = self.image.get_rect().move(0, 190)


class Player(pygame.sprite.Sprite):
    def __init__(self, what_age):
        super().__init__(player_group, all_sprites)
        self.image = player_image[what_age]
        self.rect = self.image.get_rect().move(180, 300)


def load_image(name, colorkey=None):  # загрузка изображения
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def click_processing(btn):  # вынесла обработку нажатий в отдельную функцию сейчас, т.к. все равно
    # потом будет больше функционала и действий с нажатием (чтобы сам цикл не захламлять)
    global now_room
    if btn == right_btn:
        now_room = (now_room + 1) % len(rooms)
    if btn == left_btn:
        now_room = (now_room - 1) % len(rooms)


def generate_state():  # по сути генерирует актуальное состояние игры - нужную комнату и игрока в нужном возрасте
    # т.е. обновляет их статус, в зависимости от действий (переключения комнат, прибавления возраста)
    room_group.empty()
    Room(rooms[now_room])
    Player(age)


def terminate():  # выход из программы
    pygame.quit()
    sys.exit()


pygame.init()

screen = pygame.display.set_mode(SIZE)

system_details_images = {'arrow_left': load_image('arrow_left.png', -1),
                         'arrow_right': load_image('arrow_right.png', -1),
                         'display': load_image('display.png', -1)}
# назвала системными деталями, тут все что вне маленького экранчика игры
room_images = {'kitchen': load_image('kitchen.png'),
               'bathroom': load_image('bathroom.png'), 'bedroom': load_image('bedroom.jpg'),
               'hall': load_image('hall.png'), 'gameroom': load_image('gameroom.png')}
player_image = {0: load_image('baby.jpg'), 1: load_image('baby_2.jpg'),
                2: load_image('baby_2.jpg')}

rooms = ['gameroom', 'bedroom', 'hall', 'kitchen', 'bathroom']
now_room = 2  # удобнее запоминать номер комнаты и возраст, чтобы изменять число, а не позицию в словаре
age = 0

player_group = pygame.sprite.Group()
buttons_group = pygame.sprite.Group()
room_group = pygame.sprite.Group()
dis = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

Room(rooms[now_room])
Player(age)
right_btn = Buttons('arrow_right', 'right')  # в функции потом очень удобно проверять, какая кнопка нажата
left_btn = Buttons('arrow_left', 'left')
Display()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for sprite in buttons_group:
                if sprite.rect.collidepoint(event.pos):  # при нажати на любой спрайт-кнопку отправляет на обработку
                    click_processing(sprite)
    generate_state()
    screen.fill((0, 0, 0))
    room_group.draw(screen)
    player_group.draw(screen)
    dis.draw(screen)
    buttons_group.draw(screen)
    pygame.display.flip()
pygame.quit()
