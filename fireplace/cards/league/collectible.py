from ..utils import *


##
# Minions


class LOE_003:
    """Ethereal Conjurer / 虚灵巫师
    战吼： 发现一张法术牌。"""

    play = DISCOVER(RandomSpell())


class LOE_006:
    """Museum Curator / 博物馆馆长
    战吼：发现一张亡语牌，其法力值消耗减少（1）点。"""

    play = DISCOVER(RandomCollectible(deathrattle=True))


class LOE_009:
    """Obsidian Destroyer / 黑曜石毁灭者
    在你的回合结束时，召唤一只1/1并具有嘲讽的甲虫。"""

    events = OWN_TURN_END.on(Summon(CONTROLLER, "LOE_009t"))


class LOE_011:
    """Reno Jackson / 雷诺·杰克逊
    战吼：如果你的牌库里没有相同的牌，则为你的英雄恢复所有生命值。"""

    powered_up = -FindDuplicates(FRIENDLY_DECK)
    play = powered_up & FullHeal(FRIENDLY_HERO)


class LOE_012:
    """Tomb Pillager / 盗墓匪贼
    亡语：获取一张 幸运币。"""

    deathrattle = Give(CONTROLLER, "GAME_005")


class LOE_016:
    """Rumbling Elemental / 顽石元素
    在你使用一张具有 战吼的随从牌后，随机对一个敌人造成2点伤害。"""

    events = Play(CONTROLLER, MINION + BATTLECRY).after(Hit(RANDOM_ENEMY_CHARACTER, 2))


class LOE_017:
    """Keeper of Uldaman / 奥达曼守护者
    战吼： 将一个随从的攻击力和生命值变为3。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Buff(TARGET, "LOE_017e")


class LOE_017e:
    atk = SET(3)
    max_health = SET(3)


class LOE_018:
    """Tunnel Trogg / 坑道穴居人
    每当你过载时，每一个被锁的法力水晶会使其获得+1攻击力。"""

    events = Overload(CONTROLLER).on(Buff(SELF, "LOE_018e") * Overload.AMOUNT)


LOE_018e = buff(atk=1)


class LOE_019:
    """Unearthed Raptor / 化石迅猛龙
    战吼：选择一个友方随从，获得其亡语的复制。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0,
    }
    play = CopyDeathrattleBuff(TARGET, "LOE_019e")


class LOE_020:
    """Desert Camel / 大漠沙驼
    战吼：从双方的牌库中各将一个法力值消耗为（1）的随从置入战场。"""

    play = (
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + (COST == 1))),
        Summon(OPPONENT, RANDOM(ENEMY_DECK + (COST == 1))),
    )


class LOE_023:
    """Dark Peddler / 黑市摊贩
    战吼：发现一张 法力值消耗为（1）的卡牌。"""

    play = DISCOVER(RandomCollectible(cost=1))


class LOE_029:
    """Jeweled Scarab / 宝石甲虫
    战吼：发现一张 法力值消耗为（3）的卡牌。"""

    play = DISCOVER(RandomCollectible(cost=3))


class LOE_038:
    """Naga Sea Witch / 纳迦海巫
    你的卡牌法力值消耗为（5）点。"""

    update = Refresh(FRIENDLY_HAND, {GameTag.COST: SET(5)})


class LOE_039:
    """Gorillabot A-3 / A3型机械金刚
    战吼：如果你控制着其他机械，发现一张机械牌。"""

    powered_up = Find(FRIENDLY_MINIONS + MECH - SELF)
    play = powered_up & DISCOVER(RandomMech())


class LOE_046:
    """Huge Toad / 巨型蟾蜍
    亡语：随机对一个敌人造成1点伤害。"""

    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 1)


class LOE_047:
    """Tomb Spider / 墓穴蜘蛛
    战吼： 发现一张野兽牌。"""

    play = DISCOVER(RandomBeast())


class LOE_050:
    """Mounted Raptor / 骑乘迅猛龙
    亡语：随机召唤一个法力值消耗为（1）的随从。"""

    deathrattle = Summon(CONTROLLER, RandomMinion(cost=1))


class LOE_051:
    """Jungle Moonkin / 丛林枭兽
    双方玩家拥有 法术伤害+2。"""

    update = Refresh(OPPONENT, {GameTag.SPELLPOWER: +2})


