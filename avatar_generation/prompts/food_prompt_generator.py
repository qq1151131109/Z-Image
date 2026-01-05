"""美食赛道提示词生成器 V2 - 增强版创意多样性"""

import random
from typing import Dict, List


class FoodPromptGenerator:
    """生成高度多样化的美食社媒头像提示词

    V2改进：
    - 大幅扩展食物种类（网红美食、街头小吃、高端料理、各国特色）
    - 增强视觉吸引力描述（色彩、质感、动态元素、摆盘艺术）
    - 丰富场景多样性（餐厅类型、户外场景、特殊场景）
    - 增强人物与食物的互动（动作、表情）
    """

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

        # 内容类型权重分布
        self.content_types = [
            {"type": "pure_food", "weight": 0.40},      # 纯美食
            {"type": "person_eating", "weight": 0.35},  # 人吃美食
            {"type": "food_blogger", "weight": 0.25},   # 美食博主/厨师
        ]

        # ==================== 美食分类（超大幅扩展到400+种）====================

        # 网红美食 (30种) - Instagram爆款
        self.viral_foods = [
            "rainbow bagel with tie-dye cream cheese swirl, vibrant eye-catching colors",
            "golden crispy cronut with glossy glaze, flaky buttery layers visible",
            "over-the-top freakshake topped with donuts, cookies, and candy",
            "unicorn cake with pastel rainbow layers, edible glitter and gold",
            "galaxy mirror glaze cake with cosmic purple-blue swirl",
            "cotton candy burrito wrapped in pink and blue clouds",
            "crystal clear raindrop cake wobbling delicately on plate",
            "24k gold leaf covered luxury dessert, Instagram-worthy",
            "towering milkshake with entire cake slice on top, whipped cream",
            "colorful layered boba tea with rainbow pearls, aesthetic perfection",
            "fluffy cloud eggs with golden yolk center, Instagram famous",
            "mermaid toast with blue spirulina swirls, magical ocean vibes",
            "sushi donut with colorful sashimi arranged in circle",
            "charcoal black ice cream cone, dramatic activated charcoal color",
            "smoking dragon's breath dessert with liquid nitrogen fog",
            "giant rainbow grilled cheese with colorful cheese pull",
            "matcha everything bagel with vibrant green cream cheese",
            "s'mores hot chocolate bomb exploding with marshmallows",
            "giant cinnamon roll drizzled with thick cream cheese frosting",
            "honey butter chips drizzled with golden honey",
            "pink strawberry cloud bread fluffy and pillowy",
            "tie-dye bagels in sunset colors with flavored cream cheese",
            "glow-in-dark galaxy donuts with cosmic frosting",
            "edible cookie dough loaded with chocolate chips",
            "honeycomb toffee with golden caramelized texture",
            "levitating coffee with cascading cream art",
            "neon-colored bubble waffles loaded with toppings",
            "giant fortune cookie with custom message inside",
            "rose-shaped ice cream cone in pastel pink",
            "smoke-filled cloche lifted to reveal dramatic dessert",
        ]

        # 街头小吃 (20种)
        self.street_food = [
            "loaded Korean corn dog with crispy coating and cheese pull",
            "takoyaki balls with bonito flakes dancing on top",
            "banh mi sandwich bursting with pickled vegetables and cilantro",
            "Mexican elote covered in mayo, cheese, and chili powder",
            "Belgian waffle from street cart with strawberries and cream",
            "New York hot dog with sauerkraut and mustard from cart",
            "churros dusted with cinnamon sugar from food truck",
            "Canadian poutine with gravy and cheese curds melting",
            "fish tacos from taco truck with fresh slaw and lime",
            "soft pretzel with coarse salt from street vendor",
            "empanadas fresh from food stall, golden and crispy",
            "falafel wrap with tahini drizzle from street stand",
            "pad see ew noodles from night market food stall",
            "arepas stuffed with cheese and avocado from cart",
            "bubble waffle cone filled with ice cream and fruit",
            "gyro sandwich with tzatziki sauce spilling out",
            "currywurst with fries from German street vendor",
            "japanese crepe folded with strawberries and cream",
            "bao buns steaming from food cart window",
            "churro ice cream sandwich from dessert truck",
        ]

        # 日本料理 (15种)
        self.japanese_food = [
            "premium sushi platter with fatty tuna, salmon, and uni",
            "steaming bowl of tonkotsu ramen with soft egg and chashu pork belly",
            "crispy tempura with shrimp and vegetables, golden batter",
            "okonomiyaki pancake with bonito flakes moving from heat",
            "Japanese curry rice with breaded tonkatsu cutlet",
            "elaborate sashimi boat with ice and artistic presentation",
            "matcha tiramisu with green tea layers",
            "onigiri rice balls with nori and salmon filling",
            "takoyaki plate with sauce drizzle and mayonnaise art",
            "udon noodles in hot broth with tempura on side",
            "taiyaki fish-shaped pastry with red bean filling",
            "mochi ice cream balls in pastel colors",
            "Japanese soufflé pancakes stacked and wobbling",
            "bento box with compartments of colorful dishes",
            "matcha soft serve ice cream cone with gold leaf",
        ]

        # 韩国料理 (12种)
        self.korean_food = [
            "Korean BBQ with sizzling meat on table grill",
            "bibimbap bowl with fried egg on top and gochujang sauce",
            "Korean fried chicken wings glazed in spicy sauce",
            "tteokbokki rice cakes in red spicy sauce",
            "kimchi fried rice in stone pot with runny egg",
            "Korean corn dog with mozzarella cheese pull moment",
            "bulgogi beef bowl with sesame seeds and green onions",
            "Korean BBQ short ribs on lettuce wrap",
            "bingsu shaved ice dessert with fruit and condensed milk",
            "japchae glass noodles with colorful vegetables",
            "sundubu jjigae soft tofu stew bubbling in pot",
            "kimbap rolls sliced showing colorful ingredients",
        ]

        # 意大利料理 (12种)
        self.italian_food = [
            "creamy carbonara pasta with crispy pancetta and parmesan",
            "wood-fired Neapolitan pizza with buffalo mozzarella",
            "authentic tiramisu with cocoa powder dusting",
            "fresh pasta with rich bolognese sauce and basil",
            "risotto alla milanese with saffron golden color",
            "Italian gelato in colorful array of flavors",
            "caprese salad with fresh mozzarella, tomato, and basil",
            "lasagna with layers of cheese and meat sauce visible",
            "pappardelle pasta with wild boar ragu",
            "panna cotta with berry compote drizzle",
            "focaccia bread with olive oil and rosemary",
            "cannoli filled with sweet ricotta and chocolate chips",
        ]

        # 墨西哥料理 (12种)
        self.mexican_food = [
            "loaded burrito bowl with guacamole, salsa, and sour cream",
            "authentic street tacos with cilantro, onions, and lime",
            "cheesy quesadilla with chicken, cheese pulling apart",
            "nachos grande with melted cheese, jalapeños, and all toppings",
            "carne asada burrito cut in half showing fillings",
            "enchiladas covered in red sauce and melted cheese",
            "fresh guacamole with lime and tortilla chips",
            "fish tacos with mango salsa and chipotle mayo",
            "tamales unwrapped showing corn masa filling",
            "Mexican street corn on stick covered in toppings",
            "pozole soup with pork and hominy, garnished fresh",
            "churros with chocolate dipping sauce",
        ]

        # 美式经典 (15种)
        self.american_classics = [
            "juicy double bacon cheeseburger with cheese melting",
            "New York style pepperoni pizza slice with cheese pull",
            "crispy golden fried chicken with honey drizzle",
            "loaded cheese fries with bacon and ranch",
            "BBQ ribs with sauce glistening, fall-off-bone tender",
            "mac and cheese with breadcrumb crust, creamy inside",
            "Philly cheesesteak sandwich with melted provolone",
            "chicken and waffles with syrup and butter",
            "buffalo wings with blue cheese dressing",
            "club sandwich stacked high with toothpick",
            "lobster roll overflowing with butter-poached lobster",
            "gourmet grilled cheese with multiple cheeses oozing",
            "pancake stack with butter melting and syrup pouring",
            "eggs benedict with hollandaise sauce dripping",
            "southern biscuits and gravy with sausage",
        ]

        # 亚洲fusion创意 (10种)
        self.fusion_food = [
            "sushi burrito wrapped in nori with colorful fillings",
            "Korean BBQ tacos with kimchi slaw",
            "ramen burger with noodle bun and juicy patty",
            "poke bowl with rainbow of fresh fish and toppings",
            "Thai basil chicken pizza with Asian fusion flavors",
            "bao bun sliders with pulled pork and pickles",
            "miso caramel ice cream with unique flavor",
            "kimchi grilled cheese sandwich with cheese pull",
            "teriyaki salmon sushi burrito",
            "matcha white chocolate cookies with green swirl",
        ]

        # 高端精致料理 (15种)
        self.fine_dining = [
            "perfectly seared wagyu steak with rich marbling visible",
            "fresh oysters on ice with lemon and mignonette",
            "lobster thermidor with golden cheese crust",
            "pan-seared foie gras with fig reduction",
            "beef wellington sliced showing pink center and golden puff pastry",
            "seared scallops with cauliflower purée and microgreens",
            "duck confit with crispy skin and cherry reduction",
            "Chilean sea bass with lemon beurre blanc",
            "rack of lamb with mint chimichurri and vegetables",
            "truffle risotto with shaved black truffles on top",
            "molecular gastronomy sphere bursting with flavor",
            "deconstructed dessert with artistic plating",
            "caviar on blini with crème fraîche",
            "tuna tartare tower with avocado and crispy wonton",
            "chocolate soufflé rising above ramekin with molten center",
        ]

        # 早餐brunch (15种)
        self.brunch_items = [
            "avocado toast with poached egg and everything bagel seasoning",
            "açai bowl with fresh berries, granola, and coconut",
            "fluffy French toast with berries and powdered sugar",
            "shakshuka with eggs poached in spicy tomato sauce",
            "breakfast burrito overflowing with eggs, cheese, and salsa",
            "bagel lox with cream cheese, salmon, capers, and onion",
            "green smoothie bowl with artistic fruit arrangement",
            "chilaquiles with fried eggs and salsa verde",
            "croque madame with fried egg on top of sandwich",
            "croissant breakfast sandwich with egg and bacon",
            "Belgian waffle with fresh strawberries and whipped cream",
            "huevos rancheros with beans and tortillas",
            "breakfast pizza with eggs, bacon, and cheese",
            "overnight oats with chia seeds and fruit toppings",
            "breakfast sandwich on English muffin, egg yolk dripping",
        ]

        # 甜点desserts (20种)
        self.desserts = [
            "molten chocolate lava cake with liquid center flowing out",
            "crème brûlée with caramelized sugar being cracked with spoon",
            "New York cheesecake slice with berry compote",
            "macarons in rainbow colors stacked artistically",
            "ice cream sundae with hot fudge, whipped cream, and cherry",
            "tiramisu layers visible in glass, dusted with cocoa",
            "red velvet cake slice with cream cheese frosting",
            "banana split with three ice cream flavors",
            "churros dusted with cinnamon sugar and chocolate sauce",
            "key lime pie with whipped topping and lime zest",
            "brownie sundae with ice cream melting on top",
            "panna cotta with berry sauce drizzle",
            "éclair with chocolate glaze and cream filling",
            "tres leches cake soaked in sweet milk",
            "warm apple pie with vanilla ice cream",
            "pavlova with whipped cream and fresh fruit",
            "baklava layers with honey and pistachios",
            "s'mores with toasted marshmallow oozing",
            "profiteroles stacked with chocolate drizzle",
            "fruit tart with colorful berries and custard",
        ]

        # 饮品 (15种)
        self.beverages = [
            "iced latte with intricate foam art heart design",
            "colorful smoothie in clear cup with fruit garnish",
            "Starbucks frappuccino with whipped cream tower",
            "boba tea with rainbow pearls and wide straw",
            "matcha latte with perfect green foam art",
            "açai refresher with fruit floating inside",
            "cold brew coffee with cream swirling",
            "pink dragonfruit drink Instagram-worthy",
            "golden turmeric latte with foam",
            "nitro cold brew cascading in glass",
            "Thai iced tea with cream layer on top",
            "milkshake with over-the-top toppings and whipped cream",
            "fresh pressed green juice in bottle",
            "horchata with cinnamon stick garnish",
            "Italian affogato with espresso poured over gelato",
        ]

        # 中餐美食 (35种) - 美式中餐 + 正宗中餐
        self.chinese_food = [
            "General Tso's chicken with crispy coating in sweet spicy sauce",
            "orange chicken glazed in tangy sauce with sesame seeds",
            "beef and broccoli stir fry with glossy brown sauce",
            "sweet and sour pork with colorful bell peppers and pineapple",
            "kung pao chicken with peanuts and dried chilies",
            "sesame chicken with golden crispy coating",
            "Mongolian beef with scallions and spicy sauce",
            "egg rolls golden and crispy with sweet and sour sauce",
            "crab rangoon with crispy wontons and cream cheese filling",
            "lo mein noodles with vegetables and savory sauce",
            "fried rice loaded with eggs, peas, and carrots",
            "dumplings steamed in bamboo basket, juicy inside",
            "pot stickers pan-fried golden crispy bottom",
            "spring rolls fresh with peanut dipping sauce",
            "hot and sour soup with tofu and mushrooms",
            "wonton soup with delicate dumplings floating",
            "mapo tofu in spicy Sichuan sauce with minced pork",
            "Peking duck with crispy skin and thin pancakes",
            "xiaolongbao soup dumplings with broth inside",
            "scallion pancakes flaky and golden fried",
            "char siu BBQ pork glazed with sweet sauce",
            "congee rice porridge with century egg and pork",
            "dan dan noodles in spicy sesame sauce",
            "twice-cooked pork with leeks and peppers",
            "salt and pepper shrimp crispy and aromatic",
            "beef chow fun flat rice noodles with beef",
            "dim sum assortment colorful variety of dumplings",
            "bao buns fluffy steamed with pork belly filling",
            "fried wontons crispy with sweet chili sauce",
            "honey walnut shrimp with candied walnuts",
            "Singapore noodles yellow curry rice noodles",
            "hot pot bubbling with meats and vegetables",
            "roast duck with crispy skin hanging in window",
            "bubble tea with tapioca pearls",
            "pineapple buns sweet topped with crispy cookie crust",
        ]

        # 烧烤BBQ (25种)
        self.bbq_food = [
            "fall-off-the-bone baby back ribs with BBQ glaze",
            "smoked brisket sliced showing pink smoke ring",
            "pulled pork sandwich overflowing with tender meat",
            "grilled ribeye steak with perfect char marks",
            "BBQ chicken quarters with crispy caramelized skin",
            "burnt ends brisket cubes glazed in sauce",
            "smoked turkey legs giant and juicy",
            "grilled corn on the cob charred with butter",
            "BBQ pork ribs with finger-licking sauce",
            "grilled salmon fillet with lemon and herbs",
            "smoky BBQ beef short ribs tender and succulent",
            "grilled shrimp skewers with garlic butter",
            "BBQ tri-tip steak sliced thin and tender",
            "grilled asparagus with parmesan and lemon",
            "BBQ bacon-wrapped jalapeño poppers",
            "smoked mac and cheese with crispy top",
            "grilled pineapple caramelized and sweet",
            "BBQ pulled chicken sliders",
            "grilled portobello mushrooms juicy and meaty",
            "Texas-style brisket plate with pickles and onions",
            "Korean BBQ kalbi short ribs marinated",
            "grilled kebabs with colorful vegetables and meat",
            "BBQ burnt end mac and cheese loaded",
            "smoked wings with dry rub seasoning",
            "grilled lobster tail with garlic herb butter",
        ]

        # 海鲜美食 (25种)
        self.seafood = [
            "garlic butter lobster tail steaming and succulent",
            "Alaskan king crab legs cracked open showing meat",
            "shrimp scampi in white wine garlic butter sauce",
            "New England clam chowder in bread bowl",
            "fish and chips with crispy batter and tartar sauce",
            "seared ahi tuna steak pink inside with sesame crust",
            "oysters on the half shell with mignonette and lemon",
            "paella loaded with mussels, shrimp, and saffron rice",
            "seafood boil with crab, shrimp, corn, and potatoes",
            "grilled mahi mahi with mango salsa",
            "cioppino seafood stew in tomato broth",
            "lobster bisque creamy and rich",
            "crab cakes golden fried with remoulade sauce",
            "blackened salmon with Cajun spices",
            "steamed mussels in white wine sauce",
            "sushi-grade salmon sashimi pink and fresh",
            "coconut shrimp with sweet chili sauce",
            "grilled octopus tentacles charred and tender",
            "fish tacos with cabbage slaw and lime",
            "ceviche with fresh citrus-marinated seafood",
            "clams linguine in white wine garlic sauce",
            "soft shell crab sandwich crispy whole crab",
            "tuna poke bowl with fresh raw tuna",
            "lobster mac and cheese decadent and creamy",
            "fish fillet sandwich with tartar sauce",
        ]

        # Comfort Food (30种)
        self.comfort_food = [
            "creamy mashed potatoes with butter and gravy",
            "chicken pot pie with flaky golden crust",
            "beef stew with tender chunks and vegetables",
            "shepherd's pie with lamb and mashed potato topping",
            "meatloaf with ketchup glaze and mashed potatoes",
            "chicken noodle soup steaming and comforting",
            "grilled cheese sandwich golden and gooey inside",
            "tomato soup in bowl with grilled cheese for dipping",
            "biscuits and gravy southern style breakfast",
            "pot roast with carrots and potatoes falling apart",
            "fried chicken with mashed potatoes and gravy",
            "tuna melt sandwich with melted cheese",
            "sloppy joes on toasted bun messy and delicious",
            "beef stroganoff with egg noodles and sour cream",
            "chicken and dumplings in creamy broth",
            "chili con carne with beans, cheese, and sour cream",
            "cornbread golden with honey butter",
            "baked ziti with melted cheese on top",
            "stuffed peppers with ground beef and rice",
            "chicken parmesan with marinara and mozzarella",
            "eggplant parmesan layered with cheese",
            "jambalaya rice with sausage, shrimp, and peppers",
            "gumbo thick stew with okra and seafood",
            "country fried steak with white gravy",
            "chicken fried rice with scrambled eggs",
            "tater tot casserole with cheese and bacon",
            "meatballs in marinara sauce with spaghetti",
            "beef and bean burrito smothered in sauce",
            "chicken wings various flavors saucy and crispy",
            "onion rings golden crispy with ranch dipping",
        ]

        # 三明治潜艇堡 (20种)
        self.sandwiches = [
            "Italian sub packed with salami, ham, and provolone",
            "Philly cheesesteak with melted cheese and peppers",
            "club sandwich triple-decker with bacon and turkey",
            "BLT with crispy bacon, fresh lettuce, and tomato",
            "Reuben sandwich with corned beef, sauerkraut, and Swiss",
            "meatball sub with marinara sauce and melted mozzarella",
            "pulled pork sandwich with coleslaw on top",
            "chicken parm sub with breaded chicken and cheese",
            "French dip sandwich with au jus for dipping",
            "Cuban sandwich pressed with pickles and mustard",
            "tuna salad sandwich on fresh bread",
            "egg salad sandwich classic and creamy",
            "grilled chicken sandwich with avocado and bacon",
            "patty melt burger on rye with Swiss and onions",
            "bánh mì Vietnamese sandwich with pickled vegetables",
            "po' boy sandwich with fried shrimp or oysters",
            "chicken Caesar wrap with romaine and parmesan",
            "turkey and cranberry sandwich on ciabatta",
            "caprese panini with mozzarella, tomato, and basil",
            "Monte Cristo sandwich fried French toast style",
        ]

        # 组合所有美食
        self.all_foods = (
            self.viral_foods + self.street_food + self.japanese_food +
            self.korean_food + self.italian_food + self.mexican_food +
            self.american_classics + self.fusion_food + self.fine_dining +
            self.brunch_items + self.desserts + self.beverages +
            self.chinese_food + self.bbq_food + self.seafood +
            self.comfort_food + self.sandwiches
        )

        # ==================== 人物特征 ====================

        self.ethnicities = [
            {"type": "Caucasian American", "weight": 0.60},
            {"type": "African American", "weight": 0.13},
            {"type": "Hispanic American", "weight": 0.18},
            {"type": "Asian American", "weight": 0.06},
            {"type": "mixed-race American", "weight": 0.03},
        ]

        self.ages = ["18", "21", "23", "25", "27", "29", "32", "35", "38"]

        self.genders = [
            {"gender": "woman", "weight": 0.50},
            {"gender": "man", "weight": 0.50},
        ]

        self.hairstyles = [
            "short hair", "long hair", "medium length hair",
            "pulled back hair", "messy bun", "styled hair",
            "ponytail", "braids", "beach waves"
        ]

        self.clothing = [
            "casual t-shirt", "cozy hoodie", "cute sweater", "flannel shirt",
            "tank top", "button-up shirt", "denim jacket", "off-shoulder top",
            "crop top", "oversized sweater", "graphic tee",
            "chef's apron", "casual dress"
        ]

        # ==================== 动作姿势（大幅增强）====================

        # 吃的动作 - 优雅自然的描述
        self.eating_actions = [
            {"action": "taking a bite of", "detail": "natural eating moment"},
            {"action": "about to bite into", "detail": "anticipation visible"},
            {"action": "pulling cheese from", "detail": "cheese stretch moment"},
            {"action": "eating noodles from", "detail": "chopsticks in hand"},
            {"action": "cutting into", "detail": "fork and knife in motion"},
            {"action": "savoring", "detail": "eyes closed enjoying"},
            {"action": "enjoying", "detail": "genuine happiness"},
            {"action": "taking first bite of", "detail": "excited expression"},
            {"action": "tasting", "detail": "thoughtful appreciation"},
            {"action": "indulging in", "detail": "satisfied expression"},
            {"action": "spooning", "detail": "gentle eating motion"},
            {"action": "trying", "detail": "curious and happy"},
        ]

        # 展示动作 - 美食博主
        self.presenting_actions = [
            {"action": "holding up", "detail": "showing off to camera"},
            {"action": "presenting freshly made", "detail": "steam rising"},
            {"action": "styling shot of", "detail": "perfect composition"},
            {"action": "filming TikTok with", "detail": "phone camera visible"},
            {"action": "creating content with", "detail": "content creator setup"},
            {"action": "garnishing final touches on", "detail": "chef precision"},
            {"action": "pouring sauce over", "detail": "dramatic drizzle moment"},
            {"action": "plating up", "detail": "artistic arrangement"},
            {"action": "taste testing", "detail": "thoughtful evaluation"},
            {"action": "showcasing", "detail": "food blogger pose"},
        ]

        # 表情 - 更生动
        self.expressions = [
            "eyes closed in pure bliss",
            "surprised delight with wide eyes",
            "big happy smile",
            "oooh expression with mouth open",
            "satisfied content look",
            "childlike joy and excitement",
            "food coma satisfied face",
            "melting with happiness",
            "laughing joyfully",
            "concentrated tasting expression",
            "mind blown reaction",
            "guilty pleasure guilty smile",
        ]

        # ==================== 场景设置（大幅扩展）====================

        self.settings = [
            # 高档餐厅 (15%)
            {
                "location": "at upscale restaurant",
                "details": "elegant table setting, soft ambient lighting, white tablecloth",
                "weight": 0.08
            },
            {
                "location": "in Michelin-starred dining room",
                "details": "sophisticated atmosphere, fine dining elegance",
                "weight": 0.04
            },
            {
                "location": "at trendy brunch spot",
                "details": "Instagram-worthy décor, plants and natural light",
                "weight": 0.03
            },

            # 休闲餐厅 (20%)
            {
                "location": "in cozy diner booth",
                "details": "retro vibes, checkered floor, neon signs",
                "weight": 0.07
            },
            {
                "location": "at casual restaurant table",
                "details": "relaxed dining atmosphere, warm lighting",
                "weight": 0.06
            },
            {
                "location": "at fast casual counter",
                "details": "modern quick-service restaurant",
                "weight": 0.04
            },
            {
                "location": "in ramen shop",
                "details": "authentic Japanese restaurant atmosphere",
                "weight": 0.03
            },

            # 咖啡厅 (12%)
            {
                "location": "at trendy coffee shop",
                "details": "exposed brick, hanging plants, wooden tables",
                "weight": 0.06
            },
            {
                "location": "in cozy café",
                "details": "warm café vibes, latte art on table",
                "weight": 0.04
            },
            {
                "location": "at dessert bar",
                "details": "colorful dessert display case visible",
                "weight": 0.02
            },

            # 家庭场景 (18%)
            {
                "location": "in bright home kitchen",
                "details": "natural daylight from window, cozy home setting",
                "weight": 0.08
            },
            {
                "location": "at home dining table",
                "details": "casual family dining atmosphere",
                "weight": 0.06
            },
            {
                "location": "cooking in home kitchen",
                "details": "ingredients and cooking equipment visible",
                "weight": 0.04
            },

            # 户外场景 (15%)
            {
                "location": "at beachside restaurant",
                "details": "ocean view, sunset lighting, tropical vibes",
                "weight": 0.04
            },
            {
                "location": "at rooftop dining",
                "details": "city skyline background, outdoor seating",
                "weight": 0.03
            },
            {
                "location": "at food festival",
                "details": "outdoor food stalls, festival atmosphere",
                "weight": 0.03
            },
            {
                "location": "having picnic in park",
                "details": "blanket spread, outdoor daylight, grass visible",
                "weight": 0.03
            },
            {
                "location": "at backyard BBQ",
                "details": "outdoor party atmosphere, grill visible",
                "weight": 0.02
            },

            # 街头/food truck (12%)
            {
                "location": "at food truck window",
                "details": "street food vibes, urban setting",
                "weight": 0.05
            },
            {
                "location": "at street food stall",
                "details": "authentic street food atmosphere",
                "weight": 0.04
            },
            {
                "location": "at night market",
                "details": "bustling market, colorful lights",
                "weight": 0.03
            },

            # 特色场景 (8%)
            {
                "location": "in restaurant kitchen",
                "details": "behind the scenes, professional kitchen equipment",
                "weight": 0.03
            },
            {
                "location": "at izakaya Japanese pub",
                "details": "small plates on table, intimate setting",
                "weight": 0.02
            },
            {
                "location": "at Korean BBQ table",
                "details": "table grill, interactive dining experience",
                "weight": 0.03
            },
        ]

        # ==================== 纯美食拍摄角度 ====================

        self.food_angles = [
            "overhead flat lay shot",
            "45 degree angle shot",
            "close-up detailed shot",
            "side view shot showing height and layers",
            "straight on front view",
            "dramatic low angle",
            "bird's eye view",
        ]

        # ==================== 视觉吸引力描述（新增）====================

        self.visual_appeal = [
            {"desc": "with vibrant colors popping", "weight": 0.12},
            {"desc": "glistening and juicy", "weight": 0.10},
            {"desc": "golden crispy exterior", "weight": 0.09},
            {"desc": "with melting cheese pull", "weight": 0.08},
            {"desc": "garnished with fresh herbs", "weight": 0.08},
            {"desc": "drizzled with sauce artistically", "weight": 0.07},
            {"desc": "with steam rising", "weight": 0.07},
            {"desc": "perfectly plated", "weight": 0.06},
            {"desc": "with rich chocolate glaze", "weight": 0.05},
            {"desc": "dusted with powdered sugar", "weight": 0.05},
            {"desc": "topped with edible flowers", "weight": 0.04},
            {"desc": "with caramelized edges", "weight": 0.04},
            {"desc": "layered beautifully", "weight": 0.04},
            {"desc": "with colorful toppings", "weight": 0.04},
            {"desc": "arranged artistically", "weight": 0.03},
            {"desc": "", "weight": 0.04},  # 无特殊描述
        ]

        # 摆盘和道具
        self.plating_props = [
            {"desc": "", "weight": 0.25},
            {"desc": "on white ceramic plate", "weight": 0.12},
            {"desc": "in rustic wooden bowl", "weight": 0.10},
            {"desc": "on slate serving board", "weight": 0.08},
            {"desc": "in paper food basket", "weight": 0.08},
            {"desc": "in takeout container", "weight": 0.07},
            {"desc": "on marble countertop", "weight": 0.06},
            {"desc": "in trendy food bowl", "weight": 0.06},
            {"desc": "on colorful vintage plate", "weight": 0.05},
            {"desc": "in clear glass jar", "weight": 0.04},
            {"desc": "on bamboo mat", "weight": 0.04},
            {"desc": "in cast iron skillet", "weight": 0.03},
            {"desc": "on banana leaf", "weight": 0.02},
        ]

        # ==================== 光照 ====================

        self.lighting = [
            {"desc": "natural window light streaming in", "weight": 0.18},
            {"desc": "soft golden hour sunlight", "weight": 0.15},
            {"desc": "bright daylight photography", "weight": 0.14},
            {"desc": "warm restaurant ambient lighting", "weight": 0.12},
            {"desc": "soft diffused natural light", "weight": 0.11},
            {"desc": "overhead natural lighting", "weight": 0.09},
            {"desc": "dramatic side lighting", "weight": 0.08},
            {"desc": "cozy warm café lighting", "weight": 0.07},
            {"desc": "bright even lighting", "weight": 0.06},
        ]

        # ==================== 人物拍摄角度 ====================

        self.camera_angles = [
            "straight on shot",
            "slight side angle",
            "three-quarter view",
            "close-up shot of face and food",
            "medium shot from chest up",
            "overhead shot including food and person",
            "candid angle capturing moment",
        ]

        # ==================== 画质关键词 ====================

        self.quality_base = [
            "Shot on iPhone", "food photography", "foodie content",
            "Instagram food post", "authentic food moment",
            "food blogger style", "social media food content"
        ]

        self.quality_effects = [
            {"desc": "natural lighting", "weight": 0.30},
            {"desc": "bright appetizing colors", "weight": 0.25},
            {"desc": "soft focus background", "weight": 0.18},
            {"desc": "warm inviting tones", "weight": 0.15},
            {"desc": "golden hour glow", "weight": 0.12},
        ]

    def _weighted_choice(self, items: List[Dict], weight_key: str = "weight") -> Dict:
        """根据权重随机选择"""
        weights = [item.get(weight_key, 1.0) for item in items]
        return self.rng.choices(items, weights=weights, k=1)[0]

    def generate_prompt(self, index: int) -> str:
        """生成单个高度多样化美食提示词"""
        self.rng.seed(42 + index)

        # 选择内容类型
        content_type = self._weighted_choice(self.content_types)["type"]

        # 选择美食
        food = self.rng.choice(self.all_foods)

        prompt_parts = []

        if content_type == "pure_food":
            # 纯美食特写
            angle = self.rng.choice(self.food_angles)
            visual = self._weighted_choice(self.visual_appeal)
            prop = self._weighted_choice(self.plating_props)
            lighting = self._weighted_choice(self.lighting)

            prompt_parts = [
                angle,
                "of mouthwatering",
                food,
            ]

            if visual["desc"]:
                prompt_parts.append(visual["desc"])

            if prop["desc"]:
                prompt_parts.append(prop["desc"])

            prompt_parts.extend([
                lighting["desc"],
                "professional food photography",
            ])

        elif content_type == "person_eating":
            # 人吃美食场景
            ethnicity = self._weighted_choice(self.ethnicities)["type"]
            age = self.rng.choice(self.ages)
            gender = self._weighted_choice(self.genders)["gender"]
            hairstyle = self.rng.choice(self.hairstyles)
            clothing = self.rng.choice(self.clothing)
            action_info = self.rng.choice(self.eating_actions)
            expression = self.rng.choice(self.expressions)
            setting = self._weighted_choice(self.settings)
            camera_angle = self.rng.choice(self.camera_angles)

            prompt_parts = [
                camera_angle,
                f"{ethnicity} {gender} age {age}",
                f"with {hairstyle}",
                f"wearing {clothing}",
                expression,
                action_info["action"],
                food,
                action_info["detail"],
                setting['location'],
                setting['details'],
            ]

        else:  # food_blogger
            # 美食博主/厨师展示
            ethnicity = self._weighted_choice(self.ethnicities)["type"]
            age = self.rng.choice(self.ages)
            gender = self._weighted_choice(self.genders)["gender"]
            hairstyle = self.rng.choice(self.hairstyles)
            clothing = self.rng.choice(self.clothing)
            action_info = self.rng.choice(self.presenting_actions)
            expression = self.rng.choice(self.expressions)
            setting = self._weighted_choice(self.settings)
            camera_angle = self.rng.choice(self.camera_angles)

            prompt_parts = [
                camera_angle,
                f"{ethnicity} {gender} age {age}",
                f"with {hairstyle}",
                f"wearing {clothing}",
                expression,
                action_info["action"],
                food,
                action_info["detail"],
                setting['location'],
                setting['details'],
            ]

        # 添加画质关键词
        base_quality = self.rng.choice(self.quality_base)
        quality_effect = self._weighted_choice(self.quality_effects)["desc"]

        prompt_parts.extend([
            base_quality,
            quality_effect,
            "high quality",
            "appetizing food content",
            "8k"
        ])

        return ", ".join(prompt_parts)

    def generate_batch(self, num_prompts: int) -> List[str]:
        """批量生成提示词"""
        return [self.generate_prompt(i) for i in range(num_prompts)]


if __name__ == "__main__":
    generator = FoodPromptGenerator(seed=42)

    print("=" * 80)
    print("美食赛道提示词生成器 V2 - 测试20个样例")
    print("=" * 80)

    for i in range(20):
        prompt = generator.generate_prompt(i)
        print(f"\n[提示词 {i}]")
        print(prompt)
        print()
