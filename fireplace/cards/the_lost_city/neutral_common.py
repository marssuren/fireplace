"""
失落之城 - NEUTRAL COMMON
"""
from ..utils import *
from .kindred_helpers import check_kindred_active


# DINO_419 - 饲草助手
class DINO_419:
    """饲草助手 - Herbivore Assistant
    3费 3/2
    <b>战吼：</b>使一只友方野兽获得+2/+2和<b>突袭</b>。
    
    Battlecry: Give a friendly Beast +2/+2 and Rush.
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.BEAST,
    }
    
    def play(self):
        # 给目标野兽+2/+2和突袭
        if TARGET:
            yield Buff(TARGET, "DINO_419e")


class DINO_419e:
    """饲草助手增益 - Herbivore Assistant Buff"""
    tags = {
        GameTag.RUSH: True,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


# TLC_101 - 卧底教徒
class TLC_101:
    """卧底教徒 - Undercover Cultist
    3费 2/3
    <b>嘲讽</b>。<b>复生</b>。受伤时拥有+3攻击力。
    
    Taunt. Reborn. Has +3 Attack while damaged.
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.REBORN: True,
        GameTag.ENRAGED: True,
    }
    
    @property
    def atk(self):
        """受伤时+3攻击力"""
        if self.damage:
            return 3
        return 0


# TLC_109 - 遗宝挖掘工
class TLC_109:
    """遗宝挖掘工 - Relic Excavator
    3费 3/3
    <b>战吼：</b>摧毁你牌库顶的牌，<b>发现</b>一张稀有度与其相同的牌。
    
    Battlecry: Destroy the top card of your deck. Discover a card of the same Rarity.
    """
    def play(self):
        # 摧毁牌库顶的牌
        if self.controller.deck:
            top_card = self.controller.deck[0]
            rarity = top_card.rarity
            
            # 摧毁牌库顶的牌
            yield Mill(CONTROLLER, 1)
            
            # 发现一张相同稀有度的牌
            cards = yield Discover(CONTROLLER, cards=RandomCollectible(
                rarity=rarity
            ))


# TLC_242 - 远古剑龙
class TLC_242:
    """远古剑龙 - Ancient Stegosaurus
    3费 1/5 野兽
    <b>战吼：</b>从<b>嘲讽</b>，<b>剧毒</b>或+1/+1中选择一项并获得。
    
    Battlecry: Choose One - Gain Taunt; Gain Poisonous; or Gain +1/+1.
    """
    choose = ["TLC_242a", "TLC_242b", "TLC_242c"]


class TLC_242a:
    """远古剑龙选项1 - 嘲讽"""
    tags = {
        GameTag.TAUNT: True,
    }


class TLC_242b:
    """远古剑龙选项2 - 剧毒"""
    tags = {
        GameTag.POISONOUS: True,
    }


class TLC_242c:
    """远古剑龙选项3 - +1/+1"""
    atk = 1
    max_health = 1


# TLC_243 - 涡流风暴幼龙
class TLC_243:
    """涡流风暴幼龙 - Whirlwind Wyrmling
    9费 8/8 元素/龙
    <b>突袭</b>。<b>风怒</b> <b>延系：</b>在本回合中获得<b>免疫</b>。
    
    Rush. Windfury. Kindred: Gain Immune this turn.
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.WINDFURY: True,
    }
    
    def play(self):
        # 检查延系是否激活（上回合打出过元素或龙）
        if check_kindred_active(self.controller, card_type=CardType.MINION, race=Race.ELEMENTAL) or \
           check_kindred_active(self.controller, card_type=CardType.MINION, race=Race.DRAGON):
            # 本回合获得免疫
            yield Buff(SELF, "TLC_243e")


class TLC_243e:
    """涡流风暴幼龙免疫 - Whirlwind Wyrmling Immune"""
    tags = {
        GameTag.IMMUNE: True,
        GameTag.TAG_ONE_TURN_EFFECT: True,
    }


# TLC_244 - 好奇的探险者
class TLC_244:
    """好奇的探险者 - Curious Explorer
    2费 3/5
    <b>亡语：</b>使你对手的手牌中一张随从牌的法力值消耗减少（2）点。
    
    Deathrattle: Reduce the Cost of a random minion in your opponent's hand by (2).
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = Buff(RANDOM(OPPONENT_HAND + MINION), "TLC_244e")


class TLC_244e:
    """好奇的探险者减费 - Curious Explorer Cost Reduction"""
    cost = -2


