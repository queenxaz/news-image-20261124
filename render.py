"""Render THE WORLD TODAY - Tuesday 24 November 2026 front page.

Deterministic PIL drawing: no network, no randomness, no clock. Every
story was verified against real reporting dated 24 November 2026.
"""
import math
import os

W, H = 1024, 1024

INK = (18, 18, 18)
PAPER = (250, 247, 238)
RED = (178, 34, 34)
DARKRED = (122, 20, 20)
GOLD = (176, 132, 24)
NAVY = (24, 48, 88)
TEAL = (14, 110, 110)
GREEN = (26, 110, 58)
GREY = (96, 96, 96)
LIGHTGREY = (228, 224, 212)
RULE = (180, 175, 160)
BLUE = (30, 80, 160)

# (n, headline, summary, region, field, confidence, source, icon, lon, lat)
ILLUSTRATED = [
    (1, "HUANG IS BACK: NVIDIA REINSTATES ITS CEO",
     "Board unanimously brings Jensen Huang back 11 days after he quit; Trump says he persuaded the board.",
     "N. America", "Tech", "CONFIRMED", "Reuters / WSJ", "chip", -112, 45),
    (2, "COP31 COLLAPSES IN ANTALYA",
     "90+ nations reject the draft after ~50 hours overtime.",
     "Europe", "Climate", "CONFIRMED", "Grist / Reuters", "sun", 27, 38),
    (3, "MINES IN THE HORMUZ STRAIT",
     "IRGC claims 3 tankers hit mines; US sanctions 22 Iran entities.",
     "Mid. East", "Conflict", "CLAIM", "US Treasury", "burst", 56, 26),
    (4, "WAR WIDENS TO LIBYA",
     "Russia vows a response; Libya seeks a UN probe after Ukraine's claimed sinking of the corvette Merkury.",
     "Africa", "Conflict", "REPORTED", "Mid. East Eye", "ship", 17, 32),
    (5, "ZAPORIZHZHIA HIT OVERNIGHT",
     "Russian attack kills 2 and wounds 22, including 2 children, officials say.",
     "Europe", "Conflict", "CONFIRMED", "Reuters", "burst", 40, 52),
    (6, "RUSSIAN JETS ENTER KOREA ZONE",
     "Seoul alerts Ulleung Island and scrambles fighters after warplanes enter its defence zone.",
     "Asia-Pacific", "Security", "CONFIRMED", "Reuters", "plane", 126, 38),
    (7, "GAZA STRIKES KILL THREE",
     "Israeli strikes kill 3, including UNRWA worker Adel al-Helou in Jabalia camp.",
     "Mid. East", "Conflict", "CONFIRMED", "Al Jazeera", "burst", 34, 31),
    (8, "'EL CHAPO ISIDRO' CAUGHT",
     "Mexico nabs the alleged drug lord and will try him at home, defying a US extradition request.",
     "N. America", "Crime", "CONFIRMED", "Reuters", "lens", -100, 25),
    (9, "WALL STREET ROARS BACK",
     "S&P +4.7%, Nasdaq +6.5%, Dow +3.0% - best day since April; Nvidia +31%, its biggest since 2003.",
     "N. America", "Markets", "CONFIRMED", "Reuters / CNBC", "bars", -74, 41),
    (10, "ASIA SURGES ON THE AI TRADE",
     "Kospi +7.5%, Taiex +9.1%, Nikkei +4.5%; SK Hynix +8.6% and Samsung +8.2%.",
     "Asia-Pacific", "Markets", "CONFIRMED", "Reuters / WSJ", "bars", 141, 36),
    (11, "MEGASPEED BLACKLISTED",
     "US puts the Singapore chip firm at the heart of the Nvidia spy scandal on its trade blacklist.",
     "Asia-Pacific", "Tech", "CONFIRMED", "Spyglass", "chip", 103, 2),
    (12, "TRUMP WARNS IRAN: 'VERY TRAUMATIC'",
     "President warns of a 'very traumatic' outcome if no nuclear deal; a second carrier is weighed.",
     "N. America", "Diplomacy", "CONFIRMED", "Access24", "flag", -84, 33),
    (13, "FACTORY FIRE IN INDONESIA",
     "Major blaze at an industrial plant kills several; workers missing as rescue teams dig in.",
     "Asia-Pacific", "Disaster", "REPORTED", "Careerindia", "flame", 112, -7),
    (14, "50M CHILDREN TO BE VACCINATED",
     "Bangladesh begins a month-long typhoid drive against drug-resistant strains.",
     "Asia-Pacific", "Health", "CONFIRMED", "Access24", "cross", 90, 24),
    (15, "DRAW IN WELLINGTON",
     "India-New Zealand first Test ends in a draw after five days at the Basin Reserve.",
     "Asia-Pacific", "Sport", "CONFIRMED", "Careerindia", "ball", 175, -41),
]

