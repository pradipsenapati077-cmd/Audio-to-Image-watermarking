import numpy as np
from scipy.io import wavfile
from PIL import Image
import sys
import os
import math

def lsb_embed(signal, wm_bits, b):
    mask = (1 << b) - 1
    num_samples_needed = (len(wm_bits) + b - 1) // b  # ceil
    if num_samples_needed > len(signal):
        raise ValueError(f"Not enough audio samples: need {num_samples_needed}, have {len(signal)}")
    signal = signal.copy()
    embedded_bits = 0
    for i in range(num_samples_needed):
        chunk = wm_bits[i*b:(i+1)*b]
        if len(chunk) < b:
            chunk = chunk.ljust(b, '0')
        w = int(chunk, 2)
        signal[i] = (signal[i] & ~mask) | w
        embedded_bits += len(chunk)
    return signal, embedded_bits

def lsb_extract(signal, b, num_bits):
    mask = (1 << b) - 1
    bits = []
    num_samples_needed = (num_bits + b - 1) // b
    for i in range(num_samples_needed):
        val = signal[i] & mask
        bits.append(f"{val:0{b}b}")
    bits_str = "".join(bits)
    return bits_str[:num_bits]

def compute_mse_psnr(original, watermarked, max_val):
    diff = original.astype(np.float64) - watermarked.astype(np.float64)
    mse = np.mean(diff ** 2)
    if mse == 0:
        psnr = float('inf')
    else:
        psnr = 10 * np.log10((max_val ** 2) / mse)
    return mse, psnr

def main():
    # >>>>> PUT YOUR FILE PATHS HERE <<<<<
    audio_cover = r"cover.wav"
    img_wm_file = r"color_cover.png"
    # <<<<< END INPUT SECTION <<<<<

    if not os.path.exists(audio_cover) or not os.path.exists(img_wm_file):
        print("Check your file paths!")
        sys.exit(1)

    fs, audio_orig = wavfile.read(audio_cover)
    if audio_orig.ndim == 2:
        audio_orig = audio_orig[:, 0]
    audio_orig = audio_orig.astype(np.int16)
    max_audio = 32767
    n_samples = len(audio_orig)

    img_original = Image.open(img_wm_file).convert('RGB')

    print("Audio samples:", n_samples)

    b_list = [1, 4, 7]

    for b in b_list:
        print(f"\n--- {b}-Bit LSB ---")

        # Compute max bytes we can embed for this b
        max_bits_capacity = n_samples * b
        max_bytes_capacity = max_bits_capacity // 8  # full bytes
        max_rgb_values = max_bytes_capacity          # one byte per channel value

        # Decide new image size (keep aspect ratio but limit total pixels)
        orig_w, orig_h = img_original.size
        orig_pixels = orig_w * orig_h * 3

        if max_rgb_values <= 0:
            print("Capacity is zero for this b, skipping.")
            continue

        # Scale factor based on ratio of capacity to original RGB count
        scale = math.sqrt(max_rgb_values / orig_pixels)
        if scale >= 1.0:
            # We can keep original size
            img_resized = img_original.copy()
        else:
            new_w = max(1, int(orig_w * scale))
            new_h = max(1, int(orig_h * scale))
            img_resized = img_original.resize((new_w, new_h), Image.LANCZOS)

        img_wm_np = np.array(img_resized)
        h, w, c = img_wm_np.shape
        print(f"Using resized image for {b}-bit: {w}x{h}x{c}")

        img_flat = img_wm_np.flatten().astype(np.uint8)
        wm_bits = "".join(f"{p:08b}" for p in img_flat)
        num_wm_bits = len(wm_bits)

        # Make sure bits <= capacity
        max_bits_capacity = n_samples * b
        if num_wm_bits > max_bits_capacity:
            # truncate safely (last few channels lost)
            wm_bits = wm_bits[:max_bits_capacity]
            num_wm_bits = len(wm_bits)
            # adjust flat length accordingly
            usable_bytes = num_wm_bits // 8
            img_flat = img_flat[:usable_bytes]
            extra = (h * w * 3) - usable_bytes
            if extra > 0:
                img_flat = np.pad(img_flat, (0, extra), 'constant')
        print(f"Bits to embed: {num_wm_bits}, capacity: {max_bits_capacity}")

        # Embed
        try:
            audio_embed, bits_embed = lsb_embed(audio_orig, wm_bits, b)
        except ValueError as e:
            print("Cannot embed:", e)
            continue

        mse_a, psnr_a = compute_mse_psnr(audio_orig, audio_embed, max_audio)
        audio_out = f"{os.path.splitext(audio_cover)[0]}_{b}bit.wav"
        wavfile.write(audio_out, fs, audio_embed)

        # Extract
        ext_bits_a = lsb_extract(audio_embed, b, num_wm_bits)
        ext_vals = [int(ext_bits_a[i:i+8], 2) for i in range(0, num_wm_bits, 8)]
        ext_vals = np.array(ext_vals, dtype=np.uint8)

        # If we truncated/padded, ensure length matches resized img
        needed = h * w * 3
        if ext_vals.size < needed:
            ext_vals = np.pad(ext_vals, (0, needed - ext_vals.size), 'constant')
        elif ext_vals.size > needed:
            ext_vals = ext_vals[:needed]

        ext_img = ext_vals.reshape((h, w, 3))
        ext_img_out = f"extracted_from_audio_{b}bit.png"
        Image.fromarray(ext_img).save(ext_img_out)

        print(f"Audio -> MSE: {mse_a:.4f}, PSNR: {psnr_a:.2f} dB")
        print(f"  Embedded audio: {audio_out}")
        print(f"  Extracted image: {ext_img_out}")

if __name__ == "__main__":
    main()