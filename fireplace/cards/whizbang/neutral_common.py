"""
威兹班的工坊 - 中立 - COMMON
"""
from ..utils import *


class MIS_308:
    """爆破工程师 - Explodineer
    [x]At the end of your turn, shuffle a Bomb into your opponent's deck. When drawn, it explodes for 5 damage.
    """
    # 3/2/4 在你的回合结束时，将一张"炸弹"牌洗入你对手的牌库。当抽到"炸弹"时，便会受到5点伤害
    # 炸弹卡牌 BOT_511t 已在 boomsday 扩展包中定义
    events = OWN_TURN_END.on(Shuffle(OPPONENT, "BOT_511t"))


class TOY_000:
    """焦油泥浆怪 - Tar Slime
    Taunt Has +2 Attack during your opponent's turn.
    """
    # 1/0/3 元素 嘲讽。在你对手的回合拥有+2攻击力
    taunt = True

    # 在对手回合时获得+2攻击力
    class OppTurn:
        update = Refresh(SELF, {GameTag.ATK: +2})


class TOY_006:
    """甲虫钥匙链 - Scarab Keychain
    Battlecry: Discover a 2-Cost card.
    """
    # 1/1/1 野兽 战吼：发现一张法力值消耗为（2）的卡牌
    def play(self):
        yield DISCOVER(RandomCollectible(cost=2))


class TOY_054:
    """卡牌评级师 - Card Grader
    Battlecry: If you've cast a spell while holding this, Discover a card from your deck.
    """
    # 3/2/4 鱼人 战吼：如果你在本牌在你手中时施放过法术，从你的牌库中发现一张牌
    # 需要追踪在手牌中时是否施放过法术
    powered_up = boolean_property("TOY_054_powered_up")

    class Hand:
        # 在手牌中时，监听施放法术事件
        events = Play(CONTROLLER, SPELL).after(SetAttr(SELF, "powered_up", True))

    def play(self):
        if self.powered_up:
            # 从牌库中发现一张牌
            yield DISCOVER(FRIENDLY_DECK)


class TOY_307:
    """甜蜜雪灵 - Sweetened Snowflurry
    [x]Miniaturize Battlecry: Get 2 random Temporary Frost spells.
    """
    # 3/3/3 元素 微缩。战吼：随机获取2张临时冰霜法术牌
    # Miniaturize 机制由核心 Play action 自动处理
    def play(self):
        # 获取2张随机冰霜法术
        for _ in range(2):
            card = yield Give(CONTROLLER, RandomSpell(spell_school=SpellSchool.FROST))
            # 给予临时标签（回合结束时弃掉）
            if card:
                yield Buff(card, "TOY_307e")


class TOY_307e:
    """融化 - Melting"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    # 在回合结束时弃掉这张牌
    events = OWN_TURN_END.on(Discard(OWNER))


class TOY_340:
    """恋旧的新生 - Nostalgic Initiate
    Miniaturize The first time you cast a spell, gain +2/+2.
    """
    # 3/2/3 微缩。在你施放本随从登场后的第一个法术时获得+2/+2
    # Miniaturize 机制由核心 Play action 自动处理
    # 需要追踪是否已经触发过
    triggered = boolean_property("TOY_340_triggered")

    events = Play(CONTROLLER, SPELL).after(
        Find(SELF + ~TRIGGERED) & (Buff(SELF, "TOY_340t"), SetAttr(SELF, "triggered", True))
    )


class TOY_340t:
    """+2/+2 Buff"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_386:
    """礼盒雏龙 - Giftwrapped Whelp
    Battlecry: If you're holding a Dragon, give it and this minion +1/+1.
    """
    # 1/2/1 龙 战吼：如果你的手牌中有龙牌，使该龙牌和本随从获得+1/+1
    def play(self):
        # 检查手牌中是否有龙牌
        dragons = FRIENDLY_HAND + DRAGON
        if dragons:
            # 随机选择一张龙牌
            dragon = yield RandomTarget(dragons)
            if dragon:
                # 给龙牌和本随从+1/+1
                yield Buff(dragon, "TOY_386e")
                yield Buff(SELF, "TOY_386e")


class TOY_386e:
    """+1/+1 Buff"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_390:
    """清仓销售员 - Clearance Promoter
    Deathrattle: Reduce the Cost of two spells in your hand by (1).
    """
    # 3/3/2 亡语：使你手牌中两张法术牌的法力值消耗减少（1）点
    def deathrattle(self):
        # 随机选择手牌中的两张法术牌
        spells = yield RandomTarget(FRIENDLY_HAND + SPELL, count=2)
        if spells:
            yield Buff(spells, "TOY_390e")


class TOY_390e:
    """费用减少 Buff"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    cost_mod = -1


class TOY_391:
    """漫画美术家 - Caricature Artist
    Battlecry: Draw a minion that costs (5) or more. Give it a funny mustache!
    """
    # 4/3/4 战吼：抽一张法力值消耗大于或等于（5）点的随从牌，给它画上滑稽的小胡子
    def play(self):
        # 抽一张费用>=5的随从牌
        cards = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION + (COST >= 5))
        if cards:
            # 给予 buff（纯视觉效果）
            yield Buff(cards, "TOY_391e")


