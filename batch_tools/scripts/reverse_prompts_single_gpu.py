#!/usr/bin/env python3
"""
使用Qwen3-VL在单个GPU上批量反推图像提示词
通过命令行参数指定GPU ID、起始索引和图像数量
"""

import os
import sys
import time
import argparse
import csv
from pathlib import Path
from glob import glob

import torch
from PIL import Image
from transformers import Qwen3VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info


# 默认的反推prompt模板 (来自ComfyUI工作流)
DEFAULT_PROMPT_TEMPLATE = """Analyze the image and generate a text prompt for image generation.

**Instructions:**
1. **Output Language:** English only.
2. **Trigger Word (Mandatory):** You **MUST** start the generated text with the trigger word "**ohmx, **" followed immediately by the description.
3. **Subject:** Describe the character's gender, hairstyle, clothing, pose, and actions.
4. **Environment:** Describe the background, lighting, and objects.
5. **Style:** Describe the amateur, raw smartphone photography vibes.

**Strict Constraints:**
- **DO NOT** describe specific facial features (e.g., do not mention eye color, nose shape, lip shape, or makeup details).
- **Focus on:** Texture, lighting atmosphere, and the "imperfect" reality of the photo.

**Mandatory Style Keywords:**
At the very end of your description, ALWAYS append the following keywords:
", Shot on iPhone, authentic snapshot, visible pores, uneven skin tone, messy background, chromatic aberration, harsh flash, motion blur, Raw photo."
"""


def parse_args():
    parser = argparse.ArgumentParser(description='使用Qwen3-VL在单个GPU上批量反推图像提示词')
    parser.add_argument('--gpu', type=int, required=True, help='GPU ID (0-7)')
    parser.add_argument('--image-dir', type=str, required=True, help='图像目录路径')
    parser.add_argument('--start-idx', type=int, required=True, help='起始图像索引')
    parser.add_argument('--num-images', type=int, required=True, help='处理图像数量')
    parser.add_argument('--output-csv', type=str, required=True, help='输出CSV文件路径')
    parser.add_argument('--model-path', type=str,
                        default='/home/ubuntu/shenglin/ComfyUI/models/prompt_generator/Qwen3-VL-8B-Instruct-FP8',
                        help='Qwen3-VL模型路径')
    parser.add_argument('--prompt-template', type=str, default=None,
                        help='自定义prompt模板 (默认使用内置模板)')
    parser.add_argument('--max-new-tokens', type=int, default=512, help='最大生成token数')
    parser.add_argument('--temperature', type=float, default=0.7, help='采样温度')
    parser.add_argument('--image-extensions', type=str, default='png,jpg,jpeg,webp',
                        help='支持的图像扩展名 (逗号分隔)')
    return parser.parse_args()


def get_image_files(image_dir: str, extensions: list) -> list:
    """获取目录下所有支持格式的图像文件"""
    image_files = []
    for ext in extensions:
        image_files.extend(glob(os.path.join(image_dir, f'*.{ext}')))
        image_files.extend(glob(os.path.join(image_dir, f'*.{ext.upper()}')))
    return sorted(set(image_files))


