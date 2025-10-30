import cv2
import numpy as np
import os
import easyocr
from dotenv import load_dotenv

load_dotenv()
TEST_IMG_PATH = os.getenv("TEST_IMG_PATH")

use_cuda = True 
reader = easyocr.Reader(['en'], gpu=use_cuda)

# Зчитування зображення
image = cv2.imread(TEST_IMG_PATH)
if image is None:
    raise FileNotFoundError(f"Image not found: {TEST_IMG_PATH}")

# Детекція тексту
results = reader.readtext(image)

# Створимо список боксів
boxes = [res[0] for res in results]  # кожен res[0] = [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]

# Малюємо бокси
for box in boxes:
    box = np.array(box).astype(np.int32)
    cv2.polylines(image, [box], isClosed=True, color=(0, 255, 0), thickness=2)

# Збереження результатів
os.makedirs("output", exist_ok=True)
cv2.imwrite("output/detected.jpg", image)
np.savetxt("output/boxes.txt", np.array(boxes).reshape(len(boxes), -1), fmt="%d")

print(f"Boxes found -> {len(boxes)}")
