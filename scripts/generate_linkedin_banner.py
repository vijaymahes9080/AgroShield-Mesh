"""
Generates high-resolution LinkedIn showcase banner (image.png) for AgroShield Mesh.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

WIDTH = 1920
HEIGHT = 1080

# Load fonts
FONT_DIR = r"C:\Windows\Fonts"
title_font = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 54)
subtitle_font = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 22)
badge_font = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 16)
card_title_font = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 20)
tag_font = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 15)
metric_num_font = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 38)
metric_label_font = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 15)
metric_sub_font = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 13)
footer_font = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 18)
footer_bold = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 18)

# Create base canvas with soft gradient
img = Image.new("RGB", (WIDTH, HEIGHT), "#F8FAFC")
draw = ImageDraw.Draw(img)

# Background subtle gradient
for y in range(HEIGHT):
    r = int(248 + (241 - 248) * (y / HEIGHT))
    g = int(250 + (245 - 250) * (y / HEIGHT))
    b = int(252 + (249 - 252) * (y / HEIGHT))
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# Subtle top bar accent
draw.rectangle([(0, 0), (WIDTH, 8)], fill="#059669")

# Header Pill Badge
badge_text = "🌾 OPEN-SOURCE AGRI-INTELLIGENCE & BOUNDED DECISION ENGINE"
badge_w = draw.textlength(badge_text, font=badge_font)
badge_box = [(60, 45), (60 + badge_w + 32, 77)]
draw.rounded_rectangle(badge_box, radius=16, fill="#ECFDF5", outline="#A7F3D0", width=1)
draw.text((76, 52), badge_text, fill="#047857", font=badge_font)

# Main Title
draw.text((60, 90), "AGROSHIELD MESH", fill="#0F172A", font=title_font)

# Subtitle
draw.text(
    (60, 155),
    "Autonomous IoT Mesh Telemetry · Sentinel-2 NDVI · Grounded Agricultural RAG · Bounded Multi-Agent Workflow",
    fill="#475569",
    font=subtitle_font,
)

# Load preview images
docs_img_dir = r"d:\current project\zz\docs\images"
hero_img = Image.open(os.path.join(docs_img_dir, "hero_banner.jpg")).convert("RGB")
gis_img = Image.open(os.path.join(docs_img_dir, "gis_ndvi_map.jpg")).convert("RGB")
adv_img = Image.open(os.path.join(docs_img_dir, "advisory_ui.jpg")).convert("RGB")

cards_data = [
    {
        "title": "IoT Mesh & Satellite Ingestion",
        "tag": "LoRaWAN · 30/60cm Soil Probes · PII Masked",
        "img": hero_img,
        "x": 60,
    },
    {
        "title": "Cadastral GIS & Sentinel-2 NDVI",
        "tag": "EPSG:4326/3857 · Erode District · NDWI Wetness",
        "img": gis_img,
        "x": 670,
    },
    {
        "title": "Bilingual Advisory & Expert Gate",
        "tag": "English & தமிழ் · TNAU / ICAR Citations · Gate",
        "img": adv_img,
        "x": 1280,
    },
]

card_w = 580
card_h = 510
card_y = 205

for c in cards_data:
    cx = c["x"]
    # Card background with shadow
    draw.rounded_rectangle(
        [(cx, card_y), (cx + card_w, card_y + card_h)],
        radius=14,
        fill="#FFFFFF",
        outline="#E2E8F0",
        width=1,
    )
    
    # Title & tag
    draw.text((cx + 18, card_y + 14), c["title"], fill="#1E293B", font=card_title_font)
    draw.text((cx + 18, card_y + 40), c["tag"], fill="#64748B", font=tag_font)
    
    # Inset preview image
    img_w = card_w - 36
    img_h = 420
    resized_preview = c["img"].resize((img_w, img_h), Image.Resampling.LANCZOS)
    img.paste(resized_preview, (cx + 18, card_y + 70))
    # Border around image
    draw.rectangle([(cx + 18, card_y + 70), (cx + 18 + img_w, card_y + 70 + img_h)], outline="#CBD5E1", width=1)

# Metrics Section (y = 740 to 960)
metrics = [
    {
        "num": "97.0%",
        "label": "Irrigation Agreement",
        "sub": "Exceeds 80% Benchmark Target",
        "accent": "#059669",
        "bg": "#ECFDF5",
        "border": "#A7F3D0",
    },
    {
        "num": "100%",
        "label": "Citation Grounding",
        "sub": "TNAU & ICAR SHA-256 Hashed",
        "accent": "#0284C7",
        "bg": "#F0F9FF",
        "border": "#BAE6FD",
    },
    {
        "num": "0.0%",
        "label": "False High-Alert Rate",
        "sub": "100 Empirical Test Scenarios",
        "accent": "#10B981",
        "bg": "#F0FDF4",
        "border": "#BBF7D0",
    },
    {
        "num": "21 / 21",
        "label": "Automated Tests",
        "sub": "100% Pytest & CI Pass Rate",
        "accent": "#7C3AED",
        "bg": "#F5F3FF",
        "border": "#DDD6FE",
    },
]

m_card_w = 425
m_card_h = 175
m_start_x = 60
m_gap = 26
m_y = 745

for i, m in enumerate(metrics):
    mx = m_start_x + i * (m_card_w + m_gap)
    draw.rounded_rectangle(
        [(mx, m_y), (mx + m_card_w, m_y + m_card_h)],
        radius=14,
        fill=m["bg"],
        outline=m["border"],
        width=1,
    )
    # Number
    draw.text((mx + 24, m_y + 20), m["num"], fill=m["accent"], font=metric_num_font)
    # Label
    draw.text((mx + 24, m_y + 78), m["label"], fill="#0F172A", font=metric_label_font)
    # Sub
    draw.text((mx + 24, m_y + 110), m["sub"], fill="#475569", font=metric_sub_font)
    # Checkmark tag
    draw.text((mx + m_card_w - 45, m_y + 24), "✓", fill=m["accent"], font=metric_num_font)

# Bottom Footer Bar
draw.line([(60, 950), (WIDTH - 60, 950)], fill="#E2E8F0", width=1)
draw.text((60, 980), "Architect & Developer: ", fill="#64748B", font=footer_font)
w_lbl = draw.textlength("Architect & Developer: ", font=footer_font)
draw.text((60 + w_lbl, 980), "Vijay Mahes (Vijaypradhap2004@gmail.com)", fill="#0F172A", font=footer_bold)

draw.text((60, 1015), "GitHub Repository: ", fill="#64748B", font=footer_font)
w_gh = draw.textlength("GitHub Repository: ", font=footer_font)
draw.text((60 + w_gh, 1015), "https://github.com/vijaymahes9080/AgroShield-Mesh", fill="#0284C7", font=footer_bold)

# Badges on right side of footer
f_badges = "🔒 Zero Autonomous Pump Control  |  🛡️ Accredited Expert Review Gate  |  ⚖️ MIT License"
w_fb = draw.textlength(f_badges, font=footer_font)
draw.text((WIDTH - 60 - w_fb, 1000), f_badges, fill="#475569", font=footer_font)

# Save image.png at root and docs/images/linkedin_showcase.png
out_root = r"d:\current project\zz\image.png"
out_docs = r"d:\current project\zz\docs\images\linkedin_showcase.png"
img.save(out_root, format="PNG", quality=95)
img.save(out_docs, format="PNG", quality=95)
print("Successfully generated image.png and docs/images/linkedin_showcase.png!")
