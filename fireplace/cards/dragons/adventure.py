from ..utils import *


##
# Druid


class YOD_040:
    """Steel Beetle / 钢铁甲虫
    战吼：如果你的手牌中有法力值消耗大于或等于（5）点的法术牌，便获得5点护甲值。"""

    # <b>Battlecry:</b> If you're holding a spell that costs (5) or more, gain 5 Armor.
    powered_up = Find(FRIENDLY_HAND + SPELL + (COST >= 5))
    play = powered_up & GainArmor(FRIENDLY_HERO, 5)


class YOD_001:
    """Rising Winds / 乘风而起
    双生法术 抉择：抽一张牌；或者召唤一只3/2的鹰。"""

    # <b>Twinspell</b> <b>Choose One -</b> Draw a card; or Summon a 3/2_Eagle.
    choose = ("YOD_001b", "YOD_001c")
    play = ChooseBoth(CONTROLLER) & (Draw(CONTROLLER), Summon(CONTROLLER, "YOD_001t"))


class YOD_001b:
    play = Draw(CONTROLLER)


class YOD_001c:
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "YOD_001t")


class YOD_001ts(YOD_001):
    pass


##
# Hunter


class YOD_004:
    """Chopshop Copter / 拆件旋翼机
    在一个友方机械死亡后，随机将一张机械牌置入你的手牌。"""

    # After a friendly Mech dies, add a random Mech to your hand.
    events = Death(FRIENDLY + MECH).after(Give(CONTROLLER, RandomMech()))


class YOD_036:
    """Rotnest Drake / 腐巢幼龙
    战吼：如果你的手牌中有龙牌，随机消灭一个敌方随从。"""

    # [x]<b>Battlecry:</b> If you're holding a Dragon, destroy a random enemy minion.
    powered_up = HOLDING_DRAGON
    play = powered_up & Destroy(RANDOM_ENEMY_MINION)


class YOD_005:
    """Fresh Scent / 新鲜气息
    双生法术 使一个野兽获得+2/+2。"""

    # <b>Twinspell</b> Give a Beast +2/+2.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.BEAST,
    }
    play = Buff(TARGET, "YOD_005e")


class YOD_005ts(YOD_005):
    pass


YOD_005e = buff(+2, +2)


##
# Mage


class YOD_007:
    """Animated Avalanche / 活化雪崩
    战吼：如果你在上个回合使用过元素牌，召唤一个本随从的 复制。"""

    # [x]<b>Battlecry:</b> If you played an Elemental last turn, summon a copy of this.
    powered_up = ELEMENTAL_PLAYED_LAST_TURN
    play = powered_up & Summon(CONTROLLER, ExactCopy(SELF))


class YOD_009:
    """The Amazing Reno / 神奇的雷诺
    战吼：使所有随从消失。*咻！*"""

    # <b>Battlecry:</b> Make all minions disappear. <i>*Poof!*</i>
    play = Remove(ALL_MINIONS)


class YOD_009h:
    """What Does This Do?"""

    # [x]<b>Passive Hero Power</b> At the start of your turn, cast a random spell.
    tags = {enums.PASSIVE_HERO_POWER: True}
    events = OWN_TURN_BEGIN.on(CastSpell(RandomSpell()))


##
# Paladin


class YOD_043:
    """Scalelord / 鳞甲领主
    战吼：使你的所有鱼人获得圣盾。"""

    # <b>Battlecry:</b> Give your Murlocs <b>Divine Shield</b>.
    play = GiveDivineShield(FRIENDLY_MINIONS + MURLOC)


class YOD_012:
    """Air Raid / 空中团战
    双生法术 召唤两个1/1并具有嘲讽的白银之手新兵。"""

    # <b>Twinspell</b> Summon two 1/1 Silver_Hand Recruits with <b>Taunt</b>.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "CS2_101t").then(Taunt(Summon.CARD)) * 2


class YOD_012ts(YOD_012):
    pass


##
# Priest


class YOD_013:
    """Cleric of Scales / 龙鳞祭司
    战吼：如果你的手牌中有龙牌，便发现你牌库中的一张法术牌。"""

    # <b>Battlecry:</b> If you're holding a Dragon, <b>Discover</b> a spell from your deck.
    powered_up = HOLDING_DRAGON
    play = powered_up & Choice(
        CONTROLLER, RANDOM(DeDuplicate(FRIENDLY_DECK + SPELL)) * 3
    ).then(ForceDraw(Choice.CARD))


