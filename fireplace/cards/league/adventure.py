from ..utils import *


##
# Zinaar

RandomWish = RandomID("LOEA02_03", "LOEA02_04", "LOEA02_05", "LOEA02_06", "LOEA02_10")


class LOEA02_02:
    """Djinn’s Intuition / 灯神之赐
    抽一张牌。赐予对手一个愿望。"""

    activate = Draw(CONTROLLER), Give(OPPONENT, RandomWish)


class LOEA02_02h:
    activate = Draw(CONTROLLER), GainMana(CONTROLLER, 1), Give(OPPONENT, RandomWish)


class LOEA02_03:
    """Wish for Power / 能量愿望
    发现一张法术牌。"""

    play = DISCOVER(RandomSpell())


class LOEA02_04:
    """Wish for Valor / 勇气愿望
    发现一张 法力值消耗为（4）的卡牌。"""

    play = DISCOVER(RandomCollectible(cost=4))


class LOEA02_05:
    """Wish for Glory / 荣耀愿望
    发现一张随从牌。"""

    play = DISCOVER(RandomMinion())


class LOEA02_06:
    """Wish for More Wishes / 更多愿望
    获得两个愿望。"""

    play = Give(CONTROLLER, RandomWish) * 2


class LOEA02_10:
    """Wish for Companionship / 伙伴愿望
    发现一个动物伙伴。"""

    play = DISCOVER(RandomID("NEW1_032", "NEW1_033", "NEW1_034"))


