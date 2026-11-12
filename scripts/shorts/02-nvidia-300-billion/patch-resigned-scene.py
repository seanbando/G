import sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = sys.argv[1]
W, H, FPS, DUR = 864, 1536, 30, 3.7
anchor = Image.open(f"{S}/f_21.6.png").convert("RGB")
ceo_src = Image.open(f"{S}/f_18.4.png").convert("RGB")
bg = anchor.getpixel((20, 20))
font = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"

# Anchor frame with "THIS JUST IN" on the red desk banner (spoken words).
a = anchor.copy(); d = ImageDraw.Draw(a)
f = ImageFont.truetype(font, 62)
d.text((344, 802), "THIS JUST IN", font=f, fill="white", anchor="mm")

# CEO crop, scaled up onto a clean board.
src = ceo_src.copy(); ImageDraw.Draw(src).rectangle((480, 380, 590, 770), fill=bg)
crop = src.crop((500, 420, 830, 1060))
scale = 1180 / crop.height
crop = crop.resize((int(crop.width * scale), 1180), Image.LANCZOS)
ceo = Image.new("RGB", (W, H), bg)
ceo.paste(crop, ((W - crop.width) // 2, 170))

# RESIGNED stamp on a transparent layer.
sf = ImageFont.truetype(font, 128)
tw = int(ImageDraw.Draw(ceo).textlength("RESIGNED", font=sf))
stamp = Image.new("RGBA", (tw + 80, 220), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
red = (196, 30, 45, 235)
sd.rounded_rectangle((8, 8, stamp.width - 8, stamp.height - 8), radius=18, outline=red, width=12)
sd.text((stamp.width // 2, stamp.height // 2 + 4), "RESIGNED", font=sf, fill=red, anchor="mm")
stamp = stamp.rotate(-9, expand=True, resample=Image.BICUBIC)

def zoom(img, z, cx, cy):
    w, h = W / z, H / z
    x0 = min(max(cx - w / 2, 0), W - w); y0 = min(max(cy - h / 2, 0), H - h)
    return img.crop((x0, y0, x0 + w, y0 + h)).resize((W, H), Image.LANCZOS)

n = int(DUR * FPS)
for i in range(n):
    t = i / FPS
    if t < 1.0:                                   # 37.3-38.3 "This just in"
        fr = zoom(a, 1.30 + 0.10 * t, 344, 590)
        flash = max(0.0, 1 - t / 0.22)
        if flash > 0:
            fr = Image.blend(fr, Image.new("RGB", (W, H), "white"), flash * 0.9)
    else:                                         # 38.3-41.0 CEO, then the stamp
        u = t - 1.0
        fr = zoom(ceo, 1.0 + 0.05 * u, W / 2, 700).convert("RGBA")
        st = t - 2.0                              # stamp lands on "resigned" (39.3)
        if st >= 0:
            k = 1.0 + 0.8 * max(0.0, 1 - st / 0.12)
            s = stamp.resize((int(stamp.width * k), int(stamp.height * k)), Image.LANCZOS)
            fr.alpha_composite(s, (W // 2 - s.width // 2, 1180 - s.height // 2))
        fr = fr.convert("RGB")
        sh = t - 3.2                              # shake on the door slam (40.5)
        if 0 <= sh < 0.22:
            amp = 14 * (1 - sh / 0.22)
            dx = int(amp * math.sin(sh * 90)); dy = int(amp * math.cos(sh * 70))
            fr = zoom(fr, 1.03, W / 2 - dx, H / 2 - dy)
    fr.save(f"{S}/ins/{i:04d}.png")
print(n, "frames, background", bg)
