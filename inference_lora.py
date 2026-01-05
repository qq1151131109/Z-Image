"""Z-Image LoRA Inference using Diffusers Pipeline.

This script demonstrates how to use Z-Image with LoRA adapters using the Diffusers library.
"""

import argparse
import os
import time
from pathlib import Path

import torch
from diffusers import ZImagePipeline


def parse_args():
    parser = argparse.ArgumentParser(description="Z-Image LoRA Inference")
    parser.add_argument(
        "--model_id",
        type=str,
        default="Tongyi-MAI/Z-Image-Turbo",
        help="HuggingFace model ID or local path to Z-Image model",
    )
    parser.add_argument(
        "--lora_path",
        type=str,
        required=False,
        default=None,
        help="Path to LoRA weights (local directory or HuggingFace repo ID)",
    )
    parser.add_argument(
        "--lora_scale",
        type=float,
        default=0.75,
        help="LoRA scale factor (0.0 to 1.0, higher means stronger LoRA effect)",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="A beautiful landscape with mountains and a lake at sunset",
        help="Text prompt for image generation",
    )
    parser.add_argument(
        "--negative_prompt",
        type=str,
        default=None,
        help="Negative prompt (optional)",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=1024,
        help="Image height (must be divisible by 16)",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1024,
        help="Image width (must be divisible by 16)",
    )
    parser.add_argument(
        "--num_inference_steps",
        type=int,
        default=9,
        help="Number of denoising steps (9 steps = 8 NFEs for Turbo model)",
    )
    parser.add_argument(
        "--guidance_scale",
        type=float,
        default=0.0,
        help="Guidance scale (0.0 for Turbo models, 4.5-7.5 for Base models)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output_lora.png",
        help="Output image path",
    )
    parser.add_argument(
        "--dtype",
        type=str,
        default="bfloat16",
        choices=["float32", "float16", "bfloat16"],
        help="Model dtype",
    )
    parser.add_argument(
        "--attention_backend",
        type=str,
        default="sdpa",
        choices=["sdpa", "flash", "_flash_3"],
        help="Attention backend (sdpa=default, flash=FA2, _flash_3=FA3)",
    )
    parser.add_argument(
        "--compile",
        action="store_true",
        help="Compile the transformer model for faster inference",
    )
    parser.add_argument(
        "--enable_cpu_offload",
        action="store_true",
        help="Enable CPU offloading to reduce VRAM usage",
    )
    parser.add_argument(
        "--list_loras",
        action="store_true",
        help="List all loaded LoRA adapters and exit",
    )
    return parser.parse_args()


def get_dtype(dtype_str: str):
    """Convert dtype string to torch dtype."""
    dtype_map = {
        "float32": torch.float32,
        "float16": torch.float16,
        "bfloat16": torch.bfloat16,
    }
    return dtype_map[dtype_str]


def main():
    args = parse_args()

    print("=" * 80)
    print("Z-Image LoRA Inference")
    print("=" * 80)

    # Setup dtype
    dtype = get_dtype(args.dtype)
    print(f"\nConfiguration:")
    print(f"  Model ID: {args.model_id}")
    print(f"  LoRA Path: {args.lora_path if args.lora_path else 'None (base model only)'}")
    print(f"  LoRA Scale: {args.lora_scale}")
    print(f"  Dtype: {args.dtype}")
    print(f"  Attention Backend: {args.attention_backend}")
    print(f"  Compile: {args.compile}")
    print(f"  CPU Offload: {args.enable_cpu_offload}")

    # Check device
    if torch.cuda.is_available():
        device = "cuda"
        print(f"\nUsing device: cuda ({torch.cuda.get_device_name(0)})")
        print(f"  CUDA Version: {torch.version.cuda}")
        print(f"  Available VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
    else:
        device = "cpu"
        print(f"\nWarning: CUDA not available, using CPU (will be slow)")

    # Load pipeline
    print(f"\nLoading Z-Image pipeline from {args.model_id}...")
    start_time = time.time()

    pipe = ZImagePipeline.from_pretrained(
        args.model_id,
        torch_dtype=dtype,
        low_cpu_mem_usage=True,
    )

    if not args.enable_cpu_offload:
        pipe.to(device)
    else:
        print("Enabling CPU offloading...")
        pipe.enable_model_cpu_offload()

    load_time = time.time() - start_time
    print(f"Pipeline loaded in {load_time:.2f} seconds")

    # Set attention backend
    if args.attention_backend != "sdpa":
        print(f"Setting attention backend to: {args.attention_backend}")
        try:
            pipe.transformer.set_attention_backend(args.attention_backend)
        except Exception as e:
            print(f"Warning: Failed to set attention backend: {e}")
            print("Falling back to default SDPA")

    # Compile model if requested
    if args.compile:
        print("Compiling transformer model (first run will be slow)...")
        compile_start = time.time()
        pipe.transformer = torch.compile(pipe.transformer, mode="max-autotune")
        print(f"Model compiled in {time.time() - compile_start:.2f} seconds")

    # Load LoRA weights
    if args.lora_path:
        print(f"\nLoading LoRA weights from: {args.lora_path}")
        lora_start = time.time()

        try:
            # Check if lora_path is a HuggingFace repo or local path
            lora_path = Path(args.lora_path)
            if lora_path.exists():
                # Local path
                pipe.load_lora_weights(str(lora_path))
                print(f"LoRA weights loaded from local path in {time.time() - lora_start:.2f} seconds")
            else:
                # Try as HuggingFace repo ID
                pipe.load_lora_weights(args.lora_path)
                print(f"LoRA weights loaded from HuggingFace in {time.time() - lora_start:.2f} seconds")

            # Set LoRA scale
            pipe.set_adapters(["default"], adapter_weights=[args.lora_scale])
            print(f"LoRA scale set to: {args.lora_scale}")

        except Exception as e:
            print(f"Error loading LoRA weights: {e}")
            print("Continuing with base model only...")

    # List LoRAs if requested
    if args.list_loras:
        print("\nCurrently loaded LoRA adapters:")
        if hasattr(pipe, "get_active_adapters"):
            adapters = pipe.get_active_adapters()
            if adapters:
                for adapter in adapters:
                    print(f"  - {adapter}")
            else:
                print("  No LoRA adapters loaded")
        else:
            print("  (Adapter listing not supported in this diffusers version)")
        return

    # Generate image
    print("\n" + "=" * 80)
    print("Generating Image")
    print("=" * 80)
    print(f"Prompt: {args.prompt}")
    if args.negative_prompt:
        print(f"Negative Prompt: {args.negative_prompt}")
    print(f"Size: {args.width}x{args.height}")
    print(f"Steps: {args.num_inference_steps}")
    print(f"Guidance Scale: {args.guidance_scale}")
    print(f"Seed: {args.seed}")

    gen_start = time.time()

    # Set up generator for reproducibility
    generator = torch.Generator(device).manual_seed(args.seed)

    # Generate
    image = pipe(
        prompt=args.prompt,
        negative_prompt=args.negative_prompt,
        height=args.height,
        width=args.width,
        num_inference_steps=args.num_inference_steps,
        guidance_scale=args.guidance_scale,
        generator=generator,
    ).images[0]

    gen_time = time.time() - gen_start
    print(f"\nImage generated in {gen_time:.2f} seconds")

    # Save image
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(str(output_path))
    print(f"Image saved to: {output_path.absolute()}")

    print("\n" + "=" * 80)
    print(f"Total time: {time.time() - start_time:.2f} seconds")
    print("=" * 80)


if __name__ == "__main__":
    main()
