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
    # TODO: 实现复杂的奥秘效果 - 需要追踪对手本回合打出的所有牌
    # 目前先留空，等待后续实现
    pass


class SCH_305:
    """Secret Passage / 秘密通道
    Replace your hand with 4 cards from your deck. Swap back next turn.
    将你的手牌替换为你牌库中的4张牌。下回合换回来。"""

    # 2费 将你的手牌替换为你牌库中的4张牌。下回合换回来
    # TODO: 实现复杂的手牌交换效果 - 需要保存当前手牌并在下回合换回
    # 目前先实现简单版本：将手牌移回牌库，然后抽4张牌
    play = Shuffle(CONTROLLER, FRIENDLY_HAND), Draw(CONTROLLER) * 4


##
# Weapons

class SCH_622:
    """Self-Sharpening Sword / 自磨利剑
    After your hero attacks, gain +1 Attack.
    在你的英雄攻击后，获得+1攻击力。"""

    # 3费 1/4 武器 在你的英雄攻击后，获得+1攻击力
    events = Attack(FRIENDLY_HERO).after(Buff(SELF, "SCH_622e"))


SCH_622e = buff(atk=1)
