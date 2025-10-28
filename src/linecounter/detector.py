import os, cv2, numpy as np

try:
    from ultralytics import YOLO
except Exception:
    YOLO = None

class YOLODetector:
    def __init__(self, weights, conf=0.25, classes=None):
        if YOLO is None:
            raise RuntimeError("Ultralytics not installed")
        if not os.path.exists(weights):
            raise FileNotFoundError(weights)
        self.model = YOLO(weights); self.conf=conf; self.classes=classes or []

    def __call__(self, frame_bgr):
        res = self.model(frame_bgr, conf=self.conf, classes=self.classes or None)[0]
        boxes=[]; scores=[]; clss=[]
        if hasattr(res, 'boxes'):
            xyxy = res.boxes.xyxy.cpu().numpy().astype(int)
            conf = res.boxes.conf.cpu().numpy().tolist()
            cls = res.boxes.cls.cpu().numpy().astype(int).tolist()
            for b,s,c in zip(xyxy, conf, cls):
                boxes.append(tuple(map(int, b)))
                scores.append(float(s))
                clss.append(int(c))
        return boxes, scores, clss

class MotionDetector:
    def __init__(self):
        self.back = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)

    def __call__(self, frame_bgr):
        fg = self.back.apply(frame_bgr)
        fg = cv2.threshold(fg, 200, 255, cv2.THRESH_BINARY)[1]
        fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((3,3),np.uint8), iterations=1)
        contours,_ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        boxes=[]; scores=[]; clss=[]
        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            if w*h < 500: 
                continue
            boxes.append((x,y,x+w,y+h))
            scores.append(0.5)
            clss.append(0)
        return boxes, scores, clss

def build_detector(cfg):
    backend = cfg['detector']['backend']
    if backend == 'yolo':
        return YOLODetector(cfg['detector']['model_path'], cfg['detector']['conf'], cfg['detector']['classes'])
    if backend == 'auto':
        try:
            return YOLODetector(cfg['detector']['model_path'], cfg['detector']['conf'], cfg['detector']['classes'])
        except Exception:
            return MotionDetector()
    return MotionDetector()
