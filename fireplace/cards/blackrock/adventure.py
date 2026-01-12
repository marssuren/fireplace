from ..utils import *


##
# Hero Powers


class BRMA01_2:
    """Pile On! / 干杯！
    从双方的牌库中各将一个随从置入战场。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = (
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)),
        Summon(OPPONENT, RANDOM(ENEMY_DECK + MINION)),
    )


class BRMA01_2H:
    """Pile On! / 干杯！
    从你的牌库中将两个随从置入战场；对手将一个随从置入战场。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = (
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION) * 2),
        Summon(OPPONENT, RANDOM(ENEMY_DECK + MINION)),
    )


class BRMA01_3:
    """Dark Iron Bouncer / 黑铁保镖
    总会赢得绝命乱斗的胜利。"""

    tags = {
        enums.ALWAYS_WINS_BRAWLS: True,
    }


class BRMA02_2:
    """Jeering Crowd / 强势围观
    召唤一个1/1并具有嘲讽的观众。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "BRMA02_2t")


class BRMA02_2H:
    """Jeering Crowd / 强势围观
    召唤一个1/1并具有嘲讽的观众。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "BRMA02_2t")


class BRMA03_2:
    """Power of the Firelord / 炎魔之王的力量
    造成30点伤害。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Hit(TARGET, 2)


class BRMA04_2:
    """Magma Pulse / 熔岩脉动
    对所有随从造成1点伤害。"""

    activate = Hit(ALL_MINIONS, 1)


class BRMA05_2:
    """Ignite Mana / 点燃法力
    如果敌方英雄有任何未使用的法力水晶，便对其造成5点伤害。"""

    activate = (MANA(OPPONENT) > USED_MANA(OPPONENT)) & Hit(ENEMY_HERO, 5)


class BRMA05_2H:
    """Ignite Mana / 点燃法力
    如果敌方英雄有任何未使用的法力水晶，便对其造成10点伤害。"""

    activate = (MANA(OPPONENT) > USED_MANA(OPPONENT)) & Hit(ENEMY_HERO, 10)


class BRMA06_2:
    """The Majordomo / 火妖管理者
    召唤一个1/3的火妖卫士。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "BRMA06_4")


class BRMA06_2H:
    """The Majordomo / 火妖管理者
    召唤一个3/3的火妖卫士。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "BRMA06_4H")


class BRMA07_2:
    """ME SMASH / 猛砸
    随机消灭一个受伤的敌方随从。"""

    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    activate = Destroy(RANDOM(ENEMY_MINIONS + DAMAGED))


class BRMA07_2H:
    """ME SMASH / 猛砸
    随机消灭一个敌方随从。"""

    activate = Destroy(RANDOM_ENEMY_MINION)


class BRMA08_2:
    """Intense Gaze / 猛烈凝视
    被动 所有卡牌的法力值消耗改为（1）点。玩家最多只能拥有一个法力水晶。"""

    update = (
        Refresh(ALL_PLAYERS, {GameTag.MAXRESOURCES: SET(1)}),
        Refresh(IN_HAND, {GameTag.COST: SET(1)}),
    )


class BRMA08_2H:
    """Intense Gaze / 猛烈凝视
    被动 所有卡牌法力值消耗改为（1）点。你最多只能拥有两个法力水晶，你的对手最多只能拥有一个法力水晶。"""

    update = (
        Refresh(CONTROLLER, {GameTag.MAXRESOURCES: SET(2)}),
        Refresh(OPPONENT, {GameTag.MAXRESOURCES: SET(1)}),
        Refresh(IN_HAND, {GameTag.COST: SET(1)}),
    )


class BRMA09_2:
    """Open the Gates / 打开大门
    召唤三条1/1的雏龙。获得另一个英雄技能。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    entourage = ["BRMA09_3", "BRMA09_4"]
    activate = Summon(CONTROLLER, "BRMA09_2t") * 3, Summon(
        CONTROLLER, RandomEntourage()
    )


class BRMA09_2H:
    """Open the Gates / 打开大门
    召唤三条2/2的雏龙。获得另一个英雄技能。"""

    entourage = ["BRMA09_3H", "BRMA09_4H"]
    activate = Summon(CONTROLLER, "BRMA09_2Ht") * 3, Summon(
        CONTROLLER, RandomEntourage()
    )


