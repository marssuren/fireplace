"""纳斯利亚堡的悬案（Murder at Castle Nathria）法师卡牌实现"""
from ..utils import *


# ========== Volatile Skeleton Token 定义 ==========

class REV_505t:
    """Volatile Skeleton - 不稳定的骷髅
    2/2 亡灵
    亡语：对所有随从造成2点伤害。
    """
    # Token属性在CardDefs.xml中定义
    # 亡语：对所有随从造成2点伤害
    deathrattle = Hit(ALL_MINIONS, 2)


# ========== 简单卡牌实现 ==========

class MAW_013:
    """Life Sentence - 终身刑罚
    Remove a minion from the game.
    从游戏中移除一个随从。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = (Silence(TARGET), Destroy(TARGET))


class REV_505:
    """Cold Case - 冰冷案例
    Summon two 2/2 Volatile Skeletons. Gain 4 Armor.
    召唤两个2/2的不稳定骷髅。获得4点护甲值。
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}

    def play(self):
        yield Summon(CONTROLLER, "REV_505t") * 2
        yield GainArmor(FRIENDLY_HERO, 4)


class REV_601:
    """Frozen Touch - 冰冻之触
    Deal $3 damage.
<b>Infuse (3):</b> Add a Frozen Touch to your hand.
    造成$3点伤害。<b>注能（3）：</b>将一张冰冻之触置入你的手牌。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    infuse = 3

    def play(self):
        yield Hit(TARGET, 3)
        if self.infused:
            yield Give(CONTROLLER, "REV_601")


class REV_602:
    """Nightcloak Sanctum - 夜隐者圣所
    <b>Freeze</b> a minion. Summon a 2/2 Volatile Skeleton.
    <b>冻结</b>一个随从。召唤一个2/2的不稳定骷髅。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self):
        yield Freeze(TARGET)
        yield Summon(CONTROLLER, "REV_505t")


class MAW_101:
    """Contract Conjurer - 契约咒术师
    Costs (3) less for each <b>Secret</b> you control.
    你每控制一个<b>奥秘</b>，本牌的法力值消耗便减少（3）点。
    """
    cost_mod = lambda self, i: -3 * len([s for s in self.controller.secrets if s.zone == Zone.SECRET])


# ========== 奥秘卡牌 ==========

class MAW_006:
    """Objection! - 异议
    <b>Secret:</b> When your opponent plays a minion, <b>Counter</b> it.
    <b>奥秘：</b>当你的对手打出一张随从牌时，<b>反制</b>它。
    """
    secret = True
    events = Play(OPPONENT, MINION).on(Counter(Play.CARD), Reveal(SELF))


class REV_516:
    """Vengeful Visage - 复仇之像
    [x]<b>Secret:</b> After an enemy
minion attacks your hero,
summon a copy of it to
attack the enemy hero.
    <b>奥秘：</b>在一个敌方随从攻击你的英雄后，召唤它的一个复制并攻击敌方英雄。
    """
    secret = True

    def _trigger(self, attacker, defender=None):
        # 召唤攻击者的复制
        copy = yield Summon(CONTROLLER, ExactCopy(attacker))
        if copy:
            # 让复制攻击敌方英雄
            yield Attack(copy, ENEMY_HERO)
        yield Reveal(SELF)

    events = Attack(ENEMY_MINIONS, FRIENDLY_HERO).after(_trigger)


# ========== 复杂卡牌 ==========

class REV_504:
    """Solid Alibi - 脱罪力证
    Until your next turn, your hero can only take 1 damage at a time.
    直到你的下个回合，你的英雄每次只会受到1点伤害。
    """
    play = Buff(FRIENDLY_HERO, "REV_504e")


class REV_504e:
    """Solid Alibi Effect - 脱罪力证效果"""
    # 限制英雄每次只受到1点伤害
    max_health_damage = 1
    events = OWN_TURN_BEGIN.on(Destroy(SELF))


