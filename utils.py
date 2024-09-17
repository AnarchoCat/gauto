import pyautogui, time
import platform
import kp

def isMac():
    return platform.system().startswith('Darwin')

# Wait single image
def locate(img, time_limit=60, gray_scale=True, confidence=0.9):
    loop_limit = time_limit * 5
    for _ in range(loop_limit):
        try:
            # pos = pyautogui.locateCenterOnScreen(img, grayscale=gray_scale, confidence=confidence)
            pos = kp.locateCenterOnScreen(img)
            if pos:
                loc = pos
        except pyautogui.ImageNotFoundException:
            pass
        if 'loc' in locals():
            return loc
        time.sleep(0.2)

# Wait until any one of images appears
def wait_any_img(*imgs, time_limit=60, gray_scale=True, confidence=0.9):
    loop_limit = time_limit * 5
    for _ in range(loop_limit):
        for img in imgs:
            try:
                # loc = pyautogui.locateCenterOnScreen(img, grayscale=gray_scale, confidence=confidence)
                loc = kp.locateCenterOnScreen(img)
                if loc:
                    img_loc = loc
                    break
            except pyautogui.ImageNotFoundException:
                pass
        if 'img_loc' in locals():
            return img_loc
        time.sleep(0.2)

# Wait until all images appears
def wait_all_imgs(*imgs, time_limit=60, gray_scale=True, confidence=0.9):
    loop_limit = time_limit * 5
    locs = [None for _ in range(len(imgs))]
    for _ in range(loop_limit):
        for i, img in enumerate(imgs):
            if locs[i]:
                continue
            try:
                # loc = pyautogui.locateCenterOnScreen(img, grayscale=gray_scale, confidence=confidence)
                loc = kp.locateCenterOnScreen(img)
                if loc:
                    locs[i] = loc
            except pyautogui.ImageNotFoundException:
                pass
        if all(locs):
            return locs
        time.sleep(0.2)

# Wait until image disappears
def wait_until_disappear(*imgs, time_limit=60, gray_scale=True, confidence=0.9):
    loop_limit = time_limit * 5  # 待機時間（int）
    get_img = [True for _ in range(len(imgs))]
    for _ in range(loop_limit):
        for i, img in enumerate(imgs):
            try:
                # if pyautogui.locateOnScreen(img, grayscale=gray_scale, confidence=confidence) is None:
                loc = kp.locateCenterOnScreen(img)
                if loc is None:
                    get_img[i] = False
            except pyautogui.ImageNotFoundException:
                get_img[i] = False
        if not any(get_img):
            return True
        time.sleep(0.2)
    return False

# Move to location returned by locateCenterOnScreen
def moveTo(pos, duration=0.0, time_limit=60):
    if isinstance(pos, str):
        pos = locate(pos, time_limit=time_limit)
    x, y = pos
    if isMac():
        x = x // 2
        y = y // 2
    pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeOutQuad)

# Move to pos and click
def click(pos, duration=0.0, time_limit=60):
    if isinstance(pos, str):
        pos = locate(pos, time_limit=time_limit)
    if pos:
        x, y = pos
        if isMac():
            x = x // 2
            y = y // 2
        pyautogui.click(x, y, duration=duration, tween=pyautogui.easeOutQuad)

def swipeLeft():
    pyautogui.drag(-100, 0, 0.2, button='left')
    time.sleep(2)

def swipeRight():
    pyautogui.drag(100, 0, 0.2, button='left')
    time.sleep(2)