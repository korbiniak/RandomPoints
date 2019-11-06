from random import randint as rand, shuffle
import sys
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __mul__(self, other):
        return self.x * other.y - self.y * other.x 
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        if self.x == 0 and self.y == 0:
            return True
        t1 = (self.x > 0 or (self.x == 0 and self.y >= 0))
        t2 = (other.x > 0 or (other.x == 0 and other.y >= 0))
        if t1 != t2:
            return t1
        return self * other < 0

class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.val = 0
        self.lazy = 0


class Tree:
    def __init__(self, size):
        self.size = 1
        while self.size < size:
            self.size *= 2
        
        self.root = Node()
        self.update(0, size, 1)

    def update(self, l, r, val):
        self._update(self.root, 0, self.size-1, l, r, val)

    def propagate(self, node, start, end):
        if not node:
            return
        node.val += node.lazy * (end-start+1)
        if start != end:
            if not node.left:
                node.left = Node()
            if not node.right:
                node.right = Node()
            node.left.lazy += node.lazy
            node.right.lazy += node.lazy
        node.lazy = 0

    def _update(self, node, start, end, l, r, val):
        self.propagate(node, start, end)
        if start > end or l > end or r < start:
            return
        
        if start >= l and end <= r:
            node.lazy += val
            self.propagate(node, start, end)
            return

        mid = (start + end) // 2
        if not node.left:
            node.left = Node()
        if not node.right:
            node.right = Node()
        self._update(node.left, start, mid, l, r, val)
        self._update(node.right, mid + 1, end, l, r, val)

        node.val = node.left.val + node.right.val
         
    def get_random(self):
        node = self.root
        start, end = 0, self.size - 1
        while start < end:
            mid = (start+end) // 2
            self.propagate(node, start, end)
            self.propagate(node.left, start, mid)
            self.propagate(node.right, mid+1, end)

            l = 0 if not node.left else node.left.val
            r = 0 if not node.right else node.right.val

            k = rand(1, l+r)

            if k <= l:
                node = node.left
                end = (start+end)//2
            else:
                node = node.right
                start = (start+end)//2 + 1
        self.update(start, start, -1)
        return start

def random_set(l, r, k):
    r -= l
    if r+1 < k:
        return None
    if r == 0:
        return [0]

    randTree = Tree(r)
    
    ans = []    
    while len(ans) < k:
        ans.append(randTree.get_random())    
    
    return [i + l for i in ans]

def split_list(a):
    b = a[:len(a)//2]
    c = a[len(a)//2:]
    return b, c

def get_random_vectors(l, r, k):
    t = random_set(l, r, k)
    t.sort()
    mini, maks = t[0], t[-1]
    t = t[1:-1]
    shuffle(t)
    a, b, = split_list(t)
    a = [mini] + a + [maks]
    b = [mini] + b + [maks]

    a.sort()
    b.sort()

    vect = [a[i+1] - a[i] for i in range(0,len(a)-1)]
    vect += [b[i] - b[i+1] for i in range(0,len(b)-1)]
    shuffle(vect)
    return vect

def random_hull(maksCoord, k):
    vectX = get_random_vectors(0, maksCoord, k)
    vectY = get_random_vectors(0, maksCoord, k)

    hull = [Point(x, y) for x, y in zip(vectX, vectY)]
    hull.sort()

    cur = Point()
    ret = []

    for p in hull:
        ret.append(cur)
        cur = cur + p
    
    return ret

def is_in_triangle(a, b, c, d):
    if (a-d) * (b-d) <= 0 and (b-d) * (c-d) <= 0 and (c-d) * (a-d) <= 0: 
        return True
    return False

def _random_points(n, k, maks):
    print ("Generating hull....")
    hull = random_hull(maks, k)
    print ("Done")

    x_min = min([pnt.x for pnt in hull])
    x_max = max([pnt.x for pnt in hull])
    y_min = min([pnt.y for pnt in hull])
    y_max = max([pnt.y for pnt in hull])

    pnts = set()
    for pnt in hull:
        pnts.add(pnt)
    hull.append(Point())

    ind = 1

    print("Generating points inside hull...")
    it = 0
    while len(pnts) < n:
        randPnts = [Point(rand(x_min, x_max), rand(y_min, y_max)) for i in range(n)] + hull
        randPnts.sort()
        it += 1
        
        if it > 100:
            return None

        curPnts = []

        for pnt in randPnts:
            if hull[ind+1] == pnt:
                ind += 1
            elif is_in_triangle(Point(), hull[ind], hull[ind+1], pnt) and (pnt not in pnts):
                if not (hull[1] * pnt == 0) and not (hull[-2] * pnt == 0):
                    if not (hull[ind]-pnt) * (hull[ind+1]-pnt) == 0:
                        curPnts.append(pnt)

        shuffle(curPnts)
        for pnt in curPnts:
            if pnt not in pnts:
                pnts.add(pnt)
            if len(pnts) >= n:
                break
        ind = 1
    print ("Done")
    return list(pnts), hull[:-1]


def random_points(n, k, maks):
    if maks < k:
        print ("Max cannot be smaller than K!")
        return

    if n < k:
        print ("N cannot be smaller than K!")
        return

    main_it = 0
    ret = None
    while main_it < 100 and not ret:
        ret = _random_points(n, k, maks)
        main_it += 1
    if not ret:
        print ("Too many iterations, try another seed and be sure that the task is possible to be accomplished with given constraints.")
        sys.exit()
    return ret
    