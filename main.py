import pygame
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
    return image


class Hero(pygame.sprite.Sprite):
    image = load_image("hero.png")

    def __init__(self):
        super().__init__(all_sprites)

        self.add(hero)

    def update(self):
        pass


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


if __name__ == '__main__':
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if random.randint(0, 40) == 3:
            block = Blocks()
        screen.fill((0, 0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        clock.tick(200)
        pygame.display.flip()
