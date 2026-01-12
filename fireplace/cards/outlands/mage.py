from ..utils import *


##
# Minions


class BT_004:
    """Imprisoned Observer / 被禁锢的眼魔
    休眠2回合。唤醒时，对所有敌方随从造成2点伤害。"""

    # <b>Dormant</b> for 2 turns. When this awakens, deal 2 damage to all enemy
    # minions.
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2
    awaken = Hit(ENEMY_MINIONS, 2)


class BT_014:
    """Starscryer / 星占师
    亡语：抽一张法术牌。"""

    # <b>Deathrattle:</b> Draw a spell.
    deathrattle = ForceDraw(RANDOM(FRIENDLY_DECK + SPELL))


class BT_022:
    """Apexis Smuggler / 埃匹希斯走私犯
    在你使用一张奥秘牌后，发现一张 法术牌。"""

    # After you play a <b>Secret</b>, <b>Discover</b> a spell.
    events = Play(CONTROLLER, SECRET).after(DISCOVER(RandomSpell()))


class BT_028:
    """Astromancer Solarian / 星术师索兰莉安
    法术伤害+1 亡语：将“终极索兰莉安”洗入你的牌库。"""

    # [x]<b>Spell Damage +1</b> <b>Deathrattle:</b> Shuffle 'Solarian Prime'
    # into your deck.
    deathrattle = Shuffle(CONTROLLER, "BT_028t")


class BT_028t:
    """Solarian Prime"""

    # <b>Spell Damage +1</b> <b>Battlecry:</b> Cast 5 random Mage spells
    # <i>(targets enemies if possible)</i>.
    def play(self):
        # 施放5个随机法师法术
        for _ in range(5):
            spell = self.controller.card(RandomSpell(card_class=CardClass.MAGE))
            if spell:
                yield CastSpellTargetsEnemiesIfPossible(CONTROLLER, spell)


##
# Spells


class BT_002:
    """Incanter's Flow / 咒术洪流
    使你牌库中所有法术牌的法力值消耗减少（1）点。"""

    # Reduce the Cost of spells in your deck by_(1).
    play = Buff(FRIENDLY_DECK + SPELL, "BT_002e")


class BT_002e:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


class BT_003:
    """Netherwind Portal / 虚空之风传送门
    奥秘：在你的对手施放一个法术后，随机召唤一个法力值消耗为（4）的随从。"""

    # <b>Secret:</b> After your opponent casts a spell, summon a random 4-Cost
    # minion.
    secret = Play(OPPONENT, SPELL).after(
        FULL_BOARD | (Reveal(SELF), Summon(CONTROLLER, RandomMinion(cost=4)))
    )


class BT_006:
    """Evocation / 唤醒
    用随机法师法术牌填满你的手牌。这些牌为临时牌。"""

    # Fill your hand with random Mage spells. At the end of your turn, discard
    # them.
    play = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE)).then(
        Buff(Give.CARD, "BT_006e")
    ) * (MAX_HAND_SIZE(CONTROLLER) - Count(FRIENDLY_HAND))


class BT_006e:
    class Hand:
        events = OWN_TURN_END.on(Destroy(OWNER))

    events = REMOVED_IN_PLAY


class BT_021:
    """Font of Power / 能量之泉
    发现一张法师随从牌。如果你的牌库中没有随从牌，改为保留全部三张牌。"""

    # <b>Discover</b> a Mage minion. If your deck has no minions, keep all 3.
    powered_up = -Find(FRIENDLY_DECK + MINION)
    play = powered_up & (
        Give(CONTROLLER, RandomMinion(card_class=CardClass.MAGE) * 3)
    ) | (DISCOVER(RandomMinion(card_class=CardClass.MAGE)))


class BT_072:
    """Deep Freeze / 深度冻结
    冻结一个敌人。召唤两个3/6的水元素。"""

    # <b>Freeze</b> an enemy. Summon two 3/6 Water Elementals.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = Freeze(TARGET), Summon(CONTROLLER, "CS2_033") * 2


class BT_291:
    """Apexis Blast / 埃匹希斯冲击
    造成$5点伤害。如果你的牌库中没有随从牌，随机召唤一个法力值消耗为（5）的随从。"""

    # Deal $5 damage. If your deck has no minions, summon a random 5-Cost
    # minion.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    powered_up = -Find(FRIENDLY_DECK + MINION)
    play = Hit(TARGET, 5), powered_up & Summon(CONTROLLER, RandomMinion(cost=5))
