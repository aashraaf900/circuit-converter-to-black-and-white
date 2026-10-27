from __future__ import annotations

import hashlib
import io
import zipfile
from pathlib import Path
from typing import Any

import numpy as np
import streamlit as st
from PIL import Image, ImageFilter, ImageOps, UnidentifiedImageError

# ============================================================
# CIRCUIT STUDIO — colored circuit + label output
# By ASHRAF AHMED
# Dependencies: streamlit, numpy, Pillow
# ============================================================

st.set_page_config(
    page_title="Circuit Studio | ASHRAF AHMED",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

COLOR_OPTIONS: dict[str, str] = {
    "White": "#F5F8FF",
    "Red": "#FF414B",
    "Orange": "#FF9123",
    "Yellow": "#FFDC37",
    "Blue": "#4191FF",
    "Cyan": "#2DE1E1",
    "Green": "#4BDC87",
    "Purple": "#B473FF",
    "Pink": "#FF78BD",
    "Mint": "#77F0CA",
}

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
    .topbar { display:flex; align-items:center; justify-content:space-between; gap:18px; padding:13px 17px; margin-bottom:30px; background:rgba(34,37,46,.88); border:1px solid #3a3f4b; border-radius:18px; box-shadow:0 10px 34px rgba(0,0,0,.12); }
    .brand-lockup { display:flex; align-items:center; gap:12px; min-width:0; }
    .brand-mark { display:flex; align-items:center; justify-content:center; flex-shrink:0; width:45px; height:45px; border-radius:14px; background:linear-gradient(145deg,#f4f6ff,#bac7ef); color:#191b23; font-size:25px; }
    .brand-name { color:#f7f8fc; font-size:1rem; font-weight:850; letter-spacing:.10em; }
    .brand-sub { color:#aab2c2; font-size:.76rem; margin-top:3px; }
    .creator-chip { border:1px solid #4a5365; background:#2a2e39; border-radius:999px; padding:9px 13px; color:#e9edfa; font-size:.76rem; font-weight:800; letter-spacing:.09em; white-space:nowrap; }
    .hero-title { font-size:clamp(2.45rem,5.2vw,4.65rem); font-weight:900; line-height:1.01; letter-spacing:-.055em; margin:.25rem 0 1.1rem; color:#fbfcff; }
    .hero-gradient { background:linear-gradient(100deg,#f5f7ff 4%,#bac9ff 53%,#a5ebd8 100%); -webkit-background-clip:text; background-clip:text; color:transparent; }
    .hero-copy { max-width:780px; color:#c0c6d3; font-size:1.04rem; line-height:1.8; }
    .hero-note { margin-top:18px; color:#aab2c2; font-size:.84rem; }
    .status-pill { display:inline-flex; align-items:center; gap:7px; border:1px solid #414958; background:#252934; color:#e2e8f7; padding:7px 10px; border-radius:999px; font-size:.75rem; font-weight:700; margin:0 6px 7px 0; }
    .status-dot { width:7px; height:7px; display:inline-block; border-radius:100%; background:#84dec7; box-shadow:0 0 12px rgba(132,222,199,.4); }
    .section-head { display:flex; align-items:center; gap:11px; margin:.45rem 0 .4rem; color:#f4f6fb; font-size:1.13rem; font-weight:800; }
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
    .stButton > button, .stDownloadButton > button { min-height:46px; border-radius:12px; border:1px solid #e2e7fa; background:linear-gradient(100deg,#f0f3ff,#cbd6fb); color:#191d28; font-weight:800; transition:transform .15s ease, box-shadow .15s ease, filter .15s ease; }
    .stButton > button:hover, .stDownloadButton > button:hover { color:#11141c; border-color:#fff; filter:brightness(1.04); transform:translateY(-1px); box-shadow:0 8px 22px rgba(173,190,242,.13); }
    .stDownloadButton > button { width:100%; }
    div[data-testid="stProgress"] > div > div { background:linear-gradient(90deg,#b8c7ff,#91e2ce); }
    .metric-card { height:100%; border:1px solid #414754; background:linear-gradient(145deg,#292d37,#22252d); border-radius:16px; padding:16px 17px; }
    .metric-value { font-size:1.6rem; line-height:1.2; font-weight:900; color:#fbfcff; letter-spacing:-.03em; }
    .metric-label { color:#b9c1d0; font-size:.79rem; margin-top:6px; }
    .fine-print { color:#a6afbf; font-size:.78rem; line-height:1.55; }
    .success-banner { border:1px solid #3f796d; background:rgba(48,103,91,.18); border-radius:13px; padding:12px 15px; color:#c9f2e7; font-size:.9rem; }
    .warning-banner { border:1px solid #71613d; background:rgba(122,97,43,.16); border-radius:13px; padding:12px 15px; color:#f7e4b7; font-size:.88rem; }
    .stTabs [data-baseweb="tab-list"] { gap:8px; border-bottom:1px solid #3b414e; }
    .stTabs [data-baseweb="tab"] { color:#b9c1d0; padding:10px 14px; border-radius:10px 10px 0 0; font-weight:700; }
    .stTabs [aria-selected="true"] { color:#f6f8ff !important; background:#2b303b; }
    [data-testid="stExpander"] { border:1px solid #3d4350; border-radius:14px; background:rgba(35,38,47,.7); }
    [data-testid="stExpander"] summary p { color:#f1f4fb; font-weight:750; }
    label, .stMarkdown p { color:inherit; }
    [data-testid="stCaptionContainer"] { color:#aab2c1; }
    [data-testid="stAlert"] { border-radius:13px; }
    hr { border-color:#3a404c; }
    .footer-line { text-align:center; color:#8e97a8; font-size:.78rem; padding:22px 0 2px; }
    @media (max-width: 760px) { .block-container { padding-left:1rem; padding-right:1rem; padding-top:1rem; } .topbar { padding:11px; margin-bottom:25px; } .brand-mark { width:39px; height:39px; } .brand-name { font-size:.86rem; } .brand-sub { font-size:.68rem; } .creator-chip { font-size:.64rem; padding:8px; letter-spacing:.04em; } .hero-copy { font-size:.98rem; } .panel { padding:17px; } }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="topbar">
      <div class="brand-lockup"><div class="brand-mark">⚡</div><div>
        <div class="brand-name">CIRCUIT STUDIO</div>
        <div class="brand-sub">A sharper look for your study notes</div>
      </div></div>
      <div class="creator-chip">BY ASHRAF AHMED</div>
    </div>
    <div>
      <span class="status-pill"><span class="status-dot"></span> MULTI-IMAGE WORKFLOW</span>
      <span class="status-pill">CUSTOM CIRCUIT + LABEL COLORS</span>
      <span class="status-pill">PNG + ZIP EXPORT</span>
    </div>
    <div class="hero-title">Your circuits.<br><span class="hero-gradient">Your colors.</span></div>
    <div class="hero-copy">Choose one color for circuit lines and another for text labels. The background stays pure black. Preview every diagram, then download individual PNGs or the whole batch as a ZIP.</div>
    <div class="hero-note">Made for electrical engineering lecture notes · Smooth-edge output · Browser-based</div>
    """,
    unsafe_allow_html=True,
)


def _hex_to_rgb(hex_value: str) -> tuple[int, int, int]:
    value = hex_value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _safe_stem(filename: str) -> str:
    stem = Path(filename).stem.strip()
    clean = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in stem)
    return clean[:75] or "circuit"


def _upload_signature(files: list[Any]) -> str:
    digest = hashlib.sha256()
    for item in files:
        digest.update(item.name.encode("utf-8", errors="replace"))
        digest.update(item.getvalue())
    return digest.hexdigest()


def _find_root(parent: list[int], item: int) -> int:
    while parent[item] != item:
        parent[item] = parent[parent[item]]
        item = parent[item]
    return item


def _union(parent: list[int], a: int, b: int) -> None:
    root_a = _find_root(parent, a)
    root_b = _find_root(parent, b)
    if root_a != root_b:
        parent[root_b] = root_a


def _detect_label_mask(strength_original: np.ndarray, threshold: int = 58) -> np.ndarray:
    """Best-effort heuristic to identify small, isolated text glyphs.

    The segmentation is done at up to 1400 px on the long side to control
    processing time. Connected components that look like small glyphs are
    assigned to the label color. It is heuristic, not OCR, so a few small
    disconnected circuit symbols can occasionally be treated as labels.
    """
    height, width = strength_original.shape
    max_side = max(height, width)
    if max_side > 1400:
        seg_w = max(1, round(width * 1400 / max_side))
        seg_h = max(1, round(height * 1400 / max_side))
        seg_img = Image.fromarray(strength_original).resize((seg_w, seg_h), Image.Resampling.LANCZOS)
        seg = np.asarray(seg_img, dtype=np.uint8)
    else:
        seg = strength_original.astype(np.uint8, copy=False)
        seg_h, seg_w = seg.shape

    binary = seg >= int(threshold)
    all_runs: list[tuple[int, int, int, int]] = []  # y, x_start, x_end, component label
    parent: list[int] = []
    previous: list[tuple[int, int, int]] = []  # x_start, x_end, label

    for y in range(seg_h):
        row = binary[y]
        changes = np.diff(np.pad(row.astype(np.int8), (1, 1)))
        starts = np.flatnonzero(changes == 1)
        ends = np.flatnonzero(changes == -1) - 1
        current: list[tuple[int, int, int]] = []
        p = 0
        for x0, x1 in zip(starts.tolist(), ends.tolist()):
            label = len(parent)
            parent.append(label)
            while p < len(previous) and previous[p][1] < x0 - 1:
                p += 1
            k = p
            while k < len(previous) and previous[k][0] <= x1 + 1:
                if previous[k][1] >= x0 - 1:
                    _union(parent, label, previous[k][2])
                k += 1
            current.append((x0, x1, label))
            all_runs.append((y, x0, x1, label))
        previous = current

    if not all_runs:
        return np.zeros((height, width), dtype=bool)

    # Aggregate each connected component's bounding box and foreground area.
    stats: dict[int, list[int]] = {}
    for y, x0, x1, label in all_runs:
        root = _find_root(parent, label)
        area = x1 - x0 + 1
        if root not in stats:
            stats[root] = [area, x0, y, x1, y]
        else:
            item = stats[root]
            item[0] += area
            item[1] = min(item[1], x0)
            item[2] = min(item[2], y)
            item[3] = max(item[3], x1)
            item[4] = max(item[4], y)

    max_h = max(18, min(58, int(seg_h * 0.055)))
    max_w = max(38, min(100, int(seg_w * 0.095)))
    max_area = max(140, int(seg_h * seg_w * 0.0020))
    label_roots: set[int] = set()

    for root, (area, x0, y0, x1, y1) in stats.items():
        w = x1 - x0 + 1
        h = y1 - y0 + 1
        if area < 4 or w > max_w or h > max_h or area > max_area:
            continue
        aspect = w / max(h, 1)
        occupancy = area / max(w * h, 1)
        # Text glyphs are commonly compact. Allow very short horizontal
        # marks (+/-/minus) but reject long, thin lines and likely wires.
        shape_looks_like_glyph = (0.09 <= aspect <= 2.05) or (w <= 42 and h <= 18 and 2.05 < aspect <= 4.0) or (max(w, h) <= 18 and 4.0 < aspect <= 5.5)
        if shape_looks_like_glyph and occupancy >= 0.07:
            label_roots.add(root)

    if not label_roots:
        return np.zeros((height, width), dtype=bool)

    label_small = np.zeros((seg_h, seg_w), dtype=np.uint8)
    for y, x0, x1, label in all_runs:
        if _find_root(parent, label) in label_roots:
            label_small[y, x0:x1 + 1] = 255

    # Slight dilation includes anti-aliased edges around the detected letters.
    label_image = Image.fromarray(label_small).filter(ImageFilter.MaxFilter(3))
    if (seg_w, seg_h) != (width, height):
        label_image = label_image.resize((width, height), Image.Resampling.NEAREST)
    return np.asarray(label_image) > 0


def _convert_circuit(
    image_bytes: bytes,
    circuit_hex: str,
    label_hex: str,
    scale: int,
    low: int,
    high: int,
    separate_labels: bool,
    label_threshold: int,
) -> tuple[bytes, tuple[int, int], bool, tuple[int, int], int]:
    """Return PNG bytes, original size, detected background polarity, output size and label-mask pixel count."""
    try:
        with Image.open(io.BytesIO(image_bytes)) as opened:
            original = ImageOps.exif_transpose(opened).convert("L")
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise ValueError("This file could not be safely read as an image.") from exc

    original_size = (original.width, original.height)
    source_gray = np.asarray(original, dtype=np.uint8)
    border = np.concatenate((source_gray[0, :], source_gray[-1, :], source_gray[:, 0], source_gray[:, -1]))
    light_background = float(np.median(border)) >= 127
    strength_source = 255 - source_gray if light_background else source_gray

    target_width = original.width * scale
    target_height = original.height * scale
    if target_width * target_height > 45_000_000:
        raise ValueError("This image is too large at the selected scale. Choose a lower output resolution.")

    if scale > 1:
        gray_up_image = original.resize((target_width, target_height), Image.Resampling.LANCZOS)
    else:
        gray_up_image = original
    gray_up = np.asarray(gray_up_image, dtype=np.float32)
    strength = 255.0 - gray_up if light_background else gray_up

    hi = max(int(high), int(low) + 1)
    t = np.clip((strength - float(low)) / float(hi - low), 0.0, 1.0)
    alpha = t * t * (3.0 - 2.0 * t)  # Smoothstep anti-aliasing

    circuit_rgb = np.array(_hex_to_rgb(circuit_hex), dtype=np.float32)
    label_rgb = np.array(_hex_to_rgb(label_hex), dtype=np.float32)
    # Pure black canvas; smooth alpha controls each colored foreground pixel.
    output = alpha[..., None] * circuit_rgb[None, None, :]

    label_pixels = 0
    if separate_labels:
        label_mask_source = _detect_label_mask(strength_source, threshold=label_threshold)
        label_mask_image = Image.fromarray((label_mask_source.astype(np.uint8) * 255))
        if scale > 1:
            label_mask_image = label_mask_image.resize((target_width, target_height), Image.Resampling.NEAREST)
        label_mask = np.asarray(label_mask_image) > 0
        label_pixels = int(np.count_nonzero(label_mask))
        output[label_mask] = alpha[label_mask][:, None] * label_rgb[None, :]

    output_u8 = np.clip(output, 0, 255).astype(np.uint8)
    out = io.BytesIO()
    Image.fromarray(output_u8, mode="RGB").save(out, format="PNG", optimize=True)
    return out.getvalue(), original_size, light_background, (target_width, target_height), label_pixels


def _make_preview_png(image_bytes: bytes, max_side: int = 850) -> bytes:
    """Create a small PNG for the gallery so previews do not use excess memory."""
    with Image.open(io.BytesIO(image_bytes)) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        image.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG", optimize=True)
        return buffer.getvalue()


# ------------------------------
# Upload area and feature panel
# ------------------------------
left, right = st.columns([1.25, 0.85], gap="large")
with left:
    st.markdown('<div class="section-head"><span class="section-number">01</span> Add your circuit images</div>', unsafe_allow_html=True)
    st.markdown('<div class="muted-copy">Select multiple diagrams in one go. Supported formats: PNG, JPG, WEBP, BMP, and TIFF.</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Choose circuit images", type=["png", "jpg", "jpeg", "webp", "bmp", "tif", "tiff"],
        accept_multiple_files=True, label_visibility="collapsed", key="circuit_color_upload",
        help="Images are processed by this app for the current session.",
    )
    if uploaded_files:
        total_mb = sum(len(item.getvalue()) for item in uploaded_files) / (1024 * 1024)
        st.markdown(f'<div class="success-banner">✓ {len(uploaded_files)} image(s) ready · {total_mb:.1f} MB selected</div>', unsafe_allow_html=True)
        with st.expander("Review uploaded files", expanded=False):
            for idx, item in enumerate(uploaded_files, start=1):
                st.caption(f"{idx:02d} · {item.name}")

with right:
    st.markdown(
        """
        <div class="panel">
          <div class="panel-title">Made for polished lecture notes</div>
          <div class="panel-copy">Create a consistent color style for textbook circuits and electrical engineering notes.</div>
          <div class="feature-row"><div class="feature-icon">◉</div><div><div class="feature-title">Black background, always</div><div class="feature-copy">The export canvas stays pure black, regardless of the original background.</div></div></div>
          <div class="feature-row"><div class="feature-icon">✦</div><div><div class="feature-title">Two colors</div><div class="feature-copy">Pick a circuit-line color and a separate text/label color.</div></div></div>
          <div class="feature-row"><div class="feature-icon">⇩</div><div><div class="feature-title">Batch export</div><div class="feature-copy">Preview each result, download PNGs individually, or export a single ZIP.</div></div></div>
        </div>
        """, unsafe_allow_html=True,
    )

# ------------------------------
# Color settings
# ------------------------------
st.markdown('<div class="section-head"><span class="section-number">02</span> Choose your colors</div>', unsafe_allow_html=True)
st.markdown('<div class="muted-copy">Background is fixed to black. Select a different color for the circuit and for labels such as 3 Ω, 20 V, A and B.</div>', unsafe_allow_html=True)
color_col_a, color_col_b, preview_col = st.columns([1, 1, 0.8], gap="large")
with color_col_a:
    circuit_preset = st.selectbox("Circuit / wire color", list(COLOR_OPTIONS.keys()), index=3, key="circuit_color_preset")
    circuit_custom = st.checkbox("Use custom circuit color", value=False, key="custom_circuit_toggle")
    circuit_hex = st.color_picker("Custom circuit color", value=COLOR_OPTIONS[circuit_preset], key="custom_circuit_color", disabled=not circuit_custom)
    circuit_hex = circuit_hex if circuit_custom else COLOR_OPTIONS[circuit_preset]
with color_col_b:
    label_preset = st.selectbox("Text / label color", list(COLOR_OPTIONS.keys()), index=0, key="label_color_preset")
    label_custom = st.checkbox("Use custom label color", value=False, key="custom_label_toggle")
    label_hex = st.color_picker("Custom label color", value=COLOR_OPTIONS[label_preset], key="custom_label_color", disabled=not label_custom)
    label_hex = label_hex if label_custom else COLOR_OPTIONS[label_preset]
with preview_col:
    st.markdown('<div class="panel-title">Color preview</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="background:#000;border:1px solid #4a5160;border-radius:14px;padding:22px 14px;text-align:center;">'
        f'<div style="color:{circuit_hex};font-size:1.15rem;font-weight:850;letter-spacing:.04em;">─── /  / ───</div>'
        f'<div style="color:{label_hex};font-size:1.05rem;font-weight:800;margin-top:10px;">3 Ω &nbsp; 20 V &nbsp; A–B</div>'
        f'<div style="color:#a9b1c0;font-size:.7rem;margin-top:14px;">BLACK BACKGROUND</div></div>',
        unsafe_allow_html=True,
    )

with st.expander("⚙ Image quality and label-detection settings", expanded=False):
    q1, q2, q3 = st.columns(3, gap="medium")
    with q1:
        upscale = st.select_slider("Output resolution", options=[1, 2, 3, 4], value=4, format_func=lambda v: f"{v}×")
    with q2:
        low_cutoff = st.slider("Soft-edge start", 0, 80, 18, 1, help="Lower values preserve faint lines; raise it to suppress background noise.")
    with q3:
        high_cutoff = st.slider("Full-color threshold", 100, 255, 210, 1, help="Controls how quickly foreground pixels reach the selected color.")
    separate_labels = st.toggle("Color text labels separately", value=True, help="Best-effort detection of isolated text glyphs. A few small disconnected symbols may also be treated as labels.")
    label_threshold = st.slider("Label detection sensitivity", 20, 140, 58, 2, help="Lower values detect faint/dim labels but can include more small symbols or noise.")
    st.caption("Label separation is heuristic rather than OCR. If a small resistor or symbol receives the label color, turn off separate labels or adjust sensitivity.")

# ------------------------------
# Convert button
# ------------------------------
st.markdown('<div class="section-head"><span class="section-number">03</span> Convert and preview</div>', unsafe_allow_html=True)
st.markdown('<div class="muted-copy">Review the outputs below. Download any PNG individually or collect the whole batch in a ZIP.</div>', unsafe_allow_html=True)
button_col, helper_col = st.columns([0.48, 0.52], vertical_alignment="center")
with button_col:
    convert_clicked = st.button("⚡ Convert selected images", type="primary", use_container_width=True, disabled=not uploaded_files or high_cutoff <= low_cutoff)
with helper_col:
    st.markdown('<div class="fine-print">For lecture notes, 2× or 4× is recommended. Very large images may need a lower scale to fit available memory.</div>', unsafe_allow_html=True)

current_signature = _upload_signature(uploaded_files) if uploaded_files else None
current_settings = (circuit_hex, label_hex, upscale, low_cutoff, high_cutoff, separate_labels, label_threshold)

if convert_clicked and uploaded_files:
    active_files = uploaded_files[:30]
    if len(uploaded_files) > 30:
        st.warning("A maximum of 30 images is processed per batch. The first 30 selected files will be used.")

    entries: list[dict[str, Any]] = []
    errors: list[str] = []
    used_names: dict[str, int] = {}
    progress = st.progress(0, text="Preparing your diagrams…")

    for index, uploaded in enumerate(active_files):
        stem = _safe_stem(uploaded.name)
        used_names[stem] = used_names.get(stem, 0) + 1
        if used_names[stem] > 1:
            stem = f"{stem}_{used_names[stem]}"
        out_name = f"{stem}_circuit-{circuit_hex.lstrip('#')}_labels-{label_hex.lstrip('#')}.png"
        try:
            input_bytes = uploaded.getvalue()
            output_bytes, original_size, light_bg, output_size, label_pixels = _convert_circuit(
                input_bytes, circuit_hex, label_hex, upscale,
                low_cutoff, high_cutoff, separate_labels, label_threshold,
            )
            entries.append({
                "filename": out_name, "data": output_bytes,
                "original_preview": _make_preview_png(input_bytes),
                "converted_preview": _make_preview_png(output_bytes),
                "original_size": original_size, "output_size": output_size,
                "light_bg": light_bg, "source_name": uploaded.name,
                "label_pixels": label_pixels,
            })
        except (ValueError, MemoryError, OSError, Image.DecompressionBombError) as exc:
            errors.append(f"{uploaded.name}: {exc}")
        except Exception as exc:
            errors.append(f"{uploaded.name}: Unexpected processing error: {exc}")
        progress.progress((index + 1) / len(active_files), text=f"Processing {index + 1} of {len(active_files)}…")
    progress.empty()

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        for entry in entries:
            archive.writestr(entry["filename"], entry["data"])

    st.session_state["circuit_color_result"] = {
        "signature": current_signature,
        "settings": current_settings,
        "entries": entries,
        "errors": errors,
        "zip_data": zip_buffer.getvalue(),
        "circuit_hex": circuit_hex,
        "label_hex": label_hex,
        "upscale": upscale,
    }

# ------------------------------
# Gallery + downloads
# ------------------------------
if not uploaded_files:
    st.session_state.pop("circuit_color_result", None)
result = st.session_state.get("circuit_color_result")
if result:
    matches_current = result["signature"] == current_signature and result["settings"] == current_settings
    if not matches_current:
        st.markdown('<div class="warning-banner">You changed the images or settings after the last conversion. Press “Convert selected images” again to refresh the results.</div>', unsafe_allow_html=True)

    entries = result["entries"]
    errors = result["errors"]
    if entries:
        st.markdown(f'<div class="success-banner">✓ Conversion complete · {len(entries)} image(s) ready · circuit {result["circuit_hex"]} · labels {result["label_hex"]}</div>', unsafe_allow_html=True)
        st.write("")
        a, b, c = st.columns(3, gap="medium")
        with a:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{len(entries)}</div><div class="metric-label">Images converted</div></div>', unsafe_allow_html=True)
        with b:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{result["upscale"]}×</div><div class="metric-label">Output enlargement</div></div>', unsafe_allow_html=True)
        with c:
            st.markdown('<div class="metric-card"><div class="metric-value">PNG + ZIP</div><div class="metric-label">Download formats</div></div>', unsafe_allow_html=True)

        gallery_tab, files_tab = st.tabs(["✦ Visual gallery", "☷ Batch details"])
        with gallery_tab:
            st.markdown('<div class="muted-copy">Original and converted images are shown side by side. Scroll through the gallery to review your batch.</div>', unsafe_allow_html=True)
            for start in range(0, len(entries), 2):
                group = entries[start:start + 2]
                cols = st.columns(len(group), gap="large")
                for col, entry in zip(cols, group):
                    with col:
                        st.markdown(f'<div class="file-title">{entry["filename"]}</div>', unsafe_allow_html=True)
                        preview_a, preview_b = st.columns(2, gap="small")
                        with preview_a:
                            st.caption("Original")
                            st.image(entry["original_preview"], use_container_width=True)
                        with preview_b:
                            st.caption("Converted")
                            st.image(entry["converted_preview"], use_container_width=True)
                        st.caption(f'{entry["output_size"][0]:,} × {entry["output_size"][1]:,} px · input background detected as {"light" if entry["light_bg"] else "dark"}')
                        st.download_button(
                            "↓ Download PNG", data=entry["data"], file_name=entry["filename"],
                            mime="image/png", key=f'png_{entry["filename"]}_{start}', use_container_width=True,
                        )
        with files_tab:
            st.markdown("**Files included in this batch**")
            for idx, entry in enumerate(entries, start=1):
                st.markdown(f'<div class="panel" style="padding:12px 15px;margin:8px 0;"><div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;"><span style="color:#f4f6fb;font-weight:750;">{idx:02d} · {entry["filename"]}</span><span style="color:#b5bfd0;font-size:.82rem;">{entry["output_size"][0]:,} × {entry["output_size"][1]:,} px</span></div></div>', unsafe_allow_html=True)
        st.download_button(
            "⇩ Download all converted images · ZIP", data=result["zip_data"],
            file_name="circuit_studio_colored_images.zip", mime="application/zip",
            type="primary", use_container_width=True, disabled=not matches_current,
        )
    if errors:
        st.warning("Some files could not be converted:")
        for error in errors:
            st.caption(f"• {error}")
elif not uploaded_files:
    st.markdown(
        """
        <div class="panel" style="margin-top:6px;">
          <div class="panel-title">Your workspace is ready</div>
          <div class="panel-copy">Upload circuit diagrams, choose your circuit and label colors, then convert and export PNGs or a ZIP.</div>
          <div class="feature-row"><div class="feature-icon">1</div><div><div class="feature-title">Upload</div><div class="feature-copy">Select multiple diagrams from your device.</div></div></div>
          <div class="feature-row"><div class="feature-icon">2</div><div><div class="feature-title">Customize</div><div class="feature-copy">Pick circuit color, label color, and output resolution.</div></div></div>
          <div class="feature-row"><div class="feature-icon">3</div><div><div class="feature-title">Export</div><div class="feature-copy">Preview, download PNGs individually, or download everything in a ZIP.</div></div></div>
        </div>
        """, unsafe_allow_html=True,
    )

st.markdown('<div class="footer-line">CIRCUIT STUDIO · BY <strong style="color:#dfe5f5;">ASHRAF AHMED</strong></div>', unsafe_allow_html=True)
