"""
威兹班的工坊 - PRIEST
"""
from ..utils import *


# COMMON

class TOY_381:
    """纸艺天使 - Paper Angel
    Your Hero Power costs (0).
    你的英雄技能的法力值消耗为（0）点。
    """
    # 2费 2/3 随从
    # 光环效果：使英雄技能费用为0
    
    class Hand:
        """在手牌时也生效的光环"""
        update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: SET(0)})
    
    update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: SET(0)})


class TOY_384:
    """净化之力 - Purified Strength
    <b>Silence</b> all friendly minions, then give them +1/+2.
    <b>沉默</b>所有友方随从，然后使其获得+1/+2。
    """
    # 2费圣光法术
    # 效果：沉默所有友方随从，然后+1/+2
    
    def play(self):
        # 先沉默所有友方随从
        yield Silence(FRIENDLY_MINIONS)
        # 然后给予+1/+2
        yield Buff(FRIENDLY_MINIONS, "TOY_384e")


class MIS_714:
    """哈哈镜 - Funhouse Mirror
    Summon a copy of an enemy minion and make it attack the original.
    召唤一个敌方随从的一个复制并使其攻击本体。
    """
    # 3费暗影法术
    # 效果：召唤敌方随从复制，并让复制攻击本体
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        # 召唤目标的复制
        copy = yield Summon(CONTROLLER, ExactCopy(TARGET))
        
        if copy:
            # 让复制攻击原始目标
            # 需要等待召唤完成后再攻击
            yield Attack(copy[0], TARGET)


class TOY_382:
    """粗心的匠人 - Careless Crafter
    <b>Deathrattle:</b> Get two (0)-Cost Bandages that Restore 3 Health.
    <b>亡语：</b>获取两张法力值消耗为（0）的可以恢复3点生命值的绷带。
    """
    # 3费 3/3 随从
    # 亡语：获取两张绷带
    
    def deathrattle(self):
        # 获取两张绷带 Token
        yield Give(CONTROLLER, "TOY_382t")
        yield Give(CONTROLLER, "TOY_382t")


class MIS_919:
    """木偶剧场 - Puppet Theatre
    Choose an enemy minion. Get a 1/1 copy of it that costs (1).
    选择一个敌方随从，获取一张它的1/1且法力值消耗为（1）点的复制。
    """
    # 4费地标 2耐久
    # 效果：选择敌方随从，获取1/1费用为1的复制
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def activate(self):
        # 获取目标随从的ID
        target_id = TARGET.id
        
        # 创建复制
        copy = yield Give(CONTROLLER, target_id)
        
        if copy:
            # 设置为1/1，费用为1
            # 使用 Buff 设置属性（参考 TOY_813 的实现）
            yield Buff(copy[0], "MIS_919e", atk=1, max_health=1, cost=1)


# RARE

class TOY_387:
    """对照鳞摹 - Contrasted Scales
    Draw your lowest and highest Cost Dragon.
    抽取你法力值消耗最低和最高的龙牌。
    """
    # 2费法术
    # 效果：抽取牌库中费用最低和最高的龙牌
    
    def play(self):
        # 获取牌库中所有龙牌
        dragons = (FRIENDLY_DECK + DRAGON).eval(self.game, self)
        
        if not dragons:
            return
        
        # 找到费用最低的龙牌
        min_cost = min(card.cost for card in dragons)
        lowest_dragons = [card for card in dragons if card.cost == min_cost]
        
        if lowest_dragons:
            # 随机抽取一张最低费用的龙牌
            lowest = self.game.random.choice(lowest_dragons)
            yield ForceDraw(CONTROLLER, lowest)
        
        # 重新获取牌库中的龙牌（因为可能抽走了一张）
        dragons = (FRIENDLY_DECK + DRAGON).eval(self.game, self)
        
        if not dragons:
            return
        
        # 找到费用最高的龙牌
        max_cost = max(card.cost for card in dragons)
        highest_dragons = [card for card in dragons if card.cost == max_cost]
        
        if highest_dragons:
            # 随机抽取一张最高费用的龙牌
            highest = self.game.random.choice(highest_dragons)
            yield ForceDraw(CONTROLLER, highest)


