"""
威兹班的工坊 - HUNTER
"""
from ..utils import *


# COMMON

class TOY_352:
    """抛接嬉戏 - Fetch!
    Draw a minion. If it's a Beast, draw a spell.
    """
    # 1费法术 抽一张随从牌。如果是野兽牌，抽一张法术牌
    # 官方数据：条件抽牌
    
    def play(self):
        # 抽一张随从牌
        cards = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION)
        
        # 检查抽到的牌是否为野兽
        if cards:
            drawn_card = cards[0]
            if drawn_card.race == Race.BEAST:
                # 如果是野兽，再抽一张法术牌
                yield ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL)


class TOY_356:
    """玩具暴龙 - Toy T-Rex
    Rush Deathrattle: Deal 7 damage to a random enemy.
    """
    # 7费 7/7 野兽 突袭。亡语：随机对一个敌人造成7点伤害
    # 官方数据：Rush + 随机伤害亡语
    rush = True
    
    def deathrattle(self):
        # 随机对一个敌人造成7点伤害
        yield Hit(RANDOM_ENEMY_CHARACTER, 7)


class TOY_358:
    """遥控骨 - Remote Control Bone
    After your hero attacks, summon a 1/1 Hound.
    """
    # 2费 1/3 武器 在你的英雄攻击后，召唤一只1/1的猎犬
    # 官方数据：英雄攻击触发效果
    
    events = Attack(FRIENDLY_HERO).after(Summon(CONTROLLER, "TOY_358t"))


class MIS_105:
    """折价包 - Bargain Bin
    Secret: After your opponent plays a minion, spell, or weapon, draw one of the other two.
    """
    # 2费奥秘 在你的对手使用一张随从，法术或武器牌后，你抽取其余两种类型的牌各一张
    # 官方数据：奥秘，根据对手打出的牌类型抽牌
    secret = True
    
    events = [
        # 对手打出随从牌，抽法术和武器
        Play(OPPONENT, MINION).after(
            Reveal(SELF),
            ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL),
            ForceDraw(CONTROLLER, FRIENDLY_DECK + WEAPON)
        ),
        # 对手打出法术牌，抽随从和武器
        Play(OPPONENT, SPELL).after(
            Reveal(SELF),
            ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION),
            ForceDraw(CONTROLLER, FRIENDLY_DECK + WEAPON)
        ),
        # 对手打出武器牌，抽随从和法术
        Play(OPPONENT, WEAPON).after(
            Reveal(SELF),
            ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION),
            ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL)
        ),
    ]


# RARE

class TOY_350:
    """漆彩帆布鸟 - Painted Canvasaur
    Battlecry: Give each other friendly Beast a random bonus effect.
    """
    # 2费 3/3 野兽 战吼：使每只其他友方野兽各获得一项随机额外效果
    # 官方数据：给其他野兽添加随机 Buff
    # 
    # 【随机额外效果】官方数据验证的8种效果：
    # - 嘲讽 (Taunt)
    # - 风怒 (Windfury)
    # - 圣盾 (Divine Shield)
    # - 剧毒 (Poisonous)
    # - 扰魔 (Elusive)
    # - 突袭 (Rush)
    # - 吸血 (Lifesteal)
    # - 复生 (Reborn)
    
    def play(self):
        # 获取所有其他友方野兽
        beasts = (FRIENDLY_MINIONS + BEAST - SELF).eval(self.game, self)
        
        # 为每只野兽添加随机 Buff
        for beast in beasts:
            # 随机选择一个 Buff（8种效果）
            buffs = ["TOY_350e1", "TOY_350e2", "TOY_350e3", "TOY_350e4", "TOY_350e5", "TOY_350e6", "TOY_350e7", "TOY_350e8"]
            buff_id = yield RandomChoice(buffs)
            if buff_id:
                yield Buff(beast, buff_id[0])


