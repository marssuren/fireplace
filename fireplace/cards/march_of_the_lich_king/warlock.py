"""巫妖王的进军 - 术士 (March of the Lich King - Warlock)"""
from ..utils import *


class RLK_531:
    """步军重生官 (Infantry Reanimator)
    战吼：复活一个友方亡灵，使其获得复生。
    机制: BATTLECRY, REBORN
    """
    def play(self):
        # 复活一个友方亡灵，并赋予复生
        # 筛选死亡的友方亡灵
        dead_undead = self.controller.graveyard.filter(type=CardType.MINION, race=Race.UNDEAD)
        if dead_undead:
            # 随机选择一个
            target = self.controller.game.random.choice(dead_undead)
            # 召唤它并赋予复生
            # 注意：Summon 会把卡牌从坟场移回战场
            yield Summon(CONTROLLER, target)
            yield Buff(target, "RLK_531e")


class RLK_531e:
    """步军重生官增益 (Infantry Reanimator Buff)"""
    tags = {GameTag.REBORN: True}


class RLK_532:
    """行尸 (Walking Dead)
    嘲讽。如果你弃掉了这张随从牌，则会召唤它。
    机制: TAUNT, InvisibleDeathrattle, DISCARD
    """
    tags = {GameTag.TAUNT: True}
    
    # 弃牌触发逻辑
    # 通常这是一个 Hand trigger 或者 Global listener
    # 但 fireplace 的 Card 定义支持 `discard` script
    # 当卡牌被弃掉时，actions.py 会调用 get_actions("discard")
    
    def discard(self):
        # 召唤自身
        # 注意：此时卡牌已经在 REMOVEDFROMGAME 或者类似区域
        # Summon 可以处理来自任何区域的卡牌
        yield Summon(CONTROLLER, SELF)


class RLK_533:
    """天灾补给 (Scourge Supplies)
    抽三张牌，从中选择一张弃掉。
    """
    def play(self):
        # 抽三张牌
        cards_drawn = []
        for i in range(3):
            res = yield Draw(CONTROLLER)
            if res:
                cards_drawn.append(res[0])
        
        # 如果抽到了牌，选择一张弃掉
        # 这里的“从中选择”通常意味着这三张牌
        # 如果手牌混合了其他牌，UI 上会显示这三张
        # 在 Fireplace 中，GenericChoice 可以限制选项
        if cards_drawn:
            yield GenericChoice(CONTROLLER, cards_drawn, callback=lambda card: Discard(card))


class RLK_534:
    """灵魂弹幕 (Soul Barrage)
    当你使用或弃掉这张牌时，造成6点伤害，随机分配到所有敌人身上。
    机制: Immutable
    """
    # 这里的 "使用或弃掉" 分别对应 play 和 discard script
    
    def play(self):
        yield Hit(RANDOM_ENEMY_CHARACTER, 1) * 6
        
    def discard(self):
        # 弃掉时也触发同样的效果
        yield Hit(RANDOM_ENEMY_CHARACTER, 1) * 6


class RLK_535:
    """野蛮的伊米亚人 (Savage Ymirjar)
    突袭，战吼：弃两张牌。
    机制: BATTLECRY, RUSH
    """
    tags = {GameTag.RUSH: True}
    
    def play(self):
        # 弃两张牌 (随机)
        # Discard(CONTROLLER, RANDOM(FRIENDLY_HAND) * 2) ?
        # RandomDiscard action
        yield Discard(RANDOM(FRIENDLY_HAND) * 2)


class RLK_536:
    """薄葬 (Shallow Grave)
    触发一个友方随从的亡语，然后将其消灭。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        # 触发亡语
        yield Deathrattle(TARGET)
        # 消灭
        yield Destroy(TARGET)


class RLK_537:
    """扭曲束缚 (Twisted Tether)
    消灭一个随从，随机使你手牌中的一张亡灵牌获得其属性值。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        target = self.target
        if target is None:
            return
        # 获取目标属性
        atk = target.atk
        health = target.health
        
        # 消灭目标
        yield Destroy(target)
        
        # 随机使手牌中一张亡灵获得属性
        undead_in_hand = self.controller.hand.filter(race=Race.UNDEAD)
        if undead_in_hand:
            target_card = self.controller.game.random.choice(undead_in_hand)
            yield Buff(target_card, "RLK_537e", atk=atk, health=health)

class RLK_537e:
    """扭曲束缚增益 (Twisted Tether Buff)"""
    # 动态属性增益
    # 需要在应用时传入 atk 和 health 参数
    pass


class RLK_538:
    """噬魂者 (Devourer of Souls)
    在一个友方随从死亡后，获得其亡语。
    机制: TRIGGER_VISUAL
    """
    # 监听友方随从死亡，并复制其亡语
    # 使用 CopyDeathrattleBuff，它会将 Death.ENTITY 的亡语复制给 "RLK_538e" 这个 Buff，并贴在 SELF 身上
    events = Death(FRIENDLY_MINIONS - SELF).on(
        CopyDeathrattleBuff(Death.ENTITY, "RLK_538e")
    )


class RLK_538e:
    """噬魂者亡语增益 (Devourer of Souls Buff)"""
    tags = {GameTag.DEATHRATTLE: True}


class RLK_539:
    """达尔坎·德拉希尔 (Dar'Khan Drathir)
    吸血。在你的回合结束时，对敌方英雄造成6点伤害。
    机制: LIFESTEAL, TRIGGER_VISUAL
    """
    tags = {GameTag.LIFESTEAL: True}
    # 回合结束触发
    events = OWN_TURN_END.on(
        Hit(ENEMY_HERO, 6)
    )


class RLK_540:
    """流形泥浆怪 (Amorphous Slime)
    战吼：随机弃掉一张亡灵牌。亡语：召唤被弃掉的亡灵的一个复制。
    机制: BATTLECRY, DEATHRATTLE
    """
    def play(self):
        # 筛选手牌中的亡灵
        undead_hand = self.controller.hand.filter(race=Race.UNDEAD)
        if undead_hand:
            # 随机选择一张
            target = self.controller.game.random.choice(undead_hand)
            # 记录并弃牌
            # 使用 StoringBuff 记录目标卡牌，以便亡语通过 STORE_CARD 读取
            yield StoringBuff(SELF, "RLK_540e", target)
            yield Discard(target)


class RLK_540e:
    """流形泥浆怪记忆 (Amorphous Slime Memory)"""
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, Copy(STORE_CARD))
