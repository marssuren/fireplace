# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 潜行者
"""

from ..utils import *


class TID_078:
    """Shattershambler - 碎裂蹒跚者
    1费 1/3 战吼：你的下一张亡语随从的法力值消耗减少(1)点，但在打出时立即死亡。
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 3,
        GameTag.COST: 1,
    }
    play = Buff(CONTROLLER, "TID_078e")


class TID_078e:
    """Shattershambler Buff"""
    # 下一张亡语随从减少1费并在打出时死亡
    update = Refresh(FRIENDLY_HAND + MINION + DEATHRATTLE, {GameTag.COST: -1})
    events = Play(CONTROLLER, MINION + DEATHRATTLE).on(
        Destroy(Play.CARD),
        Destroy(SELF)
    )


class TID_080:
    """Inkveil Ambusher - 墨纱伏击者
    2费 1/2 潜行 在攻击时，获得+3攻击力和免疫。
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.STEALTH: True,
    }
    # 攻击时获得+3攻击力和免疫
    events = Attack(SELF).on(
        Buff(SELF, "TID_080e"),
        SetAttr(SELF, GameTag.IMMUNE, True)
    )


class TID_080e:
    """+3攻击力"""
    tags = {
        GameTag.ATK: 3,
    }
    # 攻击结束后移除免疫
    events = Attack(OWNER).after(
        SetAttr(OWNER, GameTag.IMMUNE, False),
        Destroy(SELF)
    )


class TID_931:
    """Jackpot! - 头奖！
    2费法术 随机将两张法力值消耗大于或等于(5)点的其他职业法术牌置入你的手牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    play = lambda self: (
        Give(CONTROLLER, RandomSpell(cost_min=5, exclude_class=CardClass.ROGUE)),
        Give(CONTROLLER, RandomSpell(cost_min=5, exclude_class=CardClass.ROGUE)),
    )


class TSC_085:
    """Cutlass Courier - 弯刀信使
    3费 2/5 在你的英雄攻击后，抽一张海盗牌。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 5,
        GameTag.COST: 3,
    }
    events = Attack(FRIENDLY_HERO).after(ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION + PIRATE))


class TSC_086:
    """Swordfish - 剑鱼
    3费 2/0武器 战吼：探底。如果是海盗牌，使本武器和该海盗获得+2攻击力。
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 2,
        GameTag.DURABILITY: 0,
        GameTag.COST: 3,
    }
    
    def play(self):
        """
        探底，如果是海盗牌，使本武器和该海盗获得+2攻击力
        """
        # 探底
        yield Dredge(CONTROLLER)
        
        # 检查牌库顶的牌是否是海盗
        if self.controller.deck:
            top_card = self.controller.deck[0]
            if top_card.type == CardType.MINION and Race.PIRATE in top_card.races:
                # 使本武器获得+2攻击力
                yield Buff(SELF, "TSC_086e")
                # 使该海盗获得+2攻击力
                yield Buff(top_card, "TSC_086e2")


class TSC_086e:
    """+2攻击力（武器）"""
    tags = {
        GameTag.ATK: 2,
    }


class TSC_086e2:
    """+2攻击力（海盗）"""
    tags = {
        GameTag.ATK: 2,
    }


class TSC_912:
    """Azsharan Vessel - 艾萨拉船只
    5费法术 召唤两个3/3并具有潜行的海盗。将一张"沉没的船只"置于你的牌库底部。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
    }
    play = (
        Summon(CONTROLLER, "TSC_912t") * 2,
        ShuffleIntoDeck(CONTROLLER, "TSC_912t2"),
    )


class TSC_912t:
    """Stealthy Pirate - 潜行海盗
    3费 3/3 潜行
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
        GameTag.STEALTH: True,
    }


class TSC_912t2:
    """Sunken Vessel - 沉没的船只
    5费法术 召唤四个3/3并具有潜行的海盗。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
    }
    play = Summon(CONTROLLER, "TSC_912t") * 4


class TSC_916:
    """Gone Fishin' - 垂钓时光
    1费法术 探底。连击：抽一张牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    play = Dredge(CONTROLLER)
    combo = Draw(CONTROLLER)


class TSC_932:
    """Blood in the Water - 水中之血
    6费法术 对一个敌人造成$3点伤害。召唤一个5/5并具有突袭的鲨鱼。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 6,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = (
        Hit(TARGET, 3),
        Summon(CONTROLLER, "TSC_932t"),
    )


class TSC_932t:
    """Shark - 鲨鱼
    5费 5/5 突袭
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
        GameTag.RUSH: True,
    }


class TSC_933:
    """Bootstrap Sunkeneer - 靴带沉没者
    5费 4/4 连击：将一个敌方随从置于对手的牌库底部。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
    }
    requirements = {
        PlayReq.REQ_TARGET_FOR_COMBO: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    combo = ShuffleIntoDeck(OPPONENT, TARGET)


class TSC_934:
    """Pirate Admiral Hooktusk - 海盗上将胡克塔斯克
    7费 7/7 战吼：如果你在本局对战中召唤过7个其他海盗，掠夺敌人！
    """
    tags = {
        GameTag.ATK: 7,
        GameTag.HEALTH: 7,
        GameTag.COST: 7,
    }
    
    def play(self):
        """
        如果召唤过7个其他海盗，掠夺敌人（从对手牌库抽3张牌）
        """
        # 统计召唤过的海盗数量（不包括自己）
        pirate_count = sum(
            1 for card in self.controller.cards_played_this_game
            if card.type == CardType.MINION and Race.PIRATE in card.races and card != self
        )
        
        if pirate_count >= 7:
            # 掠夺：从对手牌库抽3张牌到自己手牌
            yield ForceDraw(CONTROLLER, ENEMY_DECK) * 3


class TSC_936:
    """Swiftscale Trickster - 迅鳞诡术师
    4费 2/2 战吼：你本回合的下一个法术的法力值消耗为(0)点。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 4,
    }
    play = Buff(CONTROLLER, "TSC_936e")


class TSC_936e:
    """Swiftscale Trickster Buff"""
    # 下一个法术费用为0
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: SET(0)})
    events = Play(CONTROLLER, SPELL).on(Destroy(SELF))


class TSC_937:
    """Crabatoa - 可拉巴托亚
    6费 6/5 巨型+2 你的蟹巴托亚之爪获得+2攻击力。
    """
    tags = {
        GameTag.ATK: 6,
        GameTag.HEALTH: 5,
        GameTag.COST: 6,
    }
    # 巨型+2：召唤2个附属部件
    colossal_appendages = ["TSC_937t", "TSC_937t"]
    # 光环：蟹爪获得+2攻击力
    update = Refresh(FRIENDLY_MINIONS + ID("TSC_937t"), {GameTag.ATK: +2})


class TSC_937t:
    """Crabatoa Claw - 蟹巴托亚之爪
    2费 2/2
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }


class TSC_963:
    """Filletfighter - 切片斗士
    1费 3/1 战吼：造成1点伤害。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
    }
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Hit(TARGET, 1)
