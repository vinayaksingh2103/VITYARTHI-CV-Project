import os
import sys
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        if self._pageNumber == 1:
            return  # Skip cover page
        self.saveState()
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Running header
        self.drawString(54, 800, "VisionCount AI - Comprehensive Project Report")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 792, 540, 792)
        
        # Running footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(540, 36, page_text)
        self.drawString(54, 36, "Confidential & Academic Submission - Mayank Kailas Tiwari")
        self.line(54, 48, 540, 48)
        self.restoreState()

def build_pdf():
    pdf_filename = "Project_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=48,
        rightMargin=48,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    primary_color = colors.HexColor("#0F172A")
    accent_color = colors.HexColor("#0284C7")
    text_color = colors.HexColor("#1E293B")
    muted_color = colors.HexColor("#64748B")
    card_bg = colors.HexColor("#F8FAFC")

    title_style = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=primary_color,
        alignment=0,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        fontName='Helvetica',
        fontSize=12,
        leading=17,
        textColor=muted_color,
        alignment=0,
        spaceAfter=24
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=accent_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=text_color,
        spaceAfter=7
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=text_color,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F172A")
    )

    caption_style = ParagraphStyle(
        'Caption_Custom',
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=muted_color,
        alignment=1,
        spaceAfter=10
    )

    callout_style = ParagraphStyle(
        'Callout_Custom',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#0369A1")
    )

    story = []

    # ==================== 1. COVER PAGE ====================
    story.append(Spacer(1, 30))
    
    # Badge
    badge_data = [[Paragraph("<b>OFFICIAL PROJECT REPORT SUBMISSION</b>", ParagraphStyle('B', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.white))]]
    badge_table = Table(badge_data, colWidths=[240])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), accent_color),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('CORNERPAD', (0,0), (-1,-1), 4),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 16))

    story.append(Paragraph("VisionCount AI", title_style))
    story.append(Paragraph("Real-Time Client-Side Computer Vision System for Finger-Based Number Recognition (0–10) Utilizing MediaPipe Hands and Pure Web Architecture", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=accent_color, spaceBefore=0, spaceAfter=25))

    # Meta Table
    meta_info = [
        [Paragraph("<b>Project Domain:</b>", body_style), Paragraph("Computer Vision, Edge AI, Human-Computer Interaction (HCI)", body_style)],
        [Paragraph("<b>Target Platform:</b>", body_style), Paragraph("Cross-Platform Web Browser (Desktop & Mobile)", body_style)],
        [Paragraph("<b>Core Technology:</b>", body_style), Paragraph("HTML5, CSS3, Vanilla JavaScript (ES6+), MediaPipe Hands", body_style)],
        [Paragraph("<b>Execution Model:</b>", body_style), Paragraph("100% Client-Side WebAssembly (Wasm) & WebGL (Zero Backend)", body_style)],
        [Paragraph("<b>Author / Developer:</b>", body_style), Paragraph("Mayank Kailas Tiwari", body_style)],
        [Paragraph("<b>Repository:</b>", body_style), Paragraph("https://github.com/mayank-aiml/VITYARTHI-CV-Project.git", body_style)],
        [Paragraph("<b>Submission Date:</b>", body_style), Paragraph("September 2026", body_style)],
        [Paragraph("<b>Document Version:</b>", body_style), Paragraph("1.0 (Production Release)", body_style)]
    ]
    meta_table = Table(meta_info, colWidths=[140, 350])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), card_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 40))
    abstract_text = (
        "<b>Executive Abstract:</b> VisionCount AI demonstrates a touchless, high-performance computer vision "
        "application that translates real-time human hand gestures into numerical digits from 0 to 10. "
        "Engineered with zero third-party UI frameworks and zero server dependencies, all video capture, deep learning "
        "landmark extraction, geometric classification heuristics, temporal jitter filtering, and audio synthesis run "
        "strictly inside client browser memory at 30–60 FPS. This report details the architecture, design diagrams, "
        "implementation mechanics, testing strategies, and challenges encountered."
    )
    abstract_table = Table([[Paragraph(abstract_text, callout_style)]], colWidths=[490])
    abstract_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0F9FF")),
        ('LINELEFT', (0,0), (-1,-1), 3.5, accent_color),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(abstract_table)

    story.append(PageBreak())

    # ==================== 2. INTRODUCTION ====================
    story.append(Paragraph("2. Introduction", h1_style))
    story.append(Paragraph(
        "Human-Computer Interaction (HCI) has evolved rapidly from text-based command interfaces to graphical "
        "desktop windows, touch surfaces, and now natural perceptual user interfaces. Hand gestures represent "
        "one of the most universal, expressive, and instinctive forms of human communication. Specifically, "
        "counting on fingers is taught in early childhood across cultures and serves as a primary non-verbal "
        "signaling mechanism in daily life.",
        body_style
    ))
    story.append(Paragraph(
        "Historically, real-time hand gesture tracking was constrained to dedicated sensor hardware (e.g., Leap Motion, "
        "Microsoft Kinect) or high-latency client-server architectures where camera feeds were streamed over "
        "WebSockets to Python servers running heavy OpenCV/PyTorch models. These approaches introduced substantial latency, "
        "bandwidth consumption, and profound privacy vulnerabilities.",
        body_style
    ))
    story.append(Paragraph(
        "<b>VisionCount AI</b> bridges this gap by introducing a lightweight, instant-loading web application "
        "written in pure HTML5, CSS3, and Vanilla JavaScript. By embedding Google MediaPipe Hands through WebAssembly "
        "and WebGL acceleration, the entire 21-landmark neural network executes on the client device's GPU/CPU. "
        "The system delivers real-time gesture counting from 0 (closed fist) to 10 (both open hands) with sub-35ms latency, "
        "zero server costs, and absolute data privacy.",
        body_style
    ))

    # ==================== 3. PROBLEM STATEMENT ====================
    story.append(Paragraph("3. Problem Statement", h1_style))
    story.append(Paragraph(
        "Conventional physical input devices (keyboards, mice, and touchscreens) face significant limitations across "
        "specialized operational environments and user demographics:",
        body_style
    ))
    story.append(Paragraph("• <b>Sanitary & Sterile Environments:</b> In healthcare facilities, surgical theaters, cleanrooms, and public kiosks, physical touch surfaces become vectors for pathogen contamination.", bullet_style))
    story.append(Paragraph("• <b>Accessibility Barriers:</b> Individuals with vocal or physical motor impairments frequently encounter friction using standard keyboards. Vision-based finger count detection provides an accessible, non-contact signaling channel.", bullet_style))
    story.append(Paragraph("• <b>Cloud CV Privacy & Bandwidth:</b> Streaming video feeds to remote cloud servers exposes sensitive personal visual data to interception and server storage while demanding high continuous bandwidth.", bullet_style))
    story.append(Paragraph("• <b>Setup Friction:</b> Traditional CV projects require Python environments, CUDA drivers, and heavy dependencies, preventing everyday users from running solutions easily.", bullet_style))

    # ==================== 4. FUNCTIONAL REQUIREMENTS ====================
    story.append(Paragraph("4. Functional Requirements", h1_style))
    fr_data = [
        [Paragraph("<b>Req ID</b>", body_style), Paragraph("<b>Functionality</b>", body_style), Paragraph("<b>Description</b>", body_style)],
        [Paragraph("<b>FR-01</b>", body_style), Paragraph("Webcam Stream Ingestion", body_style), Paragraph("Capture real-time video frames via <code>navigator.mediaDevices.getUserMedia</code> at up to 720p.", body_style)],
        [Paragraph("<b>FR-02</b>", body_style), Paragraph("3D Landmark Extraction", body_style), Paragraph("Extract 21 landmark coordinates (X, Y, Z) per hand using MediaPipe Hands WebAssembly runtime.", body_style)],
        [Paragraph("<b>FR-03</b>", body_style), Paragraph("Geometric Digit Classification", body_style), Paragraph("Compute vector distances to determine state (extended vs. folded) for all 5 fingers independently.", body_style)],
        [Paragraph("<b>FR-04</b>", body_style), Paragraph("Dual-Hand Identification (0–10)", body_style), Paragraph("Track up to 2 hands simultaneously and aggregate total raised fingers from 0 to 10.", body_style)],
        [Paragraph("<b>FR-05</b>", body_style), Paragraph("Temporal Jitter Filtering", body_style), Paragraph("Apply rolling-window majority voting over last 5 frames to eliminate frame-by-frame flickering.", body_style)],
        [Paragraph("<b>FR-06</b>", body_style), Paragraph("Cyber-Glass HUD & Skeleton", body_style), Paragraph("Render glowing neon connections and color-coded extended fingertip rings on HTML5 Canvas.", body_style)],
        [Paragraph("<b>FR-07</b>", body_style), Paragraph("Harmonic Audio Feedback", body_style), Paragraph("Synthesize pleasant tonal chimes via Web Audio API when a new stable number is identified.", body_style)],
        [Paragraph("<b>FR-08</b>", body_style), Paragraph("Viewport Controls", body_style), Paragraph("Provide camera device selection, horizontal mirror toggle, and skeleton overlay toggle.", body_style)]
    ]
    fr_table = Table(fr_data, colWidths=[55, 135, 300])
    fr_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(fr_table)

    # ==================== 5. NON-FUNCTIONAL REQUIREMENTS ====================
    story.append(Paragraph("5. Non-functional Requirements", h1_style))
    nfr_data = [
        [Paragraph("<b>Category</b>", body_style), Paragraph("<b>Target Metric</b>", body_style), Paragraph("<b>Implementation & Validation</b>", body_style)],
        [Paragraph("<b>Performance & Latency</b>", body_style), Paragraph("&lt; 35ms latency, 30–60 FPS", body_style), Paragraph("Validated with live on-screen FPS/telemetry counter on consumer laptops.", body_style)],
        [Paragraph("<b>Data Privacy</b>", body_style), Paragraph("100% Local Execution", body_style), Paragraph("Zero outbound network telemetry. Frames are processed solely in volatile client RAM.", body_style)],
        [Paragraph("<b>Zero Installation</b>", body_style), Paragraph("Pure Static Web Bundle", body_style), Paragraph("HTML/CSS/JS deployable instantly to GitHub Pages, Netlify, or local web server.", body_style)],
        [Paragraph("<b>Cross-Browser Support</b>", body_style), Paragraph("All Modern Browsers", body_style), Paragraph("Verified on Google Chrome, Microsoft Edge, and Safari using standard Web APIs.", body_style)]
    ]
    nfr_table = Table(nfr_data, colWidths=[110, 110, 270])
    nfr_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(nfr_table)

    story.append(PageBreak())

    # ==================== 6. SYSTEM ARCHITECTURE ====================
    story.append(Paragraph("6. System Architecture", h1_style))
    story.append(Paragraph(
        "VisionCount AI implements an asynchronous, event-driven pipeline divided into four clear tiers: "
        "<b>Hardware Ingestion</b>, <b>Neural Perception</b>, <b>Mathematical Classification</b>, and <b>Presentation/Audio HUD</b>.",
        body_style
    ))
    
    arch_box = [
        [Paragraph("<b>[Layer 1: Video Ingestion]</b><br/>Webcam Stream &bull; navigator.mediaDevices.getUserMedia() &bull; Resolution negotiation (1280x720)", body_style)],
        [Paragraph("<b>&darr; Frame Delivery via requestAnimationFrame()</b>", caption_style)],
        [Paragraph("<b>[Layer 2: Neural Landmark Regression (MediaPipe Hands)]</b><br/>Wasm/WebGL Execution &bull; Palm Detector &bull; Hand Landmark Model &bull; 21 3D Coordinates (X, Y, Z)", body_style)],
        [Paragraph("<b>&darr; Normalized Landmark Vectors</b>", caption_style)],
        [Paragraph("<b>[Layer 3: Geometric Classification & Temporal Filter]</b><br/>3D Euclidean Distance Ratio Engine &bull; Thumb Abduction Check &bull; 5-Frame Rolling Majority Voting", body_style)],
        [Paragraph("<b>&darr; Filtered Number & Hand Breakdown</b>", caption_style)],
        [Paragraph("<b>[Layer 4: Glassmorphic Presentation & Audio Engine]</b><br/>HTML5 Canvas Mesh Rendering &bull; Big Animated Number Badge &bull; Web Audio API Harmonic Synthesis", body_style)]
    ]
    arch_table = Table(arch_box, colWidths=[490])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E0F2FE")),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#F3E8FF")),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor("#DCFCE7")),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#FEF9C3")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94A3B8")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 10))

    # ==================== 7. DESIGN DIAGRAMS ====================
    story.append(Paragraph("7. Design Diagrams", h1_style))

    # 7.1 Use Case Diagram
    story.append(Paragraph("7.1 Use Case Diagram", h2_style))
    uc_text = (
        "<b>Use Cases Defined:</b><br/>"
        "• <b>UC-1 (Start/Stop Video Stream):</b> User initiates webcam stream and camera hardware initialization.<br/>"
        "• <b>UC-2 (Present Finger Gestures):</b> User displays 0 to 10 fingers in camera field of view.<br/>"
        "• <b>UC-3 (Inspect Identified Number):</b> System displays animated number, word label, and confidence score.<br/>"
        "• <b>UC-4 (Toggle Viewport Settings):</b> User switches input webcam, toggles mirror view, or toggles skeleton mesh.<br/>"
        "• <b>UC-5 (Audio Tone Feedback):</b> System generates tonal feedback on detected count transition."
    )
    story.append(Table([[Paragraph(uc_text, body_style)]], colWidths=[490], style=[
        ('BACKGROUND', (0,0), (-1,-1), card_bg),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(Spacer(1, 10))

    # 7.2 Workflow Diagram
    story.append(Paragraph("7.2 Workflow Diagram", h2_style))
    wf_text = (
        "<b>Execution Flow:</b><br/>"
        "<b>[User clicks 'Launch Camera']</b> &rarr; [Prompt Media Permission] &rarr; [Load MediaPipe Wasm Binaries] &rarr; "
        "<br/>&rarr; <b>[Loop Start]</b> &rarr; [Capture Video Frame] &rarr; [Regress 21 Landmarks] &rarr; "
        "[Calculate Euclidean Distance Ratios] &rarr; [Evaluate Finger States] &rarr; [Push to 5-Frame Rolling Window] &rarr; "
        "[Determine Modal Count] &rarr; [Render Skeleton & Draw Frame] &rarr; [Play Chime if Count Changed] &rarr; <b>[Repeat Frame]</b>"
    )
    story.append(Table([[Paragraph(wf_text, body_style)]], colWidths=[490], style=[
        ('BACKGROUND', (0,0), (-1,-1), card_bg),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(Spacer(1, 10))

    # 7.3 Sequence Diagram
    story.append(Paragraph("7.3 Sequence Diagram", h2_style))
    seq_text = (
        "1. <b>User &rarr; UI Controller:</b> Click 'Start Camera'.<br/>"
        "2. <b>UI Controller &rarr; Navigator MediaDevices:</b> <code>getUserMedia({video: {width: 1280, height: 720}})</code>.<br/>"
        "3. <b>Navigator MediaDevices &rarr; HTML5 Video Element:</b> Return active MediaStream object.<br/>"
        "4. <b>Video Element &rarr; MediaPipe Hands Wasm:</b> <code>handsModel.send({image: videoElement})</code>.<br/>"
        "5. <b>MediaPipe Hands &rarr; Classifier:</b> Trigger <code>onResults()</code> with <code>multiHandLandmarks</code> array.<br/>"
        "6. <b>Classifier &rarr; Smoothing Buffer:</b> Pass instantaneous integer finger sum.<br/>"
        "7. <b>Smoothing Buffer &rarr; Dashboard & Canvas:</b> Render neon skeleton and animated numeric display.<br/>"
        "8. <b>Smoothing Buffer &rarr; Web Audio API:</b> Trigger oscillator pitch chime on state change."
    )
    story.append(Table([[Paragraph(seq_text, body_style)]], colWidths=[490], style=[
        ('BACKGROUND', (0,0), (-1,-1), card_bg),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(Spacer(1, 10))

    # 7.4 Class / Component Diagram
    story.append(Paragraph("7.4 Class / Component Diagram", h2_style))
    comp_text = (
        "• <b>CameraStreamManager:</b> Manages MediaStream lifecycle, device enumeration, and track termination.<br/>"
        "• <b>LandmarkDetector:</b> Wraps MediaPipe Hands instance and configures detection/tracking thresholds (0.6).<br/>"
        "• <b>FingerGeometryClassifier:</b> Contains <code>dist()</code> and geometric logic for index, middle, ring, pinky, and thumb.<br/>"
        "• <b>TemporalSmoother:</b> Implements rolling FIFO array (size=5) and computes frequency-based modal vote.<br/>"
        "• <b>CanvasRenderer:</b> Executes 2D canvas drawing, coordinate scaling, mirroring transforms, and neon glow filters.<br/>"
        "• <b>AudioSynthesizer:</b> Generates sine-wave oscillator tones with exponential gain decay via Web Audio API."
    )
    story.append(Table([[Paragraph(comp_text, body_style)]], colWidths=[490], style=[
        ('BACKGROUND', (0,0), (-1,-1), card_bg),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(Spacer(1, 10))

    # 7.5 Entity / State Data Model
    story.append(Paragraph("7.5 Entity & Ephemeral State Model (Client-Side Storage)", h2_style))
    story.append(Paragraph(
        "Because VisionCount AI is privacy-first, <b>zero persistent database or file storage</b> is used. "
        "All data exists as ephemeral JavaScript state objects inside memory during active streaming:",
        body_style
    ))
    storage_data = [
        [Paragraph("<b>Entity Object</b>", body_style), Paragraph("<b>Key Attributes</b>", body_style), Paragraph("<b>Scope & Retention</b>", body_style)],
        [Paragraph("<b>RawVideoFrame</b>", body_style), Paragraph("width, height, timestamp, pixelBuffer", body_style), Paragraph("Per-frame lifecycle, discarded after inference", body_style)],
        [Paragraph("<b>HandLandmarkSet</b>", body_style), Paragraph("21 points {x, y, z}, handedness, score", body_style), Paragraph("In-memory callback lifecycle", body_style)],
        [Paragraph("<b>HandAnalysisResult</b>", body_style), Paragraph("thumb, index, middle, ring, pinky (boolean)", body_style), Paragraph("Computed per frame per hand", body_style)],
        [Paragraph("<b>TemporalBuffer</b>", body_style), Paragraph("history[5], modalCount, confidenceAvg", body_style), Paragraph("Active streaming session state", body_style)]
    ]
    storage_table = Table(storage_data, colWidths=[120, 190, 180])
    storage_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(storage_table)

    story.append(PageBreak())

    # ==================== 8. DESIGN DECISIONS & RATIONALE ====================
    story.append(Paragraph("8. Design Decisions & Rationale", h1_style))
    dd_data = [
        [Paragraph("<b>Architectural Decision</b>", body_style), Paragraph("<b>Alternative Evaluated</b>", body_style), Paragraph("<b>Technical Justification</b>", body_style)],
        [Paragraph("<b>Vanilla Web Architecture</b>", body_style), Paragraph("React / Next.js / Vue", body_style), Paragraph("Eliminates node_modules bloat, build steps, and hydration overhead. Loads instantly on any static file server.", body_style)],
        [Paragraph("<b>Client-Side Wasm Inference</b>", body_style), Paragraph("Flask / FastAPI OpenCV Server", body_style), Paragraph("Zero cloud hosting costs, sub-35ms latency, and 100% privacy compliance without external video streaming.", body_style)],
        [Paragraph("<b>3D Vector Distance Ratio</b>", body_style), Paragraph("Absolute Y-coordinate check (tip.y &lt; pip.y)", body_style), Paragraph("Absolute Y checks fail when hands are tilted or inverted. Distance ratios from the wrist are rotation-invariant.", body_style)],
        [Paragraph("<b>5-Frame Majority Filter</b>", body_style), Paragraph("Unfiltered raw frame data", body_style), Paragraph("Eliminates single-frame tracking oscillations caused by hand tremor or camera sensor noise.", body_style)],
        [Paragraph("<b>Synthetic Web Audio API</b>", body_style), Paragraph("Static MP3 audio clips", body_style), Paragraph("Zero download footprint; dynamic microtonal frequencies mapped cleanly across numbers 0 through 10.", body_style)]
    ]
    dd_table = Table(dd_data, colWidths=[120, 140, 230])
    dd_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(dd_table)

    # ==================== 9. IMPLEMENTATION DETAILS ====================
    story.append(Paragraph("9. Implementation Details", h1_style))
    story.append(Paragraph(
        "<b>1. Mathematical Distance Metric:</b> 3D Euclidean distances between landmark points are computed as:<br/>"
        "<code>dist(p1, p2) = sqrt((x1 - x2)^2 + (y1 - y2)^2 + (z1 - z2)^2)</code>",
        body_style
    ))
    story.append(Paragraph(
        "<b>2. Multi-Finger Extension Heuristics:</b><br/>"
        "• <b>Index, Middle, Ring, Pinky:</b> A finger is marked <code>true</code> if:<br/>"
        "<code>dist(tip, wrist) &gt; dist(pip, wrist) * 1.15 AND dist(tip, mcp_adjacent) &gt; dist(pip, mcp_adjacent) * 1.08</code>.<br/>"
        "• <b>Thumb Abduction:</b> The thumb articulates laterally away from the palm. The system measures separation from Pinky MCP (17) and Index MCP (5):<br/>"
        "<code>dist(thumbTip, pinkyMcp) &gt; dist(thumbIp, pinkyMcp) * 1.14 AND dist(thumbTip, wrist) &gt; dist(thumbMcp, wrist) * 1.15</code>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>3. Rolling Window Modal Filter:</b><br/>"
        "Raw frame counts are accumulated in a FIFO array of length 5. A frequency histogram is computed each frame, "
        "and the modal number is presented to the user. State transitions trigger the visual 'pop' animation and audio chime.",
        body_style
    ))

    # ==================== 10. SCREENSHOTS / RESULTS ====================
    story.append(Paragraph("10. Screenshots / Results", h1_style))
    story.append(Paragraph("Below are photographic records of the live execution in browser:", body_style))

    img_path1 = os.path.abspath("assets/screenshot1.png")
    img_path2 = os.path.abspath("assets/screenshot2.png")

    if os.path.exists(img_path1):
        story.append(Image(img_path1, width=6.5*inch, height=3.5*inch))
        story.append(Paragraph("Figure 7: Main GUI with Live Viewport, Camera HUD, and Metric Telemetry", caption_style))
        story.append(Spacer(1, 10))

    if os.path.exists(img_path2):
        story.append(Image(img_path2, width=6.5*inch, height=1.6*inch))
        story.append(Paragraph("Figure 8: Quick Gesture Cheat-Sheet for Numbers 0 through 10", caption_style))
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # ==================== 11. TESTING APPROACH ====================
    story.append(Paragraph("11. Testing Approach", h1_style))
    test_data = [
        [Paragraph("<b>Test Case Category</b>", body_style), Paragraph("<b>Test Procedure</b>", body_style), Paragraph("<b>Observed Result</b>", body_style)],
        [Paragraph("<b>Single Hand (0 to 5)</b>", body_style), Paragraph("Present fist (0), single finger (1), peace sign (2), three (3), four (4), and open palm (5).", body_style), Paragraph("100% correct classification with immediate visual feedback.", body_style)],
        [Paragraph("<b>Two Hands (6 to 10)</b>", body_style), Paragraph("Present 5 on left hand + 1 on right (6) up to 5 on left + 5 on right (10).", body_style), Paragraph("Seamless dual-hand tracking and correct summed count.", body_style)],
        [Paragraph("<b>Rotational Invariance</b>", body_style), Paragraph("Rotate hand laterally 45° and 90° relative to camera axis.", body_style), Paragraph("Accurate counts maintained due to wrist distance ratios.", body_style)],
        [Paragraph("<b>Camera Switching</b>", body_style), Paragraph("Select different cameras from device selector dropdown.", body_style), Paragraph("Active stream stopped, new hardware initialized cleanly.", body_style)],
        [Paragraph("<b>Audio Toggle</b>", body_style), Paragraph("Mute/unmute sound feedback button.", body_style), Paragraph("AudioContext suspended/resumed without thread interruption.", body_style)]
    ]
    test_table = Table(test_data, colWidths=[120, 200, 170])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(test_table)

    # ==================== 12. CHALLENGES FACED ====================
    story.append(Paragraph("12. Challenges Faced", h1_style))
    story.append(Paragraph("• <b>Thumb Flexion vs. Abduction:</b> The thumb does not articulate vertically toward the wrist. Simple Y-axis checks misclassified curled thumbs as extended. <i>Solution:</i> Implemented comparative Euclidean distance ratios relative to Pinky MCP (17) and Index MCP (5).", bullet_style))
    story.append(Paragraph("• <b>Webcam Mirroring Alignment:</b> Unmirrored camera feeds confuse human users during spatial alignment. <i>Solution:</i> Applied horizontal canvas mirroring (<code>scale(-1, 1)</code>) while dynamically inverting MediaPipe handedness labels (Left vs. Right) to maintain intuitive user experience.", bullet_style))
    story.append(Paragraph("• <b>Boundary Flickering:</b> Fingers held halfway extended produced rapid count toggling. <i>Solution:</i> Developed an in-memory 5-frame rolling majority voting filter that smoothed transitions without perceivable latency.", bullet_style))

    # ==================== 13. LEARNINGS & KEY TAKEAWAYS ====================
    story.append(Paragraph("13. Learnings & Key Takeaways", h1_style))
    story.append(Paragraph("• <b>WebAssembly Transforms Edge AI:</b> Neural networks that previously required dedicated desktop installations can now run directly inside sandboxed browsers at full frame rates.", bullet_style))
    story.append(Paragraph("• <b>Heuristics + Deep Learning Synergy:</b> Combining neural regression (finding 21 landmarks) with deterministic vector geometry (distance checks) provides an optimal balance between accuracy and computational speed.", bullet_style))
    story.append(Paragraph("• <b>Zero-Framework Efficiency:</b> Vanilla HTML, CSS, and JavaScript provide clean codebases with zero dependency vulnerabilities and instant deployment.", bullet_style))

    # ==================== 14. FUTURE ENHANCEMENTS ====================
    story.append(Paragraph("14. Future Enhancements", h1_style))
    story.append(Paragraph("• <b>Touch-Free Gesture Calculator:</b> Allow users to present two numbers separated by an operator gesture (e.g., peace sign for addition, thumbs up for equals) to perform touch-free arithmetic.", bullet_style))
    story.append(Paragraph("• <b>Continuous Dynamic Gestures:</b> Implement motion trajectory analysis to detect air-writing, swiping, and pinch-to-zoom gestures.", bullet_style))
    story.append(Paragraph("• <b>Multilingual Voice Output:</b> Integrate the browser Web Speech API to synthesize spoken number pronunciation in multiple languages.", bullet_style))

    # ==================== 15. REFERENCES ====================
    story.append(Paragraph("15. References", h1_style))
    story.append(Paragraph("1. Lugaresi, C., et al. 'MediaPipe: A Framework for Building Perception Pipelines.' <i>arXiv preprint arXiv:1906.08172</i> (2019).", body_style))
    story.append(Paragraph("2. Zhang, F., et al. 'MediaPipe Hands: On-device Real-time Hand Tracking.' <i>CVPR Workshop on Computer Vision for AR/VR</i> (2020).", body_style))
    story.append(Paragraph("3. W3C Media Capture and Streams Working Group. 'Media Capture and Streams (getUserMedia).' <i>W3C Recommendation</i> (2022).", body_style))
    story.append(Paragraph("4. W3C Audio Working Group. 'Web Audio API.' <i>W3C Recommendation</i> (2021).", body_style))
    story.append(Paragraph("5. Google Developers. 'MediaPipe Solutions - Hand Landmark Detection Guide.' https://developers.google.com/mediapipe/solutions/vision/hand_landmarker", body_style))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Project Report PDF generated successfully: {pdf_filename}")

if __name__ == "__main__":
    build_pdf()
