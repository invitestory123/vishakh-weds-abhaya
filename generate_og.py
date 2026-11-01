import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

WIDTH = 1200
HEIGHT = 630

# Elegant Ivory & Warm Gold Palette matching storybook aesthetic
IVORY_BG = (253, 248, 239)        # #fdf8ef
CREAM_WARM = (248, 238, 222)      # #f8eedc
GOLD_MAIN = (196, 148, 58)        # #c4943a
GOLD_LIGHT = (235, 204, 138)      # #ebcc8a
GOLD_DEEP = (145, 104, 30)        # #91681e
GOLD_BORDER = (196, 148, 58, 160)
PRIMARY_DARK = (46, 26, 14)       # Deep espresso brown for readable elegance
MUTED_BROWN = (115, 84, 62)       # Medium warm brown

def create_og_image():
    # 1. Base canvas with subtle radial ivory-to-cream gradient
    base = Image.new("RGBA", (WIDTH, HEIGHT), IVORY_BG + (255,))
    draw_base = ImageDraw.Draw(base)

    cx_bg, cy_bg = int(WIDTH * 0.35), int(HEIGHT * 0.5)
    max_radius = int(math.hypot(WIDTH, HEIGHT))

    for r in range(max_radius, 0, -8):
        t = r / max_radius
        # Interpolate from soft warm cream center to subtle blush ivory edge
        cr = int(255 * (1 - t) + 248 * t)
        cg = int(250 * (1 - t) + 238 * t)
        cb = int(242 * (1 - t) + 225 * t)
        draw_base.ellipse([cx_bg - r, cy_bg - r, cx_bg + r, cy_bg + r], fill=(cr, cg, cb, 255))

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 2. Outer and Inner Gold Borders
    pad_out = 20
    draw.rectangle(
        [pad_out, pad_out, WIDTH - pad_out, HEIGHT - pad_out],
        outline=(196, 148, 58, 140),
        width=2
    )

    pad_in = 28
    draw.rectangle(
        [pad_in, pad_in, WIDTH - pad_in, HEIGHT - pad_in],
        outline=(196, 148, 58, 90),
        width=1
    )

    # Corner brackets with gold accent dots
    bracket_len = 34
    for (x0, y0, dx, dy) in [
        (pad_in + 4, pad_in + 4, 1, 1),
        (WIDTH - pad_in - 4, pad_in + 4, -1, 1),
        (pad_in + 4, HEIGHT - pad_in - 4, 1, -1),
        (WIDTH - pad_in - 4, HEIGHT - pad_in - 4, -1, -1),
    ]:
        draw.line([x0, y0, x0 + dx * bracket_len, y0], fill=GOLD_MAIN, width=2)
        draw.line([x0, y0, x0, y0 + dy * bracket_len], fill=GOLD_MAIN, width=2)
        draw.ellipse([x0 - 3, y0 - 3, x0 + 3, y0 + 3], fill=GOLD_MAIN)

    # 3. Right Side: Couple Photo Frame (Arch / Rounded Plate)
    photo_path = os.path.join("public", "photos", "couple-traditional.jpg")
    frame_x = 645
    frame_y = 38
    frame_w = 495
    frame_h = 554
    corner_r = 28

    if os.path.exists(photo_path):
        photo = Image.open(photo_path).convert("RGBA")
        # Crop & resize to fit frame_w x frame_h
        target_ratio = frame_w / frame_h
        img_w, img_h = photo.size
        img_ratio = img_w / img_h

        if img_ratio > target_ratio:
            new_w = int(img_h * target_ratio)
            left = (img_w - new_w) // 2
            photo_cropped = photo.crop((left, 0, left + new_w, img_h))
        else:
            new_h = int(img_w / target_ratio)
            # Bias crop slightly towards the upper portion to keep faces in view
            top = int((img_h - new_h) * 0.25)
            photo_cropped = photo.crop((0, top, img_w, top + new_h))

        photo_resized = photo_cropped.resize((frame_w, frame_h), Image.Resampling.LANCZOS)

        # Enhance vibrancy slightly for a radiant wedding look
        photo_resized = ImageEnhance.Color(photo_resized).enhance(1.06)
        photo_resized = ImageEnhance.Sharpness(photo_resized).enhance(1.1)

        # Create rounded mask for photo
        mask = Image.new("L", (frame_w, frame_h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, frame_w, frame_h], radius=corner_r, fill=255)

        # Create soft shadow behind photo frame
        shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle(
            [frame_x + 3, frame_y + 8, frame_x + frame_w + 5, frame_y + frame_h + 10],
            radius=corner_r,
            fill=(40, 20, 10, 50)
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=10))
        base = Image.alpha_composite(base, shadow)

        # Composite photo onto base
        base.paste(photo_resized, (frame_x, frame_y), mask)

        # Double Gold Border on the photo
        draw.rounded_rectangle(
            [frame_x, frame_y, frame_x + frame_w, frame_y + frame_h],
            radius=corner_r,
            outline=GOLD_MAIN,
            width=3
        )
        draw.rounded_rectangle(
            [frame_x + 5, frame_y + 5, frame_x + frame_w - 5, frame_y + frame_h - 5],
            radius=corner_r - 4,
            outline=(235, 204, 138, 160),
            width=1
        )

    # 4. Left Side Card Content
    left_cx = (pad_in + frame_x) // 2 - 10  # ~330px center

    # Monogram Emblem Logo (A & V)
    emblem_y = 100
    emblem_r = 44

    # Dash circle
    for angle in range(0, 360, 12):
        rad = math.radians(angle)
        rad_end = math.radians(angle + 6)
        x1 = left_cx + (emblem_r + 6) * math.cos(rad)
        y1 = emblem_y + (emblem_r + 6) * math.sin(rad)
        x2 = left_cx + (emblem_r + 6) * math.cos(rad_end)
        y2 = emblem_y + (emblem_r + 6) * math.sin(rad_end)
        draw.line([x1, y1, x2, y2], fill=(196, 148, 58, 140), width=1)

    draw.ellipse(
        [left_cx - emblem_r, emblem_y - emblem_r, left_cx + emblem_r, emblem_y + emblem_r],
        outline=GOLD_MAIN,
        width=2
    )
    draw.ellipse(
        [left_cx - (emblem_r - 4), emblem_y - (emblem_r - 4), left_cx + (emblem_r - 4), emblem_y + (emblem_r - 4)],
        outline=(196, 148, 58, 100),
        width=1
    )

    # Cardinal diamonds on emblem
    for dx, dy in [(0, -emblem_r - 6), (0, emblem_r + 6), (-emblem_r - 6, 0), (emblem_r + 6, 0)]:
        px, py = left_cx + dx, emblem_y + dy
        draw.polygon([(px, py - 3), (px + 3, py), (px, py + 3), (px - 3, py)], fill=GOLD_MAIN)

    # Fonts
    font_mono_main = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 36)
    font_mono_amp = ImageFont.truetype(r"C:\Windows\Fonts\georgiai.ttf", 22)
    font_eyebrow = ImageFont.truetype(r"C:\Windows\Fonts\pala.ttf", 13)
    font_names = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 52)
    font_amp = ImageFont.truetype(r"C:\Windows\Fonts\georgiai.ttf", 42)
    font_sub = ImageFont.truetype(r"C:\Windows\Fonts\palai.ttf", 18)
    font_date_pill = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 17)
    font_time = ImageFont.truetype(r"C:\Windows\Fonts\pala.ttf", 16)
    font_venue = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 20)
    font_loc = ImageFont.truetype(r"C:\Windows\Fonts\pala.ttf", 15)
    font_foot = ImageFont.truetype(r"C:\Windows\Fonts\pala.ttf", 12)

    # Monogram Letters: A & V
    draw.text((left_cx - 18, emblem_y + 1), "A", font=font_mono_main, fill=PRIMARY_DARK, anchor="mm")
    draw.text((left_cx, emblem_y - 1), "&", font=font_mono_amp, fill=GOLD_MAIN, anchor="mm")
    draw.text((left_cx + 19, emblem_y + 1), "V", font=font_mono_main, fill=PRIMARY_DARK, anchor="mm")

    # Eyebrow
    eyebrow_text = "T O G E T H E R   W I T H   T H E I R   F A M I L I E S"
    draw.text((left_cx, 174), eyebrow_text, font=font_eyebrow, fill=MUTED_BROWN, anchor="mm")

    # Couple Names: Abhaya & Vishakh
    names_y = 236
    draw.text((left_cx, names_y), "Abhaya & Vishakh", font=font_names, fill=PRIMARY_DARK, anchor="mm")

    # Subtitle
    draw.text((left_cx, 280), "invite you to celebrate their wedding", font=font_sub, fill=MUTED_BROWN, anchor="mm")

    # Divider line with diamond ✦
    div_y = 312
    line_w = 170
    draw.line([left_cx - line_w, div_y, left_cx - 18, div_y], fill=(196, 148, 58, 180), width=1)
    draw.line([left_cx + 18, div_y, left_cx + line_w, div_y], fill=(196, 148, 58, 180), width=1)
    draw.polygon([(left_cx, div_y - 4), (left_cx + 4, div_y), (left_cx, div_y + 4), (left_cx - 4, div_y)], fill=GOLD_MAIN)

    # Date Pill Badge
    pill_w = 390
    pill_h = 44
    pill_x0 = left_cx - pill_w // 2
    pill_y0 = 338
    # Subtle pill shadow
    draw.rounded_rectangle(
        [pill_x0, pill_y0 + 2, pill_x0 + pill_w, pill_y0 + pill_h + 2],
        radius=22,
        fill=(196, 148, 58, 40)
    )
    draw.rounded_rectangle(
        [pill_x0, pill_y0, pill_x0 + pill_w, pill_y0 + pill_h],
        radius=22,
        fill=(255, 255, 255, 230),
        outline=GOLD_MAIN,
        width=1
    )
    draw.text((left_cx, pill_y0 + pill_h // 2), "SUNDAY, 15 NOVEMBER 2026", font=font_date_pill, fill=PRIMARY_DARK, anchor="mm")

    # Time line
    draw.text((left_cx, 408), "Time: 11:00 AM – 12:30 PM", font=font_time, fill=PRIMARY_DARK, anchor="mm")

    # Venue & Destination
    draw.text((left_cx, 452), "Kabani Auditorium", font=font_venue, fill=GOLD_DEEP, anchor="mm")
    draw.text((left_cx, 480), "Pulpally, Wayanad, Kerala", font=font_loc, fill=MUTED_BROWN, anchor="mm")

    # View Invitation Button / CTA
    btn_w = 230
    btn_h = 34
    btn_x0 = left_cx - btn_w // 2
    btn_y0 = 514
    draw.rounded_rectangle(
        [btn_x0, btn_y0, btn_x0 + btn_w, btn_y0 + btn_h],
        radius=17,
        fill=PRIMARY_DARK
    )
    font_btn = ImageFont.truetype(r"C:\Windows\Fonts\pala.ttf", 11)
    draw.text((left_cx, btn_y0 + btn_h // 2), "VIEW INVITATION  →", font=font_btn, fill=(248, 238, 222), anchor="mm")

    # Footer hashtag
    draw.text((left_cx, 574), "#ABHAYAWEDSVIHSAKH   ·   INVITESTORY.IN", font=font_foot, fill=(160, 120, 60, 200), anchor="mm")

    # Composite layers
    final_img = Image.alpha_composite(base, overlay)
    final_rgb = final_img.convert("RGB")

    os.makedirs("public", exist_ok=True)
    os.makedirs(os.path.join("public", "assets"), exist_ok=True)

    # 5. Save with Lossless Compression (PNG with optimize=True, compress_level=9)
    og_png_path = os.path.join("public", "og-image.png")
    final_rgb.save(og_png_path, format="PNG", optimize=True, compress_level=9)

    # Also save to public/assets/og-image.png
    assets_og_path = os.path.join("public", "assets", "og-image.png")
    final_rgb.save(assets_og_path, format="PNG", optimize=True, compress_level=9)

    # Also generate high-quality progressive JPEG for platforms that prefer JPG
    og_jpg_path = os.path.join("public", "og-image.jpg")
    final_rgb.save(og_jpg_path, format="JPEG", quality=95, optimize=True)

    # Generate square IG preview (1080x1080) with lossless compression
    ig_size = 1080
    ig_img = Image.new("RGB", (ig_size, ig_size), IVORY_BG)
    scale = ig_size / WIDTH
    new_h = int(HEIGHT * scale)
    scaled_content = final_rgb.resize((ig_size, new_h), Image.Resampling.LANCZOS)
    ig_img.paste(scaled_content, (0, (ig_size - new_h) // 2))
    ig_png_path = os.path.join("public", "ig-image.png")
    ig_img.save(ig_png_path, format="PNG", optimize=True, compress_level=9)

    print(f"Generated Lossless OG Image: {og_png_path} ({os.path.getsize(og_png_path)} bytes)")
    print(f"Generated Assets OG Image: {assets_og_path} ({os.path.getsize(assets_og_path)} bytes)")
    print(f"Generated Progressive OG JPG: {og_jpg_path} ({os.path.getsize(og_jpg_path)} bytes)")
    print(f"Generated Lossless IG Image: {ig_png_path} ({os.path.getsize(ig_png_path)} bytes)")

if __name__ == "__main__":
    create_og_image()

