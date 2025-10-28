from shapely.geometry import Polygon, Point, LineString

def point_in_polygon(pt, poly_pts):
    return Polygon(poly_pts).contains(Point(pt))

def segment_crossed(prev_center, curr_center, p1, p2):
    # returns +1 if crossed in p1->p2 direction, -1 opposite, 0 otherwise
    seg = LineString([p1, p2])
    path = LineString([prev_center, curr_center])
    if not seg.crosses(path) and not seg.touches(path):
        return 0
    # direction: compute signed area wrt line normal (left/right)
    # use dot with line normal to infer direction
    import numpy as np
    v = np.array(p2) - np.array(p1)
    n = np.array([-v[1], v[0]])
    s1 = n.dot(np.array(prev_center) - np.array(p1))
    s2 = n.dot(np.array(curr_center) - np.array(p1))
    if s1 <= 0 and s2 > 0:
        return +1
    if s1 >= 0 and s2 < 0:
        return -1
    return 0

def box_center(box):
    x1,y1,x2,y2 = box
    return ((x1+x2)//2, (y1+y2)//2)
