# 🎬 ImageMotion - Video Generator from Image

Transform static images into dynamic animated videos with beautiful motion effects.

![Made with Love](https://img.shields.io/badge/Made%20with-❤️-red)
![Open Source](https://img.shields.io/badge/Open%20Source-Yes!-green)
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Deployable-blue)

## ✨ Features

- 📤 **Easy Upload** - Drag & drop or browse for images (PNG, JPG, WEBP)
- 🎬 **8 Animation Effects:**
  - Ken Burns Zoom In
  - Ken Burns Zoom Out
  - Pan Left/Right/Up/Down
  - Zoom & Rotate
  - Fade Through
- ⚙️ **Customizable Settings:**
  - Duration: 1-10 seconds
  - Zoom Level: 1.0x - 2.0x
  - Frame Rate: 24/30/60 FPS
- 📥 **Direct Download** - Get your animated video instantly
- 🎨 **Beautiful Dark Theme** - Modern, responsive UI

## 🚀 Quick Start

### Option 1: Web Version (GitHub Pages)
Simply open `index.html` in any modern browser - no server required!

### Option 2: Local Development (Python/Streamlit)

```bash
# Clone the repository
git clone https://github.com/antono4/-Image-to-Video-Generator.git
cd -Image-to-Video-Generator

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📁 Project Structure

```
├── index.html              # Web version (HTML/CSS/JS)
├── app.py                  # Python/Streamlit version
├── utils/
│   ├── effects.py          # Animation effect definitions
│   └── video_generator.py  # Video generation logic
├── requirements.txt        # Python dependencies
└── SPEC.md                 # Project specification
```

## 🎯 Usage

1. **Upload Image** - Click the upload area or drag & drop your image
2. **Select Effect** - Choose from 8 animation effects
3. **Adjust Settings** - Set duration, zoom, and frame rate
4. **Generate** - Click "Generate Video" and watch the magic
5. **Download** - Save your animated video

## 🛠️ Technologies

### Web Version
- HTML5 Canvas API
- JavaScript (ES6+)
- CSS3 (Flexbox/Grid)

### Python Version
- Python 3.8+
- Streamlit
- OpenCV
- Pillow

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

*Made with ❤️ by the OpenHands Team*