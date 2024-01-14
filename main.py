import pygame
import os
import sys
from pygame.locals import *
import random

pygame.init()
pygame.display.set_caption('Jump to space')
size = width, height = 576, 800
running = True

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


class Hero(pygame.sprite.Sprite):
    right = load_image("graphics/animations/default/default_right.png")
    right = pygame.transform.scale(right, (32, 56))
    left = load_image("graphics/animations/default/default_left.png")
    left = pygame.transform.scale(left, (32, 56))

    run_left = [load_image("graphics/animations/left/1.png"),
                load_image("graphics/animations/left/2.png"),
                load_image("graphics/animations/left/3.png"),
                load_image("graphics/animations/left/4.png"),
                load_image("graphics/animations/left/5.png"),
                load_image("graphics/animations/left/6.png"),
                load_image("graphics/animations/left/7.png"),
                load_image("graphics/animations/left/8.png")]

    for i in range(len(run_left)):
        run_left[i] = pygame.transform.scale(run_left[i], (32, 56))

    run_right = [load_image("graphics/animations/right/1.png"),
                 load_image("graphics/animations/right/2.png"),
                 load_image("graphics/animations/right/3.png"),
                 load_image("graphics/animations/right/4.png"),
                 load_image("graphics/animations/right/5.png"),
                 load_image("graphics/animations/right/6.png"),
                 load_image("graphics/animations/right/7.png"),
                 load_image("graphics/animations/right/8.png")]

    for i in range(len(run_right)):
        run_right[i] = pygame.transform.scale(run_right[i], (32, 56))

    death = [load_image("graphics/animations/death/1.png"),
             load_image("graphics/animations/death/2.png"),
             load_image("graphics/animations/death/3.png"),
             load_image("graphics/animations/death/4.png")]

    for i in range(len(death)):
        death[i] = pygame.transform.scale(death[i], (32, 56))

    blink = [load_image("graphics/animations/blink/eyes.png"),
             load_image("graphics/animations/blink/void.png")]

    for i in range(len(blink)):
        blink[i] = pygame.transform.scale(blink[i], (32, 56))

    jumpAn = [load_image("graphics/animations/jump/1.png"),
              load_image("graphics/animations/jump/2.png"),
              load_image("graphics/animations/jump/3.png"),
              load_image("graphics/animations/jump/4.png"),
              load_image("graphics/animations/jump/5.png"),
              load_image("graphics/animations/jump/6.png"),
              load_image("graphics/animations/jump/7.png"),
              load_image("graphics/animations/jump/8.png")]

    for i in range(len(jumpAn)):
        jumpAn[i] = pygame.transform.scale(jumpAn[i], (32, 56))

    def __init__(self):
        super().__init__(all_sprites)

        self.add(hero)
        self.image = self.right

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.direction_x = 0
        self.direction_y = 1
        self.tick_jump_counter = 1
        self.jump_counter = 0

        self.moved = False
        self.jump_flag = [False, 'stand', 0]
        self.falling_flag = [False, "stand"]

        self.rect.x = 100
        self.rect.y = 600

    def run(self, nx):
        if 0 < self.rect.x + nx < 576:
            self.rect.x += nx
            self.direction_x = nx
            self.moved = True

    def jump(self):
        self.jump_counter += 1
        if self.jump_counter <= 1:
            if self.moved is True:
                if self.direction_x > 0:
                    self.jump_flag = [True, "right", 10]
                else:
                    self.jump_flag = [True, "left", 10]
            else:
                self.jump_flag = [True, "stand", 10]

    def check_air(self):
        if not pygame.sprite.spritecollideany(self,
                                              fallen_blocks) and self.rect.y + 64 != 800 and self.jump_flag[0] is False:
            self.rect.y += 3
            if self.falling_flag[0] is True:
                if self.falling_flag[1] == "right" and 48 <= self.rect.x + 3 <= 496:
                    self.rect.x += 3
                    self.direction_x = 3
                elif self.falling_flag[1] == "left" and 48 <= self.rect.x - 3 <= 496:
                    self.rect.x -= 3
                    self.direction_x = -3

            if pygame.sprite.spritecollideany(self,
                                              fallen_blocks) or self.rect.midbottom[1] == 800:
                self.rect.y -= 3
                self.jump_counter -= 1
                self.falling_flag = [False, "stand"]

        elif self.jump_flag[0] is True and self.jump_flag[1] == "stand" and self.tick_jump_counter != 10:
            self.rect.y -= self.jump_flag[2]
            self.tick_jump_counter += 1
            self.jump_flag[2] -= 1

        elif self.jump_flag[0] is True and self.jump_flag[1] == "right" and self.tick_jump_counter != 10:
            self.rect.y -= self.jump_flag[2]
            self.tick_jump_counter += 1
            self.jump_flag[2] -= 1
            self.direction_x = 3
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

    def check_ground(self):
        if self.moved is True:
            for i in fallen_blocks:
                while pygame.sprite.collide_rect(self, i):
                    if self.rect.midbottom[1] != i.rect.midtop[1] + 3:
                        self.rect.x -= self.direction_x

                    else:
                        break
            for i in blocks:
                while pygame.sprite.collide_rect(self, i):
                    if self.rect.midbottom[1] != i.rect.midtop[1] + 3:
                        self.rect.x -= self.direction_x

                    else:
                        break
            for i in walls:
                while pygame.sprite.collide_rect(self, i):
                    if self.rect.midbottom[1] != i.rect.midtop[1] + 3:
                        self.rect.x -= self.direction_x

                    else:
                        break
            self.moved = False

    def lower(self):
        self.rect.y += 1
        if pygame.sprite.spritecollideany(self, fallen_blocks) or self.rect.y + 64 != 800:
            self.rect.y -= 1

    def check_death(self):
        for i in blocks:
            if (pygame.sprite.collide_rect(self, i) and (
                    i.rect.topleft[0] <= self.rect.left <= i.rect.topright[0]
                    or i.rect.topleft[0] <= self.rect.right <= i.rect.topright[
                        0])):
                return True
            return False


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.upFlag = False
        self.count = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self):
        if self.upFlag is True and self.count <= 46:
            self.dy = 1
            self.count += 1

    def default(self):
        self.count = 0
        self.upFlag = False

    def death(self):
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

        self.rotate_angle = 0

        self.image = pygame.transform.rotate(self.grass_fallingTitle, self.rotate_angle)

        self.add(blocks)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.movement_flag = False

        self.rect.y = 900

    def update(self):
        global background_y

        for i in fallen_blocks:
            if pygame.sprite.collide_rect(self, i):
                self.add(fallen_blocks)
                self.remove(blocks)
                self.movement_flag = False
                if background_y < -1226:
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

        if background_y < -1226:
            for value in blocks_dct.values():
                if value[0].rect.y > self.rect.y and pygame.sprite.collide_rect(value[0], self):
                    value[0].image = pygame.transform.rotate(self.dirt_placedTitle, self.rotate_angle)

                elif value[0].rect.y < self.rect.y and pygame.sprite.collide_rect(value[0], self):
                    self.image = pygame.transform.rotate(self.dirt_placedTitle, self.rotate_angle)

    def spawn(self):
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

    def invisible(self):
        self.rect.y = 900

    def default(self):
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

    def replace(self, x, y, rotation, image):
        self.rect.x, self.rect.y = x, y
        self.image = pygame.transform.rotate(image, rotation)

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

        if wall_counter[0] == 0:
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

    def update(self):
        global background_y

        if background_y >= -1226:
            self.image = pygame.transform.rotate(self.spacewall, self.angle)


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
              28: [block28, False], 29: [block29, False], 30: [block30, False]}

