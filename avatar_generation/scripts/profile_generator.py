"""TikTok账号昵称和简介生成器 - 规则+LLM混合方案"""

import random
import pandas as pd
from typing import List, Dict, Tuple
from datetime import datetime


class BeautyProfileGenerator:
    """美女领域账号生成器"""

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.used_nicknames = set()

        # TikTok限制
        self.MAX_NICKNAME_LENGTH = 30
        self.MAX_BIO_LENGTH = 80

        # 昵称组件
        self.adjectives = [
            "Sexy", "Hot", "Sweet", "Wild", "Cute", "Divine", "Angel", "Devil",
            "Naughty", "Sassy", "Classy", "Flirty", "Fierce", "Goddess", "Queen",
            "Diamond", "Pearl", "Ruby", "Crystal", "Golden", "Silver", "Velvet",
            "Midnight", "Sunset", "Moon", "Star", "Cherry", "Peach", "Rose",
            "Violet", "Scarlet", "Amber", "Jade", "Ivory", "Mystic", "Secret"
        ]

        self.nouns = [
            "Kitty", "Kitten", "Bunny", "Fox", "Vixen", "Angel", "Doll",
            "Babe", "Beauty", "Princess", "Queen", "Goddess", "Dream", "Fantasy",
            "Rose", "Lily", "Orchid", "Jewel", "Diamond", "Pearl", "Gem",
            "Butterfly", "Bird", "Swan", "Dove", "Cherry", "Peach", "Berry",
            "Honey", "Sugar", "Candy", "Spice", "Silk", "Satin", "Lace"
        ]

        self.female_names = [
            "Bella", "Emma", "Olivia", "Ava", "Mia", "Sophia", "Isabella",
            "Luna", "Aria", "Chloe", "Lily", "Zoey", "Leah", "Maya", "Ruby",
            "Grace", "Ivy", "Rose", "Jade", "Eve", "Nina", "Lola", "Coco",
            "Gigi", "Fifi", "Kiki", "Mimi", "Tina", "Dina", "Lena"
        ]

        self.suffixes = ["xo", "xx", "bby", "bb", "luv", "hun", "angel", "babe"]

        # 简介模板
        self.bio_templates = [
            "Living my best life {emoji1}",
            "Your favorite distraction {emoji1}",
            "Here for a good time {emoji1} DM open {emoji2}",
            "Just a girl who loves to have fun {emoji1}",
            "Life is short, make it sweet {emoji1}{emoji2}",
            "Manifesting my dreams {emoji1}",
            "Vibes and good times only {emoji1}",
            "Creating my own sunshine {emoji1}{emoji2}",
            "Living wild and free {emoji1}",
            "Sweet but psycho {emoji1}{emoji2}",
            "Chasing dreams and good vibes {emoji1}",
            "Too glam to give a damn {emoji1}",
            "Confidence level: Selfie with no filter {emoji1}",
            "Messy bun and getting stuff done {emoji1}",
            "Sassy, classy with a touch of bad-assy {emoji1}",
        ]

        self.bio_emojis = [
            "💋", "😈", "🔥", "💕", "✨", "💎", "👑", "🌹",
            "🦋", "🌙", "⭐", "💫", "🍒", "🍑", "🌺", "💖"
        ]

    def generate_nickname(self) -> str:
        """生成昵称（规则系统）"""
        max_attempts = 100
        for _ in range(max_attempts):
            pattern = self.rng.choice([
                "adjective_noun",      # SexyKitty
                "name_suffix",         # Bella_xo
                "adjective_name",      # DivineBella
                "name_number",         # Emma2024
                "adjective_noun_num",  # HotBabe69
                "name_adj",            # BellaSweet
                "single_word",         # Goddess
            ])

            if pattern == "adjective_noun":
                nickname = f"{self.rng.choice(self.adjectives)}{self.rng.choice(self.nouns)}"
            elif pattern == "name_suffix":
                nickname = f"{self.rng.choice(self.female_names)}_{self.rng.choice(self.suffixes)}"
            elif pattern == "adjective_name":
                nickname = f"{self.rng.choice(self.adjectives)}{self.rng.choice(self.female_names)}"
            elif pattern == "name_number":
                nickname = f"{self.rng.choice(self.female_names)}{self.rng.randint(2020, 2025)}"
            elif pattern == "adjective_noun_num":
                nickname = f"{self.rng.choice(self.adjectives)}{self.rng.choice(self.nouns)}{self.rng.randint(10, 99)}"
            elif pattern == "name_adj":
                nickname = f"{self.rng.choice(self.female_names)}{self.rng.choice(self.adjectives)}"
            else:  # single_word
                nickname = self.rng.choice(self.adjectives + self.nouns)

            # 添加随机变体
            if self.rng.random() < 0.3:
                nickname = self._add_variation(nickname)

            # 检查长度和去重
            if len(nickname) <= self.MAX_NICKNAME_LENGTH and nickname not in self.used_nicknames:
                self.used_nicknames.add(nickname)
                return nickname

        # 如果失败，添加随机数字
        base = f"{self.rng.choice(self.female_names)}"
        nickname = f"{base}{self.rng.randint(1000, 9999)}"
        self.used_nicknames.add(nickname)
        return nickname

    def _add_variation(self, nickname: str) -> str:
        """添加变体：下划线、双字母、数字等"""
        variations = [
            lambda s: s.lower(),
            lambda s: s + str(self.rng.randint(1, 99)),
            lambda s: s + "_",
            lambda s: "_" + s,
            lambda s: s.replace("e", "3") if "e" in s else s,
            lambda s: s.replace("a", "4") if "a" in s else s,
            lambda s: s.replace("o", "0") if "o" in s else s,
            lambda s: s[0].lower() + s[1:],
        ]
        return self.rng.choice(variations)(nickname)

    def generate_bio(self) -> str:
        """生成简介（规则系统）"""
        template = self.rng.choice(self.bio_templates)
        emoji1 = self.rng.choice(self.bio_emojis)
        emoji2 = self.rng.choice(self.bio_emojis)

        bio = template.format(emoji1=emoji1, emoji2=emoji2)

        # 确保不超过80字符
        if len(bio) > self.MAX_BIO_LENGTH:
            bio = bio[:self.MAX_BIO_LENGTH-3] + "..."

        return bio

    def generate(self, count: int) -> List[Dict]:
        """生成指定数量的账号"""
        profiles = []
        for i in range(count):
            profile = {
                "category": "beauty",
                "index": i,
                "nickname": self.generate_nickname(),
                "bio": self.generate_bio()
            }
            profiles.append(profile)

            if (i + 1) % 500 == 0:
                print(f"[Beauty] 已生成 {i+1}/{count} 个账号")

        return profiles


