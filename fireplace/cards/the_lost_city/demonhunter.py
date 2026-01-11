"""
失落之城 - DEMON HUNTER
"""
from ..utils import *
from .kindred_helpers import check_kindred_active
from .map_helpers import mark_map_discovered_card, check_is_map_discovered_card


# COMMON

class DINO_136:
    """盛宴之角 - Feast Horn
    4费 法术
    召唤三只2/1并具有<b>突袭</b>的迅猛龙。<b>流放：</b>使其在本回合中获得攻击时<b>免疫</b>。
    
    Summon three 2/1 Raptors with Rush. Outcast: They are Immune while attacking this turn.
    """
    requirements = {}
    
    def play(self):
        # 检查是否为流放
        is_outcast = self.outcast
        
        # 召唤三只2/1突袭迅猛龙
        for _ in range(3):
            raptor = yield Summon(CONTROLLER, "DINO_136t")
            
            # 如果是流放，给迅猛龙添加攻击时免疫的buff
            if is_outcast and raptor:
                yield Buff(raptor[0], "DINO_136e")


class DINO_136e:
    """进食 - Feeding
    
    攻击时免疫（本回合）
    
    参考实现：paradise/warrior.py - DEEP_912e (溅射伤害)
    使用 IMMUNE_WHILE_ATTACKING 标签
    """
    tags = {
        GameTag.TAG_ONE_TURN_EFFECT: True,
        GameTag.IMMUNE_WHILE_ATTACKING: True,  # 攻击时免疫
    }


class DINO_137:
    """灵敏的厨师 - Nimble Chef
    3费 4/2 随从
    <b>战吼：</b>使相邻手牌的法力值消耗减少（1）点。
    
    Battlecry: Reduce the Cost of adjacent cards in your hand by (1).
    
    核心引擎支持：使用 _hand_position_when_played 属性（已在 actions.py 中扩展）
    """
    def play(self):
        # 获取当前手牌
        hand = list(self.controller.hand)
        
        # 获取打出前的手牌位置（核心引擎已在 Play action 中保存）
        if hasattr(self, '_hand_position_when_played'):
            pos = self._hand_position_when_played
            
            # 减少左边相邻卡牌的费用
            # 注意：由于卡牌已经打出，手牌索引会发生变化
            # 原位置 pos 的左边是 pos-1，但现在手牌中 pos-1 的位置实际上是原来的 pos-1
            # 原位置 pos 的右边是 pos+1，但现在手牌中 pos 的位置实际上是原来的 pos+1
            # 因为当前卡牌已经从手牌中移除
            
            # 左边相邻：原位置 pos-1，现在索引为 pos-1
            if pos > 0 and pos - 1 < len(hand):
                yield Buff(hand[pos - 1], "DINO_137e")
            
            # 右边相邻：原位置 pos+1，现在索引为 pos（因为当前卡牌已移除）
            if pos < len(hand):
                yield Buff(hand[pos], "DINO_137e")


class DINO_137e:
    """灵敏的厨师减费 - Nimble Chef Cost Reduction"""
    tags = {GameTag.COST: -1}


class TLC_840:
    """格里什掘洞虫 - Qiraji Burrower
    3费 2/4 随从
    <b>潜行</b>。在本随从攻击后，对敌方英雄造成2点伤害。
    
    Stealth. After this attacks, deal 2 damage to the enemy hero.
    """
    tags = {
        GameTag.STEALTH: True,
    }
    
    # 攻击后对敌方英雄造成2点伤害
    events = Attack.after(
        lambda self, source, target: source == self,
        lambda self, source, target: Hit(ENEMY_HERO, 2)
    )


class TLC_900:
    """虫巢地图 - Hive Map
    1费 法术
    <b>发现</b>一张邪能法术牌，如果你在本回合中使用该牌，再从其余选项中选择一张。
    
    Discover a Fel spell. If you play it this turn, pick from the other options.
    """
    requirements = {}
    
    def play(self):
        # 发现一张邪能法术牌
        cards = yield GenericChoice(CONTROLLER, cards=RandomCardGenerator(
            CONTROLLER,
            card_filter=lambda c: c.type == CardType.SPELL and c.spell_school == SpellSchool.FEL,
            count=3
        ))
        
        # 标记发现的卡牌
        if cards and self.controller.hand:
            discovered_card = self.controller.hand[-1]
            mark_map_discovered_card(self.controller, discovered_card.id)
            
            # 给玩家添加监听buff
            yield Buff(CONTROLLER, "TLC_900e")


class TLC_900e:
    """虫巢地图效果 - Hive Map Effect
    
    监听本回合打出地图发现的卡牌
    """
    tags = {
        GameTag.TAG_ONE_TURN_EFFECT: True,
    }
    
    # 监听玩家打出卡牌事件
    events = Play(CONTROLLER).after(
        lambda self, source, card: (
            check_is_map_discovered_card(self.controller, card.id)
            and [
                # 再次发现一张邪能法术牌
                GenericChoice(CONTROLLER, cards=RandomCardGenerator(
                    CONTROLLER,
                    card_filter=lambda c: c.type == CardType.SPELL and c.spell_school == SpellSchool.FEL,
                    count=3
                ))
            ]
        )
    )


class TLC_903:
    """异种虫女王 - Silithid Queen
    5费 5/2 随从
    <b>突袭</b>。<b>延系：</b>在本回合中，使你的英雄获得+5攻击力。
    
    Rush. Kindred: Give your hero +5 Attack this turn.
    """
    tags = {
        GameTag.RUSH: True,
    }
    
    def play(self):
        # 检查延系是否激活（上回合打出过恶魔或野兽）
        from hearthstone.enums import Race
        if check_kindred_active(self.controller, card_type=CardType.MINION, race=Race.DEMON) or \
           check_kindred_active(self.controller, card_type=CardType.MINION, race=Race.BEAST):
            # 给英雄+5攻击力（本回合）
            yield Buff(FRIENDLY_HERO, "TLC_903e")


class TLC_903e:
    """异种虫女王增益 - Silithid Queen Buff"""
    tags = {
        GameTag.TAG_ONE_TURN_EFFECT: True,
        GameTag.ATK: 5,
    }


# RARE

class DINO_138:
    """魔神暴龙 - Fel Tyrannosaurus
    6费 6/5 恶魔+野兽
    <b>延系：</b>对你的对手最左边和最右边的随从造成6点伤害。
    
    Kindred: Deal 6 damage to your opponent's left and right-most minions.
    """
    def play(self):
        # 检查延系是否激活（上回合打出过恶魔或野兽）
        from hearthstone.enums import Race
        if check_kindred_active(self.controller, card_type=CardType.MINION, race=Race.DEMON) or \
           check_kindred_active(self.controller, card_type=CardType.MINION, race=Race.BEAST):
            # 对对手最左边和最右边的随从造成6点伤害
            enemy_minions = self.controller.opponent.field
            
            if enemy_minions:
                # 对最左边的随从造成伤害
                yield Hit(enemy_minions[0], 6)
                
                # 如果有多个随从，对最右边的造成伤害
                if len(enemy_minions) > 1:
                    yield Hit(enemy_minions[-1], 6)


class TLC_633:
    """害虫克星 - Pest Exterminator
    4费 5/3 随从
    <b>战吼：</b>对一个具有随从类型的敌方随从造成6点伤害。
    
    Battlecry: Deal 6 damage to an enemy minion with a minion type.
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 检查目标是否有随从类型（种族）
        if TARGET and hasattr(TARGET, 'race'):
            from hearthstone.enums import Race
            # 检查是否有有效的种族（不是INVALID或ALL）
            if TARGET.race != Race.INVALID and TARGET.race != Race.ALL:
                yield Hit(TARGET, 6)


class TLC_833:
    """昆虫利爪 - Insect Claws
    3费 2/2 武器
    在你的英雄攻击后，召唤一只2/1并具有<b>突袭</b>的异种虫幼体。
    
    After your hero attacks, summon a 2/1 Silithid Hatchling with Rush.
    """
    # 监听英雄攻击事件
    events = Attack.after(
        lambda self, source, target: source == self.controller.hero,
        lambda self, source, target: Summon(CONTROLLER, "TLC_833t")
    )


class TLC_902:
    """虫害侵扰 - Infestation
    2费 法术
    获取两张法力值消耗为（1）的格里什毒刺虫。毒刺虫可以造成$2点伤害并召唤一只2/1具有<b>突袭</b>的异种虫幼体。
    
    Add two Qiraji Stingers to your hand that cost (1). They deal 2 damage and summon a 2/1 Silithid Hatchling with Rush.
    """
    requirements = {}
    
    def play(self):
        # 获取两张1费格里什毒刺虫
        yield Give(CONTROLLER, "TLC_902t")
        yield Give(CONTROLLER, "TLC_902t")


# EPIC

class TLC_630:
    """格里什异种虫 - Qiraji Silithid
    5费 2/7 随从
    <b>突袭</b>。每当本随从受到伤害，获取一张法力值消耗为（1）的格里什毒刺虫。
    
    Rush. Whenever this takes damage, add a Qiraji Stinger to your hand that costs (1).
    """
    tags = {
        GameTag.RUSH: True,
    }
    
    # 监听受到伤害事件
    events = Damage.on(
        lambda self, source, target, amount: target == self,
        lambda self, source, target, amount: Give(CONTROLLER, "TLC_902t")
    )


class TLC_901:
    """烟雾熏蒸 - Smoke Fumigation
    2费 法术 - 邪能学派
    对一个随从及所有相同类型的其他随从造成$3点伤害。
    
    Deal 3 damage to a minion and all other minions of the same type.
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 获取目标的种族
        if TARGET and hasattr(TARGET, 'race'):
            from hearthstone.enums import Race
            target_race = TARGET.race
            
            # 对目标造成伤害
            yield Hit(TARGET, 3)
            
            # 对所有相同类型的其他随从造成伤害
            if target_race != Race.INVALID and target_race != Race.ALL:
                for minion in ALL_MINIONS:
                    if minion != TARGET and hasattr(minion, 'race'):
                        # 检查是否有相同的种族
                        minion_races = getattr(minion, 'races', [minion.race])
                        if target_race in minion_races:
                            yield Hit(minion, 3)


