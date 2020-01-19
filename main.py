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
        elif side == 'center':
            self.rect = self.image.get_rect().move(295, 625)


class Room(pygame.sprite.Sprite):
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

    def render(self):       # отрисовка
        if self.value == 0:
            pygame.draw.rect(screen, pygame.Color(self.color), ((390, 280 + 20 * self.h), (70, 17)), 2)
        else:
            pygame.draw.rect(screen, pygame.Color(self.color), ((390, 280 + 20 * self.h), (70, 17)), 2)
            pygame.draw.rect(screen, pygame.Color(self.color), ((393, 283 + 20 * self.h), (65 / 100 * self.value, 12)))

    def fill(self, count):      # заполняет нужды
        experience_scale.update(count // 2)
        self.value = self.value + count

    def update(self):       # постоянное понижение нужд
        self.value -= 0.01
        if self.value > 100:
            self.value = 100
        if self.value < 0:
            self.value = 0
        self.render()


class XP:       # шкала опыта (для достижения новых уровней (возрастов))
    def __init__(self):
        self.experience = 0

    def render(self):
        pygame.draw.rect(screen, pygame.Color("black"), ((190, 280), (100, 17)), 2)
        pygame.draw.rect(screen, pygame.Color("purple"), ((193, 283), (95 / 100 * self.experience, 12)))

    def update(self, xp=0):
        self.experience += xp
        if self.experience > 100:
            self.experience = 100
        self.render()


# class Poop(pygame.sprite.Sprite):
#    def __init__(self):
#        super().__init__(poop_group, all_sprites)
#        self.image = system_details_images['poop']
#        self.rect = self.image.get_rect().move(260, 350)

def sleeping():     # сон
    rect = room.rect
    # рисуется полупрозрачный синий прямоугольник на всю поверхность комнаты
    surface = pygame.Surface((room.image.get_width(), room.image.get_height()), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 49, 83, 180), surface.get_rect())
    screen.blit(surface, (rect.left, rect.top))
    sleep.fill(0.1)     # сон заполняется


def washing(mouse_pos):     # мытье
    x, y = mouse_pos
    pygame.mouse.set_visible(0)
    # в поле экранчика курсор заменяется на мыло
    # пока есть косяк с мылом за пределом дисплея, но потом исправим
    cursor = system_details_images['soap']
    screen.blit(cursor, (x, y))
    if tamagotchi.rect.collidepoint(mouse_pos):
        global care
        care.fill(0.1)      # уход заполняется


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
    global actual_state
    if btn == main_btn:     # обработка нажатий главной кнопки
        if not actual_state:
            if rooms[room.number] == 'bedroom':
                actual_state = 'Sleep'
            if rooms[room.number] == 'bathroom':
                actual_state = 'Washing'
        else:
            actual_state = None     # отменяет любое состояние
    else:
        actual_state = None
        pygame.mouse.set_visible(1)
    if btn == right_btn:
        room.update(1)
    if btn == left_btn:
        room.update(-1)


def generate_state(mouse_pos):
    # по сути генерирует актуальное состояние игры - нужную комнату и игрока в нужном возрасте
    # т.е. обновляет их статус, в зависимости от действий (переключения комнат, прибавления возраста)
    global buttons_group, main_btn
    if room.number == 0:
        left_btn.kill()  # kill() - убирает спрайт из все групп; - die(*group) - из одной
    elif room.number == len(rooms) - 1:
        right_btn.kill()
    else:
        left_btn.add(buttons_group)
        right_btn.add(buttons_group)
    #  замена кнопочек в зависимости от комнат
    main_btn.kill()
    if room.number == 0:
        main_btn = Buttons('gameroom_button', 'center')
    elif room.number == 1:
        main_btn = Buttons('bedroom_button', 'center')
    elif room.number == 2:
        main_btn = Buttons('main_button', 'center')
    elif room.number == 3:
        main_btn = Buttons('kitchen_button', 'center')
    elif room.number == 4:
        main_btn = Buttons('bathroom_button', 'center')
    main_btn.add(buttons_group)
    if actual_state:
        if actual_state == 'Sleep':
            sleeping()
        elif actual_state == 'Washing':
            washing(mouse_pos)



    # в пределах "яйца" оставляем курсор, чтобы удобно было нажимать на кнопки
    dis = system_details_images['display']
    mask = pygame.mask.from_surface(dis)
    if mask.get_at(pos):
        pygame.mouse.set_visible(1)

    for n in needs:
        n.update()
    experience_scale.update()


def terminate():  # выход из программы
    pygame.quit()
    sys.exit()


pygame.init()

screen = pygame.display.set_mode(SIZE)

system_details_images = {'arrow_left': load_image('arrow_left.png', -1),
                         'arrow_right': load_image('arrow_right.png', -1),
                         'main_button': load_image('ButtonClassic.png', -1),
                         'bathroom_button': load_image('ButtonBathroom.png', -1),
                         'bedroom_button': load_image('ButtonBedroom.png', -1),
                         'gameroom_button': load_image('ButtonGameroom.png', -1),
                         'kitchen_button': load_image('ButtonKitchen.png', -1),
                         'display': load_image('egg.png', -1),
                         'poop': load_image('poop.jpg', -1),
                         'soap': load_image('soap.png', -1)}
# назвала системными деталями, тут все что вне маленького экранчика игры
room_images = {'kitchen': load_image('kitchen.jpg'),
               'bathroom': load_image('bathroom.jpg'), 'bedroom': load_image('bedroom.jpg'),
               'hall': load_image('hall.jpg'), 'gameroom': load_image('gameroom.jpg')}
player_image = {0: load_image('duck.png', -1), 1: load_image('baby_2.jpg'),
                2: load_image('baby_2.jpg')}

rooms = ['gameroom', 'bedroom', 'hall', 'kitchen', 'bathroom']
age = 0
actual_state = None

player_group = pygame.sprite.Group()
buttons_group = pygame.sprite.Group()
room_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
#  poop_group = pygame.sprite.Group()

room = Room()
tamagotchi = Player(age)
right_btn = Buttons('arrow_right', 'right')  # в функции потом очень удобно проверять, какая кнопка нажата
left_btn = Buttons('arrow_left', 'left')
main_btn = Buttons('main_button', 'center')
#  Poop()

happiness = Needs("yellow", 0)
sleep = Needs("blue", 1)
hunger = Needs("red", 2)
care = Needs("green", 3)
needs = [happiness, sleep, hunger, care]

experience_scale = XP()

pos = None
running = True
while running:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()  # позиция мышки
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for sprite in buttons_group:
                if sprite.rect.collidepoint(pos):  # при нажати на любой спрайт-кнопку отправляет на обработку
                    click_processing(sprite)
    screen.fill((0, 0, 0))
    room_group.draw(screen)
    player_group.draw(screen)
    generate_state(pos)
    screen.blit(system_details_images['display'], (0, 0))   # отрисовка яйца (убрала отдельный класс,
    # ибо бессмысленно)
    buttons_group.draw(screen)
    pygame.display.flip()
pygame.quit()
