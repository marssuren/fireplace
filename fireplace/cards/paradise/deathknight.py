"""
胜地历险记 - DEATHKNIGHT
"""
from ..utils import *


# COMMON

class VAC_427:
    """甜筒殡淇淋 - Corpsicle
    Deal $3 damage. Spend 3 Corpses to return this to your hand at the end of your turn.
    造成$3点伤害。消耗3份<b>残骸</b>，在你的回合结束时将本牌移回你的手牌。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}

    def play(self):
        yield Hit(TARGET, 3)

        # 消耗3份残骸并添加回手效果
        if self.controller.corpses >= 3:
            yield SpendCorpses(CONTROLLER, 3)
            # 给玩家添加一个 buff，在回合结束时将本法术从墓地移回手牌
            # 使用 Give 创建一个新的复制，因为原卡会进入墓地
            yield Buff(CONTROLLER, "VAC_427e")

class VAC_427e:
    """甜筒殡淇淋回手效果 (Player Enchantment)"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

    # 在回合结束时，给玩家一张新的 VAC_427
    events = OWN_TURN_END.on(
        Give(CONTROLLER, "VAC_427"),
        Destroy(SELF)
    )


class VAC_445:
    """食尸鬼之夜 - Ghouls' Night
    Summon five 1/1 Ghouls that attack random enemies.
    召唤五个1/1的食尸鬼并使其攻击随机敌人。
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    
    def play(self):
        # 召唤5个食尸鬼
        ghouls = yield Summon(CONTROLLER, "VAC_445t", 5)
        
        # 让每个召唤出来的食尸鬼攻击随机敌人
        # 注意：ghouls 可能是 None
        if ghouls:
            for ghoul in ghouls:
                # 正确获取敌方角色（随从+英雄）
                targets = list(self.controller.opponent.field) + [self.controller.opponent.hero]
                targets = [t for t in targets if t and not getattr(t, 'dead', False)]
                if targets:
                    target = self.game.random.choice(targets)
                    # 强制攻击
                    yield Attack(ghoul, target)


class VAC_514:
    """恐惧猎犬训练师 - Dreadhound Handler
    Rush. Deathrattle: Summon a 1/1 Dreadhound with Reborn.
    突袭。亡语：召唤一只1/1并具有复生的恐惧猎犬。
    """
    mechanics = [GameTag.RUSH, GameTag.DEATHRATTLE]
    deathrattle = Summon(CONTROLLER, "VAC_514t")


class WORK_010:
    """行程保安 - Travel Security
    Taunt. Deathrattle: Summon a random 8-Cost minion.
    嘲讽。亡语：随机召唤一个法力值消耗为（8）的随从。
    """
    mechanics = [GameTag.TAUNT, GameTag.DEATHRATTLE]
    deathrattle = Summon(CONTROLLER, RandomCollectible(cost=8, type=CardType.MINION))


class WORK_070:
    """灵魂检索 - Soul Searching
    Discover a card from your deck. Spend 5 Corpses to copy it.
    从你的牌库中发现一张牌。消耗5份残骸，复制发现的牌。
    """
    def play(self):
        # 从牌库中发现一张牌
        # 使用 DISCOVER 从牌库中选择
        cards = yield DISCOVER(FRIENDLY_DECK)

        if cards:
            # 发现的牌会自动加入手牌
            # 如果消耗了5份残骸，再给一张复制
            if self.controller.corpses >= 5:
                yield SpendCorpses(CONTROLLER, 5)
                # 复制发现的牌
                yield Give(CONTROLLER, Copy(cards[0]))


# RARE

class VAC_425:
    """大地之末号 - Horizon's Edge
    Deal 3 damage randomly split among all enemies. After a friendly minion dies, reopen this.
    造成3点伤害，随机分配到所有敌人身上。在一个友方随从死亡后，重新开启本地标。
    """
    # Location 默认有 Activate 能力
    def activate(self):
        # 造成3点伤害，随机分配
        for _ in range(3):
            targets = self.game.board.get_enemies(self.controller)
            if targets:
                target = self.game.random.choice(targets)
                yield Hit(target, 1)

    # 监听友方随从死亡事件
    events = Death(FRIENDLY_MINIONS).after(
        # Reopen: 重置 exhausted 和 cooldown?
        # 对于 Location，重置意味着可以再次激活
        Refresh(SELF)
        # 如果有 cooldown 属性，也可能需要重置，Refresh 通常包含这个
    )


class VAC_429:
    """滑雪高手 - Snow Shredder
    Costs (1) if a character is Frozen.
    如果有被冻结的角色，则法力值消耗为（1）点。
    """
    # 使用 Hand Aura 实现条件费用
    class Hand:
        # 当场上有冻结角色时，费用变为 1
        def cost_func(self, i):
            # 检查场上是否有冻结的角色
            if self.owner.game.board.filter(ALL_CHARACTERS + FROZEN):
                return 1
            return None  # 返回 None 表示不修改费用


class VAC_436:
    """脆骨海盗 - Brittlebone Buccaneer
    Whenever you play a Deathrattle minion, give it Reborn.
    每当你使用一张亡语随从牌时，使其获得复生。
    """
    # 监听打出亡语随从
    events = Play(CONTROLLER, MINION + DEATHRATTLE).after(
        lambda self, player, played_card, target=None: played_card.deathrattles and Buff(played_card, "VAC_436e")
    )

class VAC_436e:
    """复生 Buff"""
    tags = {
        GameTag.REBORN: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class WORK_028:
    """无限滞留 - Eternal Layover
    Give ALL minions Reborn, then destroy all minions.
    使所有随从获得复生，然后消灭所有随从。
    """
    def play(self):
        # 给所有随从复生
        for minion in self.game.board.filter(ALL_MINIONS):
            yield Buff(minion, "WORK_028e")
        # 消灭所有随从
        yield Destroy(ALL_MINIONS)

class WORK_028e:
    """复生 Buff"""
    tags = {
        GameTag.REBORN: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


# EPIC

class VAC_402:
    """霜噬海盗 - Frostbitten Freebooter
    Deathrattle: Freeze 3 random enemies. Any that were already Frozen take 5 damage instead.
    亡语：随机冻结3个敌人，已被冻结的敌人改为受到5点伤害。
    """
    mechanics = [GameTag.DEATHRATTLE]

    def deathrattle(self):
        # 选择3个随机敌方角色（包括英雄和随从）
        enemies = self.game.board.filter(ENEMY_CHARACTERS)
        count = min(3, len(enemies))
        if count > 0:
            targets = self.game.random.sample(enemies, count)
            for target in targets:
                if target.frozen:
                    yield Hit(target, 5)
                else:
                    yield Freeze(target)


class VAC_513:
    """滑坡 - Slippery Slope
    Freeze a character. Draw a card for each Frozen character.
    冻结一个角色。每有一个被冻结的角色，抽一张牌。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    def play(self):
        # 冻结目标
        yield Freeze(TARGET)
        
        # 统计冻结角色
        # 注意：board 是 CardList，不能使用 filter(selector)
        frozen_count = 0
        for player in self.game.players:
            if player.hero and getattr(player.hero, 'frozen', False):
                frozen_count += 1
            for minion in player.field:
                if getattr(minion, 'frozen', False):
                    frozen_count += 1
        
        # 抽牌
        if frozen_count > 0:
            yield Draw(CONTROLLER) * frozen_count


