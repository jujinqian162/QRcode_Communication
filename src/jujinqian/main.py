# /// script
# dependencies = ["qrcode[pil]>=8.2", "numpy>=2.2.6", "msgpack>=1.1.2", "opencv-python>=4.12.0.88", "qreader>=3.16"]
# python = 3.11
# ///
import cv2
from rcoder import encoder, decoder
   

payload = {"hello": "world", "num": 123, "list": [1,2,3]}
img = encoder(payload)          # 得到 BGR8 numpy 图像
print(type(img), img.dtype, img.shape)

cv2.imwrite("qr.png", img)
# 显示（仅本地调试）

cv2.imshow("qr", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 解码
decoded = decoder(img)
print("decoded:", decoded)