class LOE_053:
    """Djinni of Zephyrs / 西风灯神
    在你对一个其他友方随从施放法术后，将法术效果复制在本随从身上。"""

    events = Play(CONTROLLER, SPELL, FRIENDLY + MINION - SELF).after(
        Battlecry(Play.CARD, SELF)
    )


class LOE_061:
    """Anubisath Sentinel / 阿努比萨斯哨兵
    亡语：随机使一个友方随从获得+3/+3。"""

    deathrattle = Buff(RANDOM_OTHER_FRIENDLY_MINION, "LOE_061e")


LOE_061e = buff(+3, +3)


class LOE_073:
    """Fossilized Devilsaur / 化石魔暴龙
    战吼： 如果你控制着其他野兽，获得嘲讽。"""

    powered_up = Find(FRIENDLY_MINIONS + BEAST)
    play = powered_up & Taunt(SELF)


# Fossilized (Unused)
LOE_073e = buff(taunt=True)


class LOE_076:
    """Sir Finley Mrrgglton / 芬利·莫格顿爵士
    战吼：发现一个新的基础英雄技能。"""

    play = GenericChoice(
        CONTROLLER, RandomBasicHeroPower(exclude=FRIENDLY_HERO_POWER) * 3
    )


class LOE_077:
    """Brann Bronzebeard / 布莱恩·铜须
    你的战吼会触发 两次。"""

    update = Refresh(CONTROLLER, {enums.EXTRA_BATTLECRIES: True})


class LOE_079:
    """Elise Starseeker / 伊莉斯·逐星
    战吼：将“黄金猿藏宝图”洗入你的牌库。"""

    requirements = {PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Shuffle(CONTROLLER, "LOE_019t")


class LOE_019t:
    """Map to the Golden Monkey"""

    play = Shuffle(CONTROLLER, "LOE_019t2"), Draw(CONTROLLER)


class LOE_019t2:
    """Golden Monkey"""

    play = Morph(FRIENDLY + (IN_HAND | IN_DECK), RandomLegendaryMinion())


class LOE_086:
    """Summoning Stone / 召唤石
    每当你施放一个法术，随机召唤一个法力值消耗相同的随从。"""

    events = OWN_SPELL_PLAY.on(
        Summon(CONTROLLER, RandomMinion(cost=Attr(Play.CARD, GameTag.COST)))
    )


class LOE_089:
    """Wobbling Runts / 摇摆的俾格米
    亡语：召唤三个2/2的俾格米。"""

    deathrattle = Summon(CONTROLLER, ["LOE_089t", "LOE_089t2", "LOE_089t3"])


class LOE_092:
    """Arch-Thief Rafaam / 虚灵大盗拉法姆
    战吼：发现一张强大的神器牌。"""

    play = DISCOVER(RandomID("LOEA16_3", "LOEA16_5", "LOEA16_4"))


class LOEA16_3:
    """Lantern of Power / 能量之光
    使一个随从获得+10/+10。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "LOEA16_3e")


LOEA16_3e = buff(+10, +10)


class LOEA16_4:
    """Timepiece of Horror / 恐怖丧钟
    造成$10点伤害，随机分配到所有敌人身上。"""

    play = Hit(RANDOM_ENEMY_CHARACTER, 1) * SPELL_DAMAGE(10)


class LOEA16_5:
    """Mirror of Doom / 末日镜像
    用3/3的木乃伊僵尸填满你的面板。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "LOEA16_5t")


class LOE_107:
    """Eerie Statue / 诡异的雕像
    除非它是战场上唯一的一个随从，否则无法进行攻击。"""

    update = Find(ALL_MINIONS - SELF) & Refresh(SELF, {GameTag.CANT_ATTACK: True})


class LOE_110:
    """Ancient Shade / 远古暗影
    战吼：将一张“远古诅咒”牌洗入你的牌库。当你抽到该牌，便会受到7点伤害。"""

    play = Shuffle(CONTROLLER, "LOE_110t")


class LOE_110t:
    """Ancient Curse"""

    play = Hit(FRIENDLY_HERO, 7)
    draw = CAST_WHEN_DRAWN


