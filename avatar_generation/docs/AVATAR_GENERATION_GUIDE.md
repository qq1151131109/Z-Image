# 生成3000张多样化美国女性社媒头像

## 方案说明

这个方案通过**系统性地变化提示词的多个维度**来确保生成的3000张头像具有高度多样性。

### 多样性维度（共9个维度）

1. **族裔** (7种): Caucasian, African American, Hispanic, Asian American, Mixed race, Native American, Middle Eastern
2. **年龄段** (6种): 20岁初期, 20岁中期, 20岁晚期, 30岁初期, 30岁中期, 40多岁
3. **发型** (10种): 长直发, 长波浪发, 长卷发, 齐肩发, 波波头, 精灵短发, 盘发, 编发, 马尾, 凌乱发髻
4. **发色** (8种): 金发, 棕发, 黑发, 赤褐色, 红发, 深棕, 浅棕, 挑染
5. **表情** (8种): 温暖微笑, 温柔微笑, 自信微笑, 友好表情, 专业表情, 自然表情, 浅笑, 明亮微笑
6. **服装** (7种): 休闲T恤, 商务休闲衬衫, 专业西装, 毛衣, 正装衬衫, 休闲上衣, 时尚装束
7. **背景** (8种): 柔和虚化背景, 中性灰背景, 白色背景, 户外虚化背景, 散景背景, 暖色调背景, 冷色调背景, 极简背景
8. **光照** (7种): 柔和自然光, 影棚光, 黄金时段光, 柔和漫射光, 专业肖像光, 自然窗户光, 明亮均匀光
9. **拍摄角度** (4种): 正面, 轻微角度, 四分之三侧面, 稍微俯视

**理论组合数**: 7 × 6 × 10 × 8 × 8 × 7 × 8 × 7 × 4 = **7,526,400,000** 种组合

所以生成3000张完全不重复的图像绰绰有余！

## 快速开始

### 方法1: 直接运行（推荐）

```bash
# 安装依赖（如果还没安装）
pip install -e .
pip install tqdm  # 进度条

# 直接运行，生成3000张图
python generate_diverse_avatars.py
```

生成的图像会保存在 `avatars_output/` 目录下，命名为 `avatar_0000.png` 到 `avatar_2999.png`。

### 方法2: 使用配置文件

```bash
# 1. 编辑配置文件
nano avatar_config.sh  # 修改参数，比如图像数量、尺寸等

# 2. 加载配置并运行
source avatar_config.sh && python generate_diverse_avatars.py
```

## 性能预估

根据你的GPU配置，预估时间如下：

| GPU型号 | 单张耗时 | 3000张总耗时 | 优化建议 |
|---------|---------|-------------|----------|
| H100/H800 | ~0.8秒 | ~40分钟 | 开启compile，使用_flash_3 |
| A100 | ~1.5秒 | ~75分钟 | 使用flash backend |
| RTX 4090 | ~2.0秒 | ~100分钟 | 默认配置即可 |
| RTX 3090 | ~3.0秒 | ~150分钟 | 默认配置即可 |
| RTX 3060 (12GB) | ~5.0秒 | ~250分钟 | 启用CPU offload |

## 高级配置

### 1. 修改图像尺寸（适配不同平台）

编辑 `generate_diverse_avatars.py`:

```python
# Instagram/Twitter 正方形头像
height = 1024
width = 1024

# LinkedIn 竖版头像
height = 1344
width = 896

# Facebook 横版头像
height = 896
width = 1344
```

### 2. 调整生成数量

编辑 `generate_diverse_avatars.py`:

```python
NUM_IMAGES = 3000  # 改为你需要的数量
```

### 3. 性能优化（H100/H800 GPU）

编辑 `generate_diverse_avatars.py`:

```python
compile = True  # 开启编译（首次慢，后续快）
attn_backend = "_flash_3"  # 使用Flash Attention 3
```

然后运行:
```bash
ZIMAGE_ATTENTION=_flash_3 python generate_diverse_avatars.py
```

### 4. 低显存优化（8GB-16GB显存）

