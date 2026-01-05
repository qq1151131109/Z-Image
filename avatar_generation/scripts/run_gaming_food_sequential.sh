#!/bin/bash

# 顺序生成：先游戏头像，后美食头像
# 每个类别使用GPU 1-6并行生成4000张图片

IMAGES_PER_CATEGORY=4000
NUM_GPUS=6
IMAGES_PER_GPU=$((IMAGES_PER_CATEGORY / NUM_GPUS))  # 667
IMAGES_LAST_GPU=$((IMAGES_PER_CATEGORY - IMAGES_PER_GPU * (NUM_GPUS - 1)))  # 665

HEIGHT=1024
WIDTH=1024

echo "================================================================================"
echo "第一批：游戏头像生成 - GPU 1-6 并行"
echo "================================================================================"
echo "总图像数: $IMAGES_PER_CATEGORY"
echo "使用GPU: 1-6"
echo "每GPU图像数: $IMAGES_PER_GPU (最后一个GPU: $IMAGES_LAST_GPU)"
echo "分辨率: ${HEIGHT}x${WIDTH}"
echo "================================================================================"
echo ""

# 创建输出目录
mkdir -p gaming_avatars_output food_avatars_output logs

# 清理旧日志
rm -f logs/gaming_gpu*.log logs/food_gpu*.log

# ==================== 第一批：游戏头像 ====================

echo "正在启动游戏头像生成进程..."

# GPU 1: 图像 0-666
python generate_gaming_single_gpu.py \
    --gpu 1 \
    --start-idx 0 \
    --num-images $IMAGES_PER_GPU \
    --height $HEIGHT \
    --width $WIDTH \
    > logs/gaming_gpu1.log 2>&1 &
PID1=$!
echo "✓ 进程 1/6 已启动 (GPU 1, PID $PID1, 图像 0-666)"

# GPU 2: 图像 667-1333
python generate_gaming_single_gpu.py \
    --gpu 2 \
    --start-idx 667 \
    --num-images $IMAGES_PER_GPU \
    --height $HEIGHT \
    --width $WIDTH \
    > logs/gaming_gpu2.log 2>&1 &
PID2=$!
echo "✓ 进程 2/6 已启动 (GPU 2, PID $PID2, 图像 667-1333)"

# GPU 3: 图像 1334-2000
python generate_gaming_single_gpu.py \
    --gpu 3 \
    --start-idx 1334 \
    --num-images $IMAGES_PER_GPU \
    --height $HEIGHT \
    --width $WIDTH \
    > logs/gaming_gpu3.log 2>&1 &
PID3=$!
echo "✓ 进程 3/6 已启动 (GPU 3, PID $PID3, 图像 1334-2000)"

# GPU 4: 图像 2001-2667
python generate_gaming_single_gpu.py \
    --gpu 4 \
    --start-idx 2001 \
    --num-images $IMAGES_PER_GPU \
    --height $HEIGHT \
    --width $WIDTH \
    > logs/gaming_gpu4.log 2>&1 &
PID4=$!
echo "✓ 进程 4/6 已启动 (GPU 4, PID $PID4, 图像 2001-2667)"

# GPU 5: 图像 2668-3334
python generate_gaming_single_gpu.py \
    --gpu 5 \
    --start-idx 2668 \
    --num-images $IMAGES_PER_GPU \
    --height $HEIGHT \
    --width $WIDTH \
    > logs/gaming_gpu5.log 2>&1 &
PID5=$!
echo "✓ 进程 5/6 已启动 (GPU 5, PID $PID5, 图像 2668-3334)"

# GPU 6: 图像 3335-3999
python generate_gaming_single_gpu.py \
    --gpu 6 \
    --start-idx 3335 \
    --num-images $IMAGES_LAST_GPU \
    --height $HEIGHT \
    --width $WIDTH \
    > logs/gaming_gpu6.log 2>&1 &
PID6=$!
echo "✓ 进程 6/6 已启动 (GPU 6, PID $PID6, 图像 3335-3999)"

echo ""
echo "游戏头像生成进程已全部启动！等待完成..."
echo "================================================================================"

# 记录开始时间
START_TIME=$(date +%s)

# 等待所有游戏进程完成
wait $PID1
echo "✓ GPU 1 完成"
wait $PID2
echo "✓ GPU 2 完成"
wait $PID3
echo "✓ GPU 3 完成"
wait $PID4
echo "✓ GPU 4 完成"
wait $PID5
echo "✓ GPU 5 完成"
wait $PID6
echo "✓ GPU 6 完成"

# 计算游戏头像耗时
GAMING_END_TIME=$(date +%s)
GAMING_SECONDS=$((GAMING_END_TIME - START_TIME))
GAMING_MINUTES=$(echo "scale=2; $GAMING_SECONDS / 60" | bc)

echo ""
echo "================================================================================"
echo "✓ 游戏头像生成完成！"
echo "================================================================================"
echo "耗时: $GAMING_MINUTES 分钟"
total_gaming=$(find gaming_avatars_output -name "*.png" 2>/dev/null | wc -l)
echo "总计生成: $total_gaming/$IMAGES_PER_CATEGORY 张游戏头像"
echo "================================================================================"