class LOEA02_10a:
    """Leokk (Unused)"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    update = Refresh(FRIENDLY_MINIONS - SELF, buff="NEW1_033o")


##
# Sun Raider Phaerix


class LOEA01_02:
    """Blessings of the Sun / 太阳祝福
    被动 炎日权杖的控制者免疫。"""

    update = (
        Find(FRIENDLY_MINIONS + ID("LOEA01_11"))
        & (Refresh(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: True})),
        Find(ENEMY_MINIONS + ID("LOEA01_11"))
        & (Refresh(ENEMY_HERO, {GameTag.CANT_BE_DAMAGED: True})),
    )


class LOEA01_02h:
    events = Summon(CONTROLLER, ID("LOEA01_11h")).on(Buff(Summon.CARD, "LOEA01_11he"))
    update = Find(FRIENDLY_MINIONS + ID("LOEA01_11h")) & (
        Refresh(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: True})
    )


class LOEA01_11:
    """Rod of the Sun / 炎日权杖
    亡语：将权杖交予你的对手。"""

    deathrattle = Summon(OPPONENT, "LOEA01_11")


class LOEA01_11h:
    deathrattle = Summon(OPPONENT, "LOEA01_11h")


LOEA01_11he = buff(+3, +3)


class LOEA01_12:
    """Tol'vir Hoplite / 托维尔重甲兵
    亡语：对双方英雄造成5点伤害。"""

    deathrattle = Hit(ALL_HEROES, 5)


class LOEA01_12h:
    deathrattle = Hit(ALL_HEROES, 5)


##
# Temple Escape


class LOEA04_06:
    """Pit of Spikes / 钉刺陷阱
    选择方式！"""

    choose = ("LOEA04_06a", "LOEA04_06b")


class LOEA04_06a:
    """Swing Across"""

    play = COINFLIP & Hit(FRIENDLY_HERO, 10)


class LOEA04_06b:
    """Walk Across Gingerly"""

    play = Hit(FRIENDLY_HERO, 5)


class LOEA04_28:
    """A Glowing Pool / 发光的水池
    喝水？"""

    choose = ("LOEA04_28a", "LOEA04_28b")


class LOEA04_28a:
    """Drink Deeply"""

    play = Draw(CONTROLLER)


class LOEA04_28b:
    """Wade Through"""

    play = GainMana(CONTROLLER, 1)


class LOEA04_29:
    """The Eye / 宝石之眼
    选择方式！"""

    choose = ("LOEA04_29a", "LOEA04_29b")


class LOEA04_29a:
    """Touch It"""

    play = Heal(FRIENDLY_HERO, 10)


class LOEA04_29b:
    """Investigate the Runes"""

    play = Draw(CONTROLLER) * 2


class LOEA04_30:
    """The Darkness / 一片漆黑
    选择捷径？"""

    choose = ("LOEA04_30a", "LOEA04_31b")


class LOEA04_30a:
    """Take the Shortcut"""

    play = Summon(OPPONENT, "CS2_186")


class LOEA04_31b:
    """No Way!"""

    pass


class LOEA04_25:
    """Seething Statue / 炽燃雕像
    在你的回合结束时，对所有敌人造成 2点伤害。"""

    events = OWN_TURN_END.on(Hit(ENEMY_CHARACTERS, 2))


class LOEA04_25h:
    events = OWN_TURN_END.on(Hit(ENEMY_CHARACTERS, 5))


class LOE_024t:
    """Rolling Boulder"""

    events = OWN_TURN_END.on(Destroy(LEFT_OF(SELF)))


##
# Chieftain Scarvash


class LOEA05_02:
    """Trogg Hate Minions! / 穴居人讨厌随从！
    被动 敌方随从的法力值消耗增加（2）点，在你的回合开始时切换。"""

    # Hearthstone implements Scarvash's Hero Power with LOEA05_02(h) which
    # switches every turn between LOEA05_02a and LOEA05_03.
    # 实现说明：通过回合数奇偶判断来切换效果
    # 奇数回合：增加随从费用，偶数回合：增加法术费用
    update = (
        (Attr(CONTROLLER, GameTag.TURN) % 2 == 1)
        & Refresh(ENEMY_HAND + MINION, {GameTag.COST: +2})
        | Refresh(ENEMY_HAND + SPELL, {GameTag.COST: +2})
    )


class LOEA05_02a:
    update = Refresh(ENEMY_HAND + MINION, {GameTag.COST: +2})


class LOEA05_02h:
    """Trogg Hate Minions! (Heroic) / 穴居人讨厌随从！（英雄）
    被动 敌方随从的法力值消耗变为（11）点，在你的回合开始时切换。"""

    # 英雄难度：将费用设置为 11，基本无法使用
    # 奇数回合：随从费用变为 11，偶数回合：法术费用变为 11
    update = (
        (Attr(CONTROLLER, GameTag.TURN) % 2 == 1)
        & Refresh(ENEMY_HAND + MINION, {GameTag.COST: SET(11)})
        | Refresh(ENEMY_HAND + SPELL, {GameTag.COST: SET(11)})
    )


class LOEA05_02ha:
    update = Refresh(ENEMY_HAND + MINION, {GameTag.COST: SET(11)})


class LOEA05_03:
    """Trogg Hate Spells! / 穴居人讨厌法术！
    被动 敌方法术的法力值消耗增加（2）点，在你的回合开始时切换。"""

    update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: +2})


class LOEA05_03h:
    update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: SET(11)})


##
# Mine Cart Rush


class LOEA07_29:
    """Throw Rocks / 抛石
    随机对一个敌方随从造成3点伤害。"""

    activate = Hit(RANDOM_ENEMY_MINION, 3)


class LOEA07_18:
    """Dynamite / 炸药
    造成$10点伤害。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 10)


class LOEA07_20:
    """Boom! / 轰！
    对所有敌方随从造成$3点伤害。"""

    play = Hit(ENEMY_MINIONS, 3)


class LOEA07_26:
    """Consult Brann / 请教布莱恩
    抽三张牌。"""

    play = Draw(CONTROLLER) * 3


