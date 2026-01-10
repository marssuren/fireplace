"""
暗月马戏团 - 法师
"""
from ..utils import *


##
# Minions

class DMF_100:
    """甜点飓风 - Confection Cyclone
    战吼：将两张1/2的糖元素牌置入你的手牌。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    play = Give(CONTROLLER, "DMF_100t") * 2


class DMF_100t:
    """糖元素 - Sugar Elemental"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
        GameTag.COST: 1,
        GameTag.CARDRACE: Race.ELEMENTAL,
    }


class DMF_101:
    """焰火元素 - Firework Elemental
    战吼：对一个随从造成3点伤害。腐蚀：改为造成12点伤害。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
    }
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3)
    corrupt = Hit(TARGET, 12)


class DMF_102:
    """游戏管理员 - Game Master
    你在每回合中打出的第一张奥秘牌的法力值消耗为(1)点。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    # 入场时给控制者添加追踪buff
    play = Buff(CONTROLLER, "DMF_102e")
    # 每回合开始时重新添加buff（如果随从还在场）
    events = OWN_TURN_BEGIN.on(Buff(CONTROLLER, "DMF_102e"))


class DMF_102e:
    """游戏管理员减费buff
    使手牌中的奥秘减费到1点，打出第一张奥秘后自动销毁。
    """
    # 刷新手牌中所有奥秘的费用为1点
    update = Refresh(FRIENDLY_HAND + SECRET, {GameTag.COST: SET(1)})
    # 打出奥秘后，销毁此buff（确保只有第一张奥秘享受减费）
    events = Play(CONTROLLER, SECRET).on(Destroy(SELF))


class DMF_106:
    """隐秘咒术师 - Occult Conjurer
    战吼：如果你控制一个奥秘，便召唤一个本随从的复制。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    play = (Find(FRIENDLY_SECRETS), Summon(CONTROLLER, ExactCopy(SELF)))


class DMF_109:
    """暗月先知塞格 - Sayge, Seer of Darkmoon
    战吼：抽一张牌。（你在本局对战中每触发一个友方奥秘，便升级一次！）
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 6,
    }
    
    # 战吼：抽牌数量 = 1 + 奥秘触发次数
    # 使用核心机制提供的 NUM_SECRETS_REVEALED 计数器
    # 该计数器从游戏开始就自动追踪，每次友方奥秘触发时自动累加
    def play(self):
        from ...enums import NUM_SECRETS_REVEALED
        # 获取本局对战中触发的友方奥秘次数（默认为0）
        secret_count = self.controller.tags.get(NUM_SECRETS_REVEALED, 0)
        # 抽牌数量 = 1 + 触发次数
        draw_count = 1 + secret_count
        # 抽牌
        for _ in range(draw_count):
            yield Draw(CONTROLLER)


class YOP_020:
    """冰川竞速者 - Glacier Racer
    法术迸发：对所有被冻结的敌人造成3点伤害。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    spellburst = Hit(ENEMY + FROZEN, 3)


##
# Spells

class DMF_103:
    """克苏恩面具 - Mask of C'Thun
    随机对所有敌人造成共10点伤害。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 8,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    play = Hit(RANDOM_ENEMY_CHARACTER, 1) * 10


class DMF_104:
    """华丽谢幕 - Grand Finale
    召唤一个8/8的元素。你在上个回合中每打出一张元素牌，便重复一次。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 8,
    }
    # 使用 fireplace 已有的 elemental_played_last_turn 计数器
    # 该计数器在每回合结束时自动更新
    play = Summon(CONTROLLER, "DMF_104t") * (Attr(CONTROLLER, "elemental_played_last_turn") + 1)


class DMF_104t:
    """元素 - Elemental"""
    tags = {
        GameTag.ATK: 8,
        GameTag.HEALTH: 8,
        GameTag.COST: 8,
        GameTag.CARDRACE: Race.ELEMENTAL,
    }


class DMF_105:
    """套圈圈 - Ring Toss
    发现一张奥秘牌并施放。腐蚀：改为发现2张。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.ARCANE,
    }
    # 使用核心的 DiscoverAndCastSecret 动作
    # 自动处理：重复检测、数量限制、发现、施放
    play = DiscoverAndCastSecret(CONTROLLER, cards=RandomCollectible(card_class=CardClass.MAGE, card_type=CardType.SPELL, secret=True))
    # 腐蚀版本:发现并施放2张奥秘
    corrupt = DiscoverAndCastSecret(CONTROLLER, cards=RandomCollectible(card_class=CardClass.MAGE, card_type=CardType.SPELL, secret=True)) * 2