# (n, one-line text, field)
ALSO = [
    (16, "SK Hynix US shares surge 20% on Huang return", "Markets"),
    (17, "CrowdStrike to buy Zscaler for $43.9bn", "Business"),
    (18, "SoftBank to invest $2bn in Intel", "Business"),
    (19, "Gold rebounds to ~$3,640/oz; silver up 4.6%", "Markets"),
    (20, "Brent ~$89, WTI below $80 as oil slides ~4%", "Markets"),
    (21, "Bitcoin ~$60,600; Ethereum ~$1,700", "Crypto"),
    (22, "US flash PMI 54.6; Fed flags 3.5% inflation", "Economy"),
    (23, "Singapore Q3 GDP grows 6.1% year on year", "Economy"),
    (24, "Japan factory PMI 53.7 as Nikkei leads the rally", "Economy"),
    (25, "Russia rebuilding base ~60km from Finland", "Security"),
    (26, "NATO sends AWACS radar plane to Poland", "Security"),
    (27, "Russia earmarks $576m for Kaliningrad rail ferries", "Security"),
    (28, "Saudi coalition downs Houthi drone", "Conflict"),
    (29, "Iran claims it shot down a US drone over the Gulf", "Conflict"),
    (30, "Roosevelt flies round-the-clock Iran sorties", "Military"),
    (31, "India keeps 3rd place in the Asia Power Index", "Diplomacy"),
    (32, "Spain polls: right set to oust Sanchez on 29 Nov", "Politics"),
    (33, "US toughens citizenship test and H-1B visas", "Politics"),
    (34, "ICE arrests at Seattle airport called 'appalling'", "Politics"),
    (35, "FAA lifts O'Hare ground stop after staffing snarl", "Transport"),
    (36, "Indian army hunts missing after Himalayan flood", "Disaster"),
    (37, "Deadly storm displaces thousands in a Brazil town", "Disaster"),
    (38, "Two Nigerians die serving in the Russian military", "Conflict"),
    (39, "UN chief: agree AI rules within a year", "Tech"),
    (40, "Australia to treat AI as a foreign-policy challenge", "Tech"),
    (41, "Georgia plans full surrogacy ban over trafficking", "Law"),
    (42, "Al-Ittihad beat Pakhtakor 2-0 in AFC Elite", "Sport"),
    (43, "Al Quwa Al Jawiya beat Al Gharafa 2-1", "Sport"),
    (44, "Al Ain 1-1 Esteghlal; Neftchi 2-2 Al Hilal", "Sport"),
    (45, "Sun's storms mapped in 12,740-image Nature set", "Science"),
    (46, "Japan hosts US Treasury chief before trade deadline", "Trade"),
    (47, "Trump announces Japan trade deal; Nikkei rallies", "Trade"),
    (48, "Trump's Indonesia deal; EU threatens $84bn tariffs", "Trade"),
]

