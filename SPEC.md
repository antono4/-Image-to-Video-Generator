# Video Generator from Image - Specification

## 1. Project Overview

**Project Name:** ImageMotion  
**Type:** Web Application (Streamlit-based)  
**Core Functionality:** Upload images and generate animated videos with various motion effects (zoom, pan, Ken Burns effect, etc.)  
**Target Users:** Content creators, social media managers, photographers who need quick animated visuals

## 2. UI/UX Specification

### Layout Structure

```
┌─────────────────────────────────────────────────────────┐
│  HEADER (Logo + Title)                                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────┐  ┌─────────────────────────────┐  │
│  │                 │  │                             │  │
│  │   Image Upload  │  │      Video Preview          │  │
│  │   Area          │  │      (Output)               │  │
│  │                 │  │                             │  │
│  └─────────────────┘  └─────────────────────────────┘  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Animation Controls                               │   │
│  │  - Effect Type (dropdown)                         │   │
│  │  - Duration (slider)                             │   │
│  │  - Zoom Level (slider)                           │   │
│  │  - Direction (radio buttons)                     │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  [Generate Video]  [Download Video]                      │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  FOOTER                                                 │
└─────────────────────────────────────────────────────────┘
```

### Responsive Breakpoints
- Desktop: > 1024px (two-column layout)
- Tablet/Mobile: <= 1024px (single-column stacked layout)

### Visual Design

**Color Palette:**
- Primary: `#6366F1` (Indigo)
- Secondary: `#8B5CF6` (Purple)
- Accent: `#EC4899` (Pink)
- Background: `#0F0F23` (Deep Navy)
- Surface: `#1A1A2E` (Dark Card)
- Surface Light: `#25253D` (Hover State)
- Text Primary: `#F8FAFC` (White)
- Text Secondary: `#94A3B8` (Muted)
- Success: `#10B981` (Green)
- Border: `#374151` (Gray Border)

**Typography:**
- Font Family: "Plus Jakarta Sans" (headings), "Inter" (body)
- Heading H1: 32px, weight 700
- Heading H2: 24px, weight 600
- Body: 14px, weight 400
- Small/Caption: 12px, weight 400

**Spacing System:**
- Base unit: 4px
- XS: 4px, S: 8px, M: 16px, L: 24px, XL: 32px, XXL: 48px

**Visual Effects:**
- Card shadows: `0 4px 24px rgba(99, 102, 241, 0.15)`
- Gradient background: `linear-gradient(135deg, #1A1A2E 0%, #0F0F23 50%, #1A1A2E 100%)`
- Button hover: scale(1.02) + glow effect
- Transition duration: 300ms ease

### Components

**1. Header**
- Logo: Icon + "ImageMotion" text
- Subtitle: "Transform static images into dynamic videos"

**2. Upload Area**
- Dashed border with gradient
- Icon: upload cloud
- Text: "Drop your image here or click to browse"
- Supported formats badge: PNG, JPG, WEBP
- Hover state: border color change to primary, slight scale

**3. Preview Section**
- Original image preview with filename
- Generated video preview (when available)
- Tab switching between original/output

**4. Animation Controls Panel**
- Effect Type Dropdown:
  - Ken Burns Zoom In
  - Ken Burns Zoom Out
  - Pan Left
  - Pan Right
  - Pan Up
  - Pan Down
  - Zoom & Rotate
  - Fade Through
  
- Duration Slider: 1-10 seconds (default: 3s)
- Zoom Level Slider: 1.0x - 2.0x (default: 1.2x)
- Pan Direction: Auto-detected or manual

**5. Action Buttons**
- Generate Video: Primary button with loading spinner
- Download Video: Secondary button (enabled after generation)
- Reset: Icon button to clear all

**6. Footer**
- Credit text: "Powered by FFmpeg & Streamlit"

## 3. Functionality Specification

### Core Features

**Image Upload:**
- Drag and drop support
- Click to browse
- Accept: PNG, JPG, JPEG, WEBP
- Max file size: 10MB
- Preview uploaded image immediately

**Animation Effects:**
1. **Ken Burns Zoom In**: Start at 1.0x, end at zoom level, subtle pan
2. **Ken Burns Zoom Out**: Start at zoom level, end at 1.0x
3. **Pan Left**: Smooth left movement across image
4. **Pan Right**: Smooth right movement
5. **Pan Up**: Smooth upward movement
6. **Pan Down**: Smooth downward movement
7. **Zoom & Rotate**: Combined zoom and rotation effect
8. **Fade Through**: Cross-fade with black overlay

**Video Generation:**
- Output format: MP4 (H.264)
- Resolution: Match source or 1080p max
- Frame rate: 30fps
- Smooth interpolation for all movements

**Output:**
- Preview in browser (using video tag)
- Direct download button
- Auto-generated filename: `imagemotion_[timestamp].mp4`

### User Flow

1. User uploads image → Image preview appears
2. User selects animation effect
3. User adjusts parameters (duration, zoom)
4. User clicks "Generate Video"
5. Progress indicator shows generation status
6. Video preview appears
7. User downloads video

### Edge Cases
- No image uploaded: Disable generate button
- Invalid file type: Show error message
- Large file: Show loading indicator during upload
- Generation failure: Show error with retry option
- Unsupported aspect ratio: Auto-crop to 16:9 or 9:16 based on orientation

## 4. Technical Implementation

**Stack:**
- Frontend: Streamlit
- Image Processing: Pillow (PIL)
- Video Generation: FFmpeg (via subprocess)
- Styling: Custom CSS with st.markdown

**File Structure:**
```
/workspace/project/
├── app.py              # Main Streamlit application
├── utils/
│   ├── video_generator.py  # Video generation logic
│   └── effects.py           # Animation effect definitions
├── requirements.txt    # Dependencies
└── output/            # Generated videos (temp)
```

## 5. Acceptance Criteria

- [ ] User can upload images via drag-drop or file picker
- [ ] Uploaded image displays immediately in preview
- [ ] All 8 animation effects work correctly
- [ ] Duration slider adjusts video length (1-10s)
- [ ] Zoom slider affects zoom level (1.0x-2.0x)
- [ ] Generate button creates video file
- [ ] Loading indicator shows during generation
- [ ] Generated video plays in preview
- [ ] Download button saves video to device
- [ ] UI is responsive and visually polished
- [ ] Error messages display for invalid inputs
- [ ] Reset button clears all state