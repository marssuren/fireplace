"""巫妖王的进军 - 恶魔猎手 (March of the Lich King - Demon Hunter)"""
from ..utils import *


class RLK_206:
    """轻蔑印记 (Mark of Scorn)
    抽一张牌，如果不是随从牌，对生命值最低的敌人造成$4点伤害。
    """
    def play(self):
        # 抽一张牌
        drawn_card = yield Draw(CONTROLLER)
        # 如果抽到的牌不是随从牌，对生命值最低的敌人造成4点伤害
        if drawn_card and drawn_card[0].type != CardType.MINION:
            yield Hit(ENEMY_CHARACTERS + LOWESTHEALTH, 4)


class RLK_207:
    """凶猛的外来者 (Fierce Outsider)
    突袭。流放：你的下一张流放牌法力值消耗减少（1）点。
    机制: OUTCAST, RUSH
    """
    tags = {GameTag.RUSH: True}
    outcast = Buff(CONTROLLER, "RLK_207e")


class RLK_207e:
    """凶猛的外来者效果 (Fierce Outsider Effect)
    你的下一张流放牌法力值消耗减少（1）点。
    """
    update = Refresh(FRIENDLY_HAND + OUTCAST, {GameTag.COST: -1})
    events = Play(CONTROLLER, OUTCAST).on(Destroy(SELF))


class RLK_208:
    """邪多雷战队 (Fel'dorei Warband)
    造成$4点伤害。如果你的牌库中没有随从牌，召唤四个1/1并具有突袭的伊利达雷。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True}

    def play(self):
        # 造成4点伤害
        yield Hit(TARGET, 4)
        # 如果牌库中没有随从牌，召唤四个1/1突袭的伊利达雷
        if not (FRIENDLY_DECK + MINION).eval(self.controller.game, self.controller):
            yield Summon(CONTROLLER, "RLK_208t") * 4


class RLK_208t:
    """伊利达雷 (Illidari)
    1/1 突袭
    """
    tags = {GameTag.RUSH: True}


class RLK_209:
    """释放邪能 (Unleash Fel)
    对所有敌人造成$1点伤害。法力渴求（6）：吸血。
    机制: MANATHIRST
    """
    def play(self):
        # 法力渴求（6）：如果本回合使用过至少6点法力，伤害具有吸血
        if self.controller.mana_spent_this_turn >= 6:
            # 对所有敌人造成1点伤害，具有吸血效果
            for target in (ENEMY_CHARACTERS).eval(self.game, self.controller):
                yield Hit(target, 1)
                yield Heal(FRIENDLY_HERO, 1)
        else:
            # 对所有敌人造成1点伤害
            yield Hit(ENEMY_CHARACTERS, 1)


class RLK_210:
    """失心流亡者 (Wretched Exile)
    在你使用一张流放牌后，随机将一张流放牌置入你的手牌。
    机制: TRIGGER_VISUAL
    """
    events = Play(CONTROLLER, OUTCAST).after(Give(CONTROLLER, RandomCard(outcast=True)))


class RLK_211:
    """魔鬼交易 (Deal with a Devil)
    召唤两个3/3并具有吸血的邪能邪犬。如果你的牌库中没有随从牌，再召唤两个。
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}

    def play(self):
        # 召唤两个3/3吸血的邪能邪犬
        yield Summon(CONTROLLER, "RLK_211t") * 2
        # 如果牌库中没有随从牌，再召唤两个
        if not (FRIENDLY_DECK + MINION).eval(self.controller.game, self.controller):
            yield Summon(CONTROLLER, "RLK_211t") * 2


class RLK_211t:
    """邪能邪犬 (Fel Hound)
    3/3 吸血
    """
    tags = {GameTag.LIFESTEAL: True}


class RLK_212:
    """安尼赫兰蛮魔 (Brutal Annihilan)
    嘲讽。突袭。每当本随从受到伤害并存活下来时，对敌方英雄造成等量的伤害。
    机制: RUSH, TAUNT, TRIGGER_VISUAL
    """
    tags = {GameTag.TAUNT: True, GameTag.RUSH: True}
    events = Damage(SELF).on(Hit(ENEMY_HERO, Damage.AMOUNT))


class RLK_213:
    """复仇重击者 (Vengeful Walloper)
    突袭。在本局对战中，你每使用过一张流放牌，本牌的法力值消耗便减少（1）点。
    机制: RUSH
    """
    tags = {GameTag.RUSH: True}

    cost_mod = lambda self, i: -self.controller.outcast_cards_played_this_game
class RLK_214:
    """食魂者之镰 (Souleater's Scythe)
    对战开始时：吞食你套牌中3张不同的随从牌。留下灵魂，用以发现这些随从。
    机制: START_OF_GAME_KEYWORD
    """
    start_of_game = (
        Find(FRIENDLY_DECK + MINION) & (
            Buff(SELF, "RLK_214e", card_to_store=Find.CARD) +
            Destroy(Find.CARD)
        )
    ) * 3


class RLK_214e:
    """食魂者之镰效果 (Souleater's Scythe Effect)
    存储被吞食的随从牌
    """
    def apply(self, target):
        # 初始化存储列表
        if not hasattr(target, 'devoured_minions'):
            target.devoured_minions = []
        # 存储被吞食的随从
        if hasattr(self, 'card_to_store'):
            target.devoured_minions.append(self.card_to_store)

    # 攻击后发现被吞食的随从
    events = Attack(OWNER).after(
        lambda self, source: GenericChoice(
            source.controller, [Copy(card) for card in getattr(source, 'devoured_minions', [])]
        ) if hasattr(source, 'devoured_minions') and source.devoured_minions else None
    )


class RLK_215:
    """被遗忘的费勒林 (Felerin, the Forgotten)
    战吼：随机将一张流放牌分别置入你手牌的最左边和最右边，其法力值消耗减少（2）点。
    机制: BATTLECRY
    """
    def play(self):
        # 生成第一张随机流放牌（置入最左边）
        card1 = yield Give(CONTROLLER, RandomCard(outcast=True))
        if card1:
            # 减少2点费用
            yield Buff(card1[0], "RLK_215e")
            # 将卡牌移到手牌最左边（索引0）
            if card1[0] in self.controller.hand:
                self.controller.hand.remove(card1[0])
                self.controller.hand.insert(0, card1[0])

        # 生成第二张随机流放牌（置入最右边）
        card2 = yield Give(CONTROLLER, RandomCard(outcast=True))
        if card2:
            # 减少2点费用
            yield Buff(card2[0], "RLK_215e")
            # 卡牌已经在最右边，无需移动


class RLK_215e:
    """被遗忘的费勒林效果 (Felerin Effect)
    法力值消耗减少（2）点
    """
    tags = {GameTag.COST: -2}


