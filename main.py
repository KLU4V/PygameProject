import pygame

a = 'aaa'
pygame.init()
pygame.display.set_caption('Движущийся круг 2')
size = width, height = 600, 600
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

    def __init__(self):
        super().__init__(all_sprites)

        self.add(blocks)

    def update(self):
        pass


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Движущийся круг 2')
    size = width, height = 600, 600
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(60)
        pygame.display.flip()
