"""
深暗领域 - WARRIOR
"""
from ..utils import *


# COMMON

class GDB_226:
    """凶恶的入侵者 - Hostile Invader
    Battlecry, Spellburst, and Deathrattle: Deal 2 damage to all other minions.

    3费 3/3 战士随从 - 恶魔
    <b>战吼，<b>法术迸发</b>，亡语：</b>对所有其他随从造成2点伤害。
    """
    race = Race.DEMON

    # 战吼：对所有其他随从造成2点伤害
    def play(self):
        yield Hit(ALL_MINIONS - SELF, 2)

    # 法术迸发：对所有其他随从造成2点伤害
    events = Spellburst(CONTROLLER, Hit(ALL_MINIONS - SELF, 2))

    # 亡语：对所有其他随从造成2点伤害
    def deathrattle(self):
        yield Hit(ALL_MINIONS - SELF, 2)


class GDB_228:
    """舰长日志 - Captain's Log
    Draw 2 cards. Costs (1) less for each Draenei you control.

    3费 战士法术
    抽两张牌。你每控制一个德莱尼，本牌的法力值消耗便减少（1）点。
    """
    # 动态计算费用减免
    cost_mod = lambda self, i: -len([m for m in self.controller.field if hasattr(m, 'race') and m.race == Race.DRAENEI])

    def play(self):
        # 抽两张牌
        yield Draw(CONTROLLER) * 2


class GDB_232:
    """不屈的守备官 - Unyielding Vindicator
    Battlecry: The next Draenei you play gives your hero its Attack for that turn.

    4费 5/4 战士随从 - 德莱尼
    <b>战吼：</b>你使用的下一个德莱尼会使你的英雄在当回合获得该德莱尼的攻击力。
    """
    race = Race.DRAENEI

    def play(self):
        # 给控制者添加一个buff，使下一个打出的德莱尼给予英雄攻击力
        yield Buff(CONTROLLER, "GDB_232e")


