#!/bin/bash
# Z-Image LoRA 依赖安装脚本

set -e  # 出错时退出

echo "========================================"
echo "Z-Image LoRA 依赖安装脚本"
echo "========================================"
echo ""

# 检测 CUDA 是否可用
if command -v nvidia-smi &> /dev/null; then
    echo "✓ 检测到 NVIDIA GPU"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
    echo ""

    # 询问是否安装 CUDA 版本的 PyTorch
    read -p "是否安装 CUDA 版本的 PyTorch? (y/n, 默认 y): " install_cuda
    install_cuda=${install_cuda:-y}
else
    echo "⚠ 未检测到 NVIDIA GPU，将安装 CPU 版本的 PyTorch"
    install_cuda="n"
fi

echo ""
echo "开始安装依赖..."
echo ""

# 激活虚拟环境（如果存在）
if [ -d ".venv" ]; then
    echo "激活虚拟环境..."
    source .venv/bin/activate
fi

# 升级 pip
echo "升级 pip..."
pip install --upgrade pip

# 安装 PyTorch
if [ "$install_cuda" = "y" ] || [ "$install_cuda" = "Y" ]; then
    echo ""
    echo "安装 CUDA 版本的 PyTorch..."
    # 安装 PyTorch 2.5.0+ with CUDA 12.1
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
else
    echo ""
    echo "安装 CPU 版本的 PyTorch..."
    pip install torch torchvision
fi

# 从源码安装最新的 diffusers（包含 Z-Image 支持）
echo ""
echo "从源码安装最新版 Diffusers..."
pip install git+https://github.com/huggingface/diffusers

# 安装项目依赖
echo ""
echo "安装项目依赖..."
pip install -e .

# 验证安装
echo ""
echo "========================================"
echo "验证安装..."
echo "========================================"

# 检查 PyTorch
python -c "import torch; print(f'✓ PyTorch {torch.__version__} installed')"
python -c "import torch; print(f'✓ CUDA available: {torch.cuda.is_available()}')"
if python -c "import torch; exit(0 if torch.cuda.is_available() else 1)" 2>/dev/null; then
    python -c "import torch; print(f'✓ CUDA version: {torch.version.cuda}')"
    python -c "import torch; print(f'✓ GPU: {torch.cuda.get_device_name(0)}')"
fi

# 检查 Diffusers
python -c "import diffusers; print(f'✓ Diffusers {diffusers.__version__} installed')"

# 检查 ZImagePipeline
python -c "from diffusers import ZImagePipeline; print('✓ ZImagePipeline available')"

# 检查 PEFT
python -c "import peft; print(f'✓ PEFT {peft.__version__} installed')"

# 检查其他依赖
python -c "import transformers; print(f'✓ Transformers {transformers.__version__} installed')"
python -c "import accelerate; print(f'✓ Accelerate {accelerate.__version__} installed')"

echo ""
echo "========================================"
echo "✓ 所有依赖安装成功！"
echo "========================================"
echo ""
echo "接下来你可以："
echo "1. 运行基础推理（不使用 LoRA）："
echo "   python inference_lora.py --prompt \"Your prompt here\""
echo ""
echo "2. 使用 LoRA 推理："
echo "   python inference_lora.py --lora_path ./path/to/lora --prompt \"Your prompt here\""
echo ""
echo "3. 查看完整使用指南："
echo "   cat LORA_GUIDE.md"
echo ""