class BRMA09_3:
    """Old Horde / 旧部落
    召唤两个1/1并具有嘲讽的兽人。获得另一个英雄技能。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    entourage = ["BRMA09_2", "BRMA09_4", "BRMA09_5"]
    activate = Summon(CONTROLLER, "BRMA09_3t") * 2, Summon(
        CONTROLLER, RandomEntourage()
    )


class BRMA09_3H:
    """Old Horde / 旧部落
    召唤两个2/2并具有嘲讽的兽人。获得另一个英雄技能。"""

    entourage = ["BRMA09_2H", "BRMA09_4H", "BRMA09_5H"]
    activate = Summon(CONTROLLER, "BRMA09_3Ht") * 2, Summon(
        CONTROLLER, RandomEntourage()
    )


class BRMA09_4:
    """Blackwing / 黑翼
    召唤一个3/1的龙人。获得另一个英雄技能。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    entourage = ["BRMA09_2", "BRMA09_3", "BRMA09_5"]
    activate = Summon(CONTROLLER, "BRMA09_4t"), Summon(CONTROLLER, RandomEntourage())


class BRMA09_4H:
    """Blackwing / 黑翼
    召唤一个5/4的龙人。获得另一个英雄技能。"""

    entourage = ["BRMA09_2H", "BRMA09_3H", "BRMA09_5H"]
    activate = Summon(CONTROLLER, "BRMA09_4Ht"), Summon(CONTROLLER, RandomEntourage())


