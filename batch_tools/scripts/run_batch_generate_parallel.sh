#!/bin/bash
#
# 多GPU并行批量生成图像 (支持多LoRA)
# 从CSV读取提示词，对每个LoRA配置生成所有图像
#
# 使用方法:
#   ./run_batch_generate_parallel.sh --prompts-csv /path/to/prompts.csv --lora-config /path/to/lora_config.json
#

set -e

# 默认配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
BATCH_TOOLS_DIR="$PROJECT_DIR/batch_tools"

# 默认参数
PROMPTS_CSV=""
LORA_CONFIG=""
OUTPUT_DIR="$BATCH_TOOLS_DIR/output/lora_generations"
LOG_DIR="$BATCH_TOOLS_DIR/logs"
NUM_GPUS=6
GPU_START=1
MODEL_PATH="ckpts/Tongyi-MAI/Z-Image-Turbo"
HEIGHT=1024
WIDTH=1024
STEPS=9
SEED=42

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --prompts-csv)
            PROMPTS_CSV="$2"
            shift 2
            ;;
        --lora-config)
            LORA_CONFIG="$2"
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
        --height)
            HEIGHT="$2"
            shift 2
            ;;
        --width)
            WIDTH="$2"
            shift 2
            ;;
        --steps)
            STEPS="$2"
            shift 2
            ;;
        --seed)
            SEED="$2"
            shift 2
            ;;
        -h|--help)
            echo "使用方法: $0 --prompts-csv <CSV文件> --lora-config <配置文件> [选项]"
            echo ""
            echo "必需参数:"
            echo "  --prompts-csv   提示词CSV文件路径 (image_name,prompt格式)"
            echo "  --lora-config   LoRA配置文件路径 (JSON格式)"
            echo ""
            echo "可选参数:"
            echo "  --output-dir    输出目录 (默认: $OUTPUT_DIR)"
            echo "  --num-gpus      使用的GPU数量 (默认: 6)"
            echo "  --gpu-start     起始GPU ID (默认: 1)"
            echo "  --model-path    Z-Image模型路径 (默认: $MODEL_PATH)"
            echo "  --height        图像高度 (默认: 1024)"
            echo "  --width         图像宽度 (默认: 1024)"
            echo "  --steps         推理步数 (默认: 9)"
            echo "  --seed          随机种子 (默认: 42, -1表示随机)"
            echo ""
            echo "示例:"
            echo "  $0 --prompts-csv prompts.csv --lora-config my_loras.json --num-gpus 4"
            exit 0
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 检查必需参数
if [ -z "$PROMPTS_CSV" ]; then
    echo "错误: 必须指定 --prompts-csv 参数"
    echo "使用 -h 或 --help 查看帮助"
    exit 1
fi

if [ -z "$LORA_CONFIG" ]; then
    echo "错误: 必须指定 --lora-config 参数"
    echo "使用 -h 或 --help 查看帮助"
    exit 1
fi

if [ ! -f "$PROMPTS_CSV" ]; then
    echo "错误: 提示词CSV文件不存在: $PROMPTS_CSV"
    exit 1
fi

if [ ! -f "$LORA_CONFIG" ]; then
    echo "错误: LoRA配置文件不存在: $LORA_CONFIG"
    exit 1
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR" "$LOG_DIR"

# 统计提示词数量 (减去表头)
TOTAL_PROMPTS=$(($(wc -l < "$PROMPTS_CSV") - 1))

if [ "$TOTAL_PROMPTS" -le 0 ]; then
    echo "错误: CSV文件中没有提示词"
    exit 1
fi

# 读取LoRA配置数量
NUM_LORAS=$(python3 -c "import json; config=json.load(open('$LORA_CONFIG')); print(len(config['loras']))" 2>&1)
if [ $? -ne 0 ]; then
    echo "错误: 无法解析LoRA配置文件"
    echo "详情: $NUM_LORAS"
    exit 1
fi

if [ "$NUM_LORAS" -eq 0 ]; then
    echo "错误: LoRA配置文件中没有定义任何LoRA"
    exit 1
fi

