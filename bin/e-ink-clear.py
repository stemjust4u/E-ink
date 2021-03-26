#!/usr/bin/python3
# Clear screen script

import sys
import os
import socket

libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')

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
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    epd.Clear()
    
except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd.Clear()
    epd4in2.epdconfig.module_exit()
    exit()
