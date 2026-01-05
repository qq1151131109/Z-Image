#!/usr/bin/env python3
"""
使用Z-Image + LoRA在单个GPU上批量生成图像
支持多个LoRA配置，每个LoRA都会生成所有提示词对应的图像
"""

import os
import sys
import time
import json
import argparse
import csv
from pathlib import Path

import torch
from diffusers import ZImagePipeline


def parse_args():
    parser = argparse.ArgumentParser(description='使用Z-Image + LoRA在单个GPU上批量生成图像')
    parser.add_argument('--gpu', type=int, required=True, help='GPU ID (0-7)')
    parser.add_argument('--prompts-csv', type=str, required=True, help='提示词CSV文件路径')
    parser.add_argument('--lora-config', type=str, required=True, help='LoRA配置文件路径 (JSON)')
    parser.add_argument('--start-idx', type=int, required=True, help='起始提示词索引')
    parser.add_argument('--num-prompts', type=int, required=True, help='处理提示词数量')
    parser.add_argument('--output-dir', type=str, required=True, help='输出目录')
    parser.add_argument('--model-path', type=str, default='ckpts/Tongyi-MAI/Z-Image-Turbo',
                        help='Z-Image模型路径')
    parser.add_argument('--height', type=int, default=1024, help='图像高度')
    parser.add_argument('--width', type=int, default=1024, help='图像宽度')
    parser.add_argument('--num-inference-steps', type=int, default=9, help='推理步数')
    parser.add_argument('--guidance-scale', type=float, default=0.0, help='Guidance scale')
    parser.add_argument('--seed', type=int, default=42, help='随机种子 (-1表示随机)')
    parser.add_argument('--negative-prompt', type=str,
                        default="ai-generated, worst detail, sketch, monochrome, rough sketch, fewer digits, extra digits, signature, watermark, sample watermark, logo, artist name, patreon logo, censor, censored, web address, copyright name, dated, patreon, username, dust particles",
                        help='负向提示词')
    return parser.parse_args()


def load_prompts_csv(csv_path: str, start_idx: int, num_prompts: int) -> list:
    """从CSV加载提示词"""
    prompts = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        # 验证必需的列
        if reader.fieldnames is None:
            raise ValueError(f"CSV文件格式错误: 无法读取列名")
        if 'image_name' not in reader.fieldnames or 'prompt' not in reader.fieldnames:
            raise ValueError(f"CSV文件必须包含 'image_name' 和 'prompt' 列，当前列: {reader.fieldnames}")

        all_rows = list(reader)

    # 获取切片
    end_idx = min(start_idx + num_prompts, len(all_rows))
    for row in all_rows[start_idx:end_idx]:
        # 使用basename防止路径注入
        image_name = os.path.basename(row['image_name'])
        prompts.append({
            'image_name': image_name,
            'prompt': row['prompt']
        })

    return prompts


