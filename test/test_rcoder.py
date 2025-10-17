import pytest
import os
import cv2
from rcoder import Decoder
from rcoder import Encoder

def test_encode_decode_roundtrip(data_dir):
    """编码后解码应该得到原始数据"""
    data = {"msg": "hello world", "id": 42}
    img = Encoder().encode(data)
    cv2.imwrite(os.path.join(data_dir, "qr.png"), img)
    decoded = Decoder().decode(img)

    assert decoded == data


def test_decode_valid_qr(load_qr_image):
    """测试从 data 目录的二维码图片解码"""
    test_cases = [
        ("qr.png", {"msg": "hello world", "id": 42}),
    ]

    for filename, expected in test_cases:
        img = load_qr_image(filename)
        decoded = Decoder().decode(img)
        assert decoded == expected