# LEGENDARY

class VAC_426:
    """伊丽扎·刺刃 - Eliza Goreblade
    Deathrattle: For the rest of the game, your minions have +1 Attack.
    亡语：在本局对战的剩余时间内，你的随从拥有+1攻击力。
    """
    mechanics = [GameTag.DEATHRATTLE]
    deathrattle = Buff(CONTROLLER, "VAC_426e")

class VAC_426e:
    """伊丽扎·刺刃 Buff (Player Aura)
    "For the rest of the game" 效果影响所有区域的随从
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

    # 对所有友方随从生效的永久 Aura（手牌、牌库、场上）
    update = Refresh(FRIENDLY_MINIONS)

    class Hand:
        # 手牌中的随从获得 +1 攻击力
        def atk(self, i):
            return i + 1

    class Deck:
        # 牌库中的随从获得 +1 攻击力
        def atk(self, i):
            return i + 1

    class Board:
        # 场上的随从获得 +1 攻击力
        def atk(self, i):
            return i + 1


class VAC_437:
    """扣子 - Buttons
    Battlecry: Draw a spell of each spell school.
    战吼：抽取每个派系的法术牌各一张。
    """
    mechanics = [GameTag.BATTLECRY]

    def play(self):
        # 遍历所有派系，从牌库中抽取对应派系的法术
        schools = [
            SpellSchool.ARCANE,
            SpellSchool.FIRE,
            SpellSchool.FROST,
            SpellSchool.NATURE,
            SpellSchool.HOLY,
            SpellSchool.SHADOW,
            SpellSchool.FEL
        ]

        for school in schools:
            # 使用 ForceDraw 从牌库中随机抽取对应派系的法术
            # 注意：使用 getattr 安全访问 spell_school，因为某些卡牌可能没有这个属性
            spells = [c for c in self.controller.deck if c.type == CardType.SPELL and getattr(c, 'spell_school', None) == school]
            if spells:
                # 随机选择一张并使用 ForceDraw 抽取
                card = self.game.random.choice(spells)
                yield ForceDraw(card)
