# Project Title: VisionCount AI - Real-time Hand & Finger Number Identifier 🖐️🤖

## Overview of the Project
VisionCount AI is an interactive, pure web-based Computer Vision application that identifies numbers shown by human fingers in front of a camera in real-time (0 to 10). Built entirely on the client side, it processes webcam feeds locally in the browser with zero server-side computation or backend requirements. The system utilizes geometric heuristics to accurately classify hand gestures regardless of the camera angle or hand orientation.

## Features
- **100% Client-Side Computer Vision**: Powered by Google MediaPipe Hands via WebAssembly/WebGL. All processing is done locally inside the browser.
- **Numbers 0 to 10**:
  - **Single Hand (0 – 5)**: Fist for 0, up to open palm for 5.
  - **Dual Hand (6 – 10)**: Combine both hands to identify larger numbers seamlessly.
- **Orientation & Tilt Robust**: Uses euclidean distance vectors from fingertips to the palm base and wrist, making recognition accurate across varying angles.
- **Temporal Smoothing**: Rolling-window majority voting eliminates jitter and false flickers.
- **Cyber-Glass HUD Design**: Glowing joint & skeletal mesh overlay on the webcam feed, large animated number badge, and real-time finger status indicators.
- **Audio Synthesis**: Interactive pitch chimes synthesized via the Web Audio API on number changes.
- **Webcam Controls**: Horizontal mirror toggle, skeleton overlay toggle, and camera device selector.

## Technologies/Tools Used
- **Core Languages**: HTML5, CSS3, Vanilla JavaScript (ES6+).
- **Computer Vision Framework**: Google MediaPipe Hands.
- **Execution Environment**: Client-Side WebAssembly (Wasm) & WebGL.

## Steps to Install & Run the Project
This project uses vanilla web technologies and is designed to run via a local HTTP server from the command line.

### Prerequisites
- Python 3.x (for a simple local server) or Node.js (for `http-server`)
- A modern web browser (Chrome, Firefox, Edge, Safari)
- A working webcam

### 1. Clone the repository
```bash
git clone https://github.com/vinayaksingh2103/VITYARTHI-CV-Project.git
cd VITYARTHI-CV-Project
```

### 2. Run the Application
Because it relies on browser camera permissions, you must serve the files over a local web server (opening `index.html` directly from the file system (`file://`) will block webcam access).

**Using Python (Recommended):**
```bash
python -m http.server 8080
```

**Using Node.js (npx):**
```bash
npx http-server -p 8080
```

### 3. Execution
Open your browser and navigate to:
**`http://localhost:8080`**

## Instructions for Testing
1. Launch the application via `http://localhost:8080`.
2. Click **"Launch Camera"** and grant the browser camera permissions.
3. Stand in a well-lit area to ensure optimal hand detection.
4. Test single hand tracking: Show a closed fist for 0, and raise fingers consecutively up to 5. Verify the HUD and audio chimes update correctly.
5. Test dual hand tracking: Raise both hands and display fingers to count from 6 to 10.
6. Test orientation robustness: Tilt your hand sideways or slightly towards the camera. The system should still correctly identify the fingers due to vector-based logic.
7. Test the UI controls: Toggle the "Mirror Camera" and "Skeleton Overlay" buttons to ensure the visual rendering updates appropriately.

## Screenshots
*(Optional: Insert screenshots of the application running, the HUD, and gesture detection here by adding images to the assets folder and linking them like `![Screenshot](assets/screenshot1.png)`)*
