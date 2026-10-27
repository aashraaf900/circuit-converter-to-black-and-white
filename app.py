from __future__ import annotations

import hashlib
import io
import zipfile
from pathlib import Path
from typing import Any

import numpy as np
import streamlit as st
from PIL import Image, ImageOps, UnidentifiedImageError

# ============================================================
# Circuit Studio — premium batch circuit image converter
# Created by ASHRAF AHMED
# ============================================================

st.set_page_config(
    page_title="Circuit Studio | ASHRAF AHMED",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------
# Premium charcoal UI
# ------------------------------
st.markdown(
    """
    <style>
    :root { color-scheme: dark; }
    html, body, [class*="css"] { font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
    .stApp {
        background:
          radial-gradient(ellipse at 8% -8%, rgba(129, 148, 205, .15), transparent 34%),
          radial-gradient(ellipse at 96% 2%, rgba(82, 179, 160, .10), transparent 28%),
          #17191f;
        color: #f5f7fb;
    }
    [data-testid="stAppViewContainer"] { background: transparent; }
    [data-testid="stHeader"] { background: rgba(23, 25, 31, .82); }
    [data-testid="stToolbar"] { right: 1rem; }
    .block-container { max-width: 1320px; padding-top: 1.65rem; padding-bottom: 4rem; }
    footer { visibility: hidden; }

    .topbar {
        display:flex; align-items:center; justify-content:space-between; gap:18px;
        padding: 13px 17px; margin-bottom: 34px;
        background: rgba(34, 37, 46, .88); border: 1px solid #3a3f4b;
        border-radius: 18px; box-shadow: 0 10px 34px rgba(0,0,0,.12);
    }
    .brand-lockup { display:flex; align-items:center; gap:12px; min-width:0; }
    .brand-mark {
        display:flex; align-items:center; justify-content:center; flex-shrink:0;
        width:45px; height:45px; border-radius:14px;
        background:linear-gradient(145deg,#f4f6ff,#bac7ef); color:#191b23;
        font-size:25px; box-shadow:0 5px 22px rgba(178,194,240,.12);
    }
    .brand-name { color:#f7f8fc; font-size:1rem; font-weight:850; letter-spacing:.10em; }
    .brand-sub { color:#aab2c2; font-size:.76rem; margin-top:3px; }
    .creator-chip { border:1px solid #4a5365; background:#2a2e39; border-radius:999px; padding:9px 13px; color:#e9edfa; font-size:.76rem; font-weight:800; letter-spacing:.09em; white-space:nowrap; }
    .eyebrow { color:#b8c6ed; text-transform:uppercase; letter-spacing:.16em; font-size:.74rem; font-weight:800; margin-bottom:13px; }
    .hero-title { font-size:clamp(2.45rem,5.2vw,4.65rem); font-weight:900; line-height:1.01; letter-spacing:-.055em; margin:.25rem 0 1.1rem; color:#fbfcff; }
    .hero-gradient { background:linear-gradient(100deg,#f5f7ff 4%,#bac9ff 53%,#a5ebd8 100%); -webkit-background-clip:text; background-clip:text; color:transparent; }
    .hero-copy { max-width:760px; color:#c0c6d3; font-size:1.06rem; line-height:1.8; }
    .hero-note { margin-top:20px; color:#aab2c2; font-size:.84rem; }
    .status-pill { display:inline-flex; align-items:center; gap:7px; border:1px solid #414958; background:#252934; color:#e2e8f7; padding:7px 10px; border-radius:999px; font-size:.75rem; font-weight:700; margin:0 6px 7px 0; }
    .status-dot { width:7px; height:7px; display:inline-block; border-radius:100%; background:#84dec7; box-shadow:0 0 12px rgba(132,222,199,.4); }

    .section-head { display:flex; align-items:center; gap:11px; margin:.35rem 0 .35rem; color:#f4f6fb; font-size:1.13rem; font-weight:800; }
    .section-number { display:inline-flex; align-items:center; justify-content:center; width:29px; height:29px; border-radius:9px; background:#dce4ff; color:#1a1d26; font-size:.75rem; font-weight:900; }
    .muted-copy { color:#aeb6c6; font-size:.91rem; line-height:1.65; margin-bottom:14px; }
    .panel { border:1px solid #3b414e; border-radius:20px; background:linear-gradient(150deg,rgba(42,46,57,.92),rgba(31,34,42,.94)); padding:21px 22px; box-shadow:0 14px 34px rgba(0,0,0,.10); }
    .panel-title { font-size:1.03rem; font-weight:800; color:#f6f7fb; margin-bottom:7px; }
    .panel-copy { color:#b9c0ce; font-size:.88rem; line-height:1.65; }
    .feature-row { display:flex; gap:11px; align-items:flex-start; margin-top:16px; }
    .feature-icon { flex-shrink:0; width:33px; height:33px; border-radius:10px; background:#343a48; border:1px solid #4a5363; display:flex; align-items:center; justify-content:center; color:#dfe6ff; font-size:1rem; }
    .feature-title { color:#edf0f8; font-size:.88rem; font-weight:750; }
    .feature-copy { color:#aeb6c6; font-size:.8rem; line-height:1.5; margin-top:3px; }

    div[data-testid="stFileUploader"] { margin-top:6px; }
    div[data-testid="stFileUploaderDropzone"] { background:#20232b; border:1.5px dashed #68758c; border-radius:17px; transition:border-color .2s ease, background .2s ease; }
    div[data-testid="stFileUploaderDropzone"]:hover { border-color:#cad5ff; background:#252a35; }
    div[data-testid="stFileUploaderDropzone"] button { border:1px solid #616d83 !important; background:#343a48 !important; color:#f2f5ff !important; border-radius:10px !important; }
    div[data-testid="stFileUploaderDropzone"] small, div[data-testid="stFileUploaderDropzone"] span { color:#c3cad8 !important; }

    .stButton > button, .stDownloadButton > button {
        min-height:47px; border-radius:12px; border:1px solid #e2e7fa;
        background:linear-gradient(100deg,#f0f3ff,#cbd6fb); color:#191d28;
        font-weight:800; transition:transform .15s ease, box-shadow .15s ease, filter .15s ease;
    }
    .stButton > button:hover, .stDownloadButton > button:hover { color:#11141c; border-color:#fff; filter:brightness(1.04); transform:translateY(-1px); box-shadow:0 8px 22px rgba(173,190,242,.13); }
    .stButton > button:focus, .stDownloadButton > button:focus { box-shadow:0 0 0 3px rgba(190,204,255,.24); }
    .stDownloadButton > button { width:100%; }
    div[data-testid="stProgress"] > div > div { background:linear-gradient(90deg,#b8c7ff,#91e2ce); }

    .metric-card { height:100%; border:1px solid #414754; background:linear-gradient(145deg,#292d37,#22252d); border-radius:16px; padding:16px 17px; }
    .metric-value { font-size:1.6rem; line-height:1.2; font-weight:900; color:#fbfcff; letter-spacing:-.03em; }
    .metric-label { color:#b9c1d0; font-size:.79rem; margin-top:6px; }
    .result-card { border:1px solid #3d4350; border-radius:17px; background:#20232b; padding:13px; }
    .file-title { color:#f1f4fb; font-size:.9rem; font-weight:800; overflow-wrap:anywhere; }
    .fine-print { color:#a6afbf; font-size:.78rem; line-height:1.55; }
    .success-banner { border:1px solid #3f796d; background:rgba(48,103,91,.18); border-radius:13px; padding:12px 15px; color:#c9f2e7; font-size:.9rem; }
    .warning-banner { border:1px solid #71613d; background:rgba(122,97,43,.16); border-radius:13px; padding:12px 15px; color:#f7e4b7; font-size:.88rem; }
    .step-line { display:flex; gap:11px; align-items:flex-start; margin-top:14px; }
    .step-badge { display:flex; align-items:center; justify-content:center; flex-shrink:0; width:26px; height:26px; background:#343b49; border:1px solid #515c70; color:#edf1ff; border-radius:8px; font-weight:850; font-size:.76rem; }

    .stTabs [data-baseweb="tab-list"] { gap:8px; border-bottom:1px solid #3b414e; }
    .stTabs [data-baseweb="tab"] { color:#b9c1d0; padding:10px 14px; border-radius:10px 10px 0 0; font-weight:700; }
    .stTabs [aria-selected="true"] { color:#f6f8ff !important; background:#2b303b; }
    [data-testid="stExpander"] { border:1px solid #3d4350; border-radius:14px; background:rgba(35,38,47,.7); }
    [data-testid="stExpander"] summary p { color:#f1f4fb; font-weight:750; }
    label, .stMarkdown p { color:inherit; }
    [data-testid="stCaptionContainer"] { color:#aab2c1; }
    [data-testid="stAlert"] { border-radius:13px; }
    input, textarea { color:#f4f6fb !important; }
    hr { border-color:#3a404c; }
    .footer-line { text-align:center; color:#8e97a8; font-size:.78rem; padding:22px 0 2px; }

    @media (max-width: 760px) {
      .block-container { padding-left:1rem; padding-right:1rem; padding-top:1rem; }
      .topbar { padding:11px; margin-bottom:25px; }
      .brand-mark { width:39px; height:39px; }
      .brand-name { font-size:.86rem; }
      .brand-sub { font-size:.68rem; }
      .creator-chip { font-size:.64rem; padding:8px; letter-spacing:.04em; }
      .hero-copy { font-size:.98rem; }
      .panel { padding:17px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------
# Branding / hero
# ------------------------------
st.markdown(
    """
    <div class="topbar">
      <div class="brand-lockup">
        <div class="brand-mark">⚡</div>
        <div>
          <div class="brand-name">CIRCUIT STUDIO</div>
          <div class="brand-sub">A sharper look for your study notes</div>
        </div>
      </div>
      <div class="creator-chip">BY ASHRAF AHMED</div>
    </div>
    <div>
      <span class="status-pill"><span class="status-dot"></span> MULTI-IMAGE WORKFLOW</span>
      <span class="status-pill">SMOOTH EDGE OUTPUT</span>
      <span class="status-pill">PNG + ZIP EXPORT</span>
    </div>
    <div class="hero-title">Your circuits.<br><span class="hero-gradient">A cleaner finish.</span></div>
    <div class="hero-copy">Convert textbook and lecture-note circuit diagrams into crisp white linework on a soft charcoal background. Process a batch, review every result, and download the whole set in one ZIP.</div>
    <div class="hero-note">Made for electrical engineering notes · Simple, fast, browser-based</div>
    """,
    unsafe_allow_html=True,
)

st.write("")

# ------------------------------
# Upload section / value panel
# ------------------------------
left, right = st.columns([1.28, 0.82], gap="large")
with left:
    st.markdown(
        '<div class="section-head"><span class="section-number">01</span> Add your circuit images</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="muted-copy">Choose multiple diagrams at once. Supported formats: PNG, JPG, WEBP, BMP, and TIFF.</div>',
        unsafe_allow_html=True,
    )
    uploaded_files = st.file_uploader(
        "Choose circuit images",
        type=["png", "jpg", "jpeg", "webp", "bmp", "tif", "tiff"],
        accept_multiple_files=True,
        help="Images are processed for this session. Do not upload private or sensitive documents.",
        label_visibility="collapsed",
        key="circuit_batch_upload",
    )
    if uploaded_files:
        total_mb = sum(len(item.getvalue()) for item in uploaded_files) / (1024 * 1024)
        st.markdown(
            f'<div class="success-banner">✓ {len(uploaded_files)} image(s) ready · {total_mb:.1f} MB selected</div>',
            unsafe_allow_html=True,
        )
        with st.expander("Review uploaded files", expanded=False):
            file_cols = st.columns(2)
            for idx, item in enumerate(uploaded_files):
                with file_cols[idx % 2]:
                    st.caption(f"{idx + 1:02d}  ·  {item.name}")

with right:
    st.markdown(
        """
        <div class="panel">
          <div class="panel-title">Made for polished lecture notes</div>
          <div class="panel-copy">A simple workflow designed to keep your diagrams readable without manually editing every picture.</div>
          <div class="feature-row">
            <div class="feature-icon">✦</div><div><div class="feature-title">Clean contrast</div><div class="feature-copy">Detects light or dark backgrounds and reverses the diagram when needed.</div></div>
          </div>
          <div class="feature-row">
            <div class="feature-icon">⌁</div><div><div class="feature-title">Smooth edges</div><div class="feature-copy">Soft transitions help circuit lines and labels look less jagged.</div></div>
          </div>
          <div class="feature-row">
            <div class="feature-icon">⇩</div><div><div class="feature-title">One-click export</div><div class="feature-copy">Download a single PNG or collect all converted images in a ZIP.</div></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------
# Settings
# ------------------------------
with st.expander("⚙  Image quality settings", expanded=False):
    st.markdown(
        '<div class="muted-copy">The recommended settings work well for most clean textbook scans. Adjust them if thin lines or faint labels are lost.</div>',
        unsafe_allow_html=True,
    )
    set_a, set_b, set_c = st.columns(3, gap="medium")
    with set_a:
        upscale = st.select_slider(
            "Output resolution",
            options=[1, 2, 3, 4],
            value=4,
            format_func=lambda val: f"{val}×",
            help="Multiplies both the image width and height.",
        )
    with set_b:
        low_cutoff = st.slider(
            "Soft-edge start", min_value=0, max_value=80, value=18, step=1,
            help="Lower values preserve faint lines; higher values suppress light noise.",
        )
    with set_c:
        high_cutoff = st.slider(
            "Full-white threshold", min_value=100, max_value=255, value=210, step=1,
            help="Higher values require stronger source contrast for fully white pixels.",
        )
    if high_cutoff <= low_cutoff:
        st.warning("Full-white threshold must be higher than soft-edge start.")

# ------------------------------
# Image processing helpers
# ------------------------------
def convert_circuit(
    image_bytes: bytes, scale: int, low: int, high: int
) -> tuple[bytes, tuple[int, int], bool, tuple[int, int]]:
    """Convert one diagram and return PNG bytes, original size, polarity, output size."""
    try:
        with Image.open(io.BytesIO(image_bytes)) as opened:
            original = ImageOps.exif_transpose(opened).convert("L")
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise ValueError("This file could not be safely read as an image.") from exc

    original_size = (original.width, original.height)
    arr = np.asarray(original)
    border = np.concatenate([arr[0, :], arr[-1, :], arr[:, 0], arr[:, -1]])
    light_background = float(np.median(border)) >= 127

    target_width = original.width * scale
    target_height = original.height * scale
    if target_width * target_height > 45_000_000:
        raise ValueError("Image is too large at this scale. Try a lower output resolution.")

    if scale > 1:
        original = original.resize((target_width, target_height), Image.Resampling.LANCZOS)

    gray = np.asarray(original, dtype=np.float32)
    strength = 255.0 - gray if light_background else gray
    hi = max(high, low + 1)
    t = np.clip((strength - low) / (hi - low), 0.0, 1.0)
    t = t * t * (3.0 - 2.0 * t)  # Smoothstep edge transition
    result = np.clip(t * 255.0, 0, 255).astype(np.uint8)

    out = io.BytesIO()
    Image.fromarray(result).save(out, format="PNG", optimize=True)
    return out.getvalue(), original_size, light_background, (target_width, target_height)


def safe_stem(filename: str) -> str:
    stem = Path(filename).stem.strip()
    clean = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in stem)
    return clean[:80] or "circuit"


def upload_signature(files: list[Any]) -> str:
    digest = hashlib.sha256()
    for item in files:
        digest.update(item.name.encode("utf-8", errors="replace"))
        digest.update(item.getvalue())
    return digest.hexdigest()

# ------------------------------
# Convert action
# ------------------------------
st.markdown(
    '<div class="section-head"><span class="section-number">02</span> Convert and preview</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="muted-copy">Your settings are applied when you press convert. Inspect the gallery before downloading.</div>',
    unsafe_allow_html=True,
)

button_col, helper_col = st.columns([0.48, 0.52], vertical_alignment="center")
with button_col:
    convert_clicked = st.button(
        "⚡  Convert selected images",
        type="primary",
        use_container_width=True,
        disabled=(not uploaded_files or high_cutoff <= low_cutoff),
    )
with helper_col:
    st.markdown(
        '<div class="fine-print">Recommended: 4× output for lecture notes. Large images may require a lower scale.</div>',
        unsafe_allow_html=True,
    )

if convert_clicked and uploaded_files:
    if len(uploaded_files) > 30:
        st.warning("A maximum of 30 images is processed per batch. The first 30 selected files will be used.")
        active_files = uploaded_files[:30]
    else:
        active_files = uploaded_files

    entries: list[dict[str, Any]] = []
    errors: list[str] = []
    used_names: dict[str, int] = {}
    progress = st.progress(0, text="Preparing your diagrams…")

    for index, uploaded in enumerate(active_files):
        stem = safe_stem(uploaded.name)
        used_names[stem] = used_names.get(stem, 0) + 1
        if used_names[stem] > 1:
            stem = f"{stem}_{used_names[stem]}"
        output_name = f"{stem}_premium.png"

        try:
            output_bytes, original_size, light_bg, output_size = convert_circuit(
                uploaded.getvalue(), upscale, low_cutoff, high_cutoff
            )
            entries.append(
                {
                    "filename": output_name,
                    "data": output_bytes,
                    "original_size": original_size,
                    "output_size": output_size,
                    "light_bg": light_bg,
                    "source_name": uploaded.name,
                }
            )
        except (ValueError, MemoryError, OSError) as exc:
            errors.append(f"{uploaded.name}: {exc}")

        progress.progress(
            (index + 1) / len(active_files),
            text=f"Processing {index + 1} of {len(active_files)}…",
        )

    progress.empty()

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        for entry in entries:
            archive.writestr(entry["filename"], entry["data"])

    st.session_state["circuit_conversion_result"] = {
        "signature": upload_signature(uploaded_files),
        "settings": (upscale, low_cutoff, high_cutoff),
        "entries": entries,
        "errors": errors,
        "zip_data": zip_buffer.getvalue(),
    }

# ------------------------------
# Results gallery
# ------------------------------
result = st.session_state.get("circuit_conversion_result")
current_signature = upload_signature(uploaded_files) if uploaded_files else None
current_settings = (upscale, low_cutoff, high_cutoff)

if result:
    matches_current = result["signature"] == current_signature and result["settings"] == current_settings
    if not matches_current:
        st.markdown(
            '<div class="warning-banner">You changed the selected images or quality settings after the last conversion. Press “Convert selected images” again to refresh the results.</div>',
            unsafe_allow_html=True,
        )

    entries = result["entries"]
    errors = result["errors"]

    if entries:
        st.write("")
        st.markdown(
            f'<div class="success-banner">✓ Conversion complete · {len(entries)} image(s) ready to download</div>',
            unsafe_allow_html=True,
        )
        st.write("")

        stat_a, stat_b, stat_c = st.columns(3, gap="medium")
        with stat_a:
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{len(entries)}</div><div class="metric-label">Images converted</div></div>',
                unsafe_allow_html=True,
            )
        with stat_b:
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{result["settings"][0]}×</div><div class="metric-label">Output enlargement</div></div>',
                unsafe_allow_html=True,
            )
        with stat_c:
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">PNG + ZIP</div><div class="metric-label">Export formats</div></div>',
                unsafe_allow_html=True,
            )

        st.write("")
        gallery_tab, files_tab = st.tabs(["✦  Visual gallery", "☷  Batch details"])
        with gallery_tab:
            st.markdown('<div class="muted-copy">Review the converted diagrams below. Download any image individually, or use the ZIP button underneath.</div>', unsafe_allow_html=True)
            for start in range(0, len(entries), 2):
                group = entries[start : start + 2]
                cols = st.columns(len(group), gap="large")
                for col, entry in zip(cols, group):
                    with col:
                        st.markdown('<div class="result-card">', unsafe_allow_html=True)
                        st.markdown(f'<div class="file-title">{entry["filename"]}</div>', unsafe_allow_html=True)
                        st.image(entry["data"], caption=f'{entry["output_size"][0]:,} × {entry["output_size"][1]:,} px', use_container_width=True)
                        st.markdown(
                            f'<div class="fine-print">Original: {entry["original_size"][0]:,} × {entry["original_size"][1]:,} px<br>Detected background: {"light" if entry["light_bg"] else "dark"}</div>',
                            unsafe_allow_html=True,
                        )
                        st.download_button(
                            "↓  Download PNG",
                            data=entry["data"],
                            file_name=entry["filename"],
                            mime="image/png",
                            key=f'png_{entry["filename"]}_{start}',
                            use_container_width=True,
                        )
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.write("")

        with files_tab:
            st.markdown("**Files included in this batch**")
            for idx, entry in enumerate(entries, start=1):
                st.markdown(
                    f'<div class="panel" style="padding:12px 15px;margin:8px 0;">'
                    f'<div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;">'
                    f'<span style="color:#f4f6fb;font-weight:750;">{idx:02d} · {entry["filename"]}</span>'
                    f'<span style="color:#b5bfd0;font-size:.82rem;">{entry["output_size"][0]:,} × {entry["output_size"][1]:,} px</span>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )

        st.write("")
        st.download_button(
            "⇩  Download all converted images · ZIP",
            data=result["zip_data"],
            file_name="premium_circuit_images.zip",
            mime="application/zip",
            type="primary",
            use_container_width=True,
            disabled=not matches_current,
        )
        st.caption("Tip: If faint lines or labels disappear, lower ‘Soft-edge start’ and convert again.")

    if errors:
        st.warning("Some files could not be converted:")
        for error in errors:
            st.caption(f"• {error}")

elif not uploaded_files:
    st.markdown(
        """
        <div class="panel" style="margin-top:6px;">
          <div class="panel-title">Your workspace is ready</div>
          <div class="panel-copy">Upload two or more circuit images to see them processed together. Your preview gallery and ZIP download will appear here after conversion.</div>
          <div class="step-line"><div class="step-badge">1</div><div><div class="feature-title">Upload</div><div class="feature-copy">Select multiple circuit diagrams from your device.</div></div></div>
          <div class="step-line"><div class="step-badge">2</div><div><div class="feature-title">Tune</div><div class="feature-copy">Choose output scale and edge smoothness.</div></div></div>
          <div class="step-line"><div class="step-badge">3</div><div><div class="feature-title">Export</div><div class="feature-copy">Review the results and download PNGs or a ZIP.</div></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="footer-line">CIRCUIT STUDIO · Built for clearer lecture notes · <strong style="color:#dfe5f5;">ASHRAF AHMED</strong></div>',
    unsafe_allow_html=True,
)
