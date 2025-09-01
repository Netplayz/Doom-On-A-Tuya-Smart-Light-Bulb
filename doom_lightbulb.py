import os
import time
import statistics
from dotenv import load_dotenv
from mss import mss
from PIL import Image
import tinytuya

# Load bulb credentials from .env
load_dotenv()
DEVICE_ID = os.getenv("DEVICE_ID")
DEVICE_IP = os.getenv("DEVICE_IP")
LOCAL_KEY = os.getenv("LOCAL_KEY")
DEVICE_VERSION = float(os.getenv("DEVICE_VERSION", "3.3"))

# Connect to Sylvania (Tuya WiFi) bulb
light = tinytuya.BulbDevice(DEVICE_ID, DEVICE_IP, LOCAL_KEY)
light.set_version(DEVICE_VERSION)

def avg_color(bbox=None):
    """Capture average color of screen (or region)."""
    with mss() as sct:
        monitor = bbox or sct.monitors[1]  # full screen by default
        img = Image.frombytes("RGB",
                              (monitor["width"], monitor["height"]),
                              sct.grab(monitor).rgb)
        pixels = img.getdata()
        r = statistics.mean(p[0] for p in pixels)
        g = statistics.mean(p[1] for p in pixels)
        b = statistics.mean(p[2] for p in pixels)
        return int(r), int(g), int(b)

def send_color(r, g, b):
    """Send RGB color to bulb."""
    light.set_colour(r, g, b)

print("💡 Syncing Doom screen colors to your Sylvania bulb... (Ctrl+C to stop)")
try:
    while True:
        r, g, b = avg_color()
        send_color(r, g, b)
        time.sleep(0.1)  # update ~10 times per second
except KeyboardInterrupt:
    light.turn_off()
    print("Stopped.")
