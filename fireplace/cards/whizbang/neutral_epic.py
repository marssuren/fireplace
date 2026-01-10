"""
威兹班的工坊 - 中立 - EPIC
"""
from ..utils import *


class MIS_916:
    """高端玩家 - Pro Gamer
    [x]Battlecry: Challenge your opponent to a game of Rock-Paper-Scissors! The winner draws 2 cards.
    战吼：向你的对手发起挑战，玩一场剪刀石头布！胜者抽两张牌。
    """
    # 2费 2/3 中立随从
    # 官方数据：战吼效果，双方各选择一个选项（石头/布/剪刀），胜者抽两张牌
    # 实现方式：双方同时选择，然后判断胜负
    # 来源：Dr. Boom's Incredible Inventions 迷你包

    def play(self):
        # 玩家选择石头、布或剪刀
        player_choice = yield GenericChoice(CONTROLLER, ["MIS_916a", "MIS_916b", "MIS_916c"])

        # 对手选择石头、布或剪刀
        opponent_choice = yield GenericChoice(OPPONENT, ["MIS_916a", "MIS_916b", "MIS_916c"])

        if not player_choice or not opponent_choice:
            return

        player_card = player_choice[0]
        opponent_card = opponent_choice[0]

        # 判断胜负
        # MIS_916a = 石头（Rock）- 赢剪刀
        # MIS_916b = 布（Paper）- 赢石头
        # MIS_916c = 剪刀（Scissors）- 赢布

        player_wins = False
        opponent_wins = False

        if player_card == "MIS_916a" and opponent_card == "MIS_916c":  # 石头赢剪刀
            player_wins = True
        elif player_card == "MIS_916b" and opponent_card == "MIS_916a":  # 布赢石头
            player_wins = True
        elif player_card == "MIS_916c" and opponent_card == "MIS_916b":  # 剪刀赢布
            player_wins = True
        elif opponent_card == "MIS_916a" and player_card == "MIS_916c":  # 对手石头赢剪刀
            opponent_wins = True
        elif opponent_card == "MIS_916b" and player_card == "MIS_916a":  # 对手布赢石头
            opponent_wins = True
        elif opponent_card == "MIS_916c" and player_card == "MIS_916b":  # 对手剪刀赢布
            opponent_wins = True

        # 胜者抽两张牌
        if player_wins:
            yield Draw(CONTROLLER) * 2
        elif opponent_wins:
            yield Draw(OPPONENT) * 2
        # 平局则无人抽牌


class TOY_341:
    """恋旧的小丑 - Nostalgic Clown
    [x]Miniaturize Battlecry: If you've played a higher Cost card while holding this, deal 4 damage.
    微缩。战吼：如果你在本牌在你手中时使用过法力值消耗更高的牌，造成4点伤害。
    """
    # 5费 6/5 中立随从
    # 官方数据：Miniaturize 机制由核心引擎自动处理
    # 战吼：条件伤害 - 需要追踪本牌在手中时是否使用过更高费用的牌
    # 实现方式：在手牌时监听打出事件，记录是否满足条件

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}

    class Hand:
        """在手牌时追踪是否使用过更高费用的牌"""
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # 初始化追踪标记
            if not hasattr(self, 'higher_cost_played'):
                self.higher_cost_played = False

        # 监听控制者打出卡牌
        events = Play(CONTROLLER).after(lambda self, source: self._check_higher_cost(source))

        def _check_higher_cost(self, played_card):
            """检查打出的牌是否费用更高"""
            if played_card.cost > self.cost:
                self.higher_cost_played = True

    def play(self):
        # 检查是否满足条件
        if getattr(self, 'higher_cost_played', False):
            # 造成4点伤害
            yield Hit(TARGET, 4)


class TOY_530:
    """游乐巨人 - Playhouse Giant
    Costs (1) less for each card you've drawn this game.
    在本局对战中你每抽过一张牌，本牌的法力值消耗便减少（1）点。
    """
    # 25费 8/8 机械 中立随从
    # 官方数据：根据本局游戏抽牌数量减费
    # 实现方式：需要在 Player 中添加全局抽牌计数器
    # 注意：这里使用的是本局游戏的总抽牌数，不是本回合的抽牌数


    cost_mod = lambda self, i: -self.controller.cards_drawn_this_game


class TOY_601:
    """工厂装配机 - Factory Assemblybot
    Miniaturize At the end of your turn, summon a 6/7 Bot that attacks a random enemy.
    微缩。在你的回合结束时，召唤一个6/7的机器人并使其攻击一个随机敌人。
    """
    # 10费 6/7 机械 中立随从
    # 官方数据：Miniaturize 机制由核心引擎自动处理
    # 回合结束时召唤一个 6/7 机器人（TOY_601t1）并使其攻击随机敌人

    events = TurnEnd(CONTROLLER).on(
        Summon(CONTROLLER, "TOY_601t1"),
        # 召唤后立即攻击随机敌人
        # 使用 Find 找到刚召唤的机器人，然后让它攻击
        lambda self: self._attack_random_enemy()
    )

    def _attack_random_enemy(self):
        """让刚召唤的机器人攻击随机敌人"""
        # 找到场上最后一个友方随从（刚召唤的）
        if self.controller.field:
            bot = self.controller.field[-1]
            # 找到随机敌方目标
            enemies = self.controller.opponent.field + [self.controller.opponent.hero]
            valid_enemies = [e for e in enemies if e.can_be_attacked_by(bot)]
            if valid_enemies:
                target = self.game.random.choice(valid_enemies)
                yield Attack(bot, target)


class TOY_866:
    """通道沉眠者 - Corridor Sleeper
    Starts Dormant. After 7 minions die, awaken.
    起始休眠状态。在7个随从死亡后唤醒。
    """
    # 7费 9/9 野兽 中立随从
    # 官方数据：起始休眠，在7个随从死亡后唤醒
    # 实现方式：使用 dormant 标签和 PROGRESS 计数器

    dormant = True

    # 监听任意随从死亡（包括双方）
    events = Death(MINION).on(
        UpdateProgress(SELF, 1),
        If(Attr(SELF, GameTag.PROGRESS) >= 7, Awaken(SELF))
    )


class TOY_896:
    """折纸巨龙 - Origami Dragon
    [x]Divine Shield, Lifesteal Battlecry: Swap stats with another minion.
    圣盾，吸血。战吼：与另一个随从交换属性值。
    """
    # 6费 1/1 龙 中立随从
    # 官方数据：圣盾、吸血关键字，战吼交换属性
    # 实现方式：交换攻击力和生命值
    # 注意：交换后保留圣盾和吸血关键字

    divine_shield = True
    lifesteal = True
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self):
        # 与目标随从交换属性值
        if TARGET:
            # 保存当前属性
            my_atk = self.atk
            my_health = self.health
            target_atk = TARGET.atk
            target_health = TARGET.health

            # 交换属性 - 使用 Buff 设置新的属性值
            yield Buff(self, "TOY_896e", atk_value=target_atk, health_value=target_health)
            yield Buff(TARGET, "TOY_896e", atk_value=my_atk, health_value=my_health)


class TOY_896e:
    """属性交换 Buff - Swapped Stats"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

    def __init__(self, *args, atk_value=0, health_value=0, **kwargs):
        super().__init__(*args, **kwargs)
        self._atk_value = atk_value
        self._health_value = health_value

    def apply(self, target):
        """设置为固定的属性值"""
        # 设置攻击力为固定值
        target.tags[GameTag.ATK] = self._atk_value
        # 设置生命值为固定值
        target.tags[GameTag.HEALTH] = self._health_value


