from ..utils import *


##
# Minions


class KAR_005:
    """Kindly Grandmother / 慈祥的外婆
    亡语：召唤一只3/2的大灰狼。"""

    deathrattle = Summon(CONTROLLER, "KAR_005a")


class KAR_006:
    """Cloaked Huntress / 神秘女猎手
    你的奥秘牌法力值消耗为（0）点。"""

    update = Refresh(FRIENDLY_HAND + SECRET, {GameTag.COST: SET(0)})


class KAR_009:
    """Babbling Book / 呓语魔典
    战吼：随机将一张法师法术牌置入你的 手牌。"""

    play = Give(CONTROLLER, RandomSpell())


class KAR_010:
    """Nightbane Templar / 夜魇骑士
    战吼：如果你的手牌中有龙牌，便召唤两条1/1的雏龙。"""

    powered_up = HOLDING_DRAGON
    play = powered_up & (SummonBothSides(CONTROLLER, "KAR_010a") * 2)


class KAR_021:
    """Wicked Witchdoctor / 邪恶的巫医
    每当你施放一个法术，随机召唤一个基础图腾。"""

    events = OWN_SPELL_PLAY.on(Summon(CONTROLLER, RandomBasicTotem()))


class KAR_029:
    """Runic Egg / 符文蛋
    亡语：抽一张牌。"""

    deathrattle = Draw(CONTROLLER)


class KAR_030a:
    """Pantry Spider"""

    play = Summon(CONTROLLER, "KAR_030")


class KAR_033:
    """Book Wyrm / 书卷之龙
    战吼：如果你的手牌中有龙牌，则消灭一个攻击力小于或等于3的敌方随从。"""

    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NONSELF_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_DRAGON_IN_HAND: 0,
        PlayReq.REQ_TARGET_MAX_ATTACK: 3,
    }
    powered_up = HOLDING_DRAGON, Find(ENEMY_MINIONS + (ATK <= 3))
    play = HOLDING_DRAGON & Destroy(TARGET)


class KAR_035:
    """Priest of the Feast / 宴会牧师
    每当你施放一个法术，为你的英雄恢复#3点生命值。"""

    events = OWN_SPELL_PLAY.on(Heal(FRIENDLY_HERO, 3))


class KAR_036:
    """Arcane Anomaly / 奥术畸体
    在你施放一个法术后，使本随从获得+1生命值。"""

    events = OWN_SPELL_PLAY.on(Buff(SELF, "KAR_036e"))


class KAR_036e:
    """+1生命值"""
    tags = {
        GameTag.HEALTH: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class KAR_037:
    """Avian Watcher / 鸟禽守护者
    战吼：如果你控制一个奥秘，便获得+1/+1和嘲讽。"""

    powered_up = Find(FRIENDLY_SECRETS)
    play = powered_up & Buff(SELF, "KAR_037t")


class KAR_037t:
    """+1/+1和嘲讽"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.TAUNT: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class KAR_041:
    """Moat Lurker / 沟渠潜伏者
    战吼：消灭一个随从。亡语：再次召唤被消灭的随从。"""

    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(TARGET)
    deathrattle = HAS_TARGET & Summon(TARGET_PLAYER, Copy(TARGET))


class KAR_044:
    """Moroes / 莫罗斯
    潜行 在你的回合结束时，召唤一个1/1的 家仆。"""

    events = OWN_TURN_END.on(Summon(CONTROLLER, "KAR_044a"))


class KAR_057:
    """Ivory Knight / 象牙骑士
    战吼：发现一张法术牌。为你的英雄恢复等同于其法力值消耗的生命值。"""

    play = Discover(CONTROLLER, RandomSpell()).then(
        Give(CONTROLLER, Discover.CARD), Heal(FRIENDLY_HERO, COST(Discover.CARD))
    )


class KAR_061:
    """The Curator / 馆长
    嘲讽，战吼：从你的牌库中抽一张野兽牌、龙牌和鱼人牌。"""

    play = (
        ForceDraw(RANDOM(FRIENDLY_DECK + MINION + MURLOC)),
        ForceDraw(RANDOM(FRIENDLY_DECK + DRAGON)),
        ForceDraw(RANDOM(FRIENDLY_DECK + BEAST)),
    )


class KAR_062:
    """Netherspite Historian / 虚空幽龙史学家
    战吼：如果你的手牌中有龙牌，便发现一张龙牌。"""

    powered_up = HOLDING_DRAGON
    play = powered_up & DISCOVER(RandomDragon())


class KAR_065:
    """Menagerie Warden / 展览馆守卫
    战吼：选择一个友方野兽，召唤一个它的复制。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 20,
    }
    powered_up = Find(FRIENDLY_MINIONS + BEAST)
    play = Summon(CONTROLLER, ExactCopy(TARGET))