# TLC_247 - 原始剑齿豹
class TLC_247:
    """原始剑齿豹 - Primal Sabertooth
    4费 5/3 野兽
    <b>潜行</b>。在本随从攻击并消灭一个随从后，获取一张被消灭随从的复制。
    
    Stealth. After this attacks and kills a minion, add a copy of it to your hand.
    """
    tags = {
        GameTag.STEALTH: True,
    }
    
    events = Attack(SELF, MINION).after(
        lambda self, source, target: (
            target.dead and [
                Give(CONTROLLER, Copy(target))
            ]
        )
    )


# TLC_248 - 超巨摩天龙
class TLC_248:
    """超巨摩天龙 - Colossal Brontosaurus
    11费 14/28 野兽
    
    A massive dinosaur with no special abilities.
    """
    # 纯白板随从，无特殊效果
    pass


# TLC_249 - 炽烈烬火
class TLC_249:
    """炽烈烬火 - Blazing Ember
    1费 2/1 元素
    <b>亡语：</b>造成2点伤害，随机分配到所有敌人身上。
    
    Deathrattle: Deal 2 damage randomly split among all enemies.
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER * 2, 1)


# TLC_250 - 环形山鳄鱼
class TLC_250:
    """环形山鳄鱼 - Crater Crocodile
    4费 5/4 野兽
    <b>战吼：</b>直到你的下个回合开始，敌方英雄无法被治疗。
    
    Battlecry: The enemy hero can't be healed until the start of your next turn.
    """
    def play(self):
        # 给对手英雄添加一个buff，阻止治疗
        yield Buff(OPPONENT_HERO, "TLC_250e")


class TLC_250e:
    """环形山鳄鱼效果 - Crater Crocodile Effect
    
    阻止治疗，持续到下个回合开始
    """
    tags = {
        GameTag.CANT_BE_HEALED: True,
    }
    
    # 在控制者的回合开始时移除
    events = OWN_TURN_BEGIN.on(
        lambda self: Destroy(SELF)
    )


# TLC_253 - 石化食人魔
class TLC_253:
    """石化食人魔 - Petrified Ogre
    3费 5/5
    起始<b>休眠</b>状态。<b>休眠</b>状态下，在你的回合开始时，获得+2/+2。<i>（50%的几率改为唤醒。）</i>
    
    Starts Dormant. While Dormant, at the start of your turn, gain +2/+2. (50% chance to Awaken instead.)
    """
    tags = {
        GameTag.DORMANT: True,
    }
    
    events = OWN_TURN_BEGIN.on(
        lambda self: (
            self.dormant and [
                # 50%几率唤醒，50%几率+2/+2
                Random(
                    # 唤醒
                    SetTags(SELF, {GameTag.DORMANT: False}),
                    # +2/+2
                    Buff(SELF, "TLC_253e")
                )
            ]
        )
    )


class TLC_253e:
    """石化食人魔增益 - Petrified Ogre Buff"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


# TLC_256 - 沼地蛇颈龙
class TLC_256:
    """沼地蛇颈龙 - Swamp Plesiosaur
    3费 3/3 野兽
    在你施放一个法术后，获得<b>圣盾</b>。
    
    After you cast a spell, gain Divine Shield.
    """
    events = Play(CONTROLLER, SPELL).after(
        lambda self, source, card: SetTags(SELF, {GameTag.DIVINE_SHIELD: True})
    )


# TLC_427 - 抛石鱼人
class TLC_427:
    """抛石鱼人 - Stone-Throwing Murloc
    2费 1/3 鱼人
    <b>战吼：</b>获取一张法力值消耗为（1）的石头。石头可以造成$3点伤害。
    
    Battlecry: Add a (1)-Cost Stone to your hand that deals 3 damage.
    """
    def play(self):
        # 获取一张石头
        yield Give(CONTROLLER, "TLC_427t")


# TLC_429 - 蒸鳍偷蛋贼
class TLC_429:
    """蒸鳍偷蛋贼 - Steamfin Egg Thief
    2费 2/2 鱼人
    <b>延系：</b>召唤两个1/1并具有<b>突袭</b>的鱼人。
    
    Kindred: Summon two 1/1 Murlocs with Rush.
    """
    def play(self):
        # 检查延系是否激活（上回合打出过鱼人）
        if check_kindred_active(self.controller, card_type=CardType.MINION, race=Race.MURLOC):
            # 召唤两个1/1鱼人
            for _ in range(2):
                yield Summon(CONTROLLER, "TLC_429t")


