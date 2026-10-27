# Circuit Studio — Premium Circuit Converter

A public-friendly Streamlit web app for converting multiple circuit images into clean white-on-black PNG files with smooth transitions and batch ZIP download.

## Features
- Upload multiple circuit images at once (PNG, JPG, JPEG, WEBP, BMP, TIFF)
- Automatically detects whether the image background is light or dark
- Smooth edge transitions and optional 1×–4× upscaling
- Preview gallery and per-image downloads
- Download all results as a ZIP archive
- Dark premium-style interface for desktop and mobile

## Deploy publicly with Streamlit Community Cloud

1. Download and extract this project ZIP.
2. Create or sign in to GitHub: https://github.com/
3. Create a new repository, for example `circuit-studio`.
4. Upload **all files and folders inside this project** to the repository. Make sure `app.py`, `requirements.txt`, and `.streamlit/config.toml` are at the repository root.
5. Go to https://share.streamlit.io/ and connect your GitHub account.
6. Choose **Create app**, select the repository and branch, and set the main file path to `app.py`.
7. Click **Deploy**. When ready, copy the public `*.streamlit.app` URL and share it.

To update the app later, edit `app.py` on GitHub. Streamlit Community Cloud rebuilds the app from the repository.

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Resource note
The app processes uploaded images in memory and doesn't create a permanent upload folder. Large files and large batches use more RAM; the app limits a batch to 30 images and prevents extreme upscaling. Public deployments may have platform resource limits, so test with representative files before sharing widely.
