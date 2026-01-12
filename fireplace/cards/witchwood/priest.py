from ..utils import *


##
# Minions


class GIL_142:
    """Chameleos / 变色龙卡米洛斯
    如果这张牌在你的手牌中，每个回合都会变成你对手手牌中的一张牌。"""

    # Each turn this is in your hand, transform it into a card your opponent is holding.
    class Hand:
        def _morph_and_buff(self):
            if not ENEMY_HAND.eval(self.game, self):
                return
            morphed = yield Morph(SELF, ExactCopy(RANDOM(ENEMY_HAND)))
            if morphed:
                yield Buff(morphed, "GIL_142e")
        
        events = OWN_TURN_BEGIN.on(_morph_and_buff)


class GIL_142e:
    class Hand:
        def _morph_and_buff(self):
            if not ENEMY_HAND.eval(self.game, self):
                return
            morphed = yield Morph(OWNER, ExactCopy(RANDOM(ENEMY_HAND)))
            if morphed:
                yield Buff(morphed, "GIL_142e")
        
        events = OWN_TURN_BEGIN.on(_morph_and_buff)

    events = REMOVED_IN_PLAY


class GIL_156:
    """Quartz Elemental / 石英元素
    受伤时无法攻击。"""

    # Can't attack while damaged.
    update = Find(DAMAGED + SELF) & Refresh(SELF, {GameTag.CANT_ATTACK: True})


class GIL_190:
    """Nightscale Matriarch / 夜鳞龙后
    每当一个友方随从获得治疗时，召唤一条3/3的雏龙。"""

    # Whenever a friendly minion is healed, summon a 3/3_Whelp.
    events = Heal(FRIENDLY_MINIONS).on(Summon(CONTROLLER, "GIL_190t"))


class GIL_805:
    """Coffin Crasher / 破棺者
    亡语：从你的手牌中召唤一个亡语随从。"""

    # <b>Deathrattle:</b> Summon a <b>Deathrattle</b> minion from your hand.
    deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + DEATHRATTLE))


class GIL_835:
    """Squashling / 南瓜宝宝
    回响，战吼：恢复#2点生命值。"""

    # [x]<b>Echo</b> <b>Battlecry:</b> Restore 2 Health.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Heal(TARGET, 2)


class GIL_837:
    """Glitter Moth / 闪光飞蛾
    战吼： 如果你的牌库中只有法力值消耗为奇数的牌，使你所有其他随从的生命值翻倍。"""

    # <b>Battlecry:</b> If your deck has only odd-Cost cards, double the Health of your
    # other minions.
    powered_up = OddCost(FRIENDLY_DECK)
    play = powered_up & Buff(FRIENDLY_MINIONS - SELF, "GIL_837e")


class GIL_837e:
    def apply(self, target):
        self._xhealth = target.health * 2

    max_health = lambda self, _: self._xhealth


class GIL_840:
    """Lady in White / 白衣幽魂
    战吼：对你牌库中的所有随从施放“心灵之火”（使其攻击力等同于生命值）。"""

    # [x]<b>Battlecry:</b> Cast 'Inner Fire' _on every minion in your deck_ <i>(set Attack
    # equal to Health).</i>
    play = CastSpell("CS1_129", FRIENDLY_DECK + MINION)


##
# Spells


class GIL_134:
    """Holy Water / 圣水
    对一个随从造成$4点伤害。如果消灭该随从，将一张该随从的复制置入你的手牌。"""

    # Deal $4 damage to a minion. If that kills it, add a copy of it to your_hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 4), Dead(TARGET) & Give(CONTROLLER, Copy(TARGET))


class GIL_661:
    """Divine Hymn / 神圣赞美诗
    为所有友方角色恢复#6点 生命值。"""

    # Restore #6 Health to all friendly characters.
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Heal(FRIENDLY_CHARACTERS, 6)


class GIL_813:
    """Vivid Nightmare / 鲜活梦魇
    选择一个友方随从，召唤一个该随从的复制，且剩余生命值为1点。"""

    # [x]Choose a friendly minion. Summon a copy of it with 1 Health remaining.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Summon(CONTROLLER, SetCurrentHealth(ExactCopy(TARGET), 1))
