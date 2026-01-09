"""
胜地历险记 - DEMONHUNTER
"""
from ..utils import *


# COMMON

class VAC_925:
    """伞降咒符 - Sigil of Skydiving
    At the start of your next turn, summon two 1/1 Pirates with Charge.
    在你的下个回合开始时，召唤两个1/1并具有冲锋的海盗。
    """
    # 2费法术 邪能学派
    # 注意：Patch 31.2.213852 (2024-12-17) 削弱：从召唤3个改为召唤2个
    # 在下个回合开始时触发效果
    def play(self):
        # 给玩家添加一个 buff，在下个回合开始时触发
        yield Buff(CONTROLLER, "VAC_925e")


class VAC_925e:
    """伞降咒符效果 (Player Enchantment)"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

    # 在己方回合开始时触发
    events = OWN_TURN_BEGIN.on(
        Summon(CONTROLLER, "VAC_925t") * 2,
        Destroy(SELF)
    )


class VAC_927:
    """狂飙邪魔 - Adrenaline Fiend
    After a friendly Pirate attacks, give your hero +1 Attack this turn.
    在一个友方海盗攻击后，使你的英雄在本回合中获得+1攻击力。
    """
    # 2/2/2 恶魔+海盗
    # 监听友方海盗攻击事件
    events = Attack(FRIENDLY_MINIONS + PIRATE).after(
        Buff(FRIENDLY_HERO, "VAC_927e")
    )


class VAC_927e:
    """狂飙邪魔攻击力 Buff"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_ONE_TURN_EFFECT: True  # 本回合结束时移除
    }
    atk = 1


class VAC_930:
    """全地形虚空猎犬 - All Terrain Voidhound
    Whenever this attacks, give your hero +5 Attack this turn.
    每当本随从攻击时，使你的英雄在本回合中获得+5攻击力。
    """
    # 7/5/8 恶魔
    # 监听自身攻击事件
    events = Attack(SELF).on(
        Buff(FRIENDLY_HERO, "VAC_930e")
    )


class VAC_930e:
    """全地形虚空猎犬攻击力 Buff"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_ONE_TURN_EFFECT: True  # 本回合结束时移除
    }
    atk = 5


class WORK_015:
    """精魂商贩 - Spirit Peddler
    Rush. Deathrattle: Reduce the Cost of a random minion in your hand by (6).
    突袭。亡语：随机使你手牌中的一张随从牌的法力值消耗减少（6）点。
    """
    # 6/6/6 恶魔 突袭+亡语
    def deathrattle(self):
        # 随机选择手牌中的一张随从牌
        minions_in_hand = self.controller.hand.filter(type=CardType.MINION)
        if minions_in_hand:
            target = self.game.random.choice(minions_in_hand)
            yield Buff(target, "WORK_015e")


class WORK_015e:
    """精魂商贩费用减少 Buff"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    cost_mod = -6


class WORK_016:
    """狱火订书器 - Infernal Stapler
    After your hero attacks, deal 3 damage to your hero.
    在你的英雄攻击后，对你的英雄造成3点伤害。
    """
    # 2/3/2 武器
    # 监听英雄攻击事件
    events = Attack(FRIENDLY_HERO).after(
        Hit(FRIENDLY_HERO, 3)
    )


# RARE

class VAC_928:
    """飞翼滑翔 - Paraglide
    Both players draw 3 cards. Outcast: Only you do.
    双方玩家抽三张牌。流放：只有你抽牌。
    """
    # 2费法术 流放机制
    def play(self):
        # 检查是否触发流放
        if self.outcast:
            # 流放：只有你抽牌
            yield Draw(CONTROLLER) * 3
        else:
            # 正常：双方玩家都抽牌
            yield Draw(CONTROLLER) * 3
            yield Draw(OPPONENT) * 3


class VAC_929:
    """惊险悬崖 - Dangerous Cliffside
    Summon two 1/1 Pirates with Charge. After your hero attacks, reopen this.
    召唤两个1/1并具有冲锋的海盗。在你的英雄攻击后，重新开启本地标。
    """
    # 4费地标 3耐久
    # Location 默认有 activate 能力
    def activate(self):
        # 召唤两个1/1海盗
        yield Summon(CONTROLLER, "VAC_929t") * 2

    # 监听英雄攻击事件，重新开启地标
    events = Attack(FRIENDLY_HERO).after(
        Refresh(SELF)
    )


