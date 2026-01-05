#!/bin/bash
#
# 多GPU并行反推图像提示词
# 使用Qwen3-VL-8B模型批量分析图像并生成提示词
#
# 使用方法:
#   ./run_reverse_prompts_parallel.sh --image-dir /path/to/images --num-gpus 6
#

set -e

# 默认配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
BATCH_TOOLS_DIR="$PROJECT_DIR/batch_tools"

# 默认参数
IMAGE_DIR=""
OUTPUT_DIR="$BATCH_TOOLS_DIR/output/reverse_prompts"
LOG_DIR="$BATCH_TOOLS_DIR/logs"
NUM_GPUS=6
GPU_START=1
MODEL_PATH="/home/ubuntu/shenglin/ComfyUI/models/prompt_generator/Qwen3-VL-8B-Instruct-FP8"

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --image-dir)
            IMAGE_DIR="$2"
            shift 2
            ;;
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --num-gpus)
            NUM_GPUS="$2"
            shift 2
            ;;
        --gpu-start)
            GPU_START="$2"
            shift 2
            ;;
        --model-path)
            MODEL_PATH="$2"
            shift 2
            ;;
        -h|--help)
            echo "使用方法: $0 --image-dir <图像目录> [选项]"
            echo ""
            echo "选项:"
            echo "  --image-dir     图像目录路径 (必需)"
            echo "  --output-dir    输出目录 (默认: $OUTPUT_DIR)"
            echo "  --num-gpus      使用的GPU数量 (默认: 6)"
            echo "  --gpu-start     起始GPU ID (默认: 1)"
            echo "  --model-path    Qwen3-VL模型路径"
            echo ""
            echo "示例:"
            echo "  $0 --image-dir /data/images --num-gpus 4"
            exit 0
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 检查必需参数
if [ -z "$IMAGE_DIR" ]; then
    echo "错误: 必须指定 --image-dir 参数"
    echo "使用 -h 或 --help 查看帮助"
    exit 1
fi

if [ ! -d "$IMAGE_DIR" ]; then
    echo "错误: 图像目录不存在: $IMAGE_DIR"
    exit 1
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR" "$LOG_DIR"

# 统计图像数量
TOTAL_IMAGES=$(find "$IMAGE_DIR" -maxdepth 1 -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.webp" \) | wc -l)

if [ "$TOTAL_IMAGES" -eq 0 ]; then
    echo "错误: 在 $IMAGE_DIR 中没有找到图像文件"
    exit 1
fi

echo "========================================"
echo "Qwen3-VL 批量图像反推"
echo "========================================"
echo "图像目录: $IMAGE_DIR"
echo "图像总数: $TOTAL_IMAGES"
echo "输出目录: $OUTPUT_DIR"
echo "使用GPU: $NUM_GPUS 个 (GPU $GPU_START - $((GPU_START + NUM_GPUS - 1)))"
echo "模型: $MODEL_PATH"
echo "========================================"

# 计算每个GPU处理的图像数量
IMAGES_PER_GPU=$((TOTAL_IMAGES / NUM_GPUS))
REMAINDER=$((TOTAL_IMAGES % NUM_GPUS))

echo "每个GPU处理约 $IMAGES_PER_GPU 张图像"
echo ""

# 记录开始时间
START_TIME=$(date +%s)

# 启动并行进程
PIDS=()
for i in $(seq 0 $((NUM_GPUS - 1))); do
    GPU_ID=$((GPU_START + i))
    START_IDX=$((i * IMAGES_PER_GPU))

    # 最后一个GPU处理剩余的图像
    if [ $i -eq $((NUM_GPUS - 1)) ]; then
        NUM_FOR_THIS_GPU=$((IMAGES_PER_GPU + REMAINDER))
    else
        NUM_FOR_THIS_GPU=$IMAGES_PER_GPU
    fi

    OUTPUT_CSV="$OUTPUT_DIR/gpu_${GPU_ID}.csv"
    LOG_FILE="$LOG_DIR/reverse_gpu_${GPU_ID}.log"

    echo "[启动] GPU $GPU_ID: 处理 $NUM_FOR_THIS_GPU 张图像 (索引 $START_IDX 起)"

    python "$SCRIPT_DIR/reverse_prompts_single_gpu.py" \
        --gpu "$GPU_ID" \
        --image-dir "$IMAGE_DIR" \
        --start-idx "$START_IDX" \
        --num-images "$NUM_FOR_THIS_GPU" \
        --output-csv "$OUTPUT_CSV" \
        --model-path "$MODEL_PATH" \
        > "$LOG_FILE" 2>&1 &

    PIDS+=($!)
done

echo ""
echo "所有GPU进程已启动，等待完成..."
echo "可以使用以下命令监控进度:"
echo "  tail -f $LOG_DIR/reverse_gpu_${GPU_START}.log"
echo ""

# 等待所有进程完成
FAILED=0
for i in "${!PIDS[@]}"; do
    GPU_ID=$((GPU_START + i))
    if wait ${PIDS[$i]}; then
        echo "[完成] GPU $GPU_ID 处理完成"
    else
        echo "[失败] GPU $GPU_ID 处理失败，请检查日志: $LOG_DIR/reverse_gpu_${GPU_ID}.log"
        FAILED=1
    fi
done

if [ $FAILED -eq 1 ]; then
    echo ""
    echo "警告: 部分GPU处理失败，请检查日志"
fi

# 合并CSV文件
echo ""
echo "合并CSV文件..."
MERGED_CSV="$OUTPUT_DIR/prompts.csv"

# 写入表头
echo "image_name,prompt" > "$MERGED_CSV"

# 合并所有GPU的结果（跳过各自的表头）
for i in $(seq 0 $((NUM_GPUS - 1))); do
    GPU_ID=$((GPU_START + i))
    GPU_CSV="$OUTPUT_DIR/gpu_${GPU_ID}.csv"
    if [ -f "$GPU_CSV" ]; then
        tail -n +2 "$GPU_CSV" >> "$MERGED_CSV"
    fi
done

# 统计结果
TOTAL_RESULTS=$(($(wc -l < "$MERGED_CSV") - 1))

# 计算耗时
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
ELAPSED_MIN=$((ELAPSED / 60))
ELAPSED_SEC=$((ELAPSED % 60))

echo ""
echo "========================================"
echo "✓ 反推完成!"
echo "========================================"
echo "总处理: $TOTAL_RESULTS 张图像"
echo "总耗时: ${ELAPSED_MIN}分${ELAPSED_SEC}秒"
echo "输出文件: $MERGED_CSV"
echo "========================================"
