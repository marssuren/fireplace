"""
决战荒芜之地 - 中立 - EPIC
"""
from ..utils import *


class DEEP_035:
    """炫彩旋岩虫 - Iridescent Gyreworm
    Deathrattle: Give each of your minions a random Bonus Effect.
    亡语：使你的每个随从各获得一项随机额外效果。
    """
    deathrattle = Buff(FRIENDLY_MINIONS, "DEEP_035e")


class DEEP_035e:
    """随机额外效果 - Random Bonus Effect"""
    def apply(self, target):
        # 随机给予一个关键字效果：冲锋、圣盾、嘲讽、吸血、风怒、突袭等
        import random
        bonus_effects = [
            {GameTag.CHARGE: True},
            {GameTag.DIVINE_SHIELD: True},
            {GameTag.TAUNT: True},
            {GameTag.LIFESTEAL: True},
            {GameTag.WINDFURY: True},
            {GameTag.RUSH: True},
        ]
        effect = random.choice(bonus_effects)
        for tag, value in effect.items():
            target.tags[tag] = value


class WW_025:
    """艾泽里特巨人 - Azerite Giant
    [x]Costs (1) less for each turn in a row you've played an Elemental.
    每有一个你使用过元素牌的连续的回合，本牌的法力值消耗便减少（1）点。
    """
    def cost_func(self, value):
        # 根据连续回合使用元素牌的次数减费
        consecutive_turns = getattr(self.controller, 'elemental_streak', 0)
        return value - consecutive_turns


class WW_333:
    """交际鱼人 - Howdyfin
    [x]Whenever your hand has less than 3 cards in it, get a random Murloc.
    每当你的手牌少于三张，随机获取一张鱼人牌。
    """
    events = [
        Play(CONTROLLER).after(lambda self, source, *args: self._check_hand()),
        Draw(CONTROLLER).after(lambda self, source, *args: self._check_hand()),
        Discard(CONTROLLER).after(lambda self, source, *args: self._check_hand()),
    ]

    def _check_hand(self):
        # 检查手牌数量是否少于3张
        if len(self.controller.hand) < 3:
            yield Give(CONTROLLER, RandomCollectible(race=Race.MURLOC))


class WW_351:
    """偷牛贼 - Cattle Rustler
    Battlecry: Draw a Beast. It costs (3) less.
    战吼：抽一张野兽牌，其法力值消耗减少（3）点。
    """
    def play(self):
        # 抽一张野兽牌
        cards = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + BEAST)
        # 给抽到的野兽牌减费
        if cards:
            for card in cards:
                if card:
                    yield Buff(card, "WW_351e")


class WW_351e:
    """减费增益 - Cost Reduction"""
    tags = {GameTag.COST: -3}


class WW_420:
    """食人魔帮王牌 - Ogre-Gang Ace
    [x]Rush Whenever this attacks, gain Divine Shield. <i>(50% chance to gain Lifesteal instead.)</i>
    突袭。每当本随从攻击时，获得圣盾。（50%的几率改为获得吸血。）
    """
    events = Attack(SELF).on(
        COINFLIP & SetTags(SELF, {GameTag.DIVINE_SHIELD: True}) | SetTags(SELF, {GameTag.LIFESTEAL: True})
    )


class WW_431:
    """枪尾蛇 - Gattlesnake
    [x]At the end of your turn, load two bullets that deal 1 damage each. Deathrattle: Fire at random enemies!
    在你的回合结束时，装填两发枪弹，每发可以造成1点伤害。亡语：随机对敌人开火！
    """
    events = OWN_TURN_END

    def OWN_TURN_END(self):
        # 每回合结束时装填2发子弹
        # 使用 tags 存储子弹数量
        current_bullets = self.tags.get(GameTag.TAG_SCRIPT_DATA_NUM_1, 0)
        self.tags[GameTag.TAG_SCRIPT_DATA_NUM_1] = current_bullets + 2

    def deathrattle(self):
        # 亡语：发射所有子弹
        bullet_count = self.tags.get(GameTag.TAG_SCRIPT_DATA_NUM_1, 0)
        for _ in range(bullet_count):
            yield Hit(RANDOM_ENEMY_CHARACTER, 1)