# TLC_454 - 鳞皮科多兽
class TLC_454:
    """鳞皮科多兽 - Scaly Kodo
    6费 3/6 野兽
    <b>战吼：</b>消灭攻击力最低的敌方随从。<b>延系：</b>改为消灭攻击力最高的敌方随从。
    
    Battlecry: Destroy the enemy minion with the lowest Attack. Kindred: Destroy the highest instead.
    """
    def play(self):
        # 检查延系是否激活（上回合打出过野兽）
        kindred_active = check_kindred_active(self.controller, card_type=CardType.MINION, race=Race.BEAST)
        
        if kindred_active:
            # 消灭攻击力最高的敌方随从
            targets = self.game.query(ENEMY_MINIONS)
            if targets:
                highest_atk_minion = max(targets, key=lambda m: m.atk)
                yield Destroy(highest_atk_minion)
        else:
            # 消灭攻击力最低的敌方随从
            targets = self.game.query(ENEMY_MINIONS)
            if targets:
                lowest_atk_minion = min(targets, key=lambda m: m.atk)
                yield Destroy(lowest_atk_minion)


# TLC_468 - 黏团焦油
class TLC_468:
    """黏团焦油 - Tar Blob
    3费 2/4
    <b>剧毒</b>。<b>嘲讽</b>。<b>亡语：</b>召唤一个1/2并具有<b>剧毒</b>的黏团，以及一个1/2并具有<b>嘲讽</b>的黏团。
    
    Poisonous. Taunt. Deathrattle: Summon a 1/2 Poisonous Blob and a 1/2 Taunt Blob.
    """
    tags = {
        GameTag.POISONOUS: True,
        GameTag.TAUNT: True,
        GameTag.DEATHRATTLE: True,
    }
    
    def deathrattle(self):
        # 召唤一个1/2剧毒黏团
        yield Summon(CONTROLLER, "TLC_468t1")
        # 召唤一个1/2嘲讽黏团
        yield Summon(CONTROLLER, "TLC_468t2")


# TLC_603 - 栉龙
class TLC_603:
    """栉龙 - Parasaurolophus
    1费 1/2 野兽
    <b>战吼：</b>抽一张牌。<b>亡语：</b>弃掉该牌。
    
    Battlecry: Draw a card. Deathrattle: Discard that card.
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    def play(self):
        # 抽一张牌并标记
        cards = yield Draw(CONTROLLER)
        if cards:
            # 给抽到的牌添加标记enchantment
            yield Buff(cards[0], "TLC_603e")
    
    def deathrattle(self):
        # 弃掉带有TLC_603e标记的牌（如果还在手牌中）
        marked_cards = [card for card in self.controller.hand if any(
            buff.id == "TLC_603e" for buff in card.buffs
        )]
        if marked_cards:
            yield Discard(marked_cards[0])


class TLC_603e:
    """栉龙标记 - Parasaurolophus Mark
    
    标记由栉龙抽到的牌
    """
    # 仅用于标记，无实际效果
    pass


# TLC_605 - 焦油暴君
class TLC_605:
    """焦油暴君 - Tar Tyrant
    8费 1/12 元素
    <b>嘲讽</b>。<b>吸血</b> 在你对手的回合拥有+6攻击力。
    
    Taunt. Lifesteal. Has +6 Attack during your opponent's turn.
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.LIFESTEAL: True,
    }
    
    @property
    def atk(self):
        """在对手回合+6攻击力"""
        if self.game.current_player != self.controller:
            return 6
        return 0


# TLC_621 - 固执的守护者
class TLC_621:
    """固执的守护者 - Stubborn Guardian
    4费 4/7
    <b>嘲讽</b>。<b>亡语：</b>摧毁你牌库顶的三张牌。
    
    Taunt. Deathrattle: Destroy the top 3 cards of your deck.
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = Mill(CONTROLLER, 3)


# TLC_831 - 翼手龙蛋
class TLC_831:
    """翼手龙蛋 - Pterrordax Egg
    3费 0/3
    <b>亡语：</b>召唤一只3/3并会从所有其他随从处偷取1点生命值的翼手龙。
    
    Deathrattle: Summon a 3/3 Pterrordax that steals 1 Health from all other minions.
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = Summon(CONTROLLER, "TLC_831t")


# TLC_987 - 任务助理
class TLC_987:
    """任务助理 - Quest Assistant
    2费 3/2
    <b>战吼：</b>如果你在本局对战中使用过<b>任务</b>牌，对一个敌方随从造成3点伤害。
    
    Battlecry: If you've played a Quest this game, deal 3 damage to an enemy minion.
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    
    # powered_up 用于UI显示（高亮效果）
    powered_up = lambda self: self.controller.quest_played
    
    def play(self):
        # 检查是否打出过任务牌
        # 优先使用 Player 的 quest_played 属性（已在核心扩展中添加）
        if self.controller.quest_played and TARGET:
            yield Hit(TARGET, 3)
