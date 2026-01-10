"""纳斯利亚堡的悬案（Murder at Castle Nathria）卡牌实现"""
from ..utils import *


class MAW_024:
    """Dew Process - 私法程序
    [x]For the rest of the game, players draw an extra card at the start of their turn.
    在本局对战的剩余时间内，玩家会在其回合开始时额外抽一张牌。
    """
    # 给双方玩家添加永久buff，每回合开始时额外抽一张牌
    def play(self):
        yield Buff(FRIENDLY_HERO, "MAW_024e")
        yield Buff(ENEMY_HERO, "MAW_024e")


class MAW_024e:
    """Dew Process Effect - 私法程序效果"""
    # 回合开始时额外抽一张牌
    events = OWN_TURN_BEGIN.on(Draw(CONTROLLER))


class MAW_025:
    """Attorney-at-Maw - 噬渊律师
    <b>Choose One -</b> <b>Silence</b> a minion; or Give a minion <b>Immune</b> this turn.
    <b>抉择：</b><b>沉默</b>一个随从；或者使一个随从在本回合中获得<b>免疫</b>。
    """
    # 抉择：沉默或免疫
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    choose = ["MAW_025a", "MAW_025b"]


class MAW_025a:
    """Silence - 沉默"""
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Silence(TARGET)


class MAW_025b:
    """Immune - 免疫"""
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Buff(TARGET, "MAW_025be")


class MAW_025be:
    """Immune this turn"""
    tags = {GameTag.IMMUNE: True}
    events = TURN_END.on(Destroy(SELF))


class MAW_026:
    """Incarceration - 监禁
    [x]Choose a minion. It goes <b>Dormant</b> for 3 turns.
    选择一个随从。使其<b>休眠</b>3回合。
    """
    # 使目标随从休眠3回合
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = SetTags(TARGET, {GameTag.DORMANT: 3})


class REV_307:
    """Natural Causes - 自然死亡
    Deal $2 damage. Summon a 2/2 Treant.
    造成$2点伤害。召唤一个2/2的树人。
    """
    # 造成2点伤害并召唤树人
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}

    def play(self):
        yield Hit(TARGET, 2)
        yield Summon(CONTROLLER, "REV_307t")


class REV_310:
    """Death Blossom Whomper - 死亡之花践踏者
    <b>Battlecry:</b> Draw a <b>Deathrattle</b> minion and gain its <b>Deathrattle.</b>
    战吼：抽一张<b>亡语</b>随从牌并获得其<b>亡语</b>。
    """
    # 战吼：抽一张亡语随从并复制其亡语
    def play(self):
        # 抽一张亡语随从
        card = yield Draw(CONTROLLER, FRIENDLY_DECK + MINION + DEATHRATTLE)
        # 如果成功抽到，复制其亡语
        if card and hasattr(card, 'deathrattle'):
            # 给自己添加复制的亡语buff
            yield Buff(SELF, CopyDeathrattleBuff(card, "REV_310e"))


class REV_311:
    """Nightshade Bud - 夜影花蕾
    <b>Choose One - </b><b>Discover</b> a minion from your deck to summon; or a spell to cast.
    <b>抉择：</b>从你的牌库中<b>发现</b>一张随从牌并召唤；或者一张法术牌并施放。
    """
    # 抉择：发现并召唤随从，或发现并施放法术
    choose = ["REV_311a", "REV_311b"]


class REV_311a:
    """Summon a minion - 召唤随从"""
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}

    def play(self):
        # 从牌库中发现一张随从并召唤
        card = yield Discover(CONTROLLER, FRIENDLY_DECK + MINION)
        if card:
            yield Summon(CONTROLLER, card)


class REV_311b:
    """Cast a spell - 施放法术"""
    def play(self):
        # 从牌库中发现一张法术并施放
        card = yield Discover(CONTROLLER, FRIENDLY_DECK + SPELL)
        if card:
            yield CastSpell(card)


class REV_313:
    """Planted Evidence - 安插证据
    <b>Discover</b> a spell. It costs (2) less this turn.
    <b>发现</b>一张法术牌。在本回合中，其法力值消耗减少（2）点。
    """
    # 发现一张德鲁伊法术，并在本回合减费2点
    def play(self):
        # 发现一张德鲁伊法术
        card = yield Discover(CONTROLLER, RandomSpell(card_class=CardClass.DRUID))
        # 给发现的卡牌添加临时减费buff
        if card:
            yield Buff(card, "REV_313e")


