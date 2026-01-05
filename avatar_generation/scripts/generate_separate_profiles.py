"""分别生成各领域账号 - 独立文件存储"""

import pandas as pd
from datetime import datetime
from profile_generator_v2 import BeautyProfileGenerator, GamingProfileGenerator, FoodProfileGenerator


def generate_and_save(generator_class, count, category_name, file_prefix, seed):
    """生成并保存单个类别的账号"""
    print(f"正在生成 {category_name} ({count}个账号, seed={seed})...")

    generator = generator_class(seed=seed)
    profiles = generator.generate(count)

    # 创建DataFrame
    df = pd.DataFrame(profiles)

    # 生成文件名（带时间戳）
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_filename = f"{file_prefix}_{timestamp}.csv"
    excel_filename = f"{file_prefix}_{timestamp}.xlsx"

    # 保存CSV
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    print(f"  ✓ CSV已保存: {csv_filename}")

    # 保存Excel
    df.to_excel(excel_filename, index=False, engine='openpyxl')
    print(f"  ✓ Excel已保存: {excel_filename}")

    # 统计信息
    unique_nicknames = df['nickname'].nunique()
    unique_bios = df['bio'].nunique()
    print(f"  ✓ 昵称唯一性: {unique_nicknames}/{count} ({unique_nicknames/count*100:.2f}%)")
    print(f"  ✓ 简介唯一性: {unique_bios}/{count} ({unique_bios/count*100:.2f}%)")
    print()

    return profiles


def main():
    print("=" * 80)
    print("TikTok账号生成器 - 分类生成")
    print("=" * 80)
    print()
    print("生成计划:")
    print("  1. 美女领域第1批: 4000个账号")
    print("  2. 美女领域第2批: 4000个账号")
    print("  3. 游戏领域: 4000个账号")
    print("  4. 美食领域: 4000个账号")
    print("  总计: 16000个账号")
    print()
    print("=" * 80)
    print()

    # 美女领域 - 第1批（seed=42）
    beauty_batch1 = generate_and_save(
        generator_class=BeautyProfileGenerator,
        count=4000,
        category_name="美女领域 - 第1批",
        file_prefix="beauty_batch1",
        seed=42
    )

    # 美女领域 - 第2批（seed=43，确保不同）
    beauty_batch2 = generate_and_save(
        generator_class=BeautyProfileGenerator,
        count=4000,
        category_name="美女领域 - 第2批",
        file_prefix="beauty_batch2",
        seed=43
    )

    # 游戏领域（seed=44）
    gaming_profiles = generate_and_save(
        generator_class=GamingProfileGenerator,
        count=4000,
        category_name="游戏领域",
        file_prefix="gaming",
        seed=44
    )

    # 美食领域（seed=45）
    food_profiles = generate_and_save(
        generator_class=FoodProfileGenerator,
        count=4000,
        category_name="美食领域",
        file_prefix="food",
        seed=45
    )

    print("=" * 80)
    print("✓ 所有文件生成完成！")
    print("=" * 80)
    print()
    print("生成的文件:")
    print("  - beauty_batch1_*.csv / .xlsx (美女第1批)")
    print("  - beauty_batch2_*.csv / .xlsx (美女第2批)")
    print("  - gaming_*.csv / .xlsx (游戏)")
    print("  - food_*.csv / .xlsx (美食)")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
