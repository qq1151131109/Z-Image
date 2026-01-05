"""游戏赛道提示词生成器 V2 - 增强版创意多样性"""

import random
from typing import Dict, List


class GamingPromptGenerator:
    """生成高度多样化的游戏玩家社媒头像提示词

    V2改进：
    - 大幅扩展耳机/设备描述（品牌、颜色、特殊设计）
    - 增加创意场景（电竞赛事、VR、LAN party、游戏展会等）
    - 丰富拍摄角度和视觉风格
    - 增强游戏类型的视觉差异性
    """

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

        # ==================== 游戏类型权重分布 ====================

        self.game_types = [
            {"type": "pc_gaming", "weight": 0.50},
            {"type": "mobile_gaming", "weight": 0.30},
            {"type": "console_gaming", "weight": 0.20},
        ]

        # PC游戏具体类型（扩展，增加视觉描述）
        self.pc_games = [
            {"game": "playing intense FPS shooter", "vibe": "fast reflexes, quick mouse movements"},
            {"game": "playing competitive League of Legends", "vibe": "strategic clicking, team coordination"},
            {"game": "playing Valorant ranked match", "vibe": "precise aim, tactical gameplay"},
            {"game": "playing Call of Duty Warzone", "vibe": "battle royale intensity"},
            {"game": "playing Counter-Strike 2 competitive", "vibe": "pro-level concentration"},
            {"game": "playing Fortnite battle royale", "vibe": "building and shooting"},
            {"game": "playing Overwatch 2 team match", "vibe": "hero selection visible on screen"},
            {"game": "playing Apex Legends", "vibe": "fast-paced action"},
            {"game": "playing World of Warcraft raid", "vibe": "multiple hotbars and spells"},
            {"game": "playing Minecraft creative mode", "vibe": "relaxed building"},
            {"game": "playing Grand Theft Auto Online", "vibe": "open world chaos"},
            {"game": "playing Dota 2 tournament", "vibe": "MOBA strategic gameplay"},
            {"game": "playing Elden Ring boss fight", "vibe": "souls-like difficulty, focused tension"},
            {"game": "playing Cyberpunk 2077", "vibe": "immersed in RPG storytelling"},
            {"game": "playing simulation game", "vibe": "detailed management"},
            {"game": "speedrunning platformer game", "vibe": "intense precision timing"},
        ]

        # 手游类型
        self.mobile_games = [
            "playing mobile battle royale on phone",
            "playing Call of Duty Mobile",
            "playing PUBG Mobile intense match",
            "playing Clash Royale card battle",
            "playing Genshin Impact gacha game",
            "playing mobile MOBA with friends",
            "playing Candy Crush casually",
            "playing mobile racing game tilting phone",
            "playing Pokemon GO walking around",
            "playing Honkai Star Rail turn-based RPG",
            "playing mobile rhythm game with thumbs",
        ]

        # 主机游戏类型
        self.console_games = [
            {"game": "playing PlayStation 5 exclusive", "controller": "DualSense"},
            {"game": "playing Xbox Series X game", "controller": "Xbox wireless"},
            {"game": "playing Nintendo Switch handheld", "controller": "Joy-Cons"},
            {"game": "playing FIFA soccer", "controller": "standard gamepad"},
            {"game": "playing NBA 2K basketball", "controller": "standard gamepad"},
            {"game": "playing God of War", "controller": "DualSense"},
            {"game": "playing Elden Ring on console", "controller": "gamepad"},
            {"game": "playing fighting game", "controller": "arcade fight stick"},
            {"game": "playing racing game", "controller": "steering wheel and pedals"},
            {"game": "playing cozy indie game", "controller": "wireless controller"},
        ]

        # ==================== 人物特征 ====================

        self.ethnicities = [
            {"type": "Caucasian American", "weight": 0.60},
            {"type": "African American", "weight": 0.13},
            {"type": "Hispanic American", "weight": 0.18},
            {"type": "Asian American", "weight": 0.06},
            {"type": "mixed-race American", "weight": 0.03},
        ]

        self.ages = ["16", "18", "20", "22", "24", "26", "28", "30", "32", "35"]

        self.genders = [
            {"gender": "man", "weight": 0.65},
            {"gender": "woman", "weight": 0.35},
        ]

        self.hairstyles = [
            "short hair", "medium length hair", "long hair",
            "messy hair", "styled hair", "buzzcut",
            "man bun", "undercut hairstyle", "pulled back hair",
            "ponytail", "headband in hair", "dyed hair",
            "space buns", "half-up half-down", "braids"
        ]

        self.clothing = [
            "gaming hoodie", "graphic t-shirt", "esports team jersey",
            "black hoodie", "casual t-shirt", "tank top",
            "gaming branded shirt", "plain tee", "flannel shirt",
            "compression gaming sleeves", "streamer merch",
            "anime graphic hoodie", "oversized sweater", "crop top",
            "gaming org jacket", "athleisure wear"
        ]

        # ==================== 耳机/配饰（大幅扩展）====================

        self.headsets = [
            # 高端RGB耳机
            {"desc": "wearing RGB gaming headset with rainbow lighting", "weight": 0.12},
            {"desc": "wearing white wireless gaming headset with LED accents", "weight": 0.08},
            {"desc": "wearing pink gaming headset with cat ears and RGB", "weight": 0.06},
            {"desc": "wearing purple and black gaming headset with boom mic", "weight": 0.06},

            # 品牌风格描述
            {"desc": "wearing HyperX Cloud headset with red accents", "weight": 0.07},
            {"desc": "wearing SteelSeries Arctis white gaming headset", "weight": 0.07},
            {"desc": "wearing Razer Kraken neon green gaming headset", "weight": 0.06},
            {"desc": "wearing Logitech G Pro wireless headset", "weight": 0.05},
            {"desc": "wearing Astro A50 wireless headset with charging dock", "weight": 0.04},

            # 特殊设计
            {"desc": "wearing 7.1 surround sound headset with suspension headband", "weight": 0.05},
            {"desc": "wearing noise-cancelling gaming headset", "weight": 0.05},
            {"desc": "wearing open-back audiophile gaming headset", "weight": 0.03},
            {"desc": "wearing vintage retro gaming headphones", "weight": 0.03},

            # 简单款
            {"desc": "wearing basic black gaming headset", "weight": 0.10},
            {"desc": "wearing earbuds with mic", "weight": 0.05},

            # 无耳机
            {"desc": "", "weight": 0.08},
        ]

        self.accessories = [
            {"desc": "", "weight": 0.50},  # 无额外配饰
            {"desc": "wearing gaming glasses with blue light filter", "weight": 0.12},
            {"desc": "wearing baseball cap backwards", "weight": 0.10},
            {"desc": "wearing smartwatch showing heart rate", "weight": 0.08},
            {"desc": "wearing wrist support brace", "weight": 0.06},
            {"desc": "wearing fingerless gaming gloves", "weight": 0.05},
            {"desc": "wearing LED light-up glasses", "weight": 0.04},
            {"desc": "wearing team badge lanyard", "weight": 0.03},
            {"desc": "wearing compression sleeve on mouse arm", "weight": 0.02},
        ]

        # ==================== 场景设置（大幅扩展创意场景）====================

        self.settings = [
            # 传统家庭设置 (25%)
            {
                "location": "in RGB lit gaming bedroom",
                "details": "colorful LED strips, gaming posters, PC tower with RGB fans",
                "weight": 0.12
            },
            {
                "location": "in dark bedroom gaming setup",
                "details": "only screen glow lighting room, ambient blue and purple hues",
                "weight": 0.08
            },
            {
                "location": "in cozy gaming corner",
                "details": "warm desk lamp, organized cable management, plants nearby",
                "weight": 0.05
            },

            # 专业电竞/直播 (20%)
            {
                "location": "in professional streaming room",
                "details": "ring lights, green screen background, professional microphone on boom arm",
                "weight": 0.08
            },
            {
                "location": "at esports tournament stage",
                "details": "stadium lighting, audience visible in background, competitive atmosphere",
                "weight": 0.06
            },
            {
                "location": "in gaming content creator studio",
                "details": "multiple cameras, LED panel wall, professional setup",
                "weight": 0.06
            },

            # 社交游戏场景 (15%)
            {
                "location": "at LAN party with friends",
                "details": "multiple gaming PCs in same room, social gaming atmosphere",
                "weight": 0.06
            },
            {
                "location": "at internet café gaming",
                "details": "rows of gaming PCs visible, competitive environment",
                "weight": 0.05
            },
            {
                "location": "at gaming convention booth",
                "details": "expo hall visible, gaming banners and displays",
                "weight": 0.04
            },

            # 休闲客厅 (12%)
            {
                "location": "on living room couch gaming",
                "details": "big screen TV, casual home environment",
                "weight": 0.07
            },
            {
                "location": "in casual family room",
                "details": "comfortable furniture, relaxed setting",
                "weight": 0.05
            },

            # 创意场景 (18%)
            {
                "location": "in neon-lit gaming room",
                "details": "vibrant neon signs on wall, cyberpunk aesthetic, colorful glow",
                "weight": 0.05
            },
            {
                "location": "in gaming setup with neon underglow",
                "details": "neon strip lights under desk, futuristic vibe, purple and blue neon",
                "weight": 0.04
            },
            {
                "location": "during late night gaming marathon",
                "details": "energy drink cans, snacks visible, tired but focused",
                "weight": 0.03
            },
            {
                "location": "at gaming café social area",
                "details": "modern gaming lounge, group gaming atmosphere",
                "weight": 0.02
            },
            {
                "location": "in minimalist modern gaming setup",
                "details": "clean aesthetic, white and black color scheme, cable-free",
                "weight": 0.02
            },
            {
                "location": "in retro gaming room",
                "details": "vintage consoles and CRT TVs visible, nostalgic atmosphere",
                "weight": 0.01
            },
            {
                "location": "in cyberpunk streamer room",
                "details": "neon kanji signs, futuristic tech aesthetic, pink and cyan lighting",
                "weight": 0.01
            },

            # 移动游戏场景 (10%)
            {
                "location": "casually gaming on couch",
                "details": "relaxed mobile gaming, comfortable environment",
                "weight": 0.05
            },
            {
                "location": "gaming on commute",
                "details": "on train or bus, mobile gaming on-the-go",
                "weight": 0.03
            },
            {
                "location": "at park bench gaming",
                "details": "outdoor daylight, casual mobile gaming",
                "weight": 0.02
            },
        ]

        # ==================== PC设备细节（大幅扩展）====================

        self.pc_equipment = [
            # 键盘
            {"desc": "hands on RGB mechanical keyboard with custom keycaps", "weight": 0.10},
            {"desc": "typing on Cherry MX mechanical keyboard", "weight": 0.08},
            {"desc": "using hot-swappable custom keyboard with pudding keycaps", "weight": 0.06},
            {"desc": "gaming on compact 60% mechanical keyboard", "weight": 0.05},

            # 鼠标设置
            {"desc": "using lightweight honeycomb gaming mouse on RGB mousepad", "weight": 0.08},
            {"desc": "hand on wireless gaming mouse with RGB lighting", "weight": 0.07},
            {"desc": "precise mouse movements on large desk mat", "weight": 0.06},

            # 显示器设置
            {"desc": "gaming on triple monitor setup", "weight": 0.08},
            {"desc": "using ultrawide curved 240Hz monitor", "weight": 0.10},
            {"desc": "dual monitor setup with vertical secondary screen", "weight": 0.07},
            {"desc": "gaming on massive 49 inch super ultrawide", "weight": 0.04},

            # 完整设置
            {"desc": "elite gaming setup with RGB everything", "weight": 0.08},
            {"desc": "minimalist gaming setup with clean cable management", "weight": 0.06},
            {"desc": "high-end PC with tempered glass case and RGB", "weight": 0.05},
            {"desc": "water-cooled gaming PC with RGB reservoir", "weight": 0.02},
        ]

        # ==================== 姿势和动作（更具体）====================

        self.pc_poses = [
            "leaning forward intensely focused on screen, hands blur from fast movements",
            "sitting back in racing-style gaming chair, relaxed posture",
            "hunched over keyboard in intense concentration, face close to monitor",
            "perfect esports posture, elbows at 90 degrees",
            "celebrating victory with hands raised, big smile",
            "stretching arms above head during game break",
            "aggressive forward lean, intense gameplay moment",
            "one hand on mouse ready to click, other hand on WASD keys",
        ]

        self.mobile_poses = [
            "lying on bed holding phone horizontally",
            "sitting cross-legged on couch with phone",
            "intense concentration on phone screen, thumbs moving fast",
            "leaning back casually while playing phone",
            "holding phone with gaming grip attachment",
            "both hands on phone in landscape mode",
        ]

        self.console_poses = [
            "sitting on couch edge leaning forward with controller",
            "relaxed back on couch holding controller",
            "standing and moving while playing VR",
            "using racing wheel with focused driving posture",
            "intense button mashing on fight stick",
            "casual laid back console gaming",
        ]

        # ==================== 表情（更生动）====================

        self.expressions = [
            "intensely focused eyes locked on screen",
            "excited energetic expression with big smile",
            "serious competitive concentration face",
            "celebrating victory with pure joy",
            "determined look, brow furrowed",
            "surprised reaction, eyes wide open",
            "laughing at gameplay moment",
            "frustrated but determined expression",
            "calm focused professional demeanor",
            "mouth slightly open in concentration",
            "relaxed casual gaming vibe",
            "trash talking with smirk",
        ]

        # ==================== 拍摄角度（更多样化）====================

        self.camera_angles = [
            "dynamic side profile showing face and monitor glow",
            "three-quarter angle showcasing full gaming station",
            "straight on front view of gamer and setup",
            "over the shoulder shot showing game screen and hands",
            "close-up of face illuminated by screen",
            "wide shot showing entire gaming room and setup",
            "first-person POV showing hands and keyboard with screen visible",
            "reaction cam style focusing on face and upper body",
            "cinematic angle with dramatic lighting",
            "bird's eye view overhead shot of gaming setup",
        ]

        # ==================== 环境细节（更丰富）====================

        self.environment_details = [
            {"desc": "", "weight": 0.20},
            {"desc": "neon signs on wall behind setup", "weight": 0.08},
            {"desc": "anime and gaming posters on wall", "weight": 0.08},
            {"desc": "RGB LED light strips outlining desk", "weight": 0.08},
            {"desc": "neon underglow lighting beneath desk", "weight": 0.07},
            {"desc": "triple monitor setup with wallpaper engine running", "weight": 0.07},
            {"desc": "gaming collectibles and Funko Pops on shelves", "weight": 0.06},
            {"desc": "purple and pink neon accent lights", "weight": 0.06},
            {"desc": "professional microphone on boom arm", "weight": 0.05},
            {"desc": "RGB PC tower with tempered glass side panel", "weight": 0.05},
            {"desc": "racing-style gaming chair with RGB", "weight": 0.04},
            {"desc": "Nanoleaf light panels on wall", "weight": 0.04},
            {"desc": "neon kanji or gaming logos glowing", "weight": 0.04},
            {"desc": "gaming headset stand with RGB", "weight": 0.03},
            {"desc": "mini fridge next to desk", "weight": 0.02},
            {"desc": "custom cable management setup visible", "weight": 0.02},
            {"desc": "cyberpunk aesthetic neon tubes", "weight": 0.01},
        ]

        # ==================== 光照（增强视觉效果）====================

        self.lighting = [
            {"desc": "illuminated by vibrant RGB keyboard and monitor glow", "weight": 0.12},
            {"desc": "face dramatically lit by dual monitor blue glow in dark room", "weight": 0.10},
            {"desc": "colorful neon lights creating cyberpunk atmosphere", "weight": 0.10},
            {"desc": "LED strips casting purple and blue ambient light", "weight": 0.09},
            {"desc": "neon underglow and RGB creating vibrant scene", "weight": 0.08},
            {"desc": "screen glow as only light source, dramatic shadows", "weight": 0.08},
            {"desc": "professional streaming lights with perfect exposure", "weight": 0.07},
            {"desc": "natural daylight from window mixed with screen glow", "weight": 0.08},
            {"desc": "pink and cyan neon creating streamer aesthetic", "weight": 0.07},
            {"desc": "neon RGB creating vibrant color palette", "weight": 0.07},
            {"desc": "overhead room lighting with neon accent lights", "weight": 0.07},
            {"desc": "ring light creating professional content creator look", "weight": 0.05},
            {"desc": "purple neon glow illuminating gaming space", "weight": 0.02},
        ]

        # ==================== 画质关键词 ====================

        self.quality_base = [
            "Shot on iPhone", "gaming lifestyle content", "authentic gamer moment",
            "social media gaming post", "real gaming setup photo",
            "content creator shot", "gaming influencer style"
        ]

        self.quality_effects = [
            {"desc": "RGB ambient lighting", "weight": 0.25},
            {"desc": "screen glow illumination", "weight": 0.20},
            {"desc": "natural indoor lighting", "weight": 0.18},
            {"desc": "dramatic low-light gaming atmosphere", "weight": 0.15},
            {"desc": "professional streaming studio lighting", "weight": 0.12},
            {"desc": "cinematic gaming room lighting", "weight": 0.10},
        ]

    def _weighted_choice(self, items: List[Dict], weight_key: str = "weight") -> Dict:
        """根据权重随机选择"""
        weights = [item.get(weight_key, 1.0) for item in items]
        return self.rng.choices(items, weights=weights, k=1)[0]

    def generate_prompt(self, index: int) -> str:
        """生成单个高度多样化游戏玩家提示词"""
        self.rng.seed(42 + index)

        # 选择游戏类型
        game_type = self._weighted_choice(self.game_types)["type"]

        # 人物特征
        ethnicity = self._weighted_choice(self.ethnicities)["type"]
        age = self.rng.choice(self.ages)
        gender = self._weighted_choice(self.genders)["gender"]
        hairstyle = self.rng.choice(self.hairstyles)
        clothing = self.rng.choice(self.clothing)
        headset = self._weighted_choice(self.headsets)
        accessory = self._weighted_choice(self.accessories)
        expression = self.rng.choice(self.expressions)

        # 场景和环境
        setting = self._weighted_choice(self.settings)
        camera_angle = self.rng.choice(self.camera_angles)
        lighting = self._weighted_choice(self.lighting)
        env_detail = self._weighted_choice(self.environment_details)

        prompt_parts = []

        if game_type == "pc_gaming":
            game_info = self.rng.choice(self.pc_games)
            game = game_info["game"]
            game_vibe = game_info.get("vibe", "")
            equipment = self._weighted_choice(self.pc_equipment)
            pose = self.rng.choice(self.pc_poses)

            prompt_parts = [
                camera_angle,
                f"{ethnicity} {gender} age {age}",
                f"with {hairstyle}",
                f"wearing {clothing}",
            ]

            if headset["desc"]:
                prompt_parts.append(headset["desc"])
            if accessory["desc"]:
                prompt_parts.append(accessory["desc"])

            prompt_parts.extend([
                expression,
                game,
            ])

            if game_vibe:
                prompt_parts.append(game_vibe)

            prompt_parts.extend([
                pose,
                equipment["desc"],
                setting['location'],
                setting['details'],
            ])

        elif game_type == "mobile_gaming":
            game = self.rng.choice(self.mobile_games)
            pose = self.rng.choice(self.mobile_poses)

            prompt_parts = [
                camera_angle,
                f"{ethnicity} {gender} age {age}",
                f"with {hairstyle}",
                f"wearing {clothing}",
            ]

            if accessory["desc"]:
                prompt_parts.append(accessory["desc"])

            prompt_parts.extend([
                expression,
                game,
                pose,
                setting['location'],
                setting['details'],
            ])

        else:  # console_gaming
            game_info = self.rng.choice(self.console_games)
            game = game_info["game"]
            controller = game_info["controller"]
            pose = self.rng.choice(self.console_poses)

            prompt_parts = [
                camera_angle,
                f"{ethnicity} {gender} age {age}",
                f"with {hairstyle}",
                f"wearing {clothing}",
            ]

            if headset["desc"]:
                prompt_parts.append(headset["desc"])
            if accessory["desc"]:
                prompt_parts.append(accessory["desc"])

            prompt_parts.extend([
                expression,
                game,
                pose,
                f"holding {controller}",
                setting['location'],
                setting['details'],
            ])

        # 添加环境细节
        if env_detail["desc"]:
            prompt_parts.append(env_detail["desc"])

        # 添加光照
        prompt_parts.append(lighting["desc"])

        # 添加画质关键词
        base_quality = self.rng.choice(self.quality_base)
        quality_effect = self._weighted_choice(self.quality_effects)["desc"]

        prompt_parts.extend([
            base_quality,
            quality_effect,
            "high quality",
            "gaming lifestyle photography",
            "8k"
        ])

        return ", ".join(prompt_parts)

    def generate_batch(self, num_prompts: int) -> List[str]:
        """批量生成提示词"""
        return [self.generate_prompt(i) for i in range(num_prompts)]


if __name__ == "__main__":
    generator = GamingPromptGenerator(seed=42)

    print("=" * 80)
    print("游戏赛道提示词生成器 V2 - 测试20个样例")
    print("=" * 80)

    for i in range(20):
        prompt = generator.generate_prompt(i)
        print(f"\n[提示词 {i}]")
        print(prompt)
        print()
