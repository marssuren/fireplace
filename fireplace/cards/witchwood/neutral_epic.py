from ..utils import *


##
# Minions


class GIL_117:
    """Worgen Abomination / 狼人憎恶
    在你的回合结束时，对所有其他受伤的随从造成2点伤害。"""

    # At the end of your turn, deal 2 damage to all other damaged minions.
    events = OWN_TURN_END.on(Hit(ALL_MINIONS - SELF + DAMAGED, 2))


class GIL_124:
    """Mossy Horror / 苔藓恐魔
    战吼：消灭所有其他攻击力小于或等于2的随从。"""

    # <b>Battlecry:</b> Destroy all other_minions with 2_or_less_Attack.
    play = Destroy(ALL_MINIONS - SELF + (ATK <= 2))


class GIL_581:
    """Sandbinder / 缚沙者
    战吼：从你的牌库中抽一张元素牌。"""

    # <b>Battlecry:</b> Draw an Elemental from your deck.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + ELEMENTAL))


class GIL_614:
    """Voodoo Doll / 巫毒娃娃
    战吼：选择一个随从。亡语：消灭选择的随从。"""

    # <b>Battlecry:</b> Choose a minion. <b>Deathrattle:</b> Destroy the chosen minion.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    deathrattle = HAS_TARGET & Destroy(TARGET)


class GIL_616:
    """Splitting Festeroot / 分裂腐树
    亡语：召唤两个2/2的分裂树苗。"""

    # <b>Deathrattle:</b> Summon two 2/2 Splitting Saplings.
    deathrattle = Summon(CONTROLLER, "GIL_616t") * 2


class GIL_616t:
    """Splitting Sapling"""

    # <b>Deathrattle:</b> Summon two 1/1 Woodchips.
    deathrattle = Summon(CONTROLLER, "GIL_616t2") * 2


class GIL_682:
    """Muck Hunter / 泥沼狩猎者
    突袭，战吼：为你的对手召唤两个2/1的泥沼怪。"""

    # <b>Rush</b> <b>Battlecry:</b> Summon two 2/1_Mucklings for your opponent.
    play = Summon(OPPONENT, "GIL_682t") * 2


class GIL_815:
    """Baleful Banker / 恶毒的银行家
    战吼：选择一个友方随从，将一个复制洗入你的牌库。"""

    # <b>Battlecry:</b> Choose a friendly minion. Shuffle a copy into your deck.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Shuffle(CONTROLLER, Copy(TARGET))


class GIL_819:
    """Witch's Cauldron / 女巫的坩埚
    在一个友方随从死亡后，随机将一张萨满祭司法术牌置入你的手牌。"""

    # After a friendly minion dies, add a random Shaman spell to your hand.
    events = Death(FRIENDLY_MINIONS).on(
        Give(CONTROLLER, RandomSpell(card_class=CardClass.SHAMAN))
    )
