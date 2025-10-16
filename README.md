# QRcode_Communication
----

## 流程设计
```mermaid
graph 
    A[Subscriber 节点] -->|原始数据| A1{数据校验/过滤}
    A1 -->|有效数据| B[内存缓冲区]
    B -->|定时/触发| C[Packager 节点]
    C -->|编码+图像生成| C1{二维码压缩/分片}
    C1 -->|单帧二维码| D[QR Publisher 节点]
    
    subgraph 发送端
        A; A1; B; C; C1; D
    end
    
```


```mermaid
graph 
    E[QR Subscriber 节点]
    E --> F[Decoder 节点]
    F -->|解码数据| F1{校验/纠错}
    F1 -->|有效数据| G[内存缓冲区]
    G -->|定时/触发| H[Data Publisher 节点]
    subgraph 接收端
        E; F; F1; G; H
    end
```

## 流程介绍
rcoder.encoder(data):
- 输入：data，python基本类型
- 将data用msgpack转换为二进制数据
- 用zlib压缩二进制数据
- 使用base64转换为字符串
- 使用python内置的hash函数计算哈希值的绝对值，并与数据进行拼接
- 将拼接后的字符串写入qrcode
- 对qrcode转换为ros2通常支持的BGR8格式
- 返回图像

rcoder.decoder(img):
- 输入：img，ros2通常支持的BGR8格式的图像
- 从图像中提取qrcode
- 对qrcode进行解码
- 从解码后的字符串中提取哈希值和数据
- 用python内置的hash函数计算哈希值的绝对值，并与提取的哈希值进行比较
- 用base64转换为二进制数据
- 用zlib解压二进制数据
- 将解压后的二进制数据用msgpack转换为python基本类型
- 返回数据


