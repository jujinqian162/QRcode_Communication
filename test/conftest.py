import pytest
import cv2
import os

@pytest.fixture
def data_dir():
    return os.path.join(os.path.dirname(__file__), "data")

@pytest.fixture
def load_qr_image(data_dir):
    def _loader(filename):
        path = os.path.join(data_dir, filename)
        img = cv2.imread(path)
        if img is None:
            raise FileNotFoundError(f"Connot load {path}")
        return img

    return _loader

