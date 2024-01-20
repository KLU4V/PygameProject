import pygame
import keyboard
import os
import sys
from pygame.locals import *
import random

global select_rm, select_dc, select_cr, select_fn
pygame.init()
pygame.display.set_caption('Jump to space')
size = width, height = 576, 800
running, game_script = True, True

blocks = pygame.sprite.Group()
fallen_blocks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
hero = pygame.sprite.Group()
items = pygame.sprite.Group()
particles = pygame.sprite.Group()
ghost_blocks = pygame.sprite.Group()

possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
wall_counter = [0, 800]


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def default_change(n):
    with open('values.txt', 'r', encoding='utf8') as file:
        old_data = list()
        for i in file.readlines():
            old_data.append(i)
    old_data[-1] = f'n={n}'
    with open('values.txt', 'w', encoding='utf8') as file:
        file.write(''.join(old_data))


class Hero(pygame.sprite.Sprite):  # создание персонажа
    select_rm = True
    select_dc = False
    select_cr = False
    select_fn = False

    default_right, default_left = '', ''

    run_left, run_right = list(), list()
    death, blink, jumpAn = list(), list(), list()

    def __init__(self):
        super().__init__(all_sprites)

        with open('values.txt', 'r', encoding='utf8') as file:
            for i in file.readlines():
                if 'n=' in i:
                    n = int(list(i)[-1])

        persona = ['redman', 'finn', 'ducky', 'Crabby'][n]
        character_sizes = {'redman': (32, 56), 'finn': (35, 48), 'ducky': (46, 38), 'Crabby': (46, 38)}

        for f in os.listdir(f'graphics/animations/{persona}/default'):  # определение скина
            if 'left' in f'graphics/animations/{persona}/default/' + f:
                self.default_left = pygame.transform.scale(load_image(f'graphics/animations/{persona}/default/' + f),
                                                           character_sizes[persona])

            else:
                self.default_right = pygame.transform.scale(load_image(f'graphics/animations/{persona}/default/' + f),
                                                            character_sizes[persona])

        for f in os.listdir(f'graphics/animations/{persona}/run'):
            if 'left' in f'graphics/animations/{persona}/run/' + f:
                self.run_left.append(pygame.transform.scale(load_image(f'graphics/animations/{persona}/run/' + f),
                                                            character_sizes[persona]))

            else:
                self.run_right.append(pygame.transform.scale(load_image(f'graphics/animations/{persona}/run/' + f),
                                                             character_sizes[persona]))

        self.add(hero)
        self.image = self.default_right

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.direction_x = 0
        self.direction_y = 1
        self.tick_jump_counter = 1
        self.jump_counter = 0

        self.moved = False
        self.jump_flag = [False, 'stand', 0]  # необходимые переменные для движения
        self.falling_flag = [False, "stand"]

        self.rect.x = 100
        self.rect.y = 600

    def run(self, nx):  # бег
        if 0 < self.rect.x + nx < 576 and self.moved is not True:
            self.rect.x += nx
            self.direction_x = nx
            self.moved = True

    def jump(self):  # прыжок
        self.jump_counter += 1
        if -1 < self.jump_counter <= 1 and self.jump_flag[1] is not True:
            if self.moved is True:
                if self.direction_x > 0:
                    self.jump_flag = [True, "right", 10]
                else:
                    self.jump_flag = [True, "left", 10]
            else:
                self.jump_flag = [True, "stand", 10]

    def change_character(self, n):  # смена персонажа (считывается из файлов)
        persona = ['redman', 'finn', 'ducky', 'Crabby'][n]
        character_sizes = {'redman': (32, 56), 'finn': (35, 48), 'ducky': (46, 38), 'Crabby': (46, 38)}
        self.default_left, self.default_right = '', ''
        self.run_left, self.run_right = list(), list()

        prev_x = self.rect.x

        for f in os.listdir(f'graphics/animations/{persona}/default'):  # поиск анимаций
            if 'left' in f'graphics/animations/{persona}/default/' + f:
                self.default_left = pygame.transform.scale(load_image(f'graphics/animations/{persona}/default/' + f),
                                                           character_sizes[persona])

            else:
                self.default_right = pygame.transform.scale(load_image(f'graphics/animations/{persona}/default/' + f),
                                                            character_sizes[persona])

        for f in os.listdir(f'graphics/animations/{persona}/run'):
            if 'left' in f'graphics/animations/{persona}/run/' + f:
                self.run_left.append(pygame.transform.scale(load_image(f'graphics/animations/{persona}/run/' + f),
                                                            character_sizes[persona]))

            else:
                self.run_right.append(pygame.transform.scale(load_image(f'graphics/animations/{persona}/run/' + f),
                                                             character_sizes[persona]))

        self.image = self.default_right  # переопределение масок

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = prev_x
        self.rect.y = 600

    def check_air(self):  # проверка и вычисление траектории прыжка, также сотяние перса на поверхности
        if not pygame.sprite.spritecollideany(self,
                                              fallen_blocks) and self.rect.y + 64 != 800 and self.jump_flag[0] is False:
            self.rect.y += 3
            if self.falling_flag[0] is True and not pygame.sprite.spritecollideany(self,
                                                                                   fallen_blocks):
                if self.falling_flag[1] == "right" and 48 <= self.rect.x + 3 <= 496:
                    self.rect.x += 3
                    self.direction_x = 3
                elif self.falling_flag[1] == "left" and 48 <= self.rect.x - 3 <= 496:
                    self.rect.x -= 3
                    self.direction_x = -3

            if pygame.sprite.spritecollideany(self,
                                              fallen_blocks):
                self.rect.y -= 3
                self.falling_flag = [False, "stand"]
                if self.jump_counter > -1:
                    self.jump_counter -= 1

        elif self.jump_flag[0] is True and self.jump_flag[1] == "stand" and self.tick_jump_counter != 10:
            self.rect.y -= self.jump_flag[2]
            self.tick_jump_counter += 1
            self.jump_flag[2] -= 1

        elif self.jump_flag[0] is True and self.jump_flag[1] == "right" and self.tick_jump_counter != 10:
            self.rect.y -= self.jump_flag[2]
            self.tick_jump_counter += 1
            self.jump_flag[2] -= 1
            if 48 <= self.rect.x + 3 <= 496:
                self.rect.x += 3
                self.direction_x = 3

        elif self.jump_flag[0] is True and self.jump_flag[1] == "left" and self.tick_jump_counter != 10:
            self.rect.y -= self.jump_flag[2]
            self.tick_jump_counter += 1
            self.jump_flag[2] -= 1
            if 48 <= self.rect.x - 3 <= 496:
                self.rect.x -= 3
                self.direction_x = -3

        elif self.tick_jump_counter == 10:
            self.tick_jump_counter = 1
            self.falling_flag = [True, self.jump_flag[1]]
            self.jump_flag = [False, 'stand', 10]

    def check_ground(self):  # столкновение с объектами на одном уровне с персом
        if self.moved is True:
            for i in fallen_blocks:
                while pygame.sprite.collide_rect(self, i):
                    if self.rect.midbottom[1] >= i.rect.midtop[1]:
                        self.rect.x -= self.direction_x

                    else:
                        break
            for i in blocks:
                while pygame.sprite.collide_rect(self, i):
                    if self.rect.midbottom[1] >= i.rect.midtop[1]:
                        self.rect.x -= self.direction_x

                    else:
                        break
            for i in walls:
                while pygame.sprite.collide_rect(self, i):
                    if self.rect.midbottom[1] >= i.rect.midtop[1]:
                        self.rect.x -= self.direction_x

                    else:
                        break
            self.moved = False

    def lower(self):
        self.rect.y += 1
        if pygame.sprite.spritecollideany(self, fallen_blocks) or self.rect.y + 64 != 800:
            self.rect.y -= 1

    def check_death(self):  # проверка смерти перса
        # for i in blocks:
        #     if ((i.rect.topleft[0] <= self.rect.left <= i.rect.topright[0]
        #             or i.rect.topleft[0] <= self.rect.right <= i.rect.topright[0])
        #             and pygame.sprite.collide_rect(self, i) and i.rect.midbottom[1] <= self.rect.midtop[1]):
        if pygame.sprite.spritecollideany(self, blocks):
            return True
        return False

    def dead(self):
        self.rect.x = 100
        self.rect.y = 600
        self.direction_x = 0


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.upFlag = False
        self.count = 0

    def apply(self, obj):  # передвижение камеры при выстраивании блоков в ряд
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self):
        if self.upFlag is True and self.count <= 46:
            self.dy = 1
            self.count += 1

    def default(self):  # начальное положение
        self.count = 0
        self.upFlag = False

    def death(self):  # положение после смерти перса
        self.dx = 0
        self.dy = 0
        self.upFlag = False
        self.count = 0


