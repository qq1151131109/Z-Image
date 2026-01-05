"""灵活的多样化提示词生成器 - 美国女性"""

import random
from typing import Dict, List


class DiversePromptGenerator:
    """生成多样化的美国女性头像提示词"""

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

        # 美国女性族裔分布（真实反映美国人口）
        self.ethnicities = [
            # 白人（占比最高，60%）
            {"type": "Caucasian American", "skin": "fair skin", "weight": 0.60},
            {"type": "Caucasian American", "skin": "light tan skin", "weight": 0.60},

            # 拉丁裔（18%）
            {"type": "Latina American", "skin": "olive skin tone", "weight": 0.18},
            {"type": "Latina American", "skin": "warm bronze skin", "weight": 0.18},

            # 非裔（13%）
            {"type": "African American", "skin": "rich brown skin", "weight": 0.13},
            {"type": "African American", "skin": "deep caramel skin", "weight": 0.13},

            # 混血（9%）
            {"type": "mixed-race American", "skin": "sun-kissed skin", "weight": 0.09},
        ]

        # 年龄段
        self.ages = [
            "21", "22", "23", "24", "25", "26", "27", "28"
        ]

        # 脸型
        self.face_shapes = [
            "oval face", "heart-shaped face", "diamond face", "round face", "square face"
        ]

        # 眼睛颜色（美国常见）
        self.eye_colors = [
            "blue eyes", "green eyes", "hazel eyes", "brown eyes", "gray eyes"
        ]

        # 发型（多样化）- 更具体的样式
        self.hairstyles = [
            "long straight hair flowing past shoulders",
            "wavy shoulder-length brown hair",
            "straight silky hair cascading down back",
            "tousled beachy waves with texture",
            "high messy bun with loose strands",
            "sleek high ponytail pulled back tight",
            "loose romantic curls bouncing",
            "pin-straight hair with center part",
            "layered hair with face-framing pieces",
            "side-swept hair over one shoulder",
            "half-up half-down hairstyle",
            "low loose ponytail",
            "voluminous blow-dried hair",
            "textured shaggy layers",
        ]

        # 发色
        self.hair_colors = [
            "blonde", "light brown", "dark brown", "auburn", "black",
            "platinum blonde", "honey blonde", "chestnut brown", "caramel highlights"
        ]

        # 妆容（各种风格，可以组合）- 更具体的颜色和风格
        self.base_makeup = [
            "natural no-makeup look with bare skin",
            "fresh dewy skin with minimal foundation",
            "glowing radiant skin with highlighter",
            "soft everyday makeup with light coverage",
            "matte finish foundation with powder",
            "sun-kissed bronzed skin",
        ]

        self.eye_makeup = [
            # 可选，50%概率
            {"desc": "", "weight": 0.50},  # 无特殊眼妆
            {"desc": "sultry charcoal grey smoky eyes", "weight": 0.05},
            {"desc": "dramatic black smoky eye makeup", "weight": 0.05},
            {"desc": "sharp black winged eyeliner", "weight": 0.04},
            {"desc": "smoldering dark purple eye shadow", "weight": 0.035},
            {"desc": "shimmering gold glitter eyeshadow", "weight": 0.025},
            {"desc": "bronze metallic smoky eye", "weight": 0.025},
            {"desc": "classic cat eye with thick black liner", "weight": 0.025},
            {"desc": "vibrant blue eyeshadow", "weight": 0.015},
            {"desc": "warm copper eyeshadow", "weight": 0.02},
            {"desc": "dramatic false lashes with volume", "weight": 0.02},
            {"desc": "nude champagne eyeshadow with dark liner", "weight": 0.015},
            {"desc": "pink shimmer eyeshadow", "weight": 0.015},
            {"desc": "deep burgundy smoky eye", "weight": 0.015},
            {"desc": "silver glitter eyeshadow", "weight": 0.01},
        ]

        self.lip_makeup = [
            # 可选，40%概率
            {"desc": "", "weight": 0.60},  # 无特殊唇妆
            {"desc": "bold classic red lipstick", "weight": 0.04},
            {"desc": "deep wine red lips", "weight": 0.03},
            {"desc": "nude beige glossy lips", "weight": 0.035},
            {"desc": "soft pink glossy lips", "weight": 0.03},
            {"desc": "plump pink lips with gloss", "weight": 0.025},
            {"desc": "dark burgundy matte lipstick", "weight": 0.025},
            {"desc": "coral orange lip color", "weight": 0.02},
            {"desc": "matte dark brown lips", "weight": 0.02},
            {"desc": "shiny clear lip gloss", "weight": 0.03},
            {"desc": "mauve pink lipstick", "weight": 0.02},
            {"desc": "berry stained lips", "weight": 0.015},
            {"desc": "peachy nude lips", "weight": 0.015},
        ]

        self.cheek_makeup = [
            # 可选，30%概率
            {"desc": "", "weight": 0.70},
            {"desc": "rosy pink blush on cheeks", "weight": 0.05},
            {"desc": "bronzed contoured cheekbones", "weight": 0.045},
            {"desc": "champagne highlighted cheekbones", "weight": 0.045},
            {"desc": "peachy coral blush", "weight": 0.035},
            {"desc": "soft mauve blush", "weight": 0.025},
            {"desc": "golden shimmer highlighter on cheeks", "weight": 0.025},
            {"desc": "natural flush on cheeks", "weight": 0.025},
        ]

        # 身材（各种类型）
        self.body_types = [
            # 苗条 (25%)
            {"desc": "slender petite frame", "sexy": False, "weight": 0.13},
            {"desc": "slim graceful build", "sexy": False, "weight": 0.12},
            # 运动 (25%)
            {"desc": "toned athletic physique", "sexy": False, "weight": 0.13},
            {"desc": "fit sporty figure", "sexy": False, "weight": 0.12},
            # 丰满/曲线美 (35%)
            {"desc": "curvy hourglass figure", "sexy": True, "weight": 0.12},
            {"desc": "voluptuous shapely body", "sexy": True, "weight": 0.10},
            {"desc": "thick curvy build with full hips", "sexy": True, "weight": 0.08},
            {"desc": "plus-size curvy figure", "sexy": True, "weight": 0.05},
            # 健美 (15%)
            {"desc": "muscular toned physique", "sexy": False, "weight": 0.08},
            {"desc": "strong athletic build", "sexy": False, "weight": 0.07},
        ]

        # 纹身（各种样式和位置，30%概率）- 具体图案 + 性感位置
        self.tattoo_options = [
            {"has": False, "desc": "", "weight": 0.70},

            # 腰背纹身 - 具体图案 (8%)
            {"has": True, "desc": "sexy red rose tramp stamp tattoo on lower back", "weight": 0.01},
            {"has": True, "desc": "tribal butterfly wings tattoo across lower back", "weight": 0.01},
            {"has": True, "desc": "delicate cherry blossom branch tattoo on lower back", "weight": 0.008},
            {"has": True, "desc": "Chinese dragon tattoo curving along lower back", "weight": 0.008},
            {"has": True, "desc": "ornate mandala design tattoo on lower back", "weight": 0.008},
            {"has": True, "desc": "cursive quote script tattoo across lower back", "weight": 0.008},
            {"has": True, "desc": "phoenix rising tattoo on lower back", "weight": 0.008},
            {"has": True, "desc": "vine and rose pattern tattoo on lower back", "weight": 0.008},

            # 臀部和侧腰纹身 - 具体图案 (7%)
            {"has": True, "desc": "colorful koi fish tattoo on hip showing through clothing", "weight": 0.01},
            {"has": True, "desc": "black and grey lotus flower tattoo on exposed hip", "weight": 0.009},
            {"has": True, "desc": "geometric pattern tattoo wrapping around hip and waist", "weight": 0.008},
            {"has": True, "desc": "realistic hummingbird tattoo on side of hip", "weight": 0.008},
            {"has": True, "desc": "watercolor peony flower tattoo on hip bone", "weight": 0.008},
            {"has": True, "desc": "sugar skull tattoo on side hip", "weight": 0.007},
            {"has": True, "desc": "dreamcatcher tattoo dangling down hip", "weight": 0.007},
            {"has": True, "desc": "anchor with rope tattoo on hip", "weight": 0.007},

            # 大腿纹身 - 具体图案 (6%)
            {"has": True, "desc": "full thigh sleeve tattoo with Japanese geisha and cherry blossoms", "weight": 0.008},
            {"has": True, "desc": "realistic lion face tattoo on outer thigh", "weight": 0.008},
            {"has": True, "desc": "blooming rose bouquet tattoo covering thigh", "weight": 0.007},
            {"has": True, "desc": "ornate lace garter tattoo wrapping around thigh", "weight": 0.007},
            {"has": True, "desc": "geometric sacred geometry tattoo on thigh", "weight": 0.006},
            {"has": True, "desc": "tropical hibiscus flowers tattoo on thigh", "weight": 0.006},
            {"has": True, "desc": "detailed feather tattoo running down thigh", "weight": 0.006},
            {"has": True, "desc": "snake coiled around thigh tattoo", "weight": 0.006},

            # 胸部和肋骨纹身 - 具体图案 (4%)
            {"has": True, "desc": "delicate bird silhouettes tattoo under breast", "weight": 0.007},
            {"has": True, "desc": "ornamental sternum tattoo with mandala design", "weight": 0.007},
            {"has": True, "desc": "script quote tattoo along side rib cage", "weight": 0.006},
            {"has": True, "desc": "realistic rose with stem tattoo on ribs", "weight": 0.006},
            {"has": True, "desc": "tree of life tattoo on side ribs", "weight": 0.005},
            {"has": True, "desc": "musical notes flowing down rib cage tattoo", "weight": 0.005},

            # 肩部和锁骨纹身 - 具体图案 (3%)
            {"has": True, "desc": "dainty floral vine tattoo across shoulder blade", "weight": 0.006},
            {"has": True, "desc": "tiny constellation stars tattoo on collarbone", "weight": 0.006},
            {"has": True, "desc": "cursive name script tattoo along collarbone", "weight": 0.005},
            {"has": True, "desc": "minimalist mountain range tattoo on shoulder", "weight": 0.005},
            {"has": True, "desc": "vintage key tattoo on collarbone", "weight": 0.005},

            # 手臂和手部纹身 - 具体图案 (2%)
            {"has": True, "desc": "delicate bracelet chain tattoo around wrist", "weight": 0.005},
            {"has": True, "desc": "tiny heart tattoo on wrist", "weight": 0.004},
            {"has": True, "desc": "infinity symbol tattoo on inner wrist", "weight": 0.004},
            {"has": True, "desc": "small star cluster tattoo behind ear", "weight": 0.004},
            {"has": True, "desc": "crescent moon tattoo on ankle", "weight": 0.003},
        ]

        # 首饰（可选元素，增加多样性）- 更具体的材质和款式
        self.jewelry = [
            # 可选，40%概率
            {"desc": "", "weight": 0.60},
            {"desc": "delicate silver pendant necklace", "weight": 0.04},
            {"desc": "layered thin gold chain necklaces", "weight": 0.03},
            {"desc": "large gold hoop earrings", "weight": 0.03},
            {"desc": "small diamond stud earrings", "weight": 0.03},
            {"desc": "dangling crystal earrings", "weight": 0.02},
            {"desc": "chunky gold statement earrings", "weight": 0.02},
            {"desc": "black velvet choker necklace", "weight": 0.02},
            {"desc": "thin gold chain choker", "weight": 0.02},
            {"desc": "silver anklet with tiny charms", "weight": 0.015},
            {"desc": "gold anklet chain", "weight": 0.015},
            {"desc": "multiple stackable thin gold rings", "weight": 0.025},
            {"desc": "thick silver statement ring", "weight": 0.02},
            {"desc": "rose gold bangles stacked on wrist", "weight": 0.025},
            {"desc": "leather wrap bracelet", "weight": 0.02},
            {"desc": "beaded friendship bracelets", "weight": 0.015},
        ]

        self.hair_accessories = [
            # 可选，25%概率
            {"desc": "", "weight": 0.75},
            {"desc": "hair pulled back with velvet scrunchie", "weight": 0.025},
            {"desc": "hair tied with satin scrunchie", "weight": 0.025},
            {"desc": "thin black headband", "weight": 0.02},
            {"desc": "wide fabric headband", "weight": 0.02},
            {"desc": "pearl hair clip holding hair back", "weight": 0.02},
            {"desc": "claw hair clip", "weight": 0.02},
            {"desc": "thin white ribbon tied in hair", "weight": 0.015},
            {"desc": "red bandana tied as headband", "weight": 0.015},
            {"desc": "small white flower tucked in hair", "weight": 0.015},
            {"desc": "silk hair scarf tied around ponytail", "weight": 0.015},
        ]

        self.accessories = [
            # 可选，30%概率
            {"desc": "", "weight": 0.70},
            {"desc": "black aviator sunglasses resting on head", "weight": 0.025},
            {"desc": "white cat-eye sunglasses on head", "weight": 0.025},
            {"desc": "wearing oversized black sunglasses", "weight": 0.025},
            {"desc": "wearing trendy round sunglasses", "weight": 0.025},
            {"desc": "holding iced coffee in clear cup", "weight": 0.02},
            {"desc": "holding Starbucks cup", "weight": 0.02},
            {"desc": "holding red solo cup", "weight": 0.015},
            {"desc": "holding beer bottle", "weight": 0.015},
            {"desc": "holding iPhone in hand", "weight": 0.02},
            {"desc": "carrying small black leather purse", "weight": 0.02},
            {"desc": "carrying brown crossbody bag", "weight": 0.02},
            {"desc": "wearing silver smartwatch", "weight": 0.015},
            {"desc": "wearing Apple Watch", "weight": 0.015},
            {"desc": "holding black baseball cap", "weight": 0.015},
            {"desc": "wearing backwards baseball cap", "weight": 0.015},
        ]

        # 身体特征细节（可选，增加个性）
        self.body_features = [
            # 可选，30%概率
            {"desc": "", "weight": 0.70},
            {"desc": "toned abs visible", "weight": 0.05},
            {"desc": "long legs", "weight": 0.06},
            {"desc": "freckles on skin", "weight": 0.04},
            {"desc": "sun-kissed shoulders", "weight": 0.04},
            {"desc": "dimples when smiling", "weight": 0.03},
            {"desc": "beauty mark", "weight": 0.03},
            {"desc": "defined collarbone", "weight": 0.05},
        ]

        # 头发状态/细节
        self.hair_details = [
            # 可选，40%概率添加细节
            {"desc": "", "weight": 0.60},
            {"desc": "hair blowing in wind", "weight": 0.08},
            {"desc": "wet hair look", "weight": 0.05},
            {"desc": "messy tousled hair", "weight": 0.07},
            {"desc": "sleek shiny hair", "weight": 0.05},
            {"desc": "voluminous hair", "weight": 0.05},
            {"desc": "hair with beach waves", "weight": 0.05},
            {"desc": "perfectly styled hair", "weight": 0.05},
        ]

        # 服装（性感诱人，超级具体）- 大量不同款式
        self.outfits = [
            # 内衣风/性感睡衣 (25个款式)
            "black lace push-up bralette with adjustable straps and matching Brazilian-cut thong",
            "red satin camisole with lace trim and matching high-waisted panties",
            "white sheer mesh babydoll with ruffle hem and G-string underneath",
            "pink silk sleeveless camisole with spaghetti straps and matching boy shorts with lace edges",
            "black fishnet bodysuit with snap crotch and built-in underwire bra",
            "burgundy lace teddy with plunging V-neck and thong back",
            "nude seamless balconette bra with push-up padding and matching hipster panties",
            "silk kimono robe in deep purple hanging open revealing black lace bra and panty set",
            "white cotton triangle bralette and high-cut cheeky panties",
            "champagne satin slip dress with thin adjustable straps and lace bust detail",
            "emerald green silk chemise with lace hem hitting mid-thigh",
            "hot pink lace demi-cup bra with matching thong and garter belt",
            "black mesh bodysuit with cutout details and open back",
            "ivory bridal-style babydoll with sheer panels and pearl details",
            "navy blue satin corset with boning and matching panties",
            "coral lace bralette with strappy details and high-waisted brief",
            "silver metallic bra and panty set with chain details",
            "lavender silk robe tied loosely over matching cami and shorts",
            "crimson red lace-up bustier with garter straps and stockings",
            "peach satin nightgown with spaghetti straps and lace inserts",
            "mint green lace triangle bra and matching cheeky panty",
            "rose gold satin slip with cowl neckline and lace trim",
            "black leather harness bra and matching boy shorts",
            "turquoise mesh bralette and high-cut panties with scalloped edges",
            "yellow lace bodysuit with snap crotch and underwire cups",

            # 性感夜店装 (18个款式)
            "black ribbed bandage dress with high neckline and mid-thigh hemline hugging every curve",
            "red bodycon mini dress with deep plunging neckline showing cleavage and open back",
            "silver metallic halter neck mini dress with cutout waist and barely-there hem",
            "white fitted club dress with strategic mesh panel cutouts revealing skin",
            "emerald green satin cowl neck dress with open back and side slit",
            "hot pink strapless tube dress in stretchy fabric clinging to body",
            "black faux leather high-waisted mini skirt with zipper and matching crop bustier with boning",
            "gold sequined mini dress with spaghetti straps and low scoop back",
            "sheer black mesh overlay dress with nude bodysuit underneath and long sleeves",
            "royal blue velvet mini dress with sweetheart neckline and criss-cross back",
            "neon orange bodycon dress with one-shoulder strap and ruched sides",
            "burgundy satin slip dress with cowl neck and thigh-high slit",
            "purple holographic mini dress with racer back and low cut front",
            "champagne sequin halter dress with open back and mini hemline",
            "coral wrap dress with tie waist and plunging V-neckline",
            "mint green satin mini dress with thin straps and side cutouts",
            "rose gold metallic bodysuit worn as dress with belt",
            "ivory lace mini dress with nude lining and scalloped hem",

            # 性感上衣+超短下装 (20个款式)
            "tiny black ribbed crop top showing underboob and black leather micro mini skirt with zipper",
            "red floral lace bralette as top and distressed denim hot pants with frayed hem",
            "white off-shoulder elasticated crop top and high-waisted booty shorts in denim",
            "pink knit tube top with no straps and light blue denim micro shorts with button fly",
            "black fishnet long-sleeve top worn over neon sports bra and black faux leather mini skirt",
            "purple satin halter crop top tied at neck and high-waisted thong bikini bottoms visible above waistband",
            "sheer white mesh crop top with long sleeves over black triangle bra and leather short shorts with studs",
            "emerald green velvet bralette top and black vinyl mini skirt",
            "hot pink tie-front crop top and denim cutoffs with destroyed hem",
            "silver metallic crop tank and matching metallic micro shorts",
            "navy blue corset-style crop top with lace-up front and high-waisted leather shorts",
            "orange halter neck crop and white denim booty shorts with fringe",
            "burgundy lace crop cami and black satin shorts with lace trim",
            "yellow bandeau top wrapped around chest and ripped jean shorts",
            "turquoise mesh long sleeve crop over sports bra and bike shorts",
            "coral backless halter crop and pleated tennis skirt",
            "mint green ribbed crop tank and matching high-waisted thong showing",
            "lavender crop sweater cut short and black leather mini skirt with chain belt",
            "neon green sports bra crop and matching spandex shorts",
            "champagne silk cami crop and satin pajama shorts",

            # 泳装性感款 (15个款式)
            "red triangle bikini top with adjustable side-tie string bottoms showing hip bones",
            "black Brazilian thong bikini with minimal coverage and string ties",
            "white micro bikini with tiny triangle top and barely-there bottoms",
            "neon pink halter bikini top with push-up padding and cheeky Brazilian bottoms",
            "leopard print triangle bikini top with underwire and matching Brazilian cut bottoms",
            "one-piece black swimsuit with plunging neckline to navel and high-cut French legs",
            "hot pink string bikini with side-tie bottoms and triangle top",
            "navy blue bandeau bikini top with strapless design and high-cut bottoms",
            "emerald green high-neck bikini top and cheeky bottoms with strappy sides",
            "orange crochet bikini with triangle top and Brazilian bottoms",
            "purple metallic bikini with underwire top and thong bottom",
            "yellow halter bikini with tie-neck and scrunch-butt bottoms",
            "coral ribbed bikini with scoop neck top and high-waisted bottoms",
            "silver sequin bikini with triangle top and minimal coverage bottoms",
            "turquoise one-piece with cutouts at waist and low scoop back",

            # 透视蕾丝款 (12个款式)
            "black floral lace bodysuit completely see-through with thong back and snap crotch",
            "white crochet mini dress with large open weave revealing bikini underneath",
            "red mesh crop top with long sleeves showing black push-up bra clearly visible",
            "nude fishnet dress worn over matching lingerie set",
            "ivory lace bodysuit with sheer panels and visible bra underneath",
            "black mesh catsuit with strategic lace coverage only",
            "pink sheer organza robe over matching bra and panty set",
            "emerald green lace dress with nude lining cut very short",
            "white eyelet lace top completely see-through over nude bra",
            "burgundy mesh bodysuit with floral lace appliques barely covering",
            "silver metallic fishnet dress over black thong and bra",
            "coral sheer chiffon top with long sleeves over bralette",
        ]

        # 场景（性感诱人的日常场景）
        self.scenarios = [
            # 卧室场景 (35%)
            {
                "location": "bedroom laying on bed",
                "details": "messy sheets, pillows scattered, phone on nightstand, dim lighting",
                "lighting": "soft bedroom lamp glow"
            },
            {
                "location": "bedroom sitting on edge of bed",
                "details": "unmade bed, clothes on floor, intimate setting, casual mess",
                "lighting": "warm bedside light"
            },
            {
                "location": "bedroom floor mirror selfie",
                "details": "holding phone, full-length mirror, bed visible in background, personal items around",
                "lighting": "bedroom overhead light"
            },
            {
                "location": "bedroom leaning against headboard",
                "details": "relaxed in bed, pillows behind, cozy intimate atmosphere, sheets messy",
                "lighting": "natural window light filtering in"
            },
            {
                "location": "bedroom getting dressed",
                "details": "closet open, clothes scattered, mirror visible, private moment",
                "lighting": "bedroom ceiling light"
            },
            {
                "location": "bedroom late night",
                "details": "bed sheets rumpled, phone nearby, intimate private setting, dim room",
                "lighting": "low warm lamp light"
            },

            # 浴室场景 (30%)
            {
                "location": "bathroom mirror selfie",
                "details": "phone in hand, steam on mirror, towel hanging, toiletries visible",
                "lighting": "harsh bathroom mirror lights"
            },
            {
                "location": "bathroom after shower",
                "details": "wet hair, steamy mirror, towel nearby, droplets on skin",
                "lighting": "bright bathroom lighting"
            },
            {
                "location": "bathroom getting ready to go out",
                "details": "makeup scattered on counter, hair styling tools, phone charging, messy but sexy",
                "lighting": "vanity mirror lights"
            },
            {
                "location": "bathroom taking selfie",
                "details": "holding phone up, sink visible, personal care items around, casual moment",
                "lighting": "fluorescent bathroom light"
            },
            {
                "location": "hotel bathroom",
                "details": "fancy hotel setting, marble counter, bath products, luxurious but lived-in",
                "lighting": "hotel bathroom lighting"
            },

            # 酒吧/夜店场景 (20%)
            {
                "location": "at nightclub",
                "details": "dancing crowd in background, drinks nearby, dark sexy atmosphere, neon lights",
                "lighting": "colorful club lighting with shadows"
            },
            {
                "location": "sitting at bar counter",
                "details": "cocktail glass, bartender blurred, other patrons visible, intimate bar setting",
                "lighting": "dim bar mood lighting"
            },
            {
                "location": "VIP booth at club",
                "details": "bottle service table, velvet seating, friends blurred out, exclusive vibe",
                "lighting": "purple and blue club lights"
            },
            {
                "location": "bar bathroom mirror",
                "details": "touching up makeup, phone in hand, drinks visible on counter, going out vibe",
                "lighting": "flattering bar bathroom light"
            },

            # 派对场景 (10%)
            {
                "location": "house party bedroom",
                "details": "someone's bedroom, party sounds outside door, red cups, intimate setting",
                "lighting": "dim bedroom party lighting"
            },
            {
                "location": "college party",
                "details": "beer pong table visible, people in background, casual party atmosphere, solo cups",
                "lighting": "mixed party lighting"
            },

            # 车内性感场景 (5%)
            {
                "location": "backseat of car at night",
                "details": "sitting in backseat, dark outside, car interior, intimate moment",
                "lighting": "car interior light and street lights"
            },
            {
                "location": "front seat of car parked",
                "details": "sitting in passenger seat, car dashboard visible, private moment, window showing night",
                "lighting": "dashboard glow and outside lights"
            },
        ]

        # 拍摄景别（更专业的摄影术语）
        self.shot_types = [
            # 特写 (20%)
            "close-up portrait from shoulders up",
            "tight headshot focusing on face",
            # 半身 (30%)
            "medium shot from waist up",
            "upper body shot from chest up",
            "medium close-up from mid-torso up",
            # 四分之三身 (25%)
            "three-quarter length shot from thighs up",
            "three-quarter body from mid-thigh up",
            # 全身 (25%)
            "full body shot head to toe",
            "wide full-length shot",
            "full figure from knees up",
        ]

        # 姿势（性感挑逗）- 更具体的动作描述
        self.poses = [
            # 性感站姿 (35%)
            "sultry pose with right hand resting on hip accentuating curves",
            "seductive stance arching back slightly pushing chest forward",
            "provocative standing pose with chest out and shoulders back",
            "alluring pose running fingers through hair with head tilted",
            "confident sexy pose with one hand behind head stretching",
            "flirtatious standing with weight shifted to one hip",
            "enticing pose leaning shoulder against wall suggestively",
            "standing with one leg bent showing off curves",

            # 性感坐姿/躺姿 (30%)
            "sitting with legs elegantly crossed at knee showing thighs",
            "reclining seductively on side propped up on elbow",
            "kneeling pose looking back over shoulder with arched back",
            "sitting on edge with legs apart and leaning forward",
            "laying back on bed in inviting relaxed pose",
            "provocative seated position with knees bent",
            "sitting cross-legged on floor leaning back on hands",

            # 动态性感姿势 (25%)
            "turning head to look back over bare shoulder flirtatiously",
            "playfully biting lower lip with hand running through hair",
            "stretching arms up above head showing curves and midriff",
            "mid-motion while flipping hair back seductively",
            "leaning forward toward camera with sultry expression",
            "twisting torso to show off curves from side angle",

            # 挑逗姿势 (10%)
            "bending over slightly at waist looking up at camera",
            "pulling down tank top strap suggestively off shoulder",
            "teasing pose with index finger touching lips",
            "adjusting hair with both hands raised showing curves",
        ]

        # 表情（更性感）- 更具体的眼神和表情
        self.expressions = [
            # 性感 (50%)
            "sultry smoldering gaze with half-closed eyes",
            "seductive inviting look with parted lips",
            "flirtatious playful smile with eyes looking up",
            "alluring bedroom eyes with intense stare",
            "provocative half-smile with raised eyebrow",
            "sensual look with tongue touching lips",

            # 自信迷人 (30%)
            "confident captivating expression with direct eye contact",
            "bold fierce stare with strong eye contact",
            "mesmerizing intense gaze locked on camera",
            "self-assured smirk with chin slightly raised",

            # 温柔可爱 (20%)
            "sweet tempting smile with dimples showing",
            "soft inviting expression with gentle eyes",
            "playful cute smile with slight head tilt",
        ]

        # 画质/真实感关键词（必需，每张图都要有）- 暗光+噪点
        self.quality_keywords = [
            # 拍摄设备/风格（高权重，每张必选1-2个）
            {"desc": "Shot on iPhone at night", "weight": 0.30},
            {"desc": "low light phone photo", "weight": 0.25},
            {"desc": "dim lighting smartphone capture", "weight": 0.20},
            {"desc": "grainy night shot", "weight": 0.15},
            {"desc": "dark moody phone pic", "weight": 0.10},
        ]

        self.quality_effects = [
            # 背景效果（每张必选1个）
            {"desc": "messy background", "weight": 0.30},
            {"desc": "dim lighting", "weight": 0.25},
            {"desc": "dark shadows", "weight": 0.20},
            {"desc": "low key lighting", "weight": 0.15},
            {"desc": "underexposed", "weight": 0.10},
        ]

        self.camera_effects = [
            # 相机效果（暗光噪点，必选）
            {"desc": "motion blur", "weight": 0.25},
            {"desc": "film grain noise", "weight": 0.20},
            {"desc": "high ISO noise", "weight": 0.20},
            {"desc": "digital noise", "weight": 0.15},
            {"desc": "grainy texture", "weight": 0.10},
            {"desc": "visible noise pattern", "weight": 0.10},
        ]

    def _weighted_choice(self, items: List[Dict], weight_key: str = "weight") -> Dict:
        """根据权重随机选择"""
        weights = [item.get(weight_key, 1.0) for item in items]
        return self.rng.choices(items, weights=weights, k=1)[0]

    def generate_prompt(self, index: int) -> str:
        """生成单个多样化提示词"""
        # 设置随机种子以确保可重复性，但每个index不同
        self.rng.seed(42 + index)

        # 选择族裔和肤色
        ethnicity = self._weighted_choice(self.ethnicities)

        # 基本特征
        age = self.rng.choice(self.ages)
        face = self.rng.choice(self.face_shapes)
        eyes = self.rng.choice(self.eye_colors)
        hair_color = self.rng.choice(self.hair_colors)
        hairstyle = self.rng.choice(self.hairstyles)

        # 妆容（组合多个元素）
        base_makeup = self.rng.choice(self.base_makeup)
        eye_makeup = self._weighted_choice(self.eye_makeup)
        lip_makeup = self._weighted_choice(self.lip_makeup)
        cheek_makeup = self._weighted_choice(self.cheek_makeup)

        # 身材
        body = self._weighted_choice(self.body_types)

        # 可选元素
        tattoo = self._weighted_choice(self.tattoo_options)
        jewelry = self._weighted_choice(self.jewelry)
        hair_accessory = self._weighted_choice(self.hair_accessories)
        accessory = self._weighted_choice(self.accessories)
        body_feature = self._weighted_choice(self.body_features)
        hair_detail = self._weighted_choice(self.hair_details)

        # 服装
        outfit = self.rng.choice(self.outfits)

        # 场景
        scenario = self.rng.choice(self.scenarios)

        # 拍摄类型和姿势
        shot = self.rng.choice(self.shot_types)
        pose = self.rng.choice(self.poses)
        expression = self.rng.choice(self.expressions)

        # 画质关键词（必需！）
        # 每张图都必须有这些关键词：暗光+噪点+手机拍摄
        required_keywords = [
            "Shot on iPhone at night",
            "dim lighting",
            "film grain noise",
            "motion blur"
        ]

        # 可以额外随机添加0-2个其他画质关键词
        extra_quality = []
        num_extra = self.rng.choice([0, 1, 2])
        if num_extra > 0:
            available_extras = [kw["desc"] for kw in self.quality_keywords if kw["desc"] != "Shot on iPhone"]
            available_extras += [kw["desc"] for kw in self.quality_effects if kw["desc"] != "messy background"]
            available_extras += [kw["desc"] for kw in self.camera_effects if kw["desc"] not in ["", "motion blur"]]
            if available_extras:
                extra_quality = self.rng.sample(available_extras, k=min(num_extra, len(available_extras)))

        # 组装提示词
        prompt_parts = [
            # 开头形容词
            self.rng.choice(["stunning", "beautiful", "gorgeous", "attractive", "captivating", "alluring"]),

            # 族裔和年龄
            f"{ethnicity['type']} woman, age {age}",

            # 脸型和肤色
            f"{face}, {ethnicity['skin']}",

            # 眼睛
            eyes,

            # 发型和发色
            f"{hair_color} {hairstyle}",
        ]

        # 添加头发细节（如果有）
        if hair_detail['desc']:
            prompt_parts.append(hair_detail['desc'])

        # 添加头发配饰（如果有）
        if hair_accessory['desc']:
            prompt_parts.append(hair_accessory['desc'])

        # 基础妆容
        prompt_parts.append(base_makeup)

        # 添加眼妆（如果有）
        if eye_makeup['desc']:
            prompt_parts.append(eye_makeup['desc'])

        # 添加唇妆（如果有）
        if lip_makeup['desc']:
            prompt_parts.append(lip_makeup['desc'])

        # 添加腮红（如果有）
        if cheek_makeup['desc']:
            prompt_parts.append(cheek_makeup['desc'])

        # 身材
        prompt_parts.append(body['desc'])

        # 添加身体特征（如果有）
        if body_feature['desc']:
            prompt_parts.append(body_feature['desc'])

        # 添加纹身（如果有）
        if tattoo['has']:
            prompt_parts.append(tattoo['desc'])

        # 添加首饰（如果有）
        if jewelry['desc']:
            prompt_parts.append(jewelry['desc'])

        # 表情
        prompt_parts.append(expression)

        # 服装
        prompt_parts.append(f"wearing {outfit}")

        # 添加配饰（如果有）
        if accessory['desc']:
            prompt_parts.append(accessory['desc'])

        # 场景
        prompt_parts.append(f"at {scenario['location']}")
        prompt_parts.append(scenario['details'])

        # 拍摄和姿势
        prompt_parts.append(shot)
        prompt_parts.append(pose)

        # 灯光
        prompt_parts.append(scenario['lighting'])

        # 画质/真实感关键词（每张必须有这三个！）
        prompt_parts.extend(required_keywords)
        # 额外的画质关键词（可选）
        if extra_quality:
            prompt_parts.extend(extra_quality)

        # 质量标签
        prompt_parts.extend([
            "shallow depth of field",
            "bokeh background",
            "professional lifestyle photography",
            "high quality",
            "8k"
        ])

        # 用逗号连接
        prompt = ", ".join(prompt_parts)

        return prompt

    def generate_batch(self, num_prompts: int) -> List[str]:
        """批量生成提示词"""
        return [self.generate_prompt(i) for i in range(num_prompts)]


if __name__ == "__main__":
    # 测试生成
    generator = DiversePromptGenerator(seed=42)

    print("=" * 80)
    print("测试生成10个多样化提示词")
    print("=" * 80)

    for i in range(10):
        prompt = generator.generate_prompt(i)
        print(f"\n[提示词 {i}]")
        print(prompt)
        print()