class GamingProfileGenerator:
    """游戏领域账号生成器"""

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.used_nicknames = set()

        self.MAX_NICKNAME_LENGTH = 30
        self.MAX_BIO_LENGTH = 80

        # 昵称组件
        self.prefixes = [
            "Pro", "Elite", "Mega", "Ultra", "Super", "Hyper", "Dark", "Shadow",
            "Ninja", "Cyber", "Toxic", "Lethal", "Fatal", "Deadly", "Savage",
            "Godly", "Mythic", "Epic", "Legendary", "Master", "Alpha", "Omega"
        ]

        self.gaming_nouns = [
            "Gamer", "Player", "Slayer", "Killer", "Hunter", "Sniper", "Warrior",
            "Fighter", "Assassin", "Ninja", "Dragon", "Phoenix", "Wolf", "Tiger",
            "Viper", "Reaper", "Ghost", "Demon", "Beast", "Titan", "Knight",
            "Ace", "King", "Emperor", "Legend", "Hero", "Champion"
        ]

        self.game_terms = [
            "Clutch", "Frag", "Combo", "Streak", "Rage", "Rush", "Aim", "Shot",
            "Skill", "Noob", "Pwn", "GG", "MVP", "Ace", "Solo", "Carry"
        ]

        self.games = [
            "Valorant", "CS", "Apex", "Fortnite", "COD", "LOL", "Dota",
            "Overwatch", "PUBG", "Warzone", "R6", "Rocket"
        ]

        # 简介模板
        self.bio_templates = [
            "{game} {rank} | {hours}k hrs | Main: {role} 🎮",
            "Competitive {game} player | {rank} 🏆",
            "Streaming {game} daily | {rank} | Drop a follow 🎮",
            "{rank} {game} | Grinding to top 500 💪",
            "Pro {game} player | {hours}k+ hours | Road to Radiant 🔥",
            "{game} enthusiast | {rank} | Let's squad up 🎮",
            "Cracked at {game} | {rank} | DM for coaching 🎯",
            "{hours}k hours in {game} | Still silver 😂",
            "{game} addict | {rank} | Content creator 🎥",
            "Competitive gamer | {game} {rank} | Twitch partner 🟣",
        ]

        self.ranks = [
            "Radiant", "Immortal", "Diamond", "Platinum", "Gold",
            "Master", "Grandmaster", "Challenger", "Predator",
            "Global Elite", "Supreme", "Legendary"
        ]

        self.roles = [
            "Jett", "Reyna", "Raze", "Sage", "Duelist", "Sentinel",
            "Controller", "Initiator", "Wraith", "Octane", "Bloodhound"
        ]

    def generate_nickname(self) -> str:
        """生成游戏昵称"""
        max_attempts = 100
        for _ in range(max_attempts):
            pattern = self.rng.choice([
                "prefix_noun",        # ProGamer
                "prefix_noun_x",      # EliteSniper_X
                "ttv_name",           # TTV_Shadow
                "xx_name_xx",         # xXDragonSlayerXx
                "noun_term",          # SniperAce
                "game_prefix",        # ValorantKing
                "term_number",        # Clutch_420
            ])

            if pattern == "prefix_noun":
                nickname = f"{self.rng.choice(self.prefixes)}{self.rng.choice(self.gaming_nouns)}"
            elif pattern == "prefix_noun_x":
                nickname = f"{self.rng.choice(self.prefixes)}{self.rng.choice(self.gaming_nouns)}_X"
            elif pattern == "ttv_name":
                nickname = f"TTV_{self.rng.choice(self.gaming_nouns)}"
            elif pattern == "xx_name_xx":
                name = self.rng.choice(self.gaming_nouns)
                nickname = f"xX{name}Xx"
            elif pattern == "noun_term":
                nickname = f"{self.rng.choice(self.gaming_nouns)}{self.rng.choice(self.game_terms)}"
            elif pattern == "game_prefix":
                nickname = f"{self.rng.choice(self.games)}{self.rng.choice(self.prefixes)}"
            else:  # term_number
                nickname = f"{self.rng.choice(self.game_terms)}_{self.rng.randint(100, 999)}"

            # 随机变体
            if self.rng.random() < 0.2:
                nickname = nickname + str(self.rng.randint(1, 99))

            if len(nickname) <= self.MAX_NICKNAME_LENGTH and nickname not in self.used_nicknames:
                self.used_nicknames.add(nickname)
                return nickname

        nickname = f"{self.rng.choice(self.gaming_nouns)}{self.rng.randint(1000, 9999)}"
        self.used_nicknames.add(nickname)
        return nickname

    def generate_bio(self) -> str:
        """生成游戏简介"""
        template = self.rng.choice(self.bio_templates)
        bio = template.format(
            game=self.rng.choice(self.games),
            rank=self.rng.choice(self.ranks),
            hours=self.rng.choice([1, 2, 3, 5, 10, 15, 20]),
            role=self.rng.choice(self.roles)
        )

        if len(bio) > self.MAX_BIO_LENGTH:
            bio = bio[:self.MAX_BIO_LENGTH-3] + "..."

        return bio

    def generate(self, count: int) -> List[Dict]:
        """生成指定数量的账号"""
        profiles = []
        for i in range(count):
            profile = {
                "category": "gaming",
                "index": i,
                "nickname": self.generate_nickname(),
                "bio": self.generate_bio()
            }
            profiles.append(profile)

            if (i + 1) % 500 == 0:
                print(f"[Gaming] 已生成 {i+1}/{count} 个账号")

        return profiles


