import numpy as np

def iou(a, b):
    ax1,ay1,ax2,ay2 = a; bx1,by1,bx2,by2 = b
    inter = max(0, min(ax2,bx2)-max(ax1,bx1)) * max(0, min(ay2,by2)-max(ay1,by1))
    if inter <= 0:
        return 0.0
    area_a = (ax2-ax1)*(ay2-ay1); area_b = (bx2-bx1)*(by2-by1)
    return inter / (area_a + area_b - inter + 1e-6)

class Track:
    _next = 1
    def __init__(self, box):
        self.id = Track._next; Track._next += 1
        self.box = box
        self.age = 0
        self.miss = 0
        self.history = []

class IOUTracker:
    def __init__(self, iou_thresh=0.3, max_age=30):
        self.iou_thresh = iou_thresh
        self.max_age = max_age
        self.tracks = []

    def update(self, detections):
        # detections: list of boxes
        dets = list(detections)
        used = set()
        # match existing tracks
        for tr in self.tracks:
            tr.age += 1
            # find best IoU
            best = -1; best_i = -1
            for i, d in enumerate(dets):
                if i in used: 
                    continue
                iouv = iou(tr.box, d)
                if iouv > best:
                    best = iouv; best_i = i
            if best >= self.iou_thresh:
                tr.box = dets[best_i]
                tr.miss = 0
                tr.history.append(tr.box)
                used.add(best_i)
            else:
                tr.miss += 1
        # create new tracks
        for i, d in enumerate(dets):
            if i not in used:
                t = Track(d)
                t.history.append(d)
                self.tracks.append(t)
        # remove old
        self.tracks = [t for t in self.tracks if t.miss <= self.max_age]
        return self.tracks
