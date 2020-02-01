import pygame
import random
import os

SIZE = WIDTH, HEIGHT = 670, 800
FPS = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Xod(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(all_sprites)
        self.image = images[image]
        self.rect = self.image.get_rect().move(x, y)


class Board(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.width = 3
        self.height = 3
        self.cell_size = 111

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color('black'),
                                 (x * self.cell_size + 168, y * self.cell_size + 257, self.cell_size, self.cell_size),
                                 5)

    def get_click(self, mouse_pos):
        global now_xod, board_icons, now_icons, progress, common_score
        cell_x = (mouse_pos[0] - 168) // self.cell_size
        cell_y = (mouse_pos[1] - 257) // self.cell_size

        if now_xod == 'hamster':
            if not (cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height)\
                    and board_icons[cell_y][cell_x] == 0:
                progress += 1
                common_score += 1

                x = cell_x * self.cell_size + 168
                y = cell_y * self.cell_size + 257

                Xod(now_xod, x, y)

                board_icons[cell_y][cell_x] = now_xod

                now_xod = 'shoe'
                now_icons = images[now_xod]
        elif now_xod == 'shoe':
            progress += 1
            cell_x, cell_y = random_choice()
            x = cell_x * self.cell_size + 168
            y = cell_y * self.cell_size + 257

            Xod(now_xod, x, y)

            board_icons[cell_y][cell_x] = now_xod

            now_xod = 'hamster'
            now_icons = images[now_xod]


def random_choice():
    x = random.randint(0, 2)
    y = random.randint(0, 2)
    choice = True
    while choice:
        if board_icons[y][x] == 0:
            choice = False
        else:
            x = random.randint(0, 2)
            y = random.randint(0, 2)
    return x, y


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


def stop(board):
    global running
    if board[0][0] == board[1][0] and board[1][0] == board[2][0] and board[0][0] != 0 or\
            board[0][1] == board[1][1] and board[1][1] == board[2][1] and board[0][1] != 0 or\
            board[0][2] == board[1][2] and board[1][2] == board[2][2] and board[0][2] != 0 or\
            board[0][1] == board[0][2] and board[0][2] == board[0][0] and board[0][1] != 0 or\
            board[1][1] == board[1][2] and board[1][2] == board[1][0] and board[1][1] != 0 or\
            board[2][1] == board[2][2] and board[2][2] == board[2][0] and board[2][1] != 0 or\
            board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != 0 or\
            board[2][0] == board[1][1] and board[1][1] == board[0][2] and board[2][0] != 0:
        start_screen(True)
    if progress == 9:
        running = False
        start_screen(True)


def start_screen(game_over=False):
    global text, font, new_game

    if not game_over:
        intro_text = ["Правила игры:",
                      "Ваш персонаж - фиолетовый.",
                      "Ваш противник - голубой.",
                      "Чтобы сделать ход, нажмите на клетку,",
                      "на которую хотите поставить своего героя.",
                      "Чтобы ваш противник сделал ход,",
                      "нажмите на поле.",
                      "Выигрывает тот,",
                      "кто выстроил своих героев в ряд.",
                      "Нажмите Enter для началы игры."]
        font = pygame.font.Font(None, 23)
        text_coord = 285
    else:
        if now_xod == 'hamster':
            intro_text = ["GAME OVER",
                          "Нажмите Esc для выхода ",
                          "или Enter, чтобы начать заново"]
        else:
            intro_text = ["ВЫ ВЫЙГРАЛИ!!!",
                          "Нажмите Esc для выхода ",
                          "или Enter, чтобы начать заново"]
        font = pygame.font.Font(None, 25)
        text_coord = 330
    new_game = True
    fon = pygame.transform.scale(images['fon'], (350, 400))
    screen.blit(fon, (150, 270))

    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 175
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


images = {'hamster': load_image('X.png', -1), 'shoe': load_image('O.png', -1),
          'egg': load_image('egg.png', -1), 'cookie': load_image('cookie.png', -1),
          'fon': load_image('fon.png'), 'fon2': load_image('fon2.jpg')}


egg = images['egg']
egg_mask = pygame.mask.from_surface(egg)
background = images['fon']
background_rect = background.get_rect().move(150, 255)

all_sprites = pygame.sprite.Group()
hamster_group = pygame.sprite.Group()
boots_group = pygame.sprite.Group()
icons = pygame.sprite.Group()

board_icons = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
now_xod = 'hamster'
font = pygame.font.Font(None, 30)
text = font.render('Ход:', 1, pygame.Color('black'))
boar = Board()
now_icons = images[now_xod]
progress = 0
running = True
new_game = False
moves = None
common_score = 0


def begin():
    global running, common_score, new_game, hamster_group, boots_group, icons, now_xod, all_sprites, board_icons,\
        progress, now_icons
    start_screen()

    while running:
        if new_game:
            if new_game:
                new_game = False
                all_sprites = pygame.sprite.Group()
                hamster_group = pygame.sprite.Group()
                boots_group = pygame.sprite.Group()
                icons = pygame.sprite.Group()
                board_icons.clear()
                board_icons = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                now_xod = 'hamster'
                now_icons = images[now_xod]
                progress = 0

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                boar.get_click(event.pos)
                stop(board_icons)
            if event.type == pygame.QUIT:
                running = False

        screen.fill(pygame.Color('black'))
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        boar.render()
        screen.blit(egg, (0, 0))
        screen.blit(text, (230, 670))
        screen.blit(now_icons, (285, 630))
        pygame.display.flip()
    return common_score
