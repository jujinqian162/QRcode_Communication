# /// script
# dependencies = ["qrcode[pil]>=8.2", "numpy>=2.2.6", "msgpack>=1.1.2", "opencv-python>=4.12.0.88"]
# python = 3.11
# ///

import cv2 
from rcoder import decoder

qrcode_img = cv2.imread("qr.png")

if qrcode_img is None:
    raise RuntimeError("qrcode img not opened")

data = decoder(qrcode_img)

print(data)
