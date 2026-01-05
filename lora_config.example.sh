#!/bin/bash
# Z-Image LoRA 推理配置示例
# 复制此文件为 lora_config.sh 并根据需要修改

# ============================================================
# 模型配置
# ============================================================

# Z-Image 模型路径（HuggingFace repo ID 或本地路径）
MODEL_ID="Tongyi-MAI/Z-Image-Turbo"

# LoRA 权重路径（留空则不使用 LoRA）
LORA_PATH=""
# LORA_PATH="./path/to/your/lora"
# LORA_PATH="username/lora-repo-name"

# LoRA 强度 (0.0 - 1.0)
LORA_SCALE=0.75

# ============================================================
# 生成参数
# ============================================================

# 文本提示
PROMPT="Young Chinese woman in red Hanfu, intricate embroidery. Impeccable makeup, red floral forehead pattern. Elaborate high bun, golden phoenix headdress, red flowers, beads."

# 负面提示（可选）
NEGATIVE_PROMPT=""

# 图像尺寸（必须能被 16 整除）
HEIGHT=1024
WIDTH=1024

# 推理步数（Turbo 推荐 9，Base 推荐 28）
NUM_INFERENCE_STEPS=9

# 引导强度（Turbo 用 0.0，Base 用 4.5-7.5）
GUIDANCE_SCALE=0.0

# 随机种子
SEED=42

# 输出路径
OUTPUT="output.png"

# ============================================================
# 性能配置
# ============================================================

# 模型精度 (float32, float16, bfloat16)
DTYPE="bfloat16"

# 注意力后端 (sdpa, flash, _flash_3)
ATTENTION_BACKEND="sdpa"

# 是否编译模型（首次运行慢，后续快）
COMPILE=false

# 是否启用 CPU offload（降低显存使用）
CPU_OFFLOAD=false

# ============================================================
# 运行脚本
# ============================================================

# 构建命令
CMD="python inference_lora.py \
    --model_id \"$MODEL_ID\" \
    --prompt \"$PROMPT\" \
    --height $HEIGHT \
    --width $WIDTH \
    --num_inference_steps $NUM_INFERENCE_STEPS \
    --guidance_scale $GUIDANCE_SCALE \
    --seed $SEED \
    --output \"$OUTPUT\" \
    --dtype $DTYPE \
    --attention_backend $ATTENTION_BACKEND"

# 添加 LoRA 参数
if [ -n "$LORA_PATH" ]; then
    CMD="$CMD --lora_path \"$LORA_PATH\" --lora_scale $LORA_SCALE"
fi

# 添加负面提示
if [ -n "$NEGATIVE_PROMPT" ]; then
    CMD="$CMD --negative_prompt \"$NEGATIVE_PROMPT\""
fi

# 添加编译选项
if [ "$COMPILE" = true ]; then
    CMD="$CMD --compile"
fi

# 添加 CPU offload 选项
if [ "$CPU_OFFLOAD" = true ]; then
    CMD="$CMD --enable_cpu_offload"
fi

# 执行命令
echo "Running command:"
echo "$CMD"
echo ""
eval $CMD