def load_lora_config(config_path: str) -> dict:
    """加载LoRA配置"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    args = parse_args()

    # 设置CUDA设备
    device = torch.device(f'cuda:{args.gpu}')

    print(f"[GPU {args.gpu}] 开始初始化...")
    print(f"[GPU {args.gpu}] 模型路径: {args.model_path}")
    print(f"[GPU {args.gpu}] 提示词CSV: {args.prompts_csv}")
    print(f"[GPU {args.gpu}] LoRA配置: {args.lora_config}")

    # 加载提示词
    prompts = load_prompts_csv(args.prompts_csv, args.start_idx, args.num_prompts)
    actual_count = len(prompts)

    print(f"[GPU {args.gpu}] 将处理 {actual_count} 个提示词 (索引 {args.start_idx} 起)")

    if actual_count == 0:
        print(f"[GPU {args.gpu}] 没有提示词需要处理，退出")
        return

    # 加载LoRA配置
    lora_config = load_lora_config(args.lora_config)
    loras = lora_config.get('loras', [])

    if not loras:
        print(f"[GPU {args.gpu}] LoRA配置中没有定义任何LoRA，退出")
        return

    print(f"[GPU {args.gpu}] 将使用 {len(loras)} 个LoRA配置")
    for lora in loras:
        print(f"[GPU {args.gpu}]   - {lora['name']}: {lora['path']} (scale={lora.get('scale', 0.75)})")

    # 检查BF16支持
    bf16_support = torch.cuda.get_device_capability(device)[0] >= 8
    dtype = torch.bfloat16 if bf16_support else torch.float16
    print(f"[GPU {args.gpu}] 使用dtype: {dtype}")

    try:
        # 加载基础模型
        print(f"[GPU {args.gpu}] 正在加载Z-Image Pipeline...")
        load_start = time.time()

        pipe = ZImagePipeline.from_pretrained(
            args.model_path,
            torch_dtype=dtype,
            low_cpu_mem_usage=True,
        )
        pipe = pipe.to(device)

        load_time = time.time() - load_start
        print(f"[GPU {args.gpu}] ✓ Pipeline加载完成 (耗时: {load_time:.2f}秒)")

        # 基础种子
        base_seed = args.seed

        # 对每个LoRA配置进行生成
        total_generated = 0
        total_failed = 0
        total_time = 0

        for lora_idx, lora in enumerate(loras):
            lora_name = lora['name']
            lora_path = lora['path']
            lora_scale = lora.get('scale', 0.75)

            print(f"\n[GPU {args.gpu}] ========== LoRA {lora_idx + 1}/{len(loras)}: {lora_name} ==========")

            # 创建输出目录
            lora_output_dir = Path(args.output_dir) / lora_name / f"gpu_{args.gpu}"
            lora_output_dir.mkdir(parents=True, exist_ok=True)

            # 加载LoRA
            print(f"[GPU {args.gpu}] 加载LoRA: {lora_path}")
            lora_load_start = time.time()

            try:
                pipe.load_lora_weights(lora_path)
                pipe.set_adapters(["default"], adapter_weights=[lora_scale])
                print(f"[GPU {args.gpu}] ✓ LoRA加载完成 (scale={lora_scale}, 耗时: {time.time() - lora_load_start:.2f}秒)")
            except Exception as e:
                print(f"[GPU {args.gpu}] ✗ LoRA加载失败: {e}")
                print(f"[GPU {args.gpu}] 跳过此LoRA")
                continue

            # 生成图像
            lora_success = 0
            lora_failed = 0
            lora_time = 0

            for i, prompt_data in enumerate(prompts):
                image_name = prompt_data['image_name']
                prompt = prompt_data['prompt']

                # 跳过错误的提示词
                if prompt.startswith('ERROR:'):
                    print(f"[GPU {args.gpu}] 跳过错误提示词: {image_name}")
                    lora_failed += 1
                    continue

                # 输出文件路径 (保持原图像名)
                output_path = lora_output_dir / image_name

                # 如果已存在，跳过
                if output_path.exists():
                    print(f"[GPU {args.gpu}] 跳过已存在: {image_name}")
                    lora_success += 1
                    continue

                try:
                    start_time = time.time()

                    # 为每个图像设置不同的种子，确保不同图像有不同的随机性
                    if base_seed >= 0:
                        image_seed = base_seed + args.start_idx + i
                        generator = torch.Generator(device).manual_seed(image_seed)
                    else:
                        generator = None

                    with torch.inference_mode():
                        image = pipe(
                            prompt=prompt,
                            negative_prompt=args.negative_prompt,
                            height=args.height,
                            width=args.width,
                            num_inference_steps=args.num_inference_steps,
                            guidance_scale=args.guidance_scale,
                            generator=generator,
                        ).images[0]

                    gen_time = time.time() - start_time
                    lora_time += gen_time

                    # 保存图像
                    image.save(output_path, format='PNG')
                    lora_success += 1

                    # 打印进度
                    if (i + 1) % 10 == 0 or i == 0:
                        avg_time = lora_time / lora_success if lora_success > 0 else 0
                        progress = (i + 1) / actual_count * 100
                        print(f"[GPU {args.gpu}] [{lora_name}] 进度: {i+1}/{actual_count} ({progress:.1f}%) | "
                              f"平均速度: {avg_time:.2f}秒/张 | "
                              f"成功: {lora_success} | 失败: {lora_failed}")

                except Exception as e:
                    lora_failed += 1
                    print(f"[GPU {args.gpu}] ✗ 图像 {image_name} 生成失败: {e}")
                    continue

            # LoRA统计
            total_generated += lora_success
            total_failed += lora_failed
            total_time += lora_time

            print(f"[GPU {args.gpu}] [{lora_name}] 完成: 成功 {lora_success}, 失败 {lora_failed}")

            # 卸载LoRA - 使用delete_adapters确保彻底清理
            print(f"[GPU {args.gpu}] 卸载LoRA...")
            try:
                pipe.delete_adapters(["default"])
                torch.cuda.empty_cache()  # 立即清理GPU缓存
            except Exception as e:
                print(f"[GPU {args.gpu}] 卸载LoRA时出错: {e}")
                # 尝试备选方法
                try:
                    pipe.unload_lora_weights()
                except Exception:
                    pass

        # 总体统计
        print("\n" + "=" * 80)
        print(f"[GPU {args.gpu}] ✓ 所有LoRA处理完成!")
        print(f"[GPU {args.gpu}] 总生成: {total_generated} 张")
        print(f"[GPU {args.gpu}] 总失败: {total_failed} 张")
        if total_generated > 0:
            avg_time = total_time / total_generated
            print(f"[GPU {args.gpu}] 平均速度: {avg_time:.2f} 秒/张")
            print(f"[GPU {args.gpu}] 总耗时: {total_time/60:.2f} 分钟")
        print(f"[GPU {args.gpu}] 输出目录: {args.output_dir}")
        print("=" * 80)

    except Exception as e:
        print(f"[GPU {args.gpu}] ✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        # 清理GPU内存
        try:
            del pipe
        except NameError:
            pass
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
