import mss.models
import kp
import mss
import utils
import pytesseract
from PIL import Image
import re

loc_stamina = kp.locateOnScreen('soc/img/stamina.png')
sct = mss.mss()
monitor = sct.monitors[1]
left = loc_stamina.left+loc_stamina.width
region = {'left': monitor['left']+left/2, 'top': monitor['top'], 'width': monitor['left']+monitor['width']-left/2, 'height': monitor['height']}
loc_add = kp.locateOnScreen('soc/img/add.png', region)
region = {
    'left': monitor['left'] + left/2,
    'top': monitor['top'] + loc_stamina.top/2,
    'width': (loc_add.left - loc_stamina.left - loc_stamina.width) / 2,
    'height': loc_stamina.height / 2
}
ss = sct.grab(region)
img = Image.frombytes("RGB", ss.size, ss.bgra, "raw", "BGRX")
ocr_result = pytesseract.image_to_string(img)
match = re.match(r'(\d+)/(\d+)', ocr_result)
if match:
    print(f'Current stamina: {match.group(1)}')
    print(f'Max stamina: {match.group(2)}')
