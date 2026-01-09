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
    def play(self):
        # 将牌库按费用从高到低排序
        if self.controller.deck:
            # 使用 Python 的 sort，按费用降序
            self.controller.deck.sort(key=lambda card: card.cost, reverse=True)

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

    # 战吼：召唤两个随机5费随从，秘密选择一个添加"受伤即死"buff
    # 完整实现：使用 GenericChoice 让玩家秘密选择
    def play(self):
        # 召唤两个随机5费随从
        yield Summon(CONTROLLER, RandomMinion(cost=5))
        yield Summon(CONTROLLER, RandomMinion(cost=5))
        
        # 获取刚召唤的随从（最后两个友方随从）
        minions = list(self.controller.field)
        if len(minions) >= 2:
            # 让玩家秘密选择一个添加"受伤即死"buff
            # 使用 GenericChoice 让玩家从刚召唤的两个随从中选择
            summoned_minions = minions[-2:]
            choice = yield GenericChoice(
                self.controller,
                cards=summoned_minions
            )
            
            if choice:
                target = choice[0]
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

    # 战吼：召唤两个1/1幼龙，每个获得一个本局死亡随从的亡语
    # 完整实现：使用 GenericChoice 让玩家选择要复制的亡语
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
                # 让玩家选择一个死亡随从的亡语复制给幼龙
                # 使用 GenericChoice 让玩家从死亡的有亡语的随从中选择
                choice = yield GenericChoice(
                    self.controller,
                    cards=dead_minions_with_deathrattle
                )
                
                if choice:
                    source = choice[0]
                    # 使用 CopyDeathrattleBuff 正确复制亡语效果
                    yield Retarget(whelp, source)
                    yield CopyDeathrattleBuff(source, "SCH_162e")


class SCH_162e:
    """Vectus - Copied Deathrattle / 复制的亡语"""
    # 这个 buff 会由 CopyDeathrattleBuff 填充实际的亡语效果
    pass


class SCH_162t:
    """Whelp / 幼龙
    1/1"""
    # Token: 1/1 幼龙（属性在CardDefs.xml中定义）
    pass


class SCH_717:
    """Keymaster Alabaster / 钥匙大师阿拉巴斯特
    Whenever your opponent draws a card, add a copy to your hand that costs (1)."""

    # 每当你的对手抽一张牌，将一张复制置入你的手牌，其法力值消耗为（1）点
    def _on_opponent_draw(self):
        """对手抽牌时触发"""
        # 获取对手抽的牌
        drawn_card = Draw.CARD
        
        # 创建复制
        copy = yield Give(CONTROLLER, drawn_card.id)
        
        if copy:
            # 设置费用为1
            yield Buff(copy[0], "SCH_717e")
    
    events = Draw(OPPONENT).on(lambda self: self._on_opponent_draw())


class SCH_717e:
    """Keymaster Alabaster Buff - Costs (1)"""
    tags = {GameTag.COST: 1}


##
# Weapons

class SCH_259:
    """Sphere of Sapience / 睿智法球
    At the start of your turn, look at your top card. You can put it on the bottom and lose 1 Durability."""

    # 在你的回合开始时，查看你牌库顶的卡牌，并让玩家选择是否将其置底
    # 完整实现：使用 GenericChoice 让玩家/AI 做出选择
    def _sphere_effect(self):
        """
        睿智法球效果：查看牌库顶卡牌，让玩家选择是否置底
        
        选项：
        1. 保留卡牌在牌库顶（不消耗耐久度）
        2. 将卡牌置底并消耗1点耐久度
        """
        controller = self.controller
        deck = controller.deck
        
        # 检查牌库是否为空
        if not deck:
            return
        
        # 获取牌库顶卡牌
        top_card = deck[0]
        
        # 显示牌库顶卡牌（Reveal效果）
        yield Reveal(top_card)
        
        # 让玩家选择：保留或置底
        # 使用 GenericChoice 提供两个选项
        choice = yield GenericChoice(controller, cards=[
            "SCH_259t1",  # 保留在牌库顶
            "SCH_259t2",  # 置底并消耗耐久度
        ])
        
        # 根据选择执行相应操作
        if choice and choice[0] == "SCH_259t2":
            # 选择了置底：将卡牌移到牌库底部
            deck.remove(top_card)
            deck.append(top_card)
            # 消耗1点耐久度
            yield Hit(SELF, 1)
        # 如果选择了 SCH_259t1 或没有选择，则不做任何操作（保留在牌库顶）
    
    events = OWN_TURN_BEGIN.on(lambda self: self._sphere_effect())


# 睿智法球的选项 Token
class SCH_259t1:
    """Keep on Top / 保留在牌库顶
    Keep the card on top of your deck."""
    # 这是一个选项卡牌，不需要实际效果
    # 选择此选项时不执行任何操作
    pass


class SCH_259t2:
    """Put on Bottom / 置于牌库底
    Put the card on the bottom of your deck and lose 1 Durability."""
    # 这是一个选项卡牌，不需要实际效果
    # 选择此选项时会在 SCH_259._sphere_effect 中执行置底和消耗耐久度的操作
    pass