LEFT_OUT = [
    "EU's 22nd Russia sanctions package proposed",
    "Zelensky offers four-way talks 'literally tomorrow'",
    "Sparta II towed out of Finnish waters",
    "Perm drone strike kills 1 in Russia",
    "US university shooting kills 2",
    "First report of the Merkury sinking claim",
]

NOT_YET = [
    "Spain general election, Sun 29 Nov",
    "US Senate vote on $9.4bn aid cuts",
    "Tonight's Champions League ties: Arsenal-Dortmund, Man City-Napoli, Real Madrid-PSV",
]

TIMELINE = [
    ("00:00", "Asia opens: Kospi +7.5%, Nikkei +4.5%"),
    ("04:00", "Reuters: Russian strike kills 2 in Zaporizhzhia"),
    ("06:00", "Seoul: Russian jets in air zone, Ulleung alert"),
    ("08:00", "US Treasury sanctions 22 Iran entities"),
    ("10:00", "COP31 collapses in Antalya"),
    ("13:00", "Nvidia confirms Huang return; S&P +4.7%"),
    ("19:30", "Brent settles ~$89, WTI below $80"),
]

NUMBERS = [
    ("+31%", "Nvidia"),
    ("~$1tn", "value restored"),
    ("+4.7%", "S&P 500"),
    ("+7.5%", "Kospi"),
    ("+9.1%", "Taiex"),
    ("50m", "children vaccinated"),
]

SOURCES = ("Reuters, Wall Street Journal, Bloomberg, Al Jazeera, CNBC, Grist, "
           "Middle East Eye, RFE/RL, The AFC, The Daily Edition, Spyglass, "
           "Market Index. Original drawings.")


# ---------------------------------------------------------------- helpers

def _font(name, size):
    from PIL import ImageFont
    paths = {
        "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    }
    return ImageFont.truetype(paths[name], size)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_one(draw, text, font, max_w):
    if draw.textlength(text, font=font) <= max_w:
        return text
    while text and draw.textlength(text + "...", font=font) > max_w:
        text = text[:-1]
    return text + "..."


def _star(draw, cx, cy, r, color):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=color)


