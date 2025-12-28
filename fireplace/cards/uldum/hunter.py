from ..utils import *


##
# Minions


class ULD_151:
    """Ramkahen Wildtamer / 拉穆卡恒驯兽师
    战吼：随机复制一张你手牌中的野兽牌。"""

    # <b>Battlecry:</b> Copy a random Beast in your hand.
    play = Give(CONTROLLER, Copy(RANDOM(FRIENDLY_HAND + BEAST)))


class ULD_154:
    """Hyena Alpha / 土狼头领
    战吼：如果你控制一个奥秘，便召唤两只2/2的土狼。"""

    # [x]<b>Battlecry:</b> If you control a <b>Secret</b>, summon two 2/2 Hyenas.
    powered_up = Find(FRIENDLY_SECRETS)
    play = powered_up & SummonBothSides(CONTROLLER, "ULD_154t") * 2


class ULD_156:
    """Dinotamer Brann / 恐龙大师布莱恩
    战吼：如果你的牌库里没有相同的牌，则召唤暴龙王克鲁什。"""

    # <b>Battlecry:</b> If your deck has no duplicates, summon King Krush.
    powered_up = -FindDuplicates(FRIENDLY_DECK)
    play = powered_up & Summon(CONTROLLER, "ULD_156t3")


class ULD_212:
    """Wild Bloodstinger / 刺血狂蝎
    战吼：从你对手的手牌中召唤一个随从。攻击该随从。"""

    # <b>Battlecry:</b> Summon a minion from your opponent's hand. Attack it.
    play = Summon(OPPONENT, RANDOM(ENEMY_HAND + MINION)).then(Attack(SELF, Summon.CARD))


class ULD_410:
    """Scarlet Webweaver / 猩红织网蛛
    战吼：随机使你手牌中的一张野兽牌的 法力值消耗减少（5）点。"""

    # <b>Battlecry:</b> Reduce the Cost of a random Beast in your_hand by (5).
    play = Buff(RANDOM(FRIENDLY_HAND + BEAST), "ULD_410e")


class ULD_410e:
    tags = {GameTag.COST: -5}
    events = REMOVED_IN_PLAY


##
# Spells


class ULD_152:
    """Pressure Plate / 压感陷阱
    奥秘：在你的对手施放一个法术后，随机消灭一个敌方 随从。"""

    # <b>Secret:</b> After your opponent casts a spell, destroy a random enemy_minion.
    secret = Play(OPPONENT, SPELL).after(Reveal(SELF), Destroy(RANDOM_ENEMY_MINION))


class ULD_155:
    """Unseal the Vault / 打开宝库
    任务：召唤20个随从。奖励：法老的面盔。"""

    # <b>Quest:</b> Summon 20_minions. <b>Reward:</b> Pharaoh's Warmask.
    progress_total = 20
    quest = Summon(CONTROLLER, MINION).on(AddProgress(SELF, Summon.CARD))
    reward = Summon(CONTROLLER, "ULD_155p")


class ULD_155p:
    """Pharaoh's Warmask"""

    # <b>Hero Power</b> Give your minions +2_Attack.
    activate = Buff(FRIENDLY_MINIONS, "ULD_155e")


ULD_155e = buff(atk=2)


class ULD_429:
    """Hunter's Pack / 猎人工具包
    随机将一张猎人野兽牌，奥秘牌和武器牌分别置入你的 手牌。"""

    # Add a random Hunter Beast, <b>Secret</b>, and weapon to your_hand.
    play = (
        Give(CONTROLLER, RandomBeast(card_class=CardClass.HUNTER)),
        Give(CONTROLLER, RandomSpell(secret=True, card_class=CardClass.HUNTER)),
        Give(CONTROLLER, RandomWeapon(card_class=CardClass.HUNTER)),
    )


class ULD_713:
    """Swarm of Locusts / 飞蝗虫群
    召唤七只1/1并具有突袭的 蝗虫。"""

    # Summon seven 1/1 Locusts with <b>Rush</b>.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "ULD_430t") * 7


##
# Weapons


class ULD_430:
    """Desert Spear / 沙漠之矛
    在你的英雄攻击后，召唤一只1/1并具有突袭的 蝗虫。"""

    # After your hero attacks, summon a 1/1 Locust with <b>Rush</b>.
    events = Attack(FRIENDLY_HERO).after(Summon(CONTROLLER, "ULD_430t"))
