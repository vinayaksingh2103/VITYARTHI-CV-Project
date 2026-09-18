# Project Statement

## Problem Statement
Traditional computer vision applications for gesture recognition often require heavy backend infrastructure, powerful local GPUs, or complex installations of Python dependencies (like OpenCV and PyTorch). This creates a high barrier to entry for end-users who simply want to interact with computer vision models. Furthermore, many naive implementations struggle with varying camera angles and hand orientations, leading to inaccurate gesture classification. There is a need for a lightweight, accessible, and robust hand-gesture recognition system that works universally across devices.

## Scope of the Project
The scope of VisionCount AI is to develop a real-time, browser-based application capable of counting fingers (from 0 to 10) using one or both hands. The project focuses strictly on client-side execution utilizing Google MediaPipe for landmark detection. The classification logic is limited to mathematical heuristics (Euclidean distance measurements) rather than a secondary neural network. The scope includes providing visual feedback (a skeletal overlay and HUD) and audio feedback, but excludes server-side processing, data storage, and user authentication.

## Target Users
- **Educators and Students:** For interactive learning, demonstrating computer vision principles, or counting games for early childhood education.
- **Developers and Researchers:** As a reference implementation for running complex ML models directly in the browser using WebAssembly.
- **General Public:** Individuals interested in testing human-computer interaction (HCI) applications without needing to download specialized software.

## High-Level Features
- **Zero-Install Client-Side Execution:** Runs completely in any modern web browser without server-side dependencies.
- **Real-Time Finger Detection (0-10):** Capable of tracking up to two hands simultaneously to count up to 10.
- **Orientation-Agnostic Classification:** Uses vector mathematics to ensure accurate counting regardless of hand tilt or rotation.
- **Interactive UI/UX:** Features a "Cyber-Glass" Heads-Up Display (HUD) with real-time skeletal rendering and dynamic number animations.
- **Audio Synthesis Feedback:** Generates pitch-shifting audio chimes using the Web Audio API based on the detected number.
- **Robust Smoothing Algorithm:** Implements a rolling-window majority vote to eliminate detection jitter.
