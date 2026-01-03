"""巫妖王的进军 - 战士 (March of the Lich King - Warrior)"""
from ..utils import *


class RLK_600:
    """阳炎冶锻 (Sunfire Smithing)
    装备一把4/2的剑。随机使你手牌中的一张随从牌获得+4/+2。
    """
    def play(self):
        yield Equip(CONTROLLER, "RLK_600t")
        yield Buff(RANDOM(FRIENDLY_HAND + MINION), "RLK_600e")


class RLK_600t:
    """阳炎之剑 (Sunfire Sword)"""
    # 4/2
    atk = 4
    durability = 2


class RLK_600e:
    """阳炎强化 (Sunfire Buff)"""
    tags = {GameTag.ATK: +4, GameTag.HEALTH: +2}


class RLK_601:
    """破釜沉舟 (Last Stand)
    抽一张嘲讽随从牌。法力渴求（7）：使其属性值翻倍。
    机制: MANATHIRST
    """
    def play(self):
        # 抽一张嘲讽随从牌
        # result is a list of cards drawn
        cards = yield ForceDraw(RANDOM(FRIENDLY_DECK + MINION + TAUNT))
        
        # 法力渴求（7）
        if self.controller.max_mana >= 7:
            for card in cards:
                yield Buff(card, "RLK_601e")


class RLK_601e:
    """破釜沉舟增益 (Last Stand Buff)"""
    def apply(self, target):
        # 捕捉当前属性的快照并翻倍
        # 参考 Emeriss (GIL_128e) 的实现
        self._xatk = target.atk * 2
        self._xhealth = target.max_health * 2
        
    # 将属性设置为捕捉到的值
    atk = lambda self, _: self._xatk
    max_health = lambda self, _: self._xhealth


class RLK_602:
    """银怒坚兵 (Silverfury Stalwart)
    突袭。扰魔。嘲讽
    机制: ELUSIVE, RUSH, TAUNT
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.TAUNT: True,
        # 扰魔 = 无法成为法术或英雄技能的目标
        GameTag.CANT_BE_TARGETED_BY_SPELLS: True,
        GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: True,
    }


class RLK_603:
    """凤凰之光 (Light of the Phoenix)
    抽两张牌。每有一个受伤的友方角色，本牌的法力值消耗便减少（1）点。
    """
    # 动态消耗
    cost_mod = -Count(FRIENDLY_CHARACTERS + DAMAGED)
    play = Draw(CONTROLLER) * 2


class RLK_604:
    """索利贝洛尔 (Thori'belore)
    突袭。亡语：进入休眠状态。施放一个火焰法术以复活索利贝洛尔！
    机制: DEATHRATTLE, RUSH
    """
    tags = {GameTag.RUSH: True}
    
    # 亡语：召唤休眠版本
    deathrattle = Summon(CONTROLLER, "RLK_604t")


class RLK_604t:
    """休眠的索利贝洛尔 (Dormant Thori'belore)"""
    tags = {GameTag.DORMANT: True}
    # 施放火焰法术时复活
    # 这里的复活通常意味着：销毁休眠物，召唤本体
    events = Play(CONTROLLER, SPELL + FIRE).on(
        Destroy(SELF),
        Summon(CONTROLLER, "RLK_604")
    )


class RLK_605:
    """炫目之力 (Blazing Power)
    使一个随从获得+1/+1。每有一个受伤的友方角色，重复一次。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0
    }
    
    def play(self):
        # 基础一次
        count = 1
        # 加成次数
        count += len(self.controller.game.board.filter(
            controller=self.controller,
            damaged=True
        ))
        
        # 重复 Buff
        yield Buff(TARGET, "RLK_605e") * count


class RLK_605e:
    """炫目之力 (Blazing Power Buff)"""
    tags = {GameTag.ATK: +1, GameTag.HEALTH: +1}


class RLK_607:
    """搅局破法者 (Disruptive Spellbreaker)
    在你的回合结束时，你的对手弃掉一张法术牌。
    机制: TRIGGER_VISUAL
    """
    events = OWN_TURN_END.on(Discard(RANDOM(ENEMY_HAND + SPELL)))


class RLK_608:
    """巨盾卫士阿斯维顿 (Asvedon, the Grandshield)
    嘲讽。战吼：施放你对手使用的上一张法术牌的复制。
    机制: BATTLECRY, TAUNT
    """
    tags = {GameTag.TAUNT: True}
    
    def play(self):
        # 获取对手使用的上一张法术
        opponent = self.controller.opponent
        last_spell = opponent.last_played_spell
        
        if last_spell:
            # 创建一个在 SETASIDE 的复制
            copy = self.controller.card(last_spell.id, zone=Zone.SETASIDE)
            
            # 使用标准的 CastSpell 动作来施放法术
            # 它会自动处理随机目标选择，且不消耗法力值
            yield CastSpell(copy)


class RLK_609:
    """日怒勇士 (Sunfury Champion)
    在你施放一个火焰法术后，对所有随从造成1点伤害。
    机制: TRIGGER_VISUAL
    """
    # 经典的 "Wild Pyromancer" 变体
    events = Play(CONTROLLER, SPELL + FIRE).after(Hit(ALL_MINIONS, 1))


class RLK_960:
    """力量余烬 (Embers of Strength)
    召唤两个1/2并具有嘲讽的守卫。法力渴求（6）：使其获得+1/+2。
    机制: MANATHIRST
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}

    def play(self):
        # 召唤基础代币
        minions = yield Summon(CONTROLLER, "RLK_960t") * 2
        
        # 法力渴求（6）
        if self.controller.max_mana >= 6:
            yield Buff(minions, "RLK_960e")


class RLK_960t:
    """守卫 (Guard)"""
    # 1/2 嘲讽
    tags = {GameTag.TAUNT: True}


class RLK_960e:
    """力量余烬增益 (Embers of Strength Buff)"""
    tags = {GameTag.ATK: +1, GameTag.HEALTH: +2}
