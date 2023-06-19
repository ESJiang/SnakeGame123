import os
import pygame
import sys
import time

from pygame.math import Vector2
from random import randint
from typing import List

COLOUR_BG = (175, 215, 70)
COLOUR_FRUIT = (183, 111, 122)
COLOUR_SNAKE = (126, 166, 114)
SNAKE_UPDATE = pygame.USEREVENT
MAX_FPS, CELL_SIZE, CELL_NUMBER = 60, 30, 20
package_base_path = os.path.dirname(os.path.abspath(__file__))
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.time.set_timer(SNAKE_UPDATE, 100)
canva = pygame.display.set_mode((CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))
clock = pygame.time.Clock()
SCREEN_WIDTH = CELL_SIZE * CELL_NUMBER
SCREEN_HEIGHT = CELL_SIZE * CELL_NUMBER
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((0, 191, 255))

fruit_graphic = pygame.image.load(
    os.path.join(package_base_path, "Assets", "Graphics", "apple.png")
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
        canva.blit(
            fruit_graphic,
            pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )


class Snake:
    def __init__(self):
        self.body: List[Vector2] = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = Vector2(0, 0)
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
    def tail(self):
        return self.body[0]

    @property
    def length(self):
        return len(self.body)

    def draw_score(self):
        score_surface = pygame.font.Font(
            os.path.join(package_base_path, "Assets", "Font", "PoetsenOne-Regular.ttf"),
            25,
        ).render(f"Count: {str(self.length - 3)}", True, (56, 74, 12))
        score_rect = score_surface.get_rect(
            center=(
                int(CELL_NUMBER * CELL_SIZE - 60),
                int(CELL_NUMBER * CELL_SIZE - 40),
            )
        )
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

    def update_tail_graphic(self):
        tail_direction = self.body[1] - self.tail
        if tail_direction == Vector2(1, 0):
            self.tail_graphic = tail_left_graphic
        elif tail_direction == Vector2(-1, 0):
            self.tail_graphic = tail_right_graphic
        elif tail_direction == Vector2(0, 1):
            self.tail_graphic = tail_up_graphic
        else:
            self.tail_graphic = tail_down_graphic

    def update_head_graphic(self):
        head_direction = self.head - self.body[-2]
        if head_direction == Vector2(1, 0):
            self.head_graphic = head_right_graphic
        elif head_direction == Vector2(-1, 0):
            self.head_graphic = head_left_graphic
        elif head_direction == Vector2(0, 1):
            self.head_graphic = head_down_graphic
        else:
            self.head_graphic = head_up_graphic

    def move(self):
        if self.add_body:
            self.body.append(self.head + self.direction)
            self.add_body = False
        else:
            self.body = (
                self.body[1:] + [self.head + self.direction]
                if self.direction != Vector2(0, 0)
                else self.body
            )

    def grow(self):
        self.add_body = True


class SnakeGame:
    def __init__(self):
        self.fruit = Fruit()
        self.snake = Snake()

    def draw(self):
        self.snake.draw_score()
        self.fruit.draw()
        self.snake.draw()

    def update(self):
        self.snake.move()
        self.check_eat()
        self.check_fail()

    def check_eat(self):
        if self.fruit.pos == self.snake.head:
            self.snake.play_sound()
            self.snake.grow()
            self.fruit.random_place()
        elif self.fruit.pos in self.snake.body:
            self.fruit.random_place()

    def check_fail(self):
        if (
            not 0 <= self.snake.head.x < CELL_NUMBER
            or not 0 <= self.snake.head.y < CELL_NUMBER
        ):
            self.game_over()
        elif self.snake.head in self.snake.body[:-1]:
            self.game_over()

    def game_over(self):
        gameover_color = pygame.font.SysFont("skia", 40, bold=True, italic=True).render(
            "Game Over", True, pygame.Color(153, 0, 0)
        )
        gameover_location = gameover_color.get_rect(
            midtop=(int(CELL_SIZE * CELL_NUMBER / 2), 20)
        )
        canva.blit(gameover_color, gameover_location)
        pygame.display.flip()
        while True:
            welcome("Restart")
            new_game()


def welcome(msg):
    text = pygame.font.Font(None, 80).render(msg, True, (0, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    text_rect.inflate_ip(10, 10)
    pygame.draw.rect(screen, (255, 255, 0), text_rect)
    screen.blit(text, text_rect)
    pygame.display.flip()

    while True:
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if text_rect.collidepoint(event.pos):
                    return


def new_game():
    snake_game = SnakeGame()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                snake_game.game_over()
            elif event.type == SNAKE_UPDATE:
                snake_game.update()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_game.snake.direction != Vector2(
                    0, 1
                ):
                    snake_game.snake.direction = Vector2(0, -1)
                elif (
                    event.key == pygame.K_DOWN
                    and snake_game.snake.direction != Vector2(0, -1)
                ):
                    snake_game.snake.direction = Vector2(0, 1)
                elif (
                    event.key == pygame.K_LEFT
                    and snake_game.snake.direction != Vector2(1, 0)
                    and snake_game.snake.direction != Vector2(0, 0)
                ):
                    snake_game.snake.direction = Vector2(-1, 0)
                elif (
                    event.key == pygame.K_RIGHT
                    and snake_game.snake.direction != Vector2(-1, 0)
                ):
                    snake_game.snake.direction = Vector2(1, 0)
        pygame.display.set_caption(f"PYGAME {time.ctime()[11:19]}")
        canva.fill(COLOUR_BG)
        snake_game.draw()
        pygame.display.update()
        clock.tick(MAX_FPS)


welcome("Start_Game")
new_game()
