"""
深暗领域 - HUNTER
"""
from ..utils import *


# COMMON

class GDB_840:
    """异星虫卵 - Extraterrestrial Egg
    Deathrattle: Summon a 3/5 Beast that attacks the lowest Health enemy.
    
    2费 0/2 猎人随从
    <b>亡语:</b>召唤一只3/5的野兽并使其攻击生命值最低的敌人。
    """
    # 亡语：召唤一只3/5的野兽并使其攻击生命值最低的敌人
    def deathrattle(self):
        # 召唤3/5野兽
        yield Summon(CONTROLLER, "GDB_840t")


class GDB_841:
    """游侠斥候 - Rangari Scout
    After you Discover a card, get a copy of it.
    
    1费 1/2 猎人随从 - 德莱尼
    在你<b>发现</b>一张牌后，获取一张该牌的复制。
    """
    race = Race.DRAENEI
    
    # 在发现一张牌后，获取一张该牌的复制
    # 监听Discover事件，当发现完成后，给予一张相同的牌
    events = Discover(CONTROLLER).after(
        Give(CONTROLLER, Copy(Discover.CARD))
    )


class GDB_844:
    """详尽笔记 - Detailed Notes
    Discover a Beast that costs (5) or more. Reduce its Cost by (2).
    
    2费 猎人法术
    <b>发现</b>一张法力值消耗为（5）点或更高的野兽牌。使其法力值消耗减少（2）点。
    """
    def play(self):
        # 发现一张5费或更高的野兽牌
        yield Discover(CONTROLLER, RandomMinion(race=Race.BEAST, cost_min=5)).then(
            Give(CONTROLLER, Discover.CARD),
            # 使其法力值消耗减少2点
            Buff(Discover.CARD, "GDB_844e")
        )


