#!/bin/bash

# 并行生成6000张图像，使用GPU 1-6
# 每个GPU生成1000张图像

TOTAL_IMAGES=6000
NUM_GPUS=6
IMAGES_PER_GPU=$((TOTAL_IMAGES / NUM_GPUS))  # 1000

OUTPUT_DIR="/mnt/shenglin/Z-Image/avatars_6000"
MODEL_PATH="ckpts/Tongyi-MAI/Z-Image-Turbo"
HEIGHT=1024
WIDTH=1024

echo "================================================================================"
echo "并行生成6000张多样化美国女性头像"
echo "================================================================================"
echo "总图像数: $TOTAL_IMAGES"
echo "使用GPU: 1-6"
echo "每GPU图像数: $IMAGES_PER_GPU"
echo "分辨率: ${HEIGHT}x${WIDTH}"
echo "输出目录: $OUTPUT_DIR"
echo "模型路径: $MODEL_PATH"
echo "================================================================================"
echo ""

# 创建输出目录
mkdir -p "$OUTPUT_DIR"
mkdir -p logs

# 启动6个并行进程
echo "正在启动并行进程..."

# GPU 1: 图像 0-999
python generate_on_single_gpu.py \
    --gpu 1 \
    --start-idx 0 \
    --num-images $IMAGES_PER_GPU \
    --output-dir "$OUTPUT_DIR" \
    --model-path "$MODEL_PATH" \
    --height $HEIGHT \
    --width $WIDTH \
    > logs/gpu_1.log 2>&1 &
PID1=$!
echo "✓ 进程 1/6 已启动 (GPU 1, PID $PID1, 图像 0-999)"

# GPU 2: 图像 1000-1999
python generate_on_single_gpu.py \
    --gpu 2 \
    --start-idx 1000 \
    --num-images $IMAGES_PER_GPU \
    --output-dir "$OUTPUT_DIR" \
    --model-path "$MODEL_PATH" \
    --height $HEIGHT \
    --width $WIDTH \
    > logs/gpu_2.log 2>&1 &
PID2=$!
echo "✓ 进程 2/6 已启动 (GPU 2, PID $PID2, 图像 1000-1999)"

# GPU 3: 图像 2000-2999
python generate_on_single_gpu.py \
    --gpu 3 \
    --start-idx 2000 \
    --num-images $IMAGES_PER_GPU \
    --output-dir "$OUTPUT_DIR" \
    --model-path "$MODEL_PATH" \
    --height $HEIGHT \
    --width $WIDTH \
    > logs/gpu_3.log 2>&1 &
PID3=$!
echo "✓ 进程 3/6 已启动 (GPU 3, PID $PID3, 图像 2000-2999)"

# GPU 4: 图像 3000-3999
python generate_on_single_gpu.py \
    --gpu 4 \
    --start-idx 3000 \
    --num-images $IMAGES_PER_GPU \
    --output-dir "$OUTPUT_DIR" \
    --model-path "$MODEL_PATH" \
    --height $HEIGHT \
    --width $WIDTH \
    > logs/gpu_4.log 2>&1 &
PID4=$!
echo "✓ 进程 4/6 已启动 (GPU 4, PID $PID4, 图像 3000-3999)"

# GPU 5: 图像 4000-4999
python generate_on_single_gpu.py \
    --gpu 5 \
    --start-idx 4000 \
    --num-images $IMAGES_PER_GPU \
    --output-dir "$OUTPUT_DIR" \
    --model-path "$MODEL_PATH" \
    --height $HEIGHT \
    --width $WIDTH \
    > logs/gpu_5.log 2>&1 &
PID5=$!
echo "✓ 进程 5/6 已启动 (GPU 5, PID $PID5, 图像 4000-4999)"

# GPU 6: 图像 5000-5999
python generate_on_single_gpu.py \
    --gpu 6 \
    --start-idx 5000 \
    --num-images $IMAGES_PER_GPU \
    --output-dir "$OUTPUT_DIR" \
    --model-path "$MODEL_PATH" \
    --height $HEIGHT \
    --width $WIDTH \
    > logs/gpu_6.log 2>&1 &
PID6=$!
echo "✓ 进程 6/6 已启动 (GPU 6, PID $PID6, 图像 5000-5999)"

echo ""
echo "所有进程已启动！等待完成..."
echo "================================================================================"
echo ""
echo "可以使用以下命令监控进度:"
echo "  - 查看GPU 1日志: tail -f logs/gpu_1.log"
echo "  - 查看GPU 2日志: tail -f logs/gpu_2.log"
echo "  - 查看所有进程: ps -p $PID1,$PID2,$PID3,$PID4,$PID5,$PID6"
echo "  - 统计已生成图像: ls avatars_6000/gpu_*/avatar_*.png | wc -l"
echo ""
echo "================================================================================"

# 记录开始时间
START_TIME=$(date +%s)

# 等待所有进程完成
wait $PID1
echo "✓ 进程 1/6 已完成 (GPU 1)"

wait $PID2
echo "✓ 进程 2/6 已完成 (GPU 2)"

wait $PID3
echo "✓ 进程 3/6 已完成 (GPU 3)"

wait $PID4
echo "✓ 进程 4/6 已完成 (GPU 4)"

wait $PID5
echo "✓ 进程 5/6 已完成 (GPU 5)"

wait $PID6
echo "✓ 进程 6/6 已完成 (GPU 6)"

# 计算总耗时
END_TIME=$(date +%s)
TOTAL_SECONDS=$((END_TIME - START_TIME))
TOTAL_MINUTES=$(echo "scale=2; $TOTAL_SECONDS / 60" | bc)
TOTAL_HOURS=$(echo "scale=2; $TOTAL_SECONDS / 3600" | bc)

# 打印最终统计
echo ""
echo "================================================================================"
echo "✓ 所有进程完成!"
echo "================================================================================"
echo "总耗时: $TOTAL_MINUTES 分钟 ($TOTAL_HOURS 小时)"
echo "输出目录: $OUTPUT_DIR"
echo ""

# 统计生成的图像数量
echo "各GPU生成统计:"
for gpu_id in 1 2 3 4 5 6; do
    count=$(ls "$OUTPUT_DIR/gpu_$gpu_id"/*.png 2>/dev/null | wc -l)
    echo "  GPU $gpu_id: $count 张图像"
done

echo ""
total_generated=$(ls "$OUTPUT_DIR"/gpu_*/*.png 2>/dev/null | wc -l)
success_rate=$(echo "scale=1; $total_generated * 100 / $TOTAL_IMAGES" | bc)
echo "总计生成: $total_generated/$TOTAL_IMAGES 张图像"
echo "成功率: $success_rate%"
echo "================================================================================"
