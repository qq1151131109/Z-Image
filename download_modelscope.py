"""从ModelScope下载Z-Image-Turbo模型"""

import os
from pathlib import Path

print("=" * 80)
print("从 ModelScope 下载 Z-Image-Turbo 模型")
print("=" * 80)
print()

# 检查并安装modelscope
try:
    from modelscope import snapshot_download
    print("✓ modelscope 已安装")
except ImportError:
    print("正在安装 modelscope...")
    import subprocess
    subprocess.check_call(["pip", "install", "modelscope", "-q"])
    from modelscope import snapshot_download
    print("✓ modelscope 安装完成")

# 配置
model_id = "Tongyi-MAI/Z-Image-Turbo"
target_dir = Path("ckpts/Z-Image-Turbo")

print(f"\n模型ID: {model_id}")
print(f"目标目录: {target_dir}")
print()

# 确保目录存在
target_dir.parent.mkdir(parents=True, exist_ok=True)

try:
    print("开始下载...（这可能需要一些时间，模型约13GB）")
    print()

    # 下载模型
    model_path = snapshot_download(
        model_id,
        cache_dir="ckpts",
        revision='master'
    )

    print()
    print("=" * 80)
    print("✓ 下载完成！")
    print("=" * 80)
    print(f"模型路径: {model_path}")

    # 显示下载的文件
    if Path(model_path).exists():
        import subprocess
        size = subprocess.check_output(["du", "-sh", model_path]).decode().split()[0]
        print(f"目录大小: {size}")

        # 列出主要文件
        print("\n主要模型文件：")
        for subdir in ["transformer", "text_encoder", "vae"]:
            subdir_path = Path(model_path) / subdir
            if subdir_path.exists():
                safetensors = list(subdir_path.glob("*.safetensors"))
                if safetensors:
                    print(f"\n  {subdir}/:")
                    for f in safetensors[:3]:  # 只显示前3个
                        size_bytes = f.stat().st_size
                        size_mb = size_bytes / (1024 * 1024)
                        print(f"    - {f.name} ({size_mb:.1f} MB)")

    print()
    print("=" * 80)
    print("✓ 模型准备就绪！")
    print()
    print("现在可以运行：")
    print("  python test_20_avatars.py          # 测试生成20张")
    print("  ./run_parallel_generation.sh       # 6GPU并行生成3000张")
    print("=" * 80)

except Exception as e:
    print()
    print("=" * 80)
    print(f"✗ 下载失败: {e}")
    print("=" * 80)
    print()
    print("备选方案：")
    print()
    print("1. 浏览器访问: https://modelscope.cn/models/Tongyi-MAI/Z-Image-Turbo")
    print("2. 点击「文件」标签")
    print("3. 点击右上角「下载模型」按钮")
    print("4. 下载完成后解压到: ckpts/Z-Image-Turbo/")
    print()
    print("或者使用git-lfs下载：")
    print("  cd ckpts/")
    print("  git lfs install")
    print("  git clone https://www.modelscope.cn/Tongyi-MAI/Z-Image-Turbo.git")
    print()
