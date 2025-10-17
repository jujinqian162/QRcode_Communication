import msgpack
import zlib
import base64
import qrcode
import cv2
import numpy as np

"""
rcoder.encoder(data):
- 输入：data，python基本类型
- 将data用msgpack转换为二进制数据
- 用zlib压缩二进制数据
- 使用base64转换为字符串
- 将base64字符串写入qrcode
- 对qrcode转换为ros2通常支持的BGR8格式
- 返回图像
"""

class Encoder:
    def __init__(self,compress=True,compress_level=9,qr_version=None,error_correction=qrcode.constants.ERROR_CORRECT_L):
        self.compress = compress
        self.compress_level = compress_level
        self.qr_version = qr_version
        self.error_correction = error_correction
    
    def encode(self,data):
        packed_data = msgpack.packb(data)
        if self.compress:
            compressed_data = zlib.compress(packed_data, self.compress_level)
        else:
            compressed_data = packed_data
        base64_data = base64.b64encode(compressed_data).decode('utf-8')
        qr = qrcode.QRCode(
            version=self.qr_version,
            error_correction=self.error_correction,
            box_size=10,
            border=4,
        )
        qr.add_data(base64_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_array = np.array(img.convert("RGB"))
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        return img_bgr
