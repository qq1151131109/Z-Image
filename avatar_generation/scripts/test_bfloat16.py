"""测试使用bfloat16 - 官方推荐配置 + 多样化提示词生成"""

import os
import time
from pathlib import Path

import torch
from diffusers import ZImagePipeline
from tqdm import tqdm

# 导入提示词生成器
from diverse_prompt_generator import DiversePromptGenerator

# 测试配置
NUM_IMAGES = 20
MODEL_PATH = "ckpts/Tongyi-MAI/Z-Image-Turbo"
OUTPUT_DIR = Path("test_avatars_diverse")
OUTPUT_DIR.mkdir(exist_ok=True)

# 1024x1024配置（官方推荐）
HEIGHT = 1024
WIDTH = 1024
NUM_INFERENCE_STEPS = 9
GUIDANCE_SCALE = 0.0

# 创建提示词生成器
prompt_generator = DiversePromptGenerator(seed=42)


def generate_diverse_prompt(index: int) -> str:
    """使用生成器创建多样化提示词"""
    return prompt_generator.generate_prompt(index)


def main():
    print("=" * 80)
    print("测试bfloat16 - 多样化美国女性头像生成")
    print("=" * 80)

    # 选择设备
    if torch.cuda.is_available():
        device = "cuda"
        print(f"✓ 使用设备: {device}")
        print(f"✓ GPU: {torch.cuda.get_device_name(0)}")
    else:
        device = "cpu"
        print(f"✓ 使用设备: CPU")

    # 加载pipeline - 使用官方推荐的bfloat16配置
    print(f"\n正在加载pipeline从: {MODEL_PATH}")
    print("✓ 使用官方推荐配置: torch.bfloat16 + low_cpu_mem_usage=False")
    load_start = time.time()

    # 完全按照README.md示例配置
    pipe = ZImagePipeline.from_pretrained(
        MODEL_PATH,
        torch_dtype=torch.bfloat16,  # 官方推荐
        low_cpu_mem_usage=False,     # 官方示例中的配置
        trust_remote_code=True,
    )
    pipe.to(device)

    load_time = time.time() - load_start
    print(f"✓ Pipeline加载完成 (耗时: {load_time:.2f}秒)")

    # 不使用CPU offload - 测试在24GB VRAM上是否能直接运行
    print("\n测试配置:")
    print("  - dtype: bfloat16")
    print("  - CPU offload: 关闭")
    print("  - 分辨率: 1024x1024")
    print("  - 提示词: 动态生成（美国女性，30%烟熏妆，40%丰满身材，25%纹身）")
    print("  - 场景: 8种生活化场景随机组合")

    # 生成图像
    print(f"\n开始生成 {NUM_IMAGES} 张图像 ({HEIGHT}x{WIDTH})...")
    print("=" * 80)

    generation_times = []
    success_count = 0

    for i in tqdm(range(NUM_IMAGES), desc="生成进度"):
        prompt = generate_diverse_prompt(i)
        seed = 42 + i
        generator = torch.Generator(device).manual_seed(seed)
        output_path = OUTPUT_DIR / f"test_avatar_{i:02d}.png"

        try:
            start_time = time.time()

            images = pipe(
                prompt=prompt,
                height=HEIGHT,
                width=WIDTH,
                num_inference_steps=NUM_INFERENCE_STEPS,
                guidance_scale=GUIDANCE_SCALE,
                generator=generator,
            ).images

            elapsed = time.time() - start_time
            generation_times.append(elapsed)

            # 保存图像
            images[0].save(output_path)
            success_count += 1

            # 打印前3张的提示词
            if i < 3:
                print(f"\n[图像 {i}] 生成成功")
                print(f"  提示词: {prompt[:80]}...")
                print(f"  生成时间: {elapsed:.2f}秒")

        except Exception as e:
            print(f"\n✗ 错误 (图像 {i}): {e}")
            continue

    # 统计
    print("\n" + "=" * 80)
    print("✓ 生成完成!")
    print("=" * 80)

    if generation_times:
        avg_time = sum(generation_times) / len(generation_times)
        min_time = min(generation_times)
        max_time = max(generation_times)
        total_time = sum(generation_times)

        print(f"\n📊 性能统计:")
        print(f"  成功生成: {success_count}/{NUM_IMAGES} 张")
        print(f"  总耗时: {total_time:.2f} 秒 ({total_time/60:.2f} 分钟)")
        print(f"  平均速度: {avg_time:.2f} 秒/张")
        print(f"  最快: {min_time:.2f} 秒")
        print(f"  最慢: {max_time:.2f} 秒")

        # 预估3000张的时间
        estimated_3000 = avg_time * 3000
        print(f"\n📈 预估生成3000张所需时间:")
        print(f"  单GPU: {estimated_3000/60:.1f} 分钟 ({estimated_3000/3600:.2f} 小时)")
        print(f"  6个GPU并行: {estimated_3000/60/6:.1f} 分钟 ({estimated_3000/3600/6:.2f} 小时)")

    print(f"\n📁 输出目录: {OUTPUT_DIR.absolute()}")
    print(f"   查看图像: ls {OUTPUT_DIR}/")
    print("=" * 80)


if __name__ == "__main__":
    main()