background_y = -1600


class Block(pygame.sprite.Sprite):
    grass_placedTitle = load_image("graphics/textures/grass/grass_fallen_tile.png")
    grass_placedTitle = pygame.transform.scale(grass_placedTitle, (48, 48))
    grass_fallingTitle = load_image("graphics/textures/grass/grass_falling_tile.png")
    grass_fallingTitle = pygame.transform.scale(grass_fallingTitle, (48, 48))
    dirt_placedTitle = load_image("graphics/textures/dirt/dirt_fallen_tile.png")
    dirt_placedTitle = pygame.transform.scale(dirt_placedTitle, (48, 48))
    space_fallingTitle = load_image("graphics/textures/space/space_falling_tile.png")
    space_fallingTitle = pygame.transform.scale(space_fallingTitle, (48, 48))
    space_placedTitle = load_image("graphics/textures/space/space_fallen_tile.png")
    space_placedTitle = pygame.transform.scale(space_placedTitle, (48, 48))

    def __init__(self):
        super().__init__(all_sprites)

        self.rotate_angle = 0  # угол наклона текстуры

        self.image = pygame.transform.rotate(self.grass_fallingTitle, self.rotate_angle)

        self.add(blocks)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.movement_flag = False

        self.rect.y = 900

    def update(self):  # обновление координат по у, также проверка столкновений и текстур
        global background_y

        for i in fallen_blocks:
            if pygame.sprite.collide_rect(self, i) and self.movement_flag is True:
                self.add(fallen_blocks)
                self.remove(blocks)
                self.movement_flag = False
                if self.rotate_angle == 0:
                    self.image = pygame.transform.rotate(self.grass_placedTitle, self.rotate_angle)
                else:
                    self.image = pygame.transform.rotate(self.space_placedTitle, self.rotate_angle)

        if self.movement_flag:
            if 0 <= self.rect.y + 48 < 800:
                self.rect = self.rect.move(0, 2)

            elif self.rect.y + 48 == 800:
                if background_y < -1226:
                    self.image = pygame.transform.rotate(self.grass_placedTitle, self.rotate_angle)
                else:
                    self.image = pygame.transform.rotate(self.space_placedTitle, self.rotate_angle)
                self.add(fallen_blocks)
                self.remove(blocks)
                self.movement_flag = False

        if self.rotate_angle == 0:
            for value in blocks_dct.values():
                if value[0].rect.y > self.rect.y and pygame.sprite.collide_rect(value[0], self):
                    value[0].image = pygame.transform.rotate(self.dirt_placedTitle, self.rotate_angle)

                elif value[0].rect.y < self.rect.y and pygame.sprite.collide_rect(value[0], self):
                    self.image = pygame.transform.rotate(self.dirt_placedTitle, self.rotate_angle)

    def spawn(self):  # появление новго блока и определение его позиции по иксу
        global possibilities, background_y

        if background_y <= -1226:
            self.rotate_angle = 0
            self.image = pygame.transform.rotate(self.grass_fallingTitle, self.rotate_angle)

        else:
            self.rotate_angle = random.randint(1, 4) * 90
            self.image = pygame.transform.rotate(self.space_fallingTitle, self.rotate_angle)

        self.rect = self.image.get_rect()

        self.add(blocks)
        self.remove(fallen_blocks)

        random.shuffle(possibilities)
        if possibilities:
            x = possibilities[0]
            possibilities.pop(0)

        else:
            possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            x = possibilities[0]
            possibilities.pop(0)

        self.movement_flag = True

        self.rect.x = x * 48
        self.rect.y = -48

    def invisible(self):  # убирание блока с экрана
        self.rect.y = 900

    def default(self):  # возращение блока в исходную позицию
        global possibilities

        possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        self.rotate_angle = random.randint(1, 4) * 90

        self.image = pygame.transform.rotate(self.grass_fallingTitle, self.rotate_angle)

        self.add(blocks)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.movement_flag = False

        self.rect.y = 900


class GhostBlock(pygame.sprite.Sprite):
    dirt = load_image("graphics/textures/dirt/dirt_fallen_tile.png")
    dirt = pygame.transform.scale(dirt, (48, 48))
    space = load_image("graphics/textures/space/space_falling_tile.png")
    space = pygame.transform.scale(space, (48, 48))

    def __init__(self):
        super().__init__(all_sprites)

        self.image = pygame.transform.rotate(self.dirt, 0)

        self.add(ghost_blocks)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.y = 900

    def replace(self, x, y, image):  # замена настоящего блока на призрачный
        self.rect.x, self.rect.y = x, y
        self.image = image

    def change_texture(self):
        pass


