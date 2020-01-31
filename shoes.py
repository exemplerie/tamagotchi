import pygame
import random
import os

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


def cut_sheet(lst, sheet, columns, rows):
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            lst.append(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)))


def start_screen(game_over=False):
    if not game_over:
        intro_text = ["Space - выстрел",
                      "Движение - стрелки вправо, влево,",
                      "Ловите печеньки!",
                      "Нажмите Enter",
                      "для начала игры"]
    else:
        intro_text = ["GAME OVER",
                      "Нажмите Esc для выхода ",
                      "или Enter, чтобы начать заново"]
        global score, text, font, common_score
        common_score += score
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


class Player(pygame.sprite.Sprite):
    def __init__(self, lives=3):
        super().__init__(all_sprites)
        self.orig_image = pygame.transform.scale(images['player'], (50, 38))
        self.image = self.orig_image
        self.rect = self.image.get_rect().move(310, 535)
        self.mask = pygame.mask.from_surface(self.image)
        self.lives = lives
        self.shoot_timer = pygame.time.get_ticks()

    def update(self):
        global moves
        if moves[pygame.K_LEFT] and self.rect.left > 175:
            self.rect.x += -5
        elif moves[pygame.K_RIGHT] and self.rect.right < 485:
            self.rect.x += 5
        if moves[pygame.K_SPACE]:
            self.shoot()

    def die(self):
        for s in shoes:
            s.kill()
        self.__init__(self.lives - 1)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > 600:
            self.shoot_timer = now
            Ball(self.rect.centerx, self.rect.top)

    def catch_cookie(self):
        if self.lives < 3:
            self.lives += 1


class Shoe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(shoes, all_sprites)
        self.image_orig = images['shoe']
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(random.randrange(150, 450), random.randrange(230, 240))
        self.speed_y = random.randrange(*speed_range)
        self.speed_x = random.randrange(-1, 1)
        self.rot = 0
        self.rot_speed = random.randrange(-5, 5)
        self.timer = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.timer > 50:
            self.timer = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left < 100 or self.rect.right > 600 or self.rect.bottom > 700:
            Shoe()
            self.kill()


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(balls, all_sprites)
        self.image = images['ball']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -5

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 150:
            self.kill()


class Cookie(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__(cookies, all_sprites)
        self.image = images['cookie']
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = coords
        self.speed_y = 3

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > 700:
            self.kill()
        if pygame.sprite.collide_mask(self, player):
            player.catch_cookie()
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__(all_sprites)
        self.image = clouds[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.timer = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.timer > 50:
            self.timer = now
            self.frame += 1
            if self.frame == len(clouds):
                self.kill()
            else:
                self.image = clouds[self.frame]
                self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)


class Lives(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(hearts, all_sprites)
        self.image = images['heart']
        self.rect = self.image.get_rect()


images = {'player': load_image('hamster.png', -1), 'shoe': load_image('boot.png', -1),
          'cloud': load_image('cloud.png', -1), 'egg': load_image('egg.png', -1),
          'ball': load_image('ball.png', -1), 'cookie': load_image('cookie.png', -1),
          'fon': load_image('fon.png'), 'fon2': load_image('fon2.jpg'), 'heart': load_image('heart.png', -1)}

egg = images['egg']
egg_mask = pygame.mask.from_surface(egg)
background = images['fon']
background_rect = background.get_rect().move(150, 255)

clouds = []
cut_sheet(clouds, images['cloud'], 4, 2)

all_sprites = pygame.sprite.Group()
shoes = pygame.sprite.Group()
balls = pygame.sprite.Group()
cookies = pygame.sprite.Group()
hearts = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
score = 0
common_score = 0
lifes = Lives()
speed_range = (1, 3)
moves = None
running = True

font = pygame.font.Font(None, 30)
text = font.render(str(score), 1, pygame.Color('black'))


def begin():
    global all_sprites, shoes, balls, cookies, player, score, clock, \
        hearts, speed_range, text, screen, running, moves, common_score
    running = True
    start_screen()
    new_game = True
    while running:
        if new_game:
            new_game = False
            all_sprites = pygame.sprite.Group()
            shoes = pygame.sprite.Group()
            balls = pygame.sprite.Group()
            cookies = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            for i in range(8):
                Shoe()
            score = 0

        clock.tick(FPS)

        moves = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or moves[pygame.K_ESCAPE]:
                common_score += score
                running = False

        all_sprites.update()

        booms = pygame.sprite.groupcollide(shoes, balls, True, True, pygame.sprite.collide_mask)
        for boom in booms:
            score += 1
            text = font.render(str(score), 1, pygame.Color('black'))
            Cloud(boom.rect.center)
            if score % 10 == 0:
                Cookie(boom.rect.center)
                speed_range = speed_range[0], speed_range[1] + 1
                if score % 15:
                    speed_range = speed_range[0] + 1, speed_range[1]

        # тапок ударил хомяка
        booms = pygame.sprite.spritecollide(player, shoes, True, pygame.sprite.collide_mask)
        for boom in booms:
            Cloud((boom.rect.centerx, boom.rect.bottom))
            Shoe()
            player.die()

        if len(shoes) < 5:
            Shoe()
        if player.lives == 0:
            start_screen(game_over=True)
            new_game = True

        screen.fill(pygame.Color('black'))
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        for i in range(player.lives):
            img_rect = lifes.rect
            img_rect.x = 450 - 30 * i
            img_rect.y = 280
            screen.blit(lifes.image, img_rect)
        screen.blit(text, (330, 280))
        screen.blit(egg, (0, 0))
        pygame.display.flip()
    return common_score
