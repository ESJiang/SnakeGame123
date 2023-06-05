import os
import pygame
import pytz
import time

from datetime import datetime
from pygame.math import Vector2
from random import randint
from typing import List

COLOUR_BG = (175, 215, 70)
COLOUR_FRUIT = (183, 111, 122)
COLOUR_SNAKE = (126, 166, 114)
MAX_FPS = 60
CELL_SIZE, CELL_NUMBER = 30, 20
package_base_path = os.path.dirname(os.path.abspath(__file__))
pygame.init()
SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 100)
canva = pygame.display.set_mode((CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))
clock = pygame.time.Clock()

SCREEN_WIDTH = CELL_SIZE * CELL_NUMBER
SCREEN_HEIGHT = CELL_SIZE * CELL_NUMBER

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bigfont = pygame.font.Font(None, 80)
smallfont = pygame.font.Font(None, 45)


fruit_graphic = pygame.image.load(
    os.path.join("./", "Assets", "Graphics", "apple.png")
).convert_alpha()

head_up_graphic = pygame.image.load(
    os.path.join(package_base_path, "Assets", "Graphics", "head_up.png")
).convert_alpha()
head_down_graphic = pygame.image.load(
    os.path.join(package_base_path, "Assets", "Graphics", "head_down.png")
).convert_alpha()
head_right_graphic = pygame.image.load(
    os.path.join(package_base_path, "Assets", "Graphics", "head_right.png")
).convert_alpha()
head_left_graphic = pygame.image.load(
    os.path.join(package_base_path, "Assets", "Graphics", "head_left.png")
).convert_alpha()

tail_up_graphic = pygame.image.load(
    os.path.join(package_base_path, "Assets", "Graphics", "tail_up.png")
).convert_alpha()
tail_down_graphic = pygame.image.load(
    os.path.join(package_base_path, "Assets", "Graphics", "tail_down.png")
).convert_alpha()
tail_right_graphic = pygame.image.load(
    os.path.join(package_base_path, "Assets", "Graphics", "tail_right.png")
).convert_alpha()
tail_left_graphic = pygame.image.load(
    os.path.join(package_base_path, "Assets", "Graphics", "tail_left.png")
).convert_alpha()

body_vertical_graphic = pygame.image.load(
    os.path.join(package_base_path, "Assets", "Graphics", "body_vertical.png")
).convert_alpha()
body_horizontal_graphic = pygame.image.load(
    os.path.join(package_base_path, "Assets", "Graphics", "body_horizontal.png")
).convert_alpha()

body_tr_graphic = pygame.image.load(
    os.path.join(package_base_path, "Assets", "Graphics", "body_tr.png")
).convert_alpha()
body_tl_graphic = pygame.image.load(
    os.path.join(package_base_path, "Assets", "Graphics", "body_tl.png")
).convert_alpha()
body_br_graphic = pygame.image.load(
    os.path.join(package_base_path, "Assets", "Graphics", "body_br.png")
).convert_alpha()
body_bl_graphic = pygame.image.load(
    os.path.join(package_base_path, "Assets", "Graphics", "body_bl.png")
).convert_alpha()
crunch_sound_graphic = pygame.mixer.Sound(
    os.path.join(package_base_path, "Assets", "Sound", "crunch.wav")
)


class Fruit:
    def __init__(self):
        self.random_place()

    def random_place(self):
        self.x = randint(0, CELL_NUMBER - 1)
        self.y = randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

    def draw(self):
        fruit_rect = pygame.Rect(
            self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE
        )
        canva.blit(fruit_graphic, fruit_rect)


