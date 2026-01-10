"""巫妖王的进军 - 圣骑士 (March of the Lich King - Paladin)"""
from ..utils import *


class RLK_527:
    """时空守卫 (Timewarden)
    战吼：直到你的下个回合结束，在此期间你召唤的龙获得嘲讽和圣盾。
    机制: BATTLECRY
    """
    play = Buff(CONTROLLER, "RLK_527e")


class RLK_527e:
    """时空守卫增益 (Timewarden Buff)"""
    # 在下个回合结束时移除
    events = OWN_TURN_END.after(Destroy(SELF))
    update = Summon(CONTROLLER, DRAGON).after(Buff(Summon.CARD, "RLK_527e2"))


class RLK_527e2:
    """龙增益 (Dragon Buff)"""
    tags = {GameTag.TAUNT: True, GameTag.DIVINE_SHIELD: True}


class RLK_916:
    """胆大的幼龙 (Daring Drake)
    突袭。战吼：如果你的手牌中有龙牌，便获得+1/+1。
    机制: BATTLECRY, RUSH
    """
    tags = {GameTag.RUSH: True}
    
    def play(self):
        # 检查手牌中是否有龙牌
        if self.controller.hand.filter(race=Race.DRAGON):
            yield Buff(SELF, "RLK_916e")


class RLK_916e:
    """胆大的幼龙增益 (Daring Drake Buff)"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
    }
    health = 1


class RLK_917:
    """青铜龙军团 (Flight of the Bronze)
    发现一张龙牌。法力渴求（7）：召唤一条5/5并具有嘲讽的幼龙。
    机制: DISCOVER, MANATHIRST
    """
    def play(self):
        # 发现一张龙牌
        yield GenericChoice(CONTROLLER, DISCOVER(DRAGON))
        # 法力渴求（7）：召唤5/5嘲讽幼龙
        if self.controller.max_mana >= 7:
            yield Summon(CONTROLLER, "RLK_917t")


class RLK_917t:
    """幼龙 (Whelp)
    5/5 嘲讽
    """
    tags = {GameTag.TAUNT: True}


class RLK_918:
    """为了奎尔萨拉斯！ (For Quel'Thalas!)
    使一个友方随从获得+3攻击力。在本回合中，使你的英雄获得+2攻击力。
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        # 使目标随从获得+3攻击力
        if TARGET:
            yield Buff(TARGET, "RLK_918e")
        # 使英雄获得+2攻击力（本回合）
        yield Buff(FRIENDLY_HERO, "RLK_918e2")


class RLK_918e:
    """为了奎尔萨拉斯增益 (For Quel'Thalas Buff)"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 3,
    }


class RLK_918e2:
    """英雄攻击力增益 (Hero Attack Buff)"""
    tags = {GameTag.ATK: 2}
    events = OWN_TURN_END.on(Destroy(SELF))


class RLK_919:
    """阿纳克洛斯 (Anachronos)
    战吼：
将所有其他随从送入2回合后的未来。
    机制: BATTLECRY
    """
    def play(self):
        # 将所有其他随从送入未来（休眠）
        for minion in ALL_MINIONS - SELF:
            yield SetTag(minion, {GameTag.DORMANT: True})
            # 2回合后唤醒
            yield Buff(minion, "RLK_919e")


class RLK_919e:
    """阿纳克洛斯增益 (Anachronos Buff)
    追踪回合数，2回合后唤醒随从
    """
    def apply(self, target):
        # 初始化剩余回合数为2（双方各1回合）
        target.anachronos_turns_remaining = 2
    
    events = OWN_TURN_BEGIN.on(
        lambda self: [
            # 减少剩余回合数
            setattr(self.owner, 'anachronos_turns_remaining', self.owner.anachronos_turns_remaining - 1),
            # 如果回合数到了，唤醒随从并销毁buff
            (
                Awaken(self.owner) &
                Destroy(SELF)
            ) if self.owner.anachronos_turns_remaining <= 0 else None
        ]
    )




class RLK_921:
    """血色士兵 (Sanguine Soldier)
    圣盾。战吼：对你的英雄造成2点伤害。
    机制: BATTLECRY, DIVINE_SHIELD
    """
    tags = {GameTag.DIVINE_SHIELD: True}
    play = Hit(FRIENDLY_HERO, 2)


class RLK_922:
    """鲜血圣印 (Seal of Blood)
    使一个随从获得+3/+3和圣盾。对你的英雄造成$3点伤害。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    play = (
        Buff(TARGET, "RLK_922e"),
        Hit(FRIENDLY_HERO, 3)
    )


class RLK_922e:
    """鲜血圣印增益 (Seal of Blood Buff)"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 3,
        GameTag.DIVINE_SHIELD: True,
    }
    health = 3


class RLK_923:
    """馑时锦食 (Feast and Famine)
    在本回合中，使你的英雄获得+3攻击力。法力渴求（4）：以及吸血。
    机制: MANATHIRST
    """
    def play(self):
        # 法力渴求（4）：获得+3攻击力和吸血
        if self.controller.max_mana >= 4:
            yield Buff(FRIENDLY_HERO, "RLK_923e2")
        else:
            # 否则只获得+3攻击力
            yield Buff(FRIENDLY_HERO, "RLK_923e")


class RLK_923e:
    """馑时锦食增益 (Feast and Famine Buff)
    +3攻击力
    """
    tags = {GameTag.ATK: 3}
    events = OWN_TURN_END.on(Destroy(SELF))


class RLK_923e2:
    """馑时锦食增益（吸血）(Feast and Famine Buff with Lifesteal)
    +3攻击力和吸血
    """
    tags = {GameTag.ATK: 3, GameTag.LIFESTEAL: True}
    events = OWN_TURN_END.on(Destroy(SELF))


class RLK_924:
    """血骑士领袖莉亚德琳 (Blood Matriarch Liadrin)
    在你召唤攻击力低于本随从的随从后，使其获得圣盾和突袭。
    机制: TRIGGER_VISUAL
    """
    events = Summon(CONTROLLER, MINION).after(
        lambda self, player, card: Buff(card, "RLK_924e") if card != SELF and card.atk < SELF.atk else None
    )


class RLK_924e:
    """血骑士领袖增益 (Blood Matriarch Buff)"""
    tags = {GameTag.DIVINE_SHIELD: True, GameTag.RUSH: True}


class RLK_927:
    """鲜血远征军 (Blood Crusader)
    战吼：在本回合中，你的下一个圣骑士随从消耗生命值,而非法力值。
    机制: BATTLECRY
    """
    play = Buff(CONTROLLER, "RLK_927e")


class RLK_927e:
    """鲜血远征军增益 (Blood Crusader Buff)
    下一个圣骑士随从消耗生命值而非法力值
    """
    events = (
        # 打出圣骑士随从时，给予生命值消耗标签
        Play(CONTROLLER, MINION + PALADIN).on(
            Buff(Play.CARD, "RLK_927e2")
        ).then(Destroy(SELF)),
        # 回合结束时移除buff
        OWN_TURN_END.on(Destroy(SELF))
    )


class RLK_927e2:
    """生命值消耗标签 (Health Cost Tag)"""
    tags = {
        enums.HEALTH_COST: True,
    }



