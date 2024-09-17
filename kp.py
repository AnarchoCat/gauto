import cv2
import numpy as np
import mss
import pyautogui
import utils
import collections

Box = collections.namedtuple('Box', 'left top width height')
Point = collections.namedtuple('Point', 'x y')

def locateOnScreen(img, region=None):
    target = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    sift = cv2.SIFT_create()
    keypoints1, descriptors1 = sift.detectAndCompute(target, None)
    sct = mss.mss()
    monitor = sct.monitors[1] if region is None else region
    screenshot = np.array(sct.grab(monitor))
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    keypoints2, descriptors2 = sift.detectAndCompute(screenshot_gray, None)

    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)
    matches = sorted(matches, key=lambda x: x.distance)
    if matches:
        x_offsets, y_offsets = [], []
        for match in matches[:10]:
            key_point_1 = keypoints1[match.queryIdx]
            key_point_2 = keypoints2[match.trainIdx]
            x_offsets.append(key_point_1.pt[0] - key_point_2.pt[0])
            y_offsets.append(key_point_1.pt[1] - key_point_2.pt[1])
        tolerance = 256
        is_true_match = np.std(x_offsets) < tolerance and np.std(y_offsets) < tolerance
        if not is_true_match:
            return None
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matches_mask = mask.ravel().tolist()

        h, w = target.shape
        pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        topLeft = pyautogui.Point(dst[0][0][0], dst[0][0][1])
        bottomLeft = pyautogui.Point(dst[1][0][0], dst[1][0][1])
        bottomRight = pyautogui.Point(dst[2][0][0], dst[2][0][1])
        topRight = pyautogui.Point(dst[3][0][0], dst[3][0][1])
        return Box(left=monitor["left"]*2+topLeft.x, top=monitor["top"]*2+topLeft.y, width=bottomRight.x-topLeft.x, height=bottomRight.y-topLeft.y)

def center(box):
    return Point(x=box.left+box.width/2, y=box.top+box.height/2)

def locateCenterOnScreen(img):
    box = locateOnScreen(img)
    if box:
        return center(box)

if __name__ == '__main__':
    pos = locateCenterOnScreen('soc/start-voyage.png')
    print(pos)
    utils.moveTo(pos)
