"""打包游戏和美食头像为ZIP文件"""

import os
import zipfile
from pathlib import Path


def create_zip(source_dir, zip_filename):
    """创建ZIP压缩包"""
    print(f"正在打包 {source_dir} -> {zip_filename}...")

    # 统计文件数量
    png_files = list(Path(source_dir).rglob("*.png"))
    total_files = len(png_files)

    print(f"  找到 {total_files} 个PNG文件")

    # 创建ZIP文件
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for i, file_path in enumerate(png_files, 1):
            # 获取相对路径
            arcname = str(file_path.relative_to(Path(source_dir).parent))
            zipf.write(file_path, arcname)

            # 进度显示
            if i % 500 == 0 or i == total_files:
                print(f"  进度: {i}/{total_files} ({i/total_files*100:.1f}%)")

    # 获取文件大小
    zip_size = os.path.getsize(zip_filename)
    zip_size_mb = zip_size / (1024 * 1024)

    print(f"  ✓ 完成！文件大小: {zip_size_mb:.1f} MB")
    print()

    return zip_filename, zip_size_mb


def main():
    print("=" * 80)
    print("打包游戏和美食头像")
    print("=" * 80)
    print()

    # 打包游戏头像
    gaming_zip, gaming_size = create_zip(
        source_dir="gaming_avatars_output",
        zip_filename="gaming_avatars.zip"
    )

    # 打包美食头像
    food_zip, food_size = create_zip(
        source_dir="food_avatars_output",
        zip_filename="food_avatars.zip"
    )

    print("=" * 80)
    print("✓ 打包完成！")
    print("=" * 80)
    print()
    print("生成的文件:")
    print(f"  - {gaming_zip} ({gaming_size:.1f} MB)")
    print(f"  - {food_zip} ({food_size:.1f} MB)")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
