# Z-Image LoRA 快速入门

## 🚀 5 分钟上手

### 步骤 1: 安装依赖

运行自动安装脚本：

```bash
./install_lora_deps.sh
```

或手动安装：

```bash
# 激活虚拟环境
source .venv/bin/activate

# 安装 PyTorch (CUDA 12.1)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# 安装最新版 Diffusers
pip install git+https://github.com/huggingface/diffusers

# 安装项目依赖
pip install -e .
```

### 步骤 2: 运行推理

**不使用 LoRA（基础模型）：**

```bash
python inference_lora.py \
    --prompt "A beautiful landscape with mountains and a lake at sunset" \
    --output output.png
```

**使用 LoRA：**

```bash
python inference_lora.py \
    --lora_path ./path/to/your/lora \
    --lora_scale 0.75 \
    --prompt "A beautiful landscape with mountains and a lake at sunset" \
    --output output_lora.png
```

### 步骤 3: 查看结果

生成的图像会保存到指定的输出路径。

## 📖 详细文档

更多高级用法和配置选项，请查看：

- [完整 LoRA 使用指南](LORA_GUIDE.md)
- [配置示例](lora_config.example.sh)

## 🎯 常用命令

### 调整图像尺寸

```bash
python inference_lora.py \
    --prompt "Your prompt" \
    --height 768 \
    --width 1344 \
    --output wide.png
```

### 使用高性能模式（H100/H800）

```bash
python inference_lora.py \
    --prompt "Your prompt" \
    --compile \
    --attention_backend _flash_3 \
    --lora_path ./lora
```

### 低显存模式

```bash
python inference_lora.py \
    --prompt "Your prompt" \
    --enable_cpu_offload \
    --dtype float16 \
    --lora_path ./lora
```

## ❓ 遇到问题？

1. 查看 [常见问题](LORA_GUIDE.md#常见问题)
2. 检查 GitHub Issues
3. 提交新的 Issue

## 📚 资源链接

- [Z-Image 官方文档](https://tongyi-mai.github.io/Z-Image-blog/)
- [HuggingFace 模型](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo)
- [Diffusers 文档](https://huggingface.co/docs/diffusers)
