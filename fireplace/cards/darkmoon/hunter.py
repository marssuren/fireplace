"""
暗月马戏团 - 猎人
"""
from ..utils import *


##
# Minions

class DMF_083:
    """舞动的眼镜蛇 - Dancing Cobra
    腐蚀：获得剧毒。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    corrupt = Buff(SELF, "DMF_083e")


class DMF_083e:
    """剧毒"""
    tags = {
        GameTag.POISONOUS: True,
    }


class DMF_085:
    """暗月坦克 - Darkmoon Tonk
    亡语：向随机敌人发射四枚导弹，每枚造成2点伤害。
    """
    tags = {
        GameTag.ATK: 8,
        GameTag.HEALTH: 5,
        GameTag.COST: 7,
    }
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 2) * 4


class DMF_087:
    """狂踏的犀牛 - Trampling Rhino
    突袭。在本随从攻击并消灭一个随从后，超量伤害会命中敌方英雄。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
        GameTag.RUSH: True,
        GameTag.OVERKILL: True,  # 使用 OVERKILL 标签实现超量伤害
    }


class DMF_089:
    """玛克希玛·雷管 - Maxima Blastenheimer
    战吼：从你的牌库中召唤一个随从。该随从攻击敌方英雄，然后死亡。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 2,
        GameTag.COST: 8,
    }
    
    def play(self):
        # 从牌库中随机召唤一个随从
        # 使用 RANDOM 选择器而非 Python random
        minions_in_deck = [card for card in self.controller.deck if card.type == CardType.MINION]
        if not minions_in_deck:
            return
        
        # 使用 fireplace 的随机系统
        minion = self.game.random.choice(minions_in_deck)
        
        # 召唤该随从
        yield Summon(CONTROLLER, minion)
        
        # 检查随从是否成功召唤到场上
        if minion.zone != Zone.PLAY:
            return
        
        # 强制该随从攻击敌方英雄
        enemy_hero = self.controller.opponent.hero
        if enemy_hero and minion.can_attack():
            yield Attack(minion, enemy_hero)
        
        # 攻击后，摧毁该随从
        yield Destroy(minion)


class DMF_089e:
    """雷管标记 - Blastenheimer Mark"""
    # 这个buff只是一个标记，表示随从是被雷管召唤的
    # 主要用于视觉效果或日志记录
    pass


class DMF_122:
    """神秘获奖者 - Mystery Winner
    战吼：发现一张奥秘牌。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
    }
    # 发现一张猎人奥秘牌
    play = DISCOVER(RandomCollectible(card_class=CardClass.HUNTER, secret=True))


class YOP_028:
    """鞍座管理员 - Saddlemaster
    在你打出一张野兽牌后，随机将一张野兽牌置入你的手牌。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    events = Play(CONTROLLER, MINION + BEAST).after(
        Give(CONTROLLER, RandomCollectible(card_class=CardClass.HUNTER, race=Race.BEAST))
    )


##
# Spells

class DMF_084:
    """恩佐斯宝石 - Jewel of N'Zoth
    召唤三个在本局对战中死亡的友方亡语随从。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    play = Summon(CONTROLLER, RANDOM(FRIENDLY + KILLED + MINION + DEATHRATTLE) * 3)


class DMF_086:
    """宠物乐园 - Petting Zoo
    召唤一个3/3的陆行鸟。你每控制一个奥秘，便重复一次。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    play = Summon(CONTROLLER, "DMF_086t") * (Count(FRIENDLY_SECRETS) + 1)


class DMF_086t:
    """陆行鸟 - Strider"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
        GameTag.CARDRACE: Race.BEAST,
    }


class DMF_090:
    """请勿投食 - Don't Feed the Animals
    使你手牌中的所有野兽牌获得+1/+1。腐蚀：改为使其获得+2/+2。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    play = Buff(FRIENDLY_HAND + MINION + BEAST, "DMF_090e")
    corrupt = Buff(FRIENDLY_HAND + MINION + BEAST, "DMF_090e2")


class DMF_090e:
    """+1/+1"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class DMF_090e2:
    """+2/+2（腐蚀版本）"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class DMF_123:
    """打开兽笼 - Open the Cages
    奥秘：在你的回合开始时，如果你控制两个随从，便召唤一个动物伙伴。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SECRET: True,
    }
    secret = OWN_TURN_BEGIN.on(
        Find(Count(FRIENDLY_MINIONS) >= 2) & (
            Summon(CONTROLLER, RandomEntourage()),
            Reveal(SELF),
        )
    )
    entourage = ["NEW1_032", "NEW1_033", "NEW1_034"]  # Misha, Leokk, Huffer


class YOP_027:
    """套索射击 - Bola Shot
    对一个随从造成1点伤害，并对其相邻的随从造成2点伤害。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Hit(TARGET, 1),
        Hit(TARGET_ADJACENT, 2),
    )


##
# Weapons

class DMF_088:
    """瑞林的步枪 - Rinling's Rifle
    在你的英雄攻击后，发现一张奥秘牌并施放。
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 2,
        GameTag.DURABILITY: 2,
        GameTag.COST: 4,
    }
    
    # 在你的英雄攻击后,发现一张猎人奥秘并施放
    def _discover_and_cast_secret(self, card):
        """发现一张奥秘并自动施放"""
        # 发现一张猎人奥秘
        cards = yield DISCOVER(RandomCollectible(card_class=CardClass.HUNTER, secret=True))
        if cards:
            # 自动施放发现的奥秘
            yield Summon(CONTROLLER, cards[0])
    
    events = Attack(FRIENDLY_HERO).after(_discover_and_cast_secret)
