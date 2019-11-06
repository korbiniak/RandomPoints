from random import seed, randint as rand, shuffle
import sys
from utils import *
from display import Plane

if len(sys.argv) != 5:
    print ("Usage: seed, N, K, max")
    sys.exit()

seed(sys.argv[1])
n = int(sys.argv[2])
k = int(sys.argv[3])
maks = int(sys.argv[4])

points, hull = random_points(n, k, maks)

plane1 = Plane(points,hull)
plane1.draw()