class VAC_931:
    """生死一线 - Skirting Death
    Choose a minion. This turn, your hero steals 4 Attack from it.
    选择一个随从。在本回合中，你的英雄从该随从处偷取4点攻击力。
    """
    # 3费法术 暗影学派
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self):
        # 给目标随从减少4点攻击力（本回合）
        yield Buff(TARGET, "VAC_931e")
        # 给英雄增加4点攻击力（本回合）
        yield Buff(FRIENDLY_HERO, "VAC_931e2")


class VAC_931e:
    """生死一线攻击力减少 Buff"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_ONE_TURN_EFFECT: True
    }
    atk = -4


class VAC_931e2:
    """生死一线攻击力增加 Buff"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_ONE_TURN_EFFECT: True
    }
    atk = 4


class WORK_014:
    """恶魔交易 - Demonic Deal
    Lifesteal. Deal $4 damage to a minion. Put a random Demon that costs (5) or more on top of your deck.
    吸血。对一个随从造成$4点伤害。将一张法力值消耗大于或等于（5）点的随机恶魔牌置于你的牌库顶。
    """
    # 3费法术 邪能学派 吸血
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    lifesteal = True

    def play(self):
        # 造成4点伤害
        yield Hit(TARGET, 4)
        # 将一张随机恶魔牌（费用>=5）置于牌库顶
        yield Shuffle(CONTROLLER, RandomCollectible(race=Race.DEMON, cost_min=5), to_top=True)


# EPIC

class VAC_926:
    """高崖跳水 - Cliff Dive
    Summon 2 minions from your deck and give them Rush. They go back at the end of your turn.
    从你的牌库中召唤2个随从并使其获得突袭。在你的回合结束时，将它们移回牌库。
    """
    # 6费法术
    def play(self):
        # 从牌库中召唤2个随从
        minions = yield Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION) * 2)

        # 给召唤的随从添加突袭和回合结束时返回牌库的效果
        for minion in minions:
            # 给予突袭
            yield Buff(minion, "VAC_926e")


class VAC_926e:
    """高崖跳水 Buff"""
    tags = {
        GameTag.RUSH: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }

    # 在回合结束时，将随从移回牌库
    events = OWN_TURN_END.on(
        Bounce(OWNER),
        Shuffle(CONTROLLER, Copy(OWNER))
    )


class VAC_932:
    """登山钩爪 - Climbing Hook
    Doesn't lose Durability while you control a minion with 5 or more Attack.
    当你控制着攻击力大于或等于5的随从时，不会失去耐久度。
    """
    # 6/5/2 武器
    # 使用 Aura 实现条件性耐久度保护
    # 当控制攻击力>=5的随从时，武器不会失去耐久度
    class Hand:
        # 在手牌中也显示效果
        pass

    # 使用 IMMUNE_WHILE_ATTACKING 或自定义逻辑
    # 检查是否有攻击力>=5的随从
    update = Find(FRIENDLY_MINIONS + (ATK >= 5)) & Refresh(SELF, {
        GameTag.IMMUNE_WHILE_ATTACKING: True
    })


# LEGENDARY

class VAC_501:
    """极限追逐者阿兰娜 - Aranna, Thrill Seeker
    Priest Tourist. Damage your hero takes on your turn is redirected to a random enemy.
    牧师游客。你的英雄在你的回合中受到的伤害会转移给一个随机敌人。
    """
    # 5/5/6 传说随从
    # 游客机制：允许在套牌中加入牧师卡牌（构筑规则，无需战斗逻辑）
    # 核心效果：在己方回合中，英雄受到的伤害转移给随机敌人

    # 使用 Predamage 事件拦截伤害
    events = Predamage(FRIENDLY_HERO).on(
        lambda self, source, target, amount: (
            # 检查是否是己方回合
            self.controller.current_player and [
                # 取消对英雄的伤害
                SetTag(Predamage.TARGET, {(GameTag.PREDAMAGE: 0})),
                # 对随机敌人造成相同伤害
                Hit(RANDOM_ENEMY_CHARACTER, amount)
            ] or []
        )
    )


class VAC_933:
    """飞行员帕奇斯 - Patches the Pilot
    Battlecry: Shuffle six Parachutes into your deck that summon a 1/1 Pirate with Charge when drawn.
    战吼：将六张降落伞洗入你的牌库。当抽到降落伞时，召唤一个1/1并具有冲锋的海盗。
    """
    # 1/1/1 传说随从 恶魔+海盗
    def play(self):
        # 将6张降落伞洗入牌库
        yield Shuffle(CONTROLLER, "VAC_933t") * 6
