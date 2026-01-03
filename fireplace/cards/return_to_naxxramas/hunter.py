from ..utils import *

class NX2_013:
    """僵尸蜂群 (ZOMBEEEES!!!)
    奥秘：在你的对手使用一张随从牌后，召唤四只1/1的尸蜂攻击它。
    机制: SECRET
    [迷你扩展包]
    """
    secret = Play(OPPONENT, MINION).after(
        lambda self, player, card, *args: [
            # 召唤4只1/1的尸蜂
            Summon(CONTROLLER, "NX2_013t") * 4,
            # 使它们攻击刚打出的随从
            Attack(FRIENDLY_MINIONS, card) * 4
        ]
    )



class NX2_013t:
    """尸蜂 (Zombee)
    1/1 野兽
    """
    # Token 卡牌，无需额外效果
    pass



class NX2_014:
    """坠饰追踪者 (Trinket Tracker)
    战吼：抽一张法力值消耗为（1）的法术牌。
    机制: BATTLECRY
    [迷你扩展包]
    """
    play = ForceDraw(RANDOM(FRIENDLY_DECK + SPELL + (COST == 1)))



class NX2_015:
    """可靠伙伴 (Faithful Companions)
    从你的牌库中发现一张野兽牌并召唤。法力渴求（10）：还会召唤一个它的复制。
    机制: DISCOVER, MANATHIRST
    [迷你扩展包]
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    
    def play(self):
        # 从牌库中发现一张野兽牌
        discovered = yield GenericChoice(CONTROLLER, RANDOM(FRIENDLY_DECK + BEAST) * 3)
        if discovered:
            # 召唤发现的野兽
            yield Summon(CONTROLLER, discovered)
            # 法力渴求（10）：召唤一个复制
            if self.controller.max_mana >= 10:
                yield Summon(CONTROLLER, ExactCopy(discovered))



