from ..utils import *


##
# Minions


class DRG_225:
    """Sky Claw / 空中飞爪
    你的其他机械拥有+1攻击力。战吼：召唤两个1/1的微型 旋翼机。"""

    # Your other Mechs have +1 Attack. <b>Battlecry:</b> Summon two 1/1 Microcopters.
    update = Refresh(FRIENDLY_MINIONS + MECH - SELF, buff="DRG_225e")
    play = SummonBothSides(CONTROLLER, "DRG_225t") * 2


DRG_225e = buff(atk=1)


class DRG_226:
    """Amber Watcher / 琥珀看守者
    战吼： 恢复#8点生命值。"""

    # <b>Battlecry:</b> Restore #8_Health.
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Heal(TARGET, 8)


class DRG_229:
    """Bronze Explorer / 青铜龙探险者
    吸血 战吼：发现一张 龙牌。"""

    # <b>Lifesteal</b> <b>Battlecry:</b> <b>Discover</b> a Dragon.
    play = DISCOVER(RandomDragon())


class DRG_231:
    """Lightforged Crusader / 光铸远征军
    战吼：如果你的牌库中没有中立卡牌，随机将五张圣骑士卡牌置入你的手牌。"""

    # [x]<b>Battlecry:</b> If your deck has no Neutral cards, add 5 random Paladin cards to
    # your hand.
    powered_up = -Find(FRIENDLY_DECK + NEUTRAL)
    play = powered_up & Give(
        CONTROLLER, RandomCollectible(card_class=CardClass.PALADIN)
    )


class DRG_232:
    """Lightforged Zealot / 光铸狂热者
    战吼： 如果你的牌库中没有中立卡牌，便装备一把4/2的真银圣剑。"""

    # <b>Battlecry:</b> If your deck has no Neutral cards, equip a
    # __4/2_Truesilver_Champion._
    powered_up = -Find(FRIENDLY_DECK + NEUTRAL)
    play = powered_up & Summon(CONTROLLER, "DRG_232t")


class DRG_235:
    """Dragonrider Talritha / 龙骑士塔瑞萨
    亡语：使你手牌中的一张龙牌获得+3/+3以及此亡语。"""

    # <b>Deathrattle:</b> Give a Dragon in your hand +3/+3 and this <b>Deathrattle</b>.
    deathrattle = Buff(RANDOM(FRIENDLY_HAND + DRAGON), "DRG_235e")


class DRG_235e:
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.DEATHRATTLE: True,
    }
    deathrattle = Buff(RANDOM(FRIENDLY_HAND + DRAGON), "DRG_235e")


class DRG_309:
    """Nozdormu the Timeless / 时光巨龙诺兹多姆
    战吼： 将每个玩家的法力水晶重置为十个。"""

    # <b>Battlecry:</b> Set each player to 10 Mana Crystals.
    play = SetMana(ALL_PLAYERS, 10)


##
# Spells


class DRG_008:
    """Righteous Cause / 正义感召
    支线任务： 召唤五个随从。奖励：使你的所有随从获得+1/+1。"""

    # <b>Sidequest:</b> Summon 5 minions. <b>Reward:</b> Give your minions +1/+1.
    progress_total = 5
    sidequest = Summon(CONTROLLER, MINION).after(AddProgress(SELF, Summon.CARD))
    reward = Buff(FRIENDLY_MINIONS, "DRG_008e")


DRG_008e = buff(+1, +1)


class DRG_233:
    """Sand Breath / 沙尘吐息
    使一个随从获得+1/+2。如果你的手牌中有龙牌，使其获得圣盾。"""

    # [x]Give a minion +1/+2. Give it <b>Divine Shield</b> if you're holding a Dragon.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    powered_up = HOLDING_DRAGON
    play = Buff(TARGET, "DRG_233e"), powered_up & GiveDivineShield(TARGET)


DRG_233e = buff(+1, +2)


class DRG_258:
    """Sanctuary / 庇护
    支线任务： 在一回合内不受伤害。奖励：召唤一个3/6并具有嘲讽的随从。"""

    # [x]<b>Sidequest:</b> Take no damage for a turn. <b>Reward:</b> Summon a 3/6 minion
    # with <b>Taunt</b>.
    progress_total = 1
    sidequest = OWN_TURN_BEGIN.on(
        (DAMAGED_THIS_TURN(FRIENDLY_HERO) == 0) & AddProgress(SELF, SELF)
    )
    reward = Summon(CONTROLLER, "DRG_258t")