class LOEA07_28:
    """Repairs / 修理
    恢复#10点生命值。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Heal(TARGET, 10)


##
# Archaedas


class LOEA06_02:
    """Stonesculpting / 石雕之术
    为双方玩家召唤一个0/2的雕像。"""

    activate = Summon(ALL_PLAYERS, "LOEA06_02t")


class LOEA06_02h:
    activate = Summon(CONTROLLER, "LOEA06_02t"), Summon(OPPONENT, "LOEA06_02th")


class LOEA06_03:
    """Animate Earthen / 活化岩土
    使你的所有随从获得+1/+1和 嘲讽。"""

    requirements = {PlayReq.REQ_MINIMUM_TOTAL_MINIONS: 1}
    play = Buff(FRIENDLY_MINIONS, "LOEA06_03e")


LOEA06_03e = buff(+1, +1, taunt=True)


class LOEA06_03h:
    play = Buff(FRIENDLY_MINIONS, "LOEA06_03eh")


LOEA06_03eh = buff(+3, +3, taunt=True)


class LOEA06_04:
    """Shattering Spree / 粉碎之击
    消灭所有雕像。每消灭一个雕像，便造成1点伤害。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = (
        Hit(TARGET, Count(ALL_MINIONS + ID("LOEA06_02t"))),
        Destroy(ALL_MINIONS + ID("LOEA06_02t")),
    )


class LOEA06_04h:
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = (
        Hit(TARGET, Count(ALL_MINIONS + ID("LOEA06_02th")) * 3),
        Destroy(ALL_MINIONS + ID("LOEA06_02th")),
    )


##
# Lord Slitherspear

HUNGRY_NAGA = (
    ID("LOEA09_5")
    | ID("LOEA09_5H")
    | ID("LOEA09_10")
    | ID("LOEA09_11")
    | ID("LOEA09_12")
    | ID("LOEA09_13")
)


class LOEA09_2:
    """Enraged! / 激怒！
    在本回合中，使你的英雄获得+2攻击力。"""

    activate = Buff(FRIENDLY_HERO, "LOEA09_2e")


LOEA09_2e = buff(atk=2)


class LOEA09_2H:
    """Enraged! / 激怒！
    在本回合中，使你的英雄获得+5攻击力。"""

    activate = Buff(FRIENDLY_HERO, "LOEA09_2e")


LOEA09_2eH = buff(atk=5)


class LOEA09_3:
    """Getting Hungry / 饥肠辘辘
    召唤一个饥饿的纳迦。"""

    activate = Summon(CONTROLLER, "LOEA09_5").then(
        Buff(Summon.CARD, "LOEA09_3a")
        * Attr(CONTROLLER, GameTag.NUM_TIMES_HERO_POWER_USED_THIS_GAME)
    )


LOEA09_3a = buff(atk=1)


class LOEA09_3H:
    """Endless Hunger / 无尽饥饿
    召唤一个饥饿的纳迦。"""

    activate = Summon(CONTROLLER, "LOEA09_5").then(
        Buff(Summon.CARD, "LOEA09_3aH")
        * Attr(CONTROLLER, GameTag.NUM_TIMES_HERO_POWER_USED_THIS_GAME)
    )


LOEA09_3aH = buff(+1, +1)


class LOEA09_3b:
    """Getting Hungry (Unused versions)"""

    activate = Summon(CONTROLLER, "LOEA09_11")


class LOEA09_3c:
    activate = Summon(CONTROLLER, "LOEA09_10")


class LOEA09_3d:
    activate = Summon(CONTROLLER, "LOEA09_13")


class LOEA09_6:
    """Slithering Archer / 滑鳞弓箭手
    战吼：造成1点伤害。"""

    requirements = {PlayReq.REQ_NONSELF_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, 1)


class LOEA09_6H:
    """Slithering Archer / 滑鳞弓箭手
    战吼： 对所有敌方随从造成2点伤害。"""

    play = Hit(ENEMY_MINIONS, 2)


class LOEA09_7:
    """Cauldron / 大锅
    嘲讽 亡语：救出芬利爵士，阻截纳迦追兵！"""

    deathrattle = Give(OPPONENT, "LOE_076"), Summon(CONTROLLER, "LOEA09_2")


class LOEA09_7H:
    """Cauldron / 大锅
    嘲讽 亡语：救出芬利爵士！"""

    deathrattle = Give(OPPONENT, "LOE_076"), Summon(CONTROLLER, "LOEA09_2H")


class LOEA09_9:
    """Naga Repellent / 纳迦克星
    消灭所有饥饿的纳迦。"""

    play = Destroy(ALL_MINIONS + HUNGRY_NAGA)


class LOEA09_9H:
    """Naga Repellent / 纳迦克星
    使所有饥饿的纳迦的攻击力 变为1。"""

    play = Buff(ALL_MINIONS + HUNGRY_NAGA, "EX1_360e")


