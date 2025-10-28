import cv2

def draw_box(img, box, tid=None, color=(0,255,0)):
    x1,y1,x2,y2 = box
    cv2.rectangle(img, (x1,y1), (x2,y2), color, 2)
    if tid is not None:
        cv2.putText(img, f"ID {tid}", (x1, max(0,y1-6)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

def draw_poly(img, pts, name="zone", color=(0,0,255)):
    import numpy as np
    p=np.array(pts, dtype=int)
    cv2.polylines(img, [p], isClosed=True, color=color, thickness=2)
    cv2.putText(img, name, tuple(p[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)

def draw_line(img, p1, p2, name="line", color=(255,0,0)):
    cv2.line(img, tuple(p1), tuple(p2), color, 2)
    cv2.putText(img, name, tuple(p1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)
