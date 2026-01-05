#!/bin/bash
# 从ModelScope下载Z-Image-Turbo模型

echo "==================================================================="
echo "从 ModelScope 下载 Z-Image-Turbo 模型"
echo "==================================================================="
echo ""

# 检查是否安装了modelscope
if ! python -c "import modelscope" 2>/dev/null; then
    echo "正在安装 modelscope..."
    pip install modelscope -q
fi

# 目标目录
TARGET_DIR="ckpts/Z-Image-Turbo"

echo "下载目标: $TARGET_DIR"
echo "模型ID: Tongyi-MAI/Z-Image-Turbo"
echo ""

# 使用Python下载
python << 'EOF'
from modelscope import snapshot_download
import os

model_id = "Tongyi-MAI/Z-Image-Turbo"
target_dir = "ckpts/Z-Image-Turbo"

print(f"开始下载模型: {model_id}")
print(f"目标目录: {target_dir}")
print("")

try:
    # 下载模型
    model_dir = snapshot_download(
        model_id,
        cache_dir=os.path.dirname(target_dir),
        revision='master'
    )

    print(f"\n✓ 下载完成！")
    print(f"模型路径: {model_dir}")

except Exception as e:
    print(f"\n✗ 下载失败: {e}")
    print("\n备选方案：")
    print("1. 检查网络连接")
    print("2. 访问 https://modelscope.cn/models/Tongyi-MAI/Z-Image-Turbo")
    print("3. 手动下载并解压到 ckpts/Z-Image-Turbo/")
    exit(1)

EOF

echo ""
echo "==================================================================="
echo "检查下载结果..."
echo "==================================================================="

# 检查下载的文件
if [ -d "$TARGET_DIR" ]; then
    echo "✓ 目录存在: $TARGET_DIR"
    echo "目录大小: $(du -sh $TARGET_DIR | cut -f1)"
    echo ""
    echo "主要文件："
    ls -lh $TARGET_DIR/transformer/*.safetensors 2>/dev/null | head -5
    ls -lh $TARGET_DIR/text_encoder/*.safetensors 2>/dev/null | head -3
    ls -lh $TARGET_DIR/vae/*.safetensors 2>/dev/null
else
    echo "✗ 目录不存在，下载可能失败"
    exit 1
fi

echo ""
echo "==================================================================="
echo "✓ 模型准备就绪！现在可以运行："
echo "   python test_20_avatars.py"
echo "==================================================================="