class YOD_014:
    """Aeon Reaver / 永世掠夺者
    战吼：对一个随从造成等同于其攻击力的伤害。"""

    # <b>Battlecry:</b> Deal damage to_a minion equal to its_Attack.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, ATK(SELF))


class YOD_015:
    """Dark Prophecy / 黑暗预兆
    发现一张法力值消耗为（2）的随从牌。召唤该随从并使其获得+3生命值。"""

    # <b>Discover</b> a 2-Cost minion. Summon it and give it +3 Health.
    play = Discover(CONTROLLER, RandomMinion(cost=2)).then(
        Summon(CONTROLLER, Discover.CARD).then(Buff(Summon.CARD, "YOD_015e"))
    )


YOD_015e = buff(health=3)


##
# Rogue


class YOD_016:
    """Skyvateer / 空中私掠者
    潜行 亡语：抽一张牌。"""

    # <b>Stealth</b> <b>Deathrattle:</b> Draw a card.
    deathrattle = Draw(CONTROLLER)


class YOD_017:
    """Shadow Sculptor / 暗影塑形师
    连击：在本回合中，你每使用一张其他牌，便抽一张牌。"""

    # <b>Combo:</b> Draw a card for each card you've played this turn.
    combo = Draw(CONTROLLER) * NUM_CARDS_PLAYED_THIS_TURN


class YOD_018:
    """Waxmancy / 蜡烛学
    发现一张战吼随从牌。其法力值消耗减少（2）点。"""

    # <b>Discover</b> a <b>Battlecry</b> minion. Reduce its Cost by (2).
    play = Discover(CONTROLLER, RandomMinion(battlecry=True)).then(
        Give(CONTROLLER, Discover.CARD).then(Buff(Give.CARD, "YOD_018e"))
    )


class YOD_018e:
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY


##
# Shaman


class YOD_020:
    """Explosive Evolution / 惊爆异变
    将一个随从随机变形成为一个法力值消耗增加（3）点的 随从。"""

    # Transform a minion into a random one that costs (3) more.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Evolve(TARGET, 3)


class YOD_041:
    """Eye of the Storm / 风暴之眼
    召唤三个5/6并具有嘲讽的元素。 过载：（3）"""

    # Summon three 5/6 Elementals with <b>Taunt</b>. <b>Overload:</b> (3)
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "YOD_041t") * 3


class YOD_042:
    """The Fist of Ra-den / 莱登之拳
    在你施放一个法术后，召唤一个法力值消耗相同的传说随从。失去1点耐久度。"""

    # [x]After you cast a spell, summon a <b>Legendary</b> minion of that Cost. Lose 1
    # Durability.
    events = OWN_SPELL_PLAY.after(
        (COST(Play.CARD) > 0)
        & (
            Summon(CONTROLLER, RandomLegendaryMinion(cost=COST(Play.CARD))),
            Hit(SELF, 1),
        )
    )


##
# Warlock


class YOD_026:
    """Fiendish Servant / 邪魔仆从
    亡语：随机使一个友方随从获得本随从的攻击力。"""

    # [x]<b>Deathrattle:</b> Give this minion's Attack to a random friendly minion.
    deathrattle = Buff(RANDOM_OTHER_FRIENDLY_MINION, "YOD_026e", atk=ATK(SELF))