class GDB_844e:
    """法力值消耗减少（2）点"""
    tags = {
        GameTag.COST: -2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class SC_021:
    """进化腔 - Evolution Chamber
    Give your minions +1 Attack. Give your Zerg an extra +1/+1.
    
    2费 猎人法术
    使你的随从获得+1攻击力。使你的异虫额外获得+1/+1。
    """
    def play(self):
        # 给所有友方随从+1攻击力
        yield Buff(FRIENDLY_MINIONS, "SC_021e1")
        # 给所有友方异虫额外+1/+1
        for minion in self.controller.field:
            if minion.race == Race.ZERG:
                yield Buff(minion, "SC_021e2")


class SC_021e1:
    """+1攻击力"""
    tags = {
        GameTag.ATK: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class SC_021e2:
    """异虫额外+1/+1"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


# RARE

class GDB_111:
    """生化罐仓 - Biopod
    Deathrattle: Deal damage equal to this minion's Attack to a random enemy. Starship Piece

    2费 2/2 猎人随从 - 星舰组件
    <b>亡语：</b>随机对一个敌人造成等同于本随从攻击力的伤害。
    <b>星舰组件</b>
    """
    # 亡语：随机对一个敌人造成等同于本随从攻击力的伤害
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, ATK(SELF))


class GDB_237:
    """接触异星生物 - Alien Encounters
    Summon two 2/4 Beasts with Taunt. Costs (1) less for each card you Discovered this game.
    
    5费 猎人法术
    召唤两只2/4并具有<b>嘲讽</b>的野兽。在本局对战中，你每<b>发现</b>一张牌，本牌的法力值消耗便减少（1）点。
    """
    # 动态计算费用减免
    @property
    def cost(self):
        # 基础费用5点，每发现一张牌减少1点
        base_cost = self.data.cost
        if hasattr(self.controller, 'cards_discovered_this_game'):
            reduction = self.controller.cards_discovered_this_game
            return max(0, base_cost - reduction)
        return base_cost
    
    def play(self):
        # 召唤两只2/4嘲讽野兽
        yield Summon(CONTROLLER, "GDB_237t") * 2


class GDB_845:
    """激光弹幕 - Laser Barrage
    Deal $3 damage to a minion. If you're building a Starship, also damage its neighbors.
    
    2费 猎人法术
    对一个随从造成$3点伤害。如果你正在建造<b>星舰</b>，则也对其相邻的随从造成伤害。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        # 对目标造成3点伤害
        yield Hit(TARGET, 3)
        
        # 如果正在建造星舰，也对相邻随从造成伤害
        if self.controller.starship_in_progress:
            # 获取目标的相邻随从
            target_pos = self.target.zone_position
            for minion in self.target.controller.field:
                # 检查是否相邻（位置差为1）
                if abs(minion.zone_position - target_pos) == 1:
                    yield Hit(minion, 3)


class SC_008:
    """刺蛇 - Hydralisk
    Battlecry: Deal 2 damage to a random enemy. Repeat for each other Zerg minion you control.
    
    3费 4/2 猎人随从 - 异虫
    <b>战吼：</b>随机对一个敌人造成2点伤害。你每控制一个其他异虫随从，便重复一次。
    """
    race = Race.ZERG
    
    def play(self):
        # 计算其他异虫随从数量（不包括自己）
        zerg_count = len([m for m in self.controller.field if m.race == Race.ZERG and m != self])
        
        # 基础1次 + 每个其他异虫1次
        times = 1 + zerg_count
        
        # 对随机敌人造成2点伤害，重复times次
        for _ in range(times):
            yield Hit(RANDOM_ENEMY_CHARACTER, 2)


class SC_012:
    """蟑螂 - Roach
    When you draw this, get a copy of it. Battlecry: If you control another Zerg minion, gain +1/+2.
    
    2费 2/2 猎人随从 - 异虫
    在你抽到本牌时，获取一张本牌的复制。<b>战吼：</b>如果你控制另一个异虫随从，则获得+1/+2。
    """
    race = Race.ZERG
    
    # 抽到时获取一张复制
    events = Draw(CONTROLLER, SELF).on(
        Give(CONTROLLER, Copy(SELF))
    )
    
    def play(self):
        # 检查是否控制其他异虫随从
        has_other_zerg = any(m.race == Race.ZERG and m != self for m in self.controller.field)
        
        if has_other_zerg:
            # 获得+1/+2
            yield Buff(SELF, "SC_012e")


class SC_012e:
    """+1/+2增益"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


# EPIC

class GDB_107:
    """取样探爪 - Specimen Claw
    After your opponent plays a minion, attack it. Starship Piece

    3费 2/6 猎人随从 - 星舰组件
    在你的对手使用一张随从牌后，攻击该随从。
    <b>星舰组件</b>
    """
    # 在你的对手使用一张随从牌后，攻击该随从
    events = Play(OPPONENT, MINION).after(Attack(SELF, Play.CARD))


class GDB_843:
    """视差光枪 - Parallax Cannon
    Has +2 Attack if you've Discovered this turn. Spellburst: Your hero is Immune this turn.
    
    3费 2/3 猎人武器
    在本回合中，如果你<b>发现</b>过，则具有+2攻击力。<b>法术迸发：</b>在本回合中，你的英雄<b>免疫</b>。
    """
    tags = {
        GameTag.SPELLBURST: True,
    }
    
    # 如果本回合发现过，+2攻击力
    @property
    def atk(self):
        base_atk = self.data.atk
        if hasattr(self.controller, 'cards_discovered_this_turn') and self.controller.cards_discovered_this_turn > 0:
            return base_atk + 2
        return base_atk
    
    # 法术迸发：英雄免疫本回合
    # 使用buff机制,在回合结束时自动移除免疫效果
    events = OWN_SPELL_PLAY.on(
        Buff(FRIENDLY_HERO, "GDB_843e"),
        SetTags(SELF, {GameTag.SPELLBURST: False})
    )


class GDB_843e:
    """英雄免疫本回合"""
    tags = {
        GameTag.IMMUNE: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }
    # 回合结束时移除
    events = OWN_TURN_END.on(Destroy(SELF))


# LEGENDARY

class GDB_842:
    """吞世巨虫戈姆 - Gorm the Worldeater
    Dormant for 5 turns. At the end of your turn, destroy the minion to the right of this to awaken 1 turn sooner.
    
    3费 12/12 猎人随从 - 野兽（传说）
    <b>休眠</b>5回合。在你的回合结束时，摧毁本随从右侧的随从，以提前1回合苏醒。
    """
    race = Race.BEAST
    
    # 进场时休眠5回合
    def play(self):
        # 设置休眠5回合
        yield SetTags(SELF, {GameTag.DORMANT: 5})
    
    # 在回合结束时，摧毁右侧随从以提前苏醒
    events = OWN_TURN_END.on(
        lambda self, player: DestroyRightMinionToAwaken(self)
    )


def DestroyRightMinionToAwaken(gorm):
    """摧毁右侧随从以提前苏醒
    
    在回合结束时，如果戈姆右侧有随从，摧毁它并使戈姆提前1回合苏醒。
    """
    def action(source):
        # 如果戈姆不在场上或不是休眠状态，不执行
        if gorm.zone != Zone.PLAY or not gorm.dormant:
            return
        
        # 找到戈姆右侧的随从
        gorm_pos = gorm.zone_position
        right_minion = None
        
        for minion in gorm.controller.field:
            if minion.zone_position == gorm_pos + 1:
                right_minion = minion
                break
        
        # 如果右侧有随从，摧毁它并减少休眠回合数
        if right_minion:
            yield Destroy(right_minion)
            # 减少休眠回合数（最少为0）
            current_dormant = gorm.tags.get(GameTag.DORMANT, 0)
            if current_dormant > 0:
                yield SetTags(gorm, {GameTag.DORMANT: current_dormant - 1})
    
    return action


class GDB_846:
    """大主教奈丽 - Exarch Naielle
    Battlecry: Replace your Hero Power with Tracking (Discover a card from your deck).
    
    3费 3/4 猎人随从 - 德莱尼（传说）
    <b>战吼：</b>将你的英雄技能替换为追踪<i>（从你的牌库中<b>发现</b>一张牌）</i>。
    """
    race = Race.DRAENEI
    
    def play(self):
        # 替换英雄技能为追踪
        # 参考其他英雄技能替换的实现(如stormwind/warlock.py的TOY_829)
        old_power = self.controller.hero.power
        if old_power:
            old_power.destroy()
        
        # 创建新的英雄技能
        new_power = self.controller.card("GDB_846t", source=self)
        new_power.zone = Zone.PLAY
        self.controller.hero.power = new_power
