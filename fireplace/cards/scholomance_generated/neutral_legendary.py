from ..utils import *


##
# Minions

class SCH_182:
    """Speaker Gidra / 演说者吉德拉
    Rush, Windfury Spellburst: Gain Attack and Health equal to the spell's Cost."""

    # 突袭、风怒（在CardDefs.xml中已定义）
    # 法术迸发：获得等同于该法术的法力值消耗的攻击力和生命值
    spellburst = Buff(SELF, "SCH_182e", atk=COST(SPELLBURST_SPELL), health=COST(SPELLBURST_SPELL))

class SCH_428:
    """Lorekeeper Polkelt / 博学者普克尔特
    Battlecry: Reorder your deck from the highest Cost card to the lowest Cost card."""

    # 战吼：将你的牌库中的卡牌按照法力值消耗从高到低重新排序
    play = Reorder(FRIENDLY_DECK, ORDER_BY_COST_DESC)

class SCH_425:
    """Doctor Krastinov / 克拉斯迪诺夫博士
    Rush Whenever this attacks, give your weapon +1/+1."""

    # 突袭（在CardDefs.xml中已定义）
    # 每当本随从攻击，使你的武器获得+1/+1
    events = Attack(SELF).on(Buff(FRIENDLY_WEAPON, "SCH_425e"))

class SCH_224:
    """Headmaster Kel'Thuzad / 校长克尔苏加德
    Spellburst: If the spell destroys any minions, summon them."""

    # 法术迸发：如果该法术消灭了任何随从，召唤它们
    spellburst = Summon(CONTROLLER, Copy(KILLED))

class SCH_351:
    """Jandice Barov / 詹迪斯·巴罗夫
    Battlecry: Summon two random 5-Cost minions. Secretly pick one that dies when it takes damage."""

    # 战吼：召唤两个随机5费随从，随机选择一个添加"受伤即死"buff
    # 注：原版需要玩家秘密选择，AI训练中使用随机选择是合理的实现
    def play(self):
        # 召唤两个随机5费随从
        yield Summon(CONTROLLER, RandomMinion(cost=5))
        yield Summon(CONTROLLER, RandomMinion(cost=5))
        # 获取刚召唤的随从（最后两个友方随从）
        minions = list(self.controller.field)
        if len(minions) >= 2:
            # 随机选择一个添加"受伤即死"buff
            target = self.game.random_choice(minions[-2:])
            yield Buff(target, "SCH_351e")


class SCH_351e:
    """Jandice Barov - Dies when damaged / 受伤即死"""
    # 受到伤害时立即死亡
    events = Damage(OWNER).on(Destroy(OWNER))


class SCH_273:
    """Ras Frostwhisper / 莱斯·霜语
    At the end of your turn, deal $1 damage to all enemies (improved by Spell Damage)."""

    # 在你的回合结束时，对所有敌人造成1点伤害（受法术伤害加成影响）
    events = OWN_TURN_END.on(Hit(ENEMY_CHARACTERS, 1))

class SCH_162:
    """Vectus / 维克图斯
    Battlecry: Summon two 1/1 Whelps. Each gains a Deathrattle from your minions that died this game."""

    # 战吼：召唤两个1/1幼龙，每个随机获得一个本局死亡随从的亡语
    # 注：原版需要玩家选择，AI训练中使用随机选择是合理的实现
    def play(self):
        # 召唤两个幼龙
        yield Summon(CONTROLLER, "SCH_162t")
        yield Summon(CONTROLLER, "SCH_162t")
        # 获取本局死亡的友方随从中有亡语的随从
        dead_minions_with_deathrattle = [
            m for m in self.controller.graveyard
            if m.type == CardType.MINION and hasattr(m, 'deathrattle')
        ]
        if dead_minions_with_deathrattle:
            # 获取刚召唤的两个幼龙
            whelps = [m for m in self.controller.field if m.id == "SCH_162t"][-2:]
            for whelp in whelps:
                # 随机选择一个死亡随从的亡语复制给幼龙
                source = self.game.random_choice(dead_minions_with_deathrattle)
                # 复制亡语效果（简化实现：添加相同的亡语）
                if hasattr(source, 'deathrattle'):
                    whelp.deathrattle = source.deathrattle


class SCH_162t:
    """Whelp / 幼龙
    1/1"""
    # Token: 1/1 幼龙（属性在CardDefs.xml中定义）
    pass


class SCH_717:
    """Keymaster Alabaster / 钥匙大师阿拉巴斯特
    Whenever your opponent draws a card, add a copy to your hand that costs (1)."""

    # 每当你的对手抽一张牌，将一张复制置入你的手牌，其法力值消耗为（1）点
    events = Draw(OPPONENT).on(Give(CONTROLLER, Copy(Draw.CARD, cost=1)))


##
# Weapons

class SCH_259:
    """Sphere of Sapience / 睿智法球
    At the start of your turn, look at your top card. You can put it on the bottom and lose 1 Durability."""

    # 在你的回合开始时，查看你牌库顶的卡牌
    # 注：原版需要玩家交互选择是否置底，AI训练中简化为仅显示
    events = OWN_TURN_BEGIN.on(Reveal(TOP(FRIENDLY_DECK)))
