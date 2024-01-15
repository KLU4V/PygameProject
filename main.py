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
        if 0 < self.rect.x + nx < 576 and self.moved is not True:
            self.rect.x += nx
            self.direction_x = nx
            self.moved = True

    def jump(self):
        self.jump_counter += 1
        if -1 < self.jump_counter <= 1 and self.jump_flag[1] is not True:
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
                    if self.rect.midbottom[1] != i.rect.midtop[1] + 4:
                        self.rect.x -= self.direction_x

                    else:
                        break
            for i in blocks:
                while pygame.sprite.collide_rect(self, i):
                    if self.rect.midbottom[1] != i.rect.midtop[1] + 4:
                        self.rect.x -= self.direction_x

                    else:
                        break
            for i in walls:
                while pygame.sprite.collide_rect(self, i):
                    if self.rect.midbottom[1] != i.rect.midtop[1] + 4:
                        self.rect.x -= self.direction_x

                    else:
                        break
            self.moved = False

    def lower(self):
        self.rect.y += 1
        if pygame.sprite.spritecollideany(self, fallen_blocks) or self.rect.y + 64 != 800:
            self.rect.y -= 1

    def check_death(self):
        # for i in blocks:
        #     if ((i.rect.topleft[0] <= self.rect.left <= i.rect.topright[0]
        #             or i.rect.topleft[0] <= self.rect.right <= i.rect.topright[0])
        #             and pygame.sprite.collide_rect(self, i) and i.rect.midbottom[1] <= self.rect.midtop[1]):
        if pygame.sprite.spritecollideany(self, blocks):
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

    def replace(self, x, y, image):
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

            if character.check_death() or dead[0] is True:
                dead[0] = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

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

                if character.check_death() or dead[0] is True:
                    dead[0] = True

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
                if background_y <= -2:
                    background_y += 1

            respawn = list()

            for value in blocks_dct.values():
                for up in blocks_dct.values():
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

            if len(respawn) == 10:
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

            f = pygame.font.Font("graphics/fonts/Silkscreen-Regular.ttf"
                                 , 20)
            score_text = f.render(str(score), True,
                                  (255, 255, 255))
            f2 = pygame.font.Font("graphics/fonts/Silkscreen-Regular.ttf"
                                  , 22)
            bolding = f2.render(str(score), True,
                                (0, 0, 0))
            screen.blit(bolding, (270, 20))
            screen.blit(score_text, (270, 20))

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
            character.image = character.right

            background_y = -1600

            f = pygame.font.Font("graphics/fonts/Silkscreen-Regular.ttf"
                                 , 36)
            deadtext = f.render('R to restart', True,
                                (255, 255, 255))
            screen.blit(deadtext, (150, 400))

            score = 0

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
