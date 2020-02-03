import pygame
import random
import os

pygame.font.init()


def load_image(name, colorkey=None):  # загрузка изображения
    fullname = os.path.join('data/games_data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# глобальные переменные
s_width = 670
s_height = 800
screen = pygame.display.set_mode((s_width, s_height))
play_width = 320
play_height = 300
block_size = 20

top_left_x = (s_width - play_width) // 2
top_left_y = 270

# фигуры(все виды при вращении) в столбик для наглядности
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
Ii = [['..0..',   # i в таком виде из-за PEP8
       '..0..',
       '..0..',
       '..0..',
       '.....'],
      ['.....',
       '0000.',
       '.....',
       '.....',
       '.....']]
o = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, Ii, o, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# цвета фигур


class Piece(object):  # инициализация фигур
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_pos={}):  # создание сетки размером 15 на 16
    grid = [[(0, 0, 0) for _ in range(16)] for _ in range(15)]
    # Параметр locked_pos будет содержать словарь пар «ключ-значение»,
    # где каждый ключ - это позиция уже упавшего куска, а каждое значение - его цвет
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):     # преобразование наглядных списков фигур в список позиций, понятных компьютеру
    positions = []
    form = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(form):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):    # определение свободного места для движения фигуры: если клетка не черная - она занята
    accepted_pos = [[(j, i) for j in range(16) if grid[i][j] == (0, 0, 0)] for i in range(15)]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):   # проверка, проиграли ли игру: если какая-то фигура над экраном, то проигрыш
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))   # выбор произвольной (рандомной) фигуры


def draw_grid(screen, grid):    # эта функция рисует сетку
    sx = top_left_x
    sy = top_left_y
    for i in range(len(grid)):
        pygame.draw.line(screen, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(screen, (128, 128, 128), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))
    pygame.draw.line(screen, (128, 128, 128), (sx, 570), (sx + play_width, 570))


def clear_rows(grid, locked):   # очищение заполненного ряда
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda q: q[1])[::-1]:
            x, y = key
            if y < ind:
                newkey = (x, y + inc)
                locked[newkey] = locked.pop(key)
    return inc


def draw_next_shape(shape, screen):    # рисует следующую фигуру справа
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (0, 0, 0))

    sx = top_left_x + play_width + 10
    sy = top_left_y + play_height / 2 - 40
    form = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(form):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(screen, shape.color, (sx + j*block_size,
                                                       sy + i*block_size, block_size, block_size), 0)
    screen.blit(label, (520, 350))


def draw_window(screen, grid, score=0):   # рисование самого окна
    screen.fill((255, 0, 0))
    screen.blit(load_image('egg.png'), (0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (0, 0, 0))

    screen.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 100))

    # текущий счет
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (0, 0, 0))   # счет

    screen.blit(label, (50, 350))

    for i in range(len(grid)):    # рисуем падающую фигуру
        for j in range(len(grid[i])):
            pygame.draw.rect(screen, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size,
                                                  block_size, block_size), 0)
    draw_grid(screen, grid)


def main(screen):
    locked_positions = {}
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()   # рандомный выбор следующего блока
    clock = pygame.time.Clock()
    fall_time = 0  # время падения блоков
    fall_speed = 0.27  # скорость падения блоков
    score = 0

    while run:
        grid = create_grid(locked_positions)   # создаем сетку
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time/1000 > fall_speed:   # условие для передвижения блока на ячейку вниз
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:   # передвижение блока влево
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:  # передвижение блока вправо
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:   # перемещение на 1 вниз
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:   # разворот блока
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False  # выход

        shape_pos = convert_shape_format(current_piece)  # получение координат блока

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:   # смена блока (какой блок упадет следующим)
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 5   # добавление счета (5 очков за каждый заполненный ряд)

        draw_window(screen, grid, score)   # отображение на окне блока, счета
        draw_next_shape(next_piece, screen)  # отображение следующего блока
        pygame.display.update()

        if check_lost(locked_positions):   # если проиграли
            start_screen(score, game_over=True)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
        screen.blit(load_image('egg.png'), (0, 0))


def start_screen(score=0, game_over=False):
    global common_score
    fon = pygame.transform.scale(load_image('fon2.jpg'), (320, 300))
    if not game_over:
        intro_text = ["Правила игры:",
                      "Перемещайте блоки в стороны",
                      "с помощью стрелок влево и вправо.",
                      "Стрелка вверх - вращение блока.",
                      "Стрелка вниз - увеличение скорости",
                      "падения блоков вниз",
                      "Для начала игры нажмите Enter,",
                      "Для выхода - Esc"]
    else:
        common_score += score
        intro_text = ["GAME OVER",
                      "Нажмите Esc для выхода ",
                      "или Enter, чтобы начать заново"]
    font = pygame.font.Font(None, 23)
    text_coord = 330
    screen.blit(load_image('egg.png'), (0, 0))
    screen.blit(fon, (175, 272))
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 180
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        global running, moves
        moves = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                return int(common_score)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                main(screen)
            else:
                continue
            return
        pygame.display.flip()


pygame.display.set_caption('Tetris')
clock = pygame.time.Clock()
common_score = 0
running = True
moves = None
fps = pygame.time.Clock()


def begin():
    start_screen()
