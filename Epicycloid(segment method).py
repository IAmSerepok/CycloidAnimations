import pygame as pg
import math


class Cardioid:
    def __init__(self, app_, n_lines):
        self.app = app_
        self.radius = 300
        self.num_lines = n_lines
        self.translate = self.app.screen.get_width() // 2, self.app.screen.get_height() // 2
        self.counter, self.inc = 0, 0.01

    def get_color(self):
        self.counter += self.inc
        self.counter, self.inc = (self.counter, self.inc) if 0 < self.counter < 1 else (
            max(min(self.counter, 1), 0), -self.inc)

        return pg.Color('red').lerp('green', self.counter)

    def draw(self, i, k):

        theta = (2 * math.pi / self.num_lines) * i
        x1 = int(self.radius * math.cos(theta)) + self.translate[0]
        y1 = int(self.radius * math.sin(theta)) + self.translate[1]

        x2 = int(self.radius * math.cos(k * theta)) + self.translate[0]
        y2 = int(self.radius * math.sin(k * theta)) + self.translate[1]

        pg.draw.line(self.app.screen, self.get_color(), (x1, y1), (x2, y2))


class App:
    def __init__(self, n_lines):
        self.screen = pg.display.set_mode([1200, 800])
        self.clock = pg.time.Clock()
        self.cardioid = Cardioid(self, n_lines)

    def draw(self, i, k):
        self.cardioid.draw(i, k)
        pg.display.flip()

    def run(self, k):
        self.screen.fill('black')
        pg.draw.circle(self.screen, 'blue',
                       self.cardioid.translate, self.cardioid.radius, 2)
        counter = 0
        i = 0
        while True:
            if i < int(self.cardioid.num_lines):
                counter += 1
                if counter > 2:
                    counter = 0
                    self.draw(i, k)
                    i += 1
            for _ in pg.event.get():
                if _.type == pg.QUIT:
                    exit()
            self.clock.tick(60)


app = App(n_lines=200)
app.run(k=4)
#нужно улучшить для дробного k_number
