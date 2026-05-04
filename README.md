# 🌍 VLBI Audio Fourier Explorer

An interactive Streamlit application that demonstrates the core ideas behind **Very Long Baseline Interferometry (VLBI)** using audio signals and Fourier transforms.

Instead of observing radio waves from space, this tool maps telescope baselines to frequency-domain sampling of an audio signal, allowing users to intuitively explore how sparse interferometric sampling affects reconstruction.

---

## ✨ Features

- 🗺️ Interactive world map for placing telescopes
- 📡 Predefined telescope arrays:
  - VLBA (Very Long Baseline Array)
  - EVN (European VLBI Network)
- 🖱️ Click-to-add telescopes directly on the map
- ♻️ Reset system for clearing the array
- 🎧 WAV audio upload and processing
- 📊 Fourier-domain sampling based on baseline geometry
- 🔁 Signal reconstruction from sparse frequency coverage
- 📉 Clean spectral comparison (original vs sampled)

---

## 🧠 Concept

This project builds an analogy between:

- **Baseline length (km)** → **Fourier frequency (Hz)**  
- **Interferometric sampling (uv-plane)** → **Frequency-domain masking**

Each telescope pair defines a baseline:

d_ij → frequency band

This creates a simplified model of how VLBI samples spatial frequencies in radio astronomy.

---

## ⚠️ Important Disclaimer

This is a **didactic simulation**, not a physically accurate VLBI correlator.

- km → Hz mapping is artificial (set to 1:1 scaling)
- No Earth rotation synthesis is included
- No real visibility function or uv-plane sampling is computed

The goal is **intuition and visualization**, not scientific analysis.

---

## 🚀 Installation

### 1. Clone the repository
git clone https://github.com/your-username/vlbi-audio-explorer.git
cd vlbi-audio-explorer

### 2. Install dependencies
pip install streamlit numpy scipy matplotlib folium streamlit-folium

---

## ▶️ Run the application

streamlit run run5.py

---

## 🎮 How to use

1. Upload a WAV audio file  
2. Add telescopes by clicking on the map  
3. Or use presets:
   - Add VLBA
   - Add EVN
4. Click Reconstruct audio
5. Compare original vs sampled spectrum

---

## 📡 Telescope arrays

### VLBA
A simplified representation of the Very Long Baseline Array (USA + Caribbean stations).

### EVN
Includes major global VLBI stations:
Effelsberg (EF), Hartebeesthoek (HH), Irbene (IR), Medicina (MC), Noto (NT), Onsala (ON), Tianma (Tm65), Urumqi (UR), Yebes (YS), Kashima (KM), Torun (TR), Westerbork (WB)

---

## 📊 Visualization

The app shows a frequency-domain comparison:

- Original Fourier spectrum  
- Masked spectrum from VLBI baselines  

---

## 🧩 Future ideas

- uv-plane visualization  
- Earth rotation synthesis  
- CLEAN algorithm demo  
- Image reconstruction instead of audio  

---

## 🧑‍🚀 Author

Built as an educational bridge between VLBI, Fourier analysis, and signal processing intuition.

---

## 📜 License

MIT License
