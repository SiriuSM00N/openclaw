"""
黄金矿工 - 增益卡牌系统
2026-03-10 设计
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Callable
import random


# ==================== 稀有度定义 ====================

class Rarity(Enum):
    COMMON = "common"      # 普通 - 白色
    RARE = "rare"          # 稀有 - 蓝色
    EPIC = "epic"          # 史诗 - 紫色
    LEGENDARY = "legendary" # 传说 - 橙色


# 稀有度配置
RARITY_CONFIG = {
    Rarity.COMMON: {"color": "white", "weight": 50, "multiplier": 1.0},
    Rarity.RARE: {"color": "blue", "weight": 30, "multiplier": 1.5},
    Rarity.EPIC: {"color": "purple", "weight": 15, "multiplier": 2.5},
    Rarity.LEGENDARY: {"color": "orange", "weight": 5, "multiplier": 4.0},
}


# ==================== 卡牌类型定义 ====================

class CardType(Enum):
    HOOK = "hook"      # 钩子类
    ITEM = "item"      # 物品类
    TIME = "time"      # 时间类
    SPECIAL = "special" # 特殊类


# ==================== 卡牌数据类 ====================

@dataclass
class Card:
    """卡牌基类"""
    id: str
    name: str
    description: str
    card_type: CardType
    rarity: Rarity
    duration: float = 0  # 持续时间（秒），0=整局
    max_stacks: int = 1  # 最大叠加次数
    
    # 数值配置
    value_multiplier: float = 1.0  # 价值倍率
    speed_multiplier: float = 1.0  # 速度倍率
    length_multiplier: float = 1.0  # 长度倍率
    
    # 特殊效果
    effect_data: dict = field(default_factory=dict)
    
    def get_value_score(self) -> float:
        """计算卡牌价值分（用于平衡）"""
        config = RARITY_CONFIG[self.rarity]
        base_value = 100
        
        # 时长系数
        if self.duration > 0:
            duration_factor = 1 + (self.duration / 60)  # 每 60 秒 +1 系数
        else:
            duration_factor = 1.5  # 整局效果默认 1.5
        
        return base_value × config["multiplier"] × duration_factor


# ==================== 具体卡牌定义 ====================

def create_all_cards() -> List[Card]:
    """创建所有卡牌"""
    cards = []
    
    # --- 钩子类 ---
    cards.append(Card(
        id="hook_speed",
        name="快速钩",
        description="钩子速度 +50%",
        card_type=CardType.HOOK,
        rarity=Rarity.COMMON,
        speed_multiplier=1.5
    ))
    
    cards.append(Card(
        id="hook_length",
        name="加长钩",
        description="钩子长度 +30%",
        card_type=CardType.HOOK,
        rarity=Rarity.COMMON,
        length_multiplier=1.3
    ))
    
    cards.append(Card(
        id="double_hook",
        name="双钩",
        description="一次可以抓 2 个物品",
        card_type=CardType.HOOK,
        rarity=Rarity.RARE,
        duration=30,
        effect_data={"hook_count": 2}
    ))
    
    cards.append(Card(
        id="magnet_hook",
        name="磁力钩",
        description="自动吸附附近金块",
        card_type=CardType.HOOK,
        rarity=Rarity.RARE,
        duration=20,
        effect_data={"magnet_radius": 50}
    ))
    
    cards.append(Card(
        id="penetrate_hook",
        name="穿透钩",
        description="可穿透石头抓后方物品",
        card_type=CardType.HOOK,
        rarity=Rarity.EPIC,
        duration=15,
        effect_data={"can_penetrate": True}
    ))
    
    # --- 物品类 ---
    cards.append(Card(
        id="stone_to_gold",
        name="点石成金",
        description="石头变成金块（价值 50）",
        card_type=CardType.ITEM,
        rarity=Rarity.RARE,
        effect_data={"transform_stone": True, "max_count": 3, "gold_value": 50}
    ))
    
    cards.append(Card(
        id="double_value",
        name="双倍价值",
        description="所有物品价值 ×2",
        card_type=CardType.ITEM,
        rarity=Rarity.COMMON,
        value_multiplier=2.0
    ))
    
    cards.append(Card(
        id="gold_spawn",
        name="金块增生",
        description="金块生成数量 +50%",
        card_type=CardType.ITEM,
        rarity=Rarity.RARE,
        effect_data={"spawn_rate": 1.5}
    ))
    
    cards.append(Card(
        id="diamond_vein",
        name="钻石矿脉",
        description="生成 5 个钻石（价值 500）",
        card_type=CardType.ITEM,
        rarity=Rarity.EPIC,
        effect_data={"spawn_diamonds": 5, "diamond_value": 500}
    ))
    
    cards.append(Card(
        id="remove_stones",
        name="消除石头",
        description="移除场上所有石头",
        card_type=CardType.ITEM,
        rarity=Rarity.COMMON,
        effect_data={"remove_all_stones": True}
    ))
    
    # --- 时间类 ---
    cards.append(Card(
        id="time_freeze",
        name="时间暂停",
        description="时间停止流动",
        card_type=CardType.TIME,
        rarity=Rarity.RARE,
        duration=10,
        effect_data={"time_stopped": True}
    ))
    
    cards.append(Card(
        id="time_extend",
        name="时间延长",
        description="总时间 +30 秒",
        card_type=CardType.TIME,
        rarity=Rarity.COMMON,
        effect_data={"add_time": 30}
    ))
    
    cards.append(Card(
        id="slow_motion",
        name="慢动作",
        description="游戏速度 50%",
        card_type=CardType.TIME,
        rarity=Rarity.EPIC,
        duration=20,
        effect_data={"game_speed": 0.5}
    ))
    
    # --- 特殊类 ---
    cards.append(Card(
        id="lucky_hit",
        name="幸运一击",
        description="下次抓取必定暴击（×3 价值）",
        card_type=CardType.SPECIAL,
        rarity=Rarity.EPIC,
        effect_data={"crit_multiplier": 3, "crit_count": 1}
    ))
    
    cards.append(Card(
        id="treasure_radar",
        name="宝藏雷达",
        description="显示所有隐藏宝藏位置",
        card_type=CardType.SPECIAL,
        rarity=Rarity.RARE,
        effect_data={"show_treasures": True}
    ))
    
    return cards


# ==================== 卡牌管理器 ====================

class CardManager:
    """卡牌管理器"""
    
    def __init__(self):
        self.all_cards = create_all_cards()
        self.player_cards: List[Card] = []  # 玩家拥有的卡牌
        self.active_cards: List[Card] = []  # 当前局激活的卡牌
        self.card_levels: dict = {}  # 卡牌升级等级
    
    def draw_random_card(self, exclude_rarity: List[Rarity] = None) -> Card:
        """随机抽取一张卡牌（按稀有度权重）"""
        exclude_rarity = exclude_rarity or []
        
        # 过滤可选卡牌
        available_cards = [
            card for card in self.all_cards
            if card.rarity not in exclude_rarity
        ]
        
        # 按权重随机选择
        weights = [RARITY_CONFIG[card.rarity]["weight"] for card in available_cards]
        return random.choices(available_cards, weights=weights)[0]
    
    def draw_multiple_cards(self, count: int) -> List[Card]:
        """随机抽取多张卡牌（不重复）"""
        drawn_cards = []
        drawn_ids = set()
        
        for _ in range(count):
            # 过滤已抽取的卡牌
            available = [c for c in self.all_cards if c.id not in drawn_ids]
            if not available:
                break
            
            weights = [RARITY_CONFIG[c.rarity]["weight"] for c in available]
            card = random.choices(available, weights=weights)[0]
            drawn_cards.append(card)
            drawn_ids.add(card.id)
        
        return drawn_cards
    
    def add_card(self, card: Card):
        """添加卡牌到玩家卡组"""
        self.player_cards.append(card)
        if card.id not in self.card_levels:
            self.card_levels[card.id] = 1
    
    def upgrade_card(self, card_id: str) -> bool:
        """升级卡牌"""
        if card_id not in self.card_levels:
            return False
        
        current_level = self.card_levels[card_id]
        if current_level >= 5:  # 满级
            return False
        
        self.card_levels[card_id] = current_level + 1
        return True
    
    def get_upgrade_cost(self, card_id: str) -> int:
        """获取升级消耗"""
        level = self.card_levels.get(card_id, 1)
        costs = {1: 100, 2: 300, 3: 600, 4: 1000, 5: 9999}
        return costs.get(level, 9999)
    
    def activate_cards(self, selected_cards: List[Card]):
        """在关卡开始时激活选中的卡牌"""
        self.active_cards = selected_cards.copy()
    
    def get_active_effects(self, effect_type: str) -> list:
        """获取所有激活的指定类型效果"""
        effects = []
        for card in self.active_cards:
            if effect_type in card.effect_data:
                effects.append(card.effect_data[effect_type])
        return effects
    
    def calculate_value_multiplier(self) -> float:
        """计算总价值倍率"""
        multiplier = 1.0
        for card in self.active_cards:
            multiplier *= card.value_multiplier
        return multiplier
    
    def calculate_speed_multiplier(self) -> float:
        """计算总速度倍率"""
        multiplier = 1.0
        for card in self.active_cards:
            multiplier *= card.speed_multiplier
        return multiplier
    
    def calculate_length_multiplier(self) -> float:
        """计算总长度倍率"""
        multiplier = 1.0
        for card in self.active_cards:
            multiplier *= card.length_multiplier
        return multiplier


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 创建卡牌管理器
    manager = CardManager()
    
    print("=== 黄金矿工卡牌系统 ===\n")
    
    # 显示所有卡牌
    print(f"总卡牌数：{len(manager.all_cards)}\n")
    
    for rarity in Rarity:
        cards = [c for c in manager.all_cards if c.rarity == rarity]
        print(f"【{rarity.value.upper()}】{len(cards)}张")
        for card in cards:
            print(f"  - {card.name}: {card.description}")
        print()
    
    # 模拟抽卡
    print("=== 模拟抽卡（3 张）===")
    drawn = manager.draw_multiple_cards(3)
    for card in drawn:
        print(f"  抽到：{card.name} ({card.rarity.value})")
    
    # 计算价值倍率
    print("\n=== 激活卡牌效果 ===")
    manager.activate_cards(drawn)
    print(f"价值倍率：{manager.calculate_value_multiplier():.2f}x")
    print(f"速度倍率：{manager.calculate_speed_multiplier():.2f}x")
    print(f"长度倍率：{manager.calculate_length_multiplier():.2f}x")
