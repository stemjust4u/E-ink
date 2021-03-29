#!/usr/bin/python3
# Demo version with shorter show time
#
# Use commands below in a terminal
# Have script run at boot = $ sudo systemctl enable e-ink-art
# (use disable to stop at boot)
# To start/stop script = $ sudo systemctl stop e-ink-art
#
# To clear screen $ /E-ink/bin/e-ink-clear.py
# To run shorter demo $ /E-ink/bin/e-ink-demo.py

# Images should fit e-ink screen of 400X300 pixels
# Best format is bmp or png

import sys
import os
import socket

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

SHOWTIME = 5 # How long to show the e-art in seconds

fontsdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'fonts')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
album_art_dir = '/home/osmc/Pictures/'

if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import traceback
from waveshare_epd import epd4in2
import time
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("OSMC/Kode e-ink display")
    
    epd = epd4in2.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    
    font24 = ImageFont.truetype(os.path.join(fontsdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(fontsdir, 'Font.ttc'), 18)
    font35 = ImageFont.truetype(os.path.join(fontsdir, 'Font.ttc'), 35)

    Himage = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(Himage)
    draw.text((10, 5), 'Web remote is at:', font = font24, fill = 0)
    draw.text((10, 35), 'http://' + hostname + '.local', font = font24, fill = 0)
    draw.text((10, 65), 'or go to ', font = font24, fill = 0)
    draw.text((10, 95), 'http://' + ip_address + ':80', font = font24, fill = 0)
    draw.text((10, 125), 'to login from a terminal', font = font24, fill = 0)
    draw.text((10, 155), '$ ssh osmc@' + hostname + '.local', font = font24, fill =0)
    draw.text((10, 185), '$ sudo systemctl stop e-ink-art', font = font24, fill =0)
    draw.text((10, 215), 'stop/start and enable/disable for', font = font24, fill =0) 
    draw.text((10, 245), 'turning start at boot on/off', font = font24, fill =0) 
    draw.rectangle((5, 5, 395, 295), outline = 0)
    epd.display(epd.getbuffer(Himage))
    time.sleep(SHOWTIME)

    Himage = Image.new(mode='1', size= (epd.width, epd.height), color=255)
    draw=ImageDraw.Draw(Himage)
    album_art = os.listdir(album_art_dir)
    while True:
        for picture in album_art:
            album_art_img = Image.open(os.path.join(album_art_dir, picture))
            Himage.paste(album_art_img, (0, 0))
            epd.display(epd.getbuffer(Himage))
            time.sleep(SHOWTIME)

    # epd.Clear()
    # logging.info("Goto Sleep...")
    # epd.sleep()
    
except IOError as e:
    logging.info(e)
    epd.Clear()
    
except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd.Clear()
    epd4in2.epdconfig.module_exit()
    exit()
