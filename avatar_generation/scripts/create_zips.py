#!/usr/bin/env python3
"""创建两个ZIP压缩包"""

import zipfile
import sys
from pathlib import Path

def create_zip_from_list(file_list_path, output_zip_path, base_dir):
    """从文件列表创建ZIP"""
    print(f"正在创建 {output_zip_path}...")

    with open(file_list_path, 'r') as f:
        files = [line.strip() for line in f if line.strip()]

    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        for i, file_path in enumerate(files, 1):
            # 移除开头的 "./"
            clean_path = file_path.lstrip('./')
            full_path = base_dir / clean_path

            if full_path.exists():
                # 在ZIP中使用简化的路径
                arcname = clean_path
                zipf.write(full_path, arcname=arcname)

                if i % 500 == 0:
                    print(f"  已添加 {i}/{len(files)} 个文件...")
            else:
                print(f"  警告: 文件不存在 - {full_path}")

    # 检查ZIP文件大小
    zip_size = Path(output_zip_path).stat().st_size / (1024**3)  # GB
    print(f"✓ 完成! 文件大小: {zip_size:.2f} GB")
    print(f"  包含 {len(files)} 个图像")
    print()

if __name__ == "__main__":
    base_dir = Path("/mnt/shenglin/Z-Image/avatars_6000")

    print("=" * 80)
    print("创建两个ZIP压缩包（每个4000张图片）")
    print("=" * 80)
    print()

    # 创建第一个压缩包 (前4000张)
    create_zip_from_list(
        "/tmp/part1_files.txt",
        "/mnt/shenglin/Z-Image/avatars_part1.zip",
        base_dir
    )

    # 创建第二个压缩包 (后1992张 + 前2008张)
    create_zip_from_list(
        "/tmp/part2_files.txt",
        "/mnt/shenglin/Z-Image/avatars_part2.zip",
        base_dir
    )

    print("=" * 80)
    print("✓ 所有压缩包创建完成!")
    print("=" * 80)
    print()
    print("文件位置:")
    print("  - /mnt/shenglin/Z-Image/avatars_part1.zip (4000张图片)")
    print("  - /mnt/shenglin/Z-Image/avatars_part2.zip (4000张图片)")
    print()
