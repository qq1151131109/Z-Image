#!/bin/bash
# 配置文件：生成多样化头像的参数设置

# =============================================================================
# 基础配置
# =============================================================================

# 生成图像数量（可以修改为你需要的数量）
export NUM_IMAGES=3000

# 输出目录
export OUTPUT_DIR="avatars_output"

# =============================================================================
# 模型配置
# =============================================================================

# 模型路径（会自动下载）
export MODEL_PATH="ckpts/Z-Image-Turbo"

# 数据类型（bfloat16/float16/float32）
# bfloat16: 推荐，最佳性能和质量平衡
# float16: 更省显存
export DTYPE="bfloat16"

# 注意力后端
# _native_flash: 默认，兼容性最好
# flash: Flash Attention 2，需要安装flash-attn
# _flash_3: Flash Attention 3，仅支持H100/H800等Hopper架构
export ZIMAGE_ATTENTION="_native_flash"

# 是否编译模型（True/False）
# True: 首次运行慢，后续快（推荐H100/H800使用）
# False: 每次运行速度一致
export COMPILE="False"

# =============================================================================
# 图像参数
# =============================================================================

# 图像尺寸（必须能被16整除）
# 社媒头像推荐尺寸：
# - 1024x1024: Instagram, Twitter等
# - 896x1344: 竖版头像
# - 1344x896: 横版头像
export HEIGHT=1024
export WIDTH=1024

# 推理步数（Turbo模型推荐8-9步）
export NUM_INFERENCE_STEPS=8

# 引导强度（Turbo模型必须用0.0）
export GUIDANCE_SCALE=0.0

# =============================================================================
# 性能优化
# =============================================================================

# 启用CPU卸载（低显存设备使用）
# True: 显存占用低，速度慢
# False: 显存占用高，速度快
export ENABLE_CPU_OFFLOAD="False"

# 批量大小（一次生成多张，需要更多显存）
# 1: 最安全，显存占用最少
# 2-4: 更快，需要更多显存
export BATCH_SIZE=1

# =============================================================================
# 多样性控制
# =============================================================================

# 是否包含不同年龄段（True/False）
export INCLUDE_DIFFERENT_AGES="True"

# 是否包含不同族裔（True/False）
export INCLUDE_DIFFERENT_ETHNICITIES="True"

# 起始随机种子
export SEED_START=42

# =============================================================================
# 使用说明
# =============================================================================
#
# 1. 修改上面的参数
# 2. 运行: source avatar_config.sh
# 3. 运行: python generate_diverse_avatars.py
#
# 或者一行命令：
# source avatar_config.sh && python generate_diverse_avatars.py
#
# =============================================================================

echo "Configuration loaded:"
echo "  - Images to generate: $NUM_IMAGES"
echo "  - Output directory: $OUTPUT_DIR"
echo "  - Image size: ${WIDTH}x${HEIGHT}"
echo "  - Attention backend: $ZIMAGE_ATTENTION"
echo "  - Compile: $COMPILE"
