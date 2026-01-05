#!/usr/bin/env python3
"""美食赛道 - 在单个GPU上生成图像"""

import os
import sys
import time
import argparse
import torch
from pathlib import Path
from diffusers import ZImagePipeline
from food_prompt_generator import FoodPromptGenerator


def generate_negative_prompt() -> str:
    """美食专用负面提示词"""
    return (
        "blurry, low quality, distorted, deformed, ugly, bad anatomy, "
        "bad proportions, watermark, text, cartoon, anime, drawing, "
        "artificial, oversaturated, multiple people in focus, "
        "drooling, saliva, dripping from mouth, wet mouth, liquid dripping, "
        "messy face, food on face, sauce on face, excessive liquid"
    )


def main():
    parser = argparse.ArgumentParser(description='美食赛道单GPU生成')
    parser.add_argument('--gpu', type=int, required=True, help='GPU ID (1-6)')
    parser.add_argument('--start-idx', type=int, required=True, help='起始图像索引')
    parser.add_argument('--num-images', type=int, required=True, help='生成图像数量')
    parser.add_argument('--output-dir', type=str, default='food_avatars_output', help='输出目录')
    parser.add_argument('--model-path', type=str, default='ckpts/Z-Image-Turbo', help='模型路径')
    parser.add_argument('--height', type=int, default=1024, help='图像高度')
    parser.add_argument('--width', type=int, default=1024, help='图像宽度')

    args = parser.parse_args()

    # 设置CUDA设备 - 直接使用指定的GPU编号
    device = torch.device(f'cuda:{args.gpu}')

    print(f"[GPU {args.gpu}] 美食赛道 - 开始初始化...")
    print(f"[GPU {args.gpu}] 将生成 {args.num_images} 张图像 (索引 {args.start_idx} 到 {args.start_idx + args.num_images - 1})")
    print(f"[GPU {args.gpu}] 使用设备: {device}")

    # 创建输出目录
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 初始化提示词生成器
    generator = FoodPromptGenerator(seed=42)

    try:
        # 加载模型
        print(f"[GPU {args.gpu}] 正在加载pipeline...")
        load_start = time.time()

        pipe = ZImagePipeline.from_pretrained(
            args.model_path,
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=False,
            trust_remote_code=True,
        )
        pipe = pipe.to(device)

        load_time = time.time() - load_start
        print(f"[GPU {args.gpu}] ✓ Pipeline加载完成 (耗时: {load_time:.2f}秒)")

        # 生成图像
        success_count = 0
        fail_count = 0
        total_time = 0
        negative_prompt = generate_negative_prompt()

        print(f"[GPU {args.gpu}] 开始生成图像...")
        print("=" * 80)

        for i in range(args.num_images):
            global_idx = args.start_idx + i

            try:
                # 生成提示词
                prompt = generator.generate_prompt(global_idx)

                # 生成图像
                start_time = time.time()

                with torch.no_grad():
                    image = pipe(
                        prompt=prompt,
                        negative_prompt=negative_prompt,
                        height=args.height,
                        width=args.width,
                        num_inference_steps=9,
                        guidance_scale=0.0,
                    ).images[0]

                generation_time = time.time() - start_time
                total_time += generation_time

                # 保存图像
                output_path = output_dir / f"food_avatar_{global_idx:05d}.png"
                image.save(output_path, format='PNG')

                success_count += 1

                # 每10张图片报告一次进度
                if (i + 1) % 10 == 0:
                    avg_time = total_time / success_count
                    remaining = args.num_images - (i + 1)
                    eta = remaining * avg_time / 60
                    print(f"[GPU {args.gpu}] 进度: {i+1}/{args.num_images} | "
                          f"成功: {success_count} | 失败: {fail_count} | "
                          f"平均: {avg_time:.2f}s/张 | 预计剩余: {eta:.1f}分钟")

            except Exception as e:
                fail_count += 1
                print(f"[GPU {args.gpu}] ✗ 图像 {global_idx} 生成失败: {str(e)}")
                continue

        # 最终统计
        print("=" * 80)
        print(f"[GPU {args.gpu}] ✓ 生成完成!")
        print(f"[GPU {args.gpu}]   成功: {success_count}/{args.num_images}")
        print(f"[GPU {args.gpu}]   失败: {fail_count}")
        if success_count > 0:
            print(f"[GPU {args.gpu}]   平均速度: {total_time/success_count:.2f}秒/张")
            print(f"[GPU {args.gpu}]   总耗时: {total_time/60:.1f}分钟")

    except Exception as e:
        print(f"[GPU {args.gpu}] ✗ 发生错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
