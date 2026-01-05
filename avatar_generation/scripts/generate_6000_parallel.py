#!/usr/bin/env python3
"""
并行生成6000张多样化美国女性头像
使用GPU 1-6并行处理，每个GPU生成1000张图像
"""

import os
import sys
import time
import torch
from pathlib import Path
import multiprocessing
from PIL import Image
from diverse_prompt_generator import DiversePromptGenerator

# 必须在导入CUDA相关模块前设置multiprocessing启动方法
multiprocessing.set_start_method('spawn', force=True)

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from diffusers import ZImagePipeline


def generate_images_on_gpu(
    gpu_id: int,
    start_idx: int,
    num_images: int,
    output_dir: str,
    model_path: str = "ckpts/Tongyi-MAI/Z-Image-Turbo",
    height: int = 1024,
    width: int = 1024,
):
    """
    在指定GPU上生成图像

    Args:
        gpu_id: CUDA设备ID (1-6)
        start_idx: 起始图像索引
        num_images: 要生成的图像数量
        output_dir: 输出目录
        model_path: 模型路径
        height: 图像高度
        width: 图像宽度
    """
    # 设置CUDA设备
    os.environ['CUDA_VISIBLE_DEVICES'] = str(gpu_id)
    device = torch.device('cuda:0')  # 因为CUDA_VISIBLE_DEVICES已设置，所以这里用cuda:0

    print(f"[GPU {gpu_id}] 开始初始化...")
    print(f"[GPU {gpu_id}] 将生成 {num_images} 张图像 (索引 {start_idx} 到 {start_idx + num_images - 1})")

    # 创建输出目录
    gpu_output_dir = Path(output_dir) / f"gpu_{gpu_id}"
    gpu_output_dir.mkdir(parents=True, exist_ok=True)

    # 初始化提示词生成器
    # 使用不同的随机种子确保每个GPU生成的内容不同
    generator = DiversePromptGenerator(seed=42 + gpu_id * 10000)

    try:
        # 加载模型
        print(f"[GPU {gpu_id}] 正在加载pipeline...")
        pipe = ZImagePipeline.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=False,
            trust_remote_code=True,
        )
        pipe = pipe.to(device)
        print(f"[GPU {gpu_id}] ✓ Pipeline加载完成")

        # 生成图像
        success_count = 0
        fail_count = 0
        total_time = 0

        print(f"[GPU {gpu_id}] 开始生成图像...")
        print("=" * 80)

        for i in range(num_images):
            global_idx = start_idx + i

            try:
                # 生成提示词
                prompt = generator.generate_prompt(global_idx)

                # 生成图像
                start_time = time.time()

                with torch.no_grad():
                    image = pipe(
                        prompt=prompt,
                        height=height,
                        width=width,
                        num_inference_steps=9,
                        guidance_scale=0.0,
                    ).images[0]

                generation_time = time.time() - start_time
                total_time += generation_time

                # 保存图像
                output_path = gpu_output_dir / f"avatar_{global_idx:05d}.png"
                image.save(output_path, format='PNG')

                success_count += 1

                # 打印进度
                if (i + 1) % 50 == 0 or i == 0:
                    avg_time = total_time / success_count if success_count > 0 else 0
                    progress = (i + 1) / num_images * 100
                    print(f"[GPU {gpu_id}] 进度: {i+1}/{num_images} ({progress:.1f}%) | "
                          f"平均速度: {avg_time:.2f}秒/张 | "
                          f"成功: {success_count} | 失败: {fail_count}")

            except Exception as e:
                fail_count += 1
                print(f"[GPU {gpu_id}] ✗ 图像 {global_idx} 生成失败: {e}")
                continue

        # 打印统计信息
        print("=" * 80)
        print(f"[GPU {gpu_id}] ✓ 生成完成!")
        print(f"[GPU {gpu_id}] 成功生成: {success_count}/{num_images} 张")
        print(f"[GPU {gpu_id}] 失败: {fail_count} 张")
        if success_count > 0:
            avg_time = total_time / success_count
            print(f"[GPU {gpu_id}] 平均速度: {avg_time:.2f} 秒/张")
            print(f"[GPU {gpu_id}] 总耗时: {total_time/60:.2f} 分钟")
        print(f"[GPU {gpu_id}] 输出目录: {gpu_output_dir}")
        print("=" * 80)

    except Exception as e:
        print(f"[GPU {gpu_id}] ✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()


def main():
    """主函数：启动6个并行进程在GPU 1-6上生成图像"""

    # 配置参数
    TOTAL_IMAGES = 6000
    NUM_GPUS = 6
    GPU_IDS = [1, 2, 3, 4, 5, 6]  # 使用GPU 1-6
    IMAGES_PER_GPU = TOTAL_IMAGES // NUM_GPUS  # 每个GPU生成1000张

    OUTPUT_DIR = "/mnt/shenglin/Z-Image/avatars_6000"
    MODEL_PATH = "ckpts/Tongyi-MAI/Z-Image-Turbo"
    HEIGHT = 1024
    WIDTH = 1024

    print("=" * 80)
    print("并行生成6000张多样化美国女性头像")
    print("=" * 80)
    print(f"总图像数: {TOTAL_IMAGES}")
    print(f"使用GPU: {GPU_IDS}")
    print(f"每GPU图像数: {IMAGES_PER_GPU}")
    print(f"分辨率: {HEIGHT}x{WIDTH}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"模型路径: {MODEL_PATH}")
    print("=" * 80)
    print()

    # 创建输出目录
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # 启动并行进程
    processes = []

    print("正在启动并行进程...")
    for i, gpu_id in enumerate(GPU_IDS):
        start_idx = i * IMAGES_PER_GPU

        p = multiprocessing.Process(
            target=generate_images_on_gpu,
            args=(
                gpu_id,
                start_idx,
                IMAGES_PER_GPU,
                OUTPUT_DIR,
                MODEL_PATH,
                HEIGHT,
                WIDTH,
            )
        )
        p.start()
        processes.append(p)
        print(f"✓ 进程 {i+1}/6 已启动 (GPU {gpu_id}, 图像 {start_idx}-{start_idx + IMAGES_PER_GPU - 1})")

    print()
    print("所有进程已启动！等待完成...")
    print("=" * 80)
    print()

    # 等待所有进程完成
    start_time = time.time()

    for i, p in enumerate(processes):
        p.join()
        print(f"✓ 进程 {i+1}/6 已完成 (GPU {GPU_IDS[i]})")

    total_time = time.time() - start_time

    # 打印最终统计
    print()
    print("=" * 80)
    print("✓ 所有进程完成!")
    print("=" * 80)
    print(f"总耗时: {total_time/60:.2f} 分钟 ({total_time/3600:.2f} 小时)")
    print(f"输出目录: {OUTPUT_DIR}")
    print()

    # 统计生成的图像数量
    total_generated = 0
    for gpu_id in GPU_IDS:
        gpu_dir = Path(OUTPUT_DIR) / f"gpu_{gpu_id}"
        if gpu_dir.exists():
            count = len(list(gpu_dir.glob("*.png")))
            total_generated += count
            print(f"  GPU {gpu_id}: {count} 张图像")

    print()
    print(f"总计生成: {total_generated}/{TOTAL_IMAGES} 张图像")
    print(f"成功率: {total_generated/TOTAL_IMAGES*100:.1f}%")
    print("=" * 80)


if __name__ == "__main__":
    main()
