from ..utils import *


##
# Minions


class BRM_002:
    """Flamewaker / 火妖
    在你施放一个法术后，造成2点伤害，随机分配到所有敌人身上。"""

    events = OWN_SPELL_PLAY.after(Hit(ENEMY_CHARACTERS, 1) * 2)


class BRM_004:
    """Twilight Whelp / 暮光雏龙
    战吼：如果你的手牌中有龙牌，便获得+2生命值。"""

    powered_up = HOLDING_DRAGON
    play = powered_up & Buff(SELF, "BRM_004e")


BRM_004e = buff(health=2)


class BRM_006:
    """Imp Gang Boss / 小鬼首领
    每当本随从受到伤害，召唤一个1/1的 小鬼。"""

    events = SELF_DAMAGE.on(Summon(CONTROLLER, "BRM_006t"))


class BRM_008:
    """Dark Iron Skulker / 黑铁潜藏者
    战吼： 对所有未受伤的敌方随从造成2点伤害。"""

    play = Hit(ENEMY_MINIONS - DAMAGED, 2)


class BRM_009:
    """Volcanic Lumberer / 火山邪木
    嘲讽 在本回合中每有一个随从死亡，本牌的法力值消耗便减少（1）点。"""

    cost_mod = -Attr(GAME, GameTag.NUM_MINIONS_KILLED_THIS_TURN)


class BRM_010:
    """Druid of the Flame / 烈焰德鲁伊
    抉择：变形成为5/2的随从；或者变形成为2/5的随从。"""

    choose = ("BRM_010a", "BRM_010b")
    play = ChooseBoth(CONTROLLER) & Morph(SELF, "OG_044b")


class BRM_010a:
    play = Morph(SELF, "BRM_010t")


class BRM_010b:
    play = Morph(SELF, "BRM_010t2")


class BRM_012:
    """Fireguard Destroyer / 火焰驱逐者
    战吼：获得1-4点攻击力。过载：（1）"""

    play = Buff(SELF, "BRM_012e") * RandomNumber(1, 2, 3, 4)


BRM_012e = buff(atk=1)


class BRM_014:
    """Core Rager / 熔火怒犬
    战吼：如果你没有其他手牌，则获得+3/+3。"""

    powered_up = Count(FRIENDLY_HAND - SELF) == 0
    play = EMPTY_HAND & Buff(SELF, "BRM_014e")


BRM_014e = buff(+3, +3)


class BRM_016:
    """Axe Flinger / 掷斧者
    每当本随从受到伤害，对敌方英雄造成 2点伤害。"""

    events = SELF_DAMAGE.on(Hit(ENEMY_HERO, 2))


class BRM_018:
    """Dragon Consort / 龙王配偶
    战吼：你的下一张龙牌的法力值消耗减少（2）点。"""

    play = Buff(CONTROLLER, "BRM_018e")


class BRM_018e:
    update = Refresh(FRIENDLY_HAND + DRAGON, {GameTag.COST: -2})
    events = Play(CONTROLLER, DRAGON).on(Destroy(SELF))


class BRM_019:
    """Grim Patron / 恐怖的奴隶主
    在本随从受到伤害并存活下来后，召唤另一个恐怖的奴隶主。"""

    events = SELF_DAMAGE.on(Dead(SELF) | Summon(CONTROLLER, "BRM_019"))


class BRM_020:
    """Dragonkin Sorcerer / 龙人巫师
    每当你以本随从为目标施放一个法术时，获得+1/+1。"""

    events = Play(CONTROLLER, SPELL, SELF).on(Buff(SELF, "BRM_020e"))


BRM_020e = buff(+1, +1)


class BRM_022:
    """Dragon Egg / 龙蛋
    每当本随从受到 伤害，召唤一条2/1的雏龙。"""

    events = SELF_DAMAGE.on(Summon(CONTROLLER, "BRM_022t"))


class BRM_024:
    """Drakonid Crusher / 龙人打击者
    战吼：如果你对手的生命值小于或等于15点，便获得+3/+3。"""

    powered_up = CURRENT_HEALTH(ENEMY_HERO) <= 15
    play = powered_up & Buff(SELF, "BRM_024e")


BRM_024e = buff(+3, +3)


class BRM_025:
    """Volcanic Drake / 火山幼龙
    在本回合中每有一个随从死亡，本牌的 法力值消耗便减少（1）点。"""

    cost_mod = -Attr(GAME, GameTag.NUM_MINIONS_KILLED_THIS_TURN)


class BRM_026:
    """Hungry Dragon / 饥饿的巨龙
    战吼：为你的对手随机召唤一个法力值消耗为（1）的随从。"""

    play = Summon(OPPONENT, RandomMinion(cost=1))


