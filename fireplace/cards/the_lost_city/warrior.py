"""
失落之城 - WARRIOR
"""
from ..utils import *
from .kindred_helpers import check_kindred_active


# COMMON

class DINO_433:
    """守卫执勤
    随机召唤法力值消耗为（6），（4）和（2）的<b>嘲讽</b>随从各一个。
    """
    # Type: SPELL | Cost: 7 | Rarity: COMMON
    def play(self):
        # 随机召唤3个不同费用的嘲讽随从
        # 6费嘲讽随从
        taunt_6 = yield RandomCollectible(CONTROLLER, MINION + TAUNT + (COST == 6))
        if taunt_6:
            yield Summon(CONTROLLER, taunt_6)

        # 4费嘲讽随从
        taunt_4 = yield RandomCollectible(CONTROLLER, MINION + TAUNT + (COST == 4))
        if taunt_4:
            yield Summon(CONTROLLER, taunt_4)

        # 2费嘲讽随从
        taunt_2 = yield RandomCollectible(CONTROLLER, MINION + TAUNT + (COST == 2))
        if taunt_2:
            yield Summon(CONTROLLER, taunt_2)


class TLC_478:
    """远祖之斧
    在你的英雄攻击后，对所有随从造成1点伤害。
    """
    # Type: WEAPON | Cost: 3 | Attack: 2 | Durability: 2 | Rarity: COMMON
    events = Attack(FRIENDLY_HERO).after(Hit(ALL_MINIONS, 1))


class TLC_600:
    """乘风浮龙
    <b>战吼：</b>造成5点伤害，获得5点护甲值。<b>延系：</b>法力值消耗减少（3）点。
    """
    # Type: MINION | Cost: 8 | Attack: 6 | Health: 6 | Race: DRAGON | Rarity: COMMON
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: True}

    def play(self):
        yield Hit(TARGET, 5)
        yield GainArmor(FRIENDLY_HERO, 5)

    class Hand:
        # 延系：如果上回合打出过龙，费用减少3点
        update = Refresh(SELF, {
            GameTag.COST: lambda self, i: -3 if check_kindred_active(self.controller, CardType.MINION, Race.DRAGON) else 0
        })


class TLC_620:
    """强固
    获得3点护甲值。对一个敌方随从造成等同于你护甲值的伤害。
    """
    # Type: SPELL | Cost: 4 | Rarity: COMMON
    powered_up = True
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True, PlayReq.REQ_MINION_TARGET: True, PlayReq.REQ_ENEMY_TARGET: True}

    def play(self):
        yield GainArmor(FRIENDLY_HERO, 3)
        # 造成等同于护甲值的伤害
        yield Hit(TARGET, Attr(FRIENDLY_HERO, GameTag.ARMOR))


# RARE

class DINO_400:
    """怒袭甲龙
    每当你获得护甲值，获得+2/+2并随机攻击一个敌方随从。
    """
    # Type: MINION | Cost: 3 | Attack: 4 | Health: 3 | Race: BEAST | Rarity: RARE
    events = GainArmor(FRIENDLY_HERO).on(
        Buff(SELF, "DINO_400e"),
        Attack(SELF, RANDOM_ENEMY_MINION)
    )


class DINO_400e:
    """恼羞成怒"""
    tags = {GameTag.ATK: 2, GameTag.HEALTH: 2}


class TLC_601:
    """龟甲旋风
    消耗最多5点护甲值。每消耗一点，对所有随从造成$1点伤害。
    """
    # Type: SPELL | Cost: 4 | Rarity: RARE
    def play(self):
        # 计算可以消耗的护甲值（最多5点）
        armor_to_spend = min(self.controller.hero.armor, 5)

        if armor_to_spend > 0:
            # 消耗护甲值
            yield GainArmor(FRIENDLY_HERO, -armor_to_spend)

            # 每消耗一点护甲，对所有随从造成1点伤害
            for _ in range(armor_to_spend):
                yield Hit(ALL_MINIONS, 1)


class TLC_606:
    """拉特维亚护甲师
    <b>战吼：</b>对一个敌方随从造成2点伤害。如果该随从死亡，获得5点护甲值。
    """
    # Type: MINION | Cost: 3 | Attack: 3 | Health: 3 | Rarity: RARE
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: True, PlayReq.REQ_MINION_TARGET: True, PlayReq.REQ_ENEMY_TARGET: True}

    def play(self):
        yield Hit(TARGET, 2)
        # 检查目标是否死亡
        if TARGET.zone == Zone.GRAVEYARD:
            yield GainArmor(FRIENDLY_HERO, 5)