class Snake:
    def __init__(self):
        self.body: List[Vector2] = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = Vector2(1, 0)
        self.add_body = False
        self.crunch_sound_graphic = crunch_sound_graphic
        self.head_graphic = head_right_graphic
        self.tail_graphic = tail_right_graphic
        self.body_vertical_graphic = body_vertical_graphic
        self.body_horizontal_graphic = body_horizontal_graphic
        self.body_tl_graphic = body_tl_graphic
        self.body_bl_graphic = body_bl_graphic
        self.body_br_graphic = body_br_graphic
        self.body_tr_graphic = body_tr_graphic

    @property
    def head(self):
        return self.body[-1]

    @property
    def length(self):
        return len(self.body)

    def draw_score(self):
        score_text = str(self.length - 3)
        score_surface = pygame.font.Font(
            "Assets/Font/PoetsenOne-Regular.ttf", 25
        ).render(f"Count: {score_text}", True, (56, 74, 12))
        score_x = int(CELL_NUMBER * CELL_SIZE - 60)
        score_y = int(CELL_NUMBER * CELL_SIZE - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        canva.blit(score_surface, score_rect)

    def play_sound(self):
        self.crunch_sound_graphic.play()

    def draw(self):
        self.update_head_graphic()
        self.update_tail_graphic()
        for index, block in enumerate(self.body):
            block_rect = pygame.Rect(
                block.x * CELL_SIZE, block.y * CELL_SIZE, CELL_SIZE, CELL_SIZE
            )
            if index == 0:
                canva.blit(self.tail_graphic, block_rect)
            elif index == self.length - 1:
                canva.blit(self.head_graphic, block_rect)
            else:
                prev_block = self.body[index - 1] - block
                next_block = self.body[index + 1] - block
                if prev_block.x == next_block.x:
                    canva.blit(self.body_vertical_graphic, block_rect)
                elif prev_block.y == next_block.y:
                    canva.blit(self.body_horizontal_graphic, block_rect)
                else:
                    if (
                        prev_block.x == -1
                        and next_block.y == -1
                        or prev_block.y == -1
                        and next_block.x == -1
                    ):
                        canva.blit(self.body_tl_graphic, block_rect)
                    elif (
                        prev_block.x == -1
                        and next_block.y == 1
                        or prev_block.y == 1
                        and next_block.x == -1
                    ):
                        canva.blit(self.body_bl_graphic, block_rect)
                    elif (
                        prev_block.x == 1
                        and next_block.y == -1
                        or prev_block.y == -1
                        and next_block.x == 1
                    ):
                        canva.blit(self.body_tr_graphic, block_rect)
                    elif (
                        prev_block.x == 1
                        and next_block.y == 1
                        or prev_block.y == 1
                        and next_block.x == 1
                    ):
                        canva.blit(self.body_br_graphic, block_rect)
                # pygame.draw.rect(canva, COLOUR_SNAKE, block_rect)

    def update_tail_graphic(self):
        tail_relation = self.body[1] - self.body[0]
        if tail_relation == Vector2(1, 0):
            self.tail_graphic = tail_left_graphic
        elif tail_relation == Vector2(-1, 0):
            self.tail_graphic = tail_right_graphic
        elif tail_relation == Vector2(0, 1):
            self.tail_graphic = tail_up_graphic
        else:
            self.tail_graphic = tail_down_graphic

    def update_head_graphic(self):
        if self.direction == Vector2(1, 0):
            self.head_graphic = head_right_graphic
        elif self.direction == Vector2(-1, 0):
            self.head_graphic = head_left_graphic
        elif self.direction == Vector2(0, 1):
            self.head_graphic = head_down_graphic
        else:
            self.head_graphic = head_up_graphic

    def move(self):
        new_head = self.head + self.direction
        if not self.add_body:
            new_body = self.body[1:]
            new_body.append(new_head)
            self.body = new_body[:]
        else:
            self.body.append(new_head)
            self.add_body = False

    def grow(self):
        self.add_body = True


class SnakeGame:
    def __init__(self):
        self.fruit = Fruit()
        self.snake = Snake()

    def draw(self):
        # self.snake.play_sound()
        self.snake.draw_score()
        self.fruit.draw()
        self.snake.draw()

    def update(self):
        self.snake.move()
        self.check_eat()
        self.check_fail()

    def check_eat(self):
        if self.fruit.pos == self.snake.head:
            # 蛇变长了一节
            self.snake.grow()
            # 水果被重新摆放
            self.fruit.random_place()

    def check_fail(self):
        # 蛇头有没有撞墙
        if (
            not 0 <= self.snake.head.x < CELL_NUMBER
            or not 0 <= self.snake.head.y < CELL_NUMBER
        ):
            self.game_over()
        else:
            # 蛇头有没有撞到自己
            for block in self.snake.body[:-1]:
                if block == self.snake.head:
                    self.game_over()

    def game_over(self):
        # 游戏结束后的处理细节 - 可以更新一个game_over page.
        Gameover_font = pygame.font.SysFont("skia", 40, bold=True, italic=True)
        Gameover_color = Gameover_font.render(
            "Game Over", True, pygame.Color(153, 0, 0)
        )
        Gameover_location = Gameover_color.get_rect()
        Gameover_location.midtop = (int(CELL_SIZE * CELL_NUMBER / 2), 20)
        canva.blit(Gameover_color, Gameover_location)
        pygame.display.flip()
        time.sleep(0.5)
        while True:
            welcome("Restart")
            new_game()
        # pygame.quit()
        # sys.exit()


# pygame.mixer.pre_init(44100, -16, 2, 512)


def welcome(s):
    text = bigfont.render(s, 20, (0, 0, 0))  # type: ignore
    textx = SCREEN_WIDTH / 2 - text.get_width() / 2
    texty = SCREEN_HEIGHT / 2 - text.get_height() / 2
    textx_size = text.get_width()
    texty_size = text.get_height()
    pygame.draw.rect(
        screen,
        (255, 255, 0),
        ((textx - 5, texty - 5), (textx_size + 10, texty_size + 10)),
    )

    screen.blit(
        text,
        (
            SCREEN_WIDTH / 2 - text.get_width() / 2,
            SCREEN_HEIGHT / 2 - text.get_height() / 2,
        ),
    )

    clock = pygame.time.Clock()
    pygame.display.flip()
    in_main_menu = True
    while in_main_menu:
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_main_menu = False
                pygame.display.quit()
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if x >= textx - 5 and x <= textx + textx_size + 5:
                    if y >= texty - 5 and y <= texty + texty_size + 5:
                        in_main_menu = False
                        break


def new_game():
    snake_game = SnakeGame()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                snake_game.game_over()
            if event.type == SNAKE_UPDATE:
                snake_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # 蛇的前进方向是向下, 不改变其前进方向; 其他情况改变前进方向为向上
                    if snake_game.snake.direction != Vector2(0, 1):
                        snake_game.snake.direction = Vector2(0, -1)
                elif event.key == pygame.K_DOWN:
                    # 蛇的前进方向是向上, 不改变其前进方向; 其他情况改变前进方向为向下
                    if snake_game.snake.direction != Vector2(0, -1):
                        snake_game.snake.direction = Vector2(0, 1)
                elif event.key == pygame.K_LEFT:
                    # 蛇的前进方向是向右, 不改变其前进方向; 其他情况改变前进方向为向左
                    if snake_game.snake.direction != Vector2(1, 0):
                        snake_game.snake.direction = Vector2(-1, 0)
                else:
                    # 蛇的前进方向是向左, 不改变其前进方向; 其他情况改变前进方向为向右
                    if snake_game.snake.direction != Vector2(-1, 0):
                        snake_game.snake.direction = Vector2(1, 0)
        pygame.display.set_caption(
            f'PYGAME & {datetime.now(pytz.timezone("Australia/Melbourne")).strftime("%H:%M:%S")}'
        )
        canva.fill(COLOUR_BG)
        snake_game.draw()
        pygame.display.update()
        clock.tick(MAX_FPS)


screen.fill((0, 191, 255))
welcome("Start_Game")
new_game()
