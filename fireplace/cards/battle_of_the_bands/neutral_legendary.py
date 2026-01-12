# -*- coding: utf-8 -*-
"""
传奇音乐节（Festival of Legends）- 中立 传说
"""

from ..utils import *

class ETC_080:
    """乐队经理精英牛头人酋长 / E.T.C., Band Manager
    在构筑你的套牌时，用3张牌组建一支乐队。<b>战吼：发现</b>其中一张！"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    # ETC Band Manager 完整实现
    # 乐队成员存储在 player.etc_band 中,是一个包含3个卡牌ID的列表
    # 在套牌构筑时设置,例如: player.etc_band = ["CARD_ID_1", "CARD_ID_2", "CARD_ID_3"]
    
    def play(self):
        """战吼:从乐队成员中发现一张牌"""
        # 获取玩家的乐队成员
        band_cards = getattr(self.controller, 'etc_band', [])
        
        if not band_cards:
            # 如果没有设置乐队,返回空(向后兼容)
            return []
        
        # 创建可选择的卡牌列表
        choices = [self.controller.card(card_id) for card_id in band_cards]
        
        # 发现一张卡牌
        choice = yield GenericChoice(CONTROLLER, choices)
        
        if choice:
            # 将选中的卡牌加入手牌
            yield Give(CONTROLLER, choice[0].id)
            # 从乐队中移除已选择的卡牌
            if choice[0].id in band_cards:
                band_cards.remove(choice[0].id)
class JAM_037:
    """精英牛头人歌王 / Elite Tauren Champion
    <b>压轴：</b>开启摇滚对决！玩家每回合必须消耗所有法力值，否则其英雄会受到8点<i>（或更高）</i>伤害！"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
    }
    # 摇滚对决：为双方玩家添加一个持续效果
    finale = (
        Buff(FRIENDLY_HERO, "JAM_037e"),
        Buff(ENEMY_HERO, "JAM_037e")
    )


class JAM_037e:
    """摇滚对决"""
    # 每回合结束时检查是否消耗了所有法力值
    events = TURN_END.on(
        Find(OWNER + (USED_MANA < MAX_MANA)) & Hit(OWNER, 8)
    )
class JAM_036:
    """乐坛灾星玛加萨 / Magatha, Bane of Music
    <b>战吼：</b>抽五张牌。将抽到的法术牌交给你的对手。"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
    }
    play = (
        Draw(CONTROLLER) * 5,
        Give(OPPONENT, Copy(FRIENDLY_HAND + SPELL + DRAWN_THIS_TURN)),
        Discard(FRIENDLY_HAND + SPELL + DRAWN_THIS_TURN)
    )
class ETC_113:
    """摄影师菲兹尔 / Photographer Fizzle
    <b>战吼：</b>拍摄你当前的手牌，并将照片洗入你的牌库。<i>（每局对战限一次）</i>"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    # 拍摄手牌：将当前手牌的复制洗入牌库
    # 每局对战限一次需要检查是否已经使用过
    play = Find(FRIENDLY_HERO + TIMES_PLAYED_THIS_GAME("ETC_113") == 0) & Shuffle(CONTROLLER, Copy(FRIENDLY_HAND))
class ETC_425:
    """音响工程师普兹克 / Pozzik, Audio Engineer
    <b>战吼：</b>将两张3/3的机器人置入你对手的手牌。<b>亡语：</b>为你自己召唤这些机器人。"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    play = Give(OPPONENT, "ETC_425t") * 2
    deathrattle = Summon(CONTROLLER, "ETC_425t") * 2
class ETC_409:
    """融合独奏团 / The One-Amalgam Band
    <b>战吼：</b>在本局对战中，你每使用过一个不同类型的随从牌，便随机获得一项<b>额外效果</b>。0<i>（已使用0个）</i>"""
    tags = {
        GameTag.ATK: 6,
        GameTag.HEALTH: 6,
        GameTag.COST: 7,
    }
    # 根据使用过的不同种族数量,随机获得额外效果
    # 完整实现:追踪 player.unique_minion_races_played
    
    def play(self):
        """战吼:根据使用过的不同种族数量,随机获得额外效果"""
        # 获取已使用过的不同种族集合
        unique_races = getattr(self.controller, 'unique_minion_races_played', set())
        
        # 每个不同的种族给予一个随机额外效果
        num_effects = len(unique_races)
        
        for _ in range(num_effects):
            yield Buff(SELF, "ETC_409e")


class ETC_409e:
    """随机额外效果"""
    # 随机获得:冲锋、圣盾、嘲讽、吸血、风怒、剧毒、突袭、扰魔等效果之一
    
    BONUS_EFFECTS = [
        {GameTag.CHARGE: True},          # 冲锋
        {GameTag.DIVINE_SHIELD: True},   # 圣盾
        {GameTag.TAUNT: True},           # 嘲讽
        {GameTag.LIFESTEAL: True},       # 吸血
        {GameTag.WINDFURY: True},        # 风怒
        {GameTag.POISONOUS: True},       # 剧毒
        {GameTag.RUSH: True},            # 突袭
        {GameTag.CANT_BE_TARGETED_BY_ABILITIES: True},  # 扰魔
    ]
    
    def apply(self, target):
        """应用时随机选择一个额外效果"""
        import random
        effect = random.choice(self.BONUS_EFFECTS)
        self.tags = effect
class ETC_541:
    """盗版之王托尼 / Tony, King of Piracy
    <b>战吼：</b>将你的牌库替换成对手牌库的复制。<b>压轴：</b>抽一张牌。"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 6,
        GameTag.COST: 7,
    }
    play = (
        Mill(FRIENDLY_DECK),
        Shuffle(CONTROLLER, Copy(ENEMY_DECK))
    )
    finale = Draw(CONTROLLER)
