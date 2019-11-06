import matplotlib.pyplot as plt
from utils import Point

class Plane():
    def __init__(self, points, hull,*args, **kwargs):
        self.points = points
        self.hull = hull

        self.min = Point(min([pnt.x for pnt in points]), min([pnt.y for pnt in points]))
        self.max = Point(max([pnt.y for pnt in points]), max([pnt.y for pnt in points]))

    def draw(self):
        plt.plot([pnt.x for pnt in self.points], [pnt.y for pnt in self.points], 'ro' if len(self.points) < 400 else 'r.' if len(self.points) < 6000 else 'r,')
        plt.plot([pnt.x for pnt in self.hull] + [0], [pnt.y for pnt in self.hull] + [0])
        plt.show()