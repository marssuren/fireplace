"""
失落之城 - WARLOCK
"""
from ..utils import *
from .kindred_helpers import check_kindred_active
from ...enums import HEALTH_COST


# COMMON

class DINO_402:
    """蝙蝠面具 - Bat Mask
    Transform a friendly minion into a 1/1. Fill your board with copies of it.

    8费 法术
    将一个友方随从的属性值变为1/1。用它的复制填满你的面板。

    实现说明:
    - 选择一个友方随从
    - 将其变为1/1（使用Buff）
    - 计算场上剩余空位
    - 召唤该随从的复制（保持1/1状态）
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    def play(self):
        # 将目标变为1/1
        yield Buff(TARGET, "DINO_402e")
        # 计算剩余空位（最多7个随从）
        available_space = 7 - len(self.controller.field)
        # 召唤复制（已经是1/1了）
        if available_space > 0:
            yield Summon(CONTROLLER, ExactCopy(TARGET)) * available_space


class TLC_447:
    """烧蚀毒雾 - Ablative Miasma
    Destroy an enemy minion. <b>Kindred:</b> Deal $2 damage to all minions.

    4费 邪能法术
    消灭一个敌方随从。<b>延系：</b>对所有随从造成$2点伤害。

    实现说明:
    - 消灭目标敌方随从
    - 检查 Kindred 是否激活（上回合打出过邪能法术）
    - 如果激活，对所有随从造成2点伤害
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    def play(self):
        # 消灭目标敌方随从
        yield Destroy(TARGET)
        # 检查 Kindred 是否激活（邪能法术）
        from hearthstone.enums import CardType, SpellSchool
        kindred_count = check_kindred_active(self.controller, card_type=CardType.SPELL, spell_school=SpellSchool.FEL)
        # 如果激活，对所有随从造成2点伤害（可能触发多次）
        for _ in range(kindred_count):
            yield Hit(ALL_MINIONS, 2)


class TLC_450:
    """洞穴专家 - Cave Expert
    <b>Battlecry:</b> Your next <b>Temporary</b> card costs (2) less.

    2费 2/3 随从
    <b>战吼：</b>你的下一张<b>临时</b>牌的法力值消耗减少（2）点。

    实现说明:
    - 战吼：给予控制者一个buff
    - 该buff会监听下一张临时牌的使用
    - 使其减少2费
    """
    requirements = {}

    def play(self):
        # 给予控制者减费buff
        yield Buff(CONTROLLER, "TLC_450e")


class TLC_469:
    """坑道恐怪 - Tunnel Horror
    <b>Deathrattle:</b> Get two random <b>Temporary</b> 2-Cost minions.

    3费 2/3 野兽
    <b>亡语：</b>随机获取两张<b>临时</b>的法力值消耗为（2）的随从牌。

    实现说明:
    - 亡语：随机获取2张2费随从牌
    - 手动标记为临时牌（RandomCard 不支持 temporary 参数）
    """
    def deathrattle(self):
        """动态亡语：获取2张临时2费随从并标记为临时"""
        # 获取第一张2费随从
        yield RandomCard(CONTROLLER, card_filter=lambda c: c.type == CardType.MINION and c.cost == 2)
        if self.controller.hand:
            self.controller.hand[-1].tags[GameTag.TEMPORARY] = True

        # 获取第二张2费随从
        yield RandomCard(CONTROLLER, card_filter=lambda c: c.type == CardType.MINION and c.cost == 2)
        if self.controller.hand:
            self.controller.hand[-1].tags[GameTag.TEMPORARY] = True


# RARE

class DINO_131:
    """着魔的动物术师 - Possessed Animalist
    <b>Deathrattle:</b> Summon a random Beast from your deck. Give it <b>Lifesteal</b>.

    5费 2/2 随从（迷你集）
    <b>亡语：</b>随机从你的牌库中召唤一只野兽。使其获得<b>吸血</b>。

    实现说明:
    - 亡语：从牌库中随机选择一只野兽
    - 召唤该野兽
    - 给予其吸血能力
    """
    @property
    def deathrattle(self):
        """动态亡语：召唤牌库中的随机野兽并给予吸血"""
        # 获取牌库中的野兽
        deck_beasts = [c for c in self.controller.deck if c.type == CardType.MINION and Race.BEAST in getattr(c, 'races', [c.race] if hasattr(c, 'race') else [])]

        if deck_beasts:
            import random
            beast = random.choice(deck_beasts)
            # 召唤野兽并给予吸血
            return [
                Summon(CONTROLLER, beast.id),
                Buff(Find(FRIENDLY_MINIONS + LAST_SUMMONED), "DINO_131e")
            ]
        return []


class DINO_132:
    """绝息剑龙 - Suffocating Saurolisk
    <b>Taunt</b>. At the end of your turn, deal 5 damage to a random enemy minion.

    8费 6/12 恶魔+野兽（迷你集）
    <b>嘲讽</b>。在你的回合结束时，随机对一个敌方随从造成5点伤害。

    实现说明:
    - 嘲讽标签
    - 回合结束时触发效果
    - 对随机敌方随从造成5点伤害
    """
    tags = {
        GameTag.TAUNT: True,
    }

    events = OWN_TURN_END.on(
        Hit(RANDOM_ENEMY_MINION, 5)
    )


class TLC_449:
    """血瓣群系 - Bloodpetal Colony
    <b>Discover</b> a <b>Temporary</b> 1-Cost minion.

    1费 地标 2耐久
    <b>发现</b>一张<b>临时</b>的法力值消耗为（1）的随从牌。

    实现说明:
    - 地标激活时发现1费随从
    - 发现的卡牌自动带有临时标签
    """
    requirements = {}

    def activate(self):
        # 发现1费随从（临时）
        yield GenericChoice(CONTROLLER, RandomCardGenerator(
            CONTROLLER,
            card_filter=lambda c: c.type == CardType.MINION and c.cost == 1,
            count=3
        ))
        # 给予临时标签
        if self.controller.hand:
            discovered_card = self.controller.hand[-1]
            discovered_card.tags[GameTag.TEMPORARY] = True


class TLC_466:
    """拉卡利的故事 - Lakkari's Tale
    At the end of your turn, discard a card and fill your board with 3/2 Imps. Lasts 3 turns.

    7费 法术
    在你的回合结束时，弃一张牌并用3/2的小鬼填满你的面板。持续3回合。

    实现说明:
    - 给予控制者一个buff，持续3回合
    - 每回合结束时：弃一张随机手牌，然后召唤3/2小鬼填满场地
    """
    requirements = {}

    def play(self):
        # 给予控制者持续3回合的buff
        yield Buff(CONTROLLER, "TLC_466e")


class TLC_479:
    """死烂巨口 - Rotmouth
    <b>Taunt</b>. <b>Deathrattle:</b> Summon a random Fel Beast.

    6费 4/8 随从
    <b>嘲讽</b>。<b>亡语：</b>随机召唤一只邪能野兽。

    实现说明:
    - 嘲讽标签
    - 亡语：从邪能野兽池中随机召唤一只（TLC_446t2, TLC_446t3, TLC_446t4）
    """
    tags = {
        GameTag.TAUNT: True,
    }

    @property
    def deathrattle(self):
        """动态亡语：随机召唤一只邪能野兽"""
        import random
        # 邪能野兽池：邪能啸天者、邪能迅猛龙、邪能恐角龙
        fel_beasts = ["TLC_446t2", "TLC_446t3", "TLC_446t4"]
        chosen_beast = random.choice(fel_beasts)
        return [Summon(CONTROLLER, chosen_beast)]


# EPIC

class TLC_451:
    """咒怨之墓 - Tomb of Curses
    <b>Discover</b> a card from your deck. Make it <b>Temporary</b>.

    0费 邪能法术
    从你的牌库中<b>发现</b>另一张牌，将其变为<b>临时</b>卡牌。

    实现说明:
    - 从牌库中发现一张牌（3选1）
    - 将发现的牌变为临时卡牌
    """
    requirements = {}

    def play(self):
        # 从牌库中随机选择3张牌进行发现
        if len(self.controller.deck) > 0:
            yield GenericChoice(CONTROLLER, RandomCardGenerator(
                CONTROLLER,
                card_filter=lambda c: c in self.controller.deck,
                count=min(3, len(self.controller.deck))
            ))
            # 给予发现的牌临时标签
            if self.controller.hand:
                discovered_card = self.controller.hand[-1]
                discovered_card.tags[GameTag.TEMPORARY] = True


