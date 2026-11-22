#!/usr/bin/env python3
"""Draw poster.png: a newspaper front page summing up world news of Sunday
22 November 2026 (headlines from that morning's wire reports). Pillow only.
Run: python3 render_poster.py  -> writes poster.png beside this file."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

W = H = 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
RED = (179, 35, 27)
NAVY = (29, 58, 95)
GREY = (90, 86, 78)
RULE = (60, 56, 48)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, max_w, kicker, headline, deck, head_size=25):
    draw.text((x, y), kicker, font=font(SANS_B, 14), fill=RED)
    y += 22
    hf = font(SERIF_B, head_size)
    for line in wrap(draw, headline, hf, max_w):
        draw.text((x, y), line, font=hf, fill=INK)
        y += head_size + 5
    y += 2
    df = font(SERIF, 15)
    for line in wrap(draw, deck, df, max_w):
        draw.text((x, y), line, font=df, fill=(52, 50, 44))
        y += 20
    return y


def globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)
    for k in (-0.66, -0.33, 0.0, 0.33, 0.66):
        w = r * (1 - k * k) ** 0.5
        draw.ellipse([cx - w, cy - r, cx + w, cy + r], outline=(120, 145, 175), width=1)
        draw.line([cx - w, cy + k * r, cx + w, cy + k * r], fill=(120, 145, 175), width=1)
    draw.line([cx - r, cy, cx + r, cy], fill=(120, 145, 175), width=1)
    # dateline dots: (dx, dy) as fractions of r, label, label offset in px
    spots = [
        (-0.62, -0.28, "WASHINGTON", 9, 2),
        (-0.48, 0.42, "BRAZIL / PERU", 9, -6),
        (0.02, -0.42, "PARIS", -40, -16),
        (0.30, -0.05, "GULF / RED SEA", 9, -6),
        (0.58, -0.30, "SEOUL", -16, 9),
        (0.52, 0.18, "MYANMAR / INDIA", -108, -6),
    ]
    for dx, dy, label, tx, ty in spots:
        px, py = cx + dx * r, cy + dy * r
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED)
        draw.text((px + tx, py + ty), label, font=font(SANS_B, 11), fill=NAVY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 44  # page margin

    # Masthead
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 58)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 26), title, font=tf, fill=INK)
    d.line([M, 100, W - M, 100], fill=INK, width=3)
    d.line([M, 106, W - M, 106], fill=INK, width=1)
    dateline = "SUNDAY · 22 NOVEMBER 2026 · THE DAY'S WORLD NEWS ON ONE PAGE"
    df = font(SANS_B, 16)
    dw = d.textlength(dateline, font=df)
    d.text(((W - dw) / 2, 114), dateline, font=df, fill=NAVY)
    d.line([M, 140, W - M, 140], fill=RULE, width=1)

    # Lead story, left; globe, right
    y = block(
        d, M, 156, 520,
        "MIDDLE EAST — LEAD STORY",
        "Iran strikes three tankers; Houthis hit Saudi capital",
        "Tehran parades missile launchers as Gulf and Red Sea tensions boil "
        "over on a violent Sunday, with shipping in the crosshairs. The "
        "Houthis call their strike on Riyadh revenge; oil markets brace for "
        "Monday's open as the region's wars widen.",
        head_size=34,
    )
    globe(d, 800, 262, 118)
    cap = "Where today's stories broke"
    cf = font(SERIF_I, 14)
    d.text((800 - d.textlength(cap, font=cf) / 2, 392), cap, font=cf, fill=GREY)
    d.line([M, 424, W - M, 424], fill=RULE, width=2)

    # Six secondary stories in two rows of three
    stories = [
        ("WASHINGTON", "Hackers breach US Agriculture Dept and FBI",
         "Trump ousts the cyber director after tech outages spark criticism."),
        ("MARKETS & AI", "Nvidia faces US accounting probe",
         "South Korea's Lee warns speed is decisive in the AI race."),
        ("AMERICAS", "Brazil town digs out after deadly storm",
         "'We lost everything': rubble cleared as a 6.7 quake rattles Peru."),
        ("EUROPE", "French protesters rally for a sixth weekend",
         "Living costs and public services bring crowds back to the streets."),
        ("ASIA", "Rohingya hail genocide verdict on Myanmar",
         "Kim Jong Un tours factories after a 'Trump snub'."),
        ("MONEY & POWER", "Trump vows 10% cap on credit-card rates",
         "Pentagon moves to curb US–Canada defence ties; Taiwan warns Ottawa."),
    ]
    col_w = (W - 2 * M - 2 * 28) // 3
    for i, (kicker, headline, deck) in enumerate(stories):
        x = M + (i % 3) * (col_w + 28)
        y = 442 + (i // 3) * 196
        if i % 3:
            d.line([x - 14, y, x - 14, y + 168], fill=(190, 182, 164), width=1)
        block(d, x, y, col_w, kicker, headline, deck, head_size=23)
    d.line([M, 838, W - M, 838], fill=RULE, width=2)

    # Also-today strip
    d.text((M, 852), "ALSO TODAY", font=font(SANS_B, 15), fill=RED)
    also = (
        "11 die after drinking tainted alcohol in India's Manipur · Opposition "
        "protests hit Meta's offices in India · Mao Shimada wins the Finlandia "
        "Trophy to reach the Grand Prix Final · An Anthropic researcher says "
        "Claude solved 'math's greatest riddle'"
    )
    y = 876
    af = font(SERIF, 17)
    for line in wrap(d, also, af, W - 2 * M):
        d.text((M, y), line, font=af, fill=INK)
        y += 23

    # Footer
    d.line([M, 958, W - M, 958], fill=INK, width=1)
    foot = "One page, one day — the world on Sunday 22 November 2026."
    ff = font(SERIF_I, 16)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 966), foot, font=ff, fill=GREY)

    img.save(HERE / "poster.png", optimize=True)
    print("wrote", HERE / "poster.png", img.size)


if __name__ == "__main__":
    main()
