# 多GPU并行生成使用指南

## 快速开始（使用1-6号GPU）

### 一键启动

```bash
# 确保脚本可执行
chmod +x run_parallel_generation.sh

# 运行并行生成
./run_parallel_generation.sh
```

### 工作原理

脚本会自动将3000张图像分配给6个GPU：

- **GPU 1**: 生成 avatar_0000.png 到 avatar_0499.png (500张)
- **GPU 2**: 生成 avatar_0500.png 到 avatar_0999.png (500张)
- **GPU 3**: 生成 avatar_1000.png 到 avatar_1499.png (500张)
- **GPU 4**: 生成 avatar_1500.png 到 avatar_1999.png (500张)
- **GPU 5**: 生成 avatar_2000.png 到 avatar_2499.png (500张)
- **GPU 6**: 生成 avatar_2500.png 到 avatar_2999.png (500张)

所有GPU会**同时工作**，大幅缩短总时间！

### 监控进度

```bash
# 查看所有GPU的实时日志
tail -f logs/gpu_*.log

# 查看特定GPU的日志
tail -f logs/gpu_1.log

# 查看已生成的图像数量
ls avatars_output/*.png | wc -l

# 实时监控GPU使用情况
watch -n 1 nvidia-smi
```

### 预计时间

假设单GPU生成500张需要的时间：

| GPU型号 | 单张耗时 | 单GPU 500张 | 6个GPU并行总耗时 |
|---------|---------|-------------|-----------------|
| H100/H800 | 0.8秒 | 6.7分钟 | ~7分钟 |
| A100 | 1.5秒 | 12.5分钟 | ~13分钟 |
| RTX 4090 | 2.0秒 | 16.7分钟 | ~17分钟 |
| RTX 3090 | 3.0秒 | 25分钟 | ~26分钟 |

**性能提升**: 相比单GPU，速度提升约**6倍**！

## 自定义配置

### 修改GPU数量

如果你想用不同数量的GPU，编辑 `run_parallel_generation.sh`:

```bash
# 例如只用GPU 1-4
for gpu_id in {1..4}; do
    ...
done
```

记得相应修改 `NUM_GPUS` 变量。

### 修改总图像数

编辑 `run_parallel_generation.sh`:

```bash
TOTAL_IMAGES=5000  # 改为你需要的数量
```

### 使用不同的GPU编号

如果你的GPU不是1-6，而是0-5或其他编号：

```bash
# 使用GPU 0-5
for gpu_id in {0..5}; do
    ...
done

# 使用GPU 2,3,4,5,6,7
for gpu_id in {2..7}; do
    ...
done
```

### 性能优化

如果你的GPU是H100/H800，可以开启编译加速。编辑 `generate_diverse_avatars_parallel.py`:

```python
compile = True  # 第51行，改为True
```

然后使用Flash Attention 3：

```bash
ZIMAGE_ATTENTION=_flash_3 ./run_parallel_generation.sh
```

## 故障排查

### 1. 某个GPU出错了

查看日志：
```bash
cat logs/gpu_*.log | grep -i error
```

找到出错的GPU，单独重新运行：
```bash
CUDA_VISIBLE_DEVICES=3 python generate_diverse_avatars_parallel.py \
    --start_idx 1500 \
    --end_idx 2000 \
    --gpu_id 3
```

### 2. 显存不足

如果某个GPU显存不够：

1. 检查是否有其他程序占用显存：`nvidia-smi`
2. 降低分辨率（编辑脚本，改为 `height=768, width=768`）
3. 减少GPU数量，让每个GPU分配更少任务

### 3. 进程没有正常启动

检查：
```bash
# 查看运行中的Python进程
ps aux | grep generate_diverse_avatars_parallel

# 应该看到6个进程
```

### 4. 图像数量不对

生成完成后，检查：
```bash
ls avatars_output/*.png | wc -l
```

如果少于3000，查看日志找出哪些图像失败了，然后手动补充。

## 高级用法

### 断点续传

如果中途中断，不想重新生成已有的图像：

修改 `generate_diverse_avatars_parallel.py`，在生成前检查文件是否存在：

```python
# 在第94行附近添加
if output_path.exists():
    print(f"[GPU {args.gpu_id}] Skipping {output_path} (already exists)")
    continue
```

### 分阶段生成

如果不确定系统稳定性，可以分批生成：

```bash
# 第一批: 1500张 (GPU 1-6，每个250张)
TOTAL_IMAGES=1500 ./run_parallel_generation.sh

# 检查结果，确认无误后继续
# 第二批: 再生成1500张
# 修改脚本的start_idx范围...
```

### 不同风格的批次

如果想生成不同风格的头像批次：

1. 复制 `generate_diverse_avatars_parallel.py` 为 `generate_professional.py`
2. 修改提示词模板，强调专业风格
3. 运行不同的批次

## 输出结果

生成完成后：

```
avatars_output/
├── avatar_0000.png  # GPU 1 生成
├── avatar_0001.png  # GPU 1 生成
...
├── avatar_0500.png  # GPU 2 生成
...
├── avatar_2999.png  # GPU 6 生成

logs/
├── gpu_1.log
├── gpu_2.log
├── gpu_3.log
├── gpu_4.log
├── gpu_5.log
└── gpu_6.log
```

## 停止运行

如果需要中途停止：

```bash
# 按 Ctrl+C 停止脚本

# 或者杀死所有相关进程
pkill -f generate_diverse_avatars_parallel
```

## 验证结果

生成完成后，运行验证：

```bash
# 检查图像数量
total=$(ls avatars_output/*.png 2>/dev/null | wc -l)
echo "Generated: $total / 3000"

# 检查是否有损坏的图像
for img in avatars_output/*.png; do
    identify "$img" > /dev/null 2>&1 || echo "Corrupted: $img"
done
```

## 性能监控

在生成过程中，另开一个终端监控：

```bash
# 实时GPU利用率
watch -n 1 nvidia-smi

# 生成速度统计
watch -n 5 'ls avatars_output/*.png | wc -l'
```

理想情况下，6个GPU的利用率都应该接近100%。

## 总结

使用6个GPU并行生成的优势：

✓ **速度快**: 比单GPU快6倍
✓ **资源充分利用**: 所有GPU同时工作
✓ **可靠**: 即使某个GPU出错，其他GPU继续工作
✓ **灵活**: 可以轻松调整GPU数量和分配策略

预祝生成顺利！🚀
