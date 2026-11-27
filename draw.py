"""Render the 27 November 2026 world-news front page (1024x1024 PNG).

Original code, written for the make.fun news-image-20261127 bounty.
No network, no randomness: the same input always draws the same pixels.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24
GAP = 16

PAPER = (245, 239, 227)
INK = (26, 26, 26)
NAVY = (19, 41, 75)
NAVY_LIGHT = (31, 58, 95)
RED = (180, 35, 24)
ORANGE = (194, 65, 12)
TEAL = (15, 118, 110)
GOLD = (180, 83, 9)
CARD = (255, 255, 255)
BORDER = (216, 208, 190)
GREY = (90, 88, 82)
SOFT = (238, 232, 218)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = FONT_DIR + "/DejaVuSerif-Bold.ttf"
SERIF_REG = FONT_DIR + "/DejaVuSerif.ttf"
SANS = FONT_DIR + "/DejaVuSans.ttf"
SANS_BOLD = FONT_DIR + "/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_panel(d, box, accent):
    """White card with a coloured top bar and a thin border."""
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD,
                        outline=BORDER, width=2)
    d.rounded_rectangle([x0, y0, x1, y0 + 10], radius=5, fill=accent)
    d.rectangle([x0, y0 + 5, x1, y0 + 10], fill=accent)


def kicker_head_body(d, box, kicker, head, body, accent, head_size,
                     body_size, icon=None):
    """Fill a panel: coloured kicker, bold headline, short body, optional icon."""
    x0, y0, x1, y1 = box
    pad = 18
    tx = x0 + pad
    ty = y0 + 24
    text_w = x1 - x0 - 2 * pad
    if icon is not None:
        text_w -= 96
    f_kick = font(SANS_BOLD, 15)
    f_head = font(SANS_BOLD, head_size)
    f_body = font(SANS, body_size)
    d.text((tx, ty), kicker, font=f_kick, fill=accent)
    ty += 26
    for line in wrap(d, head, f_head, text_w):
        d.text((tx, ty), line, font=f_head, fill=INK)
        ty += head_size + 6
    ty += 4
    for line in wrap(d, body, f_body, text_w):
        d.text((tx, ty), line, font=f_body, fill=(58, 56, 50))
        ty += body_size + 5
    if icon is not None:
        icon(d, x1 - pad - 78, y0 + 26)


def icon_drone(d, x, y):
    """Small quadcopter silhouette."""
    s = 78
    d.ellipse([x, y, x + s, y + s], fill=(19, 41, 75))
    cx, cy = x + s // 2, y + s // 2
    d.rounded_rectangle([cx - 20, cy - 8, cx + 20, cy + 8], radius=6,
                        fill=(245, 239, 227))
    for dx, dy in ((-26, -22), (26, -22), (-26, 22), (26, 22)):
        d.line([cx, cy, cx + dx, cy + dy], fill=(245, 239, 227), width=4)
        d.ellipse([cx + dx - 9, cy + dy - 4, cx + dx + 9, cy + dy + 4],
                  fill=(245, 239, 227))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(180, 35, 24))


def icon_flame(d, x, y):
    """Flame over a refinery tower."""
    s = 78
    d.ellipse([x, y, x + s, y + s], fill=(194, 65, 12))
    cx = x + s // 2
    d.rectangle([cx - 16, y + 44, cx - 6, y + 62], fill=(245, 239, 227))
    d.rectangle([cx + 6, y + 36, cx + 16, y + 62], fill=(245, 239, 227))
    d.rectangle([cx - 22, y + 62, cx + 22, y + 66], fill=(245, 239, 227))
    flame = [(cx, y + 12), (cx + 10, y + 26), (cx + 14, y + 38),
             (cx + 4, y + 40), (cx - 2, y + 30), (cx - 12, y + 38),
             (cx - 10, y + 24)]
    d.polygon(flame, fill=(255, 214, 64))
    d.ellipse([x + 12, y + 10, x + 24, y + 20], fill=(200, 200, 200))
    d.ellipse([x + 20, y + 4, x + 30, y + 12], fill=(220, 220, 220))


def icon_skyline(d, x, y):
    """City skyline with one leaning tower and a burst above it."""
    s = 78
    d.ellipse([x, y, x + s, y + s], fill=(15, 118, 110))
    cx, cy = x + s // 2, y + s // 2
    d.rectangle([cx - 26, cy - 2, cx - 12, cy + 24], fill=(245, 239, 227))
    d.rectangle([cx - 8, cy - 14, cx + 6, cy + 24], fill=(245, 239, 227))
    d.polygon([(cx + 10, cy + 24), (cx + 14, cy - 6), (cx + 28, cy - 2),
               (cx + 26, cy + 24)], fill=(245, 239, 227))
    for dx, dy in ((-14, -26), (0, -30), (14, -26)):
        d.line([cx + dx, cy - 18 + dy // 3, cx + dx, cy - 26 + dy // 3],
               fill=(255, 214, 64), width=3)


def icon_balloon(d, x, y):
    """Parade balloon held back by wind lines."""
    s = 78
    d.ellipse([x, y, x + s, y + s], fill=(180, 83, 9))
    cx, cy = x + s // 2, y + s // 2
    d.ellipse([cx - 16, cy - 22, cx + 16, cy + 6], fill=(214, 48, 49))
    d.polygon([(cx - 10, cy + 8), (cx + 10, cy + 8), (cx + 6, cy + 22),
               (cx - 6, cy + 22)], fill=(245, 239, 227))
    for wy in (cy - 14, cy, cy + 14):
        d.line([x + 2, wy, x + 22, wy], fill=(245, 239, 227), width=3)
        d.line([x + 56, wy, x + 76, wy], fill=(245, 239, 227), width=3)


def icon_chart(d, x, y):
    """Falling bars with a downward arrow."""
    s = 78
    d.ellipse([x, y, x + s, y + s], fill=(19, 41, 75))
    cx, cy = x + s // 2, y + s // 2
    bars = [(-24, 18), (-8, 28), (8, 38)]
    for dx, h in bars:
        d.rectangle([cx + dx, cy + 20 - h, cx + dx + 12, cy + 20],
                    fill=(245, 239, 227))
    d.line([cx - 28, cy - 22, cx + 28, cy + 12], fill=(255, 214, 64), width=4)
    d.polygon([(cx + 28, cy + 12), (cx + 16, cy + 8), (cx + 24, cy + 20)],
              fill=(255, 214, 64))


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rounded_rectangle([MARGIN, MARGIN, W - MARGIN, 158], radius=12,
                        fill=NAVY)
    f_over = font(SANS_BOLD, 17)
    d.text((MARGIN + 22, MARGIN + 14), "THE WORLD TODAY  ·  ONE DAY, SIX STORIES",
           font=f_over, fill=(255, 214, 64))
    f_date = font(SERIF, 54)
    d.text((MARGIN + 20, MARGIN + 42), "Friday 27 November 2026",
           font=f_date, fill=(255, 255, 255))
    f_sub = font(SANS, 17)
    d.text((MARGIN + 22, 130),
           "From the Gulf to New York: the day the news would not slow down.",
           font=f_sub, fill=(205, 214, 228))

    # ---- Lead story: Kuwait drone attack -------------------------------
    lead = (MARGIN, 174, W - MARGIN, 408)
    draw_panel(d, lead, RED)
    kicker_head_body(
        d, lead,
        "MIDDLE EAST  ·  LEAD STORY",
        "Drone attack in Kuwait kills two Italian technicians",
        "Italy and Kuwait blame Iran for the strike on an air-defence "
        "station; Tehran denies any role. Two more people were hurt. "
        "It is the first fatal strike in the Gulf state in months.",
        RED, 33, 18, icon=icon_drone)
    d.line([MARGIN + 18, 352, W - MARGIN - 18, 352], fill=BORDER, width=2)
    f_nums = font(SANS_BOLD, 15)
    d.text((MARGIN + 18, 364),
           "THE DAY IN NUMBERS:  2 killed in Kuwait  ·  1 killed in Jazan  ·  "
           "10 killed in Gaza  ·  9 hurt in Bangkok",
           font=f_nums, fill=NAVY)

    # ---- Row 2: Jazan + Gaza -------------------------------------------
    left2 = (MARGIN, 424, 492, 648)
    right2 = (532, 424, W - MARGIN, 648)
    draw_panel(d, left2, ORANGE)
    kicker_head_body(
        d, left2,
        "SAUDI ARABIA",
        "Houthi strike hits Aramco's Jazan refinery",
        "A projectile kills one worker and halts some operations at the "
        "400,000-barrel-a-day plant. Brent crude holds above $95.",
        ORANGE, 24, 16, icon=icon_flame)
    draw_panel(d, right2, TEAL)
    kicker_head_body(
        d, right2,
        "GAZA",
        "Israeli strikes kill 10 in Gaza",
        "A deputy minister is among the dead as strikes go on despite "
        "the year-old ceasefire. Hamas says it will discuss a reply.",
        TEAL, 24, 16, icon=icon_skyline)

    # ---- Row 3: Bangkok + Macy's ---------------------------------------
    left3 = (MARGIN, 664, 492, 888)
    right3 = (532, 664, W - MARGIN, 888)
    draw_panel(d, left3, GOLD)
    kicker_head_body(
        d, left3,
        "THAILAND",
        "Blast and fire at Bangkok oil refinery",
        "Nine hurt at the Bangchak plant in Phra Khanong; all units shut "
        "down as smoke rises over the capital. Cause under inquiry.",
        GOLD, 24, 16, icon=icon_flame)
    draw_panel(d, right3, NAVY_LIGHT)
    kicker_head_body(
        d, right3,
        "UNITED STATES",
        "Macy's parade postponed, a first in 100 years",
        "A Thanksgiving storm forces the 100th parade to Saturday. "
        "Flights are cancelled and hundreds of thousands lose power.",
        NAVY_LIGHT, 24, 16, icon=icon_balloon)

    # ---- Also today -----------------------------------------------------
    briefs = (MARGIN, 900, W - MARGIN, 974)
    draw_panel(d, briefs, NAVY)
    d.text((MARGIN + 18, 910), "ALSO TODAY", font=font(SANS_BOLD, 15),
           fill=NAVY)
    col_w = (W - 2 * MARGIN - 36 - 3 * 14) // 4
    items = [
        ("UK MIGRATION", "Net migration falls to 77,000 — the lowest since 1997."),
        ("CHESS", "Gukesh v Sindarov: Game 3 of the World final ends in a draw."),
        ("NORTH KOREA", "Kim Jong-un vows to build more nuclear weapons."),
        ("SPORT", "Sinner pulls out of the 2027 Australian Open (knee)."),
    ]
    x = MARGIN + 18
    for head, body in items:
        d.text((x, 930), head, font=font(SANS_BOLD, 13), fill=RED)
        for i, line in enumerate(wrap(d, body, font(SANS, 12), col_w)):
            d.text((x, 946 + i * 14), line, font=font(SANS, 12), fill=INK)
        x += col_w + 14

    # ---- Footer ---------------------------------------------------------
    f_foot = font(SANS, 13)
    foot = "All stories reported on 27 November 2026  ·  Sources: Reuters, BBC, AP, AFP"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 986), foot, font=f_foot, fill=GREY)
    return img


if __name__ == "__main__":
    render().save("/tmp/preview-ni27.png")
    print("preview saved")
