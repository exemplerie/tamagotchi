import pygame
import sys
import os

# верунлись границы комнат

SIZE = WIDTH, HEIGHT = 670, 800
FPS = 60
LEVELS = ['Baby', 'Teen', 'Adult', 'Elder']  # пока не знаю, пригодятся ли, но можно выводить как названия


class Buttons(pygame.sprite.Sprite):  # все кнопки (для каждой - отдельный экземпляр)
    def __init__(self, detail, side):
        super().__init__(buttons_group, all_sprites)
        self.image = system_details_images[detail]
        if side == 'right':
            self.rect = self.image.get_rect().move(400, 630)
        elif side == 'left':
            self.rect = self.image.get_rect().move(160, 630)


class Room(pygame.sprite.Sprite):  # комнаты пусть пока останутся так, пока не ввели интерактива
    def __init__(self):
        super().__init__(room_group, all_sprites)
        self.number = 2
        self.image = room_images[rooms[self.number]]
        self.rect = self.image.get_rect().move(60, 200)

    def update(self, k):
        self.number += k
        self.image = room_images[rooms[self.number]]


class Player(pygame.sprite.Sprite):
    def __init__(self, what_age):
        super().__init__(player_group, all_sprites)
        self.image = player_image[what_age]
        self.rect = self.image.get_rect().move(280, 400)


class Needs:
    def __init__(self, color, h):
        self.h = h
        self.value = 100
        self.color = color

    def render(self):
        pygame.draw.rect(screen, pygame.Color(self.color), ((390, 280 + 20 * self.h), (70, 17)), 2)
        pygame.draw.rect(screen, pygame.Color(self.color), ((390, 280 + 20 * self.h), (70 / 100 * self.value, 17)))

    def update(self):
        self.value -= 0.1


# class Poop(pygame.sprite.Sprite):
#    def __init__(self):
#        super().__init__(poop_group, all_sprites)
#        self.image = system_details_images['poop']
#        self.rect = self.image.get_rect().move(260, 350)


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
    if btn == right_btn:
        room.update(1)
    if btn == left_btn:
        room.update(-1)


def generate_state():  # по сути генерирует актуальное состояние игры - нужную комнату и игрока в нужном возрасте
    # т.е. обновляет их статус, в зависимости от действий (переключения комнат, прибавления возраста)
    global buttons_group
    if room.number == 0:
        left_btn.kill()  # kill() - убирает спрайт из все групп; - die(*group) - из одной
    elif room.number == len(rooms) - 1:
        right_btn.kill()
    else:
        left_btn.add(buttons_group)
        right_btn.add(buttons_group)
    for n in needs:
        n.update()
        n.render()
    Player(age)


def terminate():  # выход из программы
    pygame.quit()
    sys.exit()


pygame.init()

screen = pygame.display.set_mode(SIZE)

system_details_images = {'arrow_left': load_image('arrow_left.png', -1),
                         'arrow_right': load_image('arrow_right.png', -1),
                         'display': load_image('egg.png', -1),
                         'poop': load_image('poop.jpg', -1)}
# назвала системными деталями, тут все что вне маленького экранчика игры
room_images = {'kitchen': load_image('kitchen.jpg'),
               'bathroom': load_image('bathroom.jpg'), 'bedroom': load_image('bedroom.jpg'),
               'hall': load_image('hall.jpg'), 'gameroom': load_image('gameroom.jpg')}
player_image = {0: load_image('duck.png', -1), 1: load_image('baby_2.jpg'),
                2: load_image('baby_2.jpg')}

rooms = ['gameroom', 'bedroom', 'hall', 'kitchen', 'bathroom']
age = 0

player_group = pygame.sprite.Group()
buttons_group = pygame.sprite.Group()
room_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
#  poop_group = pygame.sprite.Group()

room = Room()
Player(age)
right_btn = Buttons('arrow_right', 'right')  # в функции потом очень удобно проверять, какая кнопка нажата
left_btn = Buttons('arrow_left', 'left')
#  Poop()

hunger = Needs("red", 0)
care = Needs("blue", 1)
happiness = Needs("yellow", 2)
sleep = Needs("purple", 3)
needs = [hunger, care, happiness, sleep]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for sprite in buttons_group:
                if sprite.rect.collidepoint(event.pos):  # при нажати на любой спрайт-кнопку отправляет на обработку
                    click_processing(sprite)
    screen.fill((0, 0, 0))
    room_group.draw(screen)
    player_group.draw(screen)
    screen.blit(system_details_images['display'], (0, 0))
    buttons_group.draw(screen)
    generate_state()
    pygame.display.flip()
pygame.quit()