class BRMA09_5:
    """Dismount / 跃下坐骑
    召唤盖斯。获得另一个英雄技能。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    entourage = ["BRMA09_2", "BRMA09_3", "BRMA09_4"]
    activate = Summon(CONTROLLER, "BRMA09_5t"), Summon(CONTROLLER, RandomEntourage())


class BRMA09_5H:
    """Dismount / 跃下坐骑
    召唤盖斯。获得另一个英雄技能。"""

    entourage = ["BRMA09_2H", "BRMA09_3H", "BRMA09_4H"]
    activate = Summon(CONTROLLER, "BRMA09_5Ht"), Summon(CONTROLLER, RandomEntourage())


class BRMA10_3:
    """The Rookery / 雏龙孵化
    使所有腐化的蛋获得+1生命值，并召唤一个腐化的蛋。"""

    activate = Buff(ALL_MINIONS + ID("BRMA10_4"), "BRMA10_3e"), Summon(
        CONTROLLER, "BRMA10_4"
    )


class BRMA10_3H:
    """The Rookery / 雏龙孵化
    使所有腐化的蛋获得+1生命值，并召唤一个腐化的蛋。"""

    activate = Buff(ALL_MINIONS + ID("BRMA10_4"), "BRMA10_3e"), Summon(
        CONTROLLER, "BRMA10_4"
    )


BRMA10_3e = buff(health=1)


class BRMA11_2:
    """Essence of the Red / 红龙精华
    每个玩家抽两张牌。"""

    activate = Draw(ALL_PLAYERS) * 2


class BRMA11_2H:
    """Essence of the Red / 红龙精华
    每个玩家抽三张牌并获得一个法力水晶。"""

    activate = Draw(ALL_PLAYERS) * 3, GainMana(CONTROLLER, 1)


class BRMA12_2:
    """Brood Affliction / 龙血之痛
    在你的回合结束时，将一张龙血之痛牌置入对手的手牌。"""

    entourage = ["BRMA12_6", "BRMA12_5", "BRMA12_7", "BRMA12_4", "BRMA12_3"]
    activate = Give(OPPONENT, RandomEntourage())


class BRMA12_2H:
    """Brood Affliction / 龙血之痛
    在你的回合结束时，将一张龙血之痛牌置入对手的手牌。"""

    entourage = ["BRMA12_3H", "BRMA12_4H", "BRMA12_5H", "BRMA12_6H", "BRMA12_7H"]
    activate = Give(OPPONENT, RandomEntourage())


class BRMA12_10:
    """Mutation / 变异
    随机弃一张牌。"""

    activate = Discard(RANDOM(FRIENDLY_HAND))


class BRMA13_2:
    """True Form / 真正形态
    游戏开始！"""

    activate = (
        Summon(CONTROLLER, "BRMA13_3"),
        Draw(CONTROLLER) * 2,
        GainArmor(FRIENDLY_HERO, 30),
    )


class BRMA13_2H:
    """True Form / 真正形态
    游戏开始！"""

    activate = (
        Summon(CONTROLLER, "BRMA13_3H"),
        Draw(CONTROLLER) * 2,
        GainArmor(FRIENDLY_HERO, 30),
    )


class BRMA13_4:
    """Wild Magic / 狂野魔法
    随机将一张你对手职业的法术牌置入你的手牌。"""

    activate = Give(CONTROLLER, RandomSpell(card_class=ENEMY_CLASS))


class BRMA13_4H:
    """Wild Magic / 狂野魔法
    随机将一张你对手职业的法术牌置入你的手牌。"""

    activate = Give(CONTROLLER, RandomSpell(card_class=ENEMY_CLASS))


class BRMA14_2:
    """Activate Arcanotron / 激活奥能金刚
    激活奥能金刚！"""

    activate = Summon(CONTROLLER, "BRMA14_3"), Summon(CONTROLLER, "BRMA14_4")


class BRMA14_2H:
    """Activate Arcanotron / 激活奥能金刚
    激活奥能金刚！"""

    activate = Summon(CONTROLLER, "BRMA14_3"), Summon(CONTROLLER, "BRMA14_4H")


class BRMA14_4:
    """Activate Toxitron / 激活剧毒金刚
    激活剧毒金刚！"""

    activate = Summon(CONTROLLER, "BRMA14_5"), Summon(CONTROLLER, "BRMA14_6")


class BRMA14_4H:
    """Activate Toxitron / 激活剧毒金刚
    激活剧毒金刚！"""

    activate = Summon(CONTROLLER, "BRMA14_5H"), Summon(CONTROLLER, "BRMA14_6H")


class BRMA14_6:
    """Activate Electron / 激活电荷金刚
    激活电荷金刚！"""

    activate = Summon(CONTROLLER, "BRMA14_7"), Summon(CONTROLLER, "BRMA14_8")


class BRMA14_6H:
    """Activate Electron / 激活电荷金刚
    激活电荷金刚！"""

    activate = Summon(CONTROLLER, "BRMA14_7H"), Summon(CONTROLLER, "BRMA14_8H")


class BRMA14_8:
    """Activate Magmatron / 激活熔岩金刚
    激活熔岩金刚！"""

    activate = Summon(CONTROLLER, "BRMA14_9"), Summon(CONTROLLER, "BRMA14_10")


class BRMA14_8H:
    """Activate Magmatron / 激活熔岩金刚
    激活熔岩金刚！"""

    activate = Summon(CONTROLLER, "BRMA14_9H"), Summon(CONTROLLER, "BRMA14_10H")


class BRMA14_10:
    """Activate! / 激活！
    随机激活一个金刚。"""

    entourage = ["BRMA14_3", "BRMA14_5", "BRMA14_7", "BRMA14_9"]
    activate = Summon(CONTROLLER, RandomEntourage())


class BRMA14_10H:
    """Activate! / 激活！
    随机激活一个金刚。"""

    entourage = ["BRMA14_3", "BRMA14_5H", "BRMA14_7H", "BRMA14_9H"]
    activate = Summon(CONTROLLER, RandomEntourage())


class BRMA15_2:
    """The Alchemist / 炼金师
    被动 每当一个随从被召唤时，交换其攻击力和生命值。"""

    events = Summon(ALL_PLAYERS, MINION).on(Buff(Summon.CARD, "BRMA15_2e"))


class BRMA15_2e(AttackHealthSwapBuff()):
    tags = {GameTag.CARDNAME: "The Alchemist Attack/Health Swap Buff" ""}


class BRMA15_2H:
    """The Alchemist / 炼金师
    被动 所有随从的攻击力和生命值互换。你的随从拥有+2/+2。"""

    events = (
        Summon(ALL_PLAYERS, MINION).on(Buff(Summon.CARD, "BRMA15_2e")),
        Summon(CONTROLLER, MINION).on(Buff(Summon.CARD, "BRMA15_2He")),
    )


# Potion of Might (The Alchemist)
BRMA15_2He = buff(+2, +2)


class BRMA16_2:
    """Echolocate / 回音定位
    装备一把武器，每当你的对手使用牌时，该武器就会增强。"""

    activate = Summon(CONTROLLER, "BRMA16_5")


class BRMA16_2H:
    """Echolocate / 回音定位
    装备一把武器，每当你的对手使用牌时，该武器就会增强。"""

    activate = Summon(CONTROLLER, "BRMA16_5")


class BRMA17_5:
    """Bone Minions / 白骨爪牙
    召唤两个2/1的白骨结构体。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "BRMA17_6") * 2


