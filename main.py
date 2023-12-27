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
hero = pygame.sprite.Group()
items = pygame.sprite.Group()
particles = pygame.sprite.Group()

possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


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
            print(nx)

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
                if self.falling_flag[1] == "right" and 0 <= self.rect.x + 3 <= 800:
                    self.rect.x += 3
                elif self.falling_flag[1] == "left" and 0 <= self.rect.x - 3 <= 800:
                    self.rect.x -= 3

            if pygame.sprite.spritecollideany(self,
                                              fallen_blocks) or self.rect.midbottom[1] == 800:
                self.rect.y -= 3
                self.jump_counter -= 1
                self.falling_flag = [False, "stand"]

        elif self.jump_flag[0] is True and self.jump_flag[1] == "stand" and self.tick_jump_counter != 10:
            self.rect.y -= self.jump_flag[2]
            self.tick_jump_counter += 1
            self.jump_flag[2] -= 1
            self.image = self.jumpAn[5]

        elif self.jump_flag[0] is True and self.jump_flag[1] == "right" and self.tick_jump_counter != 10:
            self.rect.y -= self.jump_flag[2]
            self.tick_jump_counter += 1
            self.jump_flag[2] -= 1
            self.rect.x += 3
            self.image = self.jumpAn[5]

        elif self.jump_flag[0] is True and self.jump_flag[1] == "left" and self.tick_jump_counter != 10:
            self.rect.y -= self.jump_flag[2]
            self.tick_jump_counter += 1
            self.jump_flag[2] -= 1
            self.rect.x -= 3
            self.image = self.jumpAn[5]

        elif self.tick_jump_counter == 10:
            self.tick_jump_counter = 1
            self.falling_flag = [True, self.jump_flag[1]]
            self.jump_flag = [False, 'stand', 10]

    def check_ground(self):
        if self.moved is True:
            for i in fallen_blocks:
                while pygame.sprite.collide_rect(self, i):
                    if self.rect.midbottom[1] != i.rect.midtop[1] + 1:
                        self.rect.x -= self.direction_x

                    else:
                        break
            for i in blocks:
                while pygame.sprite.collide_rect(self, i):
                    if self.rect.midbottom[1] != i.rect.midtop[1] + 1:
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
            if pygame.sprite.collide_rect(self, i) and i.rect.topleft[0] <= self.rect.centerx <= i.rect.topright[0]:
                return True
            return False


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self):
        self.dy = +47


class Block(pygame.sprite.Sprite):
    image_placedTitle = load_image("graphics/textures/placed_tile.png")
    image_placedTitle = pygame.transform.scale(image_placedTitle, (48, 48))
    image_fallingTitle = load_image("graphics/textures/tile.png")
    image_fallingTitle = pygame.transform.scale(image_fallingTitle, (48, 48))

    def __init__(self):
        super().__init__(all_sprites)

        self.rotate_angle = random.randint(1, 4) * 90

        self.image = pygame.transform.rotate(self.image_fallingTitle, self.rotate_angle)

        self.add(blocks)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.movement_flag = False

        self.rect.y = 900

    def update(self):
        for i in fallen_blocks:
            if pygame.sprite.collide_rect(self, i):
                self.add(fallen_blocks)
                self.remove(blocks)
                self.movement_flag = False
                self.image = pygame.transform.rotate(self.image_placedTitle, self.rotate_angle)

        if self.movement_flag:
            if 0 <= self.rect.y + 48 < 800:
                self.rect = self.rect.move(0, 2)

            elif self.rect.y + 48 == 800:
                self.image = pygame.transform.rotate(self.image_placedTitle, self.rotate_angle)
                self.add(fallen_blocks)
                self.remove(blocks)
                self.movement_flag = False

    def spawn(self):
        global possibilities

        self.rotate_angle = random.randint(1, 4) * 90

        self.image = pygame.transform.rotate(self.image_fallingTitle, self.rotate_angle)

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

        self.image = pygame.transform.rotate(self.image_fallingTitle, self.rotate_angle)

        self.add(blocks)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.movement_flag = False

        self.rect.y = 900


(block1, block2, block3, block4, block5, block6, block7, block8,
 block9, block10, block11, block12, block13, block14, block15, block16, block17, block18, block19, block20) = (
    Block(), Block(), Block(), Block(),
    Block(), Block(), Block(), Block(),
    Block(), Block(),
    Block(), Block(), Block(), Block(),
    Block(), Block(), Block(), Block(),
    Block(), Block())

blocks_dct = {1: [block1, True], 2: [block2, True], 3: [block3, True], 4: [block4, True], 5: [block5, True],
              6: [block6, True], 7: [block7, True], 8: [block8, True], 9: [block9, True], 10: [block10, True],
              11: [block11, False], 12: [block12, False], 13: [block13, False], 14: [block14, False],
              15: [block15, False], 16: [block16, False], 17: [block17, False], 18: [block18, False],
              19: [block19, False], 20: [block20, False]}

character = Hero()
camera = Camera()


def main():
    global running, camera, character

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    dead = [False, 0, 0]
    anim_counter_rl = [0, 0, "right"]

    for value in blocks_dct.values():
        if value[1] is True:
            value[0].spawn()
            value[0].rect.y = 752

    while running:
        if dead[0] is False:
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

            character.check_air()
            character.check_ground()

            if character.check_death() or dead[0] is True:
                dead[0] = True

            if random.randint(0, 40) == 3:
                for value in blocks_dct.values():
                    if value[1] is False:
                        value[1] = True
                        value[0].spawn()
                        break

            respawn = list()

            for value in blocks_dct.values():
                for up in blocks_dct.values():
                    if (value[1] is True and value[0].movement_flag is False and value[0].rect.centery > 758
                            and up[0].rect.centery < 758 and pygame.sprite.collide_rect(value[0], up[0])
                            and up[0].movement_flag is False):
                        respawn.append(value[0])

            if len(respawn) == 10:
                for value in blocks_dct.values():
                    if value[0] in respawn:
                        value[1] = False
                        value[0].invisible()
                    camera.update()
                for sprite in fallen_blocks:
                    camera.apply(sprite)

            screen.fill((0, 0, 0))
            all_sprites.update()
            all_sprites.draw(screen)

        elif dead[0] is True and dead[1] <= 3:
            if dead[2] % 10 == 0:
                character.image = character.death[dead[1]]
                dead[1] += 1
            dead[2] += 1
            dead[0] = True

            screen.fill((0, 0, 0))
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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        dead = [False, 0, 0]

            f = pygame.font.Font("graphics/fonts/Silkscreen-Regular.ttf"
                                 , 36)
            deadtext = f.render('R to restart', True,
                                (255, 255, 255))
            screen.blit(deadtext, (150, 400))

        clock.tick(60)
        pygame.display.flip()


if __name__ == '__main__':
    main()
