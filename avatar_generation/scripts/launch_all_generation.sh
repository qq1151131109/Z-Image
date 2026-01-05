#!/bin/bash

# 并行生成游戏和美食头像 - 使用GPU 1-6
# 每个类别4000张图片

cd /home/ubuntu/shenglin/Z-Image

echo "================================================"
echo "启动12个并行进程 (游戏×6 + 美食×6)"
echo "================================================"

# 游戏头像生成 - GPU 1-6
nohup python generate_gaming_single_gpu.py --gpu 1 --start-idx 0 --num-images 667 > logs/gaming_gpu1.log 2>&1 &
nohup python generate_gaming_single_gpu.py --gpu 2 --start-idx 667 --num-images 667 > logs/gaming_gpu2.log 2>&1 &
nohup python generate_gaming_single_gpu.py --gpu 3 --start-idx 1334 --num-images 667 > logs/gaming_gpu3.log 2>&1 &
nohup python generate_gaming_single_gpu.py --gpu 4 --start-idx 2001 --num-images 667 > logs/gaming_gpu4.log 2>&1 &
nohup python generate_gaming_single_gpu.py --gpu 5 --start-idx 2668 --num-images 667 > logs/gaming_gpu5.log 2>&1 &
nohup python generate_gaming_single_gpu.py --gpu 6 --start-idx 3335 --num-images 665 > logs/gaming_gpu6.log 2>&1 &

echo "✓ 游戏头像生成任务已启动 (6个进程)"

# 美食头像生成 - GPU 1-6
nohup python generate_food_single_gpu.py --gpu 1 --start-idx 0 --num-images 667 > logs/food_gpu1.log 2>&1 &
nohup python generate_food_single_gpu.py --gpu 2 --start-idx 667 --num-images 667 > logs/food_gpu2.log 2>&1 &
nohup python generate_food_single_gpu.py --gpu 3 --start-idx 1334 --num-images 667 > logs/food_gpu3.log 2>&1 &
nohup python generate_food_single_gpu.py --gpu 4 --start-idx 2001 --num-images 667 > logs/food_gpu4.log 2>&1 &
nohup python generate_food_single_gpu.py --gpu 5 --start-idx 2668 --num-images 667 > logs/food_gpu5.log 2>&1 &
nohup python generate_food_single_gpu.py --gpu 6 --start-idx 3335 --num-images 665 > logs/food_gpu6.log 2>&1 &

echo "✓ 美食头像生成任务已启动 (6个进程)"

sleep 2

echo ""
echo "================================================"
echo "状态检查"
echo "================================================"
GAMING_PROCS=$(ps aux | grep "generate_gaming_single_gpu" | grep -v grep | wc -l)
FOOD_PROCS=$(ps aux | grep "generate_food_single_gpu" | grep -v grep | wc -l)
echo "运行中的进程: 游戏=${GAMING_PROCS}, 美食=${FOOD_PROCS}, 总计=$((GAMING_PROCS + FOOD_PROCS))"

echo ""
echo "日志文件:"
ls -lh logs/gaming_gpu*.log logs/food_gpu*.log 2>/dev/null | tail -12

echo ""
echo "================================================"
echo "监控命令:"
echo "  查看进度: tail -f logs/gaming_gpu1.log"
echo "  查看所有日志: ls -lh logs/"
echo "  统计生成数量: find gaming_avatars_output -name '*.png' | wc -l"
echo "  GPU使用情况: nvidia-smi"
echo "================================================"
