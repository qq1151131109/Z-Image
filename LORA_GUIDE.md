# Z-Image LoRA 使用指南

本指南介绍如何在 Z-Image 项目中使用 LoRA（Low-Rank Adaptation）进行图像生成推理。

## 目录

- [环境配置](#环境配置)
- [快速开始](#快速开始)
- [使用说明](#使用说明)
- [高级选项](#高级选项)
- [常见问题](#常见问题)

## 环境配置

### 1. 安装依赖

首先，确保安装了最新版本的 diffusers 和其他必要的依赖：

```bash
# 安装项目依赖
pip install -e .

# 从源码安装最新版 diffusers（包含 Z-Image 支持）
pip install git+https://github.com/huggingface/diffusers
```

### 2. 验证安装

运行以下命令验证安装是否成功：

```python
python -c "from diffusers import ZImagePipeline; print('ZImagePipeline imported successfully!')"
```

### 3. 硬件要求

**推荐配置：**
- GPU: NVIDIA GPU with 16GB+ VRAM (如 RTX 4090, A100, H800)
- CUDA: 11.8+
- RAM: 32GB+

**最低配置（使用 CPU Offload）：**
- GPU: NVIDIA GPU with 8GB+ VRAM (如 RTX 3060)
- CUDA: 11.8+
- RAM: 16GB+

## 快速开始

### 方式 1: 使用基础模型（不加载 LoRA）

```bash
python inference_lora.py \
    --prompt "A beautiful landscape with mountains and a lake at sunset" \
    --output output.png
```

### 方式 2: 加载本地 LoRA 权重

```bash
python inference_lora.py \
    --lora_path ./path/to/lora/weights \
    --lora_scale 0.75 \
    --prompt "A beautiful landscape with mountains and a lake at sunset" \
    --output output_lora.png
```

### 方式 3: 从 HuggingFace 加载 LoRA

```bash
python inference_lora.py \
    --lora_path "username/repo-name" \
    --lora_scale 0.75 \
    --prompt "A beautiful landscape with mountains and a lake at sunset" \
    --output output_hf_lora.png
```

## 使用说明

### 基本参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--model_id` | Z-Image 模型路径（HF repo 或本地路径） | `Tongyi-MAI/Z-Image-Turbo` |
| `--lora_path` | LoRA 权重路径（HF repo 或本地路径） | `None` |
| `--lora_scale` | LoRA 强度 (0.0-1.0) | `0.75` |
| `--prompt` | 生成图像的文本提示 | - |
| `--negative_prompt` | 负面提示（可选） | `None` |
| `--output` | 输出图像路径 | `output_lora.png` |

### 生成参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--height` | 图像高度（必须能被 16 整除） | `1024` |
| `--width` | 图像宽度（必须能被 16 整除） | `1024` |
| `--num_inference_steps` | 推理步数（Turbo 模型推荐 9） | `9` |
| `--guidance_scale` | 引导强度（Turbo 用 0.0，Base 用 4.5-7.5） | `0.0` |
| `--seed` | 随机种子 | `42` |

### 性能参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--dtype` | 模型精度 (`float32`, `float16`, `bfloat16`) | `bfloat16` |
| `--attention_backend` | 注意力后端 (`sdpa`, `flash`, `_flash_3`) | `sdpa` |
| `--compile` | 编译模型以加速（首次运行会慢） | `False` |
| `--enable_cpu_offload` | 启用 CPU 卸载以减少显存使用 | `False` |

## 高级选项

### 1. 调整 LoRA 强度

LoRA scale 控制 LoRA 权重的影响强度：

```bash
# 较弱的 LoRA 效果（更接近基础模型）
python inference_lora.py --lora_path ./lora --lora_scale 0.3

# 标准强度
python inference_lora.py --lora_path ./lora --lora_scale 0.75

# 较强的 LoRA 效果
python inference_lora.py --lora_path ./lora --lora_scale 1.0
```

### 2. 使用不同的注意力后端

对于 Hopper 架构 GPU（H100/H800），推荐使用 Flash-Attention-3：

```bash
# 使用 Flash-Attention-2
python inference_lora.py --attention_backend flash --lora_path ./lora

# 使用 Flash-Attention-3（需要 Hopper GPU）
python inference_lora.py --attention_backend _flash_3 --lora_path ./lora
```

### 3. 模型编译以获得最佳性能

启用编译可以显著提升推理速度（首次运行会较慢）：

```bash
python inference_lora.py \
    --compile \
    --attention_backend _flash_3 \
    --lora_path ./lora \
    --prompt "Your prompt here"
```

**性能提示：**
- 在 H100/H800 GPU 上使用 `--compile` + `--attention_backend _flash_3` 可以实现亚秒级生成
- 编译后的模型在首次运行时会慢，但后续运行会非常快
- 建议先进行热身运行，然后再进行实际生成

### 4. 低显存设备配置

对于显存有限的设备（如 8GB-16GB VRAM），使用 CPU offload：

```bash
python inference_lora.py \
    --enable_cpu_offload \
    --dtype float16 \
    --lora_path ./lora \
    --prompt "Your prompt here"
```

### 5. 批量生成

创建一个脚本来批量生成多张图像：

```bash
#!/bin/bash

# 定义提示词数组
prompts=(
    "A serene mountain landscape at sunrise"
    "A futuristic city with flying cars"
    "An ancient temple in a mystical forest"
)

# 循环生成图像
for i in "${!prompts[@]}"; do
    python inference_lora.py \
        --lora_path ./my_lora \
        --lora_scale 0.75 \
        --prompt "${prompts[$i]}" \
        --seed $((42 + i)) \
        --output "output_$i.png"
done
```

## 示例

### 示例 1: 风景照片 LoRA

```bash
python inference_lora.py \
    --lora_path ./landscape_lora \
    --lora_scale 0.8 \
    --prompt "Majestic mountain range reflected in a crystal clear lake, golden hour lighting, 8k uhd, professional photography" \
    --height 1024 \
    --width 1536 \
    --num_inference_steps 9 \
    --seed 42 \
    --output landscape.png
```

### 示例 2: 人像摄影 LoRA

```bash
python inference_lora.py \
    --lora_path ./portrait_lora \
    --lora_scale 0.75 \
    --prompt "Professional headshot portrait of a young woman, soft studio lighting, shallow depth of field, bokeh background" \
    --negative_prompt "blurry, low quality, distorted" \
    --height 1344 \
    --width 896 \
    --seed 123 \
    --output portrait.png
```

### 示例 3: 艺术风格 LoRA

```bash
python inference_lora.py \
    --lora_path "username/anime-style-lora" \
    --lora_scale 0.9 \
    --prompt "Anime style illustration of a magical girl with flowing hair and sparkles" \
    --height 1024 \
    --width 1024 \
    --seed 456 \
    --output anime_art.png
```

## 常见问题

### Q1: 如何获取 LoRA 权重？

**A:** 你可以：
1. 从 HuggingFace 下载社区训练的 LoRA（搜索 "Z-Image LoRA"）
2. 使用 DiffSynth-Studio 等工具训练自己的 LoRA
3. 等待官方或社区发布的 LoRA 模型

### Q2: LoRA 加载失败怎么办？

**A:** 检查以下几点：
1. 确认 LoRA 权重文件格式正确（通常是 `.safetensors` 或 `.bin`）
2. 确认 LoRA 是为 Z-Image 模型训练的（不是 Stable Diffusion 等其他模型）
3. 检查文件路径是否正确
4. 查看错误信息以获取更多细节

### Q3: 为什么生成速度很慢？

**A:** 尝试以下优化：
1. 使用更快的注意力后端：`--attention_backend flash` 或 `--attention_backend _flash_3`
2. 启用模型编译：`--compile`
3. 使用 bfloat16 或 float16：`--dtype bfloat16`
4. 确保 CUDA 版本和 PyTorch 版本匹配

### Q4: 显存不足（OOM）怎么办？

**A:** 尝试以下方法：
1. 启用 CPU offload：`--enable_cpu_offload`
2. 降低图像分辨率：`--height 768 --width 768`
3. 使用 float16：`--dtype float16`
4. 减少推理步数（可能影响质量）：`--num_inference_steps 6`

### Q5: LoRA scale 应该设置为多少？

**A:**
- `0.3-0.5`: 轻微的风格调整
- `0.6-0.8`: 标准强度（推荐）
- `0.9-1.0`: 强烈的 LoRA 效果

建议从 0.75 开始，然后根据效果调整。

### Q6: 支持同时加载多个 LoRA 吗？

**A:** 当前的 `inference_lora.py` 脚本只支持加载单个 LoRA。如需加载多个 LoRA，可以修改脚本使用 `load_lora_weights` 多次加载，并用 `set_adapters` 设置多个适配器的权重。

### Q7: 如何查看已加载的 LoRA？

**A:** 使用 `--list_loras` 参数：

```bash
python inference_lora.py --lora_path ./my_lora --list_loras
```

## 训练 LoRA

如果你想训练自己的 LoRA 模型，推荐使用以下工具：

### DiffSynth-Studio（推荐）

DiffSynth-Studio 提供了完整的 LoRA 训练支持：

```bash
# 安装 DiffSynth-Studio
git clone https://github.com/modelscope/DiffSynth-Studio
cd DiffSynth-Studio
pip install -e .

# 参考 Z-Image 文档进行训练
# https://github.com/modelscope/DiffSynth-Studio/blob/main/docs/en/Model_Details/Z-Image.md
```

### PEFT + 自定义训练脚本

使用 HuggingFace PEFT 库编写自定义训练脚本（需要一定的深度学习经验）。

## 相关资源

- [Z-Image 官方网站](https://tongyi-mai.github.io/Z-Image-blog/)
- [Z-Image HuggingFace 模型](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo)
- [Diffusers 文档](https://huggingface.co/docs/diffusers)
- [PEFT 文档](https://huggingface.co/docs/peft)
- [DiffSynth-Studio](https://github.com/modelscope/DiffSynth-Studio)

## 技术支持

如果遇到问题，请：
1. 查看上方的常见问题部分
2. 检查 GitHub Issues 是否有相似问题
3. 在项目 GitHub 仓库提交 Issue

---

**祝你使用愉快！如有问题，欢迎反馈。**
