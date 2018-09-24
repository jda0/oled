#!/usr/bin/env python

import datetime
import subprocess
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
disp.begin()

cmd = "iwgetid -r"
SSID = subprocess.check_output(cmd, shell=True)
cmd = "hostname -I | cut -d\' \' -f1"
IP = subprocess.check_output(cmd, shell=True)

while 1:
    image = Image.new('1', (disp.width / 3, disp.height / 3))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    disp.clear()

    now = datetime.datetime.utcnow()
    doy = (now.date() - datetime.date(now.year, 1, 1)).days + 1
    dec = (
        now.year % 100,
        '+' if doy >= 14*26 else chr(65 + doy / 14),
        doy % 14,
        ((now.hour * 3600 + now.minute * 60 + now.second + now.microsecond * 1e-6) / 86.4) % 1000
    )

    draw.text((2, 1), format(dec[3], '03.0f'), font=font, fill=255)

    image = image.resize((disp.width, disp.height))
    draw = ImageDraw.Draw(image)

    draw.text((60, 10), "." + str(int((dec[3] * 10) % 10)), font=font, fill=255)
    draw.text((0, 31), " " + format(dec[0], '02') + dec[1] + format(dec[2], '02'), font=font, fill=255)
    draw.line((5, disp.height - 20, 127, disp.height - 20), fill=255)
    draw.text((0, disp.height - 19), " " + str(SSID), font=font, fill=255)
    draw.text((0, disp.height - 11), " " + str(IP), font=font, fill=255)

    disp.image(image)
    disp.display()
    time.sleep(1)

