"""巫妖王的进军 - 萨满 (March of the Lich King - Shaman)"""
from ..utils import *


class RLK_550:
    """腐鳃 (Rotgill)
    战吼：使你的其他随从获得“亡语：使你的所有随从获得+1/+1。”
    机制: BATTLECRY
    """
    def play(self):
        # 使其他随从获得亡语
        yield Give(FRIENDLY_MINIONS - SELF, "RLK_550e")


class RLK_550e:
    """腐鳃亡语 (Rotgill Deathrattle)"""
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Buff(FRIENDLY_MINIONS, "RLK_550e2")


class RLK_550e2:
    """腐鳃增益 (Rotgill Buff)"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
    }
    health = 1


class RLK_551:
    """瘟血狂战士 (Blightblood Berserker)
    嘲讽，吸血，复生，亡语：随机对一个敌人造成3点伤害。
    机制: DEATHRATTLE, LIFESTEAL, REBORN, TAUNT
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.LIFESTEAL: True,
        GameTag.REBORN: True
    }
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 3)


class RLK_552:
    """无息的勇士 (Unliving Champion)
    战吼：如果在你的上回合之后有友方亡灵死亡，召唤两个3/2的僵尸。
    机制: BATTLECRY
    """
    def play(self):
        # 检查上回合之后是否有友方亡灵死亡
        if self.controller.undead_died_last_turn:
            yield Summon(CONTROLLER, "RLK_552t") * 2


class RLK_552t:
    """僵尸 (Zombie)"""
    atk = 3
    health = 2
    race = Race.UNDEAD


class RLK_553:
    """先知先觉 (Prescience)
    抽两张随从牌。每有一张法力值消耗大于或等于（5）点的牌，召唤一个2/3并具有嘲讽的幽灵。
    """
    def play(self):
        # 抽两张随从牌
        for i in range(2):
            draw_res = yield Draw(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION))
            if draw_res:
                card = draw_res[0]
                # 检查费用是否大于等于5
                if card.cost >= 5:
                    yield Summon(CONTROLLER, "RLK_553t")


class RLK_553t:
    """幽灵 (Spirit)"""
    atk = 2
    health = 3
    tags = {GameTag.TAUNT: True}
    race = Race.UNDEAD


class RLK_554:
    """恐惧感知者 (Harkener of Dread)
    嘲讽，复生 
    亡语：召唤一个4/4并具有嘲讽的亡灵。
    机制: DEATHRATTLE, REBORN, TAUNT
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.REBORN: True
    }
    deathrattle = Summon(CONTROLLER, "RLK_554t")


class RLK_554t:
    """复活的亡灵 (Risen Undead)"""
    atk = 4
    health = 4
    tags = {GameTag.TAUNT: True}
    race = Race.UNDEAD


class RLK_909:
    """织亡者光环 (Deathweaver Aura)
    使一个随从获得“亡语：召唤两个3/2的僵尸。”过载：（1）
    机制: OVERLOAD
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    overload = 1
    play = Give(TARGET, "RLK_909e")


class RLK_909e:
    """织亡者亡语 (Deathweaver Deathrattle)"""
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, "RLK_552t") * 2


class RLK_910:
    """暗影弥漫 (Shadow Suffusion)
    使你的所有随从获得“亡语：随机对一个敌人造成3点伤害。”
    """
    play = Give(FRIENDLY_MINIONS, "RLK_910e")


class RLK_910e:
    """暗影弥漫亡语 (Shadow Suffusion Deathrattle)"""
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 3)


class RLK_911:
    """彼界来客 (From De Other Side)
    召唤你手牌中每一个随从的复制。使其随机攻击敌方随从，然后死亡。
    """
    def play(self):
        # 召唤手牌中所有随从的复制
        hand_minions = self.controller.hand.filter(type=CardType.MINION)
        copies = []
        
        for minion in hand_minions:
            # 复制并召唤
            res = yield Summon(CONTROLLER, Copy(minion))
            if res:
                copies.append(res[0])
        
        # 随机攻击敌方随从
        for copy in copies:
            # 必须活着才能攻击
            if not copy.dead and copy.zone == Zone.PLAY:
                yield Attack(copy, RANDOM_ENEMY_MINION)
        
        # 死亡
        yield Destroy(copies)


class RLK_912:
    """天灾巨魔 (Scourge Troll)
    本随从获得的亡语会触发两次。
    """
    # 核心机制：使用 DEATHRATTLE_TIMES_TWO 标签
    tags = {GameTag.DEATHRATTLE_TIMES_TWO: True}


class RLK_913:
    """达库鲁大王 (Overlord Drakuru)
    突袭，风怒。
    在本随从攻击并消灭随从后，为你复活被消灭的随从。
    机制: RUSH, TRIGGER_VISUAL, WINDFURY
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.WINDFURY: True
    }
    # 攻击后，如果目标死亡，复活该目标（Summon handling entity in graveyard ressurects it）
    events = Attack(SELF).after(
        Dead(Attack.DEFENDER) & Summon(CONTROLLER, Attack.DEFENDER)
    )
