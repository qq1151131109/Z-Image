#!/bin/bash

# 顺序生成：先游戏（6个GPU并行），后美食（6个GPU并行）
# 每个类别4000张图片

cd /home/ubuntu/shenglin/Z-Image

echo "========================================================"
echo "第一批：游戏头像生成 - GPU 1-6 并行"
echo "========================================================"

# 清理旧日志
rm -f logs/gaming_gpu*.log logs/food_gpu*.log

# 启动游戏头像生成 - GPU 1-6
nohup python generate_gaming_single_gpu.py --gpu 1 --start-idx 0 --num-images 667 > logs/gaming_gpu1.log 2>&1 &
nohup python generate_gaming_single_gpu.py --gpu 2 --start-idx 667 --num-images 667 > logs/gaming_gpu2.log 2>&1 &
nohup python generate_gaming_single_gpu.py --gpu 3 --start-idx 1334 --num-images 667 > logs/gaming_gpu3.log 2>&1 &
nohup python generate_gaming_single_gpu.py --gpu 4 --start-idx 2001 --num-images 667 > logs/gaming_gpu4.log 2>&1 &
nohup python generate_gaming_single_gpu.py --gpu 5 --start-idx 2668 --num-images 667 > logs/gaming_gpu5.log 2>&1 &
nohup python generate_gaming_single_gpu.py --gpu 6 --start-idx 3335 --num-images 665 > logs/gaming_gpu6.log 2>&1 &

echo "✓ 游戏头像生成已启动 (6个GPU并行)"
echo ""
echo "监控命令:"
echo "  查看进度: tail -f logs/gaming_gpu1.log"
echo "  统计数量: find gaming_avatars_output -name '*.png' | wc -l"
echo "  GPU状态: watch -n 5 nvidia-smi"
echo ""
echo "等待游戏头像生成完成后，请手动运行第二批："
echo "  bash /home/ubuntu/shenglin/Z-Image/launch_food.sh"
echo "========================================================"