class LOE_116:
    """Reliquary Seeker / 遗物搜寻者
    战吼：如果你拥有六个其他随从，便获得+4/+4。"""

    powered_up = Count(FRIENDLY_MINIONS) == 6
    play = (Count(FRIENDLY_MINIONS) == 7) & Buff(SELF, "LOE_009e")


LOE_009e = buff(+4, +4)


class LOE_119:
    """Animated Armor / 活化铠甲
    你的英雄每次只会受到1点伤害。"""

    update = Refresh(FRIENDLY_HERO, {GameTag.HEAVILY_ARMORED: True})


##
# Spells


class LOE_002:
    """Forgotten Torch / 老旧的火把
    造成$3点伤害。将一张可造成6点伤害的“炽烈的火把”洗入你的牌库。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3), Shuffle(CONTROLLER, "LOE_002t")


class LOE_002t:
    play = Hit(TARGET, 6)
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}


class LOE_007:
    """Curse of Rafaam / 拉法姆的诅咒
    使你的对手获得一张“诅咒”。在对手的回合开始时，如果它在对手的手牌中，则造成2点伤害。"""

    play = Give(OPPONENT, "LOE_007t")


class LOE_007t:
    """Cursed!"""

    class Hand:
        events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_HERO, 2))


class LOE_026:
    """Anyfin Can Happen / 亡者归来
    召唤七个在本局对战中死亡的 鱼人。"""

    play = Summon(CONTROLLER, Copy(RANDOM(KILLED + MURLOC) * 7))


class LOE_104:
    """Entomb / 埋葬
    选择一个敌方随从。将该随从洗入你的牌库。"""

    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Steal(TARGET), Shuffle(CONTROLLER, TARGET)


class LOE_105:
    """Explorer's Hat / 探险帽
    使一个随从获得+1/+1，以及“亡语：获取一张探险帽”。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "LOE_105e")


class LOE_105e:
    deathrattle = Give(CONTROLLER, "LOE_105")
    tags = {
        GameTag.ATK: +1,
        GameTag.HEALTH: +1,
        GameTag.DEATHRATTLE: True,
    }


class LOE_111:
    """Excavated Evil / 极恶之咒
    对所有随从造成$3点伤害。将该牌洗入你对手的牌库。"""

    play = Hit(ALL_MINIONS, 3), Shuffle(OPPONENT, Copy(SELF))


class LOE_113:
    """Everyfin is Awesome / 鱼人恩典
    使你的所有随从获得+2/+2。你每控制一个鱼人，本牌的法力值消耗便减少（1）点。"""

    cost_mod = -Count(FRIENDLY_MINIONS + MURLOC)
    play = Buff(FRIENDLY_MINIONS, "LOE_113e")


LOE_113e = buff(+2, +2)


class LOE_115:
    """Raven Idol / 乌鸦神像
    抉择： 发现一张随从牌；或者发现一张法术牌。"""

    choose = ("LOE_115a", "LOE_115b")
    play = ChooseBoth(CONTROLLER) & (DISCOVER(RandomMinion()), DISCOVER(RandomSpell()))


class LOE_115a:
    play = DISCOVER(RandomMinion())


class LOE_115b:
    play = DISCOVER(RandomSpell())


##
# Secrets


class LOE_021:
    """Dart Trap / 毒镖陷阱
    奥秘： 在对方使用英雄技能后，随机对一个敌人造成$5点伤害。"""

    secret = Activate(OPPONENT, HERO_POWER).on(
        Reveal(SELF), Hit(RANDOM_ENEMY_CHARACTER, 5)
    )


class LOE_027:
    """Sacred Trial / 审判
    奥秘：在你的对手使用一张随从牌后，如果他控制至少三个其他随从，则将其消灭。"""

    secret = Play(OPPONENT, MINION | HERO).after(
        (Count(ENEMY_MINIONS) >= 4) & (Reveal(SELF), Destroy(Play.CARD))
    )


##
# Weapons


class LOE_118:
    """Cursed Blade / 诅咒之刃
    你的英雄受到的所有伤害效果翻倍。"""

    update = Refresh(FRIENDLY_HERO, buff="LOE_118e")


class LOE_118e:
    tags = {GameTag.INCOMING_DAMAGE_MULTIPLIER: True}