class BRMA17_5H:
    """Bone Minions / 白骨爪牙
    召唤两个4/2的白骨结构体。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "BRMA17_6H") * 2


class BRMA17_8:
    """Nefarian Strikes! / 黑龙吐息
    奈法利安从空中喷吐火焰！"""

    activate = Hit(ENEMY_HERO, 1) * RandomNumber(0, 1, 2, 3, 4, 20)


class BRMA17_8H:
    """Nefarian Strikes! / 黑龙吐息
    奈法利安从空中喷吐火焰！"""

    activate = Hit(ENEMY_HERO, 1) * RandomNumber(0, 1, 2, 3, 4, 20)


##
# Minions


class BRMA03_3:
    """Moira Bronzebeard / 茉艾拉·铜须
    索瑞森无法使用英雄技能。 不会攻击随从，除了拥有嘲讽的随从。"""

    update = Refresh(ALL_HERO_POWERS + ID("BRMA03_2"), {GameTag.CANT_PLAY: True})


class BRMA03_3H:
    """Moira Bronzebeard / 茉艾拉·铜须
    索瑞森无法使用英雄技能。 不会攻击随从，除了拥有嘲讽的随从。"""

    update = Refresh(ALL_HERO_POWERS + ID("BRMA03_2"), {GameTag.CANT_PLAY: True})


class BRMA10_4:
    """Corrupted Egg / 腐化的蛋
    当本随从的生命值大于 或等于4时便会孵化。"""

    update = (CURRENT_HEALTH(SELF) >= 4) & (
        Destroy(SELF),
        Summon(CONTROLLER, "BRMA10_5"),
    )


class BRMA10_4H:
    """Corrupted Egg / 腐化的蛋
    当本随从的生命值大于或等于5时，便会孵化。"""

    update = (CURRENT_HEALTH(SELF) >= 5) & (
        Destroy(SELF),
        Summon(CONTROLLER, "BRMA10_5H"),
    )


class BRMA04_3:
    """Firesworn / 火誓者
    亡语： 在本回合中每死亡一个火誓者，便对敌方英雄造成1点伤害。"""

    deathrattle = Hit(ENEMY_HERO, Count(ID("BRMA04_3") + KILLED_THIS_TURN))


class BRMA04_3H:
    """Firesworn / 火誓者
    亡语： 在本回合中每死亡一个火誓者，便对敌方英雄造成3点伤害。"""

    deathrattle = Hit(ENEMY_HERO, Count(ID("BRMA04_3H") + KILLED_THIS_TURN))


class BRMA12_8t:
    """Chromatic Dragonkin"""

    events = Play(OPPONENT, SPELL).on(Buff(SELF, "BRMA12_8te"))


BRMA12_8te = buff(+2, +2)


class BRMA13_5:
    """Son of the Flame / 烈焰之子
    战吼：造成6点伤害。"""

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, 6)


##
# Spells


class BRMA_01:
    """Flameheart / 烈焰之心
    抽两张牌。 获得4点护甲值。"""

    play = Draw(CONTROLLER) * 2, GainArmor(FRIENDLY_HERO, 4)


class BRMA01_4:
    """Get 'em! / 搞定他们!
    召唤四个1/1并具有嘲讽的 矮人。"""

    play = Summon(CONTROLLER, "BRMA01_4t") * 4


class BRMA05_3:
    """Living Bomb / 活体炸弹
    选择一个敌方随从。在你的下个回合开始时，如果该随从依然存活，则对所有敌人造成$5点伤害。"""

    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "BRMA05_3e")


class BRMA05_3e:
    events = OWN_TURN_BEGIN.on(Hit(ENEMY_CHARACTERS, 5))


class BRMA05_3H:
    """Living Bomb / 活体炸弹
    选择一个敌方随从。在你的下个回合开始时，如果该随从依然存活，则对所有敌人造成$10点伤害。"""

    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "BRMA05_3He")


class BRMA05_3He:
    events = OWN_TURN_BEGIN.on(Hit(ENEMY_CHARACTERS, 10))


class BRMA07_3:
    """TIME FOR SMASH / 砸烂
    随机对一个敌人造成$5点伤害。获得5点护甲值。"""

    play = Hit(RANDOM_ENEMY_MINION, 5), GainArmor(FRIENDLY_HERO, 5)


class BRMA08_3:
    """Drakkisath's Command / 达基萨斯的命令
    消灭一个随从。获得10点护甲值。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Destroy(TARGET), GainArmor(FRIENDLY_HERO, 10)


