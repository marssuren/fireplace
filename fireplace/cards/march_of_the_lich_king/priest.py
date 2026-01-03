"""巫妖王的进军 - 牧师 (March of the Lich King - Priest)"""
from ..utils import *


class RLK_812:
    """起尸术 (Animate Dead)
    复活一个法力值消耗小于或等于（3）点的友方随从。
    """
    play = Summon(CONTROLLER, RANDOM(FRIENDLY + KILLED + MINION + (COST <= 3)))


class RLK_813:
    """白骨召唤者 (Bonecaller)
    嘲讽。亡语：复活一个在本局对战中死亡的友方亡灵。
    机制: DEATHRATTLE, TAUNT
    """
    tags = {GameTag.TAUNT: True}
    deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY + KILLED + MINION + UNDEAD))


class RLK_814:
    """异教水晶工匠 (Crystalsmith Cultist)
    战吼：如果你的手牌中有暗影法术牌，获得+1/+1。
    机制: BATTLECRY
    """
    def play(self):
        # 检查手牌中是否有暗影法术
        if self.controller.hand.filter(type=CardType.SPELL, spell_school=SpellSchool.SHADOW):
            yield Buff(SELF, "RLK_814e")


class RLK_814e:
    """异教水晶工匠增益 (Crystalsmith Cultist Buff)"""
    atk = 1
    health = 1


class RLK_815:
    """暗言术：丧 (Shadow Word: Undeath)
    对所有敌人造成$2点伤害。如果在你的上回合之后有友方亡灵死亡，则再造成$2点。
    """
    def play(self):
        # 对所有敌人造成2点伤害
        yield Hit(ENEMY_CHARACTERS, 2)
        # 如果上回合之后有友方亡灵死亡，再造成2点伤害
        if self.controller.undead_died_last_turn:
            yield Hit(ENEMY_CHARACTERS, 2)


class RLK_816:
    """女武神席瓦娜 (Sister Svalna)
    战吼：将一张黑暗幻象永久置入你的手牌。
    机制: BATTLECRY
    """
    play = Give(CONTROLLER, "RLK_816t")


class RLK_816t:
    """黑暗幻象 (Dark Illusion)
    0费法术
    复制一个友方随从。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    play = Summon(CONTROLLER, ExactCopy(TARGET))


class RLK_822:
    """纠缠梦魇 (Haunting Nightmare)
    亡语：纠缠你的一张手牌。当你使用被纠缠的牌时，召唤一个4/3的士兵。
    机制: DEATHRATTLE
    """
    deathrattle = Buff(RANDOM(FRIENDLY_HAND), "RLK_822e")


class RLK_822e:
    """纠缠 (Haunted)
    当你使用此牌时，召唤一个4/3的士兵。
    """
    events = Play(CONTROLLER, OWNER).after(
        Summon(CONTROLLER, "RLK_822t")
    )


class RLK_822t:
    """士兵 (Soldier)
    4/3 随从
    """
    pass


class RLK_823:
    """不死盟军 (Undying Allies)
    在本回合中，在你使用一张亡灵牌后，使其获得复生。
    """
    play = Buff(CONTROLLER, "RLK_823e")


class RLK_823e:
    """不死盟军增益 (Undying Allies Buff)"""
    events = (
        # 打出亡灵牌后给予复生
        Play(CONTROLLER, MINION + UNDEAD).after(
            Buff(Play.CARD, "RLK_823e2")
        ),
        # 回合结束时移除
        OwnTurnEnds(CONTROLLER).on(Destroy(SELF))
    )


class RLK_823e2:
    """复生 (Reborn)"""
    tags = {GameTag.REBORN: True}


class RLK_829:
    """挖坟掘墓 (Grave Digging)
    抽两张牌。如果在你的上回合之后有友方亡灵死亡，本牌的法力值消耗为（1）点。
    """
    play = Draw(CONTROLLER) * 2
    
    def cost_mod(self):
        # 如果上回合之后有友方亡灵死亡，费用为1
        if self.controller.undead_died_last_turn:
            return lambda self, i: 1
        return lambda self, i: i


class RLK_832:
    """高阶教徒巴萨莱弗 (High Cultist Basaleph)
    战吼：复活在你的上回合之后死亡的所有友方亡灵。
    机制: BATTLECRY
    """
    def play(self):
        # 复活上回合之后死亡的所有友方亡灵
        for card in self.controller.undead_died_last_turn_list:
            yield Summon(CONTROLLER, card.id)


class RLK_845:
    """心灵吞食者 (Mind Eater)
    亡语：将你对手牌库中的一张牌的复制置入你的手牌。
    机制: DEATHRATTLE
    """
    deathrattle = Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK)))


