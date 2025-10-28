import streamlit as st
import yaml, json, os

st.set_page_config(page_title="Zone Annotator", layout="wide")
st.title("🖊️ Line-Counter — Zone & Line Annotator")
st.write("Edit `configs/config.yaml` directly or paste JSON here.")

cfg_path = "configs/config.yaml"
with open(cfg_path,'r') as f:
    cfg = yaml.safe_load(f)

st.subheader("Current config")
st.json(cfg)

st.subheader("Paste new counting config (JSON)")
txt = st.text_area("counting", value=json.dumps(cfg.get('counting', {}), indent=2), height=300)
if st.button("Save"):
    try:
        cfg['counting'] = json.loads(txt)
        with open(cfg_path,'w') as f:
            yaml.safe_dump(cfg, f)
        st.success("Saved to configs/config.yaml")
    except Exception as e:
        st.error(str(e))