class TLC_467:
    """低语之石 - Whispering Stone
    <b>Taunt</b>. <b>Deathrattle:</b> Get 2 random Fel spells. They cost Health instead of Mana.

    5费 0/8 随从
    <b>嘲讽</b>。<b>亡语：</b>随机获取2张邪能法术牌。这些牌会消耗生命值，而非法力值。

    实现说明:
    - 嘲讽标签
    - 亡语：随机获取2张邪能法术
    - 给予这些法术特殊buff，使其消耗生命值而非法力值
    """
    tags = {
        GameTag.TAUNT: True,
    }

    def deathrattle(self):
        from hearthstone.enums import SpellSchool
        # 随机获取2张邪能法术
        for _ in range(2):
            yield RandomCard(CONTROLLER, card_filter=lambda c: c.type == CardType.SPELL and getattr(c, 'spell_school', None) == SpellSchool.FEL)
        # 给予最后2张手牌特殊buff（消耗生命值）
        if len(self.controller.hand) >= 2:
            yield Buff(self.controller.hand[-2], "TLC_467e")
            yield Buff(self.controller.hand[-1], "TLC_467e")


# LEGENDARY

class TLC_446:
    """逃离邪能地窟 - Escape the Fel Grotto
    <b>Quest:</b> Play 6 <b>Temporary</b> cards. <b>Reward:</b> Fel Grotto Rift.

    1费 任务法术 传说
    <b>任务：</b>使用6张<b>临时</b>牌。<b>奖励：</b>邪能地窟裂隙。

    实现说明:
    - 任务：追踪临时牌的使用次数
    - 当使用6张临时牌后，完成任务
    - 奖励：邪能地窟裂隙（TLC_446t）
    """
    progress_total = 6

    # 监听打出临时牌的事件
    quest = Play(CONTROLLER, FRIENDLY + TEMPORARY).after(
        AddProgress(SELF, Play.CARD)
    )

    # 任务完成后的奖励
    reward = Give(CONTROLLER, "TLC_446t")


class TLC_463:
    """雷兹迪尔 - Rezdyr
    <b>Battlecry:</b> Discard a random card. <b>Kindred:</b> Discard one from your opponent's hand instead.

    4费 4/7 恶魔+野兽 传说
    <b>战吼：</b>随机弃掉一张手牌。<b>延系：</b>改为对手的一张手牌。

    实现说明:
    - 战吼：检查 Kindred 是否激活（上回合打出过恶魔或野兽）
    - 如果激活：弃掉对手的一张随机手牌
    - 如果未激活：弃掉自己的一张随机手牌
    """
    requirements = {}

    def play(self):
        from hearthstone.enums import CardType
        # 检查 Kindred 是否激活（恶魔或野兽）
        kindred_demon = check_kindred_active(self.controller, card_type=CardType.MINION, race=Race.DEMON)
        kindred_beast = check_kindred_active(self.controller, card_type=CardType.MINION, race=Race.BEAST)
        kindred_count = max(kindred_demon, kindred_beast)

        if kindred_count > 0:
            # Kindred 激活：弃掉对手的手牌
            for _ in range(kindred_count):
                if self.controller.opponent.hand:
                    yield Discard(RANDOM(ENEMY_HAND))
        else:
            # Kindred 未激活：弃掉自己的手牌
            if self.controller.hand:
                yield Discard(RANDOM(FRIENDLY_HAND))


# Token 定义已移至 tokens.py 文件
# 包括：
# - DINO_402e (蝙蝠面具附魔 - 1/1)
# - DINO_131e (吸血附魔)
# - TLC_450e (洞穴专家减费效果)
# - TLC_466e (拉卡利的故事持续效果)
# - TLC_467e (石之低语生命值消耗)
# - TLC_466t (小鬼 - 3/2)
# - TLC_446t (邪能地窟裂隙法术)
# - TLC_446t1 (邪能地窟裂隙随从)
# - TLC_446t2 (邪能啸天龙 - 5/3 突袭+吸血)
# - TLC_446t3 (邪能迅猛龙 - 4/4 冲锋+扰魔)
# - TLC_446t4 (邪能恐角龙 - 3/5 嘲讽+复生)
