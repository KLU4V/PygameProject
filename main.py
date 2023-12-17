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

    def check_gorund(self):
        if self.moved is True:
            for i in fallen_blocks:
                if pygame.sprite.collide_rect(self, i):
                    self.rect.x -= self.direction_x
            self.moved = False


class Blocks(pygame.sprite.Sprite):
    image_placedTitle = load_image("placed_tile.png")
    image_placedTitle = pygame.transform.scale(image_placedTitle, (48, 48))
    image = load_image("tile.png")
    image = pygame.transform.scale(image, (48, 48))

    def __init__(self):

        super().__init__(all_sprites)

        x = random.randint(1, 10)

        self.rotate_angle = random.randint(1, 4) * 90

        self.image = pygame.transform.rotate(self.image, self.rotate_angle)
        self.image_placedTitle = pygame.transform.rotate(self.image_placedTitle, self.rotate_angle)

        self.add(blocks)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.movement_flag = False
        self.transformed = False

        while self.movement_flag is False:
            for i in blocks:
                if pygame.sprite.collide_mask(self, i):
                    self.movement_flag = True
                    self.rect.x = x * 48
            x = random.randint(1, 10)
        self.rect.y = -48

    def update(self):
        for i in fallen_blocks:
            if pygame.sprite.collide_rect(self, i):
                self.add(fallen_blocks)
                self.remove(blocks)
                self.movement_flag = False
                self.image = self.image_placedTitle

        if self.movement_flag:
            if 0 <= self.rect.y + 48 < 800:
                self.rect = self.rect.move(0, 2)

            elif self.rect.y + 48 == 800:
                self.image = self.image_placedTitle
                self.add(fallen_blocks)
                self.remove(blocks)
                self.movement_flag = False

    def coords(self):
        return [self.rect.x, self.rect.y]


character = Hero()

if __name__ == '__main__':
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
            if pygame.key.get_pressed()[K_a]:
                character.run(-4)
            if pygame.key.get_pressed()[K_d]:
                character.run(4)
        character.check_air()
        character.check_gorund()
        if random.randint(0, 40) == 3:
            block = Blocks()
        screen.fill((0, 0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        clock.tick(60)
        pygame.display.flip()