class REV_513:
    """Chatty Bartender - 健谈的调酒师
    [x]At the end of your turn,
if you control a <b>Secret</b>,
deal 2 damage to
all enemies.
    在你的回合结束时，如果你控制一个<b>奥秘</b>，对所有敌人造成2点伤害。
    """
    def _trigger_if_has_secret(self, player):
        # 检查是否控制奥秘
        if len(self.controller.secrets) > 0:
            yield Hit(ENEMY_CHARACTERS, 2)

    events = OWN_TURN_END.on(_trigger_if_has_secret)


class REV_840:
    """Deathborne - 死神之躯
    Deal $2 damage to all minions. Summon a 2/2 Volatile Skeleton
for each killed.
    对所有随从造成$2点伤害。每消灭一个随从，便召唤一个2/2的不稳定骷髅。
    """
    def play(self):
        # 使用事件追踪死亡的随从数量
        killed_count = 0

        # 获取所有随从
        all_minions = ALL_MINIONS.eval(self.game, self.controller)

        # 对所有随从造成2点伤害
        yield Hit(ALL_MINIONS, 2)

        # 计算死亡的随从数量
        for minion in all_minions:
            if minion.dead:
                killed_count += 1

        # 召唤相应数量的骷髅
        for _ in range(killed_count):
            yield Summon(CONTROLLER, "REV_505t")


class REV_514:
    """Kel'Thuzad, the Inevitable - 天定之灾克尔苏加德
    [x]<b>Battlecry:</b> Resurrect your
Volatile Skeletons. Any that
can't fit on the battlefield
instantly explode!
    <b>战吼：</b>复活你的不稳定骷髅。无法放置在战场上的骷髅会立即爆炸！
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}

    def play(self):
        # 获取所有死亡的不稳定骷髅
        # 使用DSL选择器获取死亡的骷髅
        dead_skeletons = (FRIENDLY + KILLED + MINION + ID("REV_505t")).eval(self.game, self.controller)

        for skeleton in dead_skeletons:
            # 检查是否有空位
            if len(self.controller.field) < 7:
                # 有空位，复活骷髅
                yield Summon(CONTROLLER, Copy(skeleton))
            else:
                # 没有空位，触发爆炸效果（对所有随从造成2点伤害）
                yield Hit(ALL_MINIONS, 2)


class REV_515:
    """Orion, Mansion Manager - 豪宅管家俄里翁
    After a friendly <b>Secret</b> is revealed, cast a different Mage <b>Secret</b> and gain +2/+2.
    在一个友方<b>奥秘</b>被揭示后，施放一个不同的法师<b>奥秘</b>并获得+2/+2。
    """
    def _on_secret_revealed(self, secret):
        # 施放一个不同的法师奥秘
        # 排除刚刚揭示的奥秘
        yield CastSpell(RandomSecret(card_class=CardClass.MAGE, exclude=secret.card_id))
        # 获得+2/+2
        yield Buff(SELF, "REV_515e")

    events = Reveal(FRIENDLY + SECRET).on(_on_secret_revealed)


class REV_515e:
    """Orion Buff - 俄里翁强化"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
    }
    health = 2


class REV_000:
    """Suspicious Alchemist - 可疑的炼金师
    [x]<b>Battlecry:</b> <b>Discover</b> a
spell. If your opponent
guesses your choice,
they get a copy.
    <b>战吼：</b>从法师法术中<b>发现</b>一张。如果你的对手猜中了你的选择，他们会获得一张复制。
    """
    # 使用 DiscoverWithPendingGuess 实现完整的"对手猜测"机制
    # 流程：
    # 1. 玩家发现一张法师法术（从3个选项中选择）
    # 2. 记录选项和选择到对手的 pending_guesses 队列
    # 3. 在对手回合开始时，对手AI从相同选项中猜测
    # 4. 如果猜中，对手也获得一张复制
    play = DiscoverWithPendingGuess(CONTROLLER, RandomSpell(card_class=CardClass.MAGE))