##
# Giantfin


class LOEA10_2:
    """Mrglmrgl MRGL! / Mrglmrgl MRGL!
    抽若干数量的牌，直到你的手牌数量等同于你对手的手牌数量。"""

    activate = DrawUntil(CONTROLLER, Count(ENEMY_HAND))


class LOEA10_2H:
    """Mrglmrgl MRGL! / Mrglmrgl MRGL!
    抽两张牌。"""

    activate = Draw(CONTROLLER) * 2


class LOEA10_5:
    """Mrgl Mrgl Nyah Nyah / Mrgl Mrgl Nyah Nyah
    召唤三个在本局对战中死亡的鱼人。"""

    play = Summon(CONTROLLER, Copy(RANDOM(KILLED + MURLOC) * 5))


class LOEA10_5H:
    """Mrgl Mrgl Nyah Nyah / Mrgl Mrgl Nyah Nyah
    召唤五个在本局对战中死亡的 鱼人。"""

    play = Summon(CONTROLLER, Copy(RANDOM(KILLED + MURLOC) * 5))


##
# Skelesaurus Hex


class LOEA13_2:
    """Ancient Power / 远古能量
    每个玩家随机获得一张卡牌，它的法力值消耗为（0）点。"""

    activate = Give(ALL_PLAYERS, RandomCollectible()).then(Buff(Give.CARD, "LOEA13_2e"))


class LOEA13_2H:
    """Ancient Power / 远古能量
    随机将一张卡牌置入你的手牌。它的法力值消耗为（0）点。"""

    activate = Give(CONTROLLER, RandomCollectible()).then(Buff(Give.CARD, "GBL_008e"))


##
# The Steel Sentinel


class LOEA14_2:
    """Platemail Armor / 板甲外衣
    被动 你的英雄每次只会受到1点伤害。"""

    update = Refresh(FRIENDLY_HERO, {GameTag.HEAVILY_ARMORED: True})


class LOEA14_2H:
    """Platemail Armor / 板甲外衣
    被动 你的英雄和随从 每次只会受到1点伤害。"""

    update = Refresh(FRIENDLY_CHARACTERS, {GameTag.HEAVILY_ARMORED: True})


##
# Arch-Thief Rafaam


class LOEA15_2:
    """Unstable Portal / 不稳定的传送门
    随机将一张随从牌置入你的手牌。该牌的法力值消耗减少（3）点。"""

    activate = Give(CONTROLLER, RandomMinion()).then(Buff(Give.CARD, "GVG_003e"))


class LOEA15_2H:
    """Unstable Portal / 不稳定的传送门
    随机将一张随从牌置入你的手牌。该牌的法力值消耗减少（3）点。"""

    activate = Give(CONTROLLER, RandomMinion()).then(Buff(Give.CARD, "GVG_003e"))


class LOEA09_4:
    """Rare Spear / 破水之矛
    每当你的对手使用一张稀有牌时，便获得+1/+1。"""

    events = Play(OPPONENT, RARE).on(Buff(SELF, "EX1_409e"))


class LOEA09_4H:
    """Rare Spear / 破水之矛
    每当你的对手使用一张稀有牌时，便获得+1/+1。"""

    events = Play(OPPONENT, RARE).on(Buff(SELF, "EX1_409e"))


##
# Rafaam Unleashed


class LOEA16_2:
    """Staff of Origination / 源生法杖
    被动 当法杖充能时，你的英雄免疫。"""

    update = Refresh(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: True})


class LOEA16_2H:
    """Staff of Origination / 源生法杖
    被动 你的英雄免疫。"""

    update = Refresh(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: True})


class LOEA16_16:
    """Rummage / 翻箱倒柜
    找到一个神器。"""

    entourage = [
        "LOEA16_10",
        "LOEA16_11",
        "LOEA16_14",
        "LOEA16_15",
        "LOEA16_6",
        "LOEA16_7",
        "LOEA16_9",
        "LOEA16_12",
        "LOEA16_13",
        "LOEA16_8",
    ]
    activate = Give(CONTROLLER, RandomEntourage())


