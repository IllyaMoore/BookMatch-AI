import cv2
import numpy as np
import os
import easyocr
from dotenv import load_dotenv, dotenv_values

load_dotenv()

IMAGE_PATH = os.getenv("IMAGE_PATH")
BOXES_PATH = os.getenv("BOXES_PATH")
crops_dir = "output/crops"

os.makedirs(crops_dir, exist_ok=True)


boxes = np.loadtxt(BOXES_PATH).reshape(-1, 4, 2).astype(np.float32)
image = cv2.imread(IMAGE_PATH)

def crop_and_rectify(img, box):
    w = int(np.linalg.norm(box[0] - box[1]))
    h = int(np.linalg.norm(box[0] - box[3]))
    dst_pts = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype="float32")
    M = cv2.getPerspectiveTransform(box, dst_pts)
    warp = cv2.warpPerspective(img, M, (w, h))
    return warp

crops = []
for i, box in enumerate(boxes):
    crop = crop_and_rectify(image, box)
    crop_path = os.path.join(crops_dir, f"crop_{i:03d}.jpg")
    cv2.imwrite(crop_path, crop)
    crops.append(crop_path)

print(f"Boxes : {len(crops)} in {crops_dir}/")

reader = easyocr.Reader(['en', 'uk'])
results = []

for crop_path in crops:
    result = reader.readtext(crop_path, detail=0)
    text = " ".join(result).strip()
    if text:
        results.append(text)
    else:
        results.append("[EMPTY]")

with open("output/recognized.txt", "w", encoding="utf-8") as f:
    for i, text in enumerate(results):
        f.write(f"{i:03d}: {text}\n")

