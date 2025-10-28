from src.linecounter.geometry import point_in_polygon, segment_crossed, box_center

def test_point_in_polygon():
    poly = [(0,0),(10,0),(10,10),(0,10)]
    assert point_in_polygon((5,5), poly) is True
    assert point_in_polygon((15,5), poly) is False