echo "========================================"
echo "Z-Image + LoRA 批量生图"
echo "========================================"
echo "提示词CSV: $PROMPTS_CSV"
echo "提示词数量: $TOTAL_PROMPTS"
echo "LoRA配置: $LORA_CONFIG"
echo "LoRA数量: $NUM_LORAS"
echo "输出目录: $OUTPUT_DIR"
echo "使用GPU: $NUM_GPUS 个 (GPU $GPU_START - $((GPU_START + NUM_GPUS - 1)))"
echo "图像尺寸: ${WIDTH}x${HEIGHT}"
echo "推理步数: $STEPS"
echo "随机种子: $SEED"
echo "========================================"

# 计算每个GPU处理的提示词数量
PROMPTS_PER_GPU=$((TOTAL_PROMPTS / NUM_GPUS))
REMAINDER=$((TOTAL_PROMPTS % NUM_GPUS))

echo "每个GPU处理约 $PROMPTS_PER_GPU 个提示词"
echo "预计生成图像总数: $((TOTAL_PROMPTS * NUM_LORAS)) 张"
echo ""

# 记录开始时间
START_TIME=$(date +%s)

# 切换到项目目录
cd "$PROJECT_DIR"

# 启动并行进程
PIDS=()
for i in $(seq 0 $((NUM_GPUS - 1))); do
    GPU_ID=$((GPU_START + i))
    START_IDX=$((i * PROMPTS_PER_GPU))

    # 最后一个GPU处理剩余的提示词
    if [ $i -eq $((NUM_GPUS - 1)) ]; then
        NUM_FOR_THIS_GPU=$((PROMPTS_PER_GPU + REMAINDER))
    else
        NUM_FOR_THIS_GPU=$PROMPTS_PER_GPU
    fi

    LOG_FILE="$LOG_DIR/generate_gpu_${GPU_ID}.log"

    echo "[启动] GPU $GPU_ID: 处理 $NUM_FOR_THIS_GPU 个提示词 (索引 $START_IDX 起)"

    python "$SCRIPT_DIR/batch_generate_with_lora.py" \
        --gpu "$GPU_ID" \
        --prompts-csv "$PROMPTS_CSV" \
        --lora-config "$LORA_CONFIG" \
        --start-idx "$START_IDX" \
        --num-prompts "$NUM_FOR_THIS_GPU" \
        --output-dir "$OUTPUT_DIR" \
        --model-path "$MODEL_PATH" \
        --height "$HEIGHT" \
        --width "$WIDTH" \
        --num-inference-steps "$STEPS" \
        --seed "$SEED" \
        > "$LOG_FILE" 2>&1 &

    PIDS+=($!)
done

echo ""
echo "所有GPU进程已启动，等待完成..."
echo "可以使用以下命令监控进度:"
echo "  tail -f $LOG_DIR/generate_gpu_${GPU_START}.log"
echo ""

# 等待所有进程完成
FAILED=0
for i in "${!PIDS[@]}"; do
    GPU_ID=$((GPU_START + i))
    if wait ${PIDS[$i]}; then
        echo "[完成] GPU $GPU_ID 处理完成"
    else
        echo "[失败] GPU $GPU_ID 处理失败，请检查日志: $LOG_DIR/generate_gpu_${GPU_ID}.log"
        FAILED=1
    fi
done

if [ $FAILED -eq 1 ]; then
    echo ""
    echo "警告: 部分GPU处理失败，请检查日志"
fi

# 统计生成的图像
echo ""
echo "统计生成结果..."
TOTAL_GENERATED=0
for lora_dir in "$OUTPUT_DIR"/*/; do
    if [ -d "$lora_dir" ]; then
        lora_name=$(basename "$lora_dir")
        count=$(find "$lora_dir" -name "*.png" | wc -l)
        echo "  [$lora_name]: $count 张"
        TOTAL_GENERATED=$((TOTAL_GENERATED + count))
    fi
done

# 计算耗时
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
ELAPSED_MIN=$((ELAPSED / 60))
ELAPSED_SEC=$((ELAPSED % 60))

echo ""
echo "========================================"
echo "✓ 批量生成完成!"
echo "========================================"
echo "总生成: $TOTAL_GENERATED 张图像"
echo "总耗时: ${ELAPSED_MIN}分${ELAPSED_SEC}秒"
echo "输出目录: $OUTPUT_DIR"
echo "========================================"
