import pygame
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
    image = pygame.image.load(name)
    image = pygame.transform.scale(image, (36, 64))
    return image


class Hero(pygame.sprite.Sprite):
    image = load_image("hero_copy.png")

    def __init__(self):
        super().__init__(all_sprites)

        self.add(hero)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.direction_x = 0
        self.direction_y = 1
        self.moved = False
        self.tick_jump_counter = 1
        self.jump_flag = False

        self.rect.x = 100
        self.rect.y = 600

    def run(self, nx):
        if 0 < self.rect.x + nx < 576:
            self.rect.x += nx
            self.direction_x = nx
            self.moved = True

    def jump(self):
        self.rect.y -= 5
        self.jump_flag = True

    def check_air(self):
        if not pygame.sprite.spritecollideany(self,
                                              fallen_blocks) and self.rect.y + 64 != 800 and self.jump_flag is False:
            self.rect.y += 1

        elif self.jump_flag is True and self.tick_jump_counter != 8:
            self.rect.y -= 5
            self.tick_jump_counter += 1

        elif self.tick_jump_counter == 8:
            self.tick_jump_counter = 1
            self.jump_flag = False

    def check_ground(self):
        if self.moved is True:
            for i in fallen_blocks:
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
            if (i.rect.midbottom[1] != self.rect.midtop[1] + 1 and pygame.sprite.collide_rect(self, i)
                    and i.rect.x <= self.rect.x <= i.rect.x):
                return True
            return False

    # def check_blocks(self):
    #     for i in blocks:
    #         while pygame.sprite.collide_rect(self, i):
    #             if (not i.rect.midbottom[1] != self.rect.midtop[1] + 1 and not i.rect.x <= self.rect.x <= i.rect.x
    #                     and self.rect.midbottom[1] != i.rect.midtop[1] + 1 and pygame.sprite.collide_rect(self, i)):
    #                 self.rect.x -= self.direction_x
    #             else:
    #                 break


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
    image_placedTitle = load_image("placed_tile.png")
    image_placedTitle = pygame.transform.scale(image_placedTitle, (48, 48))
    image_fallingTitle = load_image("tile.png")
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

for value in blocks_dct.values():
    if value[1] is True:
        value[0].spawn()
        value[0].rect.y = 730


def main():
    global running, camera, character

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    character.jump()
                if event.key == pygame.K_w:
                    character.jump()
                character.check_ground()
            if pygame.key.get_pressed()[K_a]:
                character.run(-4)
            if pygame.key.get_pressed()[K_d]:
                character.run(4)
            if pygame.key.get_pressed()[K_s]:
                character.lower()
        character.check_air()
        character.check_ground()
        character.check_death()
        # character.check_blocks()

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
        clock.tick(60)
        pygame.display.flip()


if __name__ == '__main__':
    main()