class DMF_107:
    """非公平游戏 - Rigged Faire Game
    奥秘：如果你在对手的回合中没有受到任何伤害，便抽三张牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SECRET: True,
    }
    # 施放时给玩家添加追踪buff
    play = Buff(CONTROLLER, "DMF_107e")
    
    # 在对手回合结束时检查是否受到伤害
    def secret_trigger(self):
        # 检查是否受到伤害
        if not getattr(self.controller, "dmf_107_damaged", False):
            # 没有受到伤害,抽3张牌并揭示奥秘
            yield Draw(CONTROLLER) * 3
            yield Reveal(SELF)
    
    secret = EndTurn(OPPONENT).on(secret_trigger)


class DMF_107e:
    """非公平游戏追踪buff
    追踪对手回合中是否受到伤害。
    """
    def apply(self, target):
        # 初始化标记：未受到伤害
        target.dmf_107_damaged = False
    
    # 监听友方英雄受到伤害的事件
    def _reset_damage_flag(self):
        self.owner.dmf_107_damaged = False
    
    def _set_damage_flag(self):
        self.owner.dmf_107_damaged = True
    
    events = [
        # 对手回合开始时重置标记
        BeginTurn(OPPONENT).on(_reset_damage_flag),
        # 受到伤害时设置标记
        Damage(FRIENDLY_HERO).on(_set_damage_flag),
    ]


class DMF_108:
    """愚人套牌 - Deck of Lunacy
    将你牌库中的法术牌变形成为法力值消耗多(3)点的法术牌。（保留原本的法力值消耗。）
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.ARCANE,
    }
    
    # 使用自定义 play 方法实现"变形但保留费用"的复杂逻辑
    def play(self):
        # 获取牌库中的所有法术
        deck_spells = [card for card in self.controller.deck if card.type == CardType.SPELL]
        
        for spell in deck_spells:
            # 记录原费用
            original_cost = spell.cost
            # 目标费用 = 原费用 + 3
            target_cost = original_cost + 3
            
            # 查找费用为 target_cost 的随机法术
            from ..dsl.random_picker import RandomSpell
            new_spell_picker = RandomSpell(cost=target_cost)
            new_spell_cards = new_spell_picker.find_cards(self.controller)
            
            if not new_spell_cards:
                # 如果没有找到对应费用的法术，跳过
                continue
            
            # 随机选择一张
            import random
            new_spell_id = random.choice(new_spell_cards)
            
            # 变形
            yield Morph(spell, new_spell_id)
            
            # 获取变形后的卡牌（Morph 返回新卡牌）
            # 注意：Morph 会返回新卡牌，我们需要给它添加减费buff
            # 由于 Morph 的返回值，我们需要在变形后立即添加buff
            # 使用一个特殊的buff来永久减少费用
            morphed_card = spell.morphed  # 获取变形后的卡牌
            if morphed_card:
                # 添加永久减费buff，使费用恢复到原值
                # 减费量 = 目标费用 - 原费用 = 3
                yield Buff(morphed_card, "DMF_108e", cost=-3)


class DMF_108e:
    """愚人套牌减费buff
    永久减少3点费用，使变形后的法术保留原费用。
    """
    tags = {
        GameTag.COST: -3,
    }


class YOP_019:
    """制造法力饼干 - Conjure Mana Biscuit
    将一张饼干牌置入你的手牌，该牌可以使你恢复2个法力水晶。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.ARCANE,
    }
    play = Give(CONTROLLER, "YOP_019t")


class YOP_019t:
    """法力饼干 - Mana Biscuit"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 0,
    }
    play = ManaThisTurn(CONTROLLER, 2)