class KAR_069:
    """Swashburglar / 吹嘘海盗
    战吼：随机将一张另一职业的卡牌置入你的手牌。"""

    play = Give(CONTROLLER, RandomCollectible(card_class=ENEMY_CLASS))


class KAR_070:
    """Ethereal Peddler / 虚灵商人
    战吼：如果你的手牌中有另一职业的卡牌，则其法力值消耗减少（2）点。"""

    play = Buff(FRIENDLY_HAND + OTHER_CLASS_CHARACTER, "KAR_070e")


@custom_card
class KAR_070e:
    tags = {
        GameTag.CARDNAME: "Ethereal Peddler Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.COST: -2,
    }
    events = REMOVED_IN_PLAY


class KAR_089:
    """Malchezaar's Imp / 玛克扎尔的小鬼
    每当你弃掉一张牌时，抽一张牌。"""

    events = Discard(CONTROLLER).on(Draw(CONTROLLER))


class KAR_092:
    """Medivh's Valet / 麦迪文的男仆
    战吼： 如果你控制一个奥秘，则造成3点伤害。"""

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_FRIENDLY_SECRETS: 1}
    powered_up = Find(FRIENDLY_SECRETS)
    play = powered_up & Hit(TARGET, 3)


class KAR_094:
    """Deadly Fork / 致命餐叉
    亡语：将一张3/2的武器牌置入你的手牌。"""

    deathrattle = Give(CONTROLLER, "KAR_094a")


class KAR_095:
    """Zoobot / 机械动物管理员
    战吼：随机使一个友方野兽，龙和鱼人获得+1/+1。"""

    powered_up = Find(
        RANDOM(FRIENDLY_MINIONS + MURLOC)
        | RANDOM(FRIENDLY_MINIONS + DRAGON)
        | RANDOM(FRIENDLY_MINIONS + BEAST)
    )
    play = (
        Buff(RANDOM(FRIENDLY_MINIONS + MURLOC), "KAR_095e"),
        Buff(RANDOM(FRIENDLY_MINIONS + DRAGON), "KAR_095e"),
        Buff(RANDOM(FRIENDLY_MINIONS + BEAST), "KAR_095e"),
    )


KAR_095e = buff(+1, +1)


class KAR_096:
    """Prince Malchezaar / 玛克扎尔王子
    对战开始时：额外将五张传说随从牌置入你的牌库。"""

    class Deck:
        events = GameStart().on(
            Shuffle(
                CONTROLLER, RandomLegendaryMinion(exclude=DeDuplicate(STARTING_DECK))
            )
            * 5
        )

    class Hand:
        events = GameStart().on(
            Shuffle(
                CONTROLLER, RandomLegendaryMinion(exclude=DeDuplicate(STARTING_DECK))
            )
            * 5
        )


class KAR_097:
    """Medivh, the Guardian / 守护者麦迪文
    战吼： 装备埃提耶什，守护者的传说之杖。"""

    play = Summon(CONTROLLER, "KAR_097t")


class KAR_097t:
    events = OWN_SPELL_PLAY.on(
        Summon(CONTROLLER, RandomMinion(cost=Attr(Play.CARD, GameTag.COST))),
        Hit(SELF, 1),
    )


class KAR_114:
    """Barnes / 巴内斯
    战吼：随机挑选你牌库里的一个随从，召唤一个1/1的复制。"""

    play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY_DECK + MINION))).then(
        Buff(Summon.CARD, "KAR_114e")
    )


class KAR_114e:
    atk = SET(1)
    max_health = SET(1)


class KAR_204:
    """Onyx Bishop / 玛瑙主教
    战吼：随机召唤一个在本局对战中死亡的友方随从。"""

    play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION)))


class KAR_205:
    """Silverware Golem / 镀银魔像
    如果你弃掉了这张随从牌，则会召唤它。"""

    discard = Summon(CONTROLLER, Copy(SELF))


