# Project Statement: VisionCount AI

## 1. Problem Statement
Traditional human-computer interaction (HCI) heavily depends on physical input devices such as keyboards, mice, and touchscreens. While functional, these conventional interfaces can be limiting in touchless environments (e.g., healthcare settings, sanitary kiosks, or smart classrooms), non-verbal communication scenarios, and educational tools for children or individuals with motor or speech impairments.

Additionally, most conventional computer vision and gesture recognition systems require complex local installations, heavy deep learning frameworks (such as PyTorch or TensorFlow GPU setups), and high-latency backend servers to stream and process video feeds. This creates high infrastructure costs, severe privacy concerns associated with transmitting raw camera feeds over the internet, and high barriers of entry for everyday users who simply want an accessible, instant, and frictionless hand gesture interface directly in their web browser.

---

## 2. Scope of the Project
The scope of **VisionCount AI** is to deliver a lightweight, real-time, client-side computer vision web application that accurately recognizes and counts numbers (from 0 to 10) presented by human fingers in front of a standard webcam.

### In Scope:
- **100% Client-Side Execution**: All hand tracking and landmark estimation run locally in the browser utilizing WebAssembly and WebGL acceleration via Google MediaPipe Hands. No video data or frames leave the user's device.
- **Single & Dual-Hand Recognition**: Detecting 0 to 5 on a single hand (e.g., closed fist for 0, extended fingers up to 5) and up to 10 when combining both hands.
- **Geometric Finger Classification**: Vector-based mathematical heuristics measuring fingertip distances relative to MCP and wrist joints, ensuring invariance against hand rotation, pitch, and camera distances.
- **Interactive Visual & Audio Feedback**: Real-time HUD (Heads-Up Display) with neon joint overlays, dynamic status badges, rolling-window temporal smoothing to eliminate flicker, and Web Audio API tone synthesis.
- **Cross-Platform Accessibility**: Zero-installation web interface compatible with any modern browser (Google Chrome, Microsoft Edge, Mozilla Firefox, Safari) on laptops, desktops, and mobile devices with a camera.

### Out of Scope:
- Static hand sign languages (e.g., full ASL/BSL vocabulary beyond numerical finger counts).
- Complex dynamic motion gestures (e.g., swiping, waving, continuous hand trajectory tracing).
- Server-side database storage or user authentication (designed intentionally to be privacy-first and stateless).

---

## 3. Target Users
1. **Students and Educators**:
   - Primary and early childhood education teachers introducing numbers, counting, and interactive math games to young learners.
   - STEM students and educators demonstrating applied computer vision and human-computer interaction concepts without setting up Python/C++ environments.
2. **Individuals with Speech or Motor Impairments**:
   - Non-verbal individuals seeking accessible non-contact input systems to signal numerical selections or basic responses.
3. **Developers and Researchers**:
   - Hobbyists and frontend developers exploring browser-based edge AI, WebAssembly, and computer vision integration without dedicated GPU servers.
4. **Touchless Kiosk & Smart Environment Designers**:
   - Developers prototyping sanitary, touch-free interfaces for public kiosks, smart mirrors, or gaming experiences where touching a screen is undesirable.

---

## 4. High-Level Features
- **Real-Time Finger & Number Identification (0–10)**:
  - Instantaneous recognition of numbers 0 through 10 with high accuracy and low latency.
- **Zero-Latency Client-Side Inference**:
  - Direct frame processing at 30–60 FPS using GPU-accelerated MediaPipe Hands WebAssembly binaries.
- **Temporal Smoothing Engine**:
  - Rolling-window majority voting filter that suppresses single-frame flickering or borderline finger detection jitter.
- **Cyber-Glass HUD & Visual Skeleton**:
  - Live canvas rendering displaying 21 hand landmarks, glowing cybernetic connections, and state indicators (active green vs. inactive gray) for each fingertip.
- **Detailed Finger-Level Breakdown**:
  - Dedicated telemetry dashboard displaying the exact state of each individual digit (Thumb, Index, Middle, Ring, Pinky) for both left and right hands.
- **Multi-Device & Camera Control**:
  - In-browser camera switching (front/back or external USB webcams), mirror mode toggling, and skeleton overlay visibility control.
- **Dynamic Audio Feedback**:
  - Harmonic pitch synthesis using the native Web Audio API that chimes when a new stable number is identified.
- **Zero-Framework Deployment**:
  - Built entirely using standard HTML5, CSS3, and Vanilla JavaScript—hostable on GitHub Pages, Netlify, or Vercel with zero configuration.
