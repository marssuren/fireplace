from ..utils import *


##
# Minions


class DRG_010:
    """Diving Gryphon / 俯冲狮鹫
    突袭，战吼：从你的牌库中抽一张具有突袭的随从牌。"""

    # <b>Rush</b> <b>Battlecry:</b> Draw a <b>Rush</b> minion_from_your_deck.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + MINION + RUSH))


class DRG_095:
    """Veranus / 维拉努斯
    战吼：将所有敌方随从的生命值变为1。"""

    # <b>Battlecry:</b> Change the Health of all enemy minions to 1.
    play = Buff(ENEMY_MINIONS, "DRG_095e")


class DRG_095e:
    max_health = SET(1)


class DRG_252:
    """Phase Stalker / 相位追猎者
    在你使用你的英雄技能后，从你的牌库中施放一个奥秘。"""

    # [x]After you use your Hero Power, cast a <b>Secret</b> from your deck.
    events = Activate(CONTROLLER, FRIENDLY_HERO_POWER).after(
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + SECRET))
    )


class DRG_253:
    """Dwarven Sharpshooter / 矮人神射手
    你的英雄技能能够以随从为目标。"""

    # Your Hero Power can target_minions.
    update = Refresh(FRIENDLY_HERO_POWER, {GameTag.STEADY_SHOT_CAN_TARGET: True})


class DRG_254:
    """Primordial Explorer / 始生龙探险者
    剧毒 战吼：发现一张 龙牌。"""

    # <b>Poisonous</b> <b>Battlecry:</b> <b>Discover</b> a Dragon.
    play = DISCOVER(RandomDragon())


class DRG_256:
    """Dragonbane / 灭龙弩炮
    在你使用你的英雄技能后，随机对一个敌人造成5点伤害。"""

    # After you use your Hero Power, deal 5 damage to a random enemy.
    events = Activate(CONTROLLER, FRIENDLY_HERO_POWER).after(Hit(ENEMY_HERO, 5))


##
# Spells


class DRG_006:
    """Corrosive Breath / 腐蚀吐息
    对一个随从造成$3点伤害。如果你的手牌中有龙牌，还会命中敌方英雄。"""

    # [x]Deal $3 damage to a minion. If you're holding a Dragon, it also hits the enemy
    # hero.
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    powered_up = HOLDING_DRAGON
    play = Hit(TARGET, 3), powered_up & Hit(ENEMY_HERO, 3)


class DRG_251:
    """Clear the Way / 扫清道路
    支线任务： 召唤三个突袭随从。奖励：召唤一头4/4并具有突袭的狮鹫。"""

    # [x]<b>Sidequest:</b> Summon 3 <b>Rush</b> minions. <b>Reward:</b> Summon a 4/4
    # Gryphon with <b>Rush</b>.
    progress_total = 3
    sidequest = Summon(CONTROLLER, RUSH + MINION).after(AddProgress(SELF, Summon.CARD))
    reward = Summon(CONTROLLER, "DRG_251t")


class DRG_255:
    """Toxic Reinforcements / 病毒增援
    支线任务： 使用你的英雄技能三次。奖励：召唤三个2/1的麻风侏儒。"""

    # [x]<b>Sidequest:</b> Use your Hero Power three times. <b>Reward:</b> Summon three 1/1
    # Leper Gnomes.
    progress_total = 3
    sidequest = Activate(CONTROLLER, FRIENDLY_HERO_POWER).after(
        AddProgress(SELF, FRIENDLY_HERO_POWER)
    )
    reward = Summon(CONTROLLER, "DRG_251t") * 3


##
# Weapons


class DRG_007:
    """Stormhammer / 风暴之锤
    当你控制着一条龙时，不会失去 耐久度。"""

    # Doesn't lose Durability while you control a_Dragon.
    update = Find(FRIENDLY_MINIONS + DRAGON) & Refresh(SELF, buff="DRG_007e")


DRG_007e = buff(immune=True)
