import pygame
import os
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT

SIZE = WIDTH, HEIGHT = 670, 800
FPS = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def load_image(name, colorkey=None):  # загрузка изображения
    fullname = os.path.join('data\\shoes_data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen(game_over=False):
    if not game_over:
        intro_text = ["Правила игры:",
                      "Перемещайтесь с помощью стрелок.",
                      "Не наступайте на клетки с коробками."]
    else:
        intro_text = ["GAME OVER",
                      "Нажмите Esc для выхода ",
                      "или Enter, чтобы начать заново"]
        global score, text, font
        score = 0
        text = font.render(str(score), 1, pygame.Color('black'))
    fon = pygame.transform.scale(images['fon2'], (350, 400))
    screen.blit(fon, (150, 270))
    font = pygame.font.Font(None, 25)
    text_coord = 330
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 190
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        screen.blit(images['egg'], (0, 0))

    while True:
        global running, moves
        moves = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or moves[pygame.K_ESCAPE]:
                running = False
                return
            elif moves[pygame.K_RETURN]:
                running = True
            else:
                continue
            return
        pygame.display.flip()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


images = {'wall': load_image('box.png', -1), 'empty': load_image('grass.png', -1),
          'persona': load_image('hamster_lab.png', -1), 'egg': load_image('egg.png', -1)}

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.add(tiles_group, all_sprites)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = images['persona']
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
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
    return new_player, x, y


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

        if obj.rect.x < -obj.rect.width:
            obj.rect.x += (10 + 1) * obj.rect.width

        if obj.rect.x >= 10 * obj.rect.width:
            obj.rect.x += -obj.rect.width * (1 + 10)

        if obj.rect.y < -obj.rect.height:
            obj.rect.y += (10 + 1) * obj.rect.height
        if obj.rect.y >= 10 * obj.rect.height:
            obj.rect.y += -obj.rect.height * (1 + 10)

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


player, level_x, level_y = generate_level(load_level("level2.txt"))
egg = images['egg']
egg_mask = pygame.mask.from_surface(egg)
running = True

camera = Camera()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                player.rect = player.rect.move(0, -50)
            if event.key == K_DOWN:
                player.rect = player.rect.move(0, +50)
            if event.key == K_RIGHT:
                player.rect = player.rect.move(+50, 0)
            if event.key == K_LEFT:
                player.rect = player.rect.move(-50, 0)

    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill((0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    screen.blit(egg, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)
# завершение работы:
