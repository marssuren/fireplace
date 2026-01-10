from ..utils import *
from fireplace.enums import LIFESTEAL_DAMAGES_ENEMY


##
# Minions

class DMF_217:
    """Line Hopper (越线的游客)
    Your Outcast cards cost (1) less."""
    # 3费 3/4 - 你的流放牌法力值消耗减少(1)点

    update = Refresh(FRIENDLY_HAND + Attr(GameTag.OUTCAST, True), {GameTag.COST: -1})


class DMF_222:
    """Redeemed Pariah (获救的流民)
    After you play an Outcast card, gain +1/+1."""
    # 2费 2/3 - 在你打出一张流放牌后，获得+1/+1

    events = Play(FRIENDLY + Attr(GameTag.OUTCAST, True)).after(Buff(SELF, "DMF_222e"))


class DMF_222e:
    """Redeemed (获救)"""
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}


class DMF_223:
    """Renowned Performer (知名表演者)
    Rush Deathrattle: Summon two 1/1 Assistants with Taunt."""
    # 4费 3/3 突袭，亡语：召唤两个1/1并具有嘲讽的助理

    deathrattle = Summon(CONTROLLER, "DMF_223t") * 2


class DMF_223t:
    """Assistant (助理)"""
    # 1/1 嘲讽 - 属性在CardDefs.xml中定义
    pass


class DMF_226:
    """Bladed Lady (刀锋舞娘)
    Rush Costs (1) if your hero has 6 or more Attack."""
    # 6费 6/6 突袭 - 如果你的英雄拥有6点或以上攻击力，法力值消耗为(1)点

    update = (ATK(FRIENDLY_HERO) >= 6) & Refresh(SELF, {GameTag.COST: SET(1)})


class DMF_229:
    """Stiltstepper (高跷艺人)
    Battlecry: Draw a card. If you play it this turn, give your hero +4 Attack this turn."""
    # 3费 4/1 - 战吼：抽一张牌。如果你在本回合中使用这张牌，使你的英雄在本回合中获得+4攻击力

    play = Draw(CONTROLLER).then(Buff(Draw.CARD, "DMF_229e_tracker"))


class DMF_229e_tracker:
    """Stiltstepper Tracker"""
    # 附在抽到的卡牌上的buff，当打出时触发效果
    events = [
        Play(OWNER).on(
            Buff(FRIENDLY_HERO, "DMF_229e_hero"),
            Destroy(SELF)
        ),
        OWN_TURN_END.on(Destroy(SELF))
    ]


class DMF_229e_hero:
    """High Steps (高超舞步)"""
    tags = {GameTag.ATK: 4}
    events = REMOVED_IN_PLAY


class DMF_230:
    """Il'gynoth (伊格诺斯)
    Lifesteal Your Lifesteal damages the enemy hero instead of healing you."""
    # 4费 2/6 吸血 - 你的吸血改为对敌方英雄造成伤害

    update = Refresh(CONTROLLER, {LIFESTEAL_DAMAGES_ENEMY: 1})


class DMF_231:
    """Zai, the Incredible (扎依，出彩艺人)
    Battlecry: Copy the left- and right-most cards in your hand."""
    # 5费 5/3 - 战吼：复制你手牌中最左边和最右边的牌

    def play(self):
        hand = self.controller.hand
        if not hand:
            return

        leftmost = hand[0]
        rightmost = hand[-1]

        yield Give(CONTROLLER, Copy(leftmost) + Copy(rightmost))


class DMF_247:
    """Insatiable Felhound (贪食地狱犬)
    Taunt Corrupt: Gain +1/+1 and Lifesteal."""
    # 3费 2/5 嘲讽 - 腐蚀：获得+1/+1和吸血

    corrupt = Buff(SELF, "DMF_247e")


class DMF_247e:
    """Corrupted (已腐蚀)"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.LIFESTEAL: True,
    }


class DMF_248:
    """Felsteel Executioner (魔钢处决者)
    Corrupt: Become a weapon."""
    # 3费 4/3 - 腐蚀：变成一把武器

    corrupt = Morph(SELF, "DMF_248t")


class DMF_248t:
    """Felsteel Executioner (魔钢处决者)"""
    # 3费 4/3 武器
    pass


class YOP_002:
    """Felsaber (邪刃豹)
    Can only attack if your hero attacked this turn."""
    # 4费 5/6 - 在本回合中，除非你的英雄进行过攻击，否则无法进行攻击

    update = (NUM_ATTACKS_THIS_TURN(FRIENDLY_HERO) == 0) & Refresh(SELF, {GameTag.CANT_ATTACK: True})


##
# Spells

class DMF_219:
    """Relentless Pursuit (冷酷追杀)
    Give your hero +4 Attack and Immune this turn."""
    # 3费 - 本回合中，使你的英雄获得+4攻击力和免疫

    play = Buff(FRIENDLY_HERO, "DMF_219e")


class DMF_219e:
    """Relentless Pursuit"""
    tags = {
        GameTag.ATK: 4,
        GameTag.IMMUNE: True,
    }
    events = REMOVED_IN_PLAY


class DMF_221:
    """Felscream Blast (邪吼冲击)
    Lifesteal. Deal $1 damage to a minion and its neighbors."""
    # 1费 吸血 - 对一个随从及其相邻随从造成1点伤害
    tags = {GameTag.LIFESTEAL: True}

    play = Hit(TARGET + TARGET_ADJACENT, 1)


class DMF_224:
    """Expendable Performers (演员大接力)
    Summon seven 1/1 Illidari with Rush. If they all die this turn, summon seven more."""
    # 7费 - 召唤七个1/1并具有突袭的伊利达雷。如果他们在本回合中全部死亡，则再次召唤七个

    def play(self):
        # 召唤7个伊利达雷，并给每个添加追踪标记
        for _ in range(7):
            yield Summon(CONTROLLER, "DMF_224t").then(
                Buff(Summon.MINION, "DMF_224e_marker")
            )
        
        # 给控制器添加追踪buff，监听这批随从的死亡
        yield Buff(CONTROLLER, "DMF_224e_tracker")


class DMF_224t:
    """Illidari (伊利达雷)"""
    # 1/1 突袭 - 属性在CardDefs.xml中定义
    pass


class DMF_224e_marker:
    """Expendable Performer Marker"""
    # 标记这是演员大接力召唤的随从
    tags = {GameTag.TAG_SCRIPT_DATA_NUM_1: 1}


class DMF_224e_tracker:
    """Expendable Performers Tracker"""
    # 追踪本批次召唤的7个伊利达雷的死亡情况
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.summoned_count = 7  # 召唤的总数
        self.died_count = 0      # 已死亡的数量
    
    # 监听带有标记的随从死亡
    events = [
        Death(FRIENDLY_MINIONS + Attr(GameTag.TAG_SCRIPT_DATA_NUM_1, 1)).on(
            lambda self, source, target: setattr(self, 'died_count', getattr(self, 'died_count', 0) + 1)
        ),
        # 回合结束时检查是否全部死亡
        OWN_TURN_END.on(
            lambda self, player: (
                [Summon(CONTROLLER, "DMF_224t") for _ in range(7)],
                Destroy(SELF)
            ) if getattr(self, 'died_count', 0) >= 7 else Destroy(SELF)
        )
    ]


class DMF_225:
    """Throw Glaive (投掷利刃)
    Deal $2 damage to a minion. If it dies, add a Temporary copy of this to your hand."""
    # 1费 - 对一个随从造成2点伤害。如果该随从死亡，则将一张本牌的临时复制置入你的手牌

    def play(self):
        yield Hit(TARGET, 2)
        # 如果目标死亡，给一张临时复制
        if Dead(TARGET):
            yield Give(CONTROLLER, Copy(SELF)).then(
                Buff(Give.CARD, "DMF_225e_temporary")
            )


class DMF_225e_temporary:
    """Temporary Copy Marker"""
    # 临时复制标记，回合结束时移除
    events = OWN_TURN_END.on(Discard(OWNER))


class DMF_249:
    """Acrobatics (空翻杂技)
    Draw 2 cards. If you play both this turn, draw 2 more."""
    # 3费 - 抽两张牌。如果你在本回合中使用这两张牌，再抽两张

    def play(self):
        # 抽两张牌，并给每张添加追踪buff
        yield Draw(CONTROLLER).then(Buff(Draw.CARD, "DMF_249e_card1"))
        yield Draw(CONTROLLER).then(Buff(Draw.CARD, "DMF_249e_card2"))
        
        # 给控制器添加追踪buff
        yield Buff(CONTROLLER, "DMF_249e_tracker")


class DMF_249e_card1:
    """Acrobatics Card 1 Marker"""
    # 标记第一张抽到的牌
    tags = {GameTag.TAG_SCRIPT_DATA_NUM_1: 1}
    
    # 打出时通知追踪器
    events = [
        Play(OWNER).on(
            lambda self, source: setattr(self.controller, '_acrobatics_card1_played', True)
        ),
        OWN_TURN_END.on(Destroy(SELF))
    ]


class DMF_249e_card2:
    """Acrobatics Card 2 Marker"""
    # 标记第二张抽到的牌
    tags = {GameTag.TAG_SCRIPT_DATA_NUM_1: 2}
    
    # 打出时通知追踪器
    events = [
        Play(OWNER).on(
            lambda self, source: setattr(self.controller, '_acrobatics_card2_played', True)
        ),
        OWN_TURN_END.on(Destroy(SELF))
    ]


class DMF_249e_tracker:
    """Acrobatics Tracker"""
    # 追踪两张牌是否都打出
    
    # 回合结束时检查
    events = OWN_TURN_END.on(
        lambda self, player: (
            [Draw(CONTROLLER) for _ in range(2)],
            Destroy(SELF)
        ) if (
            getattr(player, '_acrobatics_card1_played', False) and 
            getattr(player, '_acrobatics_card2_played', False)
        ) else Destroy(SELF)
    )


class YOP_001:
    """Illidari Studies (伊利达雷研习)
    Discover an Outcast card. Your next one costs (1) less."""
    # 1费 - 发现一张流放牌。你的下一张流放牌法力值消耗减少(1)点

    play = Discover(CONTROLLER, RandomCollectible(outcast=True)).then(
        Buff(CONTROLLER, "YOP_001e")
    )


class YOP_001e:
    """Illidari Studies Buff"""
    # 下一张流放牌减费
    update = Refresh(FRIENDLY_HAND + Attr(GameTag.OUTCAST, True), {GameTag.COST: -1})
    events = Play(FRIENDLY + Attr(GameTag.OUTCAST, True)).on(Destroy(SELF))


##
# Weapons

class DMF_227:
    """Dreadlord's Bite (恐惧魔王之咬)
    Outcast: Deal 1 damage to all enemies."""
    # 3费 3/2 - 流放：对所有敌人造成1点伤害

    outcast = Hit(ENEMY_CHARACTERS, 1)
