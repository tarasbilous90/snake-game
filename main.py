import random
import pygame

pygame.init()  # pygame modules initialization

# Constants declaring
ICON_IMG = pygame.image.load("res/game_icon.png")
FONT = pygame.font.Font("res/CherryBombOne-Regular.ttf", 32)
GREEN = 0, 150, 50
WHITE = 255, 255, 255
FONT_COLOR = 225, 225, 0
TICK_EVENT = pygame.USEREVENT + 1
SPRITE_SIZE = 32
DIS_WIDTH = 320
DIS_HEIGHT = 320
# Window setup
screen = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption("Snake")
pygame.display.set_icon(ICON_IMG)
# Runtime and timing
clock = pygame.time.Clock()
running = True
pygame.time.set_timer(TICK_EVENT, 800)

# Class is created for debugging purposes. Call class method in main game loop
class Debug:
    @staticmethod
    def draw_grid():
        for i in range(0, DIS_WIDTH, SPRITE_SIZE):
            pygame.draw.line(screen, WHITE, [i, 0], [i, DIS_HEIGHT])
            pygame.draw.line(screen, WHITE, [0, i], [DIS_WIDTH, i])

# Sprite is derived class from pygame.sprite.Sprite class. For more information visit https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()


class Background:
    grass_img = pygame.image.load("res/grass.png")
    flower_img = pygame.image.load("res/flower.png")
    rocks_img = pygame.image.load("res/rocks.png")
    tile_map = list()
    population = [grass_img, flower_img, rocks_img]
    weights = [0.6, 0.1, 0.02]

    def __init__(self):
        # generating background tile map using random.choices method. For more information visit https://docs.python.org/3/library/random.html
        for x in range(0, DIS_WIDTH, SPRITE_SIZE):
            for y in range(0, DIS_HEIGHT, SPRITE_SIZE):
                tile = random.choices(self.population, self.weights)[0]
                self.tile_map.append((tile, x, y))

    def draw(self):
        screen.fill(GREEN)  # filling screen area with green color
        # rendering generated tile map to screen
        for i in range(len(self.tile_map)):
            screen.blit(self.tile_map[i][0], (self.tile_map[i][1], self.tile_map[i][2]))


class Snake:
    snake_head_img = pygame.image.load("res/snake_head.png")
    snake_tail_img = pygame.image.load("res/snake_tail.png")
    snake_body_img = pygame.image.load("res/snake_body.png")
    snake_body_bottom_right_img = pygame.image.load("res/snake_body_bottom_right.png")
    snake_body_bottom_left_img = pygame.image.load("res/snake_body_bottom_left.png")
    snake_body_top_right_img = pygame.image.load("res/snake_body_top_right.png")
    snake_body_top_left_img = pygame.image.load("res/snake_body_top_left.png")
    snake_parts = pygame.sprite.Group()
    snake_sprites = None
    direction = "up"
    snake_parts_rect = list()
    posX = 0
    posY = 0
    angle = 0
    score = 0

    def __init__(self, x, y, length=1):
        self.posX = x
        self.posY = y
        self.snake_parts.add(Sprite("res/snake_head.png"))
        self.snake_parts_rect.append((self.posX, self.posY + (SPRITE_SIZE + (SPRITE_SIZE * length)), self.angle))
        for i in reversed(range(1, length + 1)):
            self.snake_parts.add(Sprite("res/snake_body.png"))
            self.snake_parts_rect.append((self.posX, self.posY + (SPRITE_SIZE * i), self.angle))
        self.snake_parts.add(Sprite("res/snake_tail.png"))
        self.snake_sprites = self.snake_parts.sprites()
        self.snake_parts_rect.append((self.posX, self.posY, self.angle))

    def grow(self):
        self.snake_parts.add(Sprite("res/snake_body.png"))
        self.snake_sprites = self.snake_parts.sprites()
        self.snake_sprites[- 1].rect.x = -SPRITE_SIZE
        self.snake_sprites[- 1].rect.y = -SPRITE_SIZE
        self.score += 100

    def score_to_text(self):
        null_str = "00000"
        return null_str[len(str(self.score)) - 1:] + str(self.score)

    def display(self):
        self.snake_parts.update()
        self.snake_parts.draw(screen)

    def move(self):
        if self.direction == "up":
            self.posY -= SPRITE_SIZE
            self.angle = 0
            self.snake_parts_rect.append((self.posX, self.posY, self.angle))
        if self.direction == "left":
            self.angle = 90
            self.posX -= SPRITE_SIZE
            self.snake_parts_rect.append((self.posX, self.posY, self.angle))
        if self.direction == "right":
            self.angle = -90
            self.posX += SPRITE_SIZE
            self.snake_parts_rect.append((self.posX, self.posY, self.angle))
        if self.direction == "down":
            self.angle = 180
            self.posY += SPRITE_SIZE
            self.snake_parts_rect.append((self.posX, self.posY, self.angle))

        for i in range(1, len(self.snake_sprites) + 1):
            if not self.collision_check():
                self.snake_sprites[i - 1].rect.x = self.snake_parts_rect[-i][0]
                self.snake_sprites[i - 1].rect.y = self.snake_parts_rect[-i][1]
                if i == len(self.snake_sprites):
                    self.snake_sprites[i - 1].image = self.snake_tail_img
                    self.snake_sprites[i - 1].image = pygame.transform.rotate(self.snake_sprites[i - 1].image,
                                                                              self.snake_parts_rect[-i + 1][2])
                elif i == 1:
                    self.snake_sprites[i - 1].image = self.snake_head_img
                    self.snake_sprites[i - 1].image = pygame.transform.rotate(self.snake_sprites[i - 1].image,
                                                                              self.snake_parts_rect[-i][2])
                else:
                    if self.snake_parts_rect[-i][2] == self.snake_parts_rect[-i + 1][2]:
                        self.snake_sprites[i - 1].image = self.snake_body_img
                        self.snake_sprites[i - 1].image = pygame.transform.rotate(self.snake_sprites[i - 1].image,
                                                                                  self.snake_parts_rect[-i][2])
                    elif self.snake_parts_rect[-i][2] == 0 and self.snake_parts_rect[-i + 1][2] == -90 or \
                            self.snake_parts_rect[-i][2] == 90 and self.snake_parts_rect[-i + 1][2] == 180:
                        self.snake_sprites[i - 1].image = self.snake_body_bottom_right_img
                    elif self.snake_parts_rect[-i][2] == 0 and self.snake_parts_rect[-i + 1][2] == 90 or \
                            self.snake_parts_rect[-i][2] == -90 and self.snake_parts_rect[-i + 1][2] == 180:
                        self.snake_sprites[i - 1].image = self.snake_body_bottom_left_img
                    elif self.snake_parts_rect[-i][2] == 90 and self.snake_parts_rect[-i + 1][2] == 0 or \
                            self.snake_parts_rect[-i][2] == 180 and self.snake_parts_rect[-i + 1][2] == -90:
                        self.snake_sprites[i - 1].image = self.snake_body_top_right_img
                    elif self.snake_parts_rect[-i][2] == -90 and self.snake_parts_rect[-i + 1][2] == 0 or \
                            self.snake_parts_rect[-i][2] == 180 and self.snake_parts_rect[-i + 1][2] == 90:
                        self.snake_sprites[i - 1].image = self.snake_body_top_left_img

    def collision_check(self):
        for i in range(2, len(self.snake_sprites) + 1):
            if self.snake_parts_rect[-1][0] < 0 or self.snake_parts_rect[-1][0] >= DIS_WIDTH or \
                    self.snake_parts_rect[-1][1] < 0 or self.snake_parts_rect[-1][1] >= DIS_HEIGHT:
                return True
            elif self.snake_parts_rect[-1][0] == self.snake_parts_rect[-i][0] and self.snake_parts_rect[-1][1] == \
                    self.snake_parts_rect[-i][1]:
                return True
        return False


