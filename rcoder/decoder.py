import msgpack
import zlib
import base64
import cv2
import qreader

"""
rcoder.decoder(img):
- 输入：img，ros2通常支持的BGR8格式的图像
- 对图片进行等比例缩放，使最长边为1280
- 从图像中识别qrcode
- 从qrcode中提取base64字符串
- 使用base64转换为二进制数据
- 用zlib解压缩二进制数据
- 使用msgpack解压缩数据
- 返回python基本类型
"""

class Decoder:
    def __init__(self,compress=True):
        self.qreader = qreader.QReader()
        self.compress = compress

    def decode(self,img):
        try:
            qr_data = self.qreader.detect_and_decode(img)
            if qr_data is None or len(qr_data) == 0:
                return None
            base64_data = qr_data[0]
            if base64_data is None:
                return None
            compressed_data = base64.b64decode(base64_data)
            if self.compress:
                packed_data = zlib.decompress(compressed_data)
            else:
                packed_data = compressed_data
            data = msgpack.unpackb(packed_data)
            return data
        except Exception:
            return None