class TOY_350e1:
    """圣盾 Buff"""
    tags = {
        GameTag.DIVINE_SHIELD: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_350e2:
    """嘲讽 Buff"""
    tags = {
        GameTag.TAUNT: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_350e3:
    """突袭 Buff"""
    tags = {
        GameTag.RUSH: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_350e4:
    """剧毒 Buff"""
    tags = {
        GameTag.POISONOUS: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_350e5:
    """风怒 Buff"""
    tags = {
        GameTag.WINDFURY: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_350e6:
    """吸血 Buff"""
    tags = {
        GameTag.LIFESTEAL: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_350e7:
    """扰魔 Buff"""
    tags = {
        GameTag.CANT_BE_TARGETED_BY_SPELLS: True,
        GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_350e8:
    """复生 Buff"""
    tags = {
        GameTag.REBORN: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_353:
    """拼布好朋友 - Patchwork Pals
    Get all 3 Animal Companions. They cost (1) less.
    """
    # 2费法术 获取全部3种动物伙伴，其法力值消耗减少（1）点
    # 官方数据：获取3种动物伙伴（米莎、霍弗、雷欧克）
    # 动物伙伴 ID：NEW1_032（米莎）、NEW1_033（雷欧克）、NEW1_034（霍弗）
    
    def play(self):
        # 获取3种动物伙伴
        companions = ["NEW1_032", "NEW1_033", "NEW1_034"]
        for companion_id in companions:
            card = yield Give(CONTROLLER, companion_id)
            if card:
                # 添加费用减少 Buff
                yield Buff(card, "TOY_353e")


class TOY_353e:
    """拼布 Buff - 费用减少"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    cost_mod = -1


class TOY_359:
    """丛林乐园 - Jungle Gym
    Deal 1 damage to a random enemy. Repeat for each friendly Beast.
    """
    # 2费地标 2耐久 随机对一个敌人造成1点伤害。每有一只友方野兽，重复一次
    # 官方数据：Location 类型，伤害次数基于友方野兽数量
    
    def activate(self):
        # 计算友方野兽数量
        beast_count = COUNT(FRIENDLY_MINIONS + BEAST)
        
        # 造成伤害，次数 = 1 + 野兽数量
        for _ in range(beast_count.eval(self.game, self) + 1):
            yield Hit(RANDOM_ENEMY_CHARACTER, 1)


# EPIC

class TOY_351:
    """神秘的蛋 - Mysterious Egg
    Miniaturize Deathrattle: Get a copy of a random Beast in your deck. It costs (3) less.
    """
    # 4费 0/3 微缩。亡语：获取你牌库中一张随机野兽牌的一张复制，其法力值消耗减少（3）点
    # 官方数据：Miniaturize 机制由核心引擎自动处理，生成 1费 1/1 的 TOY_351t
    
    def deathrattle(self):
        # 从牌库中随机获取一张野兽牌
        beasts_in_deck = FRIENDLY_DECK + BEAST
        beasts = beasts_in_deck.eval(self.game, self)
        
        if beasts:
            # 随机选择一张野兽
            beast = yield RandomChoice(beasts)
            if beast:
                # 获取复制
                card = yield Give(CONTROLLER, beast[0].id)
                if card:
                    # 添加费用减少 Buff
                    yield Buff(card, "TOY_351e1")


class TOY_351e1:
    """孵化完毕 Buff - 费用减少"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    cost_mod = -3


class TOY_354:
    """遥控狂潮 - Remote Control Swarm
    Summon six 1/1 Hounds. For each that doesn't fit, give the others +1/+1.
    """
    # 5费法术 召唤六只1/1的猎犬。每有一只放不下的猎犬，使其余猎犬获得+1/+1
    # 官方数据：场地空间检查，溢出的猎犬转化为 Buff
    # 召唤的是 R.C. Hound（TOY_358t），双种族（野兽+机械）
    
    def play(self):
        # 计算场地剩余空间
        board_space = 7 - COUNT(FRIENDLY_MINIONS).eval(self.game, self)
        
        # 召唤猎犬（最多召唤 board_space 只）
        hounds_summoned = min(6, board_space)
        summoned_hounds = []
        for _ in range(hounds_summoned):
            hound = yield Summon(CONTROLLER, "TOY_358t")  # 使用正确的 R.C. Hound Token
            if hound:
                summoned_hounds.append(hound)
        
        # 计算溢出的猎犬数量
        overflow = 6 - hounds_summoned
        
        # 为每只溢出的猎犬，给场上的猎犬 +1/+1
        if overflow > 0:
            for _ in range(overflow):
                for hound in summoned_hounds:
                    yield Buff(hound, "TOY_354e")


class TOY_354e:
    """冲呀！Buff"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


# LEGENDARY

class TOY_355:
    """绵弹枪神赫米特 - Hermit Hammershot
    After a friendly Beast dies, get a random Legendary Beast from the past. It costs (2) less.
    """
    # 5费 3/6 传说 在一只友方野兽死亡后，随机获取一张来自过去的传说野兽牌，其法力值消耗减少（2）点
    # 官方数据：野兽死亡触发，获取随机传说野兽
    # "来自过去"指的是所有可收集的传说野兽牌
    
    events = Death(FRIENDLY + BEAST).after(
        lambda self, player: [
            # 获取随机传说野兽
            RandomCollectible(card_type=CardType.MINION, race=Race.BEAST, rarity=Rarity.LEGENDARY).then(
                lambda cards: (
                    # 给予卡牌并添加费用减少 Buff
                    Give(CONTROLLER, cards[0]).then(
                        lambda given_cards: Buff(given_cards[0], "TOY_355e2") if given_cards else None
                    )
                ) if cards else None
            )
        ]
    )


class TOY_355e2:
    """绵弹之力 Buff - 费用减少"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    cost_mod = -2


class TOY_357:
    """抱龙王噗鲁什 - Plush Bear Plushy
    Battlecry: If your opponent has 15 or less Health, return all other minions to their owner's deck and gain Charge.
    """
    # 9费 6/6 野兽 传说 战吼：如果你对手的生命值小于或等于15点，将所有其他随从移回其拥有者的牌库，并获得冲锋
    # 官方数据：条件清场 + 获得冲锋
    
    def play(self):
        # 检查对手生命值
        if self.controller.opponent.hero.health <= 15:
            # 将所有其他随从移回牌库
            minions = (ALL_MINIONS - SELF).eval(self.game, self)
            for minion in minions:
                yield Bounce(minion)
            
            # 获得冲锋
            yield Buff(SELF, "TOY_357e")


class TOY_357e:
    """冲锋 Buff"""
    tags = {
        GameTag.CHARGE: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class MIS_914:
    """量产泰迪 - Mass Production
    Battlecry: Recast each friendly Secret that has been triggered this game.
    """
    # 5费 4/4 传说 机械+野兽 战吼：再次施放本局对战中触发过的每个友方奥秘
    # 官方数据：双种族，重新施放已触发的奥秘
    # 
    # 【核心引擎扩展】使用 controller.triggered_secrets 列表追踪触发过的奥秘
    # 这个属性在 Player 类的 __init__ 中初始化
    # 在 Reveal action 中自动记录触发的奥秘ID
    
    def play(self):
        # 获取本局对战中触发过的奥秘列表
        if hasattr(self.controller, "triggered_secrets") and self.controller.triggered_secrets:
            for secret_id in self.controller.triggered_secrets:
                # 重新施放奥秘（创建卡牌并直接放入奥秘区域）
                secret = self.controller.card(secret_id, source=self)
                secret.zone = Zone.SECRET


# MINI SET

class MIS_104:
    """狂野的卡牌包 - Wild Pack of Cards
    Put 5 random Beasts into your hand. They're temporary.
    """
    # 1费法术 随机将五张野兽牌置入你的手牌。这些牌是临时牌
    # 官方数据：随机野兽 + 临时标记（回合结束时弃掉）
    
    def play(self):
        # 随机获取5张野兽牌
        for _ in range(5):
            card = yield RandomCollectible(card_type=CardType.MINION, race=Race.BEAST)
            if card:
                # 给予手牌
                given_card = yield Give(CONTROLLER, card[0])
                if given_card:
                    # 添加临时标记
                    yield Buff(given_card, "MIS_104e")


class MIS_104e:
    """山寨卡牌 Buff - 回合结束时弃掉"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_ONE_TURN_EFFECT: True
    }
    
    # 在控制者的回合结束时弃掉（临时卡牌机制）
    # 注意：只在玩家自己的回合结束时触发，不是对手回合
    events = TurnEnd(CONTROLLER).on(
        lambda self: Discard(OWNER) if self.owner.controller.current_player else None
    )
