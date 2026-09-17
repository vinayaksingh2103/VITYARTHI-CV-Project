# VisionCount AI - Real-time Hand & Finger Number Identifier 🖐️🤖

An interactive, pure web-based Computer Vision application that identifies numbers shown by human fingers in front of a camera in real-time (0 to 10). Built with **pure HTML5, CSS3, and Vanilla JavaScript**—no frameworks, no backend required!

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Tech](https://img.shields.io/badge/Tech-HTML5%20%7C%20CSS3%20%7C%20JS-brightgreen.svg)
![CV](https://img.shields.io/badge/CV-MediaPipe%20Hands-cyan.svg)

---
-Live link :- https://hand-gesture-detect.netlify.app/
## 🌟 Key Features

- **100% Client-Side Computer Vision**: Powered by Google MediaPipe Hands via WebAssembly/WebGL. All processing is done locally inside the browser.
- **Numbers 0 to 10**:
  - **Single Hand (0 – 5)**: Fist for 0, up to open palm for 5.
  - **Dual Hand (6 – 10)**: Combine both hands to identify larger numbers seamlessly.
- **Orientation & Tilt Robust**: Uses euclidean distance vectors from fingertips to the palm base and wrist, making recognition accurate across varying angles.
- **Temporal Smoothing**: Rolling-window majority voting eliminates jitter and false flickers.
- **Cyber-Glass HUD Design**:
  - Glowing joint & skeletal mesh overlay on the webcam feed.
  - Large animated number badge with pop micro-animations.
  - Real-time finger status indicators (Thumb, Index, Middle, Ring, Pinky).
- **Audio Synthesis**: Interactive pitch chimes synthesized via the Web Audio API on number changes (with mute toggle).
- **Webcam Controls**: Horizontal mirror toggle, skeleton overlay toggle, and camera device selector.

---

## 🚀 Quick Start

Because this project uses vanilla web technologies, you don't need to install Node.js, Python packages, or dependencies.

### Option 1: Live Server / Python
```bash
# Clone the repository
git clone https://github.com/mayank-aiml/VITYARTHI-CV-Project.git

# Navigate to the folder
cd VITYARTHI-CV-Project

# Start any local HTTP server (e.g. Python)
python -m http.server 8080
```
Open **`http://localhost:8080`** in your browser.

### Option 2: Direct Hosting
You can host this project with **zero configuration** on:
- **GitHub Pages**: Go to Repository Settings > Pages > Select `main` branch > Save.
- **Netlify**: Drag and drop the folder to [Netlify Drop](https://app.netlify.com/drop).
- **Vercel**: Deploy directly or import the Git repository.

---

## 📂 Project Structure

```
├── index.html        # Main HTML layout, HUD tags, and dashboard cards
├── style.css         # Dark glassmorphism styling, ambient orbs, and animations
├── app.js            # MediaPipe Hands pipeline, geometric finger classification engine
└── README.md         # Documentation & guide
```

---

## 🎮 How to Use
1. Open the web application and click **"Launch Camera"**.
2. Grant camera permissions when prompted by your browser.
3. Show your hand(s) to the camera:
   - **0**: Closed fist
   - **1**: Index finger raised
   - **2**: Peace / Victory sign (Index + Middle)
   - **3**: Three fingers raised
   - **4**: Four fingers raised (thumb tucked)
   - **5**: Open hand
   - **6 – 10**: Raise fingers on both hands simultaneously!

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
