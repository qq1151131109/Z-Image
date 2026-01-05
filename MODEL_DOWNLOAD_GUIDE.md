# 模型下载指南

Z-Image-Turbo模型约13GB，有多种下载方式。

## 方法1：ModelScope（推荐，国内速度快）

### 选项A：使用Python脚本（自动）

```bash
python download_modelscope.py
```

### 选项B：使用Shell脚本

```bash
./download_from_modelscope.sh
```

### 选项C：使用git-lfs（手动）

```bash
cd ckpts/
git lfs install
git clone https://www.modelscope.cn/Tongyi-MAI/Z-Image-Turbo.git
cd ..
```

### 选项D：浏览器手动下载

1. 访问: https://modelscope.cn/models/Tongyi-MAI/Z-Image-Turbo
2. 点击「文件」标签
3. 点击右上角「下载模型」按钮
4. 下载完成后解压到 `ckpts/Z-Image-Turbo/`

## 方法2：HuggingFace（国外速度快）

### 选项A：使用huggingface-cli

```bash
pip install huggingface_hub

huggingface-cli download Tongyi-MAI/Z-Image-Turbo \
    --local-dir ckpts/Z-Image-Turbo \
    --local-dir-use-symlinks False
```

### 选项B：使用git-lfs

```bash
cd ckpts/
git lfs install
git clone https://huggingface.co/Tongyi-MAI/Z-Image-Turbo
cd ..
```

### 选项C：让脚本自动下载

脚本会自动从HuggingFace下载（但可能较慢）：

```bash
python test_20_avatars.py
# 首次运行会自动下载模型
```

## 方法3：使用代理/镜像

### HuggingFace镜像站

如果HuggingFace访问慢，可以使用镜像：

```bash
# 设置环境变量
export HF_ENDPOINT=https://hf-mirror.com

# 然后运行下载
python test_20_avatars.py
```

### ModelScope镜像（阿里云）

```bash
# 使用阿里云镜像
pip install modelscope -i https://mirrors.aliyun.com/pypi/simple/

python download_modelscope.py
```

## 方法4：从本地复制

如果你在其他机器上已有模型：

```bash
# 从其他机器复制
scp -r user@other-machine:/path/to/Z-Image-Turbo ckpts/

# 或使用rsync
rsync -avz user@other-machine:/path/to/Z-Image-Turbo/ ckpts/Z-Image-Turbo/
```

## 验证下载

下载完成后，验证文件完整性：

```bash
# 检查目录大小（应该约13GB）
du -sh ckpts/Z-Image-Turbo/

# 检查主要文件
ls -lh ckpts/Z-Image-Turbo/transformer/*.safetensors
ls -lh ckpts/Z-Image-Turbo/text_encoder/*.safetensors
ls -lh ckpts/Z-Image-Turbo/vae/*.safetensors

# 应该看到类似：
# transformer/: 3个文件，每个约4-5GB
# text_encoder/: 3个文件，总计约1-2GB
# vae/: 1个文件，约160MB
```

预期的文件结构：

```
ckpts/Z-Image-Turbo/
├── model_index.json
├── README.md
├── scheduler/
│   └── scheduler_config.json
├── text_encoder/
│   ├── config.json
│   ├── model-00001-of-00003.safetensors  (~1GB)
│   ├── model-00002-of-00003.safetensors  (~1GB)
│   ├── model-00003-of-00003.safetensors  (~96MB)
│   └── model.safetensors.index.json
├── tokenizer/
│   ├── tokenizer.json
│   └── tokenizer_config.json
├── transformer/
│   ├── config.json
│   ├── diffusion_pytorch_model-00001-of-00003.safetensors  (~5GB)
│   ├── diffusion_pytorch_model-00002-of-00003.safetensors  (~5GB)
│   ├── diffusion_pytorch_model-00003-of-00003.safetensors  (~2GB)
│   └── diffusion_pytorch_model.safetensors.index.json
└── vae/
    ├── config.json
    └── diffusion_pytorch_model.safetensors  (~160MB)
```

## 下载完成后

运行测试：

```bash
# 测试生成20张图片
python test_20_avatars.py

# 如果成功，运行完整生成
./run_parallel_generation.sh  # 6GPU并行生成3000张
```

## 常见问题

### Q: 下载中断怎么办？

A: 所有方法都支持断点续传，重新运行下载命令即可。

### Q: 下载速度很慢？

A:
1. 国内用户使用ModelScope
2. 国外用户使用HuggingFace
3. 使用git-lfs可能比Python SDK快
4. 尝试使用代理或镜像站

### Q: 磁盘空间不够？

A: Z-Image-Turbo需要约13GB空间。确保有足够空间：

```bash
df -h .  # 检查当前目录所在分区的空间
```

### Q: 如何加速git-lfs下载？

A: 增加并行下载数：

```bash
git config --global lfs.concurrenttransfers 8
```

## 推荐下载方式

根据你的网络环境：

- 🇨🇳 **中国大陆**: 使用ModelScope（方法1）
- 🌍 **海外**: 使用HuggingFace（方法2）
- 🔥 **最快**: git-lfs clone（需要安装git-lfs）
- 💯 **最稳定**: 浏览器手动下载后解压

选择最适合你的方式！
