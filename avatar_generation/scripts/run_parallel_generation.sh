#!/bin/bash
# 使用1-6号GPU并行生成3000张头像
# 每个GPU生成500张

# 总图像数
TOTAL_IMAGES=3000

# GPU数量
NUM_GPUS=6

# 每个GPU生成的数量
IMAGES_PER_GPU=$((TOTAL_IMAGES / NUM_GPUS))

echo "==================================================================="
echo "Multi-GPU Avatar Generation"
echo "==================================================================="
echo "Total images: $TOTAL_IMAGES"
echo "GPUs: 1-6 (${NUM_GPUS} GPUs)"
echo "Images per GPU: $IMAGES_PER_GPU"
echo "==================================================================="
echo ""

# 创建日志目录
mkdir -p logs

# 启动6个并行进程，每个使用不同的GPU
for gpu_id in {1..6}; do
    # 计算这个GPU负责的图像范围
    start_idx=$(( (gpu_id - 1) * IMAGES_PER_GPU ))
    end_idx=$(( gpu_id * IMAGES_PER_GPU ))

    echo "[GPU $gpu_id] Generating images $start_idx to $((end_idx - 1))"

    # 在后台运行，将输出重定向到日志文件
    CUDA_VISIBLE_DEVICES=$gpu_id python generate_diverse_avatars_parallel.py \
        --start_idx $start_idx \
        --end_idx $end_idx \
        --gpu_id $gpu_id \
        > logs/gpu_${gpu_id}.log 2>&1 &

    # 等待1秒，避免同时加载模型导致显存问题
    sleep 1
done

echo ""
echo "All GPU processes started!"
echo "Monitor progress with: tail -f logs/gpu_*.log"
echo ""
echo "Wait for all processes to complete..."

# 等待所有后台进程完成
wait

echo ""
echo "==================================================================="
echo "✓ All GPUs finished!"
echo "==================================================================="
echo "Check output in: avatars_output/"
echo "Check logs in: logs/"
echo ""

# 统计生成的图像数量
total_generated=$(ls avatars_output/*.png 2>/dev/null | wc -l)
echo "Total images generated: $total_generated / $TOTAL_IMAGES"

if [ $total_generated -eq $TOTAL_IMAGES ]; then
    echo "✓ SUCCESS: All images generated!"
else
    echo "⚠ WARNING: Some images may be missing. Check logs for errors."
fi
