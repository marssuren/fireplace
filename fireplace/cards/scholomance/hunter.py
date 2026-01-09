from ..utils import *


##
# Minions

class SCH_133:
    """Wolpertinger / 鹿角兔
    Battlecry: Summon a copy of this.
    战吼：召唤该随从的一个复制。"""

    # 1费 1/1 野兽 战吼：召唤该随从的一个复制
    play = Summon(CONTROLLER, ExactCopy(SELF))


class SCH_340:
    """Bloated Python / 臃肿巨蟒
    Deathrattle: Summon a 4/4 Hapless Handler.
    亡语：召唤一个4/4的倒霉管理员。"""

    # 3费 1/2 野兽 亡语：召唤一个4/4的倒霉管理员
    deathrattle = Summon(CONTROLLER, "SCH_340t")


class SCH_539:
    """Professor Slate / 斯雷特教授
    Your spells are Poisonous.
    你的法术具有剧毒。"""

    # 3费 3/4 你的法术具有剧毒
    update = Refresh(FRIENDLY + SPELL, {GameTag.POISONOUS: True})

class SCH_607:
    """Shan'do Wildclaw / 山多·野爪
    Choose One - Give Beasts in your deck +1/+1; or Transform into a copy of a friendly Beast.
    抉择：使你牌库中的野兽获得+1/+1；或者变形成为一个友方野兽的复制。"""

    # 3费 3/3 传说 抉择：使你牌库中的野兽获得+1/+1；或者变形成为一个友方野兽的复制
    choose = ["SCH_607a", "SCH_607b"]


class SCH_239:
    """Krolusk Barkstripper / 克鲁斯克剥皮者
    Spellburst: Destroy a random enemy minion.
    法术迸发：消灭一个随机敌方随从。"""

    # 4费 3/5 野兽 法术迸发：消灭一个随机敌方随从
    spellburst = Destroy(RANDOM_ENEMY_MINION)

class SCH_244:
    """Teacher's Pet / 老师的宠物
    Taunt Deathrattle: Summon a random 3-Cost Beast.
    嘲讽 亡语：召唤一个随机的3费野兽。"""

    # 5费 4/5 野兽 嘲讽 亡语：召唤一个随机的3费野兽
    # 嘲讽通过 CardDefs.xml 中的 TAUNT 标签定义
    deathrattle = Summon(CONTROLLER, RandomMinion(cost=3, race=Race.BEAST))


##
# Spells

class SCH_617:
    """Adorable Infestation / 可爱的侵扰
    Give a minion +1/+1. Summon a 1/1 Cub. Add a Cub to your hand.
    使一个随从获得+1/+1。召唤一个1/1的幼崽。将一张幼崽牌加入你的手牌。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    # 1费 使一个随从获得+1/+1。召唤一个1/1的幼崽。将一张幼崽牌加入你的手牌
    play = Buff(TARGET, "SCH_617e"), Summon(CONTROLLER, "SCH_617t"), Give(CONTROLLER, "SCH_617t")


SCH_617e = buff(atk=1, health=1)

class SCH_300:
    """Carrion Studies / 腐肉研习
    Discover a Deathrattle minion. Your next one costs (1) less.
    发现一张亡语随从牌。你的下一张亡语随从牌法力值消耗减少（1）点。"""

    # 1费 发现一张亡语随从牌。你的下一张亡语随从牌法力值消耗减少（1）点
    play = Discover(CONTROLLER, RandomMinion(deathrattle=True)), Buff(CONTROLLER, "SCH_300e")


class SCH_300e:
    """Carrion Studies Buff / 腐肉研习增益"""
    update = Refresh(FRIENDLY_HAND + MINION + DEATHRATTLE, {GameTag.COST: -1})
    events = Play(FRIENDLY + MINION + DEATHRATTLE).on(Destroy(SELF))

class SCH_604:
    """Overwhelm / 压制
    Deal $2 damage to a minion. Deal one more damage for each Beast you control.
    对一个随从造成2点伤害。你每控制一个野兽，便额外造成1点伤害。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    # 1费 对一个随从造成2点伤害。你每控制一个野兽，便额外造成1点伤害
    play = Hit(TARGET, Count(FRIENDLY_MINIONS + BEAST) + 2)


class SCH_610:
    """Guardian Animals / 守护动物
    Summon two Beasts that cost (5) or less from your deck. Give them Rush.
    从你的牌库中召唤两个法力值消耗小于或等于5的野兽。使其获得突袭。"""

    # 7费 从你的牌库中召唤两个法力值消耗小于或等于5的野兽。使其获得突袭
    play = (
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + BEAST + (COST <= 5))).then(Buff(Summon.CARD, "SCH_610e")),
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + BEAST + (COST <= 5))).then(Buff(Summon.CARD, "SCH_610e"))
    )


SCH_610e = buff(rush=True)
