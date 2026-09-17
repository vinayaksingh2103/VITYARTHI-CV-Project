/**
 * VisionCount AI - Real-time Hand & Finger Number Identifier
 * Powered by MediaPipe Hands (Client-side WebAssembly / GPU)
 */

(function () {
  'use strict';

  // --- DOM Elements ---
  const videoElement = document.getElementById('webcam');
  const canvasElement = document.getElementById('outputCanvas');
  const canvasCtx = canvasElement.getContext('2d');

  const cameraToggleBtn = document.getElementById('cameraToggleBtn');
  const cameraBtnText = document.getElementById('cameraBtnText');
  const startHeroBtn = document.getElementById('startHeroBtn');
  const standbyOverlay = document.getElementById('standbyOverlay');
  const hudOverlay = document.getElementById('hudOverlay');
  const camStatusDot = document.getElementById('camStatusDot');
  const camStatusText = document.getElementById('camStatusText');

  const mirrorToggleBtn = document.getElementById('mirrorToggleBtn');
  const skeletonToggleBtn = document.getElementById('skeletonToggleBtn');
  const soundToggleBtn = document.getElementById('soundToggleBtn');
  const soundIconOn = document.getElementById('soundIconOn');
  const soundIconOff = document.getElementById('soundIconOff');
  const cameraSelect = document.getElementById('cameraSelect');

  const numberDisplay = document.getElementById('numberDisplay');
  const numberWord = document.getElementById('numberWord');
  const confidenceVal = document.getElementById('confidenceVal');
  const confidenceBar = document.getElementById('confidenceBar');
  const handsList = document.getElementById('handsList');
  const activeHandsCount = document.getElementById('activeHandsCount');
  const handCountTag = document.getElementById('handCountTag');
  const fpsTag = document.getElementById('fpsTag');

  // --- State Variables ---
  let isStreaming = false;
  let isMirrored = true;
  let showSkeleton = true;
  let soundEnabled = true;
  let currentStream = null;
  let handsModel = null;
  let modelLoaded = false;
  let processingFrame = false;

  // Smoothing & History
  let lastStableNumber = null;
  let numberHistory = [];
  const HISTORY_SIZE = 5;

  // Performance Metrics
  let lastFrameTime = performance.now();
  let frameCount = 0;
  let currentFps = 0;
  let fpsTimer = performance.now();

  // Number Word Map
  const NUMBER_WORDS = {
    0: 'Zero (Fist)',
    1: 'One',
    2: 'Two',
    3: 'Three',
    4: 'Four',
    5: 'Five (Open Palm)',
    6: 'Six',
    7: 'Seven',
    8: 'Eight',
    9: 'Nine',
    10: 'Ten (Both Palms)'
  };

  // Hand Landmark Connections
  const HAND_CONNECTIONS = [
    // Thumb
    [0, 1], [1, 2], [2, 3], [3, 4],
    // Index
    [0, 5], [5, 6], [6, 7], [7, 8],
    // Middle
    [5, 9], [9, 10], [10, 11], [11, 12],
    // Ring
    [9, 13], [13, 14], [14, 15], [15, 16],
    // Pinky
    [13, 17], [17, 18], [18, 19], [19, 20],
    // Palm base
    [0, 17]
  ];

  // --- Audio Synthesis via Web Audio API ---
  let audioCtx = null;
  function initAudio() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        audioCtx = new AudioContext();
      }
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
  }

  function playChime(number) {
    if (!soundEnabled) return;
    try {
      initAudio();
      if (!audioCtx) return;

      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();

      // Pitch based on number (C5 to E6 pentatonic scale)
      const baseFreq = 440;
      const pitches = [440, 493.88, 554.37, 659.25, 739.99, 880, 987.77, 1108.73, 1318.51, 1479.98, 1760];
      const freq = pitches[number] || baseFreq;

      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, audioCtx.currentTime);

      gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.18);

      osc.connect(gain);
      gain.connect(audioCtx.destination);

      osc.start();
      osc.stop(audioCtx.currentTime + 0.18);
    } catch (e) {
      // Audio playback blocked or not supported
    }
  }

  // --- MediaPipe Hands Setup ---
  function initHandsModel() {
    camStatusText.innerText = 'Loading CV Model...';
    camStatusDot.className = 'status-dot processing';

    handsModel = new Hands({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
    });

    handsModel.setOptions({
      maxNumHands: 2,
      modelComplexity: 1,
      minDetectionConfidence: 0.6,
      minTrackingConfidence: 0.6
    });

    handsModel.onResults(onResults);
    modelLoaded = true;
    console.log('MediaPipe Hands Model Initialized');
  }

  // --- Euclidean Distance Helper ---
  function dist(p1, p2) {
    const dx = p1.x - p2.x;
    const dy = p1.y - p2.y;
    const dz = (p1.z || 0) - (p2.z || 0);
    return Math.sqrt(dx * dx + dy * dy + dz * dz);
  }

  // --- Finger Extension Detection Algorithm ---
  function analyzeFingers(landmarks, handednessLabel) {
    // Landmarks reference:
    // 0: Wrist, 1-4: Thumb, 5-8: Index, 9-12: Middle, 13-16: Ring, 17-20: Pinky
    const wrist = landmarks[0];
    const indexMcp = landmarks[5];
    const middleMcp = landmarks[9];
    const ringMcp = landmarks[13];
    const pinkyMcp = landmarks[17];

    const fingers = {
      thumb: false,
      index: false,
      middle: false,
      ring: false,
      pinky: false
    };

    // 1. Index Finger
    const indexTip = landmarks[8];
    const indexPip = landmarks[6];
    const indexDip = landmarks[7];
    fingers.index = (
      dist(indexTip, wrist) > dist(indexPip, wrist) * 1.15 &&
      dist(indexTip, middleMcp) > dist(indexPip, middleMcp) * 1.1 &&
      dist(indexTip, indexMcp) > dist(indexDip, indexMcp)
    );

    // 2. Middle Finger
    const middleTip = landmarks[12];
    const middlePip = landmarks[10];
    const middleDip = landmarks[11];
    fingers.middle = (
      dist(middleTip, wrist) > dist(middlePip, wrist) * 1.15 &&
      dist(middleTip, indexMcp) > dist(middlePip, indexMcp) * 1.08 &&
      dist(middleTip, middleMcp) > dist(middleDip, middleMcp)
    );

    // 3. Ring Finger
    const ringTip = landmarks[16];
    const ringPip = landmarks[14];
    const ringDip = landmarks[15];
    fingers.ring = (
      dist(ringTip, wrist) > dist(ringPip, wrist) * 1.15 &&
      dist(ringTip, middleMcp) > dist(ringPip, middleMcp) * 1.08 &&
      dist(ringTip, ringMcp) > dist(ringDip, ringMcp)
    );

    // 4. Pinky Finger
    const pinkyTip = landmarks[20];
    const pinkyPip = landmarks[18];
    const pinkyDip = landmarks[19];
    fingers.pinky = (
      dist(pinkyTip, wrist) > dist(pinkyPip, wrist) * 1.15 &&
      dist(pinkyTip, ringMcp) > dist(pinkyPip, ringMcp) * 1.1 &&
      dist(pinkyTip, pinkyMcp) > dist(pinkyDip, pinkyMcp)
    );

    // 5. Thumb Detection
    // The thumb hinges outwards sideways from the palm.
    // Compare tip (4) to IP (3), MCP (2), and Pinky MCP (17).
    const thumbTip = landmarks[4];
    const thumbIp = landmarks[3];
    const thumbMcp = landmarks[2];

    const thumbToPinkyDist = dist(thumbTip, pinkyMcp);
    const thumbIpToPinkyDist = dist(thumbIp, pinkyMcp);
    const thumbToIndexMcpDist = dist(thumbTip, indexMcp);
    const thumbIpToIndexMcpDist = dist(thumbIp, indexMcp);

    // When thumb is extended, it separates from the palm / pinky base & index base
    const thumbExtendedOutward = (
      thumbToPinkyDist > thumbIpToPinkyDist * 1.14 &&
      thumbToIndexMcpDist > thumbIpToIndexMcpDist * 1.08 &&
      dist(thumbTip, wrist) > dist(thumbMcp, wrist) * 1.15
    );

    fingers.thumb = thumbExtendedOutward;

    // Count raised fingers on this hand
    const count = Object.values(fingers).filter(Boolean).length;

    return { fingers, count };
  }

  // --- MediaPipe Results Callback ---
  function onResults(results) {
    processingFrame = false;

    // Update FPS
    frameCount++;
    const now = performance.now();
    if (now - fpsTimer >= 500) {
      currentFps = Math.round((frameCount * 1000) / (now - fpsTimer));
      fpsTag.innerText = `${currentFps} FPS`;
      frameCount = 0;
      fpsTimer = now;
    }

    // Set canvas dimensions
    if (canvasElement.width !== videoElement.videoWidth && videoElement.videoWidth > 0) {
      canvasElement.width = videoElement.videoWidth;
      canvasElement.height = videoElement.videoHeight;
    }

    const width = canvasElement.width;
    const height = canvasElement.height;

    canvasCtx.save();
    canvasCtx.clearRect(0, 0, width, height);

    // Render webcam feed to canvas
    if (isMirrored) {
      canvasCtx.translate(width, 0);
      canvasCtx.scale(-1, 1);
    }
    canvasCtx.drawImage(results.image, 0, 0, width, height);

    let totalFingers = 0;
    const detectedHandsData = [];
    let avgConfidence = 0;

    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
      const numHands = results.multiHandLandmarks.length;
      handCountTag.innerText = `Hands: ${numHands}`;

      for (let i = 0; i < numHands; i++) {
        const landmarks = results.multiHandLandmarks[i];
        const handedness = results.multiHandedness && results.multiHandedness[i] 
          ? results.multiHandedness[i] 
          : { label: i === 0 ? 'Right' : 'Left', score: 0.9 };

        // Real label accounting for mirror
        let displayHandLabel = handedness.label;
        if (!isMirrored) {
          // MediaPipe reports from camera perspective
          displayHandLabel = handedness.label === 'Right' ? 'Left' : 'Right';
        }

        const score = Math.round((handedness.score || 0.85) * 100);
        avgConfidence += score;

        const analysis = analyzeFingers(landmarks, displayHandLabel);
        totalFingers += analysis.count;

        detectedHandsData.push({
          label: displayHandLabel,
          confidence: score,
          fingers: analysis.fingers,
          count: analysis.count,
          landmarks: landmarks
        });

        // Draw Skeleton overlay if enabled
        if (showSkeleton) {
          drawHandSkeleton(canvasCtx, landmarks, analysis.fingers, width, height, isMirrored);
        }
      }

      avgConfidence = Math.round(avgConfidence / numHands);
    } else {
      handCountTag.innerText = 'Hands: 0';
    }

    canvasCtx.restore();

    // Update temporal smoothing & dashboard UI
    processTemporalNumber(results.multiHandLandmarks && results.multiHandLandmarks.length > 0 ? totalFingers : null, avgConfidence, detectedHandsData);
  }

  // --- Draw Custom Neon Hand Skeleton ---
  function drawHandSkeleton(ctx, landmarks, fingersState, width, height, mirrored) {
    const tipIndices = {
      thumb: 4,
      index: 8,
      middle: 12,
      ring: 16,
      pinky: 20
    };

    // Draw connection lines
    ctx.lineWidth = 3.5;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    for (const [startIndex, endIndex] of HAND_CONNECTIONS) {
      const p1 = landmarks[startIndex];
      const p2 = landmarks[endIndex];

      const grad = ctx.createLinearGradient(
        p1.x * width, p1.y * height,
        p2.x * width, p2.y * height
      );

      // Cyan to purple gradient for cyber feel
      grad.addColorStop(0, 'rgba(6, 182, 212, 0.7)');
      grad.addColorStop(1, 'rgba(168, 85, 247, 0.7)');

      ctx.strokeStyle = grad;
      ctx.beginPath();
      ctx.moveTo(p1.x * width, p1.y * height);
      ctx.lineTo(p2.x * width, p2.y * height);
      ctx.stroke();
    }

    // Draw Joints
    landmarks.forEach((pt, idx) => {
      const x = pt.x * width;
      const y = pt.y * height;

      // Check if this point is a fingertip
      let isTip = false;
      let isFingerUp = false;

      for (const [fingerName, tipIdx] of Object.entries(tipIndices)) {
        if (tipIdx === idx) {
          isTip = true;
          isFingerUp = fingersState[fingerName];
          break;
        }
      }

      if (isTip) {
        // Glowing fingertip ring
        ctx.beginPath();
        ctx.arc(x, y, isFingerUp ? 11 : 7, 0, 2 * Math.PI);
        ctx.fillStyle = isFingerUp ? 'rgba(16, 185, 129, 0.3)' : 'rgba(148, 163, 184, 0.2)';
        ctx.fill();

        ctx.beginPath();
        ctx.arc(x, y, isFingerUp ? 7 : 4.5, 0, 2 * Math.PI);
        ctx.fillStyle = isFingerUp ? '#10b981' : '#64748b';
        ctx.shadowColor = isFingerUp ? '#10b981' : 'transparent';
        ctx.shadowBlur = isFingerUp ? 14 : 0;
        ctx.fill();
        ctx.shadowBlur = 0; // Reset
      } else {
        // Standard Joint
        ctx.beginPath();
        ctx.arc(x, y, 3.8, 0, 2 * Math.PI);
        ctx.fillStyle = '#00f0ff';
        ctx.shadowColor = '#00f0ff';
        ctx.shadowBlur = 6;
        ctx.fill();
        ctx.shadowBlur = 0;
      }
    });
  }

  // --- Temporal Smoothing & UI Update ---
  function processTemporalNumber(rawCount, confidence, detectedHands) {
    if (rawCount === null) {
      // No hands in frame
      numberHistory = [];
      numberDisplay.innerText = '-';
      numberWord.innerText = 'Waiting for hand...';
      confidenceVal.innerText = '0%';
      confidenceBar.style.width = '0%';
      activeHandsCount.innerText = '0 Active';
      renderEmptyHands();
      clearLegendHighlights();
      lastStableNumber = null;
      return;
    }

    // Add to rolling history
    numberHistory.push(rawCount);
    if (numberHistory.length > HISTORY_SIZE) {
      numberHistory.shift();
    }

    // Determine mode (majority vote)
    const frequency = {};
    let maxFreq = 0;
    let stableNumber = rawCount;

    for (const num of numberHistory) {
      frequency[num] = (frequency[num] || 0) + 1;
      if (frequency[num] > maxFreq) {
        maxFreq = frequency[num];
        stableNumber = num;
      }
    }

    // Update Number Display with animation if changed
    if (lastStableNumber !== stableNumber) {
      numberDisplay.innerText = stableNumber;
      numberDisplay.classList.remove('pop');
      void numberDisplay.offsetWidth; // Trigger reflow
      numberDisplay.classList.add('pop');

      numberWord.innerText = NUMBER_WORDS[stableNumber] || `${stableNumber} Fingers`;
      highlightLegend(stableNumber);
      playChime(stableNumber);

      lastStableNumber = stableNumber;
    }

    // Update Confidence
    confidenceVal.innerText = `${confidence}%`;
    confidenceBar.style.width = `${confidence}%`;

    // Update Active Hands Breakdown
    activeHandsCount.innerText = `${detectedHands.length} Active`;
    renderHandsList(detectedHands);
  }

  // --- Render Detected Hands Breakdown Card ---
  function renderHandsList(hands) {
    if (!hands || hands.length === 0) {
      renderEmptyHands();
      return;
    }

    handsList.innerHTML = '';
    hands.forEach((hand, idx) => {
      const row = document.createElement('div');
      row.className = 'hand-row';

      const fingers = hand.fingers;
      const fingerNames = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky'];

      const chipsHtml = fingerNames.map(fName => {
        const key = fName.toLowerCase();
        const active = fingers[key];
        return `
          <div class="finger-chip ${active ? 'active' : ''}">
            <span class="chip-name">${fName.slice(0, 3)}</span>
            <span class="chip-status"></span>
          </div>
        `;
      }).join('');

      row.innerHTML = `
        <div class="hand-row-header">
          <span class="hand-name">
            <span>${hand.label} Hand</span>
          </span>
          <span class="hand-subcount">${hand.count} / 5 fingers</span>
        </div>
        <div class="finger-chips-grid">
          ${chipsHtml}
        </div>
      `;

      handsList.appendChild(row);
    });
  }

  function renderEmptyHands() {
    handsList.innerHTML = `
      <div class="empty-hands-msg">
        <span class="hand-wave-icon">🖐️</span>
        <p>Place one or both hands in front of the lens. Make a fist for 0, or raise fingers for 1 to 10.</p>
      </div>
    `;
  }

  // --- Highlight Quick Legend ---
  function highlightLegend(number) {
    const items = document.querySelectorAll('.legend-item');
    items.forEach(item => {
      const numAttr = item.getAttribute('data-num');
      if (numAttr === String(number) || (number >= 6 && numAttr === '6-10')) {
        item.classList.add('highlight');
      } else {
        item.classList.remove('highlight');
      }
    });
  }

  function clearLegendHighlights() {
    const items = document.querySelectorAll('.legend-item');
    items.forEach(item => item.classList.remove('highlight'));
  }

  // --- Video Frame Processing Loop ---
  async function renderFrame() {
    if (!isStreaming) return;

    if (videoElement.readyState >= 2 && !processingFrame && modelLoaded) {
      processingFrame = true;
      try {
        await handsModel.send({ image: videoElement });
      } catch (err) {
        console.error('Hand frame detection error:', err);
        processingFrame = false;
      }
    }

    if (isStreaming) {
      requestAnimationFrame(renderFrame);
    }
  }

  // --- Camera Management ---
  async function populateCameraDevices() {
    try {
      const devices = await navigator.mediaDevices.enumerateDevices();
      const videoDevices = devices.filter(device => device.kind === 'videoinput');

      cameraSelect.innerHTML = '';
      if (videoDevices.length === 0) {
        cameraSelect.innerHTML = '<option value="">Default Camera</option>';
        return;
      }

      videoDevices.forEach((device, index) => {
        const option = document.createElement('option');
        option.value = device.deviceId;
        option.text = device.label || `Camera ${index + 1}`;
        cameraSelect.appendChild(option);
      });
    } catch (e) {
      console.warn('Could not enumerate video devices:', e);
    }
  }

  async function startCamera(deviceId = null) {
    initAudio();

    if (!modelLoaded) {
      initHandsModel();
    }

    camStatusText.innerText = 'Connecting camera...';
    camStatusDot.className = 'status-dot processing';

    if (currentStream) {
      currentStream.getTracks().forEach(track => track.stop());
    }

    const constraints = {
      video: {
        width: { ideal: 1280 },
        height: { ideal: 720 },
        deviceId: deviceId ? { exact: deviceId } : undefined
      },
      audio: false
    };

    try {
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      currentStream = stream;
      videoElement.srcObject = stream;

      await new Promise((resolve) => {
        videoElement.onloadedmetadata = () => {
          videoElement.play();
          resolve();
        };
      });

      isStreaming = true;
      standbyOverlay.classList.add('hidden');
      hudOverlay.classList.remove('hidden');

      camStatusText.innerText = 'Live Tracking';
      camStatusDot.className = 'status-dot active';

      cameraBtnText.innerText = 'Stop Camera';
      cameraToggleBtn.classList.add('btn-active');

      await populateCameraDevices();
      requestAnimationFrame(renderFrame);
    } catch (err) {
      console.error('Webcam Access Error:', err);
      camStatusText.innerText = 'Camera Error / Blocked';
      camStatusDot.className = 'status-dot';
      alert('Unable to access camera. Please make sure webcam permissions are granted.');
    }
  }

  function stopCamera() {
    isStreaming = false;
    if (currentStream) {
      currentStream.getTracks().forEach(track => track.stop());
      currentStream = null;
    }
    videoElement.srcObject = null;

    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    standbyOverlay.classList.remove('hidden');
    hudOverlay.classList.add('hidden');

    camStatusText.innerText = 'Camera Standby';
    camStatusDot.className = 'status-dot';

    cameraBtnText.innerText = 'Start Camera';
    cameraToggleBtn.classList.remove('btn-active');

    processTemporalNumber(null, 0, []);
  }

  // --- Event Listeners ---
  cameraToggleBtn.addEventListener('click', () => {
    if (isStreaming) {
      stopCamera();
    } else {
      const selectedId = cameraSelect.value || null;
      startCamera(selectedId);
    }
  });

  startHeroBtn.addEventListener('click', () => {
    const selectedId = cameraSelect.value || null;
    startCamera(selectedId);
  });

  mirrorToggleBtn.addEventListener('click', () => {
    isMirrored = !isMirrored;
    mirrorToggleBtn.classList.toggle('active', isMirrored);
  });

  skeletonToggleBtn.addEventListener('click', () => {
    showSkeleton = !showSkeleton;
    skeletonToggleBtn.classList.toggle('active', showSkeleton);
  });

  soundToggleBtn.addEventListener('click', () => {
    soundEnabled = !soundEnabled;
    soundIconOn.classList.toggle('hidden', !soundEnabled);
    soundIconOff.classList.toggle('hidden', soundEnabled);
    if (soundEnabled) {
      playChime(5); // Preview tone
    }
  });

  cameraSelect.addEventListener('change', () => {
    if (isStreaming) {
      startCamera(cameraSelect.value);
    }
  });

  // Pre-populate devices list on initial page load if permissions allow
  if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
    populateCameraDevices();
  }

})();
