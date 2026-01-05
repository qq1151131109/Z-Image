#!/bin/bash
# 多线程下载Z-Image-Turbo模型

echo "==================================================================="
echo "多线程下载 Z-Image-Turbo 模型"
echo "==================================================================="
echo ""

# 检查git-lfs是否安装
if ! command -v git-lfs &> /dev/null; then
    echo "正在安装 git-lfs..."
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
    sudo apt-get install git-lfs -y
    git lfs install
else
    echo "✓ git-lfs 已安装"
    git lfs install
fi

# 配置git-lfs使用多线程
echo ""
echo "配置多线程下载..."
git config --global lfs.concurrenttransfers 16  # 16个并发连接
git config --global lfs.transfer.maxretries 10   # 最大重试10次
git config --global http.postBuffer 524288000    # 500MB缓冲

echo "✓ 并发连接数: 16"
echo "✓ 最大重试次数: 10"
echo ""

# 清理之前的下载
TARGET_DIR="ckpts/Tongyi-MAI/Z-Image-Turbo"
if [ -d "$TARGET_DIR" ]; then
    echo "清理之前的下载..."
    rm -rf "$TARGET_DIR"
fi

# 创建目录
mkdir -p ckpts/Tongyi-MAI
cd ckpts/Tongyi-MAI

echo "开始从 ModelScope 下载..."
echo "URL: https://www.modelscope.cn/Tongyi-MAI/Z-Image-Turbo.git"
echo ""

# 使用git clone with LFS
GIT_LFS_SKIP_SMUDGE=0 git clone \
    --progress \
    https://www.modelscope.cn/Tongyi-MAI/Z-Image-Turbo.git

cd ../..

echo ""
echo "==================================================================="
echo "检查下载结果..."
echo "==================================================================="

if [ -d "$TARGET_DIR" ]; then
    echo "✓ 下载完成！"
    echo ""
    echo "目录大小:"
    du -sh "$TARGET_DIR"
    echo ""
    echo "主要文件:"
    ls -lh "$TARGET_DIR"/transformer/*.safetensors 2>/dev/null | head -3
    ls -lh "$TARGET_DIR"/text_encoder/*.safetensors 2>/dev/null | head -3
    ls -lh "$TARGET_DIR"/vae/*.safetensors 2>/dev/null
    echo ""
    echo "==================================================================="
    echo "✓ 模型已就绪！现在可以运行："
    echo "   python test_20_avatars.py"
    echo "==================================================================="
else
    echo "✗ 下载失败"
    exit 1
fi
