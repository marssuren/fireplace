"""贫瘠之地的锤炼（Forged in the Barrens）卡牌实现"""
from ..utils import *


class BAR_305:
    """Flurry (Rank 1) - 冰风暴（等级1）
    Freeze a random enemy minion. (Upgrades when you have 5 Mana.)
    冻结一个随机敌方随从。（在你有5点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_305t",
        enums.RANKED_SPELL_THRESHOLD: 5,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Freeze(RANDOM_ENEMY_MINION)


class BAR_305t:
    """Flurry (Rank 2) - 冰风暴（等级2）
    Freeze 2 random enemy minions. (Upgrades when you have 10 Mana.)
    冻结两个随机敌方随从。（在你有10点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_305t2",
        enums.RANKED_SPELL_THRESHOLD: 10,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Freeze(RANDOM_ENEMY_MINION * 2)


class BAR_305t2:
    """Flurry (Rank 3) - 冰风暴（等级3）
    Freeze 3 random enemy minions.
    冻结三个随机敌方随从。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Freeze(RANDOM_ENEMY_MINION * 3)


class BAR_541:
    """Runed Orb - 符文宝珠
    Deal $2 damage. Discover a spell.
    造成$2点伤害。发现一张法术牌。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 2), DISCOVER(RandomSpell(card_class=CardClass.MAGE))


class BAR_542:
    """Refreshing Spring Water - 清凉的泉水
    Draw 2 cards. Refresh 2 Mana Crystals for each spell drawn.
    抽两张牌。每抽到一张法术牌，便刷新2点法力水晶。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    def play(self):
        # 抽第一张牌
        cards1 = yield Draw(CONTROLLER)
        if cards1 and any(c.type == CardType.SPELL for c in cards1 if c):
            yield FillMana(CONTROLLER, 2)
        
        # 抽第二张牌
        cards2 = yield Draw(CONTROLLER)
        if cards2 and any(c.type == CardType.SPELL for c in cards2 if c):
            yield FillMana(CONTROLLER, 2)


class BAR_544:
    """Reckless Apprentice - 鲁莽的学徒
    Battlecry: Fire your Hero Power at all enemies.
    战吼：对所有敌人使用你的英雄技能。
    """
    play = (
        Hit(ENEMY_CHARACTERS, HeroPower(CONTROLLER)),
    )


class BAR_545:
    """Arcane Luminary - 奥术发光体
    Cards that didn't start in your deck cost (2) less (but not less than 1).
    不是以你牌库起始卡牌的牌的法力值消耗减少（2）点（但不会少于1点）。
    """
    # 使用 FuncSelector 判断卡牌是否不是起始牌库中的卡牌
    # 检查 started_in_deck 属性或 creator 是否存在
    update = Refresh(
        FRIENDLY_HAND + FuncSelector(lambda entities, src: [
            e for e in entities if not getattr(e, 'started_in_deck', True)
        ]),
        {GameTag.COST: -2}
    )


class BAR_546:
    """Wildfire - 野火
    Your Hero Power deals 1 more damage this game.
    在本局对战中，你的英雄技能多造成1点伤害。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = AddProgress(FRIENDLY_HERO, FRIENDLY_HERO, 1, "hero_power_damage_bonus")


class BAR_547(ThresholdUtils):
    """Mordresh Fire Eye - 火眼莫德雷斯
    Battlecry: If you've dealt 10 damage with your Hero Power this game, deal 10 damage to all enemies.
    战吼：如果你在本局对战中用英雄技能造成过10点伤害，对所有敌人造成10点伤害。
    """
    play = ThresholdUtils.powered_up & Hit(ENEMY_CHARACTERS, 10)


class BAR_748:
    """Varden Dawngrasp - 瓦尔登·晨拥
    Battlecry: Freeze all enemy minions. If any are already Frozen, deal 4 damage to them instead.
    战吼：冻结所有敌方随从。如果有随从已经被冻结，则改为对其造成4点伤害。
    """
    play = (
        Find(ENEMY_MINIONS + FROZEN) & Hit(ENEMY_MINIONS + FROZEN, 4),
        Freeze(ENEMY_MINIONS - FROZEN),
    )


class BAR_812:
    """Oasis Ally - 绿洲盟军
    Secret: When a friendly minion is attacked, summon a 3/6 Water Elemental.
    奥秘：当一个友方随从受到攻击时，召唤一个3/6的水元素。
    """
    secret = Attack(FRIENDLY + MINION).on(
        Reveal(SELF),
        Summon(CONTROLLER, "BAR_812t"),
    )


class BAR_888:
    """Rimetongue - 霜舌半人马
    After you cast a Frost spell, summon a 1/1 Elemental that Freezes.
    在你施放一个冰霜法术后，召唤一个1/1会冻结的元素。
    """
    events = Play(CONTROLLER, SPELL + FROST).after(
        Summon(CONTROLLER, "BAR_888t")
    )


class WC_041:
    """Shattering Blast - 冰爆冲击
    Destroy all Frozen minions.
    摧毁所有被冻结的随从。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(ALL_MINIONS + FROZEN)


class WC_805:
    """Frostweave Dungeoneer - 织霜地下城历险家
    Battlecry: Draw a spell. If it's a Frost spell, summon two 1/1 Elementals that Freeze.
    战吼：抽一张法术牌。如果是冰霜法术，召唤两个1/1会冻结的元素。
    """
    def play(self):
        cards = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL)
        if cards:
            for card in cards:
                if card and card.spell_school == SpellSchool.FROST:
                    yield Summon(CONTROLLER, "WC_805t") * 2
                    break


class WC_806:
    """Floecaster - 浮冰施法者
    Costs (2) less for each Frozen enemy.
    每有一个被冻结的敌人，本牌的法力值消耗便减少（2）点。
    """
    cost_mod = -Count(ENEMY_CHARACTERS + FROZEN) * 2