class BRMA09_6:
    """The True Warchief / 真正的酋长
    消灭一个传说随从。"""

    requirements = {
        PlayReq.REQ_LEGENDARY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Destroy(TARGET)


class BRMA04_4:
    """Rock Out / 乱石滚动
    召唤三个火誓者。过载：（2）"""

    play = Summon(CONTROLLER, "BRMA04_3") * 3


class BRMA04_4H:
    """Rock Out / 乱石滚动
    召唤三个火誓者。过载：（2）"""

    play = Summon(CONTROLLER, "BRMA04_3H") * 3


class BRMA11_3:
    """Burning Adrenaline / 燃烧刺激
    对敌方英雄造成$2点伤害。"""

    play = Hit(ENEMY_HERO, 2)


class BRMA12_8:
    """Chromatic Mutation / 多彩变形
    将一个随从 变形成为2/2的多彩龙人。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Morph(TARGET, "BRMA12_8t")


class BRMA14_11:
    """Recharge / 充能
    填满所有空的法力水晶。"""

    play = FillMana(CONTROLLER, USED_MANA(CONTROLLER))


class BRMA13_8:
    """DIE, INSECT! / 死吧，虫子！
    随机对一个敌人造成$8点伤害。"""

    play = Hit(RANDOM_ENEMY_CHARACTER, 8)


class BRMA15_3:
    """Release the Aberrations! / 释放畸变怪！
    召唤三个畸变怪。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "BRMA15_4") * 3


class BRMA14_3:
    """Arcanotron / 奥能金刚
    双方玩家拥有法术伤害+2。"""

    update = Refresh(ALL_PLAYERS, {GameTag.SPELLPOWER: +2})


class BRMA14_5:
    """Toxitron / 剧毒金刚
    在你的回合开始时，对所有其他随从造成1点伤害。"""

    events = OWN_TURN_BEGIN.on(Hit(ALL_MINIONS - SELF, 1))


class BRMA14_5H:
    """Toxitron / 剧毒金刚
    在你的回合开始时，对所有其他随从造成1点伤害。"""

    events = OWN_TURN_BEGIN.on(Hit(ALL_MINIONS - SELF, 1))


class BRMA14_7:
    """Electron / 电荷金刚
    所有法术的法力值消耗减少（3）点。"""

    update = Refresh(IN_HAND + SPELL, {GameTag.COST: -3})


class BRMA14_7H:
    """Electron / 电荷金刚
    所有法术的法力值消耗减少（3）点。"""

    update = Refresh(IN_HAND + SPELL, {GameTag.COST: -3})


class BRMA14_9:
    """Magmatron / 熔岩金刚
    每当一个玩家使用一张牌时，熔岩金刚便对其造成2点伤害。"""

    events = Play().on(Hit(ALL_HEROES + CONTROLLED_BY(Play.PLAYER)))


class BRMA14_9H:
    """Magmatron / 熔岩金刚
    每当一个玩家使用一张牌时，熔岩金刚便对其造成2点伤害。"""

    events = Play().on(Hit(ALL_HEROES + CONTROLLED_BY(Play.PLAYER)))