class Wall(pygame.sprite.Sprite):
    grasswall = load_image("graphics/textures/dirt/dirt_wall.png")
    grasswall = pygame.transform.scale(grasswall, (48, 48))
    spacewall = load_image("graphics/textures/space/space_wall.png")
    spacewall = pygame.transform.scale(spacewall, (48, 48))

    def __init__(self):
        global wall_counter

        super().__init__(all_sprites)

        self.add(walls)

        if wall_counter[0] == 0:  # выстраивание стен и поворот текстур под нужнымм углом
            self.angle = 270
            self.image = pygame.transform.rotate(self.grasswall, self.angle)
        else:
            self.angle = 90
            self.image = pygame.transform.rotate(self.grasswall, self.angle)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        wall_counter[1] -= 48
        if wall_counter[1] < -48:
            wall_counter[1] = 800
            wall_counter[0] = 528
        self.rect.y = wall_counter[1]
        self.rect.x = wall_counter[0]

    def update(self):  # обновление текстур при достижении определённой выысоты
        global background_y

        if background_y >= -1226:
            self.image = pygame.transform.rotate(self.spacewall, self.angle)

        else:
            self.image = pygame.transform.rotate(self.grasswall, self.angle)


(wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8, wall9, wall10, wall11, wall12, wall13, wall14,
 wall15, wall16, wall17wall18, wall19, wall20, wall21, wall22, wall23, wall24, wall25, wall26, wall27,
 wall28, wall29, wall30, wall31, wall32, wall33, wall34, wall35, wall36) = (Wall(), Wall(), Wall(), Wall(), Wall(),
                                                                            Wall(), Wall(), Wall(),
                                                                            Wall(), Wall(), Wall(), Wall(), Wall(),
                                                                            Wall(),
                                                                            Wall(), Wall(), Wall(), Wall(), Wall(),
                                                                            Wall(), Wall(),
                                                                            Wall(), Wall(), Wall(), Wall(),
                                                                            Wall(), Wall(), Wall(), Wall(), Wall(),
                                                                            Wall(), Wall(),
                                                                            Wall(), Wall(), Wall())

(block1, block2, block3, block4, block5, block6, block7, block8,
 block9, block10, block11, block12, block13, block14, block15, block16, block17, block18, block19, block20, block21,
 block22, block23, block24, block25, block26, block27, block28, block29, block30) = (
    Block(), Block(), Block(), Block(),
    Block(), Block(), Block(), Block(),
    Block(), Block(),
    Block(), Block(), Block(), Block(),
    Block(), Block(), Block(), Block(),
    Block(), Block(), Block(), Block(), Block(), Block(),
    Block(), Block(), Block(), Block(),
    Block(), Block())

blocks_dct = {1: [block1, True], 2: [block2, True], 3: [block3, True], 4: [block4, True], 5: [block5, True],
              6: [block6, True], 7: [block7, True], 8: [block8, True], 9: [block9, True], 10: [block10, True],
              11: [block11, False], 12: [block12, False], 13: [block13, False], 14: [block14, False],
              15: [block15, False], 16: [block16, False], 17: [block17, False], 18: [block18, False],
              19: [block19, False], 20: [block20, False], 21: [block21, False], 22: [block22, False],
              23: [block23, False],
              24: [block24, False], 25: [block25, False], 26: [block26, False], 27: [block27, False],
              28: [block28, False], 29: [block29, False],
              30: [block30, False]}  # словарь с блоками True False отвечает за возможность появления блока

(gblock1, gblock2, gblock3, gblock4, gblock5, gblock6, gblock7, gblock8, gblock9, gblock10) = (
    GhostBlock(), GhostBlock(), GhostBlock(), GhostBlock(), GhostBlock(), GhostBlock(), GhostBlock(), GhostBlock(),
    GhostBlock(), GhostBlock())

gblocks_lst = [gblock1, gblock2, gblock3, gblock4, gblock5, gblock6, gblock7, gblock8, gblock9, gblock10]

character = Hero()
camera = Camera()
tracks = ['sound/tracks/soundtrack1.mp3', 'sound/tracks/soundtrack2.mp3']
action = 'stay'


