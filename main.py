import pygame
import random

pygame.init()
pygame.display.set_caption('Jump to space')
size = width, height = 576, 800
running = True

blocks = pygame.sprite.Group()
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
        self.add(blocks)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        flag = True
        while flag:
            self.rect.x = random.randint(1, 10) * 48
            for i in blocks:
                if pygame.sprite.collide_rect(self, i):
                    flag = False
                else:
                    flag = True
        self.rect.y = 0

    def update(self):
        if 0 <= self.rect.y + 48 < 800:
            self.rect = self.rect.move(0, 2)

        elif self.rect.y + 48 == 800:
            self.image = self.image_placedTitle


if __name__ == '__main__':
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if random.randint(0, 50) == 3:
            block = Blocks()
        screen.fill((0, 0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        clock.tick(60)
        pygame.display.flip()
