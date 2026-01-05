# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Z-Image is a 6B parameter image generation foundation model based on a Scalable Single-Stream Diffusion Transformer (S3-DiT) architecture. PyTorch native implementation for inference with Z-Image-Turbo, Z-Image-Base, and Z-Image-Edit variants.

Key features:
- Sub-second inference on H800/H100 GPUs with proper optimization
- Single-stream architecture: text, visual semantic tokens, and image VAE tokens concatenated at sequence level
- Multiple attention backends (SDPA, Flash Attention 2/3)
- LoRA support via diffusers + PEFT
- Runs on 16GB VRAM consumer devices

## Common Commands

```bash
# Install project dependencies
pip install -e .

# Basic inference (PyTorch native)
python inference.py

# LoRA inference (diffusers pipeline)
python inference_lora.py --lora_path ./path/to/lora --prompt "your prompt"

# Custom attention backend
ZIMAGE_ATTENTION=_flash_3 python inference.py

# Download model from ModelScope (China, ~13GB)
python download_modelscope.py

# Generate model manifest with MD5 checksums
python -m src.tools.generate_manifest ckpts/Z-Image-Turbo

# Format code
black . && isort . && ruff check .
```

## Code Architecture

Source code is under `src/`:
- **`zimage/`**: Core model - `transformer.py` (ZImageTransformer2DModel), `autoencoder.py` (VAE), `scheduler.py` (FlowMatchEulerDiscreteScheduler), `pipeline.py` (generation loop)
- **`utils/`**: `loader.py` (sharded safetensors loading), `attention.py` (backend dispatch), `helpers.py` (model download/verification)
- **`config/`**: Architecture constants and inference defaults

### Key Architecture Details

**Single-Stream DiT Design:**
Text embeddings, visual semantic tokens, and image VAE latents concatenated into unified sequence. Dynamic timestep shifting via `calculate_shift()` adjusts noise schedules based on sequence length (resolution). Implementation: `src/zimage/transformer.py:ZImageTransformer2DModel`

**Attention Backends** (`src/utils/attention.py`):
- `_native_flash`: PyTorch SDPA (default)
- `flash`: Flash Attention 2 (CUDA required)
- `_flash_3`: Flash Attention 3 (Hopper GPUs only, fastest)
- Set via `ZIMAGE_ATTENTION` env var or `set_attention_backend()`

**Model Loading Flow:**
1. `ensure_model_weights()` → downloads to `ckpts/` if missing
2. `load_from_local_dir()` → loads transformer, VAE, text_encoder, tokenizer, scheduler
3. Returns dict ready for `generate()`

**LoRA Integration:**
- Diffusers path (recommended): `inference_lora.py` → `ZImagePipeline.from_pretrained()` + PEFT
- `lora_scale` controls adapter strength (0.0-1.0, default 0.75)
- Compatible with DiffSynth-Studio trained weights

## Model Variants

- **Z-Image-Turbo**: Distilled 8-step (num_inference_steps=9, guidance_scale=0.0) - currently released
- **Z-Image-Base**: Non-distilled (guidance_scale ~4.5-7.5) - to be released
- **Z-Image-Edit**: Image-to-image editing - to be released

## Important Constraints

- Image dimensions must be divisible by 16 (VAE scale factor 8 × 2)
- PyTorch >= 2.5.0 required
- Flash Attention 3 requires Hopper architecture GPUs
- Compilation incompatible with CPU/MPS backends

## Performance Tips

**Hopper GPUs (H100/H200/H800):** `compile=True` + `ZIMAGE_ATTENTION=_flash_3` + `torch.bfloat16`

**Low VRAM (8-16GB):** `pipe.enable_model_cpu_offload()` + `torch.float16` + lower resolution

## Avatar Generation

All avatar generation code is organized under `avatar_generation/`:
- `prompts/`: Prompt generators (implement `generate_prompt(seed_or_index)` method)
- `scripts/`: Generation scripts and shell launchers
- `output/`: Generated images (avatars_6000, food_avatars_output, gaming_avatars_output)
- `data/`: CSV/XLSX profile data
- `logs/`: Generation logs
- `docs/`: Avatar-related documentation

**Single GPU:**
```bash
python avatar_generation/scripts/generate_on_single_gpu.py --gpu 1 --start-idx 0 --num-images 1000
```

**Multi-GPU Parallel (IMPORTANT: Use bash scripts, NOT Python multiprocessing - CUDA fork() issues):**
```bash
cd avatar_generation/scripts && ./run_parallel_6000.sh
tail -f avatar_generation/logs/gpu_1.log          # Monitor progress
```

**Performance:** ~5.24s/image on RTX 4090, ~95 minutes for 6000 images across 6 GPUs
