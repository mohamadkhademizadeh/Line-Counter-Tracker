import streamlit as st
import cv2, yaml, pandas as pd, time, tempfile, os
from src.linecounter.pipeline import CounterEngine

st.set_page_config(page_title="Line Counter Dashboard", layout="wide")
st.title("📊 Line Counter — Live Dashboard")

cfg = yaml.safe_load(open('configs/config.yaml','r'))
source = st.sidebar.text_input("Video source (file path or 0 for webcam)", "data/sample.mp4")
write_out = st.sidebar.checkbox("Write annotated video", False)
out_path = st.sidebar.text_input("Out path", "data/live_out.mp4")

start = st.button("Start")

if start:
    cap = cv2.VideoCapture(0 if source.strip()=="0" else source)
    if not cap.isOpened():
        st.error("Could not open video source"); st.stop()

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if cfg['video'].get('resize_width'):
        rw = cfg['video']['resize_width']; rh = int(h * rw / max(1,w)); w=rw; h=rh
    out = None
    if write_out:
        out = cv2.VideoWriter(out_path, fourcc, 25, (w,h))

    eng = CounterEngine(cfg)
    ph = st.empty(); t0=time.time(); i=0
    while True:
        ok, frame = cap.read()
        if not ok: break
        if cfg['video'].get('resize_width'):
            frame = cv2.resize(frame, (w,h))
        vis, tracks = eng.step(frame, i)
        ph.image(vis[..., ::-1], use_column_width=True)
        if out is not None:
            out.write(vis)
        i += 1
    cap.release()
    if out: out.release()
    st.success("Done. Events below:")
    st.dataframe(eng.to_dataframe())
