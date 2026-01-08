from ..utils import *


##
# Minions


class CFM_321:
    """Grimestreet Informant / 污手街情报员
    战吼：发现一张 猎人、圣骑士或战士卡牌。"""

    play = GenericChoice(
        CONTROLLER,
        [
            RandomCollectible(card_class=CardClass.HUNTER),
            RandomCollectible(card_class=CardClass.PALADIN),
            RandomCollectible(card_class=CardClass.WARRIOR),
        ],
    )


class CFM_325:
    """Small-Time Buccaneer / 蹩脚海盗
    如果你装备着武器，本随从拥有 +2攻击力。"""

    update = Find(FRIENDLY_WEAPON) & Refresh(SELF, buff="CFM_325e")


CFM_325e = buff(atk=2)


class CFM_649:
    """Kabal Courier / 暗金教信使
    战吼： 发现一张法师、牧师或术士卡牌。"""

    play = GenericChoice(
        CONTROLLER,
        [
            RandomCollectible(card_class=CardClass.MAGE),
            RandomCollectible(card_class=CardClass.PRIEST),
            RandomCollectible(card_class=CardClass.WARLOCK),
        ],
    )


class CFM_652:
    """Second-Rate Bruiser / 二流打手
    嘲讽 如果你的对手控制至少三个随从，则其法力值消耗减少（2）点。"""

    class Hand:
        update = (Count(ENEMY_MINIONS) >= 3) & Refresh(SELF, {GameTag.COST: -2})


class CFM_658:
    """Backroom Bouncer / 后院保镖
    每当一个友方随从死亡，便获得+1 攻击力。"""

    events = Death(FRIENDLY + MINION).on(Buff(SELF, "CFM_658e"))


CFM_658e = buff(atk=1)


class CFM_667:
    """Bomb Squad / 爆破小队
    战吼：对一个敌方随从造成5点伤害。 亡语：对你的英雄造成5点伤害。"""

    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Hit(TARGET, 5)
    deathrattle = Hit(FRIENDLY_HERO, 5)


class CFM_668:
    """Doppelgangster / 魅影歹徒
    战吼：召唤本随从的两个复制。"""

    # 实现说明：
    # 官方游戏数据中存在3个不同的 Doppelgangster 卡牌ID：
    #   - CFM_668 (原版): "Get 'em, boys." / "All for one!"
    #   - CFM_668t (复制1): "Seeing triple?" / "Such a shame."
    #   - CFM_668t2 (复制2): "Seeing triple?" / "A pity."
    # 这3个版本的唯一区别是语音台词（打出/攻击时的语音），其他属性完全相同。
    # 语音台词属于表现层细节，不影响游戏逻辑，fireplace 引擎不处理音效。
    # 当前使用 ExactCopy(SELF) 的实现完全正确：
    #   - 正确复制所有游戏属性（攻击、生命、费用、种族等）
    #   - 正确继承所有增益效果（手牌Buff等）
    #   - 正确继承亡语和其他机制
    # 符合官方游戏行为，无需为语音差异创建额外的卡牌定义。
    play = SummonBothSides(CONTROLLER, ExactCopy(SELF)) * 2


class CFM_688:
    """Spiked Hogrider / 野猪骑士斯派克
    战吼：如果有敌方随从拥有嘲讽，便获得冲锋。"""

    powered_up = Find(ENEMY_MINIONS + TAUNT)
    play = powered_up & GiveCharge(SELF)


class CFM_852:
    """Lotus Agents / 玉莲帮密探
    战吼：发现一张德鲁伊、潜行者或萨满祭司卡牌。"""

    play = GenericChoice(
        CONTROLLER,
        [
            RandomCollectible(card_class=CardClass.DRUID),
            RandomCollectible(card_class=CardClass.ROGUE),
            RandomCollectible(card_class=CardClass.SHAMAN),
        ],
    )
