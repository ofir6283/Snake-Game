import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, x_direction=1, y_direction=0, color='chartreuse1'):
        self.pos = start
        self.x_direction = 1
        self.y_direction = 0
        self.color = color

    def move(self, dir_x, dir_y):
        self.x_direction = dir_x
        self.y_direction = dir_y
        self.pos = (self.pos[0] + self.x_direction, self.pos[1] + self.y_direction)

    def draw(self, surface, snake_eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if snake_eyes:
            center = dis // 2
            radius = 3
            circleMiddle = (i * dis + center - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, 'gray14', circleMiddle, radius)
            pygame.draw.circle(surface, 'gray14', circleMiddle2, radius)


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.direction_x = 0
        self.direction_y = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.direction_x = -1
                    self.direction_y = 0
                    self.turns[self.head.pos[:]] = [self.direction_x, self.direction_y]

                elif keys[pygame.K_RIGHT]:
                    self.direction_x = 1
                    self.direction_y = 0
                    self.turns[self.head.pos[:]] = [self.direction_x, self.direction_y]

                elif keys[pygame.K_UP]:
                    self.direction_x = 0
                    self.direction_y = -1
                    self.turns[self.head.pos[:]] = [self.direction_x, self.direction_y]

                elif keys[pygame.K_DOWN]:
                    self.direction_x = 0
                    self.direction_y = 1
                    self.turns[self.head.pos[:]] = [self.direction_x, self.direction_y]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.x_direction == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.x_direction == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.y_direction == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.y_direction == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.x_direction, c.y_direction)

    def reset_snake(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.direction_x = 0
        self.direction_y = 1

    def add_a_cube(self):
        tail = self.body[-1]
        dx, dy = tail.x_direction, tail.y_direction

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].x_direction = dx
        self.body[-1].y_direction = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def draw_grid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, 'white', (x, 0), (x, w))
        pygame.draw.line(surface, 'white', (0, y), (w, y))


def redraw_window(surface):
    global rows, width, s, apple
    surface.fill('black')
    s.draw(surface)
    apple.draw(surface)
    draw_grid(width, rows, surface)
    pygame.display.update()


def random_apple(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, apple
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = Snake('green', (10, 10))
    apple = Cube(random_apple(rows, s), color='red')
    # snack = Cube(random_apple(rows, s), color='brown1')
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == apple.pos:
            s.add_a_cube()
            apple = Cube(random_apple(rows, s), color='red')

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Reload Game?')
                s.reset_snake((10, 10))
                break

        redraw_window(win)

    pass


main()