class SC_411:
    """震荡弹 - Concussive Shells
    Deal $2 damage and gain 2 Armor. Your next Starship launch costs (2) less.

    1费 战士法术
    造成$2点伤害并获得2点护甲值。你的下一次<b>星舰</b>发射的法力值消耗减少（2）点。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}

    def play(self):
        # 造成2点伤害
        yield Hit(TARGET, 2)
        # 获得2点护甲值
        yield GainArmor(FRIENDLY_HERO, 2)
        # 给控制者添加buff，使下一次星舰发射减2费
        yield Buff(CONTROLLER, "SC_411e")


# RARE

class GDB_227:
    """丢弃辎重 - Jettison
    Discover a spell. Spend 2 Armor to Discover another.

    2费 战士法术
    <b>发现</b>一张法术牌。消耗2点护甲值，再<b>发现</b>一张。
    """
    def play(self):
        # 第一次发现法术牌
        yield Discover(CONTROLLER, RandomSpell())

        # 如果有至少2点护甲值，消耗2点护甲值并再发现一张
        if self.controller.hero.armor >= 2:
            yield GainArmor(FRIENDLY_HERO, -2)
            yield Discover(CONTROLLER, RandomSpell())


class GDB_229:
    """探险队中士 - Expedition Sergeant
    [x] Battlecry: The next Draenei  you play immediately attacks a random enemy.

    3费 3/4 战士随从 - 德莱尼
    <b>战吼：</b>你使用的下一个德莱尼会立即攻击一个随机敌人。
    """
    race = Race.DRAENEI

    def play(self):
        # 给控制者添加一个buff，使下一个打出的德莱尼立即攻击随机敌人
        yield Buff(CONTROLLER, "GDB_229e")


class GDB_231:
    """晶石巨槌 - Crystalline Greatmace
    After your hero attacks, give all Draenei in your hand +2 Attack.

    2费 2/2 战士武器
    在你的英雄攻击后，使你手牌中的所有德莱尼获得+2攻击力。
    """
    # 在英雄攻击后触发
    events = Attack(FRIENDLY_HERO).after(
        Buff(FRIENDLY_HAND + DRAENEI, "GDB_231e")
    )


class SC_406:
    """大和炮 - Yamato Cannon
    [x]Starship Piece Battlecry: Destroy a random enemy minion. Also triggers on launch.

    4费 4/4 战士随从 - 星舰组件
    <b>战吼：</b>随机消灭一个敌方随从。发射时也会触发。
    <b>星舰组件</b>
    """
    # 战吼：随机消灭一个敌方随从
    def play(self):
        yield Destroy(RANDOM_ENEMY_MINION)

    # 发射时也会触发
    def launch(self):
        yield Destroy(RANDOM_ENEMY_MINION)


class SC_414:
    """雷神 - Thor
    [x]Battlecry: Deal 5 damage. <i>(Transforms if you launched a Starship this game.)</i>

    5费 5/5 战士随从 - 机械
    <b>战吼：</b>造成5点伤害。<i>（如果你在本局对战中发射过<b>星舰</b>，则会变形。）</i>
    """
    race = Race.MECHANICAL
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}

    def play(self):
        # 造成5点伤害
        if TARGET:
            yield Hit(TARGET, 5)

        # 如果发射过星舰，变形为 SC_414t
        if self.controller.starships_launched_this_game > 0:
            yield Morph(SELF, "SC_414t")


# EPIC

class GDB_230:
    """坚定的复仇者 - Stalwart Avenger
    Immune while attacking. At the end of EACH turn, swap this minion's Attack and Health.

    5费 3/6 战士随从 - 德莱尼
    攻击时<b>免疫</b>。在每个回合结束时，本随从的攻击力和生命值互换。
    """
    race = Race.DRAENEI

    # 攻击时免疫（参考 VAC_410t 实现）
    events = Attack(SELF).on(
        Buff(SELF, "GDB_230e")
    )

    # 在每个回合结束时，交换攻击力和生命值
    update = TURN_END.on(SwapStats(SELF))


class GDB_233:
    """矮人矮行星 - Dwarf Planet
    Fill your board with random 2-Cost minions that attack random enemies.

    10费 战士法术
    用法力值消耗为（2）的随机随从填满你的面板并使其攻击随机敌人。
    """
    def play(self):
        # 计算可以召唤的随从数量（最多填满场地）
        space = 7 - len(self.controller.field)

        # 召唤随机2费随从填满场地
        for _ in range(space):
            minions = yield Summon(CONTROLLER, RandomMinion(cost=2))
            # 使召唤的随从立即攻击随机敌人
            if minions:
                for minion in minions:
                    if minion:
                        # 临时给予冲锋能力
                        minion.charge = True
                        # 找到随机敌方目标
                        enemies = self.controller.opponent.field + [self.controller.opponent.hero]
                        valid_enemies = [e for e in enemies if e.can_be_attacked_by(minion)]
                        if valid_enemies:
                            import random
                            target = random.choice(valid_enemies)
                            yield Attack(minion, target)


# LEGENDARY

class GDB_234:
    """孢子女皇摩尔达拉 - Spore Empress Moldara
    Start of Game: Shuffle 7 Replicating Spores into your deck.

    4费 4/4 战士传说随从
    <b>对战开始时：</b>将7张复制孢子洗入你的牌库。
    """
    # 对战开始时效果
    def start_of_game(self):
        # 将7张复制孢子洗入牌库
        for _ in range(7):
            yield Shuffle(CONTROLLER, "GDB_234t")


class GDB_235:
    """大主教阿卡玛 - Exarch Akama
    [x]After this attacks, all other friendly minions can attack again <i>(except Exarch Akama)</i>.

    5费 3/6 战士传说随从 - 德莱尼
    在本随从攻击后，所有其他友方随从可再次攻击<i>（大主教阿卡玛除外）</i>。
    """
    race = Race.DRAENEI

    # 在本随从攻击后，刷新所有其他友方随从的攻击次数
    events = Attack(SELF).after(
        Refresh(FRIENDLY_MINIONS - SELF, {GameTag.NUM_ATTACKS_THIS_TURN: -1})
    )


# Buff Enchantments

class GDB_232e:
    """不屈的守备官 Buff
    下一个打出的德莱尼会使英雄获得其攻击力
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

    events = Play(CONTROLLER, DRAENEI).on(
        lambda self, player, played_card, target=None: self._give_hero_attack(played_card)
    )

    def _give_hero_attack(self, card):
        """给英雄添加临时攻击力"""
        if card and hasattr(card, 'atk'):
            # 创建一个临时武器buff，给予英雄攻击力（参考 DMF_730e）
            # 使用 ATK 和 DURABILITY 标签
            from fireplace.cards.utils import buff
            # 动态创建buff类
            hero_buff = type('GDB_232e2', (), {
                'tags': {
                    GameTag.ATK: card.atk,
                    GameTag.DURABILITY: 1,
                    GameTag.CARDTYPE: CardType.ENCHANTMENT
                }
            })
            yield Buff(FRIENDLY_HERO, hero_buff)
        # 移除这个buff
        yield Destroy(SELF)


class GDB_229e:
    """探险队中士 Buff
    下一个打出的德莱尼会立即攻击随机敌人
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

    events = Play(CONTROLLER, DRAENEI).after(
        lambda self, player, played_card, target=None: self._make_draenei_attack(played_card)
    )

    def _make_draenei_attack(self, card):
        """使打出的德莱尼立即攻击随机敌人"""
        if card and card.zone == Zone.PLAY:
            # 临时给予冲锋能力
            card.charge = True
            # 找到随机敌方目标
            enemies = card.controller.opponent.field + [card.controller.opponent.hero]
            valid_enemies = [e for e in enemies if e.can_be_attacked_by(card)]
            if valid_enemies:
                import random
                target = random.choice(valid_enemies)
                yield Attack(card, target)
        # 移除这个buff
        yield Destroy(SELF)


class GDB_231e:
    """晶石巨槌 Buff - 德莱尼攻击力+2"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

    def apply(self, target):
        target.atk += 2


class SC_411e:
    """震荡弹 Buff - 下一次星舰发射减2费"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

    # 星舰发射减费属性（LaunchStarship action 会检查这个属性）
    starship_launch_cost_reduction = 2


class GDB_230e:
    """坚定的复仇者 - 攻击时免疫 Buff"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.IMMUNE: True
    }

    # 攻击结束后移除免疫
    events = Attack(OWNER).after(Destroy(SELF))
