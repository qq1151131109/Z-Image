# Batch Tools - 批量图像处理工具

基于Qwen3-VL和Z-Image的批量图像处理工具集。

## 功能

1. **批量反推提示词**: 使用Qwen3-VL-8B分析图像，生成用于图像生成的提示词
2. **批量生图**: 使用Z-Image + 多个LoRA，从提示词批量生成图像

## 目录结构

```
batch_tools/
├── scripts/
│   ├── reverse_prompts_single_gpu.py       # 单GPU反推提示词
│   ├── run_reverse_prompts_parallel.sh     # 多GPU并行反推
│   ├── batch_generate_with_lora.py         # 单GPU批量生图
│   └── run_batch_generate_parallel.sh      # 多GPU并行生图
├── configs/
│   └── lora_config.example.json            # LoRA配置示例
├── output/
│   ├── reverse_prompts/                    # 反推输出
│   └── lora_generations/                   # 生图输出
└── logs/                                   # 日志目录
```

## 使用方法

### 步骤1: 批量反推提示词

```bash
cd /mnt/shenglin/Z-Image

# 多GPU并行反推
./batch_tools/scripts/run_reverse_prompts_parallel.sh \
    --image-dir /path/to/your/images \
    --num-gpus 6

# 查看进度
tail -f batch_tools/logs/reverse_gpu_1.log

# 结果保存在
# batch_tools/output/reverse_prompts/prompts.csv
```

### 步骤2: 准备LoRA配置

```bash
# 复制示例配置
cp batch_tools/configs/lora_config.example.json batch_tools/configs/my_loras.json

# 编辑配置，添加你的LoRA
vim batch_tools/configs/my_loras.json
```

配置格式:
```json
{
  "loras": [
    {
      "name": "style1",
      "path": "/path/to/lora1.safetensors",
      "scale": 0.75
    },
    {
      "name": "style2",
      "path": "/path/to/lora2.safetensors",
      "scale": 0.8
    }
  ]
}
```

### 步骤3: 批量生图

```bash
# 多GPU并行生图
./batch_tools/scripts/run_batch_generate_parallel.sh \
    --prompts-csv batch_tools/output/reverse_prompts/prompts.csv \
    --lora-config batch_tools/configs/my_loras.json \
    --num-gpus 6

# 查看进度
tail -f batch_tools/logs/generate_gpu_1.log

# 结果保存在
# batch_tools/output/lora_generations/{lora_name}/
```

## 命令参数

### run_reverse_prompts_parallel.sh

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--image-dir` | 图像目录路径 (必需) | - |
| `--output-dir` | 输出目录 | batch_tools/output/reverse_prompts |
| `--num-gpus` | 使用GPU数量 | 6 |
| `--gpu-start` | 起始GPU ID | 1 |
| `--model-path` | Qwen3-VL模型路径 | 自动检测 |

### run_batch_generate_parallel.sh

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--prompts-csv` | 提示词CSV文件 (必需) | - |
| `--lora-config` | LoRA配置文件 (必需) | - |
| `--output-dir` | 输出目录 | batch_tools/output/lora_generations |
| `--num-gpus` | 使用GPU数量 | 6 |
| `--gpu-start` | 起始GPU ID | 1 |
| `--height` | 图像高度 | 1024 |
| `--width` | 图像宽度 | 1024 |
| `--steps` | 推理步数 | 9 |
| `--seed` | 随机种子 | 42 |

## 性能参考

- **反推速度** (Qwen3-VL-8B-FP8): ~2-3秒/图像
- **生图速度** (Z-Image-Turbo): ~5秒/图像 (RTX 4090)

## 依赖

- transformers >= 4.57.1
- qwen-vl-utils
- diffusers (with ZImagePipeline)
- torch >= 2.0