def main():
    global running, camera, character, background_y, select_rm, select_dc, select_cr, select_fn, tracks, game_script
    global screen, clock

    dead = [False, 0, 0]
    anim_counter_rl = [0, 0, "right"]
    score = 0

    background = load_image("graphics/background.png")
    coin = load_image('graphics/coin.png')
    coin = pygame.transform.scale(coin, (16, 20))
    death_sound = pygame.mixer.Sound('sound/misc sounds/death.ogg')
    steps_dirt = [pygame.mixer.Sound('sound/misc sounds/steps/ES_Footsteps Grass 1.ogg'), False, 0]
    steps_stone = [pygame.mixer.Sound('sound/misc sounds/steps/ES_Footsteps Cement 12.ogg'), False, 0]

    stopped_music = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(stopped_music)

    pygame.mixer.music.set_volume(music_value[0])
    death_sound.set_volume(enviroment_value[0])
    steps_dirt[0].set_volume(enviroment_value[0])
    steps_stone[0].set_volume(enviroment_value[0])

    pygame.mixer.music.load(tracks[0])
    pygame.mixer.music.play(-1)

    with open('values.txt', 'r', encoding='utf8') as file:
        for i in file.readlines():
            if 'n=' in i:
                n = int(list(i)[-1])  # номер героя из файла

    for value in blocks_dct.values():
        if value[1] is True:
            value[0].spawn()
            value[0].rect.y = 752

    while running:
        if background_y >= -1226:  # счёт времени для шагов
            if steps_stone[1] is True:
                steps_stone[2] += 1
        else:
            if steps_dirt[1] is True:
                steps_dirt[2] += 1

        if dead[0] is False:

            if character.check_death() or dead[0] is True:  # проверка смерти перса
                dead[0] = True
            values_file = open('values.txt', mode='r+', encoding='utf8')
            values = values_file.readlines()
            coins = int(values[0][2:].strip())
            skins = values[1][2:].split()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_script = False

                # открытие меню паузы
                if pygame.key.get_pressed()[K_ESCAPE]:
                    paused = True
                    # загрузка всех спрайтов
                    brightness_low = load_image("graphics/brightness_low.png")
                    brightness_low = pygame.transform.scale(brightness_low, (576, 800))
                    brightness_low = brightness_low.convert()
                    brightness_low.set_alpha(200)
                    brightness_high = load_image("graphics/brightness_high.png")
                    brightness_high = pygame.transform.scale(brightness_high, (112, 142))
                    brightness_high = brightness_high.convert()
                    brightness_high.set_alpha(50)
                    brightness_high1 = pygame.transform.scale(brightness_high, (40, 40))
                    start_active = load_image("graphics/textures/pause_menu/start/start_active.png")
                    start_inactive = load_image("graphics/textures/pause_menu/start/start_inactive.png")
                    leave_active = load_image("graphics/textures/pause_menu/leave/leave_active.png")
                    leave_inactive = load_image("graphics/textures/pause_menu/leave/leave_inactive.png")
                    store_active = load_image("graphics/textures/pause_menu/store/store_active.png")
                    store_inactive = load_image("graphics/textures/pause_menu/store/store_inactive.png")
                    wardrobe_active = load_image("graphics/textures/pause_menu/wardrobe/wardrobe_active.png")
                    wardrobe_inactive = load_image("graphics/textures/pause_menu/wardrobe/wardrobe_inactive.png")
                    select_active = load_image("graphics/textures/pause_menu/wardrobe/select_active.png")
                    select_inactive = load_image("graphics/textures/pause_menu/wardrobe/select_inactive.png")
                    select_blocked = load_image("graphics/textures/pause_menu/wardrobe/select_blocked.png")
                    back = load_image("graphics/textures/pause_menu/wardrobe/back.png")
                    buy_active = load_image("graphics/textures/pause_menu/store/buy_active.png")
                    buy_inactive = load_image("graphics/textures/pause_menu/store/buy_inactive.png")
                    buy_blocked = load_image("graphics/textures/pause_menu/store/buy_blocked.png")
                    left_rm = load_image("graphics/animations/redman/default/default_left.png")
                    last_active = load_image("graphics/textures/pause_menu/store/last_active.png")
                    last_active = pygame.transform.scale(last_active, (30, 30))
                    next_active = load_image("graphics/textures/pause_menu/store/next_active.png")
                    next_active = pygame.transform.scale(next_active, (30, 30))
                    last_inactive = load_image("graphics/textures/pause_menu/store/last_inactive.png")
                    last_inactive = pygame.transform.scale(last_inactive, (30, 30))
                    next_inactive = load_image("graphics/textures/pause_menu/store/next_inactive.png")
                    next_inactive = pygame.transform.scale(next_inactive, (30, 30))
                    left_dc = load_image('graphics/animations/ducky/default/left1.png')
                    left_fn = load_image('graphics/animations/finn/default/left1.png')
                    left_cr = load_image('graphics/animations/Crabby/default/left1.png')
                    left_dc = pygame.transform.scale(left_dc, (200, 165))
                    left_rm = pygame.transform.scale(left_rm, (115, 200))
                    left_fn = pygame.transform.scale(left_fn, (147, 200))
                    left_cr = pygame.transform.scale(left_cr, (200, 130))
                    left_dc1 = pygame.transform.scale(left_dc, (100, 82))
                    left_rm1 = pygame.transform.scale(left_rm, (57, 100))
                    left_fn1 = pygame.transform.scale(left_fn, (73, 100))
                    left_cr1 = pygame.transform.scale(left_cr, (100, 65))
                    # введение переменных для меню паузы
                    is_start_active = False
                    is_wardrobe_active = False
                    is_store_active = False
                    is_leave_active = False
                    wardrobe_open = False
                    store_open = False
                    wr_is1 = False
                    wr_is2 = False
                    wr_is3 = False
                    wr_is4 = False
                    wr_is5 = False
                    wr_is6 = False
                    wr_is_back = False
                    wr_is_select = 'blocked'
                    if n == 0:
                        wr_wh_skn = 'rm'
                        select_dc = False
                        select_rm = True
                        select_cr = False
                        select_fn = False

                    elif n == 1:
                        wr_wh_skn = 'fn'
                        select_dc = False
                        select_rm = False
                        select_cr = False
                        select_fn = True

                    elif n == 2:
                        wr_wh_skn = 'dc'
                        select_dc = True
                        select_rm = False
                        select_cr = False
                        select_fn = False

                    elif n == 3:

                        wr_wh_skn = 'cr'
                        select_dc = False
                        select_rm = False
                        select_cr = True
                        select_fn = False
                    st_is_back = False
                    st_is_purchase = 'inactive'
                    st_is_next = False
                    st_is_last = False

                    count = 0
                    # создание цикла паузы
                    while paused:
                        # вывод начальных спрайтов, надписей
                        screen.blit(background, (0, background_y))
                        all_sprites.draw(screen)
                        screen.blit(brightness_low, (0, 0))
                        f2 = pygame.font.Font("graphics/fonts/Silkscreen-Regular.ttf"
                                              , 20)
                        bolding = f2.render(str(coins), True,
                                            (255, 255, 255))
                        if len(str(coins)) == 1:
                            screen.blit(coin, (65, 15))
                        elif len(str(coins)) == 2:
                            screen.blit(coin, (82, 15))
                        elif len(str(coins)) == 3:
                            screen.blit(coin, (99, 15))
                        else:
                            screen.blit(coin, (116, 15))
                        screen.blit(bolding, (50, 10))
                        # часть цикла при открытии гардероба
                        if wardrobe_open:
                            if wardrobe_open:
                                # вывод всех спрайтов в гардеробе
                                f1 = pygame.font.Font("graphics/fonts/Silkscreen-Regular.ttf"
                                                      , 50)
                                store = f1.render('Wardrobe', True,
                                                  (255, 255, 255))
                                screen.blit(store, (130, 170))
                                screen.blit(back, (73, 260))
                                if 'rm' in skins:
                                    screen.blit(left_rm1, (302, 321))
                                if 'cr' in skins:
                                    screen.blit(left_cr1, (281, 479))
                                if 'fn' in skins:
                                    screen.blit(left_fn1, (406, 321))
                                if 'dc' in skins:
                                    screen.blit(left_dc1, (393, 472))
                                if wr_is_back:
                                    screen.blit(brightness_high1, (75, 260))
                                if 'rm' in skins:
                                    if wr_is1:
                                        screen.blit(brightness_high, (275, 300))
                                if 'cr' in skins:
                                    if wr_is2:
                                        screen.blit(brightness_high, (275, 442))
                                if 'fn' in skins:
                                    if wr_is3:
                                        screen.blit(brightness_high, (387, 300))
                                if 'dc' in skins:
                                    if wr_is4:
                                        screen.blit(brightness_high, (387, 442))
                                if wr_is_select == 'active':
                                    screen.blit(select_active, (74, 500))
                                elif wr_is_select == 'inactive':
                                    screen.blit(select_inactive, (74, 500))
                                elif wr_is_select == 'blocked':
                                    screen.blit(select_blocked, (74, 500))
                                if wr_wh_skn in skins:
                                    if wr_wh_skn == 'rm':
                                        screen.blit(left_rm, (116, 300))
                                    elif wr_wh_skn == 'dc':
                                        screen.blit(left_dc, (75, 335))
                                    elif wr_wh_skn == 'fn':
                                        screen.blit(left_fn, (101, 300))
                                    else:
                                        screen.blit(left_cr, (75, 370))
                            pygame.draw.rect(screen, (50, 50, 50), (275, 300, 224, 284), 2)
                            pygame.draw.line(screen, (50, 50, 50), (387, 300), (387, 584))
                            pygame.draw.line(screen, (50, 50, 50), (275, 442), (499, 442))
                            # создание задач для кнопок на мыши и клавиатуре
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()
                                if event.type == pygame.MOUSEMOTION:
                                    # действия при движении мыши
                                    if wr_is_select != 'blocked':
                                        if 76 <= event.pos[0] <= 276 and 500 <= event.pos[1] <= 600:
                                            wr_is_select = 'active'
                                        else:
                                            wr_is_select = 'inactive'
                                    if 275 <= event.pos[0] <= 387 and 300 <= event.pos[1] <= 442:
                                        wr_is1 = True
                                    else:
                                        wr_is1 = False
                                    if 275 <= event.pos[0] <= 387 and 443 <= event.pos[1] <= 584:
                                        wr_is2 = True
                                    else:
                                        wr_is2 = False
                                    if 388 <= event.pos[0] <= 499 and 300 <= event.pos[1] <= 442:
                                        wr_is3 = True
                                    else:
                                        wr_is3 = False
                                    if 388 <= event.pos[0] <= 499 and 443 <= event.pos[1] <= 584:
                                        wr_is4 = True
                                    else:
                                        wr_is4 = False
                                    if 75 <= event.pos[0] <= 115 and 260 <= event.pos[1] <= 300:
                                        wr_is_back = True
                                    else:
                                        wr_is_back = False
                                    # действия при нажатии мыши
                                if event.type == pygame.MOUSEBUTTONUP:
                                    if 76 <= event.pos[0] <= 276 and 500 <= event.pos[1] <= 600:
                                        wr_is_select = 'blocked'
                                        # обращение к функции изменения персонажа
                                        if wr_wh_skn == 'rm':
                                            select_rm = True
                                            select_dc = False
                                            select_cr = False
                                            select_fn = False
                                            character.change_character(0)
                                            default_change(0)
                                            n = 0

                                        elif wr_wh_skn == 'dc':
                                            select_dc = True
                                            select_cr = False
                                            select_rm = False
                                            select_fn = False
                                            character.change_character(2)
                                            default_change(2)
                                            n = 2

                                        elif wr_wh_skn == 'fn':
                                            select_fn = True
                                            select_dc = False
                                            select_rm = False
                                            select_cr = False
                                            character.change_character(1)
                                            default_change(1)
                                            n = 1

                                        else:
                                            select_cr = True
                                            select_dc = False
                                            select_rm = False
                                            select_fn = False
                                            character.change_character(3)
                                            default_change(3)

                                            n = 3
                                    if 275 <= event.pos[0] <= 387 and 300 <= event.pos[1] <= 442:
                                        if 'rm' in skins:
                                            wr_wh_skn = 'rm'
                                            if not select_rm:
                                                wr_is_select = 'inactive'
                                            else:
                                                wr_is_select = 'blocked'
                                    if 275 <= event.pos[0] <= 387 and 443 <= event.pos[1] <= 584:
                                        if 'cr' in skins:
                                            wr_wh_skn = 'cr'
                                            if not select_cr:
                                                wr_is_select = 'inactive'
                                            else:
                                                wr_is_select = 'blocked'
                                    if 388 <= event.pos[0] <= 499 and 300 <= event.pos[1] <= 442:
                                        if 'fn' in skins:
                                            wr_wh_skn = 'fn'
                                            if not select_fn:
                                                wr_is_select = 'inactive'
                                            else:
                                                wr_is_select = 'blocked'
                                    if 388 <= event.pos[0] <= 499 and 443 <= event.pos[1] <= 584:
                                        print(select_dc)
                                        if 'dc' in skins:
                                            wr_wh_skn = 'dc'
                                            if not select_dc:
                                                wr_is_select = 'inactive'
                                            else:
                                                wr_is_select = 'blocked'
                                    if 75 <= event.pos[0] <= 115 and 260 <= event.pos[1] <= 300:
                                        wardrobe_open = False
                        # часть цикла для магазина
                        elif store_open:
                            # вывод спрайтов, надписей
                            f1 = pygame.font.Font("graphics/fonts/Silkscreen-Regular.ttf"
                                                  , 50)
                            store = f1.render('Store', True,
                                              (255, 255, 255))
                            f2 = pygame.font.Font("graphics/fonts/Silkscreen-Regular.ttf"
                                                  , 30)
                            screen.blit(store, (200, 170))
                            screen.blit(back, (73, 260))
                            print(skins)
                            if st_is_back:
                                screen.blit(brightness_high1, (75, 260))
                            if st_is_purchase == 'active':
                                screen.blit(buy_active, (188, 500))
                            elif st_is_purchase == 'inactive':
                                screen.blit(buy_inactive, (188, 500))
                            else:
                                screen.blit(buy_blocked, (188, 500))
                            if st_is_last:
                                screen.blit(last_active, (155, 385))
                            else:
                                screen.blit(last_inactive, (155, 385))
                            if st_is_next:
                                screen.blit(next_active, (391, 385))
                            else:
                                screen.blit(next_inactive, (391, 385))
                            # часть действий при выборе персонажа
                            if count % 4 == 0:
                                red_man = f2.render('Red Man', True, (255, 255, 255))
                                screen.blit(red_man, (210, 250))
                                st_rm = f2.render('FREE', True, (255, 255, 255))
                                screen.blit(st_rm, (245, 580))
                                screen.blit(left_rm, (230, 300))
                                if 'rm' in skins:
                                    st_is_purchase = 'blocked'
                                else:
                                    st_is_purchase = 'inactive'
                            elif count % 4 == 1:
                                finn = f2.render('Finn', True, (255, 255, 255))
                                screen.blit(finn, (245, 250))
                                st_fn = f2.render('100 coins', True, (255, 255, 255))
                                screen.blit(st_fn, (195, 580))
                                screen.blit(left_fn, (215, 300))
                                if 'fn' in skins:
                                    st_is_purchase = 'blocked'
                                else:
                                    st_is_purchase = 'inactive'
                            elif count % 4 == 2:
                                crab = f2.render('Crab', True, (255, 255, 255))
                                screen.blit(crab, (245, 250))
                                st_cr = f2.render('500 coins', True, (255, 255, 255))
                                screen.blit(st_cr, (192, 580))
                                screen.blit(left_cr, (188, 370))
                                if 'cr' in skins:
                                    st_is_purchase = 'blocked'
                                else:
                                    st_is_purchase = 'inactive'
                            else:
                                ducky = f2.render('Ducky', True, (255, 255, 255))
                                screen.blit(ducky, (230, 250))
                                st_dc = f2.render('1000 coins', True, (255, 255, 255))
                                screen.blit(st_dc, (182, 580))
                                screen.blit(left_dc, (188, 335))
                                if 'dc' in skins:
                                    st_is_purchase = 'blocked'
                                else:
                                    st_is_purchase = 'inactive'
                            # действия для кнопок мыши клавиатуры
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()
                                # действия при движении мыши
                                if event.type == pygame.MOUSEMOTION:
                                    if st_is_purchase != 'blocked':
                                        if 188 <= event.pos[0] <= 388 and 500 <= event.pos[1] <= 600:
                                            st_is_purchase = 'active'
                                        else:
                                            st_is_purchase = 'inactive'
                                    if 155 <= event.pos[0] <= 185 and 385 <= event.pos[1] <= 415:
                                        st_is_last = True
                                    else:
                                        st_is_last = False
                                    if 391 <= event.pos[0] <= 421 and 385 <= event.pos[1] <= 415:
                                        st_is_next = True
                                    else:
                                        st_is_next = False
                                    if 75 <= event.pos[0] <= 115 and 260 <= event.pos[1] <= 300:
                                        st_is_back = True
                                    else:
                                        st_is_back = False
                                # действия при нажатии
                                if event.type == pygame.MOUSEBUTTONUP:
                                    if 75 <= event.pos[0] <= 115 and 260 <= event.pos[1] <= 300:
                                        store_open = False
                                    # покупка персонажей
                                    if 188 <= event.pos[0] <= 388 and 500 <= event.pos[1] <= 600:
                                        if st_is_purchase != 'blocked':
                                            if count % 4 == 0:
                                                st_is_purchase = 'blocked'
                                            elif count % 4 == 1:
                                                if coins > 99:
                                                    coins -= 100
                                                    st_is_purchase = 'blocked'
                                                    clean = open('values.txt', 'w+')
                                                    clean.seek(0)
                                                    clean.close()
                                                    skins.append('fn')
                                                    with open('values.txt', mode='r+',
                                                              encoding="utf8") as values_file_w:
                                                        values_file_w.write(f'c={coins}\n')
                                                        values_file_w.write(f's={" ".join(skins)}\n')
                                                        values_file_w.write(f'n={n}')
                                            elif count % 4 == 2:
                                                if coins > 499:
                                                    coins -= 500
                                                    st_is_purchase = 'blocked'
                                                    clean = open('values.txt', 'w+')
                                                    clean.seek(0)
                                                    clean.close()
                                                    skins.append('cr')
                                                    with open('values.txt', mode='r+',
                                                              encoding="utf8") as values_file_w:
                                                        values_file_w.write(f'c={coins}\n')
                                                        values_file_w.write(f's={" ".join(skins)}\n')
                                                        values_file_w.write(f'n={n}')
                                            else:
                                                if coins > 999:
                                                    coins -= 1000
                                                    st_is_purchase = 'blocked'
                                                    clean = open('values.txt', 'w+')
                                                    clean.seek(0)
                                                    clean.close()
                                                    skins.append('dc')
                                                    with open('values.txt', mode='r+',
                                                              encoding="utf8") as values_file_w:
                                                        values_file_w.write(f'c={coins}\n')
                                                        values_file_w.write(f's={" ".join(skins)}\n')
                                                        values_file_w.write(f'n={n}')
                                    # действия при смене персонажей
                                    if 155 <= event.pos[0] <= 185 and 385 <= event.pos[1] <= 415:
                                        count -= 1
                                    if 391 <= event.pos[0] <= 421 and 385 <= event.pos[1] <= 415:
                                        count += 1
                        # основное меню паузы
                        else:
                            # вывод всех спрайтов
                            f1 = pygame.font.Font("graphics/fonts/Silkscreen-Regular.ttf"
                                                  , 40)
                            pause_menu = f1.render('Pause menu', True,
                                                   (255, 255, 255))
                            screen.blit(pause_menu, (140, 270))
                            if is_start_active:
                                screen.blit(start_active, (51, 350))

                            else:
                                screen.blit(start_inactive, (51, 350))
                            if is_wardrobe_active:
                                screen.blit(wardrobe_active, (176, 350))
                            else:
                                screen.blit(wardrobe_inactive, (176, 350))
                            if is_store_active:
                                screen.blit(store_active, (301, 350))
                            else:
                                screen.blit(store_inactive, (301, 350))
                            if is_leave_active:
                                screen.blit(leave_active, (427, 350))
                            else:
                                screen.blit(leave_inactive, (427, 350))
                            # действия при нажатии на клавиатуру и мышь
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()
                                # действия при движении мыши
                                if event.type == pygame.MOUSEMOTION:
                                    if 51 <= event.pos[0] <= 151 and 350 <= event.pos[1] <= 450:
                                        is_start_active = True
                                    else:
                                        is_start_active = not True
                                    if 176 <= event.pos[0] <= 276 and 350 <= event.pos[1] <= 450:
                                        is_wardrobe_active = True
                                    else:
                                        is_wardrobe_active = not True
                                    if 301 <= event.pos[0] <= 401 and 350 <= event.pos[1] <= 450:
                                        is_store_active = True
                                    else:
                                        is_store_active = not True
                                    if 427 <= event.pos[0] <= 527 and 350 <= event.pos[1] <= 450:
                                        is_leave_active = True
                                    else:
                                        is_leave_active = not True
                                # действия при нажатии
                                if event.type == pygame.MOUSEBUTTONUP:
                                    if 51 <= event.pos[0] <= 151 and 350 <= event.pos[1] <= 450 and event.button == 1:
                                        paused = False
                                    elif (176 <= event.pos[0] <= 276 and 350 <= event.pos[1]
                                          <= 450 and event.button == 1):
                                        wardrobe_open = True
                                    elif (301 <= event.pos[0] <= 401 and 350 <= event.pos[1]
                                          <= 450 and event.button == 1):
                                        store_open = True
                                    # реализация выхода в главное меню
                                    elif 427 <= event.pos[0] <= 527 and 350 <= event.pos[
                                        1] <= 450 and event.button == 1:
                                        pygame.mixer.music.stop()
                                        paused = False
                                        running = False
                                        for c, value in enumerate(blocks_dct.values()):
                                            value[0].default()
                                            if c < 10:
                                                value[1] = True
                                            else:
                                                value[1] = False

                                        for value in blocks_dct.values():
                                            if value[1] is True:
                                                value[0].spawn()
                                                value[0].rect.y = 752
                                        character.rect.y = 650
                                        character.image = character.default_right

                                        background_y = -1600

                                        dead = [False, 0, 0]
                                        score = 0
                                        character.dead()

                        if pygame.key.get_pressed()[K_RETURN]:
                            paused = False

                        pygame.display.update()

                if not (pygame.key.get_pressed()[K_d] or pygame.key.get_pressed()[K_a]):  # сброс анимаций
                    if anim_counter_rl[2] == "right":
                        character.image = character.default_right
                        anim_counter_rl = [0, 0, "right"]
                    else:
                        character.image = character.default_left
                        anim_counter_rl = [0, 0, "left"]
                    steps_dirt[0].stop()
                    steps_dirt[2] = 0
                    steps_dirt[1] = False

                if pygame.key.get_pressed()[K_a]:  # бег влево + анимация
                    character.run(-4)
                    print(character.rect.x, character.direction_x)
                    anim_counter_rl[1] += 1
                    anim_counter_rl[2] = "left"

                    if anim_counter_rl[0] <= len(character.run_left) - 1 and anim_counter_rl[1] % 4 == 0:
                        character.image = character.run_left[anim_counter_rl[0]]
                        anim_counter_rl[0] += 1
                    elif anim_counter_rl[0] >= len(character.run_left):
                        anim_counter_rl[0] = 0

                    if background_y >= -1226:
                        pass
                    else:
                        if steps_dirt[1] is False:
                            steps_dirt[0].play()
                            steps_dirt[1] = True
                        else:
                            if steps_dirt[2] >= 300:
                                steps_dirt[0].play()
                                steps_dirt[2] = 0

                if pygame.key.get_pressed()[K_d]:  # бег вправо + анимация
                    character.run(4)
                    print(character.rect.x, character.direction_x)
                    anim_counter_rl[1] += 1
                    anim_counter_rl[2] = "right"

                    if anim_counter_rl[0] <= len(character.run_right) - 1 and anim_counter_rl[1] % 4 == 0:
                        character.image = character.run_right[anim_counter_rl[0]]
                        anim_counter_rl[0] += 1
                    elif anim_counter_rl[0] >= len(character.run_right):
                        anim_counter_rl[0] = 0

                    if background_y >= -1226:
                        if steps_stone[1] is False:
                            steps_stone[0].play()
                            steps_stone[1] = True
                        else:
                            if steps_stone[2] >= 300:
                                steps_stone[0].play()
                                steps_stone[2] = 0
                    else:
                        if steps_dirt[1] is False:
                            steps_dirt[0].play()
                            steps_dirt[1] = True
                        else:
                            if steps_dirt[2] >= 300:
                                steps_dirt[0].play()
                                steps_dirt[2] = 0

                if pygame.key.get_pressed()[K_s]:
                    character.lower()

                if event.type == pygame.KEYDOWN:  # прыжок
                    if event.key == pygame.K_SPACE:
                        character.jump()

                    elif event.key == pygame.K_w:
                        character.jump()

            if not character.check_death() and not dead[0] is True:  # проверка смерти после всех движений
                character.check_air()
                character.check_ground()

            if random.randint(0, 60) == 3:
                for value in blocks_dct.values():  # спавн блоков и добавление монет
                    if value[1] is False:
                        value[1] = True
                        value[0].spawn()
                        score += 1
                        coins += 1
                        clean = open('values.txt', 'w+')
                        clean.seek(0)
                        clean.close()
                        with open('values.txt', mode='r+',
                                  encoding="utf8") as values_file_w:
                            values_file_w.write(f'c={coins}\n')
                            values_file_w.write(f's={" ".join(skins)}\n')
                            values_file_w.write(f'n={n}')
                        break

            if camera.count > 46:  # передвижение камеры при выстраивании блоков в ряд
                camera.default()
            elif camera.upFlag is True and camera.count <= 46:
                camera.update()
                for sprite in fallen_blocks:
                    camera.apply(sprite)
                for sprite in ghost_blocks:
                    camera.apply(sprite)
                if background_y <= -2:
                    background_y += 1

            respawn = list()

            for value in blocks_dct.values():
                for up in blocks_dct.values():  # проверка выстраивания блоков в ряд
                    # и последующая их возможность для появления
                    if (value[1] is True and value[0].movement_flag is False and value[0].rect.centery > 758
                            and up[0].rect.centery < 758 and pygame.sprite.collide_rect(value[0], up[0])
                            and up[0].movement_flag is False):
                        respawn.append(value[0])
                        if camera.upFlag is False:
                            if value[0].rect.y != 753:
                                value[0].rect.y = 753
                            if up[0].rect.y != 706:
                                up[0].rect.y = 706

            i = 0

            if len(respawn) == 10: # блоки на респавн
                for value in blocks_dct.values():
                    if value[0] in respawn:
                        value[1] = False
                        gblocks_lst[i].replace(value[0].rect.x, value[0].rect.y, value[0].image)
                        i += 1
                        value[0].invisible()
                    camera.upFlag = True

            screen.blit(background, (0, background_y))

            all_sprites.update()
            all_sprites.draw(screen)

            f = pygame.font.Font("graphics/fonts/Silkscreen-Regular.ttf" # счётчик для монет
                                 , 20)
            coins_text = f.render(str(coins), True,
                                  (255, 255, 255))
            f2 = pygame.font.Font("graphics/fonts/Silkscreen-Regular.ttf"
                                  , 22)
            bolding = f2.render(str(coins), True,
                                (0, 0, 0))
            screen.blit(bolding, (50, 10))
            screen.blit(coins_text, (50, 10))
            if len(str(coins)) == 1:
                screen.blit(coin, (65, 15))
            elif len(str(coins)) == 2:
                screen.blit(coin, (82, 15))
            elif len(str(coins)) == 3:
                screen.blit(coin, (99, 15))
            else:
                screen.blit(coin, (116, 15))

        elif dead[0] is True and dead[1] <= 3: # анимация смерти
            if dead[2] % 10 == 0:
                character.rect.y += 70
                dead[1] += 1
            dead[2] += 1
            dead[0] = True

            screen.blit(background, (0, background_y))
            all_sprites.update()
            all_sprites.draw(screen)

            death_sound.play()
            steps_dirt[0].stop()
            steps_stone[0].stop()

        else: # экран смерти + сброс всего прогресса
            for c, value in enumerate(blocks_dct.values()):
                value[0].default()
                if c < 10:
                    value[1] = True
                else:
                    value[1] = False

            for value in blocks_dct.values():
                if value[1] is True:
                    value[0].spawn()
                    value[0].rect.y = 752
            character.rect.y = 650
            character.image = character.default_right

            background_y = -1600
            f = pygame.font.Font("graphics/fonts/Silkscreen-Regular.ttf",
                                 36)
            deadtext = f.render('R to restart', True,
                                (255, 255, 255))

            f2 = pygame.font.Font("graphics/fonts/Silkscreen-Regular.ttf",
                                  20)
            scorefinal = f2.render(f'You get +{score}', True,
                                   (255, 255, 255))
            if len(str(score)) == 1:
                screen.blit(coin, (365, 454))
                screen.blit(scorefinal, (220, 450))
            elif len(str(score)) == 2:
                screen.blit(scorefinal, (213, 450))
                screen.blit(coin, (372, 454))
            elif len(str(score)) == 1:
                screen.blit(scorefinal, (205, 450))
                screen.blit(coin, (380, 454))
            screen.blit(deadtext, (150, 400))
            camera.death()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_script = False
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        dead = [False, 0, 0]
                        score = 0
                        character.dead()

        clock.tick(60)
        pygame.display.flip()


screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
play_button, leave_button, settings_button = (load_image('menu/PLAY.png'), load_image('menu/LEAVE.png'),
                                              load_image('menu/SETTINGS.png'))

play_button_pressed, leave_button_pressed, settings_button_pressed, back_button_pressed = (
    load_image('menu/PLAY_PRESSED.png'), load_image('menu/LEAVE_PRESSED.png'),
    load_image('menu/SETTINGS_PRESSED.png'), load_image('menu/BACK_PRESSED.png'))

controls_window, sound_window, back_button = (
    load_image('menu/CONTROLS.png'), load_image('menu/ENVIROMENT.png'), load_image('menu/BACK.png'))

font = pygame.font.Font("graphics/fonts/Silkscreen-Regular.ttf"
                        , 22)
key_left = font.render('A', True, (0, 0, 0))
key_right = font.render('D', True, (0, 0, 0))
key_menu = font.render('ESC', True, (0, 0, 0))
key_jump = font.render('W', True, (0, 0, 0))

with open('volume.txt', 'r', encoding='utf8') as f: # считывание значений громкости
    for i in f.readlines():
        if 'v1' in i:
            v1 = float(i.split()[-1])
        elif 'v2' in i:
            v2 = float(i.split()[-1])

music_value = [v1, font.render(str(v1 * 1000), True, (0, 0, 0))] # их выставление
enviroment_value = [v2, font.render(str(v2), True, (0, 0, 0))]