# ==================== 第二批：美食头像 ====================

echo ""
echo "================================================================================"
echo "第二批：美食头像生成 - GPU 1-6 并行"
echo "================================================================================"
echo ""

echo "正在启动美食头像生成进程..."

# GPU 1: 图像 0-666
python generate_food_single_gpu.py \
    --gpu 1 \
    --start-idx 0 \
    --num-images $IMAGES_PER_GPU \
    --height $HEIGHT \
    --width $WIDTH \
    > logs/food_gpu1.log 2>&1 &
PID1=$!
echo "✓ 进程 1/6 已启动 (GPU 1, PID $PID1, 图像 0-666)"

# GPU 2: 图像 667-1333
python generate_food_single_gpu.py \
    --gpu 2 \
    --start-idx 667 \
    --num-images $IMAGES_PER_GPU \
    --height $HEIGHT \
    --width $WIDTH \
    > logs/food_gpu2.log 2>&1 &
PID2=$!
echo "✓ 进程 2/6 已启动 (GPU 2, PID $PID2, 图像 667-1333)"

# GPU 3: 图像 1334-2000
python generate_food_single_gpu.py \
    --gpu 3 \
    --start-idx 1334 \
    --num-images $IMAGES_PER_GPU \
    --height $HEIGHT \
    --width $WIDTH \
    > logs/food_gpu3.log 2>&1 &
PID3=$!
echo "✓ 进程 3/6 已启动 (GPU 3, PID $PID3, 图像 1334-2000)"

# GPU 4: 图像 2001-2667
python generate_food_single_gpu.py \
    --gpu 4 \
    --start-idx 2001 \
    --num-images $IMAGES_PER_GPU \
    --height $HEIGHT \
    --width $WIDTH \
    > logs/food_gpu4.log 2>&1 &
PID4=$!
echo "✓ 进程 4/6 已启动 (GPU 4, PID $PID4, 图像 2001-2667)"

# GPU 5: 图像 2668-3334
python generate_food_single_gpu.py \
    --gpu 5 \
    --start-idx 2668 \
    --num-images $IMAGES_PER_GPU \
    --height $HEIGHT \
    --width $WIDTH \
    > logs/food_gpu5.log 2>&1 &
PID5=$!
echo "✓ 进程 5/6 已启动 (GPU 5, PID $PID5, 图像 2668-3334)"

# GPU 6: 图像 3335-3999
python generate_food_single_gpu.py \
    --gpu 6 \
    --start-idx 3335 \
    --num-images $IMAGES_LAST_GPU \
    --height $HEIGHT \
    --width $WIDTH \
    > logs/food_gpu6.log 2>&1 &
PID6=$!
echo "✓ 进程 6/6 已启动 (GPU 6, PID $PID6, 图像 3335-3999)"

echo ""
echo "美食头像生成进程已全部启动！等待完成..."
echo "================================================================================"

# 等待所有美食进程完成
wait $PID1
echo "✓ GPU 1 完成"
wait $PID2
echo "✓ GPU 2 完成"
wait $PID3
echo "✓ GPU 3 完成"
wait $PID4
echo "✓ GPU 4 完成"
wait $PID5
echo "✓ GPU 5 完成"
wait $PID6
echo "✓ GPU 6 完成"

# 计算美食头像耗时
FOOD_END_TIME=$(date +%s)
FOOD_SECONDS=$((FOOD_END_TIME - GAMING_END_TIME))
FOOD_MINUTES=$(echo "scale=2; $FOOD_SECONDS / 60" | bc)

# 计算总耗时
TOTAL_SECONDS=$((FOOD_END_TIME - START_TIME))
TOTAL_MINUTES=$(echo "scale=2; $TOTAL_SECONDS / 60" | bc)
TOTAL_HOURS=$(echo "scale=2; $TOTAL_SECONDS / 3600" | bc)

echo ""
echo "================================================================================"
echo "✓ 美食头像生成完成！"
echo "================================================================================"
echo "耗时: $FOOD_MINUTES 分钟"
total_food=$(find food_avatars_output -name "*.png" 2>/dev/null | wc -l)
echo "总计生成: $total_food/$IMAGES_PER_CATEGORY 张美食头像"
echo "================================================================================"

# ==================== 最终统计 ====================

echo ""
echo "================================================================================"
echo "✓✓✓ 所有任务完成！✓✓✓"
echo "================================================================================"
echo ""
echo "【游戏头像】"
echo "  生成数量: $total_gaming/$IMAGES_PER_CATEGORY 张"
echo "  耗时: $GAMING_MINUTES 分钟"
echo "  输出目录: gaming_avatars_output/"
echo ""
echo "【美食头像】"
echo "  生成数量: $total_food/$IMAGES_PER_CATEGORY 张"
echo "  耗时: $FOOD_MINUTES 分钟"
echo "  输出目录: food_avatars_output/"
echo ""
echo "【总计】"
echo "  总生成数量: $((total_gaming + total_food))/8000 张"
echo "  总耗时: $TOTAL_MINUTES 分钟 ($TOTAL_HOURS 小时)"
echo ""
echo "================================================================================"
