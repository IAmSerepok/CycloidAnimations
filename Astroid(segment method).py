import pygame as pg


class Astroid:
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

    def draw(self, i):

        step = self.radius/self.num_lines
        x = self.translate[0] + i * step
        y1 = self.translate[1] + abs(i) * step - self.radius
        y2 = self.translate[1] - abs(i) * step + self.radius

        pg.draw.line(self.app.screen, self.get_color(), (x, self.translate[1]), (self.translate[0], y1))
        pg.draw.line(self.app.screen, self.get_color(), (x, self.translate[1]), (self.translate[0], y2))


class App:
    def __init__(self, n_lines):
        self.screen = pg.display.set_mode([1200, 800])
        self.clock = pg.time.Clock()
        self.astroid = Astroid(self, n_lines)

    def draw(self, i):
        self.astroid.draw(i)
        pg.display.flip()

    def run(self):
        self.screen.fill('black')
        pg.draw.line(self.screen, 'blue',
                     (self.astroid.translate[0] - self.astroid.radius, self.astroid.translate[1]),
                     (self.astroid.translate[0] + self.astroid.radius, self.astroid.translate[1]), 2)
        pg.draw.line(self.screen, 'blue',
                     (self.astroid.translate[0], self.astroid.translate[1] - self.astroid.radius),
                     (self.astroid.translate[0], self.astroid.translate[1] + self.astroid.radius), 2)
        counter = 0
        i = -self.astroid.num_lines
        while True:
            if i <= int(self.astroid.num_lines):
                counter += 1
                if counter > 2:
                    counter = 0
                    self.draw(i)
                    i += 1
            for _ in pg.event.get():
                if _.type == pg.QUIT:
                    exit()
            self.clock.tick(60)


app = App(n_lines=100)
app.run()
