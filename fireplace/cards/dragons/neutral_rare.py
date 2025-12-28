from ..utils import *


##
# Minions


class DRG_055:
    """Hoard Pillager / 藏宝匪贼
    战吼：装备一把你的被摧毁的武器。"""

    # <b>Battlecry:</b> Equip one of your destroyed weapons.
    play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + WEAPON)))


class DRG_063:
    """Dragonmaw Poacher / 龙喉偷猎者
    战吼：如果你的对手控制着一条龙，便获得+4/+4和突袭。"""

    # <b>Battlecry:</b> If your opponent controls a Dragon, gain +4/+4 and <b>Rush</b>.
    powered_up = Find(ENEMY_MINIONS + DRAGON)
    play = powered_up & Buff(SELF, "DRG_063e")


DRG_063e = buff(+4, +4, rush=True)


class DRG_064:
    """Zul'Drak Ritualist / 祖达克仪祭师
    嘲讽，战吼： 随机为你的对手召唤三个法力值消耗为（1）的随从。"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> Summon three random 1-Cost minions for your
    # opponent.
    play = Summon(OPPONENT, RandomMinion(cost=1)) * 3


class DRG_070:
    """Dragon Breeder / 幼龙饲养员
    战吼：选择一条友方的龙。将它的一张复制置入你的手牌。"""

    # <b>Battlecry:</b> Choose a friendly Dragon. Add a copy of it to_your hand.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.DRAGON,
    }
    play = Give(CONTROLLER, Copy(TARGET))


class DRG_071:
    """Bad Luck Albatross / 厄运信天翁
    亡语：将两张1/1的信天翁洗入你对手的 牌库。"""

    # <b>Deathrattle:</b> Shuffle two 1/1 Albatross into your opponent's deck.
    deathrattle = Shuffle(OPPONENT, "DRG_071t") * 2


class DRG_075:
    """Cobalt Spellkin / 深蓝系咒师
    战吼：随机将两张你职业的法力值消耗为（1）的法术牌置入你的手牌。"""

    # <b>Battlecry:</b> Add two 1-Cost spells from your class to_your hand.
    play = Give(CONTROLLER, RandomSpell(cost=1, card_class=FRIENDLY_CLASS)) * 2


class DRG_076:
    """Faceless Corruptor / 无面腐蚀者
    突袭。战吼：将你的一个随从变形成为本随从的复制。"""

    # [x]<b>Rush</b>. <b>Battlecry:</b> Transform one of your minions into a copy of this.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Morph(TARGET, ExactCopy(SELF))


class DRG_077:
    """Utgarde Grapplesniper / 乌特加德鱼叉射手
    战吼：双方玩家抽一张牌。如果是龙牌，则将其召唤。"""

    # <b>Battlecry:</b> Both players draw a card. If it's a Dragon, summon it.
    play = (
        Draw(CONTROLLER).then(Find(Draw.CARD + DRAGON) & Summon(CONTROLLER, Draw.CARD)),
        Draw(OPPONENT).then(Find(Draw.CARD + DRAGON) & Summon(OPPONENT, Draw.CARD)),
    )


class DRG_078:
    """Depth Charge / 深潜炸弹
    在你的回合开始时，对所有随从造成 5点伤害。"""

    # At the start of your turn, deal 5 damage to ALL_minions.
    events = OWN_TURN_BEGIN.on(Hit(ALL_MINIONS, 5))
