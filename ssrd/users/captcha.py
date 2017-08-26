# encoding: utf-8
from datetime import datetime
import hashlib
import base64

from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from io import StringIO
from rest_framework.views import APIView


class CaptchaView(APIView):
    authentication_classes = []
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        # import Image, ImageDraw, ImageFont, md5,cStringIO

        buf = StringIO()
        img_width = 148
        img_height = 34
        font_size = 38
        background = (200, 200, 200)
        im = Image.new('RGB', (img_width, img_height), background)
        draw = ImageDraw.Draw(im)
        mp_src = hashlib.md5(str(datetime.now()).encode()).hexdigest()
        rand_str = mp_src[0:4]
        font_path = str(settings.APPS_DIR.path('static/fonts/Vera.ttf'))
        font = ImageFont.truetype(font_path, font_size)
        draw.text((25, -5), rand_str, font=font)
        draw.text((36, 4), rand_str, font=ImageFont.load_default())

        del draw
        request.session['image_code'] = rand_str
        request.session.save()
        im.save(buf, 'gif')

        captcha = base64.b64encode(buf.getvalue())

        result = dict(captcha=captcha)
        return result
