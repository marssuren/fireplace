"""巫妖王的进军 - 猎人 (March of the Lich King - Hunter)"""
from ..utils import *


class RLK_804:
    """咒术之箭 (Conjured Arrow)
    对一个随从造成$2点伤害。法力渴求（6）：抽取相同数量的牌。
    机制: MANATHIRST
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self, target):
        # 造成2点伤害
        yield Hit(target, 2)
        # 法力渴求（6）：抽取相同数量的牌（抽2张）
        if self.controller.max_mana >= 6:
            yield Draw(CONTROLLER) * 2


class RLK_817:
    """奥术箭袋 (Arcane Quiver)
    从你的牌库中发现一张法术牌。如果选中的是奥术法术牌，使其获得法术伤害+1。
    机制: DISCOVER
    """
    def play(self):
        # 从牌库中发现一张法术牌
        discovered = yield GenericChoice(CONTROLLER, RANDOM(FRIENDLY_DECK + SPELL) * 3)
        if discovered:
            # 将发现的法术牌加入手牌
            yield Give(CONTROLLER, Copy(discovered))
            # 如果是奥术法术牌，使其获得法术伤害+1
            if discovered.spell_school == SpellSchool.ARCANE:
                # 给刚加入手牌的卡牌添加buff
                yield Buff(FRIENDLY_HAND + ID(discovered.id), "RLK_817e")


class RLK_817e:
    """奥术增强 (Arcane Enhancement)
    法术伤害+1
    """
    tags = {GameTag.SPELL_DAMAGE: 1}


class RLK_818:
    """弹溅射击 (Ricochet Shot)
    随机对三个敌人造成$1点伤害。
    """
    def play(self):
        # 随机对三个敌人造成1点伤害
        yield Hit(RANDOM_ENEMY_CHARACTER, 1) * 3


class RLK_819:
    """永歌传送门 (Eversong Portal)
    召唤$1只4/4并具有突袭的山猫（受法术伤害加成影响）。
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}

    def play(self):
        # 召唤的数量 = 1 + 法术伤害加成
        count = 1 + self.controller.spellpower
        yield Summon(CONTROLLER, "RLK_819t") * count


class RLK_819t:
    """永歌山猫 (Eversong Lynx)
    4/4 野兽，突袭
    """
    # Token 卡牌，属性在 CardDefs.xml 中定义
    pass


class RLK_820:
    """哈杜伦·明翼 (Halduron Brightwing)
    战吼：使你手牌和牌库中所有奥术法术牌获得法术伤害+1。
    机制: BATTLECRY
    """
    play = Buff(FRIENDLY_HAND + FRIENDLY_DECK + SPELL + ARCANE, "RLK_820e")


class RLK_820e:
    """奥术强化 (Arcane Empowerment)
    法术伤害+1
    """
    tags = {GameTag.SPELL_DAMAGE: 1}


class RLK_821:
    """天灾驯兽师 (Scourge Tamer)
    战吼：制造一个自定义的僵尸兽。
    机制: BATTLECRY
    """
    def play(self):
        # 第一步：从牌库中发现一张野兽牌作为第一个部件
        first_part = yield GenericChoice(CONTROLLER, RANDOM(FRIENDLY_DECK + BEAST + (COST <= 5)) * 3)
        if not first_part:
            return

        # 第二步：从牌库中发现另一张野兽牌作为第二个部件
        second_part = yield GenericChoice(CONTROLLER, RANDOM(FRIENDLY_DECK + BEAST + (COST <= 5)) * 3)
        if not second_part:
            return

        # 创建僵尸兽：复制第一个部件，并继承第二个部件的关键词和效果
        zombeast = yield Give(CONTROLLER, Copy(first_part))
        if zombeast:
            # 继承第二个部件的攻击力和生命值（叠加）
            zombeast.buff(zombeast, "RLK_821e", atk=second_part.atk, health=second_part.health)
            # 继承第二个部件的关键词
            for tag in [GameTag.TAUNT, GameTag.DIVINE_SHIELD, GameTag.WINDFURY,
                       GameTag.CHARGE, GameTag.RUSH, GameTag.LIFESTEAL,
                       GameTag.POISONOUS, GameTag.STEALTH]:
                if getattr(second_part, tag.name.lower(), False):
                    setattr(zombeast, tag.name.lower(), True)


class RLK_821e:
    """僵尸兽强化 (Zombeast Enhancement)
    继承第二个部件的属性
    """
    def apply(self, target):
        # Buff 会自动应用 atk 和 health 参数
        pass


class RLK_825:
    """哮雷龙鹰 (Shockspitter)
    战吼：造成1点伤害。（在本局对战中，你的英雄每攻击一次都会提升！）
    机制: BATTLECRY
    """
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}

    def play(self, target=None):
        # 造成伤害 = 1 + 英雄攻击次数
        damage = 1 + self.controller.hero_attacks_this_game
        if target:
            yield Hit(target, damage)


class RLK_826:
    """银月城远行者 (Silvermoon Farstrider)
    战吼：使你手牌中所有奥术法术牌获得法术伤害+1。
    机制: BATTLECRY
    """
    play = Buff(FRIENDLY_HAND + SPELL + ARCANE, "RLK_826e")


class RLK_826e:
    """奥术增幅 (Arcane Boost)
    法术伤害+1
    """
    tags = {GameTag.SPELL_DAMAGE: 1}


class RLK_827:
    """锐眼侦察兵 (Keeneye Spotter)
    每当你的英雄攻击随从时，将被攻击随从的生命值变为1。
    机制: TRIGGER_VISUAL
    """
    events = Attack(FRIENDLY_HERO, MINION).on(
        lambda self, source, target: target.set_current_health(1) if target.health > 1 else None
    )


class RLK_828:
    """奎尔萨拉斯的希望 (Hope of Quel'Thalas)
    在你的英雄攻击后，使你的所有随从获得+1/+1（无论它们在哪）。
    机制: TRIGGER_VISUAL
    """
    events = Attack(FRIENDLY_HERO).after(
        lambda self, source, target: [
            # 给场上的随从+1/+1
            Buff(FRIENDLY_MINIONS, "RLK_828e"),
            # 给手牌中的随从+1/+1
            Buff(FRIENDLY_HAND + MINION, "RLK_828e"),
            # 给牌库中的随从+1/+1
            Buff(FRIENDLY_DECK + MINION, "RLK_828e")
        ]
    )


class RLK_828e:
    """奎尔萨拉斯的祝福 (Blessing of Quel'Thalas)
    +1/+1
    """
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}


