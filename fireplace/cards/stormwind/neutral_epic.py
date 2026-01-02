# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 中立史诗
"""

from ..utils import *


class DED_521:
    """最疯狂的爆破者 / Maddest Bomber
    战吼：随机对所有其他角色造成总共12点伤害。"""
    play = Hit(ALL_CHARACTERS - SELF, 1) * 12


class SW_069:
    """热情的柜员 / Enthusiastic Banker
    在你的回合结束时，从你的牌库中存储一张牌。亡语：将存储的牌加入你的手牌。"""
    events = OwnTurnEnds(CONTROLLER).on(
        Find(FRIENDLY_DECK) & (
            Setaside(RANDOM(FRIENDLY_DECK)) & Buff(SELF, "SW_069e")
        )
    )
    deathrattle = lambda self: [Give(self.controller, card) for card in getattr(self, 'stored_cards', [])]


class SW_069e:
    """热情的柜员存储"""
    def apply(self, target):
        if not hasattr(target, 'stored_cards'):
            target.stored_cards = []
        # 存储最近被移到暂存区的卡牌
        setaside_cards = [c for c in target.game.entities if c.zone == Zone.SETASIDE and c.controller == target.controller]
        if setaside_cards:
            target.stored_cards.append(setaside_cards[-1])


class SW_073:
    """奶酪商贩 / Cheesemonger
    每当你的对手施放一个法术时，将一张法力值消耗相同的随机法术牌置入你的手牌。"""
    events = CastSpell(OPPONENT).on(
        Give(CONTROLLER, RandomSpell(cost=COST(CastSpell.CARD)))
    )


class SW_074:
    """贵族 / Nobleman
    战吼：复制你手牌中一张随机卡牌的金色版本。"""
    play = Give(CONTROLLER, Copy(RANDOM(FRIENDLY_HAND)))


class SW_075:
    """艾尔文野猪 / Elwynn Boar
    亡语：如果本局游戏中有7只艾尔文野猪死亡，装备一把15/3的千真剑。"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
        GameTag.RACE: Race.BEAST,
    }
    
    def deathrattle(self):
        """
        增加死亡计数
        如果达到7只，装备千真剑
        """
        # 增加死亡计数
        if not hasattr(self.controller, 'elwynn_boars_died'):
            self.controller.elwynn_boars_died = 0
        self.controller.elwynn_boars_died += 1
        
        # 如果达到7只，装备武器
        if self.controller.elwynn_boars_died >= 7:
            yield Equip(CONTROLLER, "SW_075t")


class SW_075t:
    """千真剑 / Sword of a Thousand Truths"""
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 15,
        GameTag.DURABILITY: 3,
        GameTag.COST: 10,
    }



class SW_077:
    """监狱囚徒 / Stockades Prisoner
    初始休眠。在你打出3张牌后，本随从苏醒。"""
    tags = {
        GameTag.DORMANT: True,  # 初始休眠
    }
    
    # 打出后开始追踪打出的卡牌
    play = Buff(SELF, "SW_077e")


class SW_077e:
    """监狱囚徒追踪器"""
    # 每次打出卡牌时增加计数
    events = Play(CONTROLLER).after(
        Find(SELF.owner) & Buff(SELF.owner, "SW_077_counter")
    )


class SW_077_counter:
    """打出卡牌计数标记"""
    def apply(self, target):
        """
        统计此囚徒上的计数标记数量
        达到3个时唤醒
        """
        # 统计此囚徒身上有多少个计数标记
        count = sum(1 for buff in target.buffs if buff.id == "SW_077_counter")
        
        # 如果达到3张，唤醒
        if count >= 3:
            if target.dormant:
                # 使用 Awaken action 唤醒
                from ..actions import Awaken
                Awaken(target).trigger(target)
                
                # 清除所有计数标记
                for buff in list(target.buffs):
                    if buff.id == "SW_077_counter":
                        buff.destroy()
