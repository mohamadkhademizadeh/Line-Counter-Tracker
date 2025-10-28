import cv2, yaml, time, pandas as pd
from .detector import build_detector
from .tracker import IOUTracker
from .geometry import box_center, point_in_polygon, segment_crossed
from .viz import draw_box, draw_poly, draw_line

class CounterEngine:
    def __init__(self, cfg):
        self.detector = build_detector(cfg)
        self.tracker = IOUTracker(cfg['tracker']['iou_thresh'], cfg['tracker']['max_age'])
        self.cfg = cfg
        self.zone_state = {}  # (track_id, zone_name) -> last_trigger_frame
        self.line_state = {}  # (track_id, line_name) -> last_side
        self.events = []

    def step(self, frame_bgr, frame_idx=0):
        boxes, scores, clss = self.detector(frame_bgr)
        tracks = self.tracker.update(boxes)
        h, w = frame_bgr.shape[:2]

        # draw primitives
        if self.cfg['video'].get('draw', True):
            for z in self.cfg['counting'].get('zones', []):
                draw_poly(frame_bgr, z['points'], z.get('name','zone'))
            for ln in self.cfg['counting'].get('lines', []):
                draw_line(frame_bgr, ln['p1'], ln['p2'], ln.get('name','line'))

        # evaluate zones/lines
        for tr in tracks:
            x1,y1,x2,y2 = tr.box
            cx, cy = box_center(tr.box)
            if self.cfg['video'].get('draw', True):
                draw_box(frame_bgr, tr.box, tr.id)

            # zones: trigger when center enters polygon (debounce frames)
            for z in self.cfg['counting'].get('zones', []):
                inside = point_in_polygon((cx, cy), z['points'])
                key = (tr.id, z['name'])
                last = self.zone_state.get(key, -1e9)
                if inside and (frame_idx - last) > int(self.cfg['counting']['debounce']):
                    self.zone_state[key] = frame_idx
                    self.events.append(dict(type='zone_enter', zone=z['name'], track_id=tr.id, frame=frame_idx, cx=cx, cy=cy))

            # lines: detect direction of crossing
            for ln in self.cfg['counting'].get('lines', []):
                if len(tr.history) < 2: 
                    continue
                prev = tr.history[-2]; now = tr.history[-1]
                p1 = tuple(ln['p1']); p2 = tuple(ln['p2'])
                dirn = segment_crossed(((prev[0]+prev[2])//2, (prev[1]+prev[3])//2), (cx,cy), p1,p2)
                if dirn != 0:
                    direction = 'up' if dirn>0 else 'down'
                    if ln.get('direction','both') in ('both', direction):
                        self.events.append(dict(type='line_cross', line=ln['name'], direction=direction, track_id=tr.id, frame=frame_idx, cx=cx, cy=cy))

        return frame_bgr, tracks

    def to_dataframe(self):
        return pd.DataFrame(self.events)