def icon(draw, x, y, s, kind, bg):
    draw.rounded_rectangle([x, y, x + s, y + s], radius=4, fill=bg)
    c = (255, 255, 255)
    m = s * 0.16
    if kind == "chip":
        draw.rectangle([x + m + 2, y + m + 2, x + s - m - 2, y + s - m - 2],
                       outline=c, width=2)
        for i in range(3):
            px = x + m + 5 + i * (s - 2 * m - 10) // 2
            draw.line([px, y + 2, px, y + m + 2], fill=c, width=2)
            draw.line([px, y + s - m - 2, px, y + s - 2], fill=c, width=2)
    elif kind == "sun":
        cx, cy, r = x + s / 2, y + s / 2, s * 0.22
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
        for a in range(8):
            ang = a * math.pi / 4
            draw.line([cx + r * 1.4 * math.cos(ang), cy + r * 1.4 * math.sin(ang),
                       cx + r * 2.0 * math.cos(ang), cy + r * 2.0 * math.sin(ang)],
                      fill=c, width=2)
    elif kind == "burst":
        _star(draw, x + s / 2, y + s / 2, s * 0.36, c)
    elif kind == "ship":
        draw.polygon([(x + m, y + s * 0.62), (x + s - m, y + s * 0.62),
                      (x + s - m - 4, y + s * 0.80), (x + m + 4, y + s * 0.80)],
                     fill=c)
        draw.rectangle([x + s * 0.42, y + m + 2, x + s * 0.58, y + s * 0.60],
                       fill=c)
    elif kind == "plane":
        draw.polygon([(x + m, y + s * 0.55), (x + s - m, y + s * 0.30),
                      (x + s * 0.62, y + s * 0.62), (x + s * 0.72, y + s * 0.72),
                      (x + s * 0.55, y + s * 0.68), (x + m + 6, y + s * 0.72)],
                     fill=c)
    elif kind == "lens":
        cx, cy, r = x + s * 0.42, y + s * 0.42, s * 0.26
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=2)
        draw.line([cx + r * 0.7, cy + r * 0.7, x + s - m, y + s - m],
                  fill=c, width=3)
    elif kind == "bars":
        for i, h in enumerate((0.35, 0.6, 0.9)):
            bx = x + m + 2 + i * (s - 2 * m - 4) // 3
            bw = (s - 2 * m - 4) // 3 - 3
            draw.rectangle([bx, y + s - m - h * (s - 2 * m), bx + bw,
                            y + s - m], fill=c)
    elif kind == "flame":
        draw.polygon([(x + s / 2, y + m), (x + s - m - 2, y + s * 0.55),
                      (x + s * 0.62, y + s - m), (x + s * 0.38, y + s - m),
                      (x + m + 2, y + s * 0.55)], fill=c)
    elif kind == "cross":
        t = s * 0.22
        draw.rectangle([x + s / 2 - t / 2, y + m, x + s / 2 + t / 2, y + s - m],
                       fill=c)
        draw.rectangle([x + m, y + s / 2 - t / 2, x + s - m, y + s / 2 + t / 2],
                       fill=c)
    elif kind == "ball":
        cx, cy, r = x + s / 2, y + s / 2, s * 0.34
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=2)
        draw.polygon([(cx, cy - r * 0.5), (cx + r * 0.5, cy),
                      (cx, cy + r * 0.5), (cx - r * 0.5, cy)], fill=c)
    elif kind == "flag":
        draw.line([x + m + 3, y + m, x + m + 3, y + s - m], fill=c, width=2)
        draw.polygon([(x + m + 3, y + m), (x + s - m, y + m + 4),
                      (x + m + 3, y + m + 9)], fill=c)
    else:
        draw.ellipse([x + m, y + m, x + s - m, y + s - m], fill=c)


# Rough continent polygons in (lon, lat), for the dotted map.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 73),
     (-75, 72), (-65, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 26),
     (-85, 20), (-90, 15), (-95, 18), (-105, 22), (-115, 30), (-125, 40),
     (-125, 49), (-140, 60), (-165, 60)],
    [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-40, -5), (-35, -8),
     (-40, -20), (-48, -28), (-55, -35), (-65, -40), (-70, -52),
     (-73, -40), (-75, -25), (-80, -15), (-80, 5)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (48, 11), (51, 12), (45, 0), (40, -10), (35, -18),
     (32, -28), (25, -34), (18, -32), (15, -20), (12, -5), (9, 4),
     (0, 5), (-8, 5), (-15, 10)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 70),
     (15, 70), (10, 68), (5, 60), (0, 55), (-5, 50), (-10, 43)],
    [(30, 62), (40, 68), (55, 72), (70, 73), (90, 75), (110, 76),
     (130, 72), (150, 70), (160, 66), (162, 60), (158, 52), (142, 50),
     (140, 40), (135, 35), (130, 33), (127, 35), (122, 38), (120, 30),
     (115, 22), (108, 18), (105, 10), (100, 8), (98, 15), (95, 16),
     (90, 22), (85, 20), (80, 13), (77, 8), (75, 15), (72, 20), (68, 23),
     (62, 25), (57, 26), (52, 28), (48, 30), (44, 30), (40, 32), (36, 36),
     (33, 36), (30, 38), (28, 42), (28, 48), (30, 55)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32),
     (150, -25), (146, -19), (142, -15), (140, -17), (136, -12),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
]


