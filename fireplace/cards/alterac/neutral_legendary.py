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
        self.controller.mana = 0
        
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
                yield SetTag(SELF, {GameTag.RUSH: True})
            elif choice == "divine_shield":
                yield SetTag(SELF, {GameTag.DIVINE_SHIELD: True})
            elif choice == "taunt":
                yield SetTag(SELF, {GameTag.TAUNT: True})


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
    cost = -3


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

    # 定义宝藏卡牌池（使用决斗模式的宝藏卡牌ID）
    # 卡扎库杉共有29个宝藏可供发现
    TREASURE_POOL = [
        # 顶级宝藏（11个）
        "PVPDR_Boombox",  # Dr. Boom's Boombox - 砰砰博士的音箱
        "PVPDR_PureCold",  # Pure Cold - 纯粹寒冷
        "PVPDR_WandOfDisintegration",  # Wand of Disintegration - 瓦解之杖
        "PVPDR_EmbersOfRagnaros",  # Embers of Ragnaros - 拉格纳罗斯的余烬
        "PVPDR_LoomingPresence",  # Looming Presence - 迫近的存在
        "PVPDR_WaxRager",  # Wax Rager - 蜡质暴怒者
        "PVPDR_CanopicJars",  # Canopic Jars - 卡诺匹克罐
        "PVPDR_StaffOfScales",  # Staff of Scales - 鳞片法杖
        "PVPDR_AnnoyoHorn",  # Annoy-o Horn - 烦人的号角
        "PVPDR_BookOfTheDead",  # Book of the Dead - 亡者之书
        "PVPDR_AncientReflections",  # Ancient Reflections - 远古倒影

        # 其他宝藏（18个）
        "PVPDR_Hyperblaster",  # Hyperblaster - 超级爆破枪
        "PVPDR_GnomishArmyKnife",  # Gnomish Army Knife - 侏儒军刀
        "PVPDR_CrustyTheCrustacean",  # Crusty the Crustacean - 硬壳蟹人
        "PVPDR_BananaSplit",  # Banana Split - 香蕉船
        "PVPDR_Bubba",  # Bubba - 布巴
        "PVPDR_ClockworkAssistant",  # Clockwork Assistant - 发条助手
        "PVPDR_PuzzleBox",  # Puzzle Box - 谜题盒
        "PVPDR_BladeOfQuelDelar",  # Blade of Quel'Delar - 奎尔德拉之刃
        "PVPDR_HiltOfQuelDelar",  # Hilt of Quel'Delar - 奎尔德拉剑柄
        "PVPDR_VampiricFangs",  # Vampiric Fangs - 吸血獠牙
        "PVPDR_TheExorcisor",  # The Exorcisor - 驱魔者
        "PVPDR_HolyBook",  # Holy Book - 圣书
        "PVPDR_MutatingInjection",  # Mutating Injection - 变异注射
        "PVPDR_Spyglass",  # Spyglass - 望远镜
        "PVPDR_NecroticPoison",  # Necrotic Poison - 死灵毒药
        "PVPDR_BeastlyBeauty",  # Beastly Beauty - 野兽美人
        "PVPDR_GrimmerPatron",  # Grimmer Patron - 更暗的顾客
    ]

    def play(self):
        """检查是否打出过4条龙，如果是则替换牌库"""
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

            # 使用发现机制让玩家选择5个宝藏
            selected_treasures = []
            for i in range(5):
                # 发现一个宝藏（从剩余的宝藏池中）
                remaining_treasures = [t for t in self.TREASURE_POOL if t not in selected_treasures]
                if not remaining_treasures:
                    break

                treasure = yield GenericChoice(
                    CONTROLLER,
                    Discover(CONTROLLER, cards=remaining_treasures)
                )
                if treasure:
                    selected_treasures.append(treasure.id if hasattr(treasure, 'id') else treasure)

            # 将选中的宝藏洗入牌库（每个2张，共10张）
            for treasure_id in selected_treasures:
                for _ in range(2):
                    yield Shuffle(CONTROLLER, treasure_id)
