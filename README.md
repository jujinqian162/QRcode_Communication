# rcoder 库使用说明

rcoder 是一个用于通过二维码进行数据编码和解码的 Python 库，适合在机器人通信、离线数据分发或跨设备配置同步等场景中传输结构化数据。库内部采用 msgpack 序列化、可选的 zlib 压缩以及 base64 编码，让二维码能够在容量与兼容性之间取得平衡。

## 项目概览

- **核心能力**：在二维码与 Python 基本数据类型（`dict`、`list`、`str`、`int` 等）之间完成高效、可靠的双向转换。
- **实现流程**：编码时按 msgpack → （可选）zlib → base64 → 二维码图像的顺序处理；解码则按相反流程还原数据，并借助 `qreader` 识别二维码内容。
- **仓库结构**：

  ```text
  QRcode_Communication/
  ├── rcoder/             # 核心库，提供 Encoder 与 Decoder 类
  ├── jujinqian/          # 示例脚本与演示二维码
  ├── WORKRECORD.md       # 历史工作记录
  └── README.md           # 当前文档
  ```

## 环境准备与安装

1. 准备 Python 3.8 及以上版本，建议启用虚拟环境：

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows 使用 .venv\Scripts\activate
   python -m pip install --upgrade pip
   ```

2. 安装依赖库（`zlib`、`base64` 属于标准库，无需额外安装）：

   ```bash
   python -m pip install msgpack opencv-python numpy qrcode qreader
   ```

3. 若需在本地项目中以包形式引用，可执行可选的可编辑安装：

   ```bash
   python -m pip install -e .
   ```

> 若你的系统中 OpenCV 依赖缺失，请参考 [`opencv-python` 官方说明](https://pypi.org/project/opencv-python/) 先安装必要的系统包。

## 快速开始

### 编码：生成带数据的二维码

```python
from rcoder import Encoder
import cv2

encoder = Encoder(
    compress=True,
    compress_level=9,
    qr_version=None,
)

payload = {
    "name": "rcoder",
    "version": "1.0.0",
    "features": ["msgpack", "zlib", "base64", "qrcode"],
    "is_active": True,
}

qr_image = encoder.encode(payload)
cv2.imwrite("encoded_qr.png", qr_image)
```

> **提示**：需要更高的容错率时，可将 `error_correction` 参数调为 `qrcode.constants.ERROR_CORRECT_M/Q/H`；对应的二维码容量会下降。

### 解码：从二维码中还原数据

```python
from rcoder import Decoder
import cv2

decoder = Decoder(compress=True)  # compress 参数需与编码端保持一致
qr_image = cv2.imread("encoded_qr.png")

payload = decoder.decode(qr_image)
if payload is None:
    raise ValueError("二维码识别失败或内容无效")

print("解析出的数据：", payload)
```

### API 速查

| 类/方法 | 作用 | 关键参数 |
| --- | --- | --- |
| `Encoder` | 将 Python 数据编码为二维码图像 | `compress`（是否压缩）、`compress_level`、`qr_version`、`error_correction` |
| `Encoder.encode(data)` | 返回 BGR8 `numpy.ndarray` 图像 | `data`：任意 msgpack 可序列化的数据 |
| `Decoder` | 解码二维码图像 | `compress`：是否按压缩流程解码 |
| `Decoder.decode(image)` | 解析 BGR8 图像并返回原始数据或 `None` | `image`：包含二维码的 `numpy.ndarray` |

## 工作流程解析

### 编码流程
1. 使用 msgpack 将数据序列化为二进制。
2. （可选）使用 zlib 压缩序列化结果。
3. 将压缩结果转换为 base64 字符串。
4. 将 base64 字符串写入二维码并生成图像。
5. 将二维码转换为 BGR8 格式返回。

### 解码流程
1. 识别二维码并提取 base64 字符串。
2. 将 base64 字符串还原为二进制数据。
3. （可选）使用 zlib 解压缩。
4. 使用 msgpack 反序列化得到原始数据。
5. 任一步失败则返回 `None`，方便上层逻辑处理异常。

## 示例与调试建议

- 结合 README 中的 `Encoder`/`Decoder` 用法调整后，可运行 `jujinqian/main.py`、`jujinqian/readqr.py` 体验完整流程。
- 二维码过于复杂导致识别失败时，可减少单次传输的数据量，或开启压缩、降低纠错等级。
- 在低光或噪声较大的场景下，提前裁剪、放大或进行灰度化处理能够提高 `qreader` 的识别率。

## 常见问题

1. **解码返回 `None`**：通常是二维码图像质量不佳、二维码被遮挡或编码/解码的 `compress` 参数不匹配所致。
2. **二维码容量不足**：可以开启压缩、降低纠错等级或拆分数据为多张二维码。
3. **OpenCV 读取失败**：检查图像路径是否正确，必要时使用绝对路径。

## 许可证

项目遵循 [MIT License](LICENSE)。

欢迎在 Issue 中反馈使用体验或提交改进建议。
