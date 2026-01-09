from ..utils import *


class EX1_002:
    """The Black Knight / 黑骑士
    可交易 战吼：消灭一个具有嘲讽的敌方随从。"""

    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_MUST_TARGET_TAUNTER: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Destroy(TARGET)


class EX1_012:
    """Bloodmage Thalnos / 血法师萨尔诺斯
    法术伤害+1，亡语：抽一张牌。"""

    deathrattle = Draw(CONTROLLER)


class EX1_014:
    """King Mukla / 穆克拉
    战吼：使你的对手获得两根香蕉。"""

    play = Give(OPPONENT, "EX1_014t") * 2


class EX1_014t:
    """Bananas"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "EX1_014te")


EX1_014te = buff(+1, +1)


class EX1_016:
    """Sylvanas Windrunner / 希尔瓦娜斯·风行者
    亡语：随机夺取一个敌方随从的控制权。"""

    deathrattle = Steal(RANDOM_ENEMY_MINION)


class EX1_062:
    """Old Murk-Eye / 老瞎眼
    冲锋，在战场上每有一个其他鱼人便拥有+1攻击力。"""

    update = Refresh(SELF, {GameTag.ATK: Count(ALL_MINIONS + MURLOC - SELF)})


class EX1_083:
    """Tinkmaster Overspark / 工匠大师欧沃斯巴克
    战吼： 随机使另一个随从变形成为一个5/5的魔暴龙或一个1/1的松鼠。"""

    play = Morph(RANDOM(ALL_MINIONS - SELF), RandomID("EX1_tk28", "EX1_tk29"))


class EX1_100:
    """Lorewalker Cho / 游学者周卓
    每当一个玩家施放一个法术，复制该法术，将其置入另一个玩家的手牌。"""

    events = Play(ALL_PLAYERS, SPELL).on(Give(Opponent(Play.PLAYER), Copy(Play.CARD)))


class EX1_110:
    """Cairne Bloodhoof / 凯恩·血蹄
    嘲讽。亡语：召唤一个5/5的贝恩·血蹄。"""

    deathrattle = Summon(CONTROLLER, "EX1_110t")


class EX1_112:
    """Gelbin Mekkatorque / 格尔宾·梅卡托克
    战吼：召唤一项惊人的发明。"""

    entourage = ["Mekka1", "Mekka2", "Mekka3", "Mekka4"]
    play = Summon(CONTROLLER, RandomEntourage())


class Mekka1:
    """Homing Chicken"""

    events = OWN_TURN_BEGIN.on(Destroy(SELF), Draw(CONTROLLER) * 3)


class Mekka2:
    """Repair Bot"""

    events = OWN_TURN_END.on(Heal(RANDOM(DAMAGED_CHARACTERS), 6))


class Mekka3:
    """Emboldener 3000"""

    events = OWN_TURN_END.on(Buff(RANDOM_MINION, "Mekka3e"))


Mekka3e = buff(+1, +1)


class Mekka4:
    """Poultryizer"""

    events = OWN_TURN_BEGIN.on(Morph(RANDOM_MINION, "Mekka4t"))


class EX1_116:
    """Leeroy Jenkins / 火车王里诺艾
    冲锋，战吼： 为你的对手召唤两条1/1的雏龙。"""

    play = Summon(OPPONENT, "EX1_116t") * 2


class EX1_249:
    """Baron Geddon / 迦顿男爵
    在你的回合结束时，对所有其他角色造成2点伤害。"""

    events = OWN_TURN_END.on(Hit(ALL_CHARACTERS - SELF, 2))


class EX1_298:
    """Ragnaros the Firelord / 炎魔之王拉格纳罗斯
    无法攻击。在你的回合结束时，随机对一个敌人造成8点伤害。"""

    events = OWN_TURN_END.on(Hit(RANDOM_ENEMY_CHARACTER, 8))


class EX1_557:
    """Nat Pagle / 纳特·帕格
    在你的回合开始时，你有50%的几率额外抽一张牌。"""

    events = OWN_TURN_BEGIN.on((COINFLIP , Draw(CONTROLLER)))


class EX1_558:
    """Harrison Jones / 哈里森·琼斯
    战吼：摧毁对手的武器，并抽数量等同于其耐久度的牌。"""

    play = (
        Draw(CONTROLLER) * Attr(ENEMY_WEAPON, GameTag.DURABILITY),
        Destroy(ENEMY_WEAPON),
    )


class EX1_560:
    """Nozdormu / 诺兹多姆
    玩家只有15秒的时间来进行他们的回合。"""

    update = Refresh(ALL_PLAYERS, {GameTag.TIMEOUT: lambda self, i: 15})


class EX1_561:
    """Alexstrasza / 阿莱克丝塔萨
    战吼： 将一方英雄的剩余生命值变为15。"""

    requirements = {PlayReq.REQ_HERO_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = (
        (Attr(TARGET, GameTag.HEALTH) <= 15) & Buff(TARGET, "EX1_561e"),
        SetCurrentHealth(TARGET, 15),
    )


class EX1_561e:
    max_health = SET(15)


class EX1_562:
    """Onyxia / 奥妮克希亚
    战吼：召唤数条1/1的雏龙，直到你的随从数量达到上限。"""

    play = SummonBothSides(CONTROLLER, "ds1_whelptoken") * 7


class EX1_572:
    """Ysera / 伊瑟拉
    在你的回合结束时，随机获取两张梦境牌。"""

    events = OWN_TURN_END.on(Give(CONTROLLER, RandomCard(card_class=CardClass.DREAM)))


class DREAM_02:
    """Ysera Awakens / 伊瑟拉苏醒
    对除了伊瑟拉之外的所有角色造成$5点伤害。"""

    play = Hit(ALL_CHARACTERS - ID("EX1_572"), 5)


class DREAM_04:
    """Dream / 梦境
    将一个随从移回其拥有者的 手牌。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Bounce(TARGET)