class LOEA16_16H:
    """Rummage / 翻箱倒柜
    找到一个神器。"""

    entourage = [
        "LOEA16_10",
        "LOEA16_11",
        "LOEA16_14",
        "LOEA16_15",
        "LOEA16_6",
        "LOEA16_7",
        "LOEA16_9",
        "LOEA16_12",
        "LOEA16_13",
        "LOEA16_8",
    ]
    activate = Give(CONTROLLER, RandomEntourage())


class LOEA16_6:
    """Shard of Sulfuras / 萨弗拉斯之怒
    对所有角色造成$5点伤害。"""

    play = Hit(ALL_CHARACTERS, 5)


class LOEA16_7:
    """Benediction Splinter / 祈福的断杖
    为所有角色恢复#10点生命值。"""

    play = Heal(ALL_CHARACTERS, 10)


class LOEA16_8:
    """Putress' Vial / 普特里斯的药剂
    随机消灭一个敌方随从。"""

    play = Destroy(RANDOM_ENEMY_MINION)


# Putressed (Unused)
LOEA16_8a = AttackHealthSwapBuff()


class LOEA16_9:
    """Lothar's Left Greave / 洛萨的左护胫
    对所有敌人造成$3点伤害。"""

    play = Hit(ENEMY_CHARACTERS, 3)


