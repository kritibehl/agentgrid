from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path("docs/images")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1600, 950
BG = (12, 18, 32)
CARD = (24, 34, 56)
TEXT = (238, 245, 255)
MUTED = (160, 180, 205)
BLUE = (95, 180, 255)
GREEN = (90, 220, 150)
YELLOW = (255, 205, 86)

try:
    big = ImageFont.truetype("Arial.ttf", 54)
    med = ImageFont.truetype("Arial.ttf", 34)
    small = ImageFont.truetype("Arial.ttf", 26)
except:
    big = med = small = None

def product_flow():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((80, 55), "Apple Store Online Product Discovery Flow", fill=TEXT, font=big)

    steps = [
        "Customer Segment",
        "Product Search Agent",
        "Recommendation Review",
        "RAG Product Answer",
        "Personalization Evaluation",
        "Eval Gate",
        "Ship / Hold Decision"
    ]

    x = W // 2
    y = 150

    for i, step in enumerate(steps):
        d.rounded_rectangle((x - 330, y, x + 330, y + 70), radius=24, fill=CARD, outline=BLUE, width=3)
        d.text((x - 285, y + 18), step, fill=TEXT, font=med)

        if i < len(steps) - 1:
            d.line((x, y + 72, x, y + 115), fill=BLUE, width=5)
            d.polygon([(x, y + 120), (x - 12, y + 100), (x + 12, y + 100)], fill=BLUE)

        y += 115

    img.save(OUT / "product_discovery_flow.png")

def eval_report():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((80, 55), "Personalization Evaluation Report", fill=TEXT, font=big)

    metrics = [
        ("Segments Evaluated", "3", BLUE),
        ("Recommendations Evaluated", "3", BLUE),
        ("Ship Decisions", "3", GREEN),
        ("Hold Decisions", "0", GREEN),
        ("Average Message Relevance", "0.91", YELLOW),
        ("Unsupported Claims", "0", GREEN),
        ("Status", "PASS", GREEN),
    ]

    y = 160
    for label, value, color in metrics:
        d.rounded_rectangle((90, y, W - 90, y + 82), radius=22, fill=CARD, outline=color, width=3)
        d.text((130, y + 22), label, fill=MUTED, font=small)
        d.text((W - 360, y + 17), value, fill=color, font=med)
        y += 100

    img.save(OUT / "personalization_eval_report.png")

product_flow()
eval_report()

print("Generated docs/images/product_discovery_flow.png")
print("Generated docs/images/personalization_eval_report.png")
