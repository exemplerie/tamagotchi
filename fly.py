import pygame
import os
import random
from pygame.locals import K_UP, K_DOWN


SIZE = WIDTH, HEIGHT = 670, 800
FPS = 20

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
                      "Перемещайтесь с помощью стрелок:",
                      "ВВЕРХ или ВНИЗ.",
                      "Не касайтсь труб.",
                      "Нажмите Enter для началы игры."]
    else:
        intro_text = ["GAME OVER",
                      "Нажмите Esc для выхода ",
                      "или Enter, чтобы начать заново"]
        global score, text, font
        score = 0
        text = font.render(str(score), 1, pygame.Color('black'))
    fon = pygame.transform.scale(images['fon'], (350, 400))
    screen.blit(fon, (150, 270))
    font = pygame.font.Font(None, 25)
    text_coord = 330
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 185
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


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(170, 350)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, type_n):
        if now % 3 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if type_n == 'down':
            self.rect.y += 2
        elif type_n == 'up':
            self.rect.y -= 20
        elif type_n == 'down_p':
            self.rect.y += 9


class Wall(pygame.sprite.Sprite):
    def __init__(self, type_sprite, y):
        super().__init__(wall_group, all_sprites)
        self.image = images[type_sprite]
        if type == 'up':
            self.rect = self.image.get_rect().move(490, y)
        else:
            self.rect = self.image.get_rect().move(490, y)

    def update(self):
        self.rect.x -= 5


images = {'player': load_image('Pepper.png', -1), 'egg': load_image('egg.png', -1),
          'fon': load_image('fon.png'), 'fon2': load_image('fon2.jpg'), 'up': load_image('up.png', -1),
          'down': load_image('down.png', -1)}

all_sprites = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
play = Player(images['player'], 4, 1)
Wall('up', 190)
Wall('down', 190 + 320)

egg = images['egg']
egg_mask = pygame.mask.from_surface(egg)
background = images['fon']
background_rect = background.get_rect().move(150, 255)

score = 0
common_score = 0
now = 0
running = True
moves = None
new_game = False

font = pygame.font.Font(None, 30)
text = font.render(str(score), 1, pygame.Color('black'))


def begin():
    global running, new_game, play, all_sprites, player_group, wall_group, score, common_score, now
    start_screen()
    while running:
        if new_game:
            new_game = False
            all_sprites = pygame.sprite.Group()
            wall_group = pygame.sprite.Group()
            player_group = pygame.sprite.Group()
            play = Player(images['player'], 4, 1)
            Wall('up', 190)
            Wall('down', 190 + 320)
            score = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    play.update('up')
                if event.key == K_DOWN:
                    play.update('down_p')

        screen.fill((0, 0, 0))
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        player_group.draw(screen)
        play.update('down')
        wall_group.update()
        num = 0
        text_score = font.render(str(int(score)), 1, pygame.Color('black'))
        for wall in wall_group:
            num += 1
            if num == len(wall_group) and wall.rect.x < 360:
                y = random.randint(110, 260)
                Wall('up', y)
                Wall('down', y + 320)
        for wall in wall_group:
            if wall.rect.x < 140:
                score += 0.5
                wall.kill()
        if pygame.sprite.spritecollide(play, wall_group, True, pygame.sprite.collide_mask)\
                or play.rect.y < 255 or play.rect.y > 580:
            common_score += score
            start_screen(game_over=True)
            new_game = True
        screen.blit(text_score, (330, 280))
        pygame.draw.rect(screen, pygame.Color('black'), (0, 0, WIDTH, 255))
        pygame.draw.rect(screen, pygame.Color('black'), (0, 580, WIDTH, HEIGHT))
        screen.blit(egg, (0, 0))
        clock.tick(FPS)
        now += 1
        pygame.display.flip()
    return common_score