class LOEA16_10:
    """Hakkari Blood Goblet / 哈卡莱血祭杯
    使一个随从变形成为2/1的 深渊巨蟒。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Morph(TARGET, "LOE_010")


class LOEA16_11:
    """Crown of Kael'thas / 凯尔萨斯的王冠
    造成$10点伤害，随机分配到所有角色身上。"""

    play = Hit(RANDOM_CHARACTER, 1) * 10


class LOEA16_12:
    """Medivh's Locket / 麦迪文的吊坠
    将你的手牌替换成不稳定的 传送门。"""

    play = Morph(FRIENDLY_HAND, "GVG_003")


class LOEA16_14:
    """Khadgar's Pipe / 卡德加的烟斗
    随机将一张法术牌置入每个玩家的手牌，你所得到的牌法力值消耗为（0）点。"""

    play = (
        Give(OPPONENT, RandomSpell()),
        Give(PLAYER, RandomSpell()).then(Buff(Give.CARD, "GBL_008e")),
    )


class LOEA16_15:
    """Ysera's Tear / 伊瑟拉之泪
    在本回合中，获得四个 法力水晶。"""

    play = ManaThisTurn(CONTROLLER, 4)


class LOEA16_18:
    """Zinaar / 辛纳尔
    在你的回合结束时，获得一个愿望。"""

    events = OWN_TURN_END.on(Give(CONTROLLER, RandomWish))


class LOEA16_18H:
    """Zinaar / 辛纳尔
    在你的回合结束时，获得一个愿望。"""

    events = OWN_TURN_END.on(Give(CONTROLLER, RandomWish))


class LOEA16_19:
    """Sun Raider Phaerix / 菲利克斯·掠日者
    在你的回合结束时，将一张太阳祝福置入你的手牌。"""

    events = OWN_TURN_END.on(Give(CONTROLLER, "LOEA16_20"))


class LOEA16_19H:
    """Sun Raider Phaerix / 菲利克斯·掠日者
    你的其他随从免疫。"""

    update = Refresh(FRIENDLY_MINIONS - SELF, {GameTag.CANT_BE_DAMAGED: True})


LOEA16_20H = buff(immune=True)


class LOEA16_21:
    """Chieftain Scarvash / 斯卡瓦什酋长
    敌方卡牌法力值消耗增加（1）点。"""

    update = Refresh(ENEMY_HAND, {GameTag.COST: +1})


class LOEA16_21H:
    """Chieftain Scarvash / 斯卡瓦什酋长
    敌方卡牌法力值消耗增加（2）点。"""

    update = Refresh(ENEMY_HAND, {GameTag.COST: +2})


class LOEA16_22:
    """Archaedas / 阿扎达斯
    在你的回合结束时，随机将一个敌方随从变为0/2的雕像。"""

    events = OWN_TURN_END.on(Morph(RANDOM_ENEMY_MINION, "LOEA06_02t"))


class LOEA16_22H:
    """Archaedas / 阿扎达斯
    在你的回合结束时，随机将一个敌方随从变为0/2的雕像。"""

    events = OWN_TURN_END.on(Morph(RANDOM_ENEMY_MINION, "LOEA06_02t"))


class LOEA16_23:
    """Lord Slitherspear / 滑矛领主
    在你的回合结束时，每有一个敌方随从，就召唤一个1/1的饥饿的纳迦。"""

    events = OWN_TURN_END.on(Summon(CONTROLLER, "LOEA09_5") * Count(ENEMY_MINIONS))


class LOEA16_23H:
    """Lord Slitherspear / 滑矛领主
    在你的回合结束时，每有一个敌方随从，就召唤一个1/1的饥饿的纳迦。"""

    events = OWN_TURN_END.on(Summon(CONTROLLER, "LOEA09_5") * Count(ENEMY_MINIONS))


class LOEA16_24:
    """Giantfin / 老蓟皮
    在你的回合结束时，抽若干数量的牌，直到你的手牌数量等同于你对手的手牌数量。"""

    events = OWN_TURN_END.on(DrawUntil(CONTROLLER, Count(ENEMY_HAND)))


class LOEA16_24H:
    """Giantfin / 老蓟皮
    在你的回合结束时，抽两张牌。"""

    events = OWN_TURN_END.on(Draw(CONTROLLER) * 2)


class LOEA16_26:
    """Skelesaurus Hex / 骨龙海克斯
    在你的回合结束时，每个玩家随机获得一张卡牌，它的法力值消耗为（0）点。"""

    events = OWN_TURN_END.on(
        Give(ALL_PLAYERS, RandomCollectible()).then(Buff(Give.CARD, "LOEA13_2e"))
    )


class LOEA16_26H:
    """Skelesaurus Hex / 骨龙海克斯
    在你的回合结束时，随机获得一张卡牌，它的法力值消耗为（0）点。"""

    events = OWN_TURN_END.on(
        Give(CONTROLLER, RandomCollectible()).then(Buff(Give.CARD, "LOEA13_2e"))
    )


class LOEA16_27:
    """The Steel Sentinel / 钢铁卫士
    本随从每次只会受到1点伤害。"""

    tags = {GameTag.HEAVILY_ARMORED: True}


class LOEA16_27H:
    """The Steel Sentinel / 钢铁卫士
    本随从每次只会受到1点伤害。"""

    tags = {GameTag.HEAVILY_ARMORED: True}


class LOEA16_20:
    """Blessing of the Sun / 太阳祝福
    在本回合中，使一个随从获得 免疫。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "LOEA16_20e")


LOEA16_20e = buff(immune=True)


##
# Misc.


class LOE_008:
    """Eye of Hakkar / 哈卡之眼
    攫取你对手的牌库中的一个奥秘，并将其置入战场。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0}
    play = Summon(CONTROLLER, RANDOM(ENEMY_DECK + SECRET))


class LOE_008H:
    """Eye of Hakkar / 哈卡之眼
    攫取你对手的牌库中的一个奥秘，并将其置入战场。"""

    play = Summon(CONTROLLER, RANDOM(ENEMY_DECK + SECRET))


class LOEA_01:
    """Looming Presence / 浮光掠影
    抽两张牌。 获得4点护甲值。"""

    play = Draw(CONTROLLER) * 2, GainArmor(FRIENDLY_HERO, 4)


class LOEA_01H:
    """Looming Presence / 浮光掠影
    抽三张牌。获得6点护甲值。"""

    play = Draw(CONTROLLER) * 3, GainArmor(FRIENDLY_HERO, 6)


class LOEA15_3:
    """Boneraptor / 骸骨迅猛龙
    战吼：控制对手的武器。"""

    play = Steal(ENEMY_WEAPON)


class LOEA15_3H:
    """Boneraptor / 骸骨迅猛龙
    战吼：控制对手的武器。"""

    play = Steal(ENEMY_WEAPON)