class BRM_027:
    """Majordomo Executus / 管理者埃克索图斯
    亡语： 用炎魔之王拉格纳罗斯替换你的英雄。"""

    deathrattle = Summon(CONTROLLER, "BRM_027h")


class BRM_027p:
    """DIE, INSECT!"""

    activate = Hit(RANDOM_ENEMY_CHARACTER, 8)


class BRM_027pH:
    """DIE, INSECTS!"""

    activate = Hit(RANDOM_ENEMY_CHARACTER, 8) * 2


class BRM_028:
    """Emperor Thaurissan / 索瑞森大帝
    在你的回合结束时，你所有手牌的法力值消耗减少（1）点。"""

    events = OWN_TURN_END.on(Buff(FRIENDLY_HAND, "BRM_028e"))


class BRM_028e:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -1}


class BRM_029:
    """Rend Blackhand / 雷德·黑手
    战吼：如果你的手牌中有龙牌，则消灭一个传说随从。"""

    requirements = {
        PlayReq.REQ_LEGENDARY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_DRAGON_IN_HAND: 0,
    }
    powered_up = HOLDING_DRAGON, Find(ENEMY_MINIONS + LEGENDARY)
    play = HOLDING_DRAGON & Destroy(TARGET)


class BRM_030:
    """Nefarian / 奈法利安
    战吼：随机将两张（你对手职业的）法术牌置入你的手牌。"""

    play = Find(ENEMY_HERO - NEUTRAL) & (
        Give(CONTROLLER, RandomSpell(card_class=ENEMY_CLASS)) * 2
    ) | (Give(CONTROLLER, "BRM_030t") * 2)


class BRM_030t:
    """Tail Swipe"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 4)


class BRM_031:
    """Chromaggus / 克洛玛古斯
    每当你抽一张牌时，将该牌的另一张复制置入你的手牌。"""

    events = Draw(CONTROLLER).on(Give(CONTROLLER, Copy(Draw.CARD)))


class BRM_033:
    """Blackwing Technician / 黑翼技师
    战吼：如果你的手牌中有龙牌，便获得+1/+1。"""

    powered_up = HOLDING_DRAGON
    play = powered_up & Buff(SELF, "BRM_033e")


BRM_033e = buff(+1, +1)


class BRM_034:
    """Blackwing Corruptor / 黑翼腐蚀者
    战吼：如果你的手牌中有龙牌，则造成5点伤害。"""

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE_AND_DRAGON_IN_HAND: 0}
    powered_up = HOLDING_DRAGON
    play = powered_up & Hit(TARGET, 5)


##
# Spells


class BRM_001:
    """Solemn Vigil / 严正警戒
    抽两张牌。在本回合中每有一个随从死亡，本牌的法力值消耗便减少（1）点。"""

    play = Draw(CONTROLLER) * 2
    cost_mod = -Attr(GAME, GameTag.NUM_MINIONS_KILLED_THIS_TURN)


class BRM_001e:
    """Melt (Unused)"""

    atk = SET(0)


class BRM_003:
    """Dragon's Breath / 龙息术
    造成$4点伤害。在本回合中每有一个随从死亡，本牌的法力值消耗便减少（1）点。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 4)
    cost_mod = -Attr(GAME, GameTag.NUM_MINIONS_KILLED_THIS_TURN)


# Dragon's Might (Unused)
class BRM_003e:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -3}


class BRM_005:
    """Demonwrath / 恶魔之怒
    对所有非恶魔随从造成$2点 伤害。"""

    play = Hit(ALL_MINIONS - DEMON, 2)


class BRM_007:
    """Gang Up / 夜幕奇袭
    选择一个随从。将该随从的三张复制洗入你的牌库。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Shuffle(CONTROLLER, Copy(TARGET)) * 3


class BRM_011:
    """Lava Shock / 熔岩震击
    造成$2点伤害。 将你所有过载的法力水晶解锁。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 2), UnlockOverload(CONTROLLER)


class BRM_011t:
    """Lava Shock (Unused)"""

    tags = {enums.CANT_OVERLOAD: True}


class BRM_013:
    """Quick Shot / 快速射击
    造成$3点伤害。 如果你没有其他手牌，则抽一张牌。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    powered_up = Count(FRIENDLY_HAND - SELF) == 0
    play = Hit(TARGET, 3), EMPTY_HAND & Draw(CONTROLLER)


class BRM_015:
    """Revenge / 复仇打击
    对所有随从造成$1点伤害。如果你的生命值小于或等于12点，则改为造成$3点伤害。"""

    powered_up = CURRENT_HEALTH(FRIENDLY_HERO) <= 12
    play = powered_up & Hit(ALL_MINIONS, 3) | Hit(ALL_MINIONS, 1)


class BRM_017:
    """Resurrect / 复活术
    随机召唤一个在本局对战中死亡的友方随从。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_MINION_DIED_THIS_GAME: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION)))
