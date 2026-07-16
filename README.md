# 🎬 ImageMotion AI - Smart Video Generator

> **Created by Antono**


Transform static images into dynamic animated videos with **AI-powered intelligence**.

![Made with Love](https://img.shields.io/badge/Made%20with-AI%20%F0%9F%A4%96-red)
![Open Source](https://img.shields.io/badge/Open%20Source-Yes!-green)
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Ready-blue)

## ✨ Features

### 🤖 AI Smart Mode
- **Automatic Scene Detection** - AI analyzes your image and detects:
  - 🌤️ Sky scenes
  - 🌊 Water/Landscape
  - 🌿 Nature/Forest
  - 🏛️ Architecture/Buildings
  - 🎭 Monochrome images
- **Smart Motion** - AI selects the best animation effect based on detected scene
- **Scene-Aware Effects** - Animation adapts to image characteristics

### 🎨 Manual Mode (12 Effects)
- Ken Burns Zoom In/Out
- Pan Left/Right/Up/Down
- Zoom & Rotate
- Fade Through
- Wave Effect
- Parallax Depth
- Optical Flow

### ⚙️ Customization
- Duration: 1-10 seconds
- Zoom Level: 1.0x - 2.0x
- Motion Intensity: 0.5x - 2.0x
- Frame Rate: 24/30/60 FPS
- Auto Loop Toggle

### 📥 Export
- Direct video download (WebM format)
- Loop-ready output

## 🚀 Quick Start

### Web Version (Recommended)
Simply open `index.html` in any modern browser - no server or installation required!

### Features
- Fully client-side (runs in browser)
- No data uploaded to servers
- Works offline after first load

## 📁 Project Structure

```
├── index.html              # Web version with AI features
├── app.py                  # Python/Streamlit version
├── utils/
│   ├── effects.py          # Animation effect definitions
│   └── video_generator.py  # Video generation logic
├── requirements.txt        # Python dependencies
├── README.md
└── SPEC.md                 # Project specification
```

## 🎯 How to Use

1. **Upload Image** - Drag & drop or click to browse
2. **Choose Mode**:
   - 🤖 **AI Smart Mode**: Let AI analyze and select the best effect
   - 🎨 **Manual Mode**: Choose your own effect
3. **Adjust Settings** - Duration, zoom, intensity, FPS
4. **Generate** - Click "Generate with AI" and watch the magic
5. **Download** - Save your animated video

## 🧠 AI Analysis

The AI analyzes images by:

1. **Color Analysis** - Detects dominant colors and brightness
2. **Scene Classification** - Identifies scene type (landscape, architecture, nature, etc.)
3. **Smart Recommendation** - Suggests the best animation effect
4. **Adaptive Motion** - Adjusts animation parameters based on detected content

## 🛠️ Technologies

### Web Version (Pure JavaScript)
- HTML5 Canvas API
- JavaScript ES6+
- CSS3 with modern design
- MediaRecorder API for video encoding

### Python Version
- Python 3.8+
- Streamlit
- OpenCV
- Pillow

## 📝 License

MIT License - Open source and free to use.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

*Made with ❤️ and 🤖 AI*