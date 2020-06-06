import pygame
import random

SIZE = WIDTH, HEIGHT = 670, 800
SCREEN_RECT = (180, 280, 480, 560)
SIDE = 330


def start_screen(game_over=False):
    if not game_over:
        intro_text = ["Правила игры:",
                      "Перемещайтесь с помощью ",
                      "стрелок ВВЕРХ, ВНИЗ, ",
                      "ВПРАВО, ВЛЕВО.",
                      "Собирайте квадратики и не",
                      "сталкивайтесь со стенами.",
                      "Нажмите Enter для начала ",
                      "игры или Esc для выхода."]

    else:
        intro_text = ["GAME OVER",
                      "Нажмите Esc для выхода или",
                      "Enter, чтобы начать заново."]
        global common_score, score, fon
        common_score += score
    fon = pygame.transform.scale(fon, (350, 400))
    screen.blit(fon, (150, 270))
    text_coord = 310

    screen.blit(egg, (0, 0))

    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 185
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        screen.blit(egg, (0, 0))

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


def show_score(now_score):  # счет
    surf = font.render(
        'Score: {0}'.format(now_score), True, pygame.Color("white"))
    rect = surf.get_rect()
    rect.midtop = (335, 300)
    screen.blit(surf, rect)


class Snake:
    def __init__(self, snake_color):
        self.snake_head_pos = [180, 280]
        # начальное тело змеи состоит из трех сегментов
        # голова змеи - первый элемент, хвост - последний
        self.snake_body = [[180, 280], [170, 280], [160, 280]]
        self.snake_color = snake_color
        self.direction = "RIGHT"
        self.change_to = self.direction

    def validate_direction_and_change(self):
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 10
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 10
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 10
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 10

    def snake_body_mechanism(self):
        global score, food
        self.snake_body.insert(0, list(self.snake_head_pos))
        # если съели еду
        if (self.snake_head_pos[0] == food.food_pos[0] and
                self.snake_head_pos[1] == food.food_pos[1]):
            # если съели еду то задаем новое положение еды случайным
            # образом и увеличивем score на один
            food_pos = [random.randrange(SCREEN_RECT[0], SCREEN_RECT[2]) // 10 * 10,
                        random.randrange(SCREEN_RECT[1], SCREEN_RECT[3]) // 10 * 10]
            while food_pos in [set(x) for x in self.snake_body]:
                food_pos = [random.randrange(SCREEN_RECT[0], SCREEN_RECT[2]) // 10 * 10,
                            random.randrange(SCREEN_RECT[1], SCREEN_RECT[3]) // 10 * 10]
            score += 5
            food.food_pos = food_pos
        else:
            # если не нашли еду, то убираем последний сегмент
            self.snake_body.pop()

    def draw_snake(self, play_surface, surface_color):
        play_surface.fill(surface_color)
        for pos in self.snake_body:
            pygame.draw.rect(
                play_surface, self.snake_color, pygame.Rect(
                    pos[0], pos[1], 10, 10))

    def check_for_boundaries(self):
        if any((
                self.snake_head_pos[0] > SCREEN_RECT[2]
                or self.snake_head_pos[0] < SCREEN_RECT[0],
                self.snake_head_pos[1] > SCREEN_RECT[3]
                or self.snake_head_pos[1] < SCREEN_RECT[1]
        )):
            return True
        for block in self.snake_body[1:]:
            # проверка на то, что первый элемент(голова) врезался в
            # любой другой элемент змеи (закольцевались)
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                return True


class Food:
    def __init__(self):
        self.food_color = pygame.Color(63, 136, 143)
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(SCREEN_RECT[0], SCREEN_RECT[2]) // 10 * 10,
                         random.randrange(SCREEN_RECT[1], SCREEN_RECT[3]) // 10 * 10]

    def draw_food(self, play_surface):
        pygame.draw.rect(
            play_surface, self.food_color, pygame.Rect(
                self.food_pos[0], self.food_pos[1],
                self.food_size_x, self.food_size_y))


pygame.init()

size = width, height = 670, 800
screen = pygame.display.set_mode(size)
fps = pygame.time.Clock()

egg = pygame.image.load('data\\GUI\\egg.png').convert_alpha()
fon = pygame.image.load('data\\games_data\\background.png').convert_alpha()
font = pygame.font.Font("data\\myfont.ttf", 15)

snake = Snake(pygame.Color(255, 204, 0))
food = Food()
change_to = "RIGHT"
score = 0
common_score = 0
running = True
moves = None


def begin():
    global snake, food, change_to, score, running, common_score
    start_screen()
    common_score = 0
    new_game = True
    while running:
        if new_game:
            new_game = False
            snake = Snake(pygame.Color(255, 204, 0))
            food = Food()
            change_to = "RIGHT"
            score = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                common_score += score
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT:
                    change_to = "LEFT"
                elif event.key == pygame.K_UP:
                    change_to = "UP"
                elif event.key == pygame.K_DOWN:
                    change_to = "DOWN"
        screen.fill(pygame.Color("black"))

        snake.change_to = change_to
        snake.validate_direction_and_change()
        snake.change_head_position()
        snake.snake_body_mechanism()
        snake.draw_snake(screen, pygame.Color("black"))
        if snake.check_for_boundaries():
            start_screen(game_over=True)
            new_game = True
        screen.blit(egg, (0, 0))
        food.draw_food(screen)

        show_score(score)

        pygame.display.flip()
        fps.tick(18)
    return common_score // 2
