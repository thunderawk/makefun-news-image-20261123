#!/usr/bin/env python3
"""Render the news-image-20261123 front page (1024x1024 PNG).

Build tooling, written in-session on 23 Nov 2026 for the make.fun
news-image-20261123 bounty. Runs on the VM with PIL + DejaVu.
The entry repo ships the rendered PNG plus a stdlib-only main.py
that copies it to /output. All facts re-verified against primary
outlets on 23 Nov 2026 ~03:00 UTC; every story is dated 23 Nov
or explicitly framed as Monday's fallout of a Sunday event.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 252, 247)
INK = (17, 17, 17)
GREY = (90, 90, 88)
RULE = (17, 17, 17)
FAINT = (205, 203, 196)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
NAVY_DK = (22, 44, 74)
SKY = (214, 226, 238)
MAP_FILL = (228, 226, 218)
MAP_LINE = (178, 176, 166)
AMBER = (247, 203, 138)
GOLD = (250, 204, 21)

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(F_SANS, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, lh, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def centered(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return w


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 34
RX = W - MX  # right margin x

# ---------- kicker + date + deck ----------
f_kick = font(F_SANS_B, 16)
d.text((MX, 16), "THE WORLD IN ONE DAY", font=f_kick, fill=RED)
cnt = "23 STORIES  ·  4 REGIONS"
cw = d.textlength(cnt, font=f_kick)
d.text((RX - cw, 16), cnt, font=f_kick, fill=GREY)

f_date = font(F_SERIF_B, 52)
centered(d, 42, "MONDAY 23 NOVEMBER 2026", f_date, INK)

f_deck = font(F_SERIF_I, 20)
centered(d, 104, "COP31 collapses  ·  Philippines names 8,320 dead  ·  NATO meets on Poland",
         f_deck, RED)

d.rectangle([MX, 132, RX, 135], fill=RULE)
d.rectangle([MX, 138, RX, 139], fill=RULE)

f_region = font(F_SANS_B, 14)
centered(d, 146, "EUROPE 2   ·   ASIA-PACIFIC 5   ·   MIDDLE EAST 1   ·   WORLD 3",
         f_region, GREY)

# ---------- BY THE NUMBERS strip ----------
NY0, NY1 = 166, 216
d.rectangle([MX, NY0, RX, NY1], fill=NAVY)
nums = [
    ("8,320", "drug-war dead named"),
    ("2035", "Women's World Cup year"),
    ("48", "teams in 2035"),
    ("499", "victims still unnamed"),
    ("$92.29", "Brent crude, Monday"),
    ("3", "Russian missiles in Poland"),
]
cell_w = (RX - MX) / 6
f_num = font(F_SANS_B, 25)
f_cap = font(F_SANS, 12)
for i, (fig, cap) in enumerate(nums):
    cx = MX + i * cell_w
    fw = d.textlength(fig, font=f_num)
    d.text((cx + (cell_w - fw) / 2, NY0 + 6), fig, font=f_num, fill=(255, 255, 255))
    cw2 = d.textlength(cap, font=f_cap)
    d.text((cx + (cell_w - cw2) / 2, NY0 + 36), cap, font=f_cap, fill=(200, 210, 225))
    if i:
        d.line([cx, NY0 + 8, cx, NY1 - 8], fill=(70, 95, 130), width=1)

# ---------- heroes ----------
def art_cop31(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # flag poles with small flags
    for fx, fc in ((x + 16, RED), (x + w - 24, NAVY)):
        d.rectangle([fx, y + 8, fx + 2, y + h - 30], fill=INK)
        d.rectangle([fx + 2, y + 8, fx + 20, y + 20], fill=fc)
    # long summit table, five empty chairs behind it
    for k in range(5):
        cx = x + 30 + k * 52
        d.rectangle([cx, y + 28, cx + 26, y + 46], fill=(110, 120, 135))
        d.rectangle([cx - 2, y + 46, cx + 28, y + 51], fill=(90, 100, 115))
        d.rectangle([cx + 2, y + 51, cx + 4, y + 56], fill=(90, 100, 115))
        d.rectangle([cx + 22, y + 51, cx + 24, y + 56], fill=(90, 100, 115))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=NAVY_DK)
    # name plates on the table
    for k in range(5):
        cx = x + 36 + k * 52
        d.rectangle([cx, y + h - 22, cx + 14, y + h - 15], fill=(255, 255, 255))


def art_philippines(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=AMBER)
    d.ellipse([x + w - 58, y + 8, x + w - 22, y + 44], fill=(250, 240, 210))
    # skyline, varied heights with lit windows
    towers = [(0, 44, 30), (36, 64, 26), (68, 38, 30), (104, 58, 28),
              (138, 46, 26), (170, 68, 30), (206, 42, 28), (240, 60, 26),
              (272, 50, 24)]
    for tx, th, tw in towers:
        # Clamp tower tops inside the art box: unclamped, the tallest
        # towers (th > 52) poked above y into the numbers strip and
        # covered the 499 caption's first letter.
        top = max(y, y + h - th - 22)
        d.rectangle([x + tx, top, x + tx + tw, y + h - 22], fill=(60, 45, 40))
        for wy in range(max(y + 8, y + h - th - 14), y + h - 26, 14):
            d.rectangle([x + tx + 6, wy, x + tx + 11, wy + 6], fill=GOLD)
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(40, 30, 26))
    # candles
    for k in range(9):
        cx = x + 12 + k * 32
        d.rectangle([cx, y + h - 16, cx + 10, y + h - 6], fill=(250, 248, 240))
        d.ellipse([cx + 2, y + h - 24, cx + 8, y + h - 16], fill=GOLD)


def art_nato(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    cx, cy = x + w // 2, y + 34
    # NATO compass star
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=(255, 255, 255), width=2)
    d.polygon([(cx, cy - 24), (cx + 6, cy - 6), (cx + 24, cy), (cx + 6, cy + 6),
               (cx, cy + 24), (cx - 6, cy + 6), (cx - 24, cy), (cx - 6, cy - 6)],
              fill=(255, 255, 255))
    # debris shards at the bottom
    for px, py, s in ((x + 20, y + h - 18, 12), (x + 70, y + h - 24, 16),
                      (x + 130, y + h - 16, 10), (x + 190, y + h - 22, 14),
                      (x + 245, y + h - 18, 12)):
        d.polygon([(px, py), (px + s, py), (px + s // 2, py - s)], fill=(150, 155, 165))
    d.rectangle([x, y + h - 6, x + w, y + h], fill=NAVY_DK)


heroes = [
    ("CLIMATE  ·  ANTALYA", "COP31 collapses, no deal", art_cop31,
     "The Antalya pact died on Sunday after record overtime; on Monday, "
     "Australia's PM called it a sign of 'difficult times'."),
    ("ASIA  ·  MANILA", "Philippines names 8,320 drug-war dead", art_philippines,
     "The Truth Commission presents its first report today, naming 8,320 "
     "killed in 2016-2022. Another 499 are still unnamed."),
    ("EUROPE  ·  BRUSSELS", "NATO meets on Poland incursion", art_nato,
     "Prosecutors confirmed on Sunday all three objects were Russian "
     "Kh-101 missiles. The council meets in Brussels today."),
]
HY0, HY1 = 224, 410
col_w = (RX - MX - 24) // 3
f_htag = font(F_SANS_B, 13)
f_hhead = font(F_SANS_B, 19)
f_hbody = font(F_SANS, 13)
for i, (tag, head, art, body) in enumerate(heroes):
    hx = MX + i * (col_w + 12)
    art(hx, HY0, col_w, 74)
    d.text((hx, HY0 + 80), tag, font=f_htag, fill=RED)
    text_block(d, hx, HY0 + 98, head, f_hhead, INK, col_w, 21, max_lines=2)
    text_block(d, hx, HY0 + 142, body, f_hbody, GREY, col_w, 14, max_lines=3)
    d.line([hx, HY1, hx + col_w, HY1], fill=FAINT, width=1)

# ---------- cards: 8 stories, 2 cols x 4 rows ----------
cards = [
    ("SPORT", "FIFA: UK to host 2035 Women's World Cup",
     "FIFA is set to confirm the UK today in Zurich — a first World Cup there since 1966. "
     "The 48-team tournament will use 19 venues."),
    ("ASIA", "Nepal's Shah meets Modi in Delhi",
     "On his first trip abroad since March, Nepal's PM holds talks today, seeking "
     "flood aid, trade and energy deals."),
    ("MIDDLE EAST", "Oil falls as the Gulf war grinds on",
     "Brent fell to $92.29 on Monday. Houthis claimed on Sunday they hit a Saudi "
     "refinery; the claim is unverified."),
    ("SPORT", "India close in on New Zealand",
     "At lunch on day five, New Zealand are 157 for 4, still 195 behind. India need "
     "six wickets after declaring on 720 for 9."),
    ("SPORT", "Sindarov gets White in Game 1",
     "Game 1 of the FIDE World Championship opens today, with Sindarov taking White "
     "in the opening game of the title match."),
    ("MARKETS", "Asian markets open on alert",
     "US stocks plunged on Friday and the AI rally wobbled, leaving Asian markets "
     "on alert as trading opened on Monday."),
    ("BUSINESS", "Tata Sons to decide on going public",
     "India's biggest conglomerate gears up for a decision this week on whether to "
     "go public or stay private."),
    ("ASIA", "Free rides as Manila drivers strike",
     "Buses run free from 6am to 9pm today and Tuesday on five Metro Manila routes "
     "during Manibela's two-day transport strike."),
]
f_ctag = font(F_SANS_B, 12)
f_chead = font(F_SANS_B, 17)
f_cbody = font(F_SANS, 13)
f_cnum = font(F_SANS_B, 15)
CARD_H = 92
CY0 = 418
card_w = (RX - MX - 20) // 2
for i, (tag, head, body) in enumerate(cards):
    row, col = divmod(i, 2)
    cx = MX + col * (card_w + 20)
    cy = CY0 + row * CARD_H
    d.line([cx, cy, cx + card_w, cy], fill=FAINT, width=1)
    # number badge
    n = i + 4
    d.rectangle([cx, cy + 8, cx + 26, cy + 34], fill=RED)
    nw = d.textlength(str(n), font=f_cnum)
    d.text((cx + (26 - nw) / 2, cy + 11), str(n), font=f_cnum, fill=(255, 255, 255))
    tx = cx + 36
    d.text((tx, cy + 6), tag, font=f_ctag, fill=RED)
    text_block(d, tx, cy + 24, head, f_chead, INK, card_w - 36, 20, max_lines=1)
    text_block(d, tx, cy + 46, body, f_cbody, GREY, card_w - 36, 16, max_lines=2)

# ---------- map + ALSO ----------
MY0 = 794
f_mtitle = font(F_SANS_B, 13)
d.text((MX, MY0), "WHERE IT HAPPENED", font=f_mtitle, fill=INK)
d.text((MX + 446, MY0), "ALSO ON MONDAY 23 NOVEMBER", font=f_mtitle, fill=INK)

MAP_X0, MAP_Y0, MAP_W, MAP_H = MX, MY0 + 20, 400, 136
d.rectangle([MAP_X0, MAP_Y0, MAP_X0 + MAP_W, MAP_Y0 + MAP_H], outline=FAINT, width=1)


def proj(lon, lat):
    px = MAP_X0 + (lon + 180) / 360 * MAP_W
    py = MAP_Y0 + (75 - lat) / 130 * MAP_H
    return px, py


continents = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 80), (-80, 73),
     (-65, 60), (-55, 52), (-60, 45), (-75, 35), (-80, 25), (-90, 20),
     (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-145, 60),
     (-165, 60)],
    [(-58, 64), (-45, 60), (-30, 68), (-20, 70), (-30, 76), (-50, 76), (-58, 70)],
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8), (-40, -20),
     (-48, -28), (-58, -38), (-68, -52), (-70, -40), (-73, -25), (-77, -12), (-80, 0)],
    [(-10, 36), (-5, 44), (0, 50), (5, 58), (10, 60), (18, 56), (25, 60),
     (30, 55), (28, 45), (20, 40), (12, 44), (3, 43), (-2, 37)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (32, 31), (35, 28),
     (40, 15), (48, 11), (51, 12), (44, 0), (40, -10), (35, -18), (30, -28),
     (20, -35), (15, -30), (12, -18), (9, -5), (9, 4), (-8, 5), (-15, 11)],
    [(30, 70), (50, 73), (70, 72), (90, 75), (110, 76), (130, 72), (150, 70),
     (170, 66), (178, 65), (170, 60), (160, 55), (150, 60), (140, 50),
     (135, 43), (127, 40), (120, 30), (110, 20), (105, 10), (100, 8),
     (95, 15), (90, 22), (80, 15), (77, 8), (72, 20), (65, 25), (60, 25),
     (55, 26), (50, 29), (48, 30), (40, 35), (35, 36), (30, 42)],
    [(113, -22), (114, -30), (115, -35), (125, -32), (130, -32), (135, -35),
     (140, -38), (145, -38), (150, -37), (153, -27), (146, -19), (142, -11),
     (136, -12), (132, -11), (126, -14), (122, -17), (118, -20)],
]
for poly in continents:
    pts = [proj(lon, lat) for lon, lat in poly]
    d.polygon(pts, fill=MAP_FILL, outline=MAP_LINE)

pins = [
    (1, 30.7, 36.9, 0, 0),      # Antalya
    (2, 121.0, 14.6, 0, 0),     # Manila
    (3, 4.35, 50.8, -8, -4),    # Brussels (nudged so it clears Zurich)
    (4, 8.5, 47.4, 10, 8),      # Zurich (nudged)
    (5, 77.2, 28.6, 0, 0),      # New Delhi
    (6, 39.0, 22.8, 0, 0),      # Rabigh
    (7, 174.8, -41.3, 0, 0),    # Wellington
    (9, 72.8, 19.0, -12, 14),   # Mumbai (nudged so it clears Delhi)
]
f_pin = font(F_SANS_B, 10)
for num, lon, lat, dx, dy in pins:
    px, py = proj(lon, lat)
    px += dx
    py += dy
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
    nw = d.textlength(str(num), font=f_pin)
    d.text((px - nw / 2, py - 6), str(num), font=f_pin, fill=(255, 255, 255))
f_mapnote = font(F_SANS, 11)
d.text((MAP_X0, MAP_Y0 + MAP_H + 4), "8 Markets — everywhere  ·  10 Manila — see 2",
       font=f_mapnote, fill=GREY)

also = [
    "FIFA confirms 2031 hosts today",
    "Duterte's ICC trial opens 30 Nov",
    "96.6% of the dead were men",
    "60 of the dead were children",
    "Official toll 6,252; ICC says more",
    "Shah leads a 34-member delegation",
    "India 720/9: biggest total in NZ",
    "2nd Test starts Fri, Christchurch",
    "COP31: 194 delegations took part",
    "US stayed away for a second year",
    "WTI crude $83.26 on Monday",
    "UK bid scored 4.3 out of 5",
]
f_also = font(F_SANS, 12)
f_anum = font(F_SANS_B, 12)
AX0 = MX + 446
col2_w = (RX - AX0 - 16) // 2
for i, item in enumerate(also):
    col, row = divmod(i, 6)
    ax = AX0 + col * (col2_w + 16)
    ay = MY0 + 20 + row * 22
    d.text((ax, ay), f"{i + 12}.", font=f_anum, fill=RED)
    d.text((ax + 26, ay), item, font=f_also, fill=INK)

# ---------- DATE CHECK + sources ----------
DY0 = 972
f_dc = font(F_SANS, 12)
f_dcb = font(F_SANS_B, 12)
dc_head = "DATE CHECK — first reported Sunday 22 Nov, so not today's news:  "
d.text((MX, DY0), dc_head, font=f_dcb, fill=INK)
dc_text = ("COP31 pact rejected  ·  Poland's Kh-101 confirmation  ·  Houthi Rabigh claim  ·  "
           "Hormuz strikes  ·  Libya drones  ·  Alcaraz wins ATP Finals  ·  Liverpool beat "
           "Man Utd  ·  Dymer strike  ·  Sudan strikes  ·  Cikande fire  ·  S. Korea minister quits.")
hw = d.textlength(dc_head, font=f_dcb)
lines = wrap(d, dc_text, f_dc, RX - MX - hw)
y = DY0
for ln in lines[:2]:
    d.text((MX + hw, y), ln, font=f_dc, fill=GREY)
    y += 13

f_src = font(F_SANS, 11)
centered(d, 1004, "Sources: Reuters, AP, AFP, BBC, The Hindu, Al Jazeera, CBS, Indian Express, Philstar, IANS.",
         f_src, GREY)

img.save("/home/hatch/workspace/makefun-kit/news-image-build/entry-20261123.png")
print("saved", img.size)
