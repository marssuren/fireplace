"""巫妖王的进军 - 迷你扩展包 (March of the Lich King)"""
from ..utils import *


class RLK_221:
    """水晶掮客 (Crystal Broker)
    法力渴求（5）：随机召唤一个法力值消耗为（3）的随从。法力渴求（10）：改为召唤法力值消耗为（8）的随从。
    机制: MANATHIRST
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}

    def play(self):
        # 法力渴求（10）：召唤8费随从
        if self.controller.max_mana >= 10:
            yield Summon(CONTROLLER, RandomMinion(cost=8))
        # 法力渴求（5）：召唤3费随从
        elif self.controller.max_mana >= 5:
            yield Summon(CONTROLLER, RandomMinion(cost=3))


class RLK_677:
    """圣殿扰咒师 (Sanctum Spellbender)
    每当你的对手以另一随从为目标施放法术时，使其改为指向本随从。
    机制: TRIGGER_VISUAL
    """
    # 监听对手施放以随从为目标的法术，将目标重定向到自己
    # 参考 tt_010 (Spellbender) 的实现
    events = Play(OPPONENT, SPELL, FRIENDLY_MINIONS - SELF).on(
        Retarget(Play.CARD, SELF)
    )


class RLK_831:
    """魔药播撒者 (Plaguespreader)
    亡语：随机将你对手手牌中的一张随从牌变形成为魔药播撒者。
    机制: DEATHRATTLE
    """
    # 亡语：随机变形对手手牌中的一张随从为魔药播撒者
    deathrattle = Morph(RANDOM(ENEMY_HAND + MINION), "RLK_831")


class RLK_952:
    """附魔师 (Enchanter)
    在你的回合中，敌方随从受到的伤害翻倍。
    机制: AURA
    """
    # 在己方回合中，给所有敌方随从添加"受到伤害翻倍"的buff
    # 使用 update 方法在己方回合时刷新buff
    def update(self, entity):
        # 检查是否是己方回合
        if entity.controller.game.current_player == entity.controller:
            # 给所有敌方随从添加伤害翻倍buff
            return Find(ENEMY_MINIONS) | Buff("RLK_952e")
        return []


class RLK_952e:
    """附魔师增益 - 伤害翻倍 (Enchanter's Curse)"""
    # 使用 INCOMING_DAMAGE_MULTIPLIER 标签使受到的伤害翻倍
    tags = {GameTag.INCOMING_DAMAGE_MULTIPLIER: 2}


class RLK_970:
    """陆行鸟牧人 (Hawkstrider Rancher)
    每当你使用一张随从牌，使其获得+1/+1和"亡语：召唤一只1/1的陆行鸟。"
    机制: TRIGGER_VISUAL
    """
    # 监听己方打出随从事件
    events = Play(CONTROLLER, MINION).on(
        Buff(Play.CARD, "RLK_970e")
    )


class RLK_970e:
    """陆行鸟牧人增益 (Hawkstrider Rancher's Blessing)"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1
    }
    # 亡语：召唤一只1/1的陆行鸟
    deathrattle = Summon(CONTROLLER, "RLK_970t")


class RLK_970t:
    """陆行鸟 (Hawkstrider)"""
    # Token 卡牌：1/1 陆行鸟
    pass