class KAR_702:
    """Menagerie Magician / 展览馆法师
    战吼：随机使一个友方野兽，龙和鱼人获得+2/+2。"""

    powered_up = Find(
        RANDOM(FRIENDLY_MINIONS + MURLOC)
        | RANDOM(FRIENDLY_MINIONS + DRAGON)
        | RANDOM(FRIENDLY_MINIONS + BEAST)
    )
    play = (
        Buff(RANDOM(FRIENDLY_MINIONS + MURLOC), "KAR_702e"),
        Buff(RANDOM(FRIENDLY_MINIONS + DRAGON), "KAR_702e"),
        Buff(RANDOM(FRIENDLY_MINIONS + BEAST), "KAR_702e"),
    )


KAR_702e = buff(+2, +2)


class KAR_710:
    """Arcanosmith / 奥能铁匠
    战吼：召唤一个0/5并具有嘲讽的随从。"""

    play = Summon(CONTROLLER, "KAR_710m")


class KAR_711:
    """Arcane Giant / 奥术巨人
    在本局对战中，你每施放一个法术，本牌的法力值消耗便减少（1）点。"""

    cost_mod = -TIMES_SPELL_PLAYED_THIS_GAME


class KAR_712:
    """Violet Illusionist / 紫罗兰幻术师
    在你的回合中，你的英雄免疫。"""

    update = Find(CURRENT_PLAYER + CONTROLLER) & Refresh(
        FRIENDLY_HERO, {GameTag.IMMUNE: True}
    )


##
# Spells


class KAR_004:
    """Cat Trick / 豹子戏法
    奥秘：在你的对手施放一个法术后，召唤一只4/2并具有潜行的猎豹。"""

    secret = Play(ENEMY, SPELL).after(Summon(CONTROLLER, "KAR_004a"))


class KAR_013:
    """Purify / 净化
    沉默一个友方随从，抽一张牌。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Silence(TARGET), Draw(CONTROLLER)


class KAR_025:
    """Kara Kazham! / 附灵术
    召唤一个1/1的蜡烛，2/2的扫帚和3/3的茶壶。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = (
        Summon(CONTROLLER, "KAR_025a"),
        Summon(CONTROLLER, "KAR_025b"),
        Summon(CONTROLLER, "KAR_025c"),
    )


class KAR_026:
    """Protect the King! / 保卫国王
    战场上每有一个敌方随从，便召唤一个1/1并具有嘲讽的 禁卫。"""

    requirements = {
        PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "KAR_026t") * Count(ENEMY_MINIONS)


class KAR_073:
    """Maelstrom Portal / 大漩涡传送门
    对所有敌方随从造成$1点伤害。随机召唤一个法力值消耗为（1）的随从。"""

    play = Hit(ENEMY_MINIONS, 1), Summon(CONTROLLER, RandomMinion(cost=1))


class KAR_075:
    """Moonglade Portal / 月光林地传送门
    恢复#6点生命值。随机召唤一个法力值消耗为（6）的 随从。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Heal(TARGET, 6), Summon(CONTROLLER, RandomMinion(cost=6))


class KAR_076:
    """Firelands Portal / 火焰之地传送门
    造成$6点伤害。随机召唤一个法力值消耗为（6）的随从。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    def play(self):
        yield Hit(TARGET, 6)
        # 检查游戏是否已结束（目标可能是英雄并被击杀）
        if not self.game.ended:
            yield Summon(CONTROLLER, RandomMinion(cost=6))


class KAR_077:
    """Silvermoon Portal / 银月城传送门
    使一个随从获得+2/+2。随机召唤一个法力值消耗为（2）的随从。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "KAR_077e"), Summon(CONTROLLER, RandomMinion(cost=2))


KAR_077e = buff(+2, +2)


class KAR_091:
    """Ironforge Portal / 铁炉堡传送门
    获得4点护甲值。随机召唤一个法力值消耗为（4）的 随从。"""

    play = GainArmor(FRIENDLY_HERO, 4), Summon(CONTROLLER, RandomMinion(cost=4))


##
# Weapons


class KAR_028:
    """Fool's Bane / 愚者之灾
    每个回合攻击次数不限，但无法攻击英雄。"""

    update = Refresh(
        FRIENDLY_HERO,
        {
            GameTag.CANNOT_ATTACK_HEROES: True,
            enums.UNLIMITED_ATTACKS: True,
        },
    )


class KAR_063:
    """Spirit Claws / 幽灵之爪
    当你拥有法术伤害时，拥有 +2攻击力。"""

    update = Find(FRIENDLY_MINIONS + SPELLPOWER) & Refresh(SELF, {GameTag.ATK: +2})