如果遇到显存不足，可以降低分辨率或使用CPU offload（需要修改脚本使用diffusers的pipeline）。

## 查看生成进度

脚本会显示实时进度：

```
Generating avatars: 45%|████████▌         | 1350/3000 [22:30<25:00,  1.1it/s]

[1400/3000] Avg time: 2.15s/image, ETA: 57.3 min
```

每100张会打印一次平均速度和预计剩余时间。

## 输出结果

生成完成后：

```
avatars_output/
├── avatar_0000.png
├── avatar_0001.png
├── avatar_0002.png
...
└── avatar_2999.png
```

每张图都会有不同的：
- 族裔和肤色
- 年龄外观
- 发型和发色
- 面部表情
- 服装风格
- 背景和光照
- 拍摄角度

## 自定义提示词维度

如果你想进一步定制，可以编辑 `generate_diverse_avatars.py` 中的列表：

```python
# 添加更多发型
HAIR_STYLES = [
    "long straight hair",
    "long wavy hair",
    # ... 添加你自己的选项
    "afro hairstyle",  # 新增
    "dreadlocks",      # 新增
]

# 添加更多服装风格
CLOTHING_STYLES = [
    "casual t-shirt",
    # ...
    "leather jacket",  # 新增
    "hoodie",          # 新增
]
```

## 批量处理技巧

### 分批生成（避免长时间运行）

如果担心中途中断，可以分批运行：

```bash
# 第一批: 0-999
python generate_diverse_avatars.py  # 修改 NUM_IMAGES=1000

# 第二批: 1000-1999
# 修改脚本中的 range(1000, 2000) 和输出文件名

# 第三批: 2000-2999
# 修改脚本中的 range(2000, 3000) 和输出文件名
```

### 并行生成（多GPU）

如果有多张GPU，可以同时运行多个实例：

```bash
# GPU 0: 生成 0-999
CUDA_VISIBLE_DEVICES=0 python generate_diverse_avatars.py &

# GPU 1: 生成 1000-1999
CUDA_VISIBLE_DEVICES=1 python generate_diverse_avatars.py &

# 等等...
```

## 质量检查

生成完成后，建议：

1. 随机抽查100-200张，确保质量和多样性
2. 删除任何质量不佳的图像
3. 如需要，对特定图像重新生成（调整seed）

## 常见问题

### Q: 生成的图像不够多样化？

A: 检查是否正确使用了随机种子。脚本使用 `seed = 42 + i` 确保每张图都不同。

### Q: 显存不足 (OOM) ？

A: 尝试：
1. 降低分辨率到 768x768
2. 使用 float16 而非 bfloat16
3. 使用diffusers的CPU offload功能

### Q: 生成速度太慢？

A:
1. 确保使用了正确的attention backend
2. 如果是H100/H800，开启compile
3. 检查GPU利用率（应该接近100%）

### Q: 如何确保符合美国审美？

A: 提示词已经包含"professional photography, high quality"等关键词。如需调整，可以修改 `generate_diverse_prompt()` 函数中的提示词模板。

## 进一步优化建议

1. **使用LoRA微调**: 如果有特定风格需求（如特定公司的品牌风格），可以训练一个LoRA
2. **后处理**: 可以用脚本批量调整亮度、对比度、裁剪等
3. **人脸检测**: 使用OpenCV或face_recognition库自动筛选出人脸居中、清晰的图像
4. **去重**: 使用图像哈希算法检测并删除可能的重复图像

## 预计资源消耗

- **磁盘空间**: 每张图约2-4MB，3000张约6-12GB
- **显存**: 16GB（推荐）或 8GB（需优化）
- **时间**: 40分钟 - 4小时（取决于GPU）

## 总结

这个方案的优势：

✓ **高度多样性**: 9个维度组合，保证每张图都独特
✓ **可重现**: 使用固定随机种子，可以重新生成特定图像
✓ **高效**: 利用批处理和GPU加速
✓ **可定制**: 所有参数都可以轻松修改
✓ **专业质量**: 使用Z-Image-Turbo模型，质量有保证

祝你生成顺利！🎉
