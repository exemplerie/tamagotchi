import pygame
import sys
import os
import random
import shoes
import snake
import labirint
import fly

# верунлись границы комнат

SIZE = WIDTH, HEIGHT = 670, 800
FPS = 60
LEVELS = ['Baby', 'Adult', 'Elder']  # пока не знаю, пригодятся ли, но можно выводить как названия
SCREEN_RECT = (170, 280, 330, 330)
SIDE = 330


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
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT // 2 + 15
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, k):
        self.number += k
        self.image = room_images[rooms[self.number]]


class Player(pygame.sprite.Sprite):
    def __init__(self, state):
        player_group.empty()
        super().__init__(player_group)
        self.state = state
        if state in player_image[LEVELS[age]]:
            dict_elem = player_image[LEVELS[age]][state]
        elif LEVELS[age] == 'Elder':
            dict_elem = player_image[LEVELS[age]]['main']
        else:
            dict_elem = player_image['Adult'][state]
        self.sheet = dict_elem[0]
        self.frames = []
        self.cut_sheet(self.sheet, dict_elem[1], 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect.center = SCREEN_RECT[0] + SIDE // 2, SCREEN_RECT[1] + SIDE // 2 + 20
        if LEVELS[age] == \
                'Baby':
            self.rect = self.rect.move(0, 30)
            if self.state != 'main':
                self.image = pygame.transform.scale(self.image, (100, 100))

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if LEVELS[age] == 'Baby' and self.state != 'main':
            self.image = pygame.transform.scale(self.image, (100, 100))


class Needs:
    def __init__(self, color, h, need_type):
        self.h = h
        self.value = 100
        self.color = color
        self.need_type = need_type
        icon = load_image('icons\\' + self.need_type + '_icon.png', -1)
        self.image = pygame.transform.scale(icon, (25, 25))

    def render(self):  # отрисовка
        pygame.draw.rect(screen, pygame.Color(self.color), ((390, 280 + 20 * self.h), (70, 17)), 2)
        if self.value != 0:
            pygame.draw.rect(screen, pygame.Color(self.color), ((393, 283 + 20 * self.h), (65 / 100 * self.value, 12)))
        screen.blit(self.image, (470, 270 + 25 * self.h))

    def fill(self, plus):  # заполняет нужды
        if plus > 0 and self.value < 96.5:
            experience_scale.update(plus / 2)
        self.value = self.value + plus

    def update(self):  # постоянное понижение нужд
        self.value -= 0.01
        if self.value > 100:
            self.value = 100
        if self.value < 0:
            self.value = 0
        self.render()


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("bubble.png", -1)]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, mouse_pos, dx, dy):
        super().__init__(particles, all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = mouse_pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 0.05

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(SCREEN_RECT):
            self.kill()


class XP:  # шкала опыта (для достижения новых уровней (возрастов))
    def __init__(self):
        self.value = 95

    def render(self):
        pygame.draw.rect(screen, pygame.Color("black"), ((190, 280), (100, 17)), 2)
        pygame.draw.rect(screen, pygame.Color("purple"), ((193, 283), (95 / 100 * self.value, 12)))

    def update(self, xp=0):
        self.value += xp
        if self.value >= 100:
            self.value = 0
            new_level()
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
    global cursor, then, now, care
    cursor = system_details_images['soap']
    now = pygame.time.get_ticks()
    if tamagotchi.rect.collidepoint(mouse_pos):
        if now - then > 200:
            then = now
            create_particles(pygame.mouse.get_pos())
        care.fill(0.1)  # уход заполняется


def feeding(mouse_pos, click=False):  # кормление
    little_left_arrow.add(buttons_group)  # переключатели блюд
    little_right_arrow.add(buttons_group)
    food_image = food[num_food]
    rect = food_image.get_rect().move(320, 535)
    global cursor
    if not cursor:
        screen.blit(food_image, (320, 525))  # если еда не взята
        food_image.set_alpha(255)
        if click and rect.collidepoint(mouse_pos):  # взятие еды
            cursor = food_image
    elif click:
        if tamagotchi.rect.collidepoint(mouse_pos):  # наполнение голода и пропадание еды
            hunger.fill(3)
            food_image.set_alpha(food_image.get_alpha() - 80)
            if food_image.get_alpha() < 60:
                cursor = None
        if rect.collidepoint(mouse_pos):  # закончилась
            cursor = None


def choose_game(mouse_pos, click=False):
    little_left_arrow.add(buttons_group)  # переключатели блюд
    little_right_arrow.add(buttons_group)
    image = game_images[games[num_game]]
    rect = image.get_rect().move(310, 535)
    screen.blit(image, (310, 525))
    if click and rect.collidepoint(mouse_pos):
        print(happiness.value)
        if games[num_game] == 'shoes':
            happiness.fill(shoes.begin())
        if games[num_game] == 'snake':
            happiness.fill(snake.begin())
            print(happiness.value)
        if games[num_game] == 'labirint':
            happiness.fill(labirint.begin())
        if games[num_game] == 'fly':
            happiness.fill(fly.begin())


def click_processing(btn):  # вынесла обработку нажатий в отдельную функцию сейчас, т.к. все равно
    # потом будет больше функционала и действий с нажатием (чтобы сам цикл не захламлять)
    global actual_state, num_food, num_game, cursor, tamagotchi
    if btn == main_btn:  # обработка нажатий главной кнопки
        if not actual_state:
            if rooms[room.number] == 'bedroom':
                tamagotchi = Player('sleep')
                actual_state = 'Sleep'
            if rooms[room.number] == 'bathroom':
                actual_state = 'Washing'
                global timer
                timer = pygame.time.get_ticks()
            if rooms[room.number] == 'kitchen':
                actual_state = 'Feeding'
            if rooms[room.number] == 'gameroom':
                actual_state = 'Gaming'
        else:
            tamagotchi = Player('main')
            actual_state = None  # отменяет любое состояние
            cursor = None

    elif btn == little_left_arrow:
        if actual_state == 'Feeding':
            num_food = (num_food - 1) % len(food)
        if actual_state == 'Gaming':
            num_game = (num_game - 1) % len(games)
    elif btn == little_right_arrow:
        if actual_state == 'Feeding':
            num_food = (num_food + 1) % len(food)
        if actual_state == 'Gaming':
            num_game = (num_game + 1) % len(games)
    else:
        if tamagotchi.state != 'main':
            tamagotchi = Player('main')
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
    global buttons_group, main_btn
    if room.number == 0:
        left_btn.kill()  # kill() - убирает спрайт из все групп; - die(*group) - из одной
    elif room.number == len(rooms) - 1:
        right_btn.kill()
    else:
        left_btn.add(buttons_group)
        right_btn.add(buttons_group)

    if not room.rect.collidepoint(mouse_pos) or not cursor:  # обработка состояния курсора
        pygame.mouse.set_visible(1)
    elif cursor:
        pygame.mouse.set_visible(0)
        screen.blit(cursor, (x, y))

    if rooms[room.number] == 'hall':  # замена кнопочек в зависимости от комнат
        main_btn.image = system_details_images['main_button']
    else:
        main_btn.image = system_details_images[rooms[room.number] + '_button']

    if actual_state:
        if actual_state == 'Sleep':
            sleeping()
        elif actual_state == 'Washing':
            washing(mouse_pos)
        elif actual_state == 'Feeding':
            feeding(mouse_pos)
        elif actual_state == 'Gaming':
            choose_game(mouse_pos)
    else:
        little_left_arrow.kill()
        little_right_arrow.kill()

    for n in needs:
        n.update()
    experience_scale.update()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def new_level():
    global age
    age += 1


def terminate():  # выход из программы
    pygame.quit()
    sys.exit()


pygame.init()

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

system_details_images = {'arrow_left': load_image('arrow_left.png', -1),
                         'arrow_right': load_image('arrow_right.png', -1),
                         'little_left': load_image('little_left.png', -1),
                         'little_right': load_image('little_right.png', -1),
                         'main_button': load_image('ButtonClassic.png', -1),
                         'bathroom_button': load_image('ButtonBathroom.png', -1),
                         'bedroom_button': load_image('ButtonBedroom.png', -1),
                         'gameroom_button': load_image('ButtonGameroom.png', -1),
                         'kitchen_button': load_image('ButtonKitchen.png', -1),
                         'display': load_image('egg.png', -1),
                         'soap': load_image('soap.png', -1)}

game_images = {'shoes': load_image('icons/shoes_game.png', -1), 'snake': load_image('icons/snake_game.png', -1),
               'labirint': load_image('icons/labirint_game.png', -1), 'fly': load_image('icons/fly_game.png', -1)}
games = ['shoes', 'snake', 'labirint', 'fly']

food = [load_image('food/banana.png', -1), load_image('food/egg.png', -1), load_image('food/grapes.png', -1),
        load_image('food/salad.png', -1),
        load_image('food/corn.png', -1), load_image('food/taco.png', -1)]

room_images = {'kitchen': load_image('kitchen.png'),
               'bathroom': load_image('bathroom.png'), 'bedroom': load_image('bedroom.jpg'),
               'hall': load_image('hall.png'), 'gameroom': load_image('gameroom.png')}
player_image = {'Baby': {'main': [load_image('baby_hamster.png', -1), 5]},
                'Adult': {'main': [load_image('hamster.png', -1), 4],
                          'sleep': [load_image('hamster_sleep.png', -1), 4]},
                'Elder': {'main': [load_image('elder-hamster.png', -1), 2],
                          'sleep': [load_image('elder_hamster_sleep.png', -1), 2]}}
rooms = ['gameroom', 'bedroom', 'hall', 'kitchen', 'bathroom']
age = 0
actual_state = None
num_food = 0
num_game = 0
cursor = None
then = pygame.time.get_ticks()
now = pygame.time.get_ticks()

player_group = pygame.sprite.Group()
buttons_group = pygame.sprite.Group()
room_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
particles = pygame.sprite.Group()
#  poop_group = pygame.sprite.Group()

room = Room()
tamagotchi = Player('main')
left_btn = Buttons('arrow_left', 160, 630)  # в функции потом очень удобно проверять, какая кнопка нажата
right_btn = Buttons('arrow_right', 400, 630)
main_btn = Buttons('main_button', 295, 640)
little_left_arrow = Buttons('little_left', 270, 530)
little_right_arrow = Buttons('little_right', 370, 530)

hunger = Needs("red", 0, "hunger")
sleep = Needs("blue", 1, "sleep")
care = Needs("green", 2, "care")
happiness = Needs("yellow", 3, "happiness")
needs = [hunger, sleep, care, happiness]
experience_scale = XP()

count = -1
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
            if actual_state == 'Gaming':
                choose_game(pos, True)
            for sprite in buttons_group:
                if sprite.rect.collidepoint(pos):  # при нажати на любой спрайт-кнопку отправляет на обработку
                    click_processing(sprite)
    count += 1
    screen.fill((0, 0, 0))
    room_group.draw(screen)
    player_group.draw(screen)
    if count % 30 == 0:
        player_group.update()
    generate_state(pos)
    particles.draw(screen)
    screen.blit(system_details_images['display'], (0, 0))  # отрисовка яйца (убрала отдельный класс,
    # ибо бессмысленно)
    buttons_group.draw(screen)
    particles.update()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