class TOY_714:
    """飞速离架 - Flying Off the Shelves
    Deal $1 damage to all enemy minions. Repeat for each Dragon in your hand.
    对所有敌方随从造成$1点伤害。你手牌中每有一张龙牌，重复一次。
    """
    # 3费法术
    # 效果：对所有敌方随从造成1点伤害，手牌中每有一张龙牌重复一次
    
    def play(self):
        # 计算手牌中龙牌的数量
        dragons_in_hand = (FRIENDLY_HAND + DRAGON).eval(self.game, self)
        dragon_count = len(dragons_in_hand)
        
        # 至少执行一次，然后每有一张龙牌额外执行一次
        times = 1 + dragon_count
        
        for _ in range(times):
            yield Hit(ENEMY_MINIONS, 1)


class MIS_305:
    """产品延期 - Product Recall
    <b>Discover</b> and summon a minion that costs (8) or more. It's <b>Dormant</b> for 2 turns.
    <b>发现</b>并召唤一个法力值消耗大于或等于（8）点的随从，并使其<b>休眠</b>2回合。
    """
    # 4费法术
    # 效果：发现并召唤8费+随从，休眠2回合
    
    def play(self):
        # 发现一个费用>=8的随从
        cards = yield DISCOVER(RandomCollectible(type=CardType.MINION, cost=Cost(8, INF)))
        
        if cards:
            # 召唤发现的随从
            minion = yield Summon(CONTROLLER, cards[0])
            
            if minion:
                # 使其休眠2回合
                # 使用 SetDormant action
                yield SetDormant(minion[0], 2)


class TOY_380:
    """黏土巢母 - Clay Matriarch
    <b>Miniaturize</b>
    <b>Taunt</b>. <b>Deathrattle:</b> Summon a 4/4 <b>Elusive</b> Whelp.
    <b>微缩</b>
    <b>嘲讽</b>。<b>亡语：</b>召唤一条4/4并具有<b>扰魔</b>的雏龙。
    """
    # 6费 3/7 龙 微缩+嘲讽
    # 亡语：召唤4/4扰魔雏龙
    taunt = True
    
    def deathrattle(self):
        # 召唤4/4扰魔雏龙 Token
        yield Summon(CONTROLLER, "TOY_380t2")


# EPIC

class TOY_388:
    """粉笔美术家 - Chalk Artist
    <b>Battlecry:</b> Draw a minion. Transform it into a random <b>Legendary</b> minion <i>(keeping its original stats and Cost)</i>.
    <b>战吼：</b>抽一张随从牌，将其变形成为随机<b>传说</b>随从牌<i>（保留其原始属性值和法力值消耗）</i>。
    """
    # 4费 4/3 随从
    # 战吼：抽随从牌，变形为传说随从（保留原始属性和费用）
    
    def play(self):
        # 抽一张随从牌
        drawn = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION)
        
        if drawn:
            card = drawn[0]
            # 保存原始属性（基础属性，不是当前属性）
            original_atk = card.data.atk if hasattr(card.data, 'atk') else card.atk
            original_health = card.data.health if hasattr(card.data, 'health') else card.max_health
            original_cost = card.cost
            
            # 变形为随机传说随从
            legendary_id = yield RandomCollectible(type=CardType.MINION, rarity=Rarity.LEGENDARY)
            if legendary_id:
                yield Morph(card, legendary_id)
                
                # 设置为原始属性值和费用
                # 使用 SetTag 确保属性正确设置
                yield SetTag(card, {
                    GameTag.ATK: original_atk,
                    GameTag.HEALTH: original_health,
                    GameTag.COST: original_cost
                })