class TLC_632:
    """萨弗拉斯的故事
    将你的英雄技能替换为"随机对一个敌人造成8点伤害。"使用两次后，换回原技能。
    """
    # Type: SPELL | Cost: 5 | Rarity: RARE | School: FIRE
    def play(self):
        # 保存原始英雄技能ID
        original_power_id = self.controller.hero.power.id
        self.controller.tlc632_original_power = original_power_id

        # 替换为新的英雄技能（使用两次后换回）
        yield Summon(CONTROLLER, "TLC_632t2")
        yield Destroy(FRIENDLY_HERO_POWER)


# EPIC

class TLC_622:
    """城防守卫
    召唤两个0/6并具有<b>嘲讽</b>的守卫。守卫在受到伤害时会获得+1攻击力。
    """
    # Type: SPELL | Cost: 4 | Rarity: EPIC
    def play(self):
        # 召唤两个城墙守卫
        yield Summon(CONTROLLER, "TLC_622t")
        yield Summon(CONTROLLER, "TLC_622t")


class TLC_622t:
    """城墙守卫
    <b>嘲讽</b>。在本随从受到伤害后，获得+1攻击力。
    """
    # Type: MINION | Cost: 2 | Attack: 0 | Health: 6
    taunt = True
    events = Damage(SELF).after(Buff(SELF, "TLC_622e"))


class TLC_622e:
    """坚韧不拔"""
    tags = {GameTag.ATK: 1}


class TLC_623:
    """石雕工匠
    在你的回合结束时，随机使一个受伤的友方随从获得+2/+2。
    """
    # Type: MINION | Cost: 2 | Attack: 1 | Health: 4 | Rarity: EPIC
    events = OWN_TURN_END.on(
        Find(FRIENDLY_MINIONS + DAMAGED) & Buff(Find.CARD, "TLC_623e")
    )


class TLC_623e:
    """+2/+2"""
    tags = {GameTag.ATK: 2, GameTag.HEALTH: 2}


# LEGENDARY

class DINO_401:
    """伟岸的德拉克雷斯
    <b>突袭</b>。在本随从攻击一个敌方随从后，还会对所有其他敌方随从造成伤害。
    """
    # Type: MINION | Cost: 8 | Attack: 5 | Health: 12 | Race: BEAST, DRAGON | Rarity: LEGENDARY
    rush = True

    events = Attack(SELF, MINION).after(
        # 对所有其他敌方随从造成等同于本随从攻击力的伤害
        Hit(ENEMY_MINIONS - Attack.DEFENDER, ATK(SELF))
    )


class TLC_602:
    """走进失落之城
    <b>任务：</b>存活10个回合。<b>奖励：</b>拉特维厄斯，城市之眼。
    """
    # Type: SPELL | Cost: 1 | Rarity: LEGENDARY
    progress_total = 10
    quest = OWN_TURN_BEGIN.on(AddProgress(SELF, FRIENDLY_HERO))
    reward = Give(CONTROLLER, "TLC_602t")


class TLC_602t:
    """拉特维厄斯，城市之眼
    <b>战吼：</b>获取2张"大门钥匙"。将其洗入你的牌库。
    """
    # Type: MINION | Cost: 5 | Attack: 8 | Health: 8 | Rarity: LEGENDARY
    def play(self):
        # 获取2张大门钥匙并洗入牌库
        # 注意：大门钥匙是一张特殊卡牌，需要在 tokens.py 中定义
        yield Shuffle(CONTROLLER, "TLC_602t2")
        yield Shuffle(CONTROLLER, "TLC_602t2")


class TLC_624:
    """观察者娜博亚
    <b>战吼：</b>召唤你受伤的随从的复制，使复制获得<b>突袭</b>。
    """
    # Type: MINION | Cost: 6 | Attack: 5 | Health: 7 | Rarity: LEGENDARY
    def play(self):
        # 获取所有受伤的友方随从
        damaged_minions = [m for m in self.controller.field if m.damage > 0]

        for minion in damaged_minions:
            # 召唤复制并给予突袭
            yield Summon(CONTROLLER, ExactCopy(minion)).then(
                SetTag(Summon.CARD, {GameTag.RUSH: True})
            )