@custom_card
class YOD_026e:
    tags = {
        GameTag.CARDNAME: "Fiendish Servant Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class YOD_027:
    """Chaos Gazer / 混乱凝视者
    战吼：诅咒你对手的一张可用手牌。对手将有一个回合的机会来使用那张牌！"""

    # [x]<b>Battlecry:</b> Corrupt a playable card in your opponent's hand. They have 1
    # turn to play it!
    play = Buff(RANDOM(ENEMY_HAND + (COST <= (MANA(OPPONENT) + 1))), "YOD_027e")


class YOD_027e:
    events = REMOVED_IN_PLAY

    class Hand:
        events = OWN_TURN_END.on(Destroy(OWNER))


class YOD_025:
    """Twisted Knowledge / 扭曲学识
    发现两张术士牌。"""

    # <b>Discover</b> 2 Warlock cards.
    play = DISCOVER(RandomCollectible(card_class=CardClass.WARLOCK)) * 2


##
# Warrior


class YOD_022:
    """Risky Skipper / 冒进的艇长
    在你使用一张随从牌后，对所有随从造成1点伤害。"""

    # After you play a minion, deal 1 damage to all_minions.
    events = Play(CONTROLLER, MINION).after(Hit(ALL_MINIONS, 1))


class YOD_024:
    """Bomb Wrangler / 炸弹牛仔
    每当本随从受到伤害，召唤一个1/1的砰砰机器人。"""

    # Whenever this minion takes damage, summon a_1/1 Boom Bot.
    events = Damage(SELF).on(Summon(CONTROLLER, "GVG_110t"))


class YOD_023:
    """Boom Squad / 砰砰战队
    发现一张跟班牌，机械牌或 龙牌。"""

    # <b>Discover</b> a <b>Lackey</b>, Mech, or Dragon.
    play = GenericChoice(CONTROLLER, [RandomLackey(), RandomMech(), RandomDragon()])


##
# Neutral


class YOD_028:
    """Skydiving Instructor / 伞降教官
    战吼：从你的牌库中召唤一个法力值消耗为（1）的随从。"""

    # [x]<b>Battlecry:</b> Summon a 1-Cost minion from your deck.
    play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + (COST == 1)))


class YOD_029:
    """Hailbringer / 冰雹使者
    战吼：召唤两个1/1的可以冻结攻击目标的寒冰碎片。"""

    # [x]<b>Battlecry:</b> Summon two 1/1 Ice Shards that <b>Freeze</b>.
    play = Summon(CONTROLLER, "YOD_029t") * 2


class YOD_029t:
    events = Damage(CHARACTER, None, SELF).on(Freeze(Damage.TARGET))


class YOD_030:
    """Licensed Adventurer / 资深探险者
    战吼：如果你控制一个任务，则将一张幸运币置入你的手牌。"""

    # [x]<b>Battlecry:</b> If you control a <b>Quest</b>, add a Coin to your hand.
    play = (Find(FRIENDLY_QUEST), Give(CONTROLLER, THE_COIN))


class YOD_032:
    """Frenzied Felwing / 狂暴邪翼蝠
    在本回合中，你的对手每受到1点伤害，本牌的法力值消耗便减少（1）点。"""

    # Costs (1) less for each damage dealt to your opponent this turn.
    cost_mod = -DAMAGED_THIS_TURN(ENEMY_HERO)


class YOD_006:
    """Escaped Manasaber / 奔逃的魔刃豹
    潜行 每当本随从攻击，便获得一个仅限本回合可用的法力水晶。"""

    # [x]<b>Stealth</b> Whenever this attacks, gain 1 Mana Crystal this turn only.
    events = Attack(SELF).on(ManaThisTurn(CONTROLLER, 1))


class YOD_033:
    """Boompistol Bully / 持枪恶霸
    战吼：下个回合敌方战吼牌的法力值消耗增加（5）点。"""

    # <b>Battlecry:</b> Enemy <b>Battlecry</b>_cards cost (5)_more next turn.
    play = Buff(OPPONENT, "YOD_033e")


class YOD_033e:
    update = CurrentPlayer(OWNER) & Refresh(ENEMY_HAND + BATTLECRY, {GameTag.COST: +5})
    events = OWN_TURN_BEGIN.on(Destroy(SELF))


class YOD_035:
    """Grand Lackey Erkh / 高级跟班厄尔克
    在你使用一张跟班牌后，将一张跟班牌置入你的手牌。"""

    # After you play a <b>Lackey</b>, add a <b>Lackey</b> to your hand.
    events = Play(CONTROLLER, LACKEY).after(Give(CONTROLLER, RandomLackey()))


class YOD_038:
    """Sky Gen'ral Kragg / 天空上将库拉格
    嘲讽，战吼：如果你在本局对战中使用过任务，则召唤一只4/2并具有突袭的鹦鹉。"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> If you've played a <b>Quest</b> this game, summon a
    # 4/2 Parrot with <b>Rush</b>.
    powered_up = Find(CARDS_PLAYED_THIS_GAME + QUEST)
    play = powered_up & Summon(CONTROLLER, "YOD_038t")
