import argparse, cv2, yaml, os, pandas as pd
from src.linecounter.pipeline import CounterEngine

def main(args):
    cfg = yaml.safe_load(open(args.config,'r'))
    cap = cv2.VideoCapture(0 if args.video.strip()=="0" else args.video)
    if not cap.isOpened():
        raise SystemExit("Could not open source")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if cfg['video'].get('resize_width'):
        rw = cfg['video']['resize_width']; rh = int(h * rw / max(1,w)); w=rw; h=rh
    out = None
    if args.out_video:
        out = cv2.VideoWriter(args.out_video, fourcc, 25, (w,h))
    eng = CounterEngine(cfg)
    i=0
    while True:
        ok, frame = cap.read()
        if not ok: break
        if cfg['video'].get('resize_width'):
            frame = cv2.resize(frame, (w,h))
        vis, tracks = eng.step(frame, i)
        if out is not None:
            out.write(vis)
        i+=1
    cap.release()
    if out: out.release()
    df = eng.to_dataframe()
    if args.out_csv:
        os.makedirs(os.path.dirname(args.out_csv), exist_ok=True)
        df.to_csv(args.out_csv, index=False)
    print("Events:", len(df))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", default="data/sample.mp4")
    ap.add_argument("--config", default="configs/config.yaml")
    ap.add_argument("--out_csv", default="data/events.csv")
    ap.add_argument("--out_video", default="")
    args = ap.parse_args()
    main(args)
