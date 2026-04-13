# Audio-to-Image-watermarking


---

# 🎵 Audio Steganography using LSB (Least Significant Bit)

This project implements **audio steganography** using the **Least Significant Bit (LSB)** technique. It allows embedding an image inside an audio file and later extracting it while evaluating quality using **MSE (Mean Squared Error)** and **PSNR (Peak Signal-to-Noise Ratio)**.

---

## 📌 Features

* 🔐 Embed an image into an audio file using LSB technique
* 🔍 Extract the hidden image from the audio
* 📊 Compute **MSE** and **PSNR** for quality evaluation
* ⚙️ Supports multiple embedding depths: **1-bit, 4-bit, 7-bit**
* 🖼️ Automatic image resizing based on audio capacity

---

## 🛠️ Technologies Used

* Python 🐍
* NumPy
* SciPy (`wavfile`)
* PIL (Python Imaging Library)

---

## 📂 Project Structure

```
├── new.py                  # Main Python script
├── cover.wav              # Input audio file (cover)
├── color_cover.png        # Image to embed (watermark)
├── output files:
│   ├── cover_1bit.wav
│   ├── cover_4bit.wav
│   ├── cover_7bit.wav
│   ├── extracted_from_audio_1bit.png
│   ├── extracted_from_audio_4bit.png
│   └── extracted_from_audio_7bit.png
```

---

## ⚙️ How It Works

### 🔹 Embedding Process

1. Convert image pixels into binary bits
2. Modify LSBs of audio samples
3. Store image bits inside audio

### 🔹 Extraction Process

1. Read LSBs from modified audio
2. Reconstruct binary data
3. Convert back to image

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/audio-steganography-lsb.git
cd audio-steganography-lsb
```

### 2️⃣ Install Dependencies

```bash
pip install numpy scipy pillow
```

---

## ▶️ Usage

1. Open `new.py`
2. Update file paths:

```python
audio_cover = r"cover.wav"
img_wm_file = r"color_cover.png"
```

3. Run the script:

```bash
python new.py
```

---

## 📊 Output

For each bit depth (1, 4, 7):

* 🎵 Watermarked audio file
* 🖼️ Extracted image
* 📈 MSE and PSNR values

Example output:

```
--- 4-Bit LSB ---
Audio -> MSE: 0.1234, PSNR: 78.45 dB
Embedded audio: cover_4bit.wav
Extracted image: extracted_from_audio_4bit.png
```

---

## 📈 Performance Metrics

* **MSE (Mean Squared Error)** → Measures distortion
* **PSNR (Peak Signal-to-Noise Ratio)** → Measures quality

Higher PSNR = Better quality 🎯

---

## ⚠️ Limitations

* Large images may be resized automatically
* Higher bit embedding may reduce audio quality
* Works best with **WAV (uncompressed audio)**

---

## 💡 Future Improvements

* GUI-based interface
* Support for other file formats (MP3, video)
* Encryption before embedding
* Adaptive LSB techniques



