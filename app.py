from __future__ import annotations

import io
import zipfile
from pathlib import Path

import numpy as np
import streamlit as st
from PIL import Image, ImageOps, UnidentifiedImageError

# ------------------------------
# Page setup
# ------------------------------
st.set_page_config(
    page_title="Circuit Studio | Premium Circuit Converter",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------
# Styling
# ------------------------------
st.markdown(
    """
    <style>
    :root { color-scheme: dark; }
    .stApp {
        background:
          radial-gradient(ellipse at 12% 0%, rgba(67, 87, 145, .20), transparent 34%),
          radial-gradient(ellipse at 95% 8%, rgba(69, 126, 125, .12), transparent 29%),
          #090b10;
        color: #eef1f7;
    }
    .block-container { max-width: 1180px; padding-top: 2.1rem; padding-bottom: 3.5rem; }
    [data-testid="stHeader"] { background: transparent; }
    .brand-row { display:flex; align-items:center; gap:12px; margin-bottom:1.1rem; }
    .brand-mark {
        display:flex; align-items:center; justify-content:center;
        width:46px; height:46px; border-radius:14px;
        background:linear-gradient(135deg,#f2f5ff,#a8b7dc); color:#111522;
        font-size:25px; box-shadow:0 8px 26px rgba(130,151,210,.18);
    }
    .brand-name { color:#eef1f7; font-size:1rem; font-weight:750; letter-spacing:.02em; }
    .brand-sub { color:#929bad; font-size:.78rem; margin-top:2px; }
    .hero-title { font-size: clamp(2.2rem, 5vw, 3.8rem); font-weight:850; line-height:1.06;
        letter-spacing:-.045em; margin:.35rem 0 .9rem 0; }
    .hero-gradient { background:linear-gradient(100deg,#f8faff 10%,#aebff1 55%,#a1e2d3 100%);
        -webkit-background-clip:text; background-clip:text; color:transparent; }
    .hero-copy { max-width:760px; color:#aab2c2; font-size:1.06rem; line-height:1.75; }
    .pill { display:inline-block; padding:6px 10px; border-radius:999px;
        border:1px solid #283244; background:#111722; color:#c9d4e8; font-size:.76rem; margin:0 6px 7px 0; }
    .section-heading { font-size:1.25rem; font-weight:750; color:#f0f3fa; margin:.5rem 0 .2rem; }
    .muted { color:#98a2b5; font-size:.91rem; line-height:1.6; }
    .panel { border:1px solid #252d3b; border-radius:20px; background:rgba(16,20,29,.72); padding:20px 22px; }
    .metric-card { border:1px solid #263143; background:rgba(20,26,37,.8); border-radius:16px; padding:16px; }
    .metric-value { font-size:1.45rem; font-weight:800; color:#f4f6fd; }
    .metric-label { color:#9ba6b9; font-size:.82rem; margin-top:4px; }
    div[data-testid="stFileUploader"] { border-radius:18px; }
    div[data-testid="stFileUploaderDropzone"] { border:1px dashed #46536c; background:rgba(18,24,35,.58); border-radius:16px; }
    div[data-testid="stFileUploaderDropzone"]:hover { border-color:#99addb; }
    .stButton > button, .stDownloadButton > button {
        border-radius:12px; font-weight:700; min-height:48px; border:1px solid #d4dcf1;
        background:linear-gradient(100deg,#eef2ff,#cbd7fa); color:#111827;
    }
    .stButton > button:hover, .stDownloadButton > button:hover { border-color:#fff; color:#080b12; }
    .stDownloadButton > button { width:100%; }
    .stTabs [data-baseweb="tab-list"] { gap:8px; }
    .stTabs [data-baseweb="tab"] { border-radius:10px 10px 0 0; padding:10px 15px; }
    hr { border-color:#252d3b; }
    footer { visibility:hidden; }
    @media (max-width: 700px) {
      .block-container { padding-left:1rem; padding-right:1rem; padding-top:1.2rem; }
      .hero-copy { font-size:.98rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="brand-row">
      <div class="brand-mark">⚡</div>
      <div><div class="brand-name">CIRCUIT STUDIO</div>
      <div class="brand-sub">A clean workspace for technical notes</div></div>
    </div>
    <div><span class="pill">BATCH PROCESSING</span><span class="pill">SMOOTH EDGES</span><span class="pill">PNG + ZIP</span></div>
    <div class="hero-title">Make every circuit<br><span class="hero-gradient">note-ready.</span></div>
    <div class="hero-copy">Turn circuit diagrams into crisp white linework on a deep black background. Upload multiple images, inspect the results, and download them together in one ZIP file.</div>
    """,
    unsafe_allow_html=True,
)

st.write("")
left, right = st.columns([1.35, 0.8], gap="large")
with left:
    st.markdown('<div class="section-heading">01 · Upload your diagrams</div>', unsafe_allow_html=True)
    st.markdown('<div class="muted">Select several PNG, JPG, JPEG, or WEBP images at once.</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Choose circuit images",
        type=["png", "jpg", "jpeg", "webp", "bmp", "tif", "tiff"],
        accept_multiple_files=True,
        help="Your images are processed in this app session. Avoid uploading sensitive documents.",
        label_visibility="collapsed",
    )
with right:
    st.markdown('<div class="section-heading">Designed for study notes</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel">
          <div style="font-size:1.02rem;font-weight:750;margin-bottom:8px;">✦ Clean, high-contrast output</div>
          <div class="muted">Automatic background polarity detection, smooth black-to-white transitions, and optional 2×–4× enlargement for larger exports.</div>
          <hr>
          <div class="muted">No account is required to use this demo. Processed images are not saved to a permanent app folder by this code.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with st.expander("Advanced image settings", expanded=False):
    a, b, c = st.columns(3)
    with a:
        upscale = st.select_slider("Output scale", options=[1, 2, 3, 4], value=4, format_func=lambda x: f"{x}×")
    with b:
        low_cutoff = st.slider("Soft-edge start", min_value=0, max_value=80, value=18, step=1)
    with c:
        high_cutoff = st.slider("Full-white threshold", min_value=100, max_value=255, value=210, step=1)
    st.caption("Higher output scales create larger files and use more memory. If faint text disappears, try lowering ‘Soft-edge start’. Keep ‘Full-white threshold’ well above it.")

# ------------------------------
# Image processing
# ------------------------------
def convert_circuit(image_bytes: bytes, scale: int, low: int, high: int) -> tuple[Image.Image, tuple[int, int], bool]:
    """Return a high-contrast black-background image with white circuit details."""
    try:
        with Image.open(io.BytesIO(image_bytes)) as opened:
            original = ImageOps.exif_transpose(opened).convert("L")
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("This file could not be read as an image.") from exc

    arr = np.asarray(original)
    border = np.concatenate([arr[0, :], arr[-1, :], arr[:, 0], arr[:, -1]])
    light_background = float(np.median(border)) >= 127

    if scale > 1:
        target = (original.width * scale, original.height * scale)
        # Guard against accidental memory spikes from unusually large uploads.
        if target[0] * target[1] > 45_000_000:
            raise ValueError("This image is too large to enlarge at the selected scale. Try a lower output scale.")
        original = original.resize(target, Image.Resampling.LANCZOS)

    gray = np.asarray(original, dtype=np.float32)
    strength = 255.0 - gray if light_background else gray

    hi = max(high, low + 1)
    t = np.clip((strength - low) / (hi - low), 0.0, 1.0)
    # Smoothstep creates antialiased transitions rather than a harsh binary edge.
    t = t * t * (3.0 - 2.0 * t)
    result = np.clip(t * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(result, mode="L"), (arr.shape[1], arr.shape[0]), light_background


def safe_stem(filename: str) -> str:
    stem = Path(filename).stem.strip()
    clean = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in stem)
    return clean[:80] or "circuit"

# ------------------------------
# Batch processing + gallery + ZIP
# ------------------------------
if uploaded_files:
    st.write("")
    st.markdown('<div class="section-heading">02 · Convert and review</div>', unsafe_allow_html=True)
    st.markdown('<div class="muted">Preview each result below before downloading the complete batch.</div>', unsafe_allow_html=True)

    if len(uploaded_files) > 30:
        st.warning("For performance, this demo processes up to 30 images per batch. Please select 30 or fewer images.")
        active_files = uploaded_files[:30]
    else:
        active_files = uploaded_files

    zip_buffer = io.BytesIO()
    converted: list[tuple[str, Image.Image, tuple[int, int], bool]] = []
    errors: list[str] = []
    seen_names: dict[str, int] = {}

    progress = st.progress(0, text="Preparing your images…")
    for index, uploaded in enumerate(active_files):
        stem = safe_stem(uploaded.name)
        seen_names[stem] = seen_names.get(stem, 0) + 1
        if seen_names[stem] > 1:
            stem = f"{stem}_{seen_names[stem]}"
        output_name = f"{stem}_premium.png"
        try:
            converted_img, original_size, light_bg = convert_circuit(
                uploaded.getvalue(), upscale, low_cutoff, high_cutoff
            )
            converted.append((output_name, converted_img, original_size, light_bg))
        except (ValueError, MemoryError) as exc:
            errors.append(f"{uploaded.name}: {exc}")
        progress.progress((index + 1) / len(active_files), text=f"Processing {index + 1} of {len(active_files)}…")

    progress.empty()

    if converted:
        # Build ZIP in memory; no persistent output folder is created.
        with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
            for output_name, converted_img, _, _ in converted:
                image_buffer = io.BytesIO()
                converted_img.save(image_buffer, format="PNG", optimize=True)
                archive.writestr(output_name, image_buffer.getvalue())

        count_col, scale_col, format_col = st.columns(3)
        with count_col:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{len(converted)}</div><div class="metric-label">Images converted</div></div>', unsafe_allow_html=True)
        with scale_col:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{upscale}×</div><div class="metric-label">Output enlargement</div></div>', unsafe_allow_html=True)
        with format_col:
            st.markdown('<div class="metric-card"><div class="metric-value">PNG</div><div class="metric-label">Lossless output</div></div>', unsafe_allow_html=True)

        st.write("")
        tab_preview, tab_list = st.tabs(["Visual gallery", "Files in this batch"])
        with tab_preview:
            per_row = 2
            for start in range(0, len(converted), per_row):
                row_items = converted[start:start + per_row]
                cols = st.columns(len(row_items), gap="large")
                for col, (output_name, output_img, original_size, light_bg) in zip(cols, row_items):
                    with col:
                        st.markdown(f"**{output_name}**")
                        st.image(output_img, caption=f"Output: {output_img.width:,} × {output_img.height:,} px", use_container_width=True)
                        st.caption(f"Original: {original_size[0]:,} × {original_size[1]:,} px · Detected {'light' if light_bg else 'dark'} background")
                        one = io.BytesIO()
                        output_img.save(one, format="PNG", optimize=True)
                        st.download_button(
                            "Download this image",
                            data=one.getvalue(),
                            file_name=output_name,
                            mime="image/png",
                            key=f"download_{output_name}_{start}",
                            use_container_width=True,
                        )
        with tab_list:
            for output_name, output_img, original_size, light_bg in converted:
                st.markdown(f"- **{output_name}** — {output_img.width:,} × {output_img.height:,} px")

        st.write("")
        st.download_button(
            label="⬇  Download all converted images (.ZIP)",
            data=zip_buffer.getvalue(),
            file_name="premium_circuit_images.zip",
            mime="application/zip",
            type="primary",
            use_container_width=True,
        )
        st.caption("Tip: if a faint line or label is missing, adjust the advanced settings and rerun the conversion.")

    if errors:
        st.warning("Some files could not be converted:")
        for error in errors:
            st.write(f"- {error}")
else:
    st.write("")
    st.markdown(
        """
        <div class="panel" style="text-align:center;padding:34px 20px;">
          <div style="font-size:2rem;margin-bottom:8px;">▧</div>
          <div style="font-size:1.05rem;font-weight:750;color:#eef1f7;">Your preview gallery will appear here</div>
          <div class="muted" style="margin-top:6px;">Upload circuit diagrams above to start a batch conversion.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
st.markdown("---")
st.markdown(
    '<div class="muted" style="text-align:center;">CIRCUIT STUDIO · Made for clearer engineering notes<br>Processing happens during your session. Please do not upload confidential or sensitive images.</div>',
    unsafe_allow_html=True,
)