class BRMA16_3:
    """Sonic Breath / 音波吐息
    对一个随从造成$3点伤害。使你的武器获得+3攻击力。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_WEAPON_EQUIPPED: 0,
    }
    play = Hit(TARGET, 3), Buff(FRIENDLY_WEAPON, "BRMA16_3e")


BRMA16_3e = buff(atk=3)


class BRMA16_4:
    """Reverberating Gong / 回响之锣
    摧毁你对手的武器。"""

    requirements = {PlayReq.REQ_ENEMY_WEAPON_EQUIPPED: 0}
    play = Destroy(ENEMY_WEAPON)


class BRMA17_4:
    """LAVA! / 熔岩！
    对所有随从造成$2点伤害。"""

    play = Hit(ALL_MINIONS, 2)


##
# Weapons


class BRMA10_6:
    """Razorgore's Claws / 拉佐格尔之爪
    每当一个腐化的蛋死亡，便获得+1攻击力。"""

    events = Death(MINION + ID("BRMA10_4")).on(Buff(SELF, "BRMA10_6e"))


BRMA10_6e = buff(atk=1)


class BRMA16_5:
    """Dragonteeth / 龙牙
    每当你的对手使用一张牌时，便获得+1攻击力。"""

    events = Play(OPPONENT).on(Buff(SELF, "BRMA16_5e"))


BRMA16_5e = buff(atk=1)


##
# Brood Afflictions (Chromaggus)


class BRMA12_3:
    """Brood Affliction: Red / 龙血之痛：红
    如果这张牌在你的手牌中，在你的回合开始时，你的英雄受到1点伤害。"""

    class Hand:
        events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_HERO, 1))


class BRMA12_3H:
    """Brood Affliction: Red / 龙血之痛：红
    如果这张牌在你的手牌中，在你的回合开始时，你的英雄受到3点伤害。"""

    class Hand:
        events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_HERO, 3))


class BRMA12_4:
    """Brood Affliction: Green / 龙血之痛：绿
    如果这张牌在你的手牌中，在你的回合开始时，敌方英雄恢复#2点生命值。"""

    class Hand:
        events = OWN_TURN_BEGIN.on(Heal(ENEMY_HERO, 2))


class BRMA12_4H:
    """Brood Affliction: Green / 龙血之痛：绿
    如果这张牌在你的手牌中，在你的回合开始时，敌方英雄恢复#6点生命值。"""

    class Hand:
        events = OWN_TURN_BEGIN.on(Heal(ENEMY_HERO, 6))


class BRMA12_5:
    """Brood Affliction: Blue / 龙血之痛：蓝
    如果这张牌在你的手牌中，克洛玛古斯的法术的法力值消耗就减少（1）点。"""

    class Hand:
        update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: -1})


class BRMA12_5H:
    """Brood Affliction: Blue / 龙血之痛：蓝
    如果这张牌在你的手牌中，克洛玛古斯的法术的法力值消耗就减少（3）点。"""

    class Hand:
        update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: -3})


class BRMA12_6:
    """Brood Affliction: Black / 龙血之痛：黑
    当这张牌在你的手牌中时，每当克洛玛古斯抽牌，他都会获取一张该牌的复制。"""

    class Hand:
        events = Draw(OPPONENT).on(Give(OPPONENT, Copy(Draw.CARD)))


class BRMA12_6H:
    """Brood Affliction: Black / 龙血之痛：黑
    当这张牌在你的手牌中时，每当克洛玛古斯抽牌，他都会获取一张该牌的复制。"""

    class Hand:
        events = Draw(OPPONENT).on(Give(OPPONENT, Copy(Draw.CARD)))


class BRMA12_7:
    """Brood Affliction: Bronze / 龙血之痛：青铜
    如果这张牌在你的手牌中，克洛玛古斯的随从的法力值消耗就减少（1）点。"""

    class Hand:
        update = Refresh(ENEMY_HAND + MINION, {GameTag.COST: -1})


class BRMA12_7H:
    """Brood Affliction: Bronze / 龙血之痛：青铜
    如果这张牌在你的手牌中，克洛玛古斯的随从的法力值消耗就减少（3）点。"""

    class Hand:
        update = Refresh(ENEMY_HAND + MINION, {GameTag.COST: -3})
