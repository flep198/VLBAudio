import numpy as np
import streamlit as st
import folium
from streamlit_folium import st_folium
from scipy.io import wavfile
from scipy.fft import fft, ifft, fftfreq
from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt
import io

st.title("🌍 VLBI Audio Fourier Explorer")

# -----------------------------
# Load audio (robust)
# -----------------------------
uploaded = st.file_uploader("Upload WAV file", type=["wav"])

if uploaded is None:
    st.info("Please upload a WAV file.")
    st.stop()

bytes_data = uploaded.read()
fs, x = wavfile.read(io.BytesIO(bytes_data))

if x.ndim > 1:
    x = x.mean(axis=1)

x = x.astype(float)
N = len(x)

X = fft(x)
freqs = fftfreq(N, d=1/fs)

# -----------------------------
# Haversine
# -----------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# -----------------------------
# Session state
# -----------------------------
if "telescopes" not in st.session_state:
    st.session_state.telescopes = []

if "last_added" not in st.session_state:
    st.session_state.last_added = None

def add_telescopes(new_telescopes):
    existing = set(st.session_state.telescopes)
    for t in new_telescopes:
        if t not in existing:
            st.session_state.telescopes.append(t)

# -----------------------------
# Arrays
# -----------------------------
VLBA = [
    (19.8016, -155.455),(34.0790, -107.618),(48.131, -119.683),
    (37.231, -118.282),(35.775, -106.245),(31.958, -111.597),
    (30.635, -103.944),(38.433, -79.839),(42.933, -71.986),
    (17.759, -64.583)
]

EVN = [
    (50.524778, 6.883972),(-25.89037, 27.68558),(57.553493, 21.854916),
    (44.5208, 11.6469),(36.87605, 14.989031),(57.393056, 11.917778),
    (31.0921, 121.1365),(43.47, 87.18),(40.525208, -3.088725),
    (25.03, 102.78),(53.095453,18.563980),(52.914781,6.602881)
]

st.subheader("Array presets")

col1, col2, col3 = st.columns(3)

if col1.button("Add VLBA"):
    add_telescopes(VLBA)
    st.rerun()

if col2.button("Add EVN"):
    add_telescopes(EVN)
    st.rerun()

if col3.button("Reset map"):
    st.session_state.telescopes = []
    st.session_state.last_added = None
    st.rerun()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Controls")

bandwidth = st.sidebar.slider(
    "Frequency bandwidth per baseline (Hz)",
    10, 500, 50
)

scale = 1.0

# -----------------------------
# Map
# -----------------------------
m = folium.Map(location=[20, 0], zoom_start=2)

for i, t in enumerate(st.session_state.telescopes):
    folium.Marker([t[0], t[1]], tooltip=f"Telescope {i}").add_to(m)

map_data = st_folium(m, height=500, width=700)

# 👇 Instruction BELOW map
st.caption("🖱️ Click on the map to add a telescope")

# Click = add telescope
if map_data["last_clicked"] is not None:
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    if st.session_state.last_added != (lat, lon):
        st.session_state.telescopes.append((lat, lon))
        st.session_state.last_added = (lat, lon)
        st.rerun()

# -----------------------------
# Baselines → frequency bands
# -----------------------------
bands = []
tel = st.session_state.telescopes

if len(tel) >= 2:
    for i in range(len(tel)):
        for j in range(i+1, len(tel)):
            d_km = haversine(*tel[i], *tel[j])
            f = d_km * scale
            bands.append((f - bandwidth, f + bandwidth))

# -----------------------------
# Reconstruction
# -----------------------------
if st.button("Reconstruct audio"):

    if len(bands) == 0:
        st.warning("Place at least 2 telescopes")
        st.stop()

    mask = np.zeros(N, dtype=bool)

    for fmin, fmax in bands:
        mask |= (np.abs(freqs) >= fmin) & (np.abs(freqs) <= fmax)

    Xf = np.zeros_like(X)
    Xf[mask] = X[mask]

    xr = np.real(ifft(Xf))
    xr = xr / (np.max(np.abs(xr)) + 1e-12)

    st.subheader("Audio")
    st.audio(xr, sample_rate=fs)

    st.subheader("Frequency coverage")

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(freqs[:N//2], np.abs(X[:N//2]), label="Original", linewidth=1.2)
    ax.plot(freqs[:N//2], np.abs(Xf[:N//2]), label="Sampled", linewidth=2)

    ax.set_xlim(0, 5000)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude")
    ax.set_title("VLBI Fourier Sampling")

    ax.grid(alpha=0.3)
    ax.set_yscale("log")
    ax.legend()

    st.pyplot(fig)