class FoodProfileGenerator:
    """美食领域账号生成器"""

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.used_nicknames = set()

        self.MAX_NICKNAME_LENGTH = 30
        self.MAX_BIO_LENGTH = 80

        # 昵称组件
        self.food_adjectives = [
            "Tasty", "Yummy", "Delicious", "Sweet", "Savory", "Spicy", "Fresh",
            "Chef", "Foodie", "Gourmet", "Cooking", "Baking", "Kitchen", "Recipe"
        ]

        self.food_nouns = [
            "Chef", "Cook", "Baker", "Foodie", "Eats", "Bites", "Kitchen",
            "Recipes", "Dishes", "Meals", "Treats", "Delights", "Flavors"
        ]

        self.food_items = [
            "Sushi", "Pizza", "Pasta", "Burger", "Taco", "Ramen", "Curry",
            "Cupcake", "Cookie", "Donut", "Cake", "Bread", "Noodles", "Rice",
            "Steak", "Salmon", "Avocado", "Matcha", "Coffee", "Tea", "Boba"
        ]

        self.cuisines = [
            "Italian", "Japanese", "Mexican", "Chinese", "Thai", "Korean",
            "French", "Indian", "American", "Mediterranean"
        ]

        self.names = [
            "Bella", "Emma", "Sophie", "Lucy", "Mia", "Chloe", "Lily",
            "Grace", "Ruby", "Maya", "Nina", "Lola", "Zoe", "Ivy"
        ]

        # 简介模板
        self.bio_templates = [
            "Home chef 🍳 | {cuisine} cuisine lover | Sharing recipes daily",
            "Baking queen 🧁 | {specialty} expert | Sweet treats & more",
            "Food enthusiast | Trying every {food} spot in town 🍕",
            "{cuisine} food lover 🍜 | Cooking up something special",
            "Chef life 👨‍🍳 | {specialty} specialist | DM for recipes",
            "Foodie adventures 🍴 | {cuisine} cuisine | Restaurant reviews",
            "Home baker 🍰 | Making your favorites | Custom orders open",
            "Cooking mama 🥘 | {cuisine} dishes | Family recipes",
            "Food content creator 📸 | {specialty} lover | Collab friendly",
            "{cuisine} chef | Sharing my culinary journey 🍽️",
        ]

        self.specialties = [
            "pasta", "sushi", "desserts", "bread", "cakes", "cookies",
            "ramen", "curry", "BBQ", "vegan food", "healthy meals"
        ]

    def generate_nickname(self) -> str:
        """生成美食昵称"""
        max_attempts = 100
        for _ in range(max_attempts):
            pattern = self.rng.choice([
                "name_food",          # BellaBakes
                "food_adj",           # SushiLover
                "adj_name",           # ChefEmma
                "food_cuisine",       # ItalianBites
                "the_noun",           # TheFoodie
                "name_eats",          # MiasEats
                "food_item",          # CupcakeQueen
            ])

            if pattern == "name_food":
                name = self.rng.choice(self.names)
                food = self.rng.choice(self.food_nouns)
                nickname = f"{name}{food}"
            elif pattern == "food_adj":
                food = self.rng.choice(self.food_items)
                adj = self.rng.choice(["Lover", "Addict", "Fanatic", "Master"])
                nickname = f"{food}{adj}"
            elif pattern == "adj_name":
                adj = self.rng.choice(self.food_adjectives)
                name = self.rng.choice(self.names)
                nickname = f"{adj}{name}"
            elif pattern == "food_cuisine":
                cuisine = self.rng.choice(self.cuisines)
                noun = self.rng.choice(self.food_nouns)
                nickname = f"{cuisine}{noun}"
            elif pattern == "the_noun":
                noun = self.rng.choice(self.food_nouns + self.food_adjectives)
                nickname = f"The{noun}"
            elif pattern == "name_eats":
                name = self.rng.choice(self.names)
                nickname = f"{name}sEats"
            else:  # food_item
                food = self.rng.choice(self.food_items)
                adj = self.rng.choice(["Queen", "King", "Cutie", "Babe"])
                nickname = f"{food}{adj}"

            # 随机变体
            if self.rng.random() < 0.2:
                nickname = nickname + str(self.rng.randint(1, 99))

            if len(nickname) <= self.MAX_NICKNAME_LENGTH and nickname not in self.used_nicknames:
                self.used_nicknames.add(nickname)
                return nickname

        nickname = f"{self.rng.choice(self.names)}{self.rng.randint(1000, 9999)}"
        self.used_nicknames.add(nickname)
        return nickname

    def generate_bio(self) -> str:
        """生成美食简介"""
        template = self.rng.choice(self.bio_templates)
        bio = template.format(
            cuisine=self.rng.choice(self.cuisines),
            specialty=self.rng.choice(self.specialties),
            food=self.rng.choice(self.food_items)
        )

        if len(bio) > self.MAX_BIO_LENGTH:
            bio = bio[:self.MAX_BIO_LENGTH-3] + "..."

        return bio

    def generate(self, count: int) -> List[Dict]:
        """生成指定数量的账号"""
        profiles = []
        for i in range(count):
            profile = {
                "category": "food",
                "index": i,
                "nickname": self.generate_nickname(),
                "bio": self.generate_bio()
            }
            profiles.append(profile)

            if (i + 1) % 500 == 0:
                print(f"[Food] 已生成 {i+1}/{count} 个账号")

        return profiles