class DREAM_05:
    """Nightmare / 梦魇
    使一个随从获得+5/+5，在你的下个回合开始时，消灭该随从。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "DREAM_05e")


class DREAM_05e:
    events = OWN_TURN_BEGIN.on(Destroy(SELF))


class EX1_577:
    """The Beast / 比斯巨兽
    亡语： 为你的对手召唤一个3/3的皮普·急智。"""

    deathrattle = Summon(OPPONENT, "EX1_finkle")


class EX1_614:
    """Xavius / 萨维斯
    在你使用一张牌后，召唤一个2/1的萨特。"""

    events = OWN_CARD_PLAY.on(Summon(CONTROLLER, "EX1_614t"))


class NEW1_024:
    """Captain Greenskin / 绿皮船长
    战吼：使你的武器获得+1/+1。"""

    play = Buff(FRIENDLY_WEAPON, "NEW1_024o")


NEW1_024o = buff(+1, +1)


class NEW1_029:
    """Millhouse Manastorm / 米尔豪斯·法力风暴
    战吼：下个回合敌方法术的法力值消耗为（0）点。"""

    play = Buff(ENEMY_HERO, "NEW1_029t")


class NEW1_029t:
    update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: lambda self, i: 0})
    events = OWN_TURN_BEGIN.on(Destroy(SELF))


class NEW1_030:
    """Deathwing / 死亡之翼
    战吼： 消灭所有其他随从，并弃掉你的手牌。"""

    play = Destroy(ALL_MINIONS - SELF), Discard(FRIENDLY_HAND)


class NEW1_038:
    """Gruul / 格鲁尔
    在每个回合结束时，获得+1/+1。"""

    events = TURN_END.on(Buff(SELF, "NEW1_038o"))


NEW1_038o = buff(+1, +1)


class NEW1_040:
    """Hogger / 霍格
    在你的回合结束时，召唤一个2/2并具有嘲讽的豺狼人。"""

    events = OWN_TURN_END.on(Summon(CONTROLLER, "NEW1_040t"))


class PRO_001:
    """Elite Tauren Chieftain / 精英牛头人酋长
    战吼：让两位玩家都具有摇滚的能力！（双方各获得一张强力和弦牌）"""

    entourage = ["PRO_001a", "PRO_001b", "PRO_001c"]
    play = Give(ALL_PLAYERS, RandomEntourage())


class PRO_001a:
    """I Am Murloc"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "PRO_001at") * RandomNumber(3, 4, 5)


class PRO_001b:
    """Rogues Do It..."""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 4), Draw(CONTROLLER)


class PRO_001c:
    """Power of the Horde"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    entourage = ["CS2_121", "EX1_021", "EX1_023", "EX1_110", "EX1_390", "CS2_179"]
    play = Summon(CONTROLLER, RandomEntourage())


class EX1_189:
    """Brightwing / 光明之翼
    战吼：随机将一张传说随从牌置入你的 手牌。"""

    # <b>Battlecry:</b> Add a random <b>Legendary</b> minion to your_hand.
    play = Give(CONTROLLER, RandomLegendaryMinion())


class EX1_190:
    """High Inquisitor Whitemane / 大检察官怀特迈恩
    战吼：召唤所有在本回合中死亡的友方 随从。"""

    # <b>Battlecry:</b> Summon all friendly minions that died_this turn.
    play = Summon(CONTROLLER, Copy(FRIENDLY + MINION + KILLED_THIS_TURN))
