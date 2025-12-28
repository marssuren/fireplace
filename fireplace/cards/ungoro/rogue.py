from collections import defaultdict

from ..utils import *


##
# Minions


class UNG_058:
    """Razorpetal Lasher / 刀瓣鞭笞者
    战吼：将一张可造成2点伤害的“刀瓣”置入你的手牌。"""

    play = Give(CONTROLLER, "UNG_057t1")


class UNG_063:
    """Biteweed / 食人草
    连击：在本回合中，你每使用一张其他牌，便获得+1/+1。"""

    combo = Buff(SELF, "UNG_063e") * NUM_CARDS_PLAYED_THIS_TURN


UNG_063e = buff(+1, +1)


class UNG_064:
    """Vilespine Slayer / 邪脊吞噬者
    连击： 消灭一个随从。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_FOR_COMBO: 0,
    }
    combo = Destroy(TARGET)


class UNG_065:
    """Sherazin, Corpse Flower / “尸魔花”瑟拉金
    亡语：进入休眠状态。在一回合中使用4张牌可复活本随从。"""

    deathrattle = Find(FRIENDLY_MINIONS + SELF) & (Morph(SELF, "UNG_065t")) | (
        Summon(CONTROLLER, "UNG_065t")
    )


class UNG_065t:
    tags = {GameTag.DORMANT: True}
    progress_total = 4
    dormant_events = [
        Play(CONTROLLER).after(AddProgress(SELF, Play.CARD)),
        TURN_BEGIN.on(ClearProgress(SELF)),
    ]
    reward = Morph(SELF, "UNG_065")


##
# Spells


class UNG_057:
    """Razorpetal Volley / 刀瓣齐射
    将两张可造成2点伤害的“刀瓣”置入你的手牌。"""

    play = Give(CONTROLLER, "UNG_057t1") * 2


class UNG_057t1:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 1)


class UNG_060:
    """Mimic Pod / 拟态豆荚
    抽一张牌，然后将一张它的复制置入你的手牌。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Draw(CONTROLLER).then(Give(CONTROLLER, Copy(Draw.CARD)))


class UNG_067:
    """The Caverns Below / 探索地下洞穴
    任务：使用四张名称相同的随从牌。 奖励：水晶核心。"""

    progress_total = 5
    quest = Play(CONTROLLER, MINION).after(AddProgress(SELF, Play.CARD))
    reward = Give(CONTROLLER, "UNG_067t1")

    def add_progress(self, card):
        if not hasattr(self, "card_name_counter"):
            self.card_name_counter = defaultdict(int)
        # 炉石简中汉化组一点都不用心
        # 存在部分英文同名但简中不同名的现象
        # * NEW1_040t: Gnoll 豺狼人
        # * OG_318t: Gnoll 腐化豺狼人
        # * TU4a_003: Gnoll 豺狼人
        name = card.name_enUS
        self.card_name_counter[name] += 1


class UNG_067t1:
    play = Buff(CONTROLLER, "UNG_067t1e")


class UNG_067t1e:
    update = Refresh(
        (IN_DECK | IN_HAND | IN_PLAY) + FRIENDLY + MINION, buff="UNG_067t1e2"
    )


class UNG_067t1e2:
    atk = SET(4)
    max_health = SET(4)


class UNG_823:
    """Envenom Weapon / 浸毒武器
    使你的武器获得剧毒。"""

    requirements = {
        PlayReq.REQ_WEAPON_EQUIPPED: 0,
    }
    play = SetTags(FRIENDLY_WEAPON, (GameTag.POISONOUS,))


class UNG_856:
    """Spore Hallucination / 孢子致幻
    发现一张你对手职业的卡牌。"""

    play = Find(ENEMY_HERO - NEUTRAL) & (
        GenericChoice(CONTROLLER, RandomSpell(card_class=ENEMY_CLASS) * 3)
    ) | (GenericChoice(CONTROLLER, RandomSpell(card_class=CardClass.ROGUE) * 3))


##
# Weapons


class UNG_061:
    """Obsidian Shard / 黑曜石碎片
    在本局对战中，你每将一张非潜行者的职业牌置入你的手牌，本牌的法力值消耗便减少（1）点。"""

    cost_mod = -Count(CARDS_PLAYED_THIS_GAME + OTHER_CLASS_CHARACTER)