def main():
    """主函数：生成所有账号并导出"""
    print("=" * 80)
    print("TikTok账号生成器 - 开始生成")
    print("=" * 80)
    print()

    # 统计头像数量
    beauty_count = 5992
    gaming_count = 4000
    food_count = 4000
    total_count = beauty_count + gaming_count + food_count

    print(f"美女领域: {beauty_count} 个账号")
    print(f"游戏领域: {gaming_count} 个账号")
    print(f"美食领域: {food_count} 个账号")
    print(f"总计: {total_count} 个账号")
    print()
    print("=" * 80)
    print()

    # 生成账号
    all_profiles = []

    print("正在生成美女领域账号...")
    beauty_gen = BeautyProfileGenerator(seed=42)
    beauty_profiles = beauty_gen.generate(beauty_count)
    all_profiles.extend(beauty_profiles)
    print(f"✓ 美女领域生成完成: {len(beauty_profiles)} 个账号")
    print()

    print("正在生成游戏领域账号...")
    gaming_gen = GamingProfileGenerator(seed=43)
    gaming_profiles = gaming_gen.generate(gaming_count)
    all_profiles.extend(gaming_profiles)
    print(f"✓ 游戏领域生成完成: {len(gaming_profiles)} 个账号")
    print()

    print("正在生成美食领域账号...")
    food_gen = FoodProfileGenerator(seed=44)
    food_profiles = food_gen.generate(food_count)
    all_profiles.extend(food_profiles)
    print(f"✓ 美食领域生成完成: {len(food_profiles)} 个账号")
    print()

    # 创建DataFrame
    df = pd.DataFrame(all_profiles)

    # 导出CSV
    csv_filename = f"tiktok_profiles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    print(f"✓ CSV文件已保存: {csv_filename}")

    # 导出Excel
    excel_filename = f"tiktok_profiles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
        # 所有账号
        df.to_excel(writer, sheet_name='All Profiles', index=False)

        # 按类别分sheet
        df[df['category'] == 'beauty'].to_excel(writer, sheet_name='Beauty', index=False)
        df[df['category'] == 'gaming'].to_excel(writer, sheet_name='Gaming', index=False)
        df[df['category'] == 'food'].to_excel(writer, sheet_name='Food', index=False)

    print(f"✓ Excel文件已保存: {excel_filename}")
    print()

    # 统计信息
    print("=" * 80)
    print("生成统计")
    print("=" * 80)
    print(f"总账号数: {len(all_profiles)}")
    print(f"美女: {len(beauty_profiles)}")
    print(f"游戏: {len(gaming_profiles)}")
    print(f"美食: {len(food_profiles)}")
    print()

    # 检查昵称重复
    all_nicknames = [p['nickname'] for p in all_profiles]
    unique_nicknames = len(set(all_nicknames))
    print(f"昵称唯一性: {unique_nicknames}/{len(all_nicknames)} ({unique_nicknames/len(all_nicknames)*100:.2f}%)")
    print()

    # 示例展示
    print("=" * 80)
    print("示例账号 (每个类别随机3个)")
    print("=" * 80)
    print()

    for category in ['beauty', 'gaming', 'food']:
        cat_profiles = [p for p in all_profiles if p['category'] == category]
        samples = random.sample(cat_profiles, min(3, len(cat_profiles)))
        print(f"【{category.upper()}】")
        for sample in samples:
            print(f"  昵称: {sample['nickname']}")
            print(f"  简介: {sample['bio']}")
            print()

    print("=" * 80)
    print("✓ 所有账号生成完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()
