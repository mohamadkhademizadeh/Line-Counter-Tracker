# Line-Counter-Tracker

A production-line **people/part counting & tracking** toolkit for videos/webcams.
- **Detectors**: YOLOv8 (if weights available) or **classical motion** fallback
- **Tracker**: lightweight IoU-based multi-object tracker with ID persistence
- **Counting**: polygon **zones** and/or crossing **counting lines**
- **Outputs**: per-event CSV (+ optional annotated MP4), live **Streamlit dashboard**
- **Config-driven** (zones, classes, thresholds)

Great portfolio piece: shows computer vision + systems thinking + UI.

---

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 1) (optional) put a test video under data/sample.mp4
# 2) configure zones in configs/config.yaml
# 3) run the pipeline (writes events.csv and optional out.mp4)
python scripts/run_video.py --video data/sample.mp4 --out_csv data/events.csv --out_video data/out.mp4
```

### Live dashboard
```bash
streamlit run app/dashboard.py
```

---

## Repo Layout
```
Line-Counter-Tracker/
├── app/
│   ├── annotator.py         # draw/edit zones interactively
│   └── dashboard.py         # live viewer + metrics
├── configs/
│   └── config.yaml          # detector/tracker/zone params
├── scripts/
│   └── run_video.py         # batch processor for video/webcam
├── src/linecounter/
│   ├── detector.py          # YOLO or motion fallback
│   ├── tracker.py           # simple IoU tracker with aging
│   ├── geometry.py          # IoU, polygons, crossings
│   ├── pipeline.py          # glue: detect->track->count
│   └── viz.py               # drawing helpers
├── tests/
│   └── test_geometry.py
├── requirements.txt
└── README.md
```

---

## Notes
- Works **out of the box** with the classical motion detector (no weights needed).
- To use YOLO: drop `yolov8n.pt` into `models/` and set `detector.backend: yolo` in `configs/config.yaml`.
- Counting logic: each track increments when **entering** a polygon zone (debounced) or **crossing** a line (directional).
