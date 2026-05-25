import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio

data = json.loads(Path("demo_outputs/end_to_end_ai_support_incident.json").read_text())

W, H = 1600, 950
BG = (12, 18, 32)
CARD = (24, 34, 56)
TEXT = (238, 245, 255)
MUTED = (160, 180, 205)
RED = (255, 110, 110)
YELLOW = (255, 205, 86)
GREEN = (90, 220, 150)
BLUE = (95, 180, 255)

try:
    big = ImageFont.truetype("Arial.ttf", 52)
    med = ImageFont.truetype("Arial.ttf", 34)
    small = ImageFont.truetype("Arial.ttf", 26)
except:
    big = med = small = None

def panel(title, lines, out):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((60, 55, W-60, H-55), 32, fill=CARD, outline=BLUE, width=3)
    d.text((100, 95), title, fill=TEXT, font=big)

    y = 190
    for line, color in lines:
        d.rounded_rectangle((100, y-12, W-100, y+58), 18, fill=(18, 27, 45))
        d.text((130, y), line, fill=color, font=med)
        y += 85

    img.save(out)
    return img

agent = data["agentgrid_detection"]
autoops = data["autoops_classification"]
rca = data["rca_and_product_feedback"]

trace_lines = [
    (f"trace_id: {agent['trace_id']}", BLUE),
    (f"decision_id: {agent['decision_id']}", BLUE),
    ("bad answer: unsupported deployment root-cause claim", RED),
    (f"eval gate: {agent['final_decision'].upper()} · safe_to_ship={agent['eval_gate']['safe_to_ship']}", YELLOW),
    (f"reason: {agent['reason']}", YELLOW),
    (f"AutoOps recurring issue: {autoops['recurring_issue_family']} · repeat_count={autoops['repeat_count']}", GREEN),
    (f"outcome: {rca['release_safety_outcome']}", GREEN),
]
panel("AgentGrid Trace Viewer — Unsafe Answer → RCA", trace_lines, "screenshots/real_trace_viewer.png")

frames = []
slides = [
    ("1. Unsafe GenAI Answer", [
        ("Claimed DB cluster was definitely overloaded and recovered", RED),
        ("Available context: timeout logs, missing runbook, no DB health snapshot", YELLOW),
    ]),
    ("2. AgentGrid Eval Gate", [
        ("Unsupported answer detected: TRUE", RED),
        ("Missing retrieval grounding: TRUE", YELLOW),
        ("Decision: HOLD", YELLOW),
    ]),
    ("3. Escalation Artifact", [
        ("Jira-style issue created", BLUE),
        ("Owner: ai_support_engineering", BLUE),
        ("Support action: request DB health + runbook evidence", TEXT),
    ]),
    ("4. AutoOps Classification", [
        ("Recurring issue family: missing_retrieval_grounding", GREEN),
        ("Repeat count: 3", GREEN),
        ("Route: support_reviewer_queue", BLUE),
    ]),
    ("5. RCA + Product Feedback", [
        ("RCA: definitive DB root cause lacked evidence", GREEN),
        ("Feedback: improve deployment-failure retrieval coverage", GREEN),
        ("Outcome: blocked_from_shipping", GREEN),
    ]),
]

for i, (title, lines) in enumerate(slides, 1):
    img = panel(title, lines, f"demo_outputs/video/frame_{i}.png")
    frames.extend([img] * 24)

imageio.mimsave("demo_outputs/video/unsafe_answer_to_rca_demo.mp4", frames, fps=12)
imageio.mimsave("demo_outputs/video/unsafe_answer_to_rca_demo.gif", frames, fps=2)

print("Generated real trace viewer screenshot and unsafe-answer RCA video.")
