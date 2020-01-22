import pygame
import sys
import random
import time


def show_score(score, choice=2):  # счет
    s_font = pygame.font.SysFont('monaco', 24)
    s_surf = s_font.render(
        'Score: {0}'.format(score), True, black)
    s_rect = s_surf.get_rect()
    # обычно
    if choice == 1:
        s_rect.midtop = (80, 10)
    # при game_overe
    else:
        s_rect.midtop = (360, 120)
    # рисуем прямоугольник поверх surface
    surface.blit(s_surf, s_rect)


def game_over(score):  # проигрыш
    surface.fill(white)
    go_font = pygame.font.SysFont('monaco', 72)
    go_surf = go_font.render('Game over', True, red)
    go_rect = go_surf.get_rect()
    go_rect.midtop = (360, 15)
    surface.blit(go_surf, go_rect)
    show_score(score, 2)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


class Snake():
    def __init__(self, snake_color):
        self.snake_head_pos = [100, 50]
        # начальное тело змеи состоит из трех сегментов
        # голова змеи - первый элемент, хвост - последний
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
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

    def snake_body_mechanism(
            self, score, food_pos, screen_width, screen_height):
        self.snake_body.insert(0, list(self.snake_head_pos))
        # если съели еду
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            # если съели еду то задаем новое положение еды случайным
            # образом и увеличивем score на один
            food_pos = [random.randrange(1, screen_width/10)*10,
                        random.randrange(1, screen_height/10)*10]
            score += 1
        else:
            # если не нашли еду, то убираем последний сегмент
            self.snake_body.pop()
        return score, food_pos

    def draw_snake(self, play_surface, surface_color):
        play_surface.fill(surface_color)
        for pos in self.snake_body:
            pygame.draw.rect(
                play_surface, self.snake_color, pygame.Rect(
                    pos[0], pos[1], 10, 10))

    def check_for_boundaries(self, screen_width, screen_height):
        if any((
            self.snake_head_pos[0] > screen_width-10
            or self.snake_head_pos[0] < 0,
            self.snake_head_pos[1] > screen_height-10
            or self.snake_head_pos[1] < 0
                )):
            game_over(score)
        for block in self.snake_body[1:]:
            # проверка на то, что первый элемент(голова) врезался в
            # любой другой элемент змеи (закольцевались)
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                game_over(score)


class Food():
    def __init__(self, food_color, screen_width, screen_height):
        self.food_color = food_color
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(1, screen_width/10)*10,
                         random.randrange(1, screen_height/10)*10]

    def draw_food(self, play_surface):
        pygame.draw.rect(
            play_surface, self.food_color, pygame.Rect(
                self.food_pos[0], self.food_pos[1],
                self.food_size_x, self.food_size_y))


pygame.init()

red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
brown = pygame.Color(165, 42, 42)

size = width, height = 720, 460

surface = pygame.display.set_mode(size)
pygame.display.set_caption('Snake Game')

fps = pygame.time.Clock()

snake = Snake(green)
food = Food(brown, width, height)
change_to = "RIGHT"
score = 0
running = True

while running:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = "RIGHT"
            elif event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = "LEFT"
            elif event.key == pygame.K_UP or event.key == ord('w'):
                change_to = "UP"
            elif event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = "DOWN"
            elif event.key == pygame.K_ESCAPE:
                running = False
    surface.fill(white)
    snake.change_to = change_to
    snake.validate_direction_and_change()
    snake.change_head_position()
    score, food.food_pos = snake.snake_body_mechanism(score, food.food_pos, width, height)
    snake.draw_snake(surface, white)
    snake.check_for_boundaries(width, height)
    food.draw_food(surface)

    show_score(score)

    pygame.display.flip()
    fps.tick(25)
game_over(score)