class REV_313e:
    """Planted Evidence Buff - 安插证据减费"""
    tags = {GameTag.COST: -2}
    events = TURN_END.on(Destroy(SELF))


class REV_314:
    """Topior the Shrubbagazzor - 灌木巨龙托匹奥
    [x]<b>Battlecry:</b> For the rest of the game, after you cast a Nature spell, summon a 3/3 Whelp with <b>Rush</b>.
    战吼：在本局对战的剩余时间内，在你施放一个自然法术后，召唤一条3/3并具有<b>突袭</b>的雏龙。
    """
    # 战吼：给控制者添加永久buff，施放自然法术后召唤雏龙
    play = Buff(FRIENDLY_HERO, "REV_314e")


class REV_314e:
    """Topior Effect - 托匹奥效果"""
    # 施放自然法术后，召唤一条3/3突袭雏龙
    events = Play(CONTROLLER, SPELL + NATURE).after(Summon(CONTROLLER, "REV_314t"))


class REV_318:
    """Widowbloom Seedsman - 孀花播种者
    [x]<b>Battlecry:</b> Draw a Nature spell. Gain an empty Mana Crystal.
    战吼：抽一张自然法术牌。获得一个空的法力水晶。
    """
    # 战吼：抽一张自然法术，并获得一个空的法力水晶
    def play(self):
        # 抽一张自然法术
        yield Draw(CONTROLLER, FRIENDLY_DECK + SPELL + NATURE)
        # 获得一个空的法力水晶
        yield GainEmptyMana(CONTROLLER, 1)


class REV_319:
    """Sesselie of the Fae Court - 法夜朝臣瑟赛莉
    [x]<b>Taunt</b>, <b>Deathrattle</b>: Draw a minion. Reduce its Cost by (8).
    <b>嘲讽</b>，<b>亡语：</b>抽一张随从牌，并使其法力值消耗减少（8）点。
    """
    # 亡语：抽一张随从并减费8点
    def deathrattle(self):
        # 抽一张随从
        card = yield Draw(CONTROLLER, FRIENDLY_DECK + MINION)
        # 给抽到的随从减费8点
        if card:
            yield Buff(card, "REV_319e")


class REV_319e:
    """Sesselie Buff - 瑟赛莉减费"""
    tags = {GameTag.COST: -8}


class REV_333:
    """Hedge Maze - 树篱迷宫
    Trigger a friendly minion's <b>Deathrattle</b>.
    触发一个友方随从的<b>亡语</b>。
    """
    # Location地标：触发友方随从的亡语
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0}
    play = Deathrattle(TARGET)


class REV_336:
    """Plot of Sin - 罪恶谋划
    [x]Summon two 2/2 Treants. <b>Infuse (5):</b> Two 5/5 Ancients instead.
    召唤两个2/2的树人。<b>注能（5）：</b>改为两个5/5的古树。
    """
    # 注能机制：需要5个友方随从死亡
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    infuse = 5

    def play(self):
        if self.infused:
            # 注能后：召唤两个5/5的古树
            yield Summon(CONTROLLER, "REV_336t2") * 2
        else:
            # 未注能：召唤两个2/2的树人
            yield Summon(CONTROLLER, "REV_336t") * 2


class REV_365:
    """Convoke the Spirits - 万灵之召
    [x]Cast 8 random Druid spells <i>(targets chosen randomly)</i>.
    随机施放8个德鲁伊法术<i>（目标随机而定）</i>。
    """
    # 随机施放8个德鲁伊法术
    def play(self):
        for _ in range(8):
            yield CastSpell(RandomSpell(card_class=CardClass.DRUID))


# Token 定义

class REV_307t:
    """Treant - 树人
    2/2 token"""
    tags = {GameTag.CARDTYPE: CardType.MINION}


class REV_310e:
    """Death Blossom Whomper Deathrattle - 死亡之花践踏者亡语"""
    # 复制的亡语buff（由CopyDeathrattleBuff动态创建）
    pass


class REV_314t:
    """Whelp - 雏龙
    3/3 Rush token"""
    tags = {GameTag.CARDTYPE: CardType.MINION, GameTag.RUSH: True}


class REV_336t:
    """Treant - 树人
    2/2 token"""
    tags = {GameTag.CARDTYPE: CardType.MINION}


class REV_336t2:
    """Ancient - 古树
    5/5 token"""
    tags = {GameTag.CARDTYPE: CardType.MINION}


