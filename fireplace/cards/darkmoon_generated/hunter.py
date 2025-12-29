from ..utils import *


##
# Minions

class DMF_083:
    """Dancing Cobra (舞动的眼镜蛇)
    Corrupt: Gain Poisonous."""

    # TODO: Implement mechanics: CORRUPT
    # TODO: Implement Corrupt effect
    # corrupt = ...

class DMF_085:
    """Darkmoon Tonk (暗月坦克)
    Deathrattle: Fire four  missiles at random enemies that deal 2 damage each."""

    # TODO: Implement mechanics: DEATHRATTLE
    # TODO: Implement Deathrattle effect
    # deathrattle = ...

class DMF_087:
    """Trampling Rhino (狂踏的犀牛)
    Rush. After this attacks and kills a minion, excess damage hits the enemy hero."""

    # TODO: Implement mechanics: RUSH, TRIGGER_VISUAL

class DMF_089:
    """Maxima Blastenheimer (玛克希玛·雷管)
    Battlecry: Summon a minion from your deck. It attacks the enemy hero, then dies."""

    # TODO: Implement mechanics: BATTLECRY
    # TODO: Implement Battlecry effect
    # play = ...

class DMF_122:
    """Mystery Winner (神秘获奖者)
    Battlecry: Discover a Secret."""

    # TODO: Implement mechanics: BATTLECRY, DISCOVER
    # TODO: Implement Battlecry effect
    # play = ...

class YOP_028:
    """Saddlemaster (鞍座管理员)
    After you play a Beast, add a random Beast to your hand."""

    # TODO: Implement mechanics: TRIGGER_VISUAL


##
# Spells

class DMF_084:
    """Jewel of N'Zoth (恩佐斯宝石)
    Summon three friendly Deathrattle minions that died this game."""

    # TODO: Implement Deathrattle effect
    # deathrattle = ...
    # TODO: Implement spell effect
    # play = ...

class DMF_086:
    """Petting Zoo (宠物乐园)
    Summon a 3/3 Strider. Repeat for each Secret you control."""

    # TODO: Implement spell effect
    # play = ...

class DMF_090:
    """Don't Feed the Animals (请勿投食)
    Give all Beasts in your hand +1/+1. Corrupt: Give them +2/+2 instead."""

    # TODO: Implement mechanics: CORRUPT
    # TODO: Implement Corrupt effect
    # corrupt = ...
    # TODO: Implement spell effect
    # play = ...

class DMF_123:
    """Open the Cages (打开兽笼)
    Secret: When your turn starts, if you control  two minions, summon an Animal Companion."""

    # TODO: Implement mechanics: SECRET
    # TODO: Implement spell effect
    # play = ...

class YOP_027:
    """Bola Shot (套索射击)
    Deal $1 damage to a minion and $2 damage to its neighbors."""

    # TODO: Implement spell effect
    # play = ...


##
# Weapons

class DMF_088:
    """Rinling's Rifle (瑞林的步枪)
    After your hero attacks, Discover a Secret and cast it."""

    # TODO: Implement mechanics: TRIGGER_VISUAL
