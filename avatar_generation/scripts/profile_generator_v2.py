"""TikTok账号生成器 V2 - 分段拼接方案"""

import random
import pandas as pd
from typing import List, Dict
from datetime import datetime


class BeautyProfileGenerator:
    """美女领域账号生成器 - 分段拼接"""

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.used_nicknames = set()

        # TikTok限制
        self.MAX_NICKNAME_LENGTH = 30
        self.MAX_BIO_LENGTH = 80

        # ==================== 昵称组件 ====================
        self.adjectives = [
            "Sexy", "Hot", "Sweet", "Wild", "Cute", "Divine", "Angel", "Devil",
            "Naughty", "Sassy", "Classy", "Flirty", "Fierce", "Goddess", "Queen",
            "Diamond", "Pearl", "Ruby", "Crystal", "Golden", "Silver", "Velvet",
            "Midnight", "Sunset", "Moon", "Star", "Cherry", "Peach", "Rose",
            "Violet", "Scarlet", "Amber", "Jade", "Ivory", "Mystic", "Secret",
            "Pretty", "Lovely", "Dreamy", "Magic", "Sparkle", "Glam", "Chic"
        ]

        self.nouns = [
            "Kitty", "Kitten", "Bunny", "Fox", "Vixen", "Angel", "Doll",
            "Babe", "Beauty", "Princess", "Queen", "Goddess", "Dream", "Fantasy",
            "Rose", "Lily", "Orchid", "Jewel", "Diamond", "Pearl", "Gem",
            "Butterfly", "Bird", "Swan", "Dove", "Cherry", "Peach", "Berry",
            "Honey", "Sugar", "Candy", "Spice", "Silk", "Satin", "Lace",
            "Star", "Moon", "Sun", "Sky", "Ocean", "Fire", "Ice"
        ]

        self.female_names = [
            "Bella", "Emma", "Olivia", "Ava", "Mia", "Sophia", "Isabella",
            "Luna", "Aria", "Chloe", "Lily", "Zoey", "Leah", "Maya", "Ruby",
            "Grace", "Ivy", "Rose", "Jade", "Eve", "Nina", "Lola", "Coco",
            "Gigi", "Fifi", "Kiki", "Mimi", "Tina", "Dina", "Lena", "Sara",
            "Kate", "Ella", "Anna", "Clara", "Lucy", "Sophie", "Harper"
        ]

        self.suffixes = ["xo", "xx", "bby", "bb", "luv", "hun", "angel", "babe", "cutie", "boo"]

        # ==================== 简介分段组件 ====================

        # 第一段：开场/状态（20+ options）
        self.bio_part1 = [
            "Living my best life",
            "Your favorite distraction",
            "Just a girl who loves life",
            "Making memories",
            "Chasing dreams",
            "Creating my own sunshine",
            "Living in the moment",
            "Here for a good time",
            "Living wild and free",
            "Manifesting my dreams",
            "Spreading good vibes",
            "Life is short, living it up",
            "On my own journey",
            "Making every day count",
            "Just being me",
            "Living unapologetically",
            "Keeping it real",
            "Enjoying the ride",
            "Living fearlessly",
            "Making magic happen",
            "Embracing my vibe",
            "Feeling myself",
            "Being authentic",
            "Living boldly",
        ]

        # 第二段：态度/风格（30+ options）
        self.bio_part2 = [
            "Vibes only",
            "Too glam to give a damn",
            "Sweet but psycho",
            "Sassy with class",
            "Confidence on point",
            "No filter needed",
            "Messy bun life",
            "Good vibes energy",
            "Boss babe energy",
            "Positive vibes",
            "Unapologetically me",
            "Living my truth",
            "Zero regrets",
            "Making moves",
            "Self love first",
            "Free spirit",
            "Wild at heart",
            "Classy never trashy",
            "Cute and dangerous",
            "Sugar and spice",
            "Sparkle and shine",
            "Fierce and fabulous",
            "Pretty and petty",
            "Hot mess express",
            "Dreamer and doer",
            "Lover not fighter",
            "Bad and bougie",
            "Thick and thriving",
            "Blessed and grateful",
            "Savage mode",
        ]

        # 第三段：行动召唤（可选，15+ options）
        self.bio_part3 = [
            "DM me",
            "DM open",
            "Come say hi",
            "Let's chat",
            "Slide into my DMs",
            "Link in bio",
            "Check my link",
            "New content daily",
            "Follow for more",
            "Stay tuned",
            "More coming soon",
            "Watch my stories",
            "Join my journey",
            "Collab friendly",
            "Always online",
        ]

        # Emoji组合
        self.bio_emojis = [
            "💋", "😈", "🔥", "💕", "✨", "💎", "👑", "🌹",
            "🦋", "🌙", "⭐", "💫", "🍒", "🍑", "🌺", "💖",
            "💗", "🌸", "🌟", "💘", "🎀", "🌼"
        ]

    def generate_nickname(self) -> str:
        """生成昵称（规则系统）"""
        max_attempts = 100
        for _ in range(max_attempts):
            pattern = self.rng.choice([
                "adjective_noun",
                "name_suffix",
                "adjective_name",
                "name_number",
                "adjective_noun_num",
                "name_adj",
                "single_word",
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
            else:
                nickname = self.rng.choice(self.adjectives + self.nouns)

            if self.rng.random() < 0.3:
                nickname = self._add_variation(nickname)

            if len(nickname) <= self.MAX_NICKNAME_LENGTH and nickname not in self.used_nicknames:
                self.used_nicknames.add(nickname)
                return nickname

        base = f"{self.rng.choice(self.female_names)}"
        nickname = f"{base}{self.rng.randint(1000, 9999)}"
        self.used_nicknames.add(nickname)
        return nickname

    def _add_variation(self, nickname: str) -> str:
        """添加变体"""
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
        """生成简介（分段拼接）"""
        # 70%概率使用3段式，30%使用2段式
        use_part3 = self.rng.random() < 0.7

        part1 = self.rng.choice(self.bio_part1)
        part2 = self.rng.choice(self.bio_part2)
        emoji1 = self.rng.choice(self.bio_emojis)

        if use_part3:
            part3 = self.rng.choice(self.bio_part3)
            emoji2 = self.rng.choice(self.bio_emojis)
            # 随机选择拼接格式
            formats = [
                f"{part1} {emoji1} | {part2} | {part3} {emoji2}",
                f"{part1} | {part2} {emoji1} | {part3}",
                f"{part1} {emoji1} {part2} | {part3} {emoji2}",
                f"{part2} {emoji1} | {part1} | {part3}",
            ]
            bio = self.rng.choice(formats)
        else:
            emoji2 = self.rng.choice(self.bio_emojis)
            formats = [
                f"{part1} {emoji1} | {part2} {emoji2}",
                f"{part1} | {part2} {emoji1}",
                f"{part2} {emoji1} {emoji2} | {part1}",
            ]
            bio = self.rng.choice(formats)

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
    """游戏领域账号生成器 - 分段拼接"""

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.used_nicknames = set()

        self.MAX_NICKNAME_LENGTH = 30
        self.MAX_BIO_LENGTH = 80

        # ==================== 昵称组件 ====================
        self.prefixes = [
            "Pro", "Elite", "Mega", "Ultra", "Super", "Hyper", "Dark", "Shadow",
            "Ninja", "Cyber", "Toxic", "Lethal", "Fatal", "Deadly", "Savage",
            "Godly", "Mythic", "Epic", "Legendary", "Master", "Alpha", "Omega",
            "Prime", "Apex", "Blazing", "Thunder", "Storm", "Dragon"
        ]

        self.gaming_nouns = [
            "Gamer", "Player", "Slayer", "Killer", "Hunter", "Sniper", "Warrior",
            "Fighter", "Assassin", "Ninja", "Dragon", "Phoenix", "Wolf", "Tiger",
            "Viper", "Reaper", "Ghost", "Demon", "Beast", "Titan", "Knight",
            "Ace", "King", "Emperor", "Legend", "Hero", "Champion", "Raider"
        ]

        self.game_terms = [
            "Clutch", "Frag", "Combo", "Streak", "Rage", "Rush", "Aim", "Shot",
            "Skill", "Noob", "Pwn", "GG", "MVP", "Ace", "Solo", "Carry",
            "Beast", "God", "Demon"
        ]

        # ==================== 简介分段组件 ====================

        # 游戏名称
        self.games = [
            "Valorant", "CS", "Apex", "Fortnite", "COD", "LOL", "Dota",
            "Overwatch", "PUBG", "Warzone", "R6", "Rocket League"
        ]

        # Rank/等级
        self.ranks = [
            "Radiant", "Immortal", "Diamond", "Platinum", "Gold", "Master",
            "Grandmaster", "Challenger", "Predator", "Global Elite",
            "Supreme", "Legendary", "Mythic"
        ]

        # 补充信息第一类：时间/经验
        self.experience = [
            "1k hrs", "2k hrs", "3k hrs", "5k hrs", "10k hrs", "15k+ hrs",
            "5 years exp", "Competitive player", "Pro player", "Semi-pro"
        ]

        # 补充信息第二类：角色/武器
        self.roles = [
            "Main: Jett", "Main: Reyna", "Main: Raze", "Main: Sage",
            "Duelist main", "Controller main", "Sentinel main",
            "Main: Wraith", "Main: Octane", "Main: Bloodhound",
            "AWP main", "Rifler", "Entry fragger", "Support main"
        ]

        # 补充信息第三类：行为/状态
        self.actions = [
            "Streaming daily", "Content creator", "Grinding ranked",
            "Road to Radiant", "Grinding to top 500", "Coaching available",
            "DM for coaching", "Twitch partner", "Let's squad up",
            "Looking for team", "Scrim partner needed", "Clan recruiting"
        ]

        # Emoji
        self.emojis = ["🎮", "🏆", "🔥", "💪", "🎯", "👑", "⚡", "💀", "🟣"]

    def generate_nickname(self) -> str:
        """生成游戏昵称"""
        max_attempts = 100
        for _ in range(max_attempts):
            pattern = self.rng.choice([
                "prefix_noun",
                "prefix_noun_x",
                "ttv_name",
                "xx_name_xx",
                "noun_term",
                "game_prefix",
                "term_number",
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
                nickname = f"{self.rng.choice(self.games[:6])}{self.rng.choice(self.prefixes)}"
            else:
                nickname = f"{self.rng.choice(self.game_terms)}_{self.rng.randint(100, 999)}"

            if self.rng.random() < 0.2:
                nickname = nickname + str(self.rng.randint(1, 99))

            if len(nickname) <= self.MAX_NICKNAME_LENGTH and nickname not in self.used_nicknames:
                self.used_nicknames.add(nickname)
                return nickname

        nickname = f"{self.rng.choice(self.gaming_nouns)}{self.rng.randint(1000, 9999)}"
        self.used_nicknames.add(nickname)
        return nickname

    def generate_bio(self) -> str:
        """生成游戏简介（分段拼接）"""
        game = self.rng.choice(self.games)
        rank = self.rng.choice(self.ranks)
        emoji = self.rng.choice(self.emojis)

        # 随机选择补充信息类型（40% experience, 30% role, 30% action）
        rand = self.rng.random()
        if rand < 0.4:
            extra = self.rng.choice(self.experience)
        elif rand < 0.7:
            extra = self.rng.choice(self.roles)
        else:
            extra = self.rng.choice(self.actions)

        # 随机选择拼接格式
        formats = [
            f"{game} {rank} | {extra} {emoji}",
            f"{rank} {game} | {extra} {emoji}",
            f"{game} {emoji} {rank} | {extra}",
            f"{extra} | {game} {rank} {emoji}",
            f"{rank} {game} {emoji} | {extra}",
        ]

        bio = self.rng.choice(formats)

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
    """美食领域账号生成器 - 分段拼接"""

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.used_nicknames = set()

        self.MAX_NICKNAME_LENGTH = 30
        self.MAX_BIO_LENGTH = 80

        # ==================== 昵称组件 ====================
        self.food_adjectives = [
            "Tasty", "Yummy", "Delicious", "Sweet", "Savory", "Spicy", "Fresh",
            "Chef", "Foodie", "Gourmet", "Cooking", "Baking", "Kitchen", "Recipe",
            "Homemade", "Organic", "Healthy", "Crispy"
        ]

        self.food_nouns = [
            "Chef", "Cook", "Baker", "Foodie", "Eats", "Bites", "Kitchen",
            "Recipes", "Dishes", "Meals", "Treats", "Delights", "Flavors",
            "Cuisine", "Table", "Plate"
        ]

        self.food_items = [
            "Sushi", "Pizza", "Pasta", "Burger", "Taco", "Ramen", "Curry",
            "Cupcake", "Cookie", "Donut", "Cake", "Bread", "Noodles", "Rice",
            "Steak", "Salmon", "Avocado", "Matcha", "Coffee", "Tea", "Boba",
            "Waffle", "Pancake", "Smoothie"
        ]

        self.cuisines = [
            "Italian", "Japanese", "Mexican", "Chinese", "Thai", "Korean",
            "French", "Indian", "American", "Mediterranean", "Vietnamese", "Greek"
        ]

        self.names = [
            "Bella", "Emma", "Sophie", "Lucy", "Mia", "Chloe", "Lily",
            "Grace", "Ruby", "Maya", "Nina", "Lola", "Zoe", "Ivy", "Sara"
        ]

        # ==================== 简介分段组件 ====================

        # 第一段：身份/角色
        self.bio_part1 = [
            "Home chef",
            "Baking queen",
            "Food enthusiast",
            "Cooking mama",
            "Chef life",
            "Home baker",
            "Food lover",
            "Foodie adventures",
            "Food content creator",
            "Culinary artist",
            "Kitchen wizard",
            "Dessert queen",
            "Recipe developer",
            "Food blogger",
            "Meal prep master",
            "Cooking enthusiast",
            "Baking addict",
            "Food photographer",
        ]

        # 第二段：专长/菜系/食物
        self.bio_part2 = [
            "Italian cuisine lover",
            "Japanese food fanatic",
            "Mexican dishes specialist",
            "Thai cuisine expert",
            "French pastry lover",
            "Chinese food addict",
            "Korean BBQ enthusiast",
            "Mediterranean flavors",
            "Pasta perfectionist",
            "Sushi master",
            "Dessert specialist",
            "Bread baking pro",
            "Cake decorator",
            "Pizza enthusiast",
            "Vegan cooking",
            "Healthy meals",
            "Comfort food expert",
            "Street food lover",
            "Farm to table",
            "Organic cooking",
        ]

        # 第三段：行为/内容
        self.bio_part3 = [
            "Sharing recipes daily",
            "New recipes weekly",
            "DM for recipes",
            "Custom orders open",
            "Cooking tutorials",
            "Restaurant reviews",
            "Food styling tips",
            "Recipe videos daily",
            "Let's cook together",
            "Collab friendly",
            "Private chef available",
            "Catering services",
            "Follow for foodie tips",
            "Join my food journey",
            "Food adventures await",
        ]

        # Emoji
        self.emojis = [
            "🍳", "🧁", "🍕", "🍜", "🍰", "🍴", "👨‍🍳", "🥘", "📸", "🍽️",
            "🍱", "🍔", "🌮", "🍝", "🥗", "☕"
        ]

    def generate_nickname(self) -> str:
        """生成美食昵称"""
        max_attempts = 100
        for _ in range(max_attempts):
            pattern = self.rng.choice([
                "name_food",
                "food_adj",
                "adj_name",
                "food_cuisine",
                "the_noun",
                "name_eats",
                "food_item",
            ])

            if pattern == "name_food":
                name = self.rng.choice(self.names)
                food = self.rng.choice(self.food_nouns)
                nickname = f"{name}{food}"
            elif pattern == "food_adj":
                food = self.rng.choice(self.food_items)
                adj = self.rng.choice(["Lover", "Addict", "Fanatic", "Master", "Queen", "King"])
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
            else:
                food = self.rng.choice(self.food_items)
                adj = self.rng.choice(["Queen", "King", "Cutie", "Babe", "Bites"])
                nickname = f"{food}{adj}"

            if self.rng.random() < 0.2:
                nickname = nickname + str(self.rng.randint(1, 99))

            if len(nickname) <= self.MAX_NICKNAME_LENGTH and nickname not in self.used_nicknames:
                self.used_nicknames.add(nickname)
                return nickname

        nickname = f"{self.rng.choice(self.names)}{self.rng.randint(1000, 9999)}"
        self.used_nicknames.add(nickname)
        return nickname

    def generate_bio(self) -> str:
        """生成美食简介（分段拼接）"""
        part1 = self.rng.choice(self.bio_part1)
        part2 = self.rng.choice(self.bio_part2)
        part3 = self.rng.choice(self.bio_part3)
        emoji = self.rng.choice(self.emojis)

        # 随机选择拼接格式
        formats = [
            f"{part1} {emoji} | {part2} | {part3}",
            f"{part1} | {part2} {emoji} | {part3}",
            f"{part2} {emoji} | {part1} | {part3}",
            f"{part1} {emoji} {part2} | {part3}",
            f"{part1} | {part2} | {part3} {emoji}",
        ]

        bio = self.rng.choice(formats)

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
    print("TikTok账号生成器 V2 - 分段拼接方案")
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
    csv_filename = f"tiktok_profiles_v2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    print(f"✓ CSV文件已保存: {csv_filename}")

    # 导出Excel
    excel_filename = f"tiktok_profiles_v2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='All Profiles', index=False)
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

    # 检查唯一性
    all_nicknames = [p['nickname'] for p in all_profiles]
    unique_nicknames = len(set(all_nicknames))
    print(f"昵称唯一性: {unique_nicknames}/{len(all_nicknames)} ({unique_nicknames/len(all_nicknames)*100:.2f}%)")

    all_bios = [p['bio'] for p in all_profiles]
    unique_bios = len(set(all_bios))
    print(f"简介唯一性: {unique_bios}/{len(all_bios)} ({unique_bios/len(all_bios)*100:.2f}%)")
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