def main():
    args = parse_args()

    # 设置CUDA设备
    device = torch.device(f'cuda:{args.gpu}')

    print(f"[GPU {args.gpu}] 开始初始化...")
    print(f"[GPU {args.gpu}] 模型路径: {args.model_path}")
    print(f"[GPU {args.gpu}] 图像目录: {args.image_dir}")

    # 获取图像文件列表
    extensions = args.image_extensions.split(',')
    all_images = get_image_files(args.image_dir, extensions)
    total_images = len(all_images)
    print(f"[GPU {args.gpu}] 目录中共有 {total_images} 张图像")

    # 获取分配给当前GPU的图像切片
    end_idx = min(args.start_idx + args.num_images, total_images)
    image_slice = all_images[args.start_idx:end_idx]
    actual_count = len(image_slice)

    print(f"[GPU {args.gpu}] 将处理 {actual_count} 张图像 (索引 {args.start_idx} 到 {end_idx - 1})")

    if actual_count == 0:
        print(f"[GPU {args.gpu}] 没有图像需要处理，退出")
        return

    # 确定prompt模板
    prompt_template = args.prompt_template if args.prompt_template else DEFAULT_PROMPT_TEMPLATE

    # 检查BF16支持
    bf16_support = torch.cuda.get_device_capability(device)[0] >= 8
    dtype = torch.bfloat16 if bf16_support else torch.float16
    print(f"[GPU {args.gpu}] 使用dtype: {dtype}")

    try:
        # 加载模型
        print(f"[GPU {args.gpu}] 正在加载Qwen3-VL模型...")
        load_start = time.time()

        processor = AutoProcessor.from_pretrained(
            args.model_path,
            min_pixels=256 * 28 * 28,
            max_pixels=1280 * 28 * 28,
        )

        model = Qwen3VLForConditionalGeneration.from_pretrained(
            args.model_path,
            torch_dtype=dtype,
            device_map=device,
            attn_implementation="eager",
        )

        load_time = time.time() - load_start
        print(f"[GPU {args.gpu}] ✓ 模型加载完成 (耗时: {load_time:.2f}秒)")

        # 创建输出目录
        output_dir = Path(args.output_csv).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        # 处理图像
        results = []
        success_count = 0
        fail_count = 0
        total_time = 0

        print(f"[GPU {args.gpu}] 开始反推提示词...")
        print("=" * 80)

        for i, img_path in enumerate(image_slice):
            global_idx = args.start_idx + i
            img_name = os.path.basename(img_path)

            try:
                start_time = time.time()

                # 构建消息
                messages = [
                    {
                        "role": "system",
                        "content": "You are QwenVL, you are a helpful assistant expert in turning images into words.",
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "image", "image": f"file://{os.path.abspath(img_path)}"},
                            {"type": "text", "text": prompt_template},
                        ],
                    },
                ]

                # 处理输入
                text = processor.apply_chat_template(
                    messages, tokenize=False, add_generation_prompt=True
                )
                image_inputs, video_inputs = process_vision_info(messages)
                inputs = processor(
                    text=[text],
                    images=image_inputs,
                    videos=video_inputs,
                    padding=True,
                    return_tensors="pt",
                )
                inputs = inputs.to(device)

                # 推理
                with torch.inference_mode():
                    generated_ids = model.generate(
                        **inputs,
                        max_new_tokens=args.max_new_tokens,
                        temperature=args.temperature,
                    )

                # 解码输出
                generated_ids_trimmed = [
                    out_ids[len(in_ids):]
                    for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
                ]
                prompt = processor.batch_decode(
                    generated_ids_trimmed,
                    skip_special_tokens=True,
                    clean_up_tokenization_spaces=False,
                )[0]

                inference_time = time.time() - start_time
                total_time += inference_time

                # 保存结果
                results.append({
                    'image_name': img_name,
                    'prompt': prompt.strip()
                })

                success_count += 1

                # 打印进度
                if (i + 1) % 10 == 0 or i == 0:
                    avg_time = total_time / success_count if success_count > 0 else 0
                    progress = (i + 1) / actual_count * 100
                    print(f"[GPU {args.gpu}] 进度: {i+1}/{actual_count} ({progress:.1f}%) | "
                          f"平均速度: {avg_time:.2f}秒/张 | "
                          f"成功: {success_count} | 失败: {fail_count}")

            except Exception as e:
                fail_count += 1
                print(f"[GPU {args.gpu}] ✗ 图像 {img_name} 处理失败: {e}")
                # 仍然记录，但prompt为空
                results.append({
                    'image_name': img_name,
                    'prompt': f"ERROR: {str(e)}"
                })
                continue

        # 保存CSV
        print(f"[GPU {args.gpu}] 保存结果到 {args.output_csv}")
        with open(args.output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['image_name', 'prompt'])
            writer.writeheader()
            writer.writerows(results)

        # 打印统计信息
        print("=" * 80)
        print(f"[GPU {args.gpu}] ✓ 反推完成!")
        print(f"[GPU {args.gpu}] 成功处理: {success_count}/{actual_count} 张")
        print(f"[GPU {args.gpu}] 失败: {fail_count} 张")
        if success_count > 0:
            avg_time = total_time / success_count
            print(f"[GPU {args.gpu}] 平均速度: {avg_time:.2f} 秒/张")
            print(f"[GPU {args.gpu}] 总耗时: {total_time/60:.2f} 分钟")
        print(f"[GPU {args.gpu}] 输出文件: {args.output_csv}")
        print("=" * 80)

    except Exception as e:
        print(f"[GPU {args.gpu}] ✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        # 清理GPU内存
        try:
            del model
        except NameError:
            pass
        try:
            del processor
        except NameError:
            pass
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
