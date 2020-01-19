import pygame
import sys
import os

# верунлись границы комнат

SIZE = WIDTH, HEIGHT = 670, 800
FPS = 60
LEVELS = ['Baby', 'Teen', 'Adult', 'Elder']  # пока не знаю, пригодятся ли, но можно выводить как названия


class Buttons(pygame.sprite.Sprite):  # все кнопки (для каждой - отдельный экземпляр)
    def __init__(self, detail, left, top):
        super().__init__(buttons_group, all_sprites)
        self.image = system_details_images[detail]
        self.rect = self.image.get_rect().move(left, top)


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
        self.rect = self.image.get_rect().move(280, 380)


class Needs:
    def __init__(self, color, h):
        self.h = h
        self.value = 100
        self.color = color

    def render(self):  # отрисовка
        pygame.draw.rect(screen, pygame.Color(self.color), ((390, 280 + 20 * self.h), (70, 17)), 2)
        pygame.draw.rect(screen, pygame.Color(self.color), ((393, 283 + 20 * self.h), (65 / 100 * self.value, 12)))

    def fill(self, count):  # заполняет нужды
        experience_scale.update(count // 2)
        self.value = self.value + count
        if self.value > 100:
            self.value = 100

    def update(self):  # постоянное понижение нужд
        self.value -= 0.01
        self.render()


class XP:  # шкала опыта (для достижения новых уровней (возрастов))
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

def sleeping():  # сон
    rect = room.rect
    # рисуется полупрозрачный синий прямоугольник на всю поверхность комнаты
    surface = pygame.Surface((room.image.get_width(), room.image.get_height()), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 49, 83, 180), surface.get_rect())
    screen.blit(surface, (rect.left, rect.top))
    sleep.fill(0.1)  # сон заполняется


def washing(mouse_pos):  # мытье
    # в поле экранчика курсор заменяется на мыло
    # пока есть косяк с мылом за пределом дисплея, но потом исправим
    global cursor
    cursor = system_details_images['soap']
    if tamagotchi.rect.collidepoint(mouse_pos):
        global care
        care.fill(0.1)  # уход заполняется


def feeding(mouse_pos, click=False):        # кормление
    little_left_arrow.add(buttons_group)        # переключатели блюд
    little_right_arrow.add(buttons_group)
    food_image = food[num_food]
    rect = food_image.get_rect().move(320, 535)
    global cursor
    if not cursor:
        screen.blit(food_image, (320, 525))     # если еда не взята
        food_image.set_alpha(255)
        if click and rect.collidepoint(mouse_pos):      # взятие еды
            cursor = food_image
    elif click:
        if tamagotchi.rect.collidepoint(mouse_pos):     # наполнение голода и пропадание еды
            hunger.fill(10)
            food_image.set_alpha(food_image.get_alpha() - 80)
            if food_image.get_alpha() < 60:
                cursor = None
        if rect.collidepoint(mouse_pos):        # закончилась
            cursor = None


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
    global actual_state, num_food, cursor
    if btn == main_btn:  # обработка нажатий главной кнопки
        if not actual_state:
            if rooms[room.number] == 'bedroom':
                actual_state = 'Sleep'
            if rooms[room.number] == 'bathroom':
                actual_state = 'Washing'
            if rooms[room.number] == 'kitchen':
                actual_state = 'Feeding'
        else:
            actual_state = None  # отменяет любое состояние
            cursor = None

    elif btn == little_left_arrow:
        num_food = (num_food - 1) % len(food)
    elif btn == little_right_arrow:
        num_food = (num_food + 1) % len(food)
    else:
        actual_state = None
        pygame.mouse.set_visible(1)
        cursor = None
    if btn == left_btn:
        room.update(-1)
    if btn == right_btn:
        room.update(1)


def generate_state(mouse_pos):
    x, y = mouse_pos
    # по сути генерирует актуальное состояние игры - нужную комнату и игрока в нужном возрасте
    # т.е. обновляет их статус, в зависимости от действий (переключения комнат, прибавления возраста)
    global buttons_group
    if room.number == 0:
        left_btn.kill()  # kill() - убирает спрайт из все групп; - die(*group) - из одной
    elif room.number == len(rooms) - 1:
        right_btn.kill()
    else:
        left_btn.add(buttons_group)
        right_btn.add(buttons_group)

    dis = system_details_images['display']      # дисплей (курсор на нем обычный)
    mask = pygame.mask.from_surface(dis)

    if mask.get_at(pos) or not cursor:      # обработка состояния курсора
        pygame.mouse.set_visible(1)
    elif cursor:
        pygame.mouse.set_visible(0)
        screen.blit(cursor, (x, y))

    if actual_state:
        if actual_state == 'Sleep':
            sleeping()
        elif actual_state == 'Washing':
            washing(mouse_pos)
        elif actual_state == 'Feeding':
            feeding(mouse_pos)
    else:
        little_left_arrow.kill()
        little_right_arrow.kill()

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
                         'little_left': load_image('little_left.png', -1),
                         'little_right': load_image('little_right.png', -1),
                         'main_button': load_image('btn.png', -1),
                         'display': load_image('egg.png', -1),
                         'poop': load_image('poop.jpg', -1),
                         'soap': load_image('soap.png', -1)}

food = [load_image('food/banana.png', -1), load_image('food/egg.png', -1), load_image('food/grapes.png', -1),
        load_image('food/salad.png', -1),
        load_image('food/corn.png', -1), load_image('food/taco.png', -1)]

room_images = {'kitchen': load_image('kitchen.jpg'),
               'bathroom': load_image('bathroom.jpg'), 'bedroom': load_image('bedroom.jpg'),
               'hall': load_image('hall.jpg'), 'gameroom': load_image('gameroom.jpg')}
player_image = {0: load_image('duck.png', -1), 1: load_image('baby_2.jpg'),
                2: load_image('baby_2.jpg')}

rooms = ['gameroom', 'bedroom', 'hall', 'kitchen', 'bathroom']
age = 0
actual_state = None
num_food = 0
cursor = None

player_group = pygame.sprite.Group()
buttons_group = pygame.sprite.Group()
room_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
#  poop_group = pygame.sprite.Group()

room = Room()
tamagotchi = Player(age)
left_btn = Buttons('arrow_left', 160, 630)  # в функции потом очень удобно проверять, какая кнопка нажата
right_btn = Buttons('arrow_right', 400, 630)
main_btn = Buttons('main_button', 285, 640)
little_left_arrow = Buttons('little_left', 270, 530)
little_right_arrow = Buttons('little_right', 370, 530)
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
            if actual_state == 'Feeding':
                feeding(pos, True)
            for sprite in buttons_group:
                if sprite.rect.collidepoint(pos):  # при нажати на любой спрайт-кнопку отправляет на обработку
                    click_processing(sprite)
    screen.fill((0, 0, 0))
    room_group.draw(screen)
    player_group.draw(screen)
    generate_state(pos)
    screen.blit(system_details_images['display'], (0, 0))  # отрисовка яйца (убрала отдельный класс,
    # ибо бессмысленно)
    buttons_group.draw(screen)
    pygame.display.flip()
pygame.quit()