(gblock1, gblock2, gblock3, gblock4, gblock5, gblock6, gblock7, gblock8, gblock9, gblock10) = (
    GhostBlock(), GhostBlock(), GhostBlock(), GhostBlock(), GhostBlock(), GhostBlock(), GhostBlock(), GhostBlock(),
    GhostBlock(), GhostBlock())

gblocks_lst = [gblock1, gblock2, gblock3, gblock4, gblock5, gblock6, gblock7, gblock8, gblock9, gblock10]

character = Hero()
camera = Camera()


def main():
    global running, camera, character, background_y

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    dead = [False, 0, 0]
    anim_counter_rl = [0, 0, "right"]
    score = 0
    background = load_image("graphics/background.png")

    for value in blocks_dct.values():
        if value[1] is True:
            value[0].spawn()
            value[0].rect.y = 752

    while running:
        if dead[0] is False:

            # if character.check_death() or dead[0] is True:
            #     dead[0] = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if pygame.key.get_pressed()[K_ESCAPE]:
                    paused = True
                    brightness_low = load_image("graphics/brightness_low.png")
                    brightness_low = pygame.transform.scale(brightness_low, (576, 800))
                    brightness_low = brightness_low.convert()
                    brightness_low.set_alpha(200)
                    brightness_high = load_image("graphics/brightness_high.png")
                    brightness_high = pygame.transform.scale(brightness_high, (112, 95))
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
                    left = load_image("graphics/animations/default/default_left.png")
                    last_active = load_image("graphics/textures/pause_menu/store/last_active.png")
                    last_active = pygame.transform.scale(last_active, (30, 30))
                    next_active = load_image("graphics/textures/pause_menu/store/next_active.png")
                    next_active = pygame.transform.scale(next_active, (30, 30))
                    last_inactive = load_image("graphics/textures/pause_menu/store/last_inactive.png")
                    last_inactive = pygame.transform.scale(last_inactive, (30, 30))
                    next_inactive = load_image("graphics/textures/pause_menu/store/next_inactive.png")
                    next_inactive = pygame.transform.scale(next_inactive, (30, 30))
                    left = pygame.transform.scale(left, (115, 200))
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
                    wr_is_select = 'inactive'
                    st_is_back = False
                    st_is_purchase = 'inactive'
                    st_is_next = False
                    st_is_last = False
                    while paused:
                        screen.blit(background, (0, background_y))
                        all_sprites.draw(screen)
                        screen.blit(brightness_low, (0, 0))
                        if wardrobe_open:
                            screen.blit(back, (73, 260))
                            if wr_is_back:
                                screen.blit(brightness_high1, (75, 260))
                            if wr_is1:
                                screen.blit(brightness_high, (275, 300))
                            if wr_is2:
                                screen.blit(brightness_high, (275, 396))
                            if wr_is3:
                                screen.blit(brightness_high, (275, 490))
                            if wr_is4:
                                screen.blit(brightness_high, (387, 300))
                            if wr_is5:
                                screen.blit(brightness_high, (387, 396))
                            if wr_is6:
                                screen.blit(brightness_high, (387, 490))
                            if wr_is_select == 'active':
                                screen.blit(select_active, (74, 500))
                            elif wr_is_select == 'inactive':
                                screen.blit(select_inactive, (74, 500))
                            else:
                                screen.blit(select_blocked, (74, 500))
                            screen.blit(left, (116, 300))
                            pygame.draw.rect(screen, (0, 0, 0), (275, 300, 224, 285), 2)
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()
                                if event.type == pygame.MOUSEMOTION:
                                    if wr_is_select != 'blocked':
                                        if 76 <= event.pos[0] <= 276 and 500 <= event.pos[1] <= 600:
                                            wr_is_select = 'active'
                                        else:
                                            wr_is_select = 'inactive'
                                    if 275 <= event.pos[0] <= 387 and 300 <= event.pos[1] <= 395:
                                        wr_is1 = True
                                    else:
                                        wr_is1 = False
                                    if 275 <= event.pos[0] <= 387 and 396 <= event.pos[1] <= 490:
                                        wr_is2 = True
                                    else:
                                        wr_is2 = False
                                    if 275 <= event.pos[0] <= 387 and 491 <= event.pos[1] <= 585:
                                        wr_is3 = True
                                    else:
                                        wr_is3 = False
                                    if 388 <= event.pos[0] <= 499 and 300 <= event.pos[1] <= 395:
                                        wr_is4 = True
                                    else:
                                        wr_is4 = False
                                    if 388 <= event.pos[0] <= 499 and 396 <= event.pos[1] <= 490:
                                        wr_is5 = True
                                    else:
                                        wr_is5 = False
                                    if 388 <= event.pos[0] <= 499 and 491 <= event.pos[1] <= 585:
                                        wr_is6 = True
                                    else:
                                        wr_is6 = False
                                    if 75 <= event.pos[0] <= 115 and 260 <= event.pos[1] <= 300:
                                        wr_is_back = True
                                    else:
                                        wr_is_back = False
                                if event.type == pygame.MOUSEBUTTONUP:
                                    if 76 <= event.pos[0] <= 276 and 500 <= event.pos[1] <= 600:
                                        wr_is_select = 'blocked'
                                    if 75 <= event.pos[0] <= 115 and 260 <= event.pos[1] <= 300:
                                        wardrobe_open = False

                        elif store_open:
                            screen.blit(back, (73, 260))
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

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()
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
                                if event.type == pygame.MOUSEBUTTONUP:
                                    if 75 <= event.pos[0] <= 115 and 260 <= event.pos[1] <= 300:
                                        store_open = False
                                    if 188 <= event.pos[0] <= 388 and 500 <= event.pos[1] <= 600:
                                        st_is_purchase = 'blocked'

                            # screen.blit(select_inactive, (50, 500))
                        else:
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
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()
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
                                if event.type == pygame.MOUSEBUTTONUP:
                                    if 51 <= event.pos[0] <= 151 and 350 <= event.pos[1] <= 450 and event.button == 1:
                                        paused = False
                                    elif 176 <= event.pos[0] <= 276 and 350 <= event.pos[
                                        1] <= 450 and event.button == 1:
                                        wardrobe_open = True
                                    elif 301 <= event.pos[0] <= 401 and 350 <= event.pos[
                                        1] <= 450 and event.button == 1:
                                        store_open = True
                                    elif 427 <= event.pos[0] <= 527 and 350 <= event.pos[
                                        1] <= 450 and event.button == 1:
                                        pass

                        if pygame.key.get_pressed()[K_RETURN]:
                            paused = False

                        pygame.display.update()

                if not (pygame.key.get_pressed()[K_d] or pygame.key.get_pressed()[K_a]):
                    if anim_counter_rl[2] == "right":
                        character.image = character.right
                        anim_counter_rl = [0, 0, "right"]
                    else:
                        character.image = character.left
                        anim_counter_rl = [0, 0, "left"]

                if pygame.key.get_pressed()[K_a]:
                    character.run(-4)
                    anim_counter_rl[1] += 1
                    anim_counter_rl[2] = "left"

                    if anim_counter_rl[0] <= 7 and anim_counter_rl[1] % 4 == 0:
                        character.image = character.run_left[anim_counter_rl[0]]
                        anim_counter_rl[0] += 1
                    elif anim_counter_rl[0] >= 8:
                        anim_counter_rl[0] = 0

                if pygame.key.get_pressed()[K_d]:
                    character.run(4)
                    anim_counter_rl[1] += 1
                    anim_counter_rl[2] = "right"

                    if anim_counter_rl[0] <= 7 and anim_counter_rl[1] % 4 == 0:
                        character.image = character.run_right[anim_counter_rl[0]]
                        anim_counter_rl[0] += 1
                    elif anim_counter_rl[0] >= 8:
                        anim_counter_rl[0] = 0

                if pygame.key.get_pressed()[K_s]:
                    character.lower()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        character.jump()

                    elif event.key == pygame.K_w:
                        character.jump()

            if not character.check_death() and not dead[0] is True:
                character.check_air()
                character.check_ground()

            if random.randint(0, 40) == 3:
                for value in blocks_dct.values():
                    if value[1] is False:
                        value[1] = True
                        value[0].spawn()
                        score += 1
                        break

            if camera.count > 46:
                camera.default()
            elif camera.upFlag is True and camera.count <= 46:
                camera.update()
                for sprite in fallen_blocks:
                    camera.apply(sprite)
                for sprite in ghost_blocks:
                    camera.apply(sprite)
                background_y += 1
                print(background_y)

            respawn = list()

            for value in blocks_dct.values():
                for up in blocks_dct.values():
                    if (value[1] is True and value[0].movement_flag is False and value[0].rect.centery > 758
                            and up[0].rect.centery < 758 and pygame.sprite.collide_rect(value[0], up[0])
                            and up[0].movement_flag is False):
                        respawn.append(value[0])

            i = 0

            if len(respawn) == 10:
                for value in blocks_dct.values():
                    if value[0] in respawn:
                        value[1] = False
                        gblocks_lst[i].replace(value[0].rect.x, value[0].rect.y, value[0].rotate_angle, value[0].image)
                        i += 1
                        value[0].invisible()
                    camera.upFlag = True

            screen.blit(background, (0, background_y))

            all_sprites.update()
            all_sprites.draw(screen)

            f = pygame.font.Font("graphics/fonts/Silkscreen-Regular.ttf",
                                 20)
            score_text = f.render(str(score), True,
                                  (255, 255, 255))
            screen.blit(score_text, (530, 20))

        elif dead[0] is True and dead[1] <= 3:
            if dead[2] % 10 == 0:
                character.image = character.death[dead[1]]
                dead[1] += 1
            dead[2] += 1
            dead[0] = True

            screen.blit(background, (0, background_y))
            all_sprites.update()
            all_sprites.draw(screen)

        else:
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
            score = 0
            character.image = character.right

            background_y = -1600

            f = pygame.font.Font("graphics/fonts/Silkscreen-Regular.ttf",
                                 36)
            deadtext = f.render('R to restart', True,
                                (255, 255, 255))
            screen.blit(deadtext, (150, 400))
            camera.death()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        dead = [False, 0, 0]

        clock.tick(60)
        pygame.display.flip()


if __name__ == '__main__':
    main()
