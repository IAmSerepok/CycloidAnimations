import pygame
import math


def get_pos(center_, radius_, angle_):
    x = center_[0] + radius_ * math.cos(math.radians(angle_) - math.pi / 2)
    y = center_[1] + radius_ * math.sin(math.radians(angle_) - math.pi / 2)
    return x, y


class BigCircle:

    def __init__(self, app_, center_, radius_, angle_):

        self.center = center_
        self.app = app_
        self.radius = radius_
        self.angle = angle_

    def draw(self):
        pygame.draw.circle(self.app.surface, 'gray', self.center, self.radius, 2)

    def update(self, delta):
        self.angle = (self.angle + delta) % 360


class SmallCircle:

    def __init__(self, app_, center_, radius_, angle_, length_):

        self.center = center_
        self.length = length_
        self.app = app_
        self.radius = radius_
        self.angle = angle_
        self.poses = set()

    def draw(self):
        pygame.draw.circle(self.app.surface, 'gray', self.center, self.radius, 2)
        pygame.draw.line(self.app.surface, 'red', self.center, get_pos(self.center, self.length, self.angle), 2)

    def update(self, delta):

        pos = get_pos(self.center, self.length, self.angle)
        self.poses.add(pos)
        r = self.radius + self.app.big_circle.radius
        self.center = get_pos(self.app.center, r, self.app.big_circle.angle)
        self.angle = (self.angle + self.app.big_circle.radius * delta / self.radius + delta) % 360


class App:

    def __init__(self, radius_static, radius_move, distance):

        pygame.init()
        self.FPS = 60
        self.screen_width = 1200
        self.screen_height = 800
        self.surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        self.dot_list = set()
        self.center = (self.screen_width//2, self.screen_height//2)
        self.big_circle = BigCircle(self, self.center, radius_static, 0)
        self.small_circle = SmallCircle(self, get_pos(self.center, radius_static + radius_move, 0),
                                        radius_move, 180, distance)

    def update(self, delta):
        self.big_circle.update(delta)
        self.small_circle.update(delta)

    def draw_dots(self):
        for pos in self.small_circle.poses:
            pygame.draw.circle(self.surface, 'red', pos, 2)

    def run(self):

        while True:

            self.surface.fill('black')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            for _ in range(5):
                self.update(0.2)
            self.big_circle.draw()
            self.small_circle.draw()
            self.draw_dots()

            pygame.display.flip()
            self.clock.tick(self.FPS)


radius_move_, k = 50, 2
app = App(radius_static=k*radius_move_, radius_move=radius_move_, distance=radius_move_*(1+k))
app.run()