def _inside(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > lat) != (yj > lat)) and \
                (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def draw_map(draw, x0, y0, w, h, pins):
    def px(lon):
        return x0 + (lon + 180.0) / 360.0 * w
    def py(lat):
        return y0 + (90.0 - lat) / 180.0 * h
    step = 5
    gx = x0
    while gx < x0 + w:
        gy = y0
        while gy < y0 + h:
            lon = (gx - x0) / w * 360.0 - 180.0
            lat = 90.0 - (gy - y0) / h * 180.0
            if any(_inside(lon, lat, p) for p in CONTINENTS):
                draw.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=NAVY)
            gy += step
        gx += step
    for n, lon, lat in pins:
        cx, cy = px(lon), py(lat)
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=GOLD,
                     outline=(255, 255, 255), width=1)
        f = _font("bold", 9)
        tw = draw.textlength(str(n), font=f)
        draw.text((cx - tw / 2, cy - 5), str(n), font=f, fill=(255, 255, 255))


# ------------------------------------------------------------- layout

ALSO_REGION = {
    16: "Asia-Pacific", 17: "N. America", 18: "Asia-Pacific",
    19: "Global", 20: "Global", 21: "Global", 22: "N. America",
    23: "Asia-Pacific", 24: "Asia-Pacific", 25: "Europe", 26: "Europe",
    27: "Europe", 28: "Mid. East", 29: "Mid. East", 30: "Mid. East",
    31: "Asia-Pacific", 32: "Europe", 33: "N. America", 34: "N. America",
    35: "N. America", 36: "Asia-Pacific", 37: "Latin America",
    38: "Europe", 39: "Global", 40: "Asia-Pacific", 41: "Europe",
    42: "Mid. East", 43: "Mid. East", 44: "Mid. East", 45: "Global",
    46: "Asia-Pacific", 47: "Asia-Pacific", 48: "Asia-Pacific",
}

REGION_COLORS = {
    "N. America": NAVY, "Europe": TEAL, "Mid. East": RED,
    "Asia-Pacific": GREEN, "Africa": GOLD, "Latin America": (140, 70, 140),
    "Global": GREY,
}

FIELD_COLORS = {
    "Tech": GREEN, "Climate": TEAL, "Conflict": RED, "Security": NAVY,
    "Crime": (90, 40, 40), "Markets": (30, 90, 30), "Diplomacy": BLUE,
    "Disaster": (150, 80, 10), "Health": (180, 40, 90), "Sport": (90, 60, 160),
    "Business": (60, 60, 60), "Economy": (30, 90, 30), "Crypto": (160, 110, 0),
    "Military": NAVY, "Politics": BLUE, "Law": (60, 60, 60),
    "Science": TEAL, "Trade": (30, 90, 30), "Transport": (60, 60, 60),
}


def _counts():
    regions = {}
    for s in ILLUSTRATED:
        regions[s[3]] = regions.get(s[3], 0) + 1
    for a in ALSO:
        r = ALSO_REGION[a[0]]
        regions[r] = regions.get(r, 0) + 1
    fields = {}
    for s in ILLUSTRATED:
        fields[s[4]] = fields.get(s[4], 0) + 1
    for a in ALSO:
        fields[a[2]] = fields.get(a[2], 0) + 1
    return regions, fields


def _rule(draw, x0, x1, y, color=RULE, width=1):
    draw.line([x0, y, x1, y], fill=color, width=width)


