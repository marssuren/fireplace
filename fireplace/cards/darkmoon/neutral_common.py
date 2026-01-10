from ..utils import *


##
# Minions

class DMF_044:
    """Rock Rager (岩石暴怒者)
    Taunt"""
    # 5费 5/1 嘲讽 - 香草卡牌
    pass


class DMF_062:
    """Gyreworm (旋岩虫)
    Battlecry: If you played an Elemental last turn, deal 3 damage."""
    # 3费 3/2 - 战吼：如果你上回合打出过元素，造成3点伤害
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    powered_up = ELEMENTAL_PLAYED_LAST_TURN
    play = powered_up & Hit(TARGET, 3)


class DMF_065:
    """Banana Vendor (香蕉商贩)
    Battlecry: Add 2 Bananas to each player's hand."""
    # 3费 2/4 - 战吼：将2根香蕉加入双方手牌
    play = Give(ALL_PLAYERS, "EX1_014t") * 2


class DMF_066:
    """Knife Vendor (小刀商贩)
    Battlecry: Deal 4 damage to each hero."""
    # 4费 3/4 - 战吼：对双方英雄造成4点伤害
    play = Hit(ALL_HEROES, 4)


class DMF_067:
    """Prize Vendor (奖品商贩)
    Battlecry and Deathrattle: Each player draws a card."""
    # 2费 2/3 - 战吼和亡语：双方各抽一张牌
    play = Draw(ALL_PLAYERS)
    deathrattle = Draw(ALL_PLAYERS)


class DMF_068:
    """Optimistic Ogre (乐观的食人魔)
    50% chance to attack the correct enemy."""
    # 6费 6/7 - 50%几率攻击错误的敌人（FORGETFUL关键词自动处理）
    pass


class DMF_069:
    """Claw Machine (娃娃机)
    Rush. Deathrattle: Draw a minion and give it +3/+3."""
    # 6费 6/3 突袭 - 亡语：抽一张随从牌并使其获得+3/+3
    deathrattle = Buff(Draw(CONTROLLER) + MINION, "DMF_069e")


class DMF_069e:
    """Rigged (作弊)"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
    }


class DMF_073:
    """Darkmoon Dirigible (暗月飞船)
    Divine Shield Corrupt: Gain Rush."""
    # 3费 3/2 圣盾 - 腐蚀：获得突袭
    corrupt = SetAttr(SELF, GameTag.RUSH, True)


class DMF_078:
    """Strongman (大力士)
    Taunt Corrupt: This costs (0)."""
    # 6费 6/6 嘲讽 - 腐蚀：法力值消耗变为(0)
    corrupt = Buff(SELF, "DMF_078e")


class DMF_078e:
    """Corrupted (已腐蚀)"""
    tags = {
        GameTag.COST: SET(0),
    }


class DMF_079:
    """Inconspicuous Rider (低调的游客)
    Battlecry: Cast a Secret from your deck."""
    # 3费 2/2 - 战吼：从你的牌库中施放一张奥秘
    play = CastSpell(RANDOM(FRIENDLY_DECK + SECRET))


class DMF_080:
    """Fleethoof Pearltusk (迅蹄珠齿象)
    Rush Corrupt: Gain +4/+4."""
    # 5费 4/4 突袭 - 腐蚀：获得+4/+4
    corrupt = Buff(SELF, "DMF_080e")


class DMF_080e:
    """Corrupted (已腐蚀)"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
    }


class DMF_082:
    """Darkmoon Statue (暗月雕像)
    Your other minions have +1 Attack. Corrupt: This gains +4 Attack."""
    # 3费 0/5 - 你的其他随从获得+1攻击力。腐蚀：本随从获得+4攻击力
    update = Refresh(FRIENDLY_MINIONS - SELF, {GameTag.ATK: +1})
    corrupt = Buff(SELF, "DMF_082e")


class DMF_082e:
    """Corrupted (已腐蚀)"""
    tags = {
        GameTag.ATK: 4,
    }


class DMF_091:
    """Wriggling Horror (蠕动的恐魔)
    Battlecry: Give adjacent minions +1/+1."""
    # 2费 3/1 - 战吼：使相邻的随从获得+1/+1
    play = Buff(SELF_ADJACENT, "DMF_091e")


class DMF_091e:
    """Corrupted (已腐蚀)"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class DMF_174:
    """Circus Medic (马戏团医师)
    Battlecry: Restore #4 Health. Corrupt: Deal 4 damage instead."""
    # 4费 3/4 - 战吼：恢复4点生命值。腐蚀：改为造成4点伤害
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    
    def play(self):
        # 检查是否已腐蚀（通过检查是否有腐蚀buff）
        if hasattr(self, 'corrupted') and self.corrupted:
            # 已腐蚀：造成伤害
            yield Hit(TARGET, 4)
        else:
            # 未腐蚀：恢复生命
            yield Heal(TARGET, 4)
    
    # 腐蚀效果：标记为已腐蚀
    corrupt = Buff(SELF, "DMF_174e")


