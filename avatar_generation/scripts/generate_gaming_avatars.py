"""生成大批量多样化游戏玩家社媒头像"""

import os
import time
from pathlib import Path

import torch
from tqdm import tqdm
from diffusers import ZImagePipeline

from gaming_prompt_generator import GamingPromptGenerator


def generate_negative_prompt() -> str:
    """通用的负面提示词，用于避免不良输出"""
    return (
        "blurry, low quality, distorted, deformed, ugly, bad anatomy, "
        "bad proportions, watermark, text, cartoon, anime, drawing, "
        "artificial, oversaturated, multiple people in focus"
    )


def select_device() -> str:
    """选择最佳可用设备"""
    if torch.cuda.is_available():
        print("Chosen device: cuda")
        return "cuda"
    try:
        import torch_xla.core.xla_model as xm
        device = xm.xla_device()
        print("Chosen device: tpu")
        return device
    except (ImportError, RuntimeError):
        if torch.backends.mps.is_available():
            print("Chosen device: mps")
            return "mps"
        print("Chosen device: cpu")
        return "cpu"


def main():
    # ==================== 配置参数 ====================

    # 生成数量（默认4000张，可根据需要调整）
    NUM_IMAGES = 4000

    # 模型配置
    model_path = "ckpts/Z-Image-Turbo"

    # 图像配置（社媒头像标准）
    height = 1024
    width = 1024

    # 生成参数（Z-Image-Turbo推荐设置）
    num_inference_steps = 9
    guidance_scale = 0.0  # Turbo模型使用0.0

    # 输出目录
    output_dir = Path("gaming_avatars_output")
    output_dir.mkdir(exist_ok=True)

    # ==================== 初始化 ====================

    print("=" * 80)
    print("游戏赛道头像批量生成")
    print("=" * 80)
    print(f"目标数量: {NUM_IMAGES} 张")
    print(f"输出目录: {output_dir.absolute()}")
    print(f"图像尺寸: {width}x{height}")
    print("=" * 80)

    # 初始化提示词生成器
    print("\n初始化游戏提示词生成器...")
    prompt_generator = GamingPromptGenerator(seed=42)

    # 负面提示词
    negative_prompt = generate_negative_prompt()

    # 初始化设备
    device = select_device()

    # 加载模型 - 使用diffusers pipeline
    print("\n加载 Z-Image-Turbo pipeline...")
    load_start = time.time()

    pipe = ZImagePipeline.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=False,
        trust_remote_code=True,
    )
    pipe = pipe.to(device)

    load_time = time.time() - load_start
    print(f"✓ Pipeline加载完成 (耗时: {load_time:.2f}秒)")

    # ==================== 开始生成 ====================

    print(f"\n开始生成 {NUM_IMAGES} 张游戏头像...")
    print("=" * 80)

    total_time = 0
    success_count = 0
    error_count = 0

    for i in tqdm(range(NUM_IMAGES), desc="生成游戏头像"):
        try:
            # 生成多样化的提示词
            prompt = prompt_generator.generate_prompt(i)

            # 使用不同的随机种子确保多样性
            seed = 42 + i
            generator = torch.Generator(device).manual_seed(seed)

            # 输出文件名
            output_path = output_dir / f"gaming_avatar_{i:05d}.png"

            # 生成图像 - 使用torch.no_grad()节省显存
            start_time = time.time()

            with torch.no_grad():
                image = pipe(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    height=height,
                    width=width,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    generator=generator,
                ).images[0]

            elapsed = time.time() - start_time
            total_time += elapsed

            # 保存图像
            image.save(output_path, format='PNG')
            success_count += 1

            # 每100张打印一次进度信息
            if (i + 1) % 100 == 0:
                avg_time = total_time / success_count
                eta = avg_time * (NUM_IMAGES - i - 1)
                print(f"\n[{i+1}/{NUM_IMAGES}] 成功: {success_count}, 失败: {error_count}")
                print(f"  平均速度: {avg_time:.2f}秒/张")
                print(f"  预计剩余时间: {eta/60:.1f} 分钟")

        except Exception as e:
            print(f"\n生成第 {i} 张图像时出错: {e}")
            error_count += 1
            continue

    # ==================== 生成完成统计 ====================

    print("\n" + "=" * 80)
    print("✓ 生成完成!")
    print("=" * 80)
    print(f"  成功生成: {success_count} 张")
    print(f"  失败: {error_count} 张")
    if success_count > 0:
        print(f"  总耗时: {total_time/60:.1f} 分钟")
        print(f"  平均速度: {total_time/success_count:.2f} 秒/张")
    print(f"  输出目录: {output_dir.absolute()}")
    print("=" * 80)

    # 显示一些示例提示词
    print("\n示例提示词（前5张）:")
    print("-" * 80)
    for i in range(min(5, NUM_IMAGES)):
        prompt = prompt_generator.generate_prompt(i)
        print(f"\n[{i}] {prompt[:150]}...")


if __name__ == "__main__":
    main()
