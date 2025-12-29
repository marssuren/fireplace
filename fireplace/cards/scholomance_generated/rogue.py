from ..utils import *


##
# Minions

class SCH_519:
    """Vulpera Toxinblade / 狐人毒刃
    Your weapon has +2 Attack. / 你的武器获得+2攻击力。"""

    # 3费 3/3 光环：你的武器获得+2攻击力
    update = Refresh(FRIENDLY_WEAPON, buff="SCH_519e")


SCH_519e = buff(atk=2)


class SCH_426:
    """Infiltrator Lilian / 渗透者莉莉安
    Stealth Deathrattle: Summon a 4/2 Forsaken Lilian that attacks a random enemy.
    潜行 亡语：召唤一个4/2的被遗忘的莉莉安，攻击一个随机敌人。"""

    # 4费 4/2 潜行 亡语：召唤一个4/2的被遗忘的莉莉安，攻击一个随机敌人
    # 潜行通过 CardDefs.xml 中的 STEALTH 标签定义
    deathrattle = Summon(CONTROLLER, "SCH_426t")


class SCH_234:
    """Shifty Sophomore / 狡猾的大二学生
    Stealth Spellburst: Add a Combo card to your hand.
    潜行 法术迸发：将一张连击牌加入你的手牌。"""

    # 4费 4/4 潜行 法术迸发：将一张连击牌加入你的手牌
    # 潜行通过 CardDefs.xml 中的 STEALTH 标签定义
    spellburst = Give(CONTROLLER, RandomCard(combo=True))


##
# Spells

class SCH_706:
    """Plagiarize / 剽窃
    Secret: At the end of your opponent's turn, add copies of the cards they played to your hand.
    奥秘：在你的对手回合结束时，将他本回合打出的牌的复制加入你的手牌。"""

    # 2费 奥秘：在你的对手回合结束时，将他本回合打出的牌的复制加入你的手牌
    # 奥秘通过 CardDefs.xml 中的 SECRET 标签定义
    # 完整实现：使用追踪buff记录对手打出的牌
    secret = Buff(CONTROLLER, "SCH_706_tracker")


class SCH_305:
    """Secret Passage / 秘密通道
    Replace your hand with 4 cards from your deck. Swap back next turn.
    将你的手牌替换为你牌库中的4张牌。下回合换回来。"""

    # 2费 将你的手牌替换为你牌库中的4张牌。下回合换回来
    # 完整实现：使用 Setaside 存储当前手牌，抽4张牌，下回合换回
    play = (
        # 1. 将当前手牌移到暂存区
        Setaside(FRIENDLY_HAND),
        # 2. 从牌库抽4张牌
        Draw(CONTROLLER) * 4,
        # 3. 添加追踪buff，下回合换回手牌
        Buff(CONTROLLER, "SCH_305_tracker")
    )


##
# Weapons

class SCH_622:
    """Self-Sharpening Sword / 自磨利剑
    After your hero attacks, gain +1 Attack.
    在你的英雄攻击后，获得+1攻击力。"""

    # 3费 1/4 武器 在你的英雄攻击后，获得+1攻击力
    events = Attack(FRIENDLY_HERO).after(Buff(SELF, "SCH_622e"))


SCH_622e = buff(atk=1)


# 手牌交换追踪buff（用于SCH_305秘密通道）
class SCH_305_tracker:
    """Secret Passage Tracker / 秘密通道追踪器

    在下回合开始时：
    1. 将当前手牌洗回牌库
    2. 从暂存区恢复原来的手牌
    3. 销毁这个buff
    """

    events = TurnBegin(CONTROLLER).on(
        # 1. 将当前手牌洗回牌库
        Shuffle(CONTROLLER, FRIENDLY_HAND),
        # 2. 从暂存区取回原来的手牌
        Give(CONTROLLER, FRIENDLY_SETASIDE),
        # 3. 销毁这个buff
        Destroy(SELF)
    )


# 剽窃追踪buff（用于SCH_706剽窃）
class SCH_706_tracker:
    """Plagiarize Tracker / 剽窃追踪器

    追踪对手本回合打出的所有牌，在对手回合结束时将复制加入手牌
    """

    def apply(self, target):
        # 初始化存储列表
        if not hasattr(target, 'plagiarize_cards'):
            target.plagiarize_cards = []

    # 监听对手打出卡牌的事件
    events = [
        # 对手打出卡牌时，记录该卡牌
        Play(OPPONENT, ALL_CARDS).on(Buff(SELF, "SCH_706_store", card_to_store=Play.CARD)),
        # 对手回合结束时，将所有记录的卡牌复制加入手牌并销毁buff
        TurnEnd(OPPONENT).on(Buff(CONTROLLER, "SCH_706_restore"), Destroy(SELF))
    ]


# 剽窃存储buff（用于存储单张卡牌）
class SCH_706_store:
    """Store a single card for Plagiarize"""

    def apply(self, target):
        # 将卡牌添加到存储列表
        if hasattr(self, 'card_to_store'):
            target.plagiarize_cards.append(self.card_to_store.id)


# 剽窃恢复buff（用于恢复所有存储的卡牌）
class SCH_706_restore:
    """Restore all stored cards for Plagiarize"""

    def apply(self, target):
        # 将所有存储的卡牌复制加入手牌
        for card_id in getattr(target, 'plagiarize_cards', []):
            target.give(card_id)
        # 清空存储列表
        target.plagiarize_cards = []
