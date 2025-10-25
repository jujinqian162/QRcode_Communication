# rcoder 库使用说明

rcoder 是一个用于通过二维码进行数据编码和解码的 Python 库，适用于需要在图像、屏幕或打印载体之间传递结构化数据的场景。库内置基于 msgpack 的序列化方案，并辅以 zlib 压缩（可选）和 base64 编码，使二维码能够携带更多信息的同时保持良好的兼容性。

## 项目简介

- **核心能力**：在二维码与 Python 基本数据类型（`dict`、`list`、`str`、`int` 等）之间完成高效、可靠的双向转换。
- **实现方式**：编码阶段依次执行 msgpack 序列化 → 可选的 zlib 压缩 → base64 编码；解码阶段反向执行上述流程，并借助 `qreader` 自动识别二维码内容。
- **适用场景**：机器人通信、线下数据分发、跨设备配置同步等需要在无网络或弱网络环境中交换数据的场景。

## 仓库结构

```
QRcode_Communication/
├── rcoder/             # 核心库，提供 Encoder 与 Decoder 类
├── jujinqian/          # 示例脚本与演示二维码
├── WORKRECORD.md       # 历史工作记录
└── README.md           # 当前文档
```

示例脚本 `jujinqian/main.py` 与 `jujinqian/readqr.py` 展示了如何在应用层集成 rcoder 库，可直接运行体验端到端流程。

## 功能特点

- **高效序列化**：使用 msgpack 在保持数据结构的同时尽量缩减体积。
- **可选压缩**：通过 zlib 压缩进一步减小二维码中嵌入的数据量，参数可自定义。
- **跨平台兼容**：编码结果为 OpenCV 常用的 BGR8 图像，可直接在 ROS2、机器人或计算机视觉流程中使用。
- **鲁棒解码**：借助 `qreader` 自动识别二维码，遇到无法识别时返回 `None` 以便上层处理。
- **易于集成**：仅依赖少量常见第三方库，提供简单直观的 API。

## 环境准备

- Python 3.8 及以上版本（建议使用虚拟环境或 [uv](https://docs.astral.sh/uv/) 管理依赖）。
- 已安装 OpenCV 所需的系统依赖（大多数环境中 pip 安装 `opencv-python` 即可）。

### 使用 pip 创建环境

```bash
python -m venv .venv
source .venv/bin/activate  # Windows 使用 .venv\Scripts\activate
pip install --upgrade pip
```

### 使用 uv 运行示例

如果希望直接运行示例脚本，可安装 uv：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

随后执行：

```bash
uv run --script jujinqian/main.py
uv run --script jujinqian/readqr.py
```

## 安装依赖

使用 pip 安装所需依赖：

```bash
pip install msgpack opencv-python numpy qrcode qreader
```

上述命令会同时安装标准库中已包含的 `zlib`、`base64` 等所需模块。

## 快速开始

### 编码：生成带数据的二维码

使用 `Encoder` 类可将 Python 基本数据类型编码为二维码图像（OpenCV/ROS2 常用的 BGR8 格式）：

```python
from rcoder import Encoder
import qrcode
import cv2

encoder = Encoder(
    compress=True,                          # 是否启用 zlib 压缩
    compress_level=9,                       # 压缩级别，1-9，数值越大压缩率越高
    qr_version=None,                        # 二维码版本，None 表示自动选择
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # 纠错级别
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

> **提示**：若希望让二维码容错率更高，可将 `error_correction` 设置为 `qrcode.constants.ERROR_CORRECT_M/Q/H`，但二维码容量会随之下降。

### 解码：从二维码中还原数据

`Decoder` 类负责从 BGR8 格式的图像中识别并解析二维码：

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

- `Encoder.encode(data)`：接收 Python 基本类型数据，返回 BGR8 `numpy.ndarray` 图像。
- `Decoder.decode(image)`：接收 BGR8 图像，成功时返回原始数据，失败时返回 `None`。

## 工作流程

### 编码流程
1. 使用 msgpack 将 Python 数据序列化为二进制。
2. （可选）使用 zlib 对二进制数据压缩。
3. 将压缩结果转换为 base64 字符串。
4. 将 base64 字符串写入二维码并生成图像。
5. 将二维码转换为 BGR8 格式供 OpenCV/ROS2 使用。

### 解码流程
1. 对输入图像进行二维码识别并提取 base64 字符串。
2. 将 base64 字符串解码为二进制数据。
3. （可选）对二进制数据进行 zlib 解压缩。
4. 使用 msgpack 反序列化得到原始 Python 数据。
5. 返回解析后的数据；若任一步骤失败，则返回 `None`。

## 示例与调试建议

- 运行 `jujinqian/main.py` 可以生成示例二维码图像 `qr.png`，再使用 `jujinqian/readqr.py` 读取并验证解码结果。
- 若二维码过于复杂导致识别失败，可尝试降低单次传输的数据量，或将 `compress=True`、提高压缩等级。
- 在低光或摄像头噪声较大的场景下，建议提前对图像做灰度化、裁剪等预处理，以提升 `qreader` 的识别率。

## 常见问题

1. **解码返回 `None`**：通常是二维码图像质量不佳、二维码被遮挡或 `compress` 参数不一致造成的，请逐一排查。
2. **二维码容量不足**：可以开启压缩、降低纠错等级或拆分数据为多张二维码。
3. **OpenCV 读取失败**：确保图像路径正确，或使用绝对路径。

## 许可证

项目遵循 [MIT License](LICENSE)。

如需进一步扩展或集成，欢迎在 issue 中反馈需求。
