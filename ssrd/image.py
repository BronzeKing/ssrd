# encoding: utf-8

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
now = datetime.now().strftime("%Y-%m-%d")


im = Image.open("demo.png").convert('RGBA')
txt = Image.new('RGBA', im.size, (0, 0, 0, 0))
d = ImageDraw.Draw(txt)
font=ImageFont.truetype("c:/Windows/fonts/Tahoma.ttf", 20)

d.text(
    (txt.size[0] - 80, txt.size[1] - 30),
    str(now),
    font=font,
    fill=(255, 255, 255, 255))
out = Image.alpha_composite(im, txt)
out.show()
