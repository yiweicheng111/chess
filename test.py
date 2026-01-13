import cv2
import numpy as np
import pyautogui

# --- Take screenshot ---
screenshot = pyautogui.screenshot()
img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# --- Load pawn template ---
# Make sure you have a small image of a pawn: "pawn.png"
template = cv2.imread("pawn.png", cv2.IMREAD_UNCHANGED)
template = cv2.resize(template,(40,40))
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# Convert screenshot to grayscale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# --- Template matching ---
res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
threshold = 0.5  # adjust 0.7-0.95 depending on accuracy
loc = np.where(res >= threshold)

# --- Draw rectangles around found pawns ---
w, h = template_gray.shape[::-1]  # width, height
for pt in zip(*loc[::-1]):
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

# --- Show result ---
cv2.imshow("Pawn Detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
