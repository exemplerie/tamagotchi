import pygame
import sys
import os
import random
import shelve
from modules import shoes, snake, labirint, fly

SIZE = WIDTH, HEIGHT = 670, 800
FPS = 60
LEVELS = ['Baby', 'Adult', 'Elder']
SCREEN_RECT = (170, 280, 330, 330)
SIDE = 330


class Save:
    def __init__(self, name_file):
        self.file = shelve.open('saves/' + name_file)

    def save(self):
        clear_all()
        self.file.clear()
        info = {'age': tamagotchi.age, 'happiness': happiness.value, 'hunger': hunger.value, 'sleep': sleep.value,
                'care': care.value, 'xp': experience_scale.value}
        self.file['Info'] = info

    def get(self):
        global info
        info = self.file['Info']
        return


def text_render(text, size, color, bold=False):  # текст
    font = pygame.font.Font("data\\myfont.ttf", size)
    if bold:
        font.set_bold(True)
    return font.render(text, 0, color)


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


def cut_sheet(obj, lst, sheet, columns, rows):  # деление картинки для анимирования
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            image = sheet.subsurface(pygame.Rect(
                frame_location, rect.size))
            if obj in player_group and LEVELS[obj.age] == 'Baby':
                image = pygame.transform.scale(image,
                                               (int(image.get_rect().size[0] // 1.3),
                                                int(image.get_rect().size[1] // 1.3)))
            lst.append(image)
    obj.rect = rect


def create_particles():
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(random.choice(numbers), random.choice(numbers))


def terminate():  # выход из программы
    pygame.quit()
    sys.exit()


def menu(pause=False):  # меню
    global new_game, save_data
    start_gif = [load_image('start_menu\\' + str(x) + '.gif') for x in range(24)]
    pic = 0
    black = (0, 0, 0)
    variants = ["new game", "load game", "quit"]
    selected = 0
    saving = False
    if pause:
        variants = ["continue", "save", "return to main menu", "quit"]
        pygame.mixer.stop()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                terminate()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    menu_sound.play()
                    selected = (selected - 1) % len(variants)
                elif e.key == pygame.K_DOWN:
                    menu_sound.play()
                    selected = (selected + 1) % len(variants)
                if e.key == pygame.K_RETURN:
                    menu_sound.play()
                    if variants[selected] in ["slot1", "slot2", "slot3"]:
                        save_data = Save(variants[selected])
                        if saving:
                            save_data.save()
                        else:
                            try:
                                save_data.get()
                                new_game = True
                                return
                            except KeyError:
                                variants = ["slot1", "slot2", "slot3", "return"]
                                variants[selected] = 'none yet!'
                    if variants[selected] == "quit":
                        terminate()
                    if variants[selected] == "new game":
                        new_game = True
                        return
                    if variants[selected] == "load game":
                        selected = 0
                        variants = ["slot1", "slot2", "slot3", "return"]
                    if variants[selected] == "continue":
                        return
                    if variants[selected] == "save":
                        selected = 0
                        variants = ["slot1", "slot2", "slot3", "return"]
                        saving = True
                    if variants[selected] == "return":
                        saving = False
                        if pause:
                            variants = ["continue", "save", "return to main menu", "quit"]
                        else:
                            variants = ["new game", "load game", "quit"]
                        selected = 0
                    if variants[selected] == "return to main menu":
                        pause = False
                        variants = ["new game", "load game", "quit"]
                        selected = 0

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, pygame.Color(255, 228, 196), ((170, 270), (330, 330)))
        screen.blit(start_gif[pic], (195, 370))
        screen.blit(system_details_images['display'], (0, 0))
        pic = (pic + 1) % len(start_gif)
        title = text_render("TAMAGOTCHI", 30, black, bold=True)
        text = []
        if selected >= len(variants):
            selected = 0
        for v in variants:
            if variants[selected] == v:
                text.append(text_render(v, 20, pygame.Color(213, 48, 50)))
            else:
                text.append(text_render(v, 20, black))

        screen.blit(title, (WIDTH / 2 - (title.get_rect()[2] / 2), SCREEN_RECT[1] + 30))

        for line in text:
            screen.blit(line, (WIDTH / 2 - (line.get_rect()[2] / 2), SCREEN_RECT[1] + 70 + 30 * text.index(line) + 1))
        pygame.display.flip()
        clock.tick(10)


class Player(pygame.sprite.Sprite):  # тамагочик
    def __init__(self):
        super().__init__(player_group)
        self.age = 0
        self.state, self.cur_frame, self.image, self.rect, self.sheet, self.mask = [None for _ in range(6)]
        self.frames = []
        self.generate_sprite()
        self.last_update = pygame.time.get_ticks()

    def generate_sprite(self, state='main', growing=False):  # генерация актуального спрайта
        if self.state == state and not growing:
            return
        if state in player_image[LEVELS[self.age]]:
            dict_elem = player_image[LEVELS[self.age]][state]
        elif LEVELS[self.age] == 'Elder':
            dict_elem = player_image[LEVELS[self.age]]['main']
        else:
            dict_elem = player_image['Adult'][state]
        self.state = state
        self.sheet = dict_elem[0]
        self.frames.clear()
        cut_sheet(self, self.frames, self.sheet, dict_elem[1], 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect.center = SCREEN_RECT[0] + SIDE // 2, SCREEN_RECT[1] + SIDE // 2 + 20
        if LEVELS[self.age] == 'Baby':
            self.rect = self.rect.move(15, 30)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 150:
            self.last_update = now
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if not actual_state and self.state != actual_mood():
            self.generate_sprite(actual_mood())


class Needs:  # потребности
    def __init__(self, color, h, need_type):
        self.h = h
        self.value = 80
        self.color = color
        self.need_type = need_type
        icon = load_image('icons\\' + self.need_type + '_icon.png', -1)
        self.image = pygame.transform.scale(icon, (25, 25))

    def render(self):  # отрисовка
        pygame.draw.rect(screen, pygame.Color(self.color), ((390, 280 + 20 * self.h), (70, 17)), 2)
        if self.value > 2:
            pygame.draw.rect(screen, pygame.Color(self.color), ((393, 283 + 20 * self.h), (65 / 100 * self.value, 12)))
        screen.blit(self.image, (470, 270 + 25 * self.h))

    def fill(self, plus):  # заполняет нужды
        self.value = self.value + plus
        if plus > 0 and (self.value < 96.5 or self.need_type == 'happiness'):
            experience_scale.fill(plus / 2)

    def update(self):  # постоянное понижение нужд
        self.value -= 0.01
        if self.value > 100:
            self.value = 100
        self.render()


class XP:  # шкала опыта (для достижения новых уровней (возрастов))
    def __init__(self):
        self.value = 0

    def render(self):  # исовка
        pygame.draw.rect(screen, pygame.Color("black"), ((190, 280), (100, 17)), 2)
        if self.value > 1:
            pygame.draw.rect(screen, pygame.Color("purple"), ((193, 283), (95 / 100 * self.value, 12)))

    def fill(self, xp):
        self.value += xp
        self.render()


class Buttons(pygame.sprite.Sprite):  # все кнопки (для каждой - отдельный экземпляр)
    def __init__(self, detail, left, top):
        super().__init__(buttons_group)
        self.image = system_details_images[detail]
        self.rect = self.image.get_rect().move(left, top)


class Room(pygame.sprite.Sprite):  # комната
    def __init__(self):
        super().__init__(room_group)
        self.number = 2
        self.image = room_images[rooms[self.number]]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT // 2 + 15
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, k):
        self.number += k
        self.image = room_images[rooms[self.number]]


class Particle(pygame.sprite.Sprite):  # частицы
    # сгенерируем частицы разного размера
    fire = [load_image("other/bubble.png", -1)]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, dx, dy):
        super().__init__(particles)
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


def clear_all():  # очищение временных особенностей
    global actual_state, cursor
    actual_state = None
    cursor = None
    little_left_arrow.kill()
    little_right_arrow.kill()
    tamagotchi.update()
    bubble_sound.stop()


def actual_mood():
    if any(need.value < 20 for need in needs):
        return 'cry'
    if any(need.value < 50 for need in needs):
        return 'sad'
    return 'main'


def sleeping():  # сон
    # рисуется полупрозрачный синий прямоугольник на всю поверхность комнаты
    surface = pygame.Surface((room.image.get_width(), room.image.get_height()), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 49, 83, 180), surface.get_rect())
    screen.blit(surface, (room.rect.left, room.rect.top))
    sleep.fill(0.1)  # сон заполняется


def washing():  # мытье
    # в поле экранчика курсор заменяется на мыло
    global cursor, then
    cursor = system_details_images['soap']
    now = pygame.time.get_ticks()
    if tamagotchi.rect.collidepoint(mouse_pos):
        bubble_sound.play()
        tamagotchi.generate_sprite('washing')
        if now - then > 200:
            then = now
            create_particles()
        care.fill(0.1)  # уход заполняется
    else:
        bubble_sound.stop()
        tamagotchi.generate_sprite(actual_mood())


def feeding(click=False):  # кормление
    little_left_arrow.add(buttons_group)  # переключатели блюд
    little_right_arrow.add(buttons_group)
    food_image = food[num_food]

    rect = food_image.get_rect().move(320, 535)
    global cursor
    if not cursor:
        screen.blit(food_image, (315, 525))  # если еда не взята
        food_image.set_alpha(255)
        if click and rect.collidepoint(mouse_pos):  # взятие еды
            cursor = food_image
    elif click:
        if tamagotchi.rect.collidepoint(mouse_pos):  # наполнение голода и пропадание еды
            random.choice(eating_sounds).play()
            hunger.fill(3)
            food_image.set_alpha(food_image.get_alpha() - 80)
            if food_image.get_alpha() < 60:
                cursor = None  # закончилась
        if rect.collidepoint(mouse_pos):  # положили обратно
            cursor = None


def choose_game(click=False):
    little_left_arrow.add(buttons_group)  # переключатели игр
    little_right_arrow.add(buttons_group)
    image = game_icons[games[num_game]]
    image = pygame.transform.scale(image,
                                   (int(image.get_rect().size[0] // 11), int(image.get_rect().size[1] // 11)))
    rect = image.get_rect().move(315, 535)
    screen.blit(image, (315, 525))
    if click and rect.collidepoint(mouse_pos):  # включение игр и заполнение счастья
        if games[num_game] == 'shoes':
            happiness.fill(shoes.begin())
        if games[num_game] == 'snake':
            happiness.fill(snake.begin())
        if games[num_game] == 'labirint':
            happiness.fill(labirint.begin())
        if games[num_game] == 'fly':
            happiness.fill(fly.begin())


def click_processing():  # обработка нажатий
    global actual_state, num_food, num_game
    if actual_state == 'Feeding':
        feeding(True)
    if actual_state == 'Gaming':
        choose_game(True)
    for btn in buttons_group:
        if btn.rect.collidepoint(mouse_pos):
            if btn == main_btn:
                if not actual_state:
                    if rooms[room.number] == 'bedroom':
                        actual_state = 'Sleep'
                        tamagotchi.generate_sprite('sleep')
                    if rooms[room.number] == 'bathroom':
                        actual_state = 'Washing'
                    if rooms[room.number] == 'kitchen':
                        actual_state = 'Feeding'
                    if rooms[room.number] == 'gameroom':
                        actual_state = 'Gaming'
                else:
                    clear_all()

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
                clear_all()
            if btn == left_btn:
                room.update(-1)
            if btn == right_btn:
                room.update(1)


def generate_state():
    # по сути генерирует актуальное состояние игры - нужную комнату и игрока
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
        screen.blit(cursor, mouse_pos)

    main_btn.image = system_details_images[rooms[room.number] + '_button']  # замена кнопочек в зависимости от комнат

    if actual_state:
        if actual_state == 'Sleep':
            sleeping()
        elif actual_state == 'Washing':
            washing()
        elif actual_state == 'Feeding':
            feeding()
        elif actual_state == 'Gaming':
            choose_game()

    for need in needs:
        need.update()
    experience_scale.render()


def new_level():  # переход на новый уровень
    pygame.mixer_music.pause()
    hb_sound.play()
    pygame.mouse.set_visible(0)
    was = tamagotchi.age
    firework_frames = [load_image('firework\\' + str(x) + '.png', -1) for x in range(6)]
    experience_scale.value = 0
    text = text_render("HAPPY BIRTHDAY!", 25, (0, 0, 0))
    text_2 = text_render("Нажмите клавишу Enter,", 13, (0, 0, 0))
    text_3 = text_render("чтобы продолжить", 13, (0, 0, 0))
    text_rect = text.get_rect()
    text2_rect = text_2.get_rect()
    text3_rect = text_3.get_rect()
    for need in needs:
        need.value = 80
    iterations = 0
    pic = 0
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                terminate()
            if e.type == pygame.KEYDOWN and iterations >= 24:
                hb_sound.stop()
                pygame.mixer_music.unpause()
                clear_all()
                return
        if iterations % 6 and 6 <= iterations < 24:
            tamagotchi.age = was
            tamagotchi.generate_sprite('main', True)
        elif 6 <= iterations <= 24:
            tamagotchi.age = was + 1
            tamagotchi.generate_sprite('main', True)
        room_group.draw(screen)
        if iterations > 24:
            screen.blit(text, (WIDTH / 2 - (text_rect[2] / 2), SCREEN_RECT[1] + 10))
            if iterations > 30:
                screen.blit(text_2, (WIDTH / 2 - (text2_rect[2] / 2), SCREEN_RECT[1] + 40))
                screen.blit(text_3, (WIDTH / 2 - (text3_rect[2] / 2), SCREEN_RECT[1] + 60))
        player_group.update()
        player_group.draw(screen)
        screen.blit(firework_frames[pic], (170, 270))
        screen.blit(system_details_images['display'], (0, 0))
        pic = (pic + 1) % len(firework_frames)
        iterations += 1
        pygame.display.flip()
        clock.tick(10)


def die(total_end=False):  # смерть:(
    if total_end:
        end_music = paradise_sound
    else:
        end_music = end_sound
    pygame.mixer_music.stop()
    end_music.play()
    iterations = 0
    wings_y = tamagotchi.rect.top - 25
    end_gif = [load_image('paradise\\' + str(x) + '.gif') for x in range(55)]
    pic = 0

    text = text_render("GAME OVER", 25, (0, 0, 0), bold=True)
    text_2 = text_render("Нажмите клавишу Enter,", 13, (0, 0, 0), bold=True)
    text_3 = text_render("чтобы вернуться в меню", 13, (0, 0, 0), bold=True)
    text_rect = text.get_rect()
    text2_rect = text_2.get_rect()
    text3_rect = text_3.get_rect()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                terminate()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    pygame.mixer.stop()
                    menu()
                    return
        room_group.draw(screen)
        screen.blit(system_details_images['wings'], (223, wings_y))
        player_group.draw(screen)
        screen.blit(system_details_images['display'], (0, 0))
        if iterations > 10 and tamagotchi.rect.bottom > SCREEN_RECT[1] - 10:
            wings_y -= 5
            tamagotchi.rect = tamagotchi.rect.move(0, -5)
        elif iterations > 10:
            if not total_end:
                screen.blit(text, (WIDTH / 2 - (text_rect[2] / 2), SCREEN_RECT[1] + 80))
                if iterations > 30:
                    screen.blit(text_2, (WIDTH / 2 - (text2_rect[2] / 2), SCREEN_RECT[1] + 150))
                    screen.blit(text_3, (WIDTH / 2 - (text3_rect[2] / 2), SCREEN_RECT[1] + 180))
            else:
                text = text_render("Все хомяки попадают в рай...", 15, (0, 0, 0))
                text_2 = text_render("Нажмите клавишу Enter,", 10, (0, 0, 0))
                text_3 = text_render("чтобы вернуться в меню", 10, (0, 0, 0))
                screen.blit(load_image('paradise\\sky.png'), (165, 255))
                screen.blit(end_gif[pic], (190, 360))
                text_rect = text.get_rect()
                text2_rect = text_2.get_rect()
                text3_rect = text_3.get_rect()
                screen.blit(text, (WIDTH / 2 - (text_rect[2] / 2), SCREEN_RECT[1] + 30))
                if iterations > 40:
                    screen.blit(text_2, (320, SCREEN_RECT[1] + 60))
                    screen.blit(text_3, (320, SCREEN_RECT[1] + 80))
                screen.blit(system_details_images['display'], (0, 0))
                pic = (pic + 1) % len(end_gif)
        player_group.update()
        iterations += 1
        pygame.display.flip()
        clock.tick(10)


pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Тамагочи')

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

system_details_images = {'arrow_left': load_image('GUI/arrow_left.png', -1),
                         'arrow_right': load_image('GUI/arrow_right.png', -1),
                         'little_left': load_image('GUI/little_left.png', -1),
                         'little_right': load_image('GUI/little_right.png', -1),
                         'hall_button': load_image('GUI/btn.png', -1),
                         'bathroom_button': load_image('GUI/btn5.png', -1),
                         'bedroom_button': load_image('GUI/btn1.png', -1),
                         'gameroom_button': load_image('GUI/btn6.png', -1),
                         'kitchen_button': load_image('GUI/btn2.png', -1),
                         'display': load_image('GUI/egg.png', -1),
                         'soap': load_image('other/soap.png', -1),
                         'wings': load_image('other/wings.png', -1)}

games = ['shoes', 'snake', 'labirint', 'fly']
game_icons = {'shoes': load_image('icons/shoes_game.png', -1), 'snake': load_image('icons/snake_game.png', -1),
              'labirint': load_image('icons/labirint_game.png', -1), 'fly': load_image('icons/fly_game.png', -1)}

food = [load_image('food/ice-cream.png', -1), load_image('food/fried-egg.png', -1), load_image('food/pizza.png', -1),
        load_image('food/orange.png', -1),
        load_image('food/corn.png', -1), load_image('food/hamburger.png', -1)]

rooms = ['gameroom', 'bedroom', 'hall', 'kitchen', 'bathroom']
room_images = {'kitchen': load_image('backgrounds/kitchen.png'),
               'bathroom': load_image('backgrounds/bathroom.png'), 'bedroom': load_image('backgrounds/bedroom.png'),
               'hall': load_image('backgrounds/hall.png'), 'gameroom': load_image('backgrounds/gameroom.png')}

player_image = {'Baby': {'main': [load_image('hamster_sprites/baby_hamster2.png', -1), 5]},
                'Adult': {'main': [load_image('hamster_sprites/hamster.png', -1), 4],
                          'sleep': [load_image('hamster_sprites/hamster_sleep.png', -1), 4],
                          'sad': [load_image('hamster_sprites/hamster_sad.png', -1), 2],
                          'cry': [load_image('hamster_sprites/hamster_cry.png', -1), 2],
                          'washing': [load_image('hamster_sprites/hamster_wash.png', -1), 6]},
                'Elder': {'main': [load_image('hamster_sprites/elder-hamster.png', -1), 2],
                          'sleep': [load_image('hamster_sprites/elder_hamster_sleep.png', -1), 2]}}

main_music = "data\\music\\main_music.wav"
pygame.mixer.music.load(main_music)
hb_sound = pygame.mixer.Sound("data\\music\\happy_birthday_music.wav")
bubble_sound = pygame.mixer.Sound("data\\music\\bubbling.wav")
eating_sounds = [pygame.mixer.Sound("data\\music\\eating.wav"), pygame.mixer.Sound("data\\music\\eating1.wav"),
                 pygame.mixer.Sound("data\\music\\eating2.wav")]
end_sound = pygame.mixer.Sound("data\\music\\ending.wav")
paradise_sound = pygame.mixer.Sound("data\\music\\paradise.wav")
menu_sound = pygame.mixer.Sound("data\\music\\menu_selection.wav")

player_group = pygame.sprite.Group()
buttons_group = pygame.sprite.Group()
room_group = pygame.sprite.Group()
particles = pygame.sprite.Group()

left_btn = Buttons('arrow_left', 168, 660)
right_btn = Buttons('arrow_right', 404, 660)
main_btn = Buttons('hall_button', 291, 650)
little_left_arrow = Buttons('little_left', 270, 535)
little_right_arrow = Buttons('little_right', 370, 530)

hunger = Needs("red", 0, "hunger")
sleep = Needs("blue", 1, "sleep")
care = Needs("green", 2, "care")
happiness = Needs("yellow", 3, "happiness")
needs = [hunger, sleep, care, happiness]

info = None
running = True
new_game = True
menu()
while running:
    mouse_pos = pygame.mouse.get_pos()
    if new_game:  # начало новой игры
        pygame.mixer.stop()
        pygame.mixer.music.play(-1)
        new_game = False
        experience_scale = XP()
        actual_state = None
        cursor = None
        num_food = 0
        num_game = 0
        player_group.empty()
        tamagotchi = Player()
        room = Room()
        then = pygame.time.get_ticks()
        little_left_arrow.kill()
        little_right_arrow.kill()
        for n in needs:
            n.value = 80
        experience_scale.value = 0
        if info:
            tamagotchi.age = info['age']
            happiness.value = info['happiness']
            hunger.value = info['hunger']
            sleep.value = info['sleep']
            care.value = info['care']
            experience_scale.value = info['xp']
            info = None
            generate_state()
            tamagotchi.generate_sprite(growing=True)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu(pause=True)
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_processing()
    if experience_scale.value >= 100:  # конец игры
        clear_all()
        if tamagotchi.age == 2:
            die(total_end=True)
        else:
            new_level()
    if any(n.value <= 0 for n in needs):
        clear_all()
        die()
    screen.fill((0, 0, 0))
    room_group.draw(screen)
    player_group.update()
    player_group.draw(screen)
    generate_state()

    particles.update()
    particles.draw(screen)
    screen.blit(system_details_images['display'], (0, 0))  # отрисовка яйца
    buttons_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