def render(path):
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    regions, fields = _counts()
    total = len(ILLUSTRATED) + len(ALSO)

    # ---- masthead ----
    f_title = _font("serif", 46)
    t = "THE WORLD TODAY"
    draw.text(((W - draw.textlength(t, font=f_title)) / 2, 6), t,
              font=f_title, fill=INK)
    f_date = _font("bold", 19)
    d = "TUESDAY 24 NOVEMBER 2026"
    draw.text(((W - draw.textlength(d, font=f_date)) / 2, 58), d,
              font=f_date, fill=DARKRED)
    f_meta = _font("bold", 12)
    m = "%d STORIES  |  %d REGIONS  |  %d FIELDS  |  DATE-CHECKED" % (
        total, len(regions), len(fields))
    draw.text(((W - draw.textlength(m, font=f_meta)) / 2, 82), m,
              font=f_meta, fill=NAVY)
    f_sub = _font("sans", 13)
    sub = ("Huang is back at Nvidia, COP31 collapses, and mines appear in the "
           "Hormuz Strait \u2014 every story here happened, or was first "
           "reported, on this day.")
    for i, ln in enumerate(wrap(draw, sub, f_sub, W - 60)):
        draw.text(((W - draw.textlength(ln, font=f_sub)) / 2, 100 + i * 16),
                  ln, font=f_sub, fill=INK)
    _rule(draw, 16, W - 16, 130, color=INK, width=2)

    # ---- UTC timeline ----
    y = 136
    f_lab = _font("bold", 11)
    draw.text((16, y), "THE DAY IN UTC", font=f_lab, fill=RED)
    f_tl = _font("sans", 10)
    f_tt = _font("bold", 10)
    x = 130
    col_w = (W - 16 - 130) // len(TIMELINE)
    for tm, txt in TIMELINE:
        draw.text((x, y), tm, font=f_tt, fill=NAVY)
        for i, ln in enumerate(wrap(draw, txt, f_tl, col_w - 8)):
            draw.text((x, y + 12 + i * 12), ln, font=f_tl, fill=INK)
        x += col_w
    _rule(draw, 16, W - 16, 172)

    # ---- leads ----
    y = 178
    # lead 1, big
    n, head, summ, reg, field, conf, src, ic, lon, lat = ILLUSTRATED[0]
    draw.rectangle([16, y, 512, y + 122], outline=INK, width=2)
    draw.rectangle([16, y, 512, y + 26], fill=DARKRED)
    f_lh = _font("bold", 16)
    draw.text((24, y + 4), "1  " + head, font=f_lh, fill=(255, 255, 255))
    f_ls = _font("sans", 12)
    for i, ln in enumerate(wrap(draw, summ, f_ls, 300)):
        draw.text((24, y + 34 + i * 15), ln, font=f_ls, fill=INK)
    draw.text((24, y + 34 + 3 * 15), "%s  |  %s  |  %s" % (reg, conf, src),
              font=_font("bold", 10), fill=GREY)
    # flat chip illustration + rising arrow
    ix, iy = 340, y + 32
    draw.rectangle([ix, iy, ix + 150, iy + 82], fill=(16, 60, 40))
    draw.rectangle([ix + 48, iy + 22, ix + 102, iy + 60], outline=GOLD,
                   width=3)
    for k in range(4):
        px = ix + 56 + k * 14
        draw.line([px, iy + 14, px, iy + 22], fill=GOLD, width=2)
        draw.line([px, iy + 60, px, iy + 68], fill=GOLD, width=2)
    draw.line([ix + 12, iy + 70, ix + 60, iy + 44, ix + 95, iy + 52,
               ix + 138, iy + 12], fill=(255, 255, 255), width=3)
    draw.polygon([(ix + 138, iy + 12), (ix + 126, iy + 12),
                  (ix + 138, iy + 24)], fill=(255, 255, 255))
    draw.text((ix + 52, iy + 30), "NVDA", font=_font("bold", 13),
              fill=(255, 255, 255))
    draw.text((ix + 8, iy + 66), "+31%", font=_font("bold", 12),
              fill=(255, 220, 100))
    # leads 2 and 3, stacked right
    ly = y
    for s in ILLUSTRATED[1:3]:
        n, head, summ, reg, field, conf, src, ic, lon, lat = s
        draw.rectangle([520, ly, W - 16, ly + 57], outline=RULE, width=1)
        draw.rectangle([520, ly, 548, ly + 57], fill=NAVY)
        f_n = _font("bold", 16)
        tw = draw.textlength(str(n), font=f_n)
        draw.text((534 - tw / 2, ly + 18), str(n), font=f_n,
                  fill=(255, 255, 255))
        icon(draw, 556, ly + 9, 38, ic, FIELD_COLORS.get(field, NAVY))
        f_h = _font("bold", 13)
        draw.text((602, ly + 5), fit_one(draw, head, f_h, W - 16 - 602),
                  font=f_h, fill=INK)
        f_s = _font("sans", 11)
        for i, ln in enumerate(wrap(draw, summ, f_s, W - 16 - 602)[:1]):
            draw.text((602, ly + 22 + i * 13), ln, font=f_s, fill=INK)
        draw.text((602, ly + 44), "%s  |  %s  |  %s" % (reg, conf, src),
                  font=_font("bold", 9), fill=GREY)
        ly += 65
    _rule(draw, 16, W - 16, 306)

    # ---- illustrated grid, stories 4-15 ----
    f_h = _font("bold", 11)
    f_s = _font("sans", 10)
    f_g = _font("bold", 9)
    cell_w, cell_h = 325, 58
    for idx, s in enumerate(ILLUSTRATED[3:]):
        n, head, summ, reg, field, conf, src, ic, lon, lat = s
        col, row = idx % 3, idx // 3
        cx = 16 + col * (cell_w + 8)
        cy = 314 + row * (cell_h + 4)
        draw.rectangle([cx, cy, cx + cell_w, cy + cell_h], outline=RULE,
                       width=1)
        draw.ellipse([cx + 6, cy + 6, cx + 26, cy + 26], fill=GOLD)
        f_n = _font("bold", 11)
        tw = draw.textlength(str(n), font=f_n)
        draw.text((cx + 16 - tw / 2, cy + 10), str(n), font=f_n,
                  fill=(255, 255, 255))
        icon(draw, cx + 32, cy + 6, 28, ic, FIELD_COLORS.get(field, NAVY))
        tx = cx + 66
        draw.text((tx, cy + 4), fit_one(draw, head, f_h, cell_w - 72),
                  font=f_h, fill=INK)
        for i, ln in enumerate(wrap(draw, summ, f_s, cell_w - 72)[:2]):
            draw.text((tx, cy + 20 + i * 12), ln, font=f_s, fill=INK)
        draw.text((tx, cy + 46), "%s  |  %s  |  %s" % (reg, conf, src),
                  font=f_g, fill=GREY)
    _rule(draw, 16, W - 16, 564)

    # ---- map + date check ----
    y = 572
    f_sec = _font("bold", 11)
    draw.text((16, y), "WHERE IT HAPPENED \u2014 15 PINNED STORIES",
              font=f_sec, fill=NAVY)
    draw.rectangle([16, y + 16, 508, y + 130], outline=RULE, width=1)
    pins = [(s[0], s[8], s[9]) for s in ILLUSTRATED]
    draw_map(draw, 20, y + 20, 484, 102, pins)
    # date check box
    draw.rectangle([516, y, W - 16, y + 130], outline=DARKRED, width=2)
    draw.rectangle([516, y, W - 16, y + 18], fill=DARKRED)
    draw.text((524, y + 3), "DATE CHECK \u2014 WHAT WE LEFT OUT, AND WHY",
              font=f_sec, fill=(255, 255, 255))
    f_dc = _font("sans", 10)
    f_dcb = _font("bold", 10)
    dy = y + 21
    draw.text((524, dy), "TODAY 24 NOV:", font=f_dcb, fill=GREEN)
    draw.text((614, dy), "All 48 stories on this page.", font=f_dc, fill=INK)
    dy += 13
    draw.text((524, dy), "LEFT OUT \u2014 23 NOV:", font=f_dcb, fill=DARKRED)
    dy += 12
    half = (len(LEFT_OUT) + 1) // 2
    for i, item in enumerate(LEFT_OUT):
        col_x = 524 if i < half else 770
        row_y = dy + (i % half) * 11
        draw.text((col_x, row_y), "\u2022 " + fit_one(
            draw, item, f_dc, 232), font=f_dc, fill=INK)
    dy += half * 11 + 3
    draw.text((524, dy), "NOT YET \u2014 25 NOV +:", font=f_dcb, fill=NAVY)
    dy += 12
    for item in NOT_YET:
        draw.text((524, dy), "\u2022 " + fit_one(draw, item, f_dc, 470),
                  font=f_dc, fill=INK)
        dy += 11
    _rule(draw, 16, W - 16, 708)

    # ---- also on ----
    y = 714
    draw.text((16, y), "ALSO ON TUESDAY 24 NOVEMBER \u2014 33 MORE STORIES",
              font=f_sec, fill=NAVY)
    f_a = _font("sans", 11)
    f_ab = _font("bold", 11)
    for idx, a in enumerate(ALSO):
        col, row = idx // 11, idx % 11
        ax = 16 + col * 333
        ay = y + 18 + row * 17
        draw.text((ax, ay), "%d." % a[0], font=f_ab, fill=RED)
        txt = fit_one(draw, a[1], f_a, 333 - 30)
        draw.text((ax + 28, ay), txt, font=f_a, fill=INK)
    _rule(draw, 16, W - 16, 922)

    # ---- region bar + by field ----
    y = 928
    draw.text((16, y), "BY REGION", font=f_lab, fill=NAVY)
    order = ["Asia-Pacific", "N. America", "Europe", "Mid. East",
             "Global", "Africa", "Latin America"]
    bx = 96
    bar_w = 560
    for r in order:
        c = regions.get(r, 0)
        seg = bar_w * c / total
        draw.rectangle([bx, y, bx + seg - 1, y + 12],
                       fill=REGION_COLORS[r])
        bx += seg
    bx = 96
    for r in order:
        c = regions.get(r, 0)
        seg = bar_w * c / total
        if seg > 34:
            lab = "%s %d" % (r, c)
            tw = draw.textlength(lab, font=_font("bold", 9))
            draw.text((bx + (seg - tw) / 2, y + 1), lab,
                      font=_font("bold", 9), fill=(255, 255, 255))
        bx += seg
    draw.text((668, y), "48 stories, 7 regions", font=f_ab, fill=INK)
    f_f = _font("sans", 9)
    f_fb = _font("bold", 9)
    parts = ["%s %d" % (k, v) for k, v in sorted(
        fields.items(), key=lambda kv: (-kv[1], kv[0]))]
    draw.text((16, 944), "BY FIELD", font=f_fb, fill=NAVY)
    draw.text((96, 944), ", ".join(parts[:10]), font=f_f, fill=INK)
    draw.text((96, 955), ", ".join(parts[10:]), font=f_f, fill=INK)

    # ---- day in numbers ----
    y = 966
    _rule(draw, 16, W - 16, y)
    draw.text((16, y + 3), "THE DAY IN NUMBERS", font=f_lab, fill=RED)
    f_num = _font("bold", 12)
    f_nl = _font("sans", 9)
    for i, (num, lab) in enumerate(NUMBERS):
        nx = 16 + i * 166
        ny = y + 18
        draw.text((nx, ny), num, font=f_num, fill=DARKRED)
        nw = draw.textlength(num + " ", font=f_num)
        draw.text((nx + nw, ny + 2), fit_one(draw, lab, f_nl, 166 - nw - 4),
                  font=f_nl, fill=INK)

    # ---- footer: how sure + sources ----
    y = 997
    _rule(draw, 16, W - 16, y)
    f_ft = _font("sans", 9)
    f_ftb = _font("bold", 9)
    draw.text((16, y + 4),
              "HOW SURE:  CONFIRMED - verified by the outlet   "
              "REPORTED - the outlet reports it   "
              "CLAIM - one side claims it",
              font=f_ftb, fill=INK)
    draw.text((16, y + 15), "Sources: " + SOURCES, font=f_ft, fill=GREY)

    img.save(path, "JPEG", quality=88, optimize=True)
    return path