class DMF_174e:
    """Corrupted (已腐蚀)"""
    def apply(self, target):
        target.corrupted = True


class DMF_189:
    """Costumed Entertainer (盛装演员)
    Battlecry: Give a random minion in your hand +2/+2."""
    # 2费 1/2 - 战吼：随机使你手牌中的一张随从牌获得+2/+2
    play = Buff(RANDOM(FRIENDLY_HAND + MINION), "DMF_189e")


class DMF_189e:
    """Entertained (娱乐)"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class DMF_190:
    """Fantastic Firebird (炫目火鸟)
    Windfury"""
    # 4费 3/5 风怒 - 香草卡牌
    pass


class DMF_191:
    """Showstopper (砸场游客)
    Deathrattle: Silence all minions."""
    # 6费 5/5 - 亡语：沉默所有随从
    deathrattle = Silence(ALL_MINIONS)


class DMF_520:
    """Parade Leader (巡游领队)
    After you summon a Rush minion, give it +2 Attack."""
    # 3费 2/3 - 在你召唤一个突袭随从后，使其获得+2攻击力
    events = Summon(CONTROLLER, FRIENDLY + MINION + RUSH).after(
        Buff(Summon.CARD, "DMF_520e")
    )


class DMF_520e:
    """Inspired (鼓舞)"""
    tags = {
        GameTag.ATK: 2,
    }


class DMF_532:
    """Circus Amalgam (马戏团融合怪)
    Taunt This has all minion types."""
    # 4费 4/5 嘲讽 - 拥有所有随从类型（ALL关键词在CardDefs.xml中定义）
    pass


class YOP_021:
    """Imprisoned Phoenix (被禁锢的凤凰)
    Dormant for 2 turns. Spell Damage +2"""
    # 2费 2/3 休眠2回合，法术伤害+2
    # Dormant机制在CardDefs.xml中定义
    pass


class YOP_030:
    """Felfire Deadeye (邪火神射手)
    Your Hero Power costs (1) less."""
    # 2费 2/3 - 你的英雄技能法力值消耗减少(1)点
    update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: -1})


class YOP_031:
    """Crabrider (螃蟹骑士)
    Rush Windfury"""
    # 2费 1/4 突袭+风怒 - 香草卡牌
    pass


##
# Spells

class YOP_005:
    """Barricade (路障)
    Summon a 2/4 Guard with Taunt. If it's your only minion, summon another."""
    # 3费法术 - 召唤一个2/4并具有嘲讽的守卫。如果它是你的唯一随从，再召唤一个
    def play(self):
        # 召唤第一个守卫
        actions = [Summon(CONTROLLER, "YOP_005t")]
        # 检查是否是唯一随从（场上只有1个随从）
        # 使用条件：如果场上友方随从数量为1，再召唤一个
        actions.append(
            Find(Count(FRIENDLY_MINIONS) == 1) & Summon(CONTROLLER, "YOP_005t")
        )
        return actions


class YOP_005t:
    """Guard (守卫)"""
    # 2/4 嘲讽 - Token随从
    pass


class YOP_015:
    """Nitroboost Poison (氮素药膏)
    Give a minion +2 Attack. Corrupt: And your weapon."""
    # 1费法术 - 使一个随从获得+2攻击力。腐蚀：同时使你的武器获得+2攻击力
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        # 基础效果：给随从+2攻击
        actions = [Buff(TARGET, "YOP_015e")]
        # 如果已腐蚀，同时给武器+2攻击
        if hasattr(self, 'corrupted') and self.corrupted:
            actions.append(Buff(FRIENDLY_WEAPON, "YOP_015e2"))
        return actions
    
    # 腐蚀效果：标记为已腐蚀
    corrupt = Buff(SELF, "YOP_015_corrupt")


class YOP_015_corrupt:
    """Corrupted (已腐蚀)"""
    def apply(self, target):
        target.corrupted = True


class YOP_015e:
    """Nitroboosted (氮素强化)"""
    tags = {
        GameTag.ATK: 2,
    }


class YOP_015e2:
    """Nitroboosted (氮素强化)"""
    tags = {
        GameTag.ATK: 2,
    }


class YOP_029:
    """Resizing Pouch (随心口袋)
    Discover a card with Cost equal to your remaining Mana Crystals."""
    # 0费法术 - 发现一张法力值消耗等于你剩余法力水晶数量的卡牌
    
    def play(self):
        # 获取当前剩余法力值
        mana = self.controller.mana
        # 发现一张费用等于剩余法力的卡牌
        yield GenericChoice(CONTROLLER, RandomCollectible(cost=mana) * 3)