# LEGENDARY

class TLC_631:
    """放出巨虫 - Release the Colossus
    1费 法术 - 任务
    <b>任务：</b>在你的回合对敌人造成刚好2点伤害，总计12次。<b>奖励：</b>格里什巨虫。
    
    Quest: Deal exactly 2 damage to enemies 12 times on your turns. Reward: Qiraji Colossus.
    """
    tags = {
        GameTag.QUEST: True,
    }
    
    def play(self):
        # 初始化任务进度
        self.controller.quest_progress = 0
        self.controller.quest_target = 12
        
        # 给玩家添加任务追踪buff
        yield Buff(CONTROLLER, "TLC_631e")


class TLC_631e:
    """放出巨虫任务追踪 - Release the Colossus Quest Tracker
    
    追踪在你的回合对敌人造成刚好2点伤害的次数
    
    参考实现：uldum/quest.py 中的任务追踪模式
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化进度计数器
        if not hasattr(self.controller, 'tlc_631_progress'):
            self.controller.tlc_631_progress = 0
    
    # 监听伤害事件
    events = Damage.after(
        lambda self, source, target, amount: (
            # 必须是在自己的回合
            self.game.current_player == self.controller and
            # 目标必须是敌方角色
            target.controller == self.controller.opponent and
            # 伤害必须刚好是2点
            amount == 2
        ),
        lambda self, source, target, amount: self._on_damage_dealt()
    )
    
    def _on_damage_dealt(self):
        """处理伤害事件"""
        # 增加进度
        self.controller.tlc_631_progress += 1
        
        # 检查是否完成任务
        if self.controller.tlc_631_progress >= 12:
            # 给玩家格里什巨虫
            yield Give(CONTROLLER, "TLC_631t")
            # 移除任务追踪
            yield Destroy(SELF)


class TLC_841:
    """昆虫学家托鲁 - Entomologist Toru
    8费 7/7 随从
    <b>战吼：</b>将你手牌中的每张随从牌分别放入法力值消耗为（1）的0/1的标本罐。打破罐子即可放出随从！
    
    Battlecry: Put each minion in your hand into a 1-Cost 0/1 Specimen Jar. Break the Jar to release the minion!
    """
    def play(self):
        # 获取手牌中的所有随从牌（排除自己）
        minions_in_hand = [c for c in self.controller.hand if c.type == CardType.MINION and c != self]
        
        for minion in minions_in_hand:
            # 保存随从的ID
            minion_id = minion.id
            
            # 移除手牌中的随从
            yield Destroy(minion)
            
            # 创建标本罐Token并加入手牌
            jar = yield Give(CONTROLLER, "TLC_841t")
            
            # 给标本罐添加buff，记录它包含的随从ID
            if jar:
                # 使用自定义属性存储随从ID
                jar[0]._contained_minion_id = minion_id
                yield Buff(jar[0], "TLC_841e")


class TLC_841e:
    """标本罐效果 - Specimen Jar Effect
    
    亡语：召唤罐子中的随从
    """
    @property
    def deathrattle(self):
        """动态亡语：召唤罐子中包含的随从"""
        if hasattr(self.owner, '_contained_minion_id'):
            minion_id = self.owner._contained_minion_id
            return [Summon(CONTROLLER, minion_id)]
        return None


# Token 定义已移至 tokens.py 文件
# 包括：DINO_136t, TLC_833t, TLC_902t, TLC_631t, TLC_841t
