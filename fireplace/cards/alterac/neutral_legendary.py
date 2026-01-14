# -*- coding: utf-8 -*-
"""
奥特兰克的决裂（Fractured in Alterac Valley）- 中立传说
"""

from ..utils import *


class AV_100:
    """德雷克塔尔 / Drek'Thar
    战吼：如果本牌的法力值消耗大于你牌库中的所有随从，召唤其中一个随从。"""
    def play(self):
        """检查是否满足条件并召唤随从"""
        deck_minions = [c for c in self.controller.deck if c.type == CardType.MINION]
        if not deck_minions:
            return
        
        # 检查是否所有牌库随从的费用都小于本牌
        if all(minion.cost < self.cost for minion in deck_minions):
            # 召唤一个随机牌库随从
            yield Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION))


class AV_141t:
    """冰雪之王洛克霍拉 / Lokholar the Ice Lord
    突袭，风怒 如果你的生命值小于或等于15点，本牌的法力值消耗减少（5）点。"""
    cost_mod = lambda self, i: -5 if self.controller.hero.health <= 15 else 0


class AV_142t:
    """森林之王伊弗斯 / Ivus, the Forest Lord
    战吼：消耗你剩余的所有法力水晶，每消耗1点随机获得+2/+2、突袭、圣盾或嘲讽。"""
    def play(self):
        """消耗剩余法力并随机获得增益"""
        mana_to_spend = self.controller.mana
        if mana_to_spend <= 0:
            return
        
        # 消耗所有法力
        yield SpendMana(CONTROLLER, mana_to_spend)
        
        # 每点法力随机获得一个增益
        for _ in range(mana_to_spend):
            choice = self.game.random.choice([
                "stats",  # +2/+2
                "rush",   # 突袭
                "divine_shield",  # 圣盾
                "taunt"   # 嘲讽
            ])
            
            if choice == "stats":
                yield Buff(SELF, "AV_142te")
            elif choice == "rush":
                yield SetTags(SELF, {GameTag.RUSH: True})
            elif choice == "divine_shield":
                yield SetTags(SELF, {GameTag.DIVINE_SHIELD: True})
            elif choice == "taunt":
                yield SetTags(SELF, {GameTag.TAUNT: True})


class AV_142te:
    """+2/+2增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class AV_143:
    """血怒者科尔拉克 / Korrak the Bloodrager
    亡语：如果本随从不是被荣誉击杀的，重新召唤科尔拉克。"""
    def deathrattle(self):
        """检查是否被荣誉击杀"""
        # 如果有荣誉击杀标记，不复活
        if hasattr(self, 'was_honorably_killed') and self.was_honorably_killed:
            return
        
        # 否则复活
        yield Summon(CONTROLLER, "AV_143")


class AV_223:
    """范达尔·雷矛 / Vanndar Stormpike
    战吼：如果本牌的法力值消耗小于你牌库中的所有随从，使它们的法力值消耗减少（3）点。"""
    def play(self):
        """检查是否满足条件并减费"""
        deck_minions = [c for c in self.controller.deck if c.type == CardType.MINION]
        if not deck_minions:
            return
        
        # 检查是否所有牌库随从的费用都大于本牌
        if all(minion.cost > self.cost for minion in deck_minions):
            # 使所有牌库随从减费3点
            yield Buff(FRIENDLY_DECK + MINION, "AV_223e")


class AV_223e:
    """范达尔减费"""
    tags = {GameTag.COST: -3}


class ONY_004:
    """团本首领奥妮克希亚 / Raid Boss Onyxia
    突袭 当你控制雏龙时免疫。战吼：召唤六个2/1并具有突袭的雏龙。"""
    play = Summon(CONTROLLER, "ONY_004t") * 6
    update = Refresh(SELF, {
        GameTag.IMMUNE: Find(FRIENDLY_MINIONS + ID("ONY_004t"))
    })


class ONY_004t:
    """雏龙 / Whelp
    2/1 突袭随从"""
    # 在 CardDefs.xml 中定义


class ONY_005:
    """卡扎库杉 / Kazakusan
    战吼：如果你本局对战中打出过4条其他龙，制作一副由宝藏组成的自定义牌组。"""

    def play(self):
        """检查是否打出过4条龙，如果是则替换牌库"""
        # 定义宝藏卡牌池（使用决斗模式的宝藏卡牌ID）
        treasure_pool = [
            "PVPDR_Boombox", "PVPDR_PureCold", "PVPDR_WandOfDisintegration",
            "PVPDR_EmbersOfRagnaros", "PVPDR_LoomingPresence", "PVPDR_WaxRager",
            "PVPDR_CanopicJars", "PVPDR_StaffOfScales", "PVPDR_AnnoyoHorn",
            "PVPDR_BookOfTheDead", "PVPDR_AncientReflections", "PVPDR_Hyperblaster",
            "PVPDR_GnomishArmyKnife", "PVPDR_CrustyTheCrustacean", "PVPDR_BananaSplit",
            "PVPDR_Bubba", "PVPDR_ClockworkAssistant", "PVPDR_PuzzleBox",
        ]
        
        # 检查打出的龙数量（不包括自己）
        dragons_played = sum(
            1 for card in self.controller.graveyard + list(self.controller.field)
            if hasattr(card, 'races') and Race.DRAGON in card.races
            and card.id != self.id
        )

        if dragons_played >= 4:
            # 清空当前牌库
            for card in list(self.controller.deck):
                yield Destroy(card)

            # 随机选择5个宝藏，每个洗入2张（共10张）
            selected_treasures = self.game.random.sample(treasure_pool, min(5, len(treasure_pool)))
            for treasure_id in selected_treasures:
                for _ in range(2):
                    yield Shuffle(CONTROLLER, treasure_id)