def change_volume(k):
    global key

    key = str(k.name)
    print(key)


play_button_flag, leave_button_flag, settings_button_flag, back_button_flag = False, False, False, False
settings_window = False
key_flag = [False, '']

key = ''

while game_script:
    pygame.mixer.init()

    screen.blit(load_image("graphics/background.png"), (0, -1600))
    if settings_window is False: # меню
        if play_button_flag: # кнопки серые при наведении
            screen.blit(play_button_pressed, (55, 193))
        else:
            screen.blit(play_button, (55, 193))

        if settings_button_flag:
            screen.blit(settings_button_pressed, (55, 399))
        else:
            screen.blit(settings_button, (55, 399))

        if leave_button_flag:
            screen.blit(leave_button_pressed, (55, 606))
        else:
            screen.blit(leave_button, (55, 606))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_script = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_c, y_c = event.pos

                if 109 <= x_c <= 467:
                    if 193 <= y_c <= 269: # запуск игры
                        running = True
                        character.rect.x = 100
                        character.rect.y = 600
                        camera.default()
                        main()

                    elif 399 <= y_c <= 475:
                        settings_window = True # выход в меню настрек

                    elif 607 <= y_c <= 682: # выход из игры
                        game_script = False

            if event.type == pygame.MOUSEMOTION:
                x_m, y_m = event.pos

                if 109 <= x_m <= 467:
                    if 193 <= y_m <= 269:
                        play_button_flag = True

                    elif 399 <= y_m <= 475:
                        settings_button_flag = True

                    elif 607 <= y_m <= 682:
                        leave_button_flag = True

                    else:
                        play_button_flag, leave_button_flag, settings_button_flag = False, False, False
    else:
        if back_button_flag is True:
            screen.blit(back_button_pressed, (55, 606))
        else:
            screen.blit(back_button, (55, 606))

        screen.blit(sound_window, (112, 356))
        screen.blit(controls_window, (48, 36))

        screen.blit(key_left, (416, 143))
        screen.blit(key_right, (416, 173))
        screen.blit(key_menu, (416, 203))
        screen.blit(key_jump, (416, 233))

        screen.blit(music_value[1], (382, 421))
        screen.blit(enviroment_value[1], (382, 471))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_script = False
            if key_flag[0] is False:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_c, y_c = event.pos
                    print(event.pos)

                    if 109 <= x_c <= 467:

                        if 607 <= y_c <= 682:
                            settings_window = False

                    if 385 <= x_c <= 427:

                        if 431 <= y_c <= 443:
                            key_flag = [True, 'm']
                            key = ''

                        elif 481 <= y_c <= 493:
                            key_flag = [True, 'e']
                            key = ''
                if event.type == pygame.MOUSEMOTION:
                    x_m, y_m = event.pos

                    if 109 <= x_m <= 467:

                        if 607 <= y_m <= 682:
                            back_button_flag = True

                        else:
                            back_button_flag = False

            else: # смена громкости
                keyboard.hook(change_volume)
                if key != '':
                    if key_flag[1] == 'm':

                        try:

                            music_value[0] = int(key) / 100
                            music_value[1] = font.render(str(music_value[0] * 1000), True, (0, 0, 0))

                            with open('volume.txt', 'r', encoding='utf8') as f: # запись в данных
                                data = list()
                                for i in f.readlines():
                                    data.append(i)
                            for i in range(len(data)):
                                if 'v1' in data[i]:
                                    data[i] = f'v1 = {music_value[0]}\n'

                            with open('volume.txt', 'w', encoding='utf8') as f:
                                f.write(''.join(data))

                            key_flag = [False, '']

                        except ValueError:

                            key_flag = [False, '']
                    else:

                        try:

                            enviroment_value[0] = int(key) * 10
                            enviroment_value[1] = font.render(str(float(enviroment_value[0])), True,
                                                              (0, 0, 0))

                            with open('volume.txt', 'r', encoding='utf8') as f: # запись в данных
                                data = list()
                                for i in f.readlines():
                                    data.append(i)
                            for i in range(len(data)):
                                if 'v2' in data[i]:
                                    data[i] = f'v2 = {enviroment_value[0]}\n'

                            with open('volume.txt', 'w', encoding='utf8') as f:
                                f.write(''.join(data))

                            key_flag = [False, '']
                        except ValueError:

                            key_flag = [False, '']

    clock.tick(60)
    pygame.display.flip()
