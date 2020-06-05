import pygame
import os
import random

SIZE = WIDTH, HEIGHT = 670, 800
FPS = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def load_image(name, colorkey=None):  # загрузка изображения
    fullname = os.path.join('data\\games_data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def show_score(now_score):  # счет
    surf = font.render(
        'Score: {0}'.format(now_score), True, pygame.Color("white"))
    rect = surf.get_rect()
    rect.midtop = (335, 300)
    screen.blit(surf, rect)


def start_screen(win=False):
    if not win:
        intro_text = ["Правила игры:",
                      "Найдите выход из лабиринта,",
                      "перемещаясь с помощью стрелок.",
                      "Нажмите Enter для начала ",
                      "игры или Esc для выхода."]
    else:
        intro_text = ["ПОБЕДА!",
                      "Нажмите Esc для выхода или",
                      "Enter, чтобы начать заново."]
    fon = pygame.transform.scale(images['fon'], (350, 400))
    screen.blit(fon, (150, 270))
    text_coord = 330
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 185
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        screen.blit(images['egg'], (0, 0))

    while True:
        global running, moves, new_game
        moves = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or moves[pygame.K_ESCAPE]:
                running = False
                return
            elif moves[pygame.K_RETURN]:
                new_game = True
                running = True
            else:
                continue
            return
        pygame.display.flip()


def load_level(filename):  # загрузка уровня
    filename = "data/games_data/levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):  # создание спрайтов
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.add(tiles_group, all_sprites)
        if tile_type == 'wall':
            self.add(box_group)
        elif tile_type == 'finish':
            self.add(finish_group)


class Player(pygame.sprite.Sprite):  # класс игрока
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image_orig = images['persona']
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.x = pos_x
        self.y = pos_y

    def update(self):  # передвижение с границами уровня и коробками
        new_image = None
        if moves[pygame.K_LEFT] and self.x > 0 and level_map[self.y][self.x - 1] != '#':
            self.rect.x -= tile_width
            self.x -= 1
            new_image = pygame.transform.rotate(self.image_orig, 90)
        elif moves[pygame.K_RIGHT] and self.x < level_x and level_map[self.y][self.x + 1] != '#':
            self.rect.x += tile_width
            self.x += 1
            new_image = pygame.transform.rotate(self.image_orig, -90)
        elif moves[pygame.K_UP] and self.y > 0 and level_map[self.y - 1][self.x] != '#':
            self.rect.y -= tile_height
            self.y -= 1
            new_image = pygame.transform.rotate(self.image_orig, 0)
        elif moves[pygame.K_DOWN] and self.y < level_y and level_map[self.y + 1][self.x] != '#':
            self.rect.y += tile_height
            self.y += 1
            new_image = pygame.transform.rotate(self.image_orig, 180)
        if new_image:
            self.image = new_image


def generate_level(level):  # обработка карты уровня
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '&':
                Tile('finish', x, y)
                Tile('empty', x, y)
    return new_player, x, y


class Camera:  # класс камеры
    def __init__(self, size):
        self.dx = 0
        self.dy = 0
        self.size = size

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - 500 // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - 500 // 2)


images = {'wall': load_image('box.png', -1), 'empty': load_image('grass.png'),
          'persona': load_image('hamster_lab.png', -1), 'egg': load_image('egg.png', -1),
          'finish': load_image('finish.png', -1), 'fon': load_image('background.png')}

tile_width = tile_height = 50

new_game = False

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()

list_level = ["level0.txt", "level1.txt", "level2.txt"]
lev = random.choice(list_level)
level_map = load_level(lev)
player, level_x, level_y = generate_level(level_map)

camera = Camera((level_x, level_y))

egg = images['egg']
egg_mask = pygame.mask.from_surface(egg)

common_score = 0
font = pygame.font.Font("data\\myfont.ttf", 15)
running = True
moves = None


def begin():
    global running, common_score, new_game, camera, player, all_sprites, player_group, \
        finish_group, tiles_group, box_group, list_level, lev, level_x, level_y, level_map, moves
    start_screen()
    common_score = 0
    while running:
        if new_game:
            new_game = False
            all_sprites = pygame.sprite.Group()
            tiles_group = pygame.sprite.Group()
            box_group = pygame.sprite.Group()
            player_group = pygame.sprite.Group()
            finish_group = pygame.sprite.Group()

            level = random.choice(list_level)
            while level == lev:
                level = random.choice(list_level)
            lev = level
            level_map = load_level(lev)
            player, level_x1, level_y1 = generate_level(level_map)
            camera = Camera((level_x1, level_y1))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    moves = pygame.key.get_pressed()
                    player.update()

        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
            sprite.rect.x += 150
            sprite.rect.y += 150

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        player_group.draw(screen)
        finish_group.draw(screen)
        pygame.draw.rect(screen, pygame.Color('black'), (0, 0, WIDTH, 255))
        pygame.draw.rect(screen, pygame.Color('black'), (500, 0, WIDTH - 500, HEIGHT))
        pygame.draw.rect(screen, pygame.Color('black'), (0, 590, WIDTH, 255))
        pygame.draw.rect(screen, pygame.Color('black'), (0, 0, WIDTH - 500, HEIGHT))
        screen.blit(egg, (0, 0))

        for finish in finish_group:
            if pygame.sprite.spritecollideany(finish, player_group):
                common_score += 15
                start_screen(win=True)

        pygame.display.flip()
        clock.tick(FPS)
    return common_score
