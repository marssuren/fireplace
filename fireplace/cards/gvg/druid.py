from ..utils import *


##
# Minions


class GVG_030:
    """Anodized Robo Cub / 电镀机械熊仔
    嘲讽，抉择： +1攻击力；或者+1生命值。"""

    choose = ("GVG_030a", "GVG_030b")
    play = ChooseBoth(CONTROLLER) & (Buff(SELF, "GVG_030ae"), Buff(SELF, "GVG_030be"))


class GVG_030a:
    play = Buff(SELF, "GVG_030ae")


GVG_030ae = buff(atk=1)


class GVG_030b:
    play = Buff(SELF, "GVG_030be")


GVG_030be = buff(health=1)


class GVG_032:
    """Grove Tender / 林地树妖
    抉择：使每个玩家获得一个法力水晶；或每个玩家抽一张牌。"""

    choose = ("GVG_032a", "GVG_032b")
    play = ChooseBoth(CONTROLLER) & ((GainMana(ALL_PLAYERS, 1), Draw(ALL_PLAYERS)))


class GVG_032a:
    play = GainMana(ALL_PLAYERS, 1)


class GVG_032b:
    play = Draw(ALL_PLAYERS)


class GVG_034:
    """Mech-Bear-Cat / 机械熊豹
    每当本随从受到伤害，将一张零件牌置入你的手牌。"""

    events = SELF_DAMAGE.on(Give(CONTROLLER, RandomSparePart()))


class GVG_035:
    """Malorne / 玛洛恩
    亡语：进入休眠状态。在2只友方野兽死亡后复活。"""

    # Caverns of Time 更新版本 (Patch 27.2.0.183876 - 2023年8月22日)
    # 原版效果：亡语：将本随从洗入你的牌库
    # 新版效果：亡语：进入休眠状态。在2只友方野兽死亡后复活
    
    def deathrattle(self):
        # 召唤休眠的玛洛恩
        yield Summon(CONTROLLER, "GVG_035t")


class GVG_035t:
    """休眠的玛洛恩 (Dormant Malorne)"""
    
    dormant = True
    
    def apply(self, target):
        # 初始化进度计数器
        target.malorne_progress = 0
    
    # 监听友方野兽死亡
    def _on_beast_death(self):
        # 增加进度
        self.owner.malorne_progress = getattr(self.owner, 'malorne_progress', 0) + 1
        # 检查是否达到2
        if self.owner.malorne_progress >= 2:
            # 唤醒
            self.owner.is_dormant = False
    
    events = Death(FRIENDLY + BEAST).on(_on_beast_death)


class GVG_080:
    """Druid of the Fang / 毒牙德鲁伊
    战吼：如果你控制任何野兽，将本随从变形成为7/7。"""

    powered_up = Find(FRIENDLY_MINIONS + BEAST)
    play = powered_up & Morph(SELF, "GVG_080t")


##
# Spells


class GVG_031:
    """Recycle / 回收
    将一个敌方随从洗入你对手的 牌库。"""

    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Shuffle(OPPONENT, TARGET)


class GVG_033:
    """Tree of Life / 生命之树
    为所有角色恢复所有生命值。"""

    play = FullHeal(ALL_CHARACTERS)


class GVG_041:
    """Dark Wispers / 黑暗私语
    抉择： 召唤5个小精灵；或者使一个随从获得+5/+5和嘲讽。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    choose = ("GVG_041a", "GVG_041b")
    play = ChooseBoth(CONTROLLER) & (
        Buff(TARGET, "GVG_041c"),
        Summon(CONTROLLER, "CS2_231") * 5,
    )


class GVG_041a:
    play = Buff(TARGET, "GVG_041c")
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}


GVG_041c = buff(+5, +5, taunt=True)


class GVG_041b:
    play = Summon(CONTROLLER, "CS2_231") * 5
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_NUM_MINION_SLOTS: 1}
