from shapely.geometry import Polygon
from shapely.geometry.polygon import LinearRing
import numpy as np

p1np = np.array([[0, 0], [1, 1], [1, 0], [0, 1]])
print(p1np)

p1 = Polygon(p1np)
lr1 = LinearRing(p1np)
p2 = Polygon([(0,1), (1,0), (1,1)])
print(p1.intersects(p2))
print(lr1.is_simple)