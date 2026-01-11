"""纳斯利亚堡的悬案（Murder at Castle Nathria）猎人卡牌实现"""
from ..utils import *


# ========== Wildseed Token 定义 ==========
# 参考: https://hearthstonetopdecks.com, https://wiki.gg

class REV_360t:
    """Fox Spirit Wildseed - 狐灵野种
    1费 3/1 野兽+亡灵
    休眠1回合。苏醒时获得突袭。
    """
    # Token属性在CardDefs.xml中定义
    pass


class REV_360t2:
    """Bear Spirit Wildseed - 熊灵野种
    2费 2/5 野兽+亡灵
    休眠2回合。苏醒时获得嘲讽。
    """
    # Token属性在CardDefs.xml中定义
    pass


class REV_360t3:
    """Stag Spirit Wildseed - 鹿灵野种
    3费 5/4 野兽
    休眠3回合。苏醒时装备一把巨弓。
    """
    # Token属性在CardDefs.xml中定义
    pass


# ========== 简单卡牌实现 ==========

class REV_356:
    """Batty Guest - 狂蝠来宾
    <b>Deathrattle:</b> Summon a 2/1 Bat.
    <b>亡语：</b>召唤一只2/1的蝙蝠。
    """
    deathrattle = Summon(CONTROLLER, "REV_356t")


class REV_356t:
    """Bat - 蝙蝠
    2/1 野兽 token
    """
    pass


class REV_364:
    """Stag Charge - 雄鹿冲锋
    Deal $3 damage. Summon a random <b>Dormant</b> Wildseed.
    造成$3点伤害。召唤一个随机的<b>休眠</b>野种。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}

    def play(self):
        yield Hit(TARGET, 3)
        # 随机召唤一个野种（Fox/Bear/Stag）
        yield Summon(CONTROLLER, RandomID("REV_360t", "REV_360t2", "REV_360t3"))


class REV_362:
    """Castle Kennels - 城堡狗舍
    [x]Give a friendly minion
+2 Attack. If it's a
Beast, give it <b>Rush</b>.
    给一个友方随从+2攻击力。如果是野兽，使其获得<b>突袭</b>。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self):
        yield Buff(TARGET, "REV_362e")
        if TARGET.race == Race.BEAST:
            yield Buff(TARGET, "REV_362e2")


class REV_362e:
    """Castle Kennels Buff - 城堡狗舍攻击加成"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
    }


class REV_362e2:
    """Castle Kennels Rush - 城堡狗舍突袭"""
    tags = {GameTag.RUSH: True}


# ========== Wildseed 相关卡牌 ==========

class REV_360:
    """Spirit Poacher - 灵体偷猎者
    <b>Battlecry:</b> Summon a random <b>Dormant</b> Wildseed.
    <b>战吼：</b>召唤一个随机的<b>休眠</b>野种。
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, RandomID("REV_360t", "REV_360t2", "REV_360t3"))


class REV_363:
    """Ara'lon - 艾拉隆
    <b>Battlecry:</b> Summon one of each <b>Dormant</b> Wildseed.
    <b>战吼：</b>召唤每种<b>休眠</b>野种各一个。
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}

    def play(self):
        # 召唤全部3种野种
        yield Summon(CONTROLLER, "REV_360t")
        yield Summon(CONTROLLER, "REV_360t2")
        yield Summon(CONTROLLER, "REV_360t3")


class REV_361:
    """Wild Spirits - 野性之魂
    [x]Summon two different
<b>Dormant</b> Wildseeds.
Make your Wildseeds
awaken 1 turn sooner.
    召唤两个不同的<b>休眠</b>野种。使你的野种提前1回合苏醒。
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}

    def play(self):
        # 召唤第一个随机野种
        first = yield Summon(CONTROLLER, RandomID("REV_360t", "REV_360t2", "REV_360t3"))
        if first:
            yield Buff(first, "REV_361e")

        # 召唤第二个不同的野种
        # 根据第一个野种的ID，排除它并从剩余的中随机选择
        remaining = []
        if first:
            all_seeds = ["REV_360t", "REV_360t2", "REV_360t3"]
            remaining = [s for s in all_seeds if s != first.card_id]
        else:
            remaining = ["REV_360t", "REV_360t2", "REV_360t3"]

        if remaining:
            # 使用 RandomID 而不是 RANDOM
            second = yield Summon(CONTROLLER, RandomID(*remaining))
            if second:
                yield Buff(second, "REV_361e")


class REV_361e:
    """Wild Spirits Buff - 野性之魂加速苏醒"""
    # 减少1回合休眠时间
    # 这个buff在召唤时应用，修改DORMANT标签
    def apply(self, target):
        if target.tags.get(GameTag.DORMANT, 0) > 0:
            target.tags[GameTag.DORMANT] -= 1


# ========== Infuse 卡牌 ==========

class REV_350:
    """Frenzied Fangs - 狂暴利齿
    Summon two 2/1 Bats.
<b>Infuse (3):</b> Give them +1/+2.
    召唤两只2/1的蝙蝠。<b>注能（3）：</b>使其获得+1/+2。
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    infuse = 3

    def play(self):
        if self.infused:
            # 注能后：召唤两只3/3的蝙蝠
            for _ in range(2):
                minion = yield Summon(CONTROLLER, "REV_350t")
                if minion:
                    yield Buff(minion, "REV_350e")
        else:
            # 未注能：召唤两只2/1的蝙蝠
            yield Summon(CONTROLLER, "REV_350t") * 2


class REV_350t:
    """Bat - 蝙蝠
    2/1 野兽 token
    """
    pass


class REV_350e:
    """Frenzied Fangs Buff - 狂暴利齿强化"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
    }
    health = 2


class REV_352:
    """Stonebound Gargon - 石缚加尔贡
    [x]<b>Rush</b>
<b>Infuse (3):</b> Also damages
the minions next to
  whomever this attacks.
    <b>突袭</b>。<b>注能（3）：</b>攻击时也会对相邻随从造成伤害。
    """
    infuse = 3

    def play(self):
        if self.infused:
            # 注能后：获得劈砍效果
            yield Buff(SELF, "REV_352e")


class REV_352e:
    """Stonebound Gargon Infused - 石缚加尔贡注能"""
    # 攻击时对相邻随从造成伤害（类似CLEAVE）
    events = Attack(OWNER).on(Hit(ADJACENT(Attack.DEFENDER), ATK(OWNER)))


class MAW_009:
    """Shadehound - 影犬
    [x]Whenever this attacks, give
your other Beasts +2/+2.
<b>Infuse (3 Beasts):</b>
Gain <b>Rush</b>.
    攻击时，使你的其他野兽获得+2/+2。<b>注能（3个野兽）：</b>获得<b>突袭</b>。
    """
    # 使用 infuse_race 属性限制只计数野兽死亡
    infuse = 3
    infuse_race = Race.BEAST  # ⭐ 只计数野兽死亡
    events = Attack(OWNER).on(Buff(FRIENDLY_MINIONS + BEAST - SELF, "MAW_009e"))

    def play(self):
        if self.infused:
            yield Buff(SELF, "MAW_009e2")


class MAW_009e:
    """Shadehound Buff - 影犬强化"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
    }
    health = 2


class MAW_009e2:
    """Shadehound Rush - 影犬突袭"""
    tags = {GameTag.RUSH: True}


# ========== 复杂卡牌 ==========

class REV_353:
    """Huntsman Altimor - 猎手阿尔迪莫
    [x]<b>Battlecry:</b> Summon a
Gargon Companion.
<b>Infuse (3):</b> Summon another.
 <b>Infuse (6):</b> And another!
    <b>战吼：</b>召唤一个加尔贡伙伴。<b>注能（3）：</b>再召唤一个。<b>注能（6）：</b>再召唤一个！
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    infuse = 3

    def play(self):
        # 基础：召唤1个加尔贡
        yield Summon(CONTROLLER, "REV_353t")

        # 注能3+：再召唤1个
        if self.tags.get(GameTag.INFUSE_COUNTER, 0) >= 3:
            yield Summon(CONTROLLER, "REV_353t")

        # 注能6+：再召唤1个
        if self.tags.get(GameTag.INFUSE_COUNTER, 0) >= 6:
            yield Summon(CONTROLLER, "REV_353t")


class REV_353t:
    """Gargon Companion - 加尔贡伙伴
    2/4 野兽 token
    """
    pass


class MAW_010:
    """Motion Denied - 否决动议
    [x]<b>Secret:</b> After your
opponent plays three cards
in a turn, deal $6 damage
to the enemy hero.
    <b>奥秘：</b>在你的对手于一个回合中打出三张牌后，对敌方英雄造成$6点伤害。
    """
    secret = True

    # 使用自定义方法追踪对手打出的牌数
    def _on_opponent_play(self, source, player, card):
        # 在奥秘上使用TAG_SCRIPT_DATA_NUM_1追踪计数
        count = self.tags.get(GameTag.TAG_SCRIPT_DATA_NUM_1, 0) + 1
        self.tags[GameTag.TAG_SCRIPT_DATA_NUM_1] = count

        # 如果达到3张，触发奥秘
        if count >= 3:
            yield Hit(ENEMY_HERO, 6)
            yield Reveal(SELF)

    def _reset_counter(self, source):
        # 回合开始时重置计数器
        self.tags[GameTag.TAG_SCRIPT_DATA_NUM_1] = 0

    events = [
        Play(OPPONENT).after(_on_opponent_play),
        OWN_TURN_BEGIN.on(_reset_counter)
    ]


class MAW_011:
    """Defense Attorney Nathanos - 辩护律师纳萨诺斯
    [x]<b>Battlecry:</b> <b>Discover</b> a friendly
<b>Deathrattle</b> minion that died
this game. Gain its <b>Deathrattle</b>
and then trigger it.
    <b>战吼：</b>从本局对战中死亡的友方<b>亡语</b>随从中<b>发现</b>一张。获得其<b>亡语</b>并触发。
    """
    def play(self):
        # 从死亡的友方亡语随从中发现
        card = yield Discover(CONTROLLER, FRIENDLY + KILLED + MINION + DEATHRATTLE)
        if card and hasattr(card, 'deathrattle'):
            # 复制亡语
            yield Buff(SELF, CopyDeathrattleBuff(card, "MAW_011e"))
            # 立即触发亡语
            yield Deathrattle(SELF)


class MAW_011e:
    """Defense Attorney Nathanos Deathrattle - 辩护律师纳萨诺斯亡语"""
    pass


class REV_369:
    """Collateral Damage - 间接伤害
    [x]Deal $6 damage to three
random enemy minions.
Excess damage hits
the enemy hero.
    对三个随机敌方随从造成$6点伤害。超出的伤害会对敌方英雄造成伤害。
    """
    def play(self):
        # 对3个随机敌方随从造成6点伤害，超出伤害打脸
        for _ in range(3):
            # 使用DSL随机选择敌方随从
            target = yield RANDOM(ENEMY_MINIONS)
            if target:
                original_health = target.health
                yield Hit(target, 6)
                # 如果目标死亡，计算超出伤害并打脸
                if target.dead:
                    excess = 6 - original_health
                    if excess > 0:
                        yield Hit(ENEMY_HERO, excess)
