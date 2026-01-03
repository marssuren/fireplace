"""巫妖王的进军 - 迷你扩展包 (March of the Lich King)"""
from ..utils import *


class RLK_012:
    """断魂 (Soulbreaker)
    在你的英雄攻击并消灭一个随从后，获得2份残骸。
    机制: TRIGGER_VISUAL
    """
    # 英雄攻击并消灭随从后，获得2份残骸
    events = Attack(FRIENDLY_HERO, ENEMY_MINIONS).after(
        Dead(Attack.DEFENDER) & GainCorpses(CONTROLLER, 2)
    )


class RLK_035:
    """邪爆 (Corpse Explosion)
    引爆一份残骸，对所有随从造成$1点伤害。如果有随从存活，重复此效果。
    """
    def play(self):
        # 循环：消耗1份残骸，对所有随从造成1点伤害，如果有随从存活则重复
        while self.controller.corpses > 0:
            # 消耗1份残骸
            yield SpendCorpses(CONTROLLER, 1)
            # 对所有随从造成1点伤害
            yield Hit(ALL_MINIONS, 1)
            # 检查是否还有随从存活
            if not self.game.board:
                break


class RLK_051:
    """吸血鬼之血 (Vampiric Blood)
    使你的英雄获得+5生命值。消耗3份残骸，多获得5点并抽一张牌。
    """
    def play(self):
        # 基础效果：英雄获得+5生命值
        yield GainArmor(FRIENDLY_HERO, 5)

        # 如果有3份或以上残骸，消耗3份并触发额外效果
        if self.controller.corpses >= 3:
            yield SpendCorpses(CONTROLLER, 3)
            yield GainArmor(FRIENDLY_HERO, 5)  # 额外+5生命值
            yield Draw(CONTROLLER)  # 抽一张牌


class RLK_116:
    """死灵殡葬师 (Necrotic Mortician)
    战吼：如果在你的上回合之后有友方亡灵死亡，发现一张邪恶符文牌。
    机制: BATTLECRY
    """
    def play(self):
        # 检查上回合之后是否有友方亡灵死亡
        if self.controller.undead_died_last_turn:
            # 发现一张邪恶符文牌（死亡骑士的邪恶符文卡牌）
            yield GenericChoice(CONTROLLER, RandomSpell(card_class=CardClass.DEATHKNIGHT) * 3)


class RLK_120:
    """绞肉机 (Meat Grinder)
    战吼：随机绞碎你牌库中的一个随从，获得4份残骸。
    机制: BATTLECRY
    """
    play = (
        Mill(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)),  # 磨掉一个随从
        GainCorpses(CONTROLLER, 4)  # 获得4份残骸
    )


class RLK_121:
    """死亡侍僧 (Acolyte of Death)
    在一个友方亡灵死亡后，抽一张牌。
    机制: TRIGGER_VISUAL
    """
    # 友方亡灵死亡后，抽一张牌
    events = Death(FRIENDLY + UNDEAD).on(Draw(CONTROLLER))


class RLK_225:
    """凋零毒牙 (Blightfang)
    战吼：感染所有敌方随从。当感染的随从死亡时，为你召唤一个2/2并具有嘲讽的僵尸。
    机制: BATTLECRY
    """
    play = Buff(ENEMY_MINIONS, "RLK_225e")


class RLK_225e:
    """凋零毒牙感染 (Blightfang Infection)"""
    # 当感染的随从死亡时，为你召唤一个2/2嘲讽僵尸
    deathrattle = Summon(CONTROLLER, "RLK_225t")


class RLK_225t:
    """僵尸 (Zombie)
    2/2 嘲讽
    """
    # Token 卡牌
    pass


class RLK_506:
    """白骨卫士指挥官 (Boneguard Commander)
    嘲讽。战吼：将最多6份残骸复活为1/3并具有嘲讽的复活的步兵。
    机制: BATTLECRY, TAUNT
    """
    tags = {GameTag.TAUNT: True}

    def play(self):
        # 计算可以复活的残骸数量（最多6份）
        corpses_to_spend = min(self.controller.corpses, 6)

        # 消耗残骸并召唤相应数量的复活步兵
        if corpses_to_spend > 0:
            yield SpendCorpses(CONTROLLER, corpses_to_spend)
            for i in range(corpses_to_spend):
                yield Summon(CONTROLLER, "RLK_506t")


class RLK_506t:
    """复活的步兵 (Risen Footman)
    1/3 嘲讽
    """
    # Token 卡牌
    pass


class RLK_706:
    """亚历山德罗斯·莫格莱尼 (Alexandros Mograine)
    战吼：在本局对战的剩余时间内，在你的回合结束时，对你的对手造成3点伤害。
    机制: BATTLECRY
    """
    play = Buff(FRIENDLY_HERO, "RLK_706e")


class RLK_706e:
    """莫格莱尼的诅咒 (Mograine's Curse)"""
    # 每回合结束时对敌方英雄造成3点伤害
    events = OwnTurnEnd(CONTROLLER).on(Hit(ENEMY_HERO, 3))


class RLK_741:
    """窃魂者 (Soulstealer)
    战吼：消灭所有其他随从。每消灭一个敌方随从，获得1份残骸。
    机制: BATTLECRY
    """
    def play(self):
        # 统计敌方随从数量
        enemy_minions_count = len([m for m in self.game.board if m.controller != self.controller and m != self])

        # 消灭所有其他随从
        yield Destroy(ALL_MINIONS - SELF)

        # 根据消灭的敌方随从数量获得残骸
        if enemy_minions_count > 0:
            yield GainCorpses(CONTROLLER, enemy_minions_count)


