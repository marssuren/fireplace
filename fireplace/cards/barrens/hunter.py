"""贫瘠之地的锤炼（Forged in the Barrens）卡牌实现"""
from ..utils import *


class BAR_030:
    """Pack Kodo - 载货科多兽
    Battlecry: Discover a Beast, Secret, or weapon.
    战吼：发现一张野兽、奥秘或武器牌。
    """
    def play(self):
        # 创建三个选项：野兽、奥秘、武器
        options = []
        # 添加一个猎人野兽
        options.append(RandomCollectible(card_class=CardClass.HUNTER, type=CardType.MINION, race=Race.BEAST))
        # 添加一个猎人奥秘
        options.append(RandomCollectible(card_class=CardClass.HUNTER, type=CardType.SPELL, secret=True))
        # 添加一个猎人武器
        options.append(RandomCollectible(card_class=CardClass.HUNTER, type=CardType.WEAPON))
        
        # 让玩家从三个选项中选择一个
        yield GenericChoice(CONTROLLER, options)


class BAR_031:
    """Sunscale Raptor - 赤鳞迅猛龙
    Frenzy: Shuffle a Sunscale Raptor into your deck with permanent +2/+1.
    暴怒：将一张赤鳞迅猛龙洗入你的牌库，并使其永久获得+2/+1。
    """
    frenzy = Shuffle(CONTROLLER, "BAR_031t")


class BAR_032:
    """Piercing Shot - 穿刺射击
    Deal $6 damage to a minion. Excess damage hits the enemy hero.
    对一个随从造成$6点伤害。超量伤害会对敌方英雄造成伤害。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 6), Hit(ENEMY_HERO, Excess(TARGET, 6))


class BAR_033:
    """Prospector's Caravan - 勘探者车队
    At the start of your turn, give all minions in your hand +1/+1.
    在你的回合开始时，使你手牌中的所有随从牌获得+1/+1。
    """
    events = OWN_TURN_BEGIN.on(Buff(FRIENDLY_HAND + MINION, "BAR_033e"))


class BAR_033e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class BAR_034:
    """Tame Beast (Rank 1) - 驯服野兽（等级1）
    Summon a 2/2 Beast with Rush. (Upgrades when you have 5 Mana.)
    召唤一个2/2并具有突袭的野兽。（在你有5点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_034t",
        enums.RANKED_SPELL_THRESHOLD: 5,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "BAR_034t")


class BAR_034t:
    """Tame Beast (Rank 2) - 驯服野兽（等级2）
    Summon a 3/3 Beast with Rush. (Upgrades when you have 10 Mana.)
    召唤一个3/3并具有突袭的野兽。（在你有10点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_034t2",
        enums.RANKED_SPELL_THRESHOLD: 10,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "BAR_034t3")


class BAR_034t2:
    """Tame Beast (Rank 3) - 驯服野兽（等级3）
    Summon a 4/4 Beast with Rush.
    召唤一个4/4并具有突袭的野兽。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "BAR_034t4")


class BAR_035:
    """Kolkar Pack Runner - 科卡尔驯犬者
    After you cast a spell, summon a 1/1 Hyena with Rush.
    在你施放一个法术后，召唤一个1/1并具有突袭的鬣狗。
    """
    events = Play(CONTROLLER, SPELL).after(
        Summon(CONTROLLER, "BAR_035t")
    )


class BAR_037:
    """Warsong Wrangler - 战歌驯兽师
    Battlecry: Discover a Beast from your deck. Give all copies of it +2/+1 (wherever they are).
    战吼：从你的牌库中发现一张野兽牌。使它的所有复制获得+2/+1（无论它们在哪里）。
    """
    play = DISCOVER(FRIENDLY_DECK + BEAST).then(
        Buff(IN_DECK + IN_HAND + (ID == Discover.CARD), "BAR_037e")
    )


class BAR_037e:
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
    }


class BAR_038:
    """Tavish Stormpike - 塔维什·雷矛
    After a friendly Beast attacks, summon a Beast from your deck that costs (1) less.
    在一个友方野兽攻击后，从你的牌库中召唤一个法力值消耗少（1）点的野兽。
    """
    events = Attack(FRIENDLY + BEAST).after(
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + BEAST + (COST == COST(Attack.ATTACKER) - 1)))
    )


class BAR_551:
    """Barak Kodobane - 巴拉克·科多班恩
    Battlecry: Draw a 1, 2, and 3-Cost spell.
    战吼：抽一张法力值消耗为1点、2点和3点的法术牌。
    """
    play = (
        ForceDraw(RANDOM(FRIENDLY_DECK + SPELL + (COST == 1))),
        ForceDraw(RANDOM(FRIENDLY_DECK + SPELL + (COST == 2))),
        ForceDraw(RANDOM(FRIENDLY_DECK + SPELL + (COST == 3))),
    )


class BAR_801:
    """Wound Prey - 击伤猎物
    Deal $1 damage. Summon a 1/1 Hyena with Rush.
    造成$1点伤害。召唤一个1/1并具有突袭的鬣狗。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 1), Summon(CONTROLLER, "BAR_801t")


class WC_007:
    """Serpentbloom - 毒蛇花
    Give a friendly Beast Poisonous.
    使一个友方野兽获得剧毒。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.BEAST,
    }
    play = SetTags(TARGET, {GameTag.POISONOUS: True})


class WC_008:
    """Sin'dorei Scentfinder - 辛多雷气味猎手
    Frenzy: Summon four 1/1 Hyenas with Rush.
    暴怒：召唤四个1/1并具有突袭的鬣狗。
    """
    frenzy = Summon(CONTROLLER, "WC_008t") * 4


class WC_037:
    """Venomstrike Bow - 毒袭之弓
    Poisonous
    剧毒。
    """
    pass  # 剧毒属性已在卡牌数据中定义


