from ..utils import *


##
# Minions


class BT_201:
    """Augmented Porcupine / 强能箭猪
    亡语： 造成等同于本随从攻击力的伤害，随机分配到所有敌人身上。"""

    # [x]<b>Deathrattle</b>: Deal this minion's Attack damage randomly split
    # among all enemies.
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 1) * ATK(SELF)


class BT_202:
    """Helboar / 地狱野猪
    亡语：随机使你手牌中的一张野兽牌获得+1/+1。"""

    # <b>Deathrattle:</b> Give a random Beast in your hand +1/+1.
    deathrattle = Buff(RANDOM(FRIENDLY_HAND + BEAST), "BT_202e")


BT_202e = buff(+1, +1)


class BT_210:
    """Zixor, Apex Predator / 顶级捕食者兹克索尔
    突袭 亡语：将“终极兹克索尔”洗入你的牌库。"""

    # [x]<b>Rush</b> <b>Deathrattle:</b> Shuffle 'Zixor Prime' into your deck.
    deathrattle = Shuffle(CONTROLLER, "BT_210t")


class BT_210t:
    """Zixor Prime"""

    # [x]<b>Rush</b> <b>Battlecry:</b> Summon 3 copies of this minion.
    play = Summon(CONTROLLER, ExactCopy(SELF)) * 3


class BT_211:
    """Imprisoned Felmaw / 被禁锢的魔喉
    休眠2回合。唤醒时，随机攻击一个 敌人。"""

    # [x]<b>Dormant</b> for 2 turns. When this awakens, __attack a random
    # enemy.
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2
    awaken = Attack(SELF, RANDOM_ENEMY_CHARACTER)


class BT_212:
    """Mok'Nathal Lion / 莫克纳萨将狮
    突袭，战吼：选择一个友方随从，获得其亡语的复制。"""

    # <b>Rush</b>. <b>Battlecry:</b> Choose a friendly minion. Gain a copy of
    # its <b>Deathrattle</b>.
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0,
    }
    play = CopyDeathrattleBuff(TARGET, "BT_212e")


class BT_214:
    """Beastmaster Leoroxx / 兽王莱欧洛克斯
    战吼：从你的手牌中召唤三只野兽。"""

    # <b>Battlecry:</b> Summon 3 Beasts from your hand.
    play = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + BEAST) * 3)


##
# Spells


class BT_163:
    """Nagrand Slam / 纳格兰大冲撞
    召唤四只3/5的裂蹄牛并使其攻击随机敌人。"""

    # Summon four 3/5 Clefthoofs that attack random enemies.
    play = (
        Summon(CONTROLLER, "BT_163t").then(Attack(Summon.CARD, RANDOM_ENEMY_CHARACTER))
        * 4
    )


class BT_203:
    """Pack Tactics / 集群战术
    奥秘：当一个友方随从受到攻击时，召唤一个该随从的3/3的复制。"""

    # <b>Secret:</b> When a friendly minion is attacked, summon a 3/3 copy.
    secret = Attack(None, FRIENDLY_MINIONS).on(
        FULL_BOARD
        | (
            Reveal(SELF),
            Summon(CONTROLLER, ExactCopy(Attack.DEFENDER)).then(
                Buff(Summon.CARD, "BT_203e")
            ),
        )
    )


class BT_203e:
    atk = SET(3)
    max_health = SET(3)


class BT_205:
    """Scrap Shot / 废铁射击
    造成$3点伤害。随机使你手牌中的一张野兽牌获得+3/+3。"""

    # Deal $3 damage. Give a random Beast in_your hand +3/+3.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3), Buff(RANDOM(FRIENDLY_HAND + BEAST), "BT_205e")


BT_205e = buff(+3, +3)


class BT_213:
    """Scavenger's Ingenuity / 拾荒者的智慧
    抽一张野兽牌。使其获得+3/+3。"""

    # Draw a Beast. Give it +3/+3.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + BEAST)).then(
        Buff(ForceDraw.TARGET, "BT_213e")
    )


BT_213e = buff(+3, +3)
