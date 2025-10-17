from typing import Any
from qreader import QReader
import msgpack
import zlib
import hashlib
import base64
import qrcode
import cv2
import numpy as np

SEP = '|'  # 分隔符： "<hash>|<b64payload>"
def _calc_hash(b64: str) -> str:
    return hashlib.sha256(b64.encode('utf-8')).hexdigest()

def _pack_and_encode(data: Any) -> str:
    """msgpack -> zlib.compress -> base64(str)"""
    packed = msgpack.packb(data, use_bin_type=True)  # bytes
    if not packed:
        raise RuntimeError("packed error") 
    compressed = zlib.compress(packed)
    b64 = base64.b64encode(compressed).decode('ascii')
    return b64

def _decode_and_unpack(b64: str) -> Any:
    """base64(str) -> zlib.decompress -> msgpack.unpackb"""
    compressed = base64.b64decode(b64)
    packed = zlib.decompress(compressed)
    data = msgpack.unpackb(packed, raw=False)
    return data

def _make_qr_image_from_text(text: str, box_size: int = 6, border: int = 4) -> 'PIL.Image.Image':
    """用 qrcode 生成 PIL.Image（RGB）"""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')  # PIL.Image
    return img

def _pil_to_bgr8_numpy(pil_img) -> np.ndarray:
    """PIL RGB -> numpy BGR8 (H, W, 3), dtype=uint8"""
    arr = np.asarray(pil_img)  # RGB
    # convert RGB -> BGR
    bgr = arr[..., ::-1].copy()
    return bgr

def _bgr8_numpy_to_gray_for_decoder(img_bgr: np.ndarray) -> np.ndarray:
    """OpenCV QR detector accepts BGR or gray; keep BGR as-is"""
    return img_bgr  # no-op, kept for clarity

# === 对外接口 ===

def encoder(data: Any, box_size: int = 6, border: int = 4) -> np.ndarray:
    """
    输入：任意 python 基本类型（能被 msgpack 序列化）
    输出：QR 图像（numpy.ndarray，BGR8，dtype=uint8）
    步骤：msgpack -> zlib -> base64 -> hash 拼接 -> 生成 QR -> 转 BGR8 numpy
    """
    # encode
    b64 = _pack_and_encode(data)  # str
    h = _calc_hash(b64)
    combined = f"{h}{SEP}{b64}"

    # generate QR (PIL) then convert to BGR numpy
    pil_img = _make_qr_image_from_text(combined, box_size=box_size, border=border)
    bgr = _pil_to_bgr8_numpy(pil_img)
    return bgr

def decoder(img_bgr8: np.ndarray) -> Any:
    """
    输入：BGR8 numpy 图像 (dtype=uint8)
    输出：原始 python 对象（经过 msgpack 解码）
    步骤：从图像提取 QR 字符串 -> 拆分 hash 和 payload -> 计算并比对 hash -> base64->zlib->msgpack -> 返回
    抛错：
      - ValueError("no_qr_found") 如果没有找到 QR
      - ValueError("invalid_payload_format") 如果分隔不正确
      - ValueError("hash_mismatch") 如果校验失败
    """

    data_str = None
    for _ in range(0, 50):
        data_str = QReader().detect_and_decode(img_bgr8)[0]
    if not data_str:
        # detectAndDecode 返回空串表示没有解出或没有二维码
        raise ValueError("no_qr_found")

    # parse "<hash>|<b64>"
    if SEP not in data_str:
        raise ValueError("invalid_payload_format")

    hash_str, b64 = data_str.split(SEP, 1)

    # verify
    expected = _calc_hash(b64) 
    if expected != hash_str:
        raise ValueError("hash_mismatch")

    # decode
    data = _decode_and_unpack(b64)
    return data

# === End of rcoder.py ===
