#!/usr/bin/python3
# Full version with longer show time
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

SHOWTIME = 60 # How long to show the e-art in seconds

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
album_art_dir = '/home/osmc/Pictures/'

if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import traceback
from waveshare_epd import epd4in2
import time
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.CRITICAL) # Logging off (only CRITICAL). Set to DEBUG to get logging messages

def check_connection():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    if ip_address == '127.0.0.2':
        connected = False
    else:
        connected = True
    return connected, hostname, ip_address

def draw_ipAddress(Himage):
    draw.text((10, 1), 'Web remote is at:', font = font24, fill = 0)
    draw.text((10, 31), 'http://' + hostname + '.local', font = font24, fill = 0)
    draw.text((10, 61), 'or go to ', font = font24, fill = 0)
    draw.text((10, 91), 'http://' + ip_address + ':80', font = font24, fill = 0)
    draw.text((10, 121), 'to login from a terminal', font = font24, fill = 0)
    draw.text((10, 151), '$ ssh osmc@' + hostname + '.local', font = font24, fill =0)
    draw.text((10, 181), 'Music/Pictures are samba share', font = font24, fill =0)
    draw.text((10, 211), 'network: login as osmc', font = font24, fill =0)
    draw.text((10, 241), 'Windows: \\\\' + ip_address, font = font24, fill =0)
    draw.text((10, 271), 'Mac/Linux: smb://' + ip_address, font = font24, fill =0)

def no_connection_first(Himage):
    draw.text((10, 5), 'Not connected to wifi', font = font24, fill =0)
    draw.text((10, 35), 'Will check again after 5sec', font = font24, fill =0)

def no_connection_last(Himage):
    draw.text((10, 5), 'May not be connected to internet', font = font24, fill =0)
    draw.text((10, 35), 'Can try address below', font = font24, fill = 0)
    draw.text((10, 65), 'http://' + hostname + '.local', font = font24, fill = 0)
    draw.text((10, 95), 'If no connection, connect monitor,', font = font24, fill =0)
    draw.text((10, 125), 'go to My OSMC Network Settings', font = font24, fill =0)
    draw.text((10, 155), 'and enable/configure wireless', font = font24, fill =0)

try:
    logging.info("OSMC/Kode e-ink display")
    
    epd = epd4in2.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)

    connected, hostname, ip_address = check_connection()
    Himage = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(Himage)
    if connected:
        draw_ipAddress(Himage)
        logging.info("connected first time")
    else:
        no_connection_first(Himage)
        logging.info("not connected first time")
    #draw.rectangle((5, 5, 395, 295), outline = 0)
    epd.display(epd.getbuffer(Himage))
    
    # Check network connection one more time
    if not connected:
        logging.info("checking connection 2nd time")
        time.sleep(5)
        connected, hostname, ip_address = check_connection()
        Himage = Image.new('1', (epd.width, epd.height), 255)
        draw = ImageDraw.Draw(Himage)
        if connected:
            draw_ipAddress(Himage)
            logging.info("2nd check successful")
        else:
            no_connection_last(Himage)
            logging.info("2nd check failed")
        draw.rectangle((5, 5, 395, 295), outline = 0)
        epd.display(epd.getbuffer(Himage))

    time.sleep(15)

    Himage = Image.new(mode='1', size= (epd.width, epd.height), color=255)
    draw=ImageDraw.Draw(Himage)
    album_art = os.listdir(album_art_dir)

    # Quick demo of images
    for picture in album_art:
        album_art_img = Image.open(os.path.join(album_art_dir, picture))
        Himage.paste(album_art_img, (0, 0))
        epd.display(epd.getbuffer(Himage))
        time.sleep(5)

    while True:
        for picture in album_art:
            album_art_img = Image.open(os.path.join(album_art_dir, picture))
            Himage.paste(album_art_img, (0, 0))
            epd.display(epd.getbuffer(Himage))
            time.sleep(SHOWTIME)

except IOError as e:
    logging.info(e)
    epd.Clear()
    
except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd.Clear()
    epd4in2.epdconfig.module_exit()
    exit()