class TOY_879:
    """重新打包 - Repackage
    Put all minions into a (2)-Cost box and shuffle it into your opponent's deck.
    将所有随从封入一个法力值消耗为（2）的箱子，然后将其洗入对手的牌库。
    """
    # 7费法术
    # 效果：将所有随从封入箱子，洗入对手牌库
    
    def play(self):
        # 获取所有场上的随从
        all_minions = (ALL_MINIONS).eval(self.game, self)
        
        if not all_minions:
            return
        
        # 创建箱子 Token
        box = yield Give(OPPONENT, "TOY_879t")
        
        if box:
            # 在箱子上记录所有随从的ID
            # 使用自定义属性存储随从列表
            box[0].stored_minions = [minion.id for minion in all_minions]
            
            # 移除所有随从
            for minion in all_minions:
                yield Destroy(minion)
            
            # 将箱子洗入对手牌库
            yield Shuffle(OPPONENT, box[0])


# LEGENDARY

class TOY_383:
    """重封者拉兹 - Raz, the Resealer
    <b>Battlecry:</b> Shuffle 5 copies of random friendly minions that died this game into your deck. They cost (0).
    <b>战吼：</b>将本局对战中死亡的5个随机友方随从的复制洗入你的牌库，其法力值消耗为（0）点。
    """
    # 5费 5/5 传说随从
    # 战吼：洗入5个死亡友方随从复制，费用为0
    
    def play(self):
        # 获取本局对战中死亡的友方随从
        dead_minions = self.controller.graveyard
        friendly_dead_minions = [card for card in dead_minions if card.type == CardType.MINION]
        
        if not friendly_dead_minions:
            return
        
        # 随机选择5个（如果不足5个则全选）
        count = min(5, len(friendly_dead_minions))
        selected = self.game.random.sample(friendly_dead_minions, count)
        
        for minion in selected:
            # 创建复制
            copy = yield Give(CONTROLLER, minion.id)
            
            if copy:
                # 设置费用为0
                yield Buff(copy[0], "TOY_383e")
                # 洗入牌库
                yield Shuffle(CONTROLLER, copy[0])


class TOY_385:
    """时空扭曲者扎里米 - Timewinder Zarimi
    <b>Battlecry:</b> Once per game. If you've played 8 other Dragons, take an extra turn.
    <b>战吼：</b>每局对战限一次。如果你使用过8张其他龙牌，获得一个额外回合。
    """
    # 5费 4/6 龙 传说随从
    # 战吼：每局限一次，打出8张其他龙牌后获得额外回合
    
    def play(self):
        # 检查是否已经使用过此效果
        if getattr(self.controller, 'toy_385_used', False):
            return
        
        # 计算本局对战中打出的龙牌数量（不包括自己）
        # 检查墓地和场上的龙（参考 ONY_005 卡扎库杉的实现）
        dragons_played = sum(
            1 for card in self.controller.graveyard + list(self.controller.field)
            if hasattr(card, 'race') and card.race == Race.DRAGON
            and card.id != self.id
        )
        
        # 也需要检查 races 属性（多种族）
        dragons_played += sum(
            1 for card in self.controller.graveyard + list(self.controller.field)
            if hasattr(card, 'races') and Race.DRAGON in card.races
            and card.id != self.id
            and not (hasattr(card, 'race') and card.race == Race.DRAGON)  # 避免重复计数
        )
        
        if dragons_played >= 8:
            # 标记已使用
            self.controller.toy_385_used = True
            # 获得额外回合
            yield ExtraTurn(CONTROLLER)


# ========================================
# Buff 定义
# ========================================

class TOY_384e:
    """净化之力增益 - Purified Strength Buff
    +1/+2
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
    }


class MIS_919e:
    """木偶剧场增益 - Puppet Theatre Buff
    Set to 1/1, costs (1)
    """
    # 设置为1/1，费用为1
    # atk, max_health, cost 会在运行时动态设置
    pass




class TOY_383e:
    """重封者拉兹增益 - Raz Buff
    Costs (0)
    """
    tags = {GameTag.COST: 0}