class TOY_391e:
    """滑稽小胡子 Buff"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}


class TOY_517:
    """泼漆彩鳍鱼人 - Plucky Paintfin
    [x]Poisonous Battlecry: Draw a Rush minion.
    """
    # 3/2/3 鱼人 剧毒。战吼：抽一张突袭随从牌
    poisonous = True

    def play(self):
        # 抽一张具有突袭的随从牌
        yield ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION + RUSH)


class TOY_518:
    """宝藏经销商 - Treasure Distributor
    After you summon a Pirate, give it +1 Attack.
    """
    # 1/1/2 海盗 在你召唤一个海盗后，使其获得+1攻击力
    events = Summon(CONTROLLER, PIRATE).after(Buff(Summon.CARD, "TOY_518e"))


class TOY_518e:
    """+1攻击力 Buff"""
    tags = {
        GameTag.ATK: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_528:
    """伴唱机 - Sing-Along Buddy
    Your Hero Power triggers twice.
    """
    # 3/2/4 机械 你的英雄技能会触发两次
    # 使用 HERO_POWER_DOUBLE 标签
    update = Refresh(FRIENDLY_HERO, {GameTag.HERO_POWER_DOUBLE: True})


class TOY_646:
    """捣蛋林精 - Messmaker
    Lifesteal, Taunt Deathrattle: Deal 1 damage to all enemies.
    """
    # 3/1/3 吸血。嘲讽。亡语：对所有敌人造成1点伤害
    lifesteal = True
    taunt = True
    deathrattle = Hit(ENEMY_CHARACTERS, 1)


class TOY_670:
    """欢乐的玩具匠 - Giggling Toymaker
    Deathrattle: Summon two 1/2 Mechs with Taunt and Divine Shield.
    """
    # 4/2/1 亡语：召唤两个1/2并具有嘲讽和圣盾的机械
    # 需要定义 Token 卡牌 TOY_670t
    deathrattle = Summon(CONTROLLER, "TOY_670t") * 2


class TOY_814:
    """玩具兵盒 - Bucket of Soldiers
    Deathrattle: Summon five 1/1 Soldiers with random Bonus Effects.
    """
    # 3/0/2 亡语：召唤五个1/1并具有随机额外效果的士兵
    # 有8种不同效果的士兵 Token：TOY_814t ~ TOY_814t8
    def deathrattle(self):
        # 召唤5个随机士兵
        soldiers = ["TOY_814t", "TOY_814t2", "TOY_814t3", "TOY_814t4",
                   "TOY_814t5", "TOY_814t6", "TOY_814t7", "TOY_814t8"]
        for _ in range(5):
            yield Summon(CONTROLLER, RandomID(*soldiers))


class TOY_820:
    """废弃电子玩偶 - Forgotten Animatronic
    At the end of your turn, destroy a minion with less Attack than this.
    """
    # 5/4/6 机械 在你的回合结束时，消灭一个攻击力低于本随从的随从
    events = OWN_TURN_END.on(
        Destroy(RANDOM(ALL_MINIONS - SELF + (ATK(ALL_MINIONS) < ATK(SELF))))
    )


class TOY_878:
    """扮装选手 - Cosplay Contestant
    After your opponent plays a minion, transform into a 3/4 copy of it.
    """
    # 3/3/4 德莱尼 在你的对手使用一张随从牌后，变形成为它的3/4的复制
    events = Play(OPPONENT, MINION).after(
        Morph(SELF, Copy(Play.CARD)),
        Buff(SELF, "TOY_878e")
    )


class TOY_878e:
    """炫酷装扮 - 属性值变为3/4"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    max_health = SET(3)
    atk = SET(3)


class TOY_891:
    """工坊保洁员 - Workshop Janitor
    Battlecry: If you control a location, draw 2 cards.
    """
    # 5/5/5 战吼：如果你控制着地标，抽两张牌
    def play(self):
        if FRIENDLY_LOCATIONS:
            yield Draw(CONTROLLER) * 2


class TOY_893:
    """套娃傀儡 - Nesting Golem
    Deathrattle: Resummon this with -1/-1.
    """
    # 4/4/3 亡灵 亡语：再次召唤本随从并具有-1/-1
    # 重要：-1/-1 是基于基础属性，不复制任何 buff
    def deathrattle(self):
        # 召唤一个干净的本随从复制（不带任何 buff），并给予-1/-1
        # 使用卡牌ID而不是 ExactCopy，确保不复制 buff
        minion = yield Summon(CONTROLLER, self.id)
        if minion:
            yield Buff(minion, "TOY_893e")


class TOY_893e:
    """-1/-1 Debuff"""
    tags = {
        GameTag.ATK: -1,
        GameTag.HEALTH: -1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_894:
    """折纸青蛙 - Origami Frog
    [x]Rush Battlecry: Swap Attack with another minion.
    """
    # 5/1/4 野兽 突袭。战吼：与另一个随从交换攻击力
    rush = True
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self):
        if TARGET:
            # 交换攻击力
            self_atk = self.atk
            target_atk = TARGET.atk
            yield Buff(SELF, "TOY_894e", atk=target_atk - self_atk)
            yield Buff(TARGET, "TOY_894e", atk=self_atk - target_atk)


class TOY_894e:
    """叠纸 - 属性值互换"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}


class TOY_943:
    """大作战狂热玩家 - Rumble Enthusiast
    [x]After you play the left- or right-most card in your hand, deal 1 damage to a random enemy.
    """
    # 3/2/5 在你使用最左或最右边的一张手牌后，随机对一个敌人造成1点伤害
    # 需要追踪打出的卡牌是否是最左或最右
    events = Play(CONTROLLER).after(
        Find(Play.CARD + LEFTMOST | Play.CARD + RIGHTMOST) & Hit(RANDOM_ENEMY_CHARACTER, 1)
    )


