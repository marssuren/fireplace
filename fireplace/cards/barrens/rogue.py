"""贫瘠之地的锤炼（Forged in the Barrens）卡牌实现"""
from ..utils import *


class BAR_316:
    """Oil Rig Ambusher - 油井伏击者
    Battlecry: Deal 2 damage. If this entered your hand this turn, deal 4 instead.
    战吼：造成2点伤害。如果该随从在本回合中进入你的手牌，则改为造成4点伤害。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    def play(self):
        damage = 4 if getattr(self, 'drawn_this_turn', False) else 2
        yield Hit(self.target, damage)


class BAR_317:
    """Field Contact - 原野联络人
    After you play a Battlecry or Combo card, draw a card.
    在你打出一张战吼或连击牌后，抽一张牌。
    """
    events = (
        Play(CONTROLLER, BATTLECRY).after(Draw(CONTROLLER)),
        Play(CONTROLLER, COMBO).after(Draw(CONTROLLER)),
    )


class BAR_318:
    """Silverleaf Poison - 银叶草药膏
    Give your weapon "After your hero attacks, draw a card."
    使你的武器获得"在你的英雄攻击后，抽一张牌。"
    """
    requirements = {
        PlayReq.REQ_WEAPON_EQUIPPED: 0,
    }
    play = Buff(FRIENDLY_WEAPON, "BAR_318e")


class BAR_318e:
    """Silverleaf Poison buff"""
    events = Attack(FRIENDLY_HERO).after(Draw(CONTROLLER))


class BAR_319:
    """Wicked Stab (Rank 1) - 邪恶挥刺（等级1）
    Deal $2 damage. (Upgrades when you have 5 Mana.)
    造成$2点伤害。（在你有5点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_319t",
        enums.RANKED_SPELL_THRESHOLD: 5,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 2)


class BAR_319t:
    """Wicked Stab (Rank 2) - 邪恶挥刺（等级2）
    Deal $3 damage. (Upgrades when you have 10 Mana.)
    造成$3点伤害。（在你有10点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_319t2",
        enums.RANKED_SPELL_THRESHOLD: 10,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 3)


class BAR_319t2:
    """Wicked Stab (Rank 3) - 邪恶挥刺（等级3）
    Deal $4 damage.
    造成$4点伤害。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 4)


class BAR_320:
    """Efficient Octo-bot - 高效八爪机器人
    Frenzy: Reduce the Cost of cards in your hand by (1).
    暴怒：使你手牌中的所有牌的法力值消耗减少（1）点。
    """
    frenzy = Buff(FRIENDLY_HAND, "BAR_320e")


class BAR_320e:
    tags = {
        GameTag.COST: -1,
    }


class BAR_321:
    """Paralytic Poison - 麻痹药膏
    Give your weapon +1 Attack and "Your hero is Immune while attacking."
    使你的武器获得+1攻击力和"你的英雄在攻击时免疫。"
    """
    requirements = {
        PlayReq.REQ_WEAPON_EQUIPPED: 0,
    }
    play = Buff(FRIENDLY_WEAPON, "BAR_321e")


class BAR_321e:
    """Paralytic Poison buff"""
    tags = {
        GameTag.ATK: 1,
    }
    events = (
        Attack(FRIENDLY_HERO).on(SetTags(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: True})),
        Attack(FRIENDLY_HERO).after(SetTags(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: False})),
    )


class BAR_322:
    """Swinetusk Shank - 猪牙匕首
    After you play a Poison, gain +1 Durability.
    在你打出一张药膏牌后，获得+1耐久度。
    """
    events = Play(CONTROLLER, FuncSelector(lambda entities, src: [
        e for e in entities 
        if e.type == CardType.SPELL and 'Poison' in e.id
    ])).after(Buff(SELF, "BAR_322e"))


class BAR_322e:
    tags = {
        GameTag.DURABILITY: 1,
    }


class BAR_323:
    """Yoink! - 偷师学艺
    Discover a Hero Power and set its Cost to (0). Swap back after 2 uses.
    发现一个英雄技能，并将其法力值消耗设置为（0）点。使用2次后换回。
    """
    play = DISCOVER(RandomHeroPower()).then(
        # 保存原英雄技能并替换
        Give(CONTROLLER, "BAR_323t")  # 临时英雄技能
    )


class BAR_324:
    """Apothecary Helbrim - 药剂师赫布瑞姆
    Battlecry and Deathrattle: Add a random Poison to your hand.
    战吼和亡语：将一张随机药膏牌置入你的手牌。
    """
    play = Give(CONTROLLER, RandomID("BAR_318", "BAR_321"))
    deathrattle = Give(CONTROLLER, RandomID("BAR_318", "BAR_321"))


class BAR_552:
    """Scabbs Cutterbutter - 斯卡布斯·刀油
    Combo: The next two cards you play this turn cost (2) less.
    连击：你在本回合中打出的接下来两张牌的法力值消耗减少（2）点。
    """
    combo = Buff(FRIENDLY_HERO, "BAR_552e")


class BAR_552e:
    """Scabbs buff"""
    tags = {
        enums.ACTIVATIONS_THIS_TURN: 0,
    }
    update = (
        Find(SELF + (ACTIVATIONS_THIS_TURN < 2))
        & Refresh(FRIENDLY_HAND, {GameTag.COST: -2})
    )
    events = (
        Play(CONTROLLER).after(AddProgress(SELF, SELF, 1, "activations_this_turn")),
        OWN_TURN_END.on(Destroy(SELF)),
    )


class WC_015:
    """Water Moccasin - 水栖蝮蛇
    Stealth. Has Poisonous while you have no other minions.
    潜行。当你没有其他随从时，具有剧毒。
    """
    update = -Find(FRIENDLY_MINIONS - SELF) & SetTags(SELF, {GameTag.POISONOUS: True})


class WC_016:
    """Shroud of Concealment - 潜伏帷幕
    Draw 2 minions. Any played this turn gain Stealth for 1 turn.
    抽两张随从牌。本回合打出的随从获得潜行，持续1回合。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        ForceDraw(RANDOM(FRIENDLY_DECK + MINION)),
        ForceDraw(RANDOM(FRIENDLY_DECK + MINION)),
        Buff(FRIENDLY_HERO, "WC_016e"),
    )


class WC_016e:
    """Shroud buff"""
    events = (
        Play(CONTROLLER, MINION).after(
            Stealth(Play.CARD),
            Buff(Play.CARD, "WC_016e2"),
        ),
        OWN_TURN_END.on(Destroy(SELF)),
    )


class WC_016e2:
    """Stealth for 1 turn"""
    events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


class WC_017:
    """Savory Deviate Delight - 美味风蛇
    Transform a minion in both players' hands into a Pirate or Stealth minion.
    将双方玩家手牌中的一个随从变形成为一个海盗或潜行随从。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    def play(self):
        import random
        # 随机选择海盗或潜行随从
        choice = random.choice([
            RandomMinion(race=Race.PIRATE),
            RandomMinion(stealth=True)
        ])
        yield Morph(RANDOM(FRIENDLY_HAND + MINION), choice)
        yield Morph(RANDOM(ENEMY_HAND + MINION), choice)


