# rcoder 库使用说明

rcoder 是一个用于通过二维码进行数据编码和解码的 Python 库，支持将 Python 基本数据类型通过 msgpack 序列化、zlib 压缩（可选）和 base64 编码后嵌入到二维码中，也可从二维码中反向解析出原始数据。

## 安装依赖
- uv 安装依赖
下载依赖：
```bash
uv sync
```
运行测试：
```bash
uv run pytest
```
- pip 安装依赖
```bash
pip install -r requirements.txt
```

## 基本使用

### 1. 数据编码（生成带数据的二维码）

使用 `Encoder` 类可将 Python 基本数据类型（如字典、列表、字符串等）编码为二维码图像（ROS2 支持的 BGR8 格式）。

```python
from rcoder import Encoder
import cv2

# 初始化编码器（默认启用压缩）
encoder = Encoder()

# 准备要编码的数据（支持Python基本类型）
data = {
    "name": "rcoder",
    "version": "1.0.0",
    "features": ["msgpack", "zlib", "base64", "qrcode"],
    "is_active": True
}

# 编码数据生成二维码图像（BGR8格式）
qr_image = encoder.encode(data)

# 保存二维码图像（可选）
cv2.imwrite("encoded_qr.png", qr_image)
```

#### 编码器参数说明

- `compress`：是否启用 zlib 压缩（默认 `True`）
- `compress_level`：压缩级别（1-9，默认 9，级别越高压缩率越高）
- `qr_version`：二维码版本（1-40， None 则自动选择合适版本，默认 None）
- `error_correction`：纠错级别（默认 `qrcode.constants.ERROR_CORRECT_L`，可选 L/M/Q/H）


### 2. 数据解码（从二维码中解析数据）

使用 `Decoder` 类可从二维码图像（BGR8 格式）中解析出原始 Python 数据。

```python
from rcoder import Decoder
import cv2

# 初始化解码器（默认启用解压缩，需与编码时保持一致）
decoder = Decoder()

# 读取二维码图像（BGR8格式）
qr_image = cv2.imread("encoded_qr.png")

# 解码获取原始数据
data = decoder.decode(qr_image)

print("解析出的数据：", data)
```

#### 解码器参数说明

- `compress`：是否启用 zlib 解压缩（默认 `True`，需与编码时的 `compress` 参数保持一致）


## 工作流程说明

### 编码流程
1. 使用 msgpack 将 Python 数据序列化为二进制数据
2. （可选）用 zlib 压缩二进制数据
3. 将二进制数据转换为 base64 字符串
4. 生成包含 base64 字符串的二维码
5. 转换为 BGR8 格式图像返回

### 解码流程
1. 从输入图像中识别二维码并提取 base64 字符串
2. 将 base64 字符串解码为二进制数据
3. （可选）用 zlib 解压缩二进制数据
4. 使用 msgpack 反序列化得到原始 Python 数据
5. 返回解析后的 Python 数据


## 注意事项
1. 编码和解码时的 `compress` 参数必须保持一致，否则会导致解析失败
2. 数据量过大可能导致二维码过于复杂而无法识别，建议控制数据大小
3. 输入到解码器的图像应为 BGR8 格式（ROS2 常用图像格式），与 OpenCV 默认读取格式一致
4. 二维码识别受图像质量影响，建议保证图像清晰、二维码完整无遮挡