class Food:
    food_img = pygame.image.load("res/food.png")
    food_rect = food_img.get_rect()

    def __init__(self):

        self.food_rect.x = random.randrange(0, DIS_WIDTH, SPRITE_SIZE)
        self.food_rect.y = random.randrange(0, DIS_HEIGHT, SPRITE_SIZE)

    def spawn(self):
        points = list()
        excluded_points = list()
        for x in range(0, DIS_WIDTH, SPRITE_SIZE):
            for y in range(0, DIS_HEIGHT, SPRITE_SIZE):
                points.append((x, y))
        for i in range(1, len(snake.snake_sprites) + 1):
            excluded_points.append((snake.snake_parts_rect[-i][0], snake.snake_parts_rect[-i][1]))
        for i in range(len(excluded_points)):
            points.remove(excluded_points[i])
        rand_point = random.choice(points)
        self.food_rect.x = rand_point[0]
        self.food_rect.y = rand_point[1]

    def draw(self):
        screen.blit(self.food_img, (self.food_rect.x, self.food_rect.y))


background = Background()
snake = Snake(DIS_WIDTH / 2, DIS_HEIGHT / 2)
snake.move()
food = Food()
food.spawn()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake.direction != "right":
                snake.direction = "left"
            elif event.key == pygame.K_UP and snake.direction != "down":
                snake.direction = "up"
            elif event.key == pygame.K_RIGHT and snake.direction != "left":
                snake.direction = "right"
            elif event.key == pygame.K_DOWN and snake.direction != "up":
                snake.direction = "down"
        if not snake.collision_check() and event.type == TICK_EVENT:
            snake.move()
            if snake.snake_sprites[0].rect.x == food.food_rect.x and snake.snake_sprites[0].rect.y == food.food_rect.y:
                snake.grow()
                food.spawn()
        background.draw()
        snake.display()
        food.draw()
        score_text = FONT.render(snake.score_to_text(), True, FONT_COLOR)
        score_text_rect = score_text.get_rect()
        screen.blit(score_text, (DIS_WIDTH - score_text_rect.width - 5, -5))
        if snake.collision_check():
            game_over_text = FONT.render("Game Over", True, FONT_COLOR)
            game_over_text_rect = game_over_text.get_rect()
            screen.blit(game_over_text, (
                (DIS_WIDTH / 2) - (game_over_text_rect.width / 2), (DIS_HEIGHT / 2) - (game_over_text_rect.height / 2)))
            if event.type == pygame.KEYDOWN:
                running = False
        pygame.display.flip()
        clock.tick(30)
pygame.quit()
