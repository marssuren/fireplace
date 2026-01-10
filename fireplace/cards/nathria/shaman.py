"""纳斯利亚堡的悬案（Murder at Castle Nathria）卡牌实现"""
from ..utils import *


class MAW_003:
    """Totemic Evidence - 图腾物证
    Choose a basic Totem and summon it.
<b>Infuse (3 Totems):</b>
Summon all 4 instead.
    选择一个基础图腾并召唤它。<b>注能(3个图腾)：</b>改为召唤全部4个。
    """
    # 注能机制：需要3个图腾死亡
    # 注意：这里的注能条件是"3 Totems"，意味着需要3个图腾死亡
    infuse = 3
    
    def play(self):
        # 基础图腾列表
        basic_totems = ["CS2_050", "CS2_051", "CS2_052", "NEW1_009"]
        
        if self.infused:
            # 注能后：召唤全部4个基础图腾
            for totem_id in basic_totems:
                yield Summon(CONTROLLER, totem_id)
        else:
            # 未注能：选择一个基础图腾并召唤
            choice = yield GenericChoice(CONTROLLER, basic_totems)
            if choice:
                yield Summon(CONTROLLER, choice[0])


class MAW_005:
    """Framester - 栽赃者
    [x]<b>Battlecry:</b> Shuffle 3 'Framed'
cards into the opponent's
deck. When drawn, they
<b>Overload</b> for (2).
    <b>战吼：</b>将3张"栽赃"牌洗入对手的牌库。当其被抽到时，使其<b>过载</b>(2)点。
    """
    def play(self):
        # 洗入3张"栽赃"牌到对手牌库
        for i in range(3):
            yield Shuffle(OPPONENT, "MAW_005t")


class MAW_005t:
    """Framed - 栽赃"""
    # Token: 栽赃牌
    # 当被抽到时，过载(2)
    def draw(self):
        # 给对手过载2点
        yield GiveOverload(CONTROLLER, 2)
        # 然后移除此卡（烧掉）
        yield Destroy(SELF)


class MAW_030:
    """Torghast Custodian - 托加斯特管理员
    [x]<b>Battlecry:</b> For each
enemy minion, randomly
gain <b>Rush</b>, <b>Divine Shield</b>,
or <b>Windfury</b>.
    <b>战吼：</b>每有一个敌方随从，便随机获得<b>突袭</b>、<b>圣盾</b>或<b>风怒</b>。
    """
    def play(self):
        # 计算敌方随从数量
        enemy_count = len(list(ENEMY_MINIONS.eval(self.game, self)))
        
        # 可选的关键词
        keywords = [GameTag.RUSH, GameTag.DIVINE_SHIELD, GameTag.WINDFURY]
        
        # 为每个敌方随从随机获得一个关键词
        for i in range(enemy_count):
            keyword = self.game.random.choice(keywords)
            self.tags[keyword] = True


class REV_517:
    """Criminal Lineup - 罪犯列队
    [x]Choose a friendly minion.
Summon 3 copies of it.
<b>Overload:</b> (2)
    选择一个友方随从。召唤3个它的复制。<b>过载：</b>(2)
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 召唤3个目标的复制
        for i in range(3):
            yield Summon(CONTROLLER, Copy(TARGET))
    
    # 过载(2)
    overload = 2


class REV_838:
    """Gigantotem - 图腾巨像
    Costs (1) less for each Totem you've summoned this game.
    你在本局对战中每召唤一个图腾，其法力值消耗便减少（1）点。
    """
    class Hand:
        cost_mod = lambda self, i: -self.controller.times_totem_summoned_this_game if hasattr(self.controller, 'times_totem_summoned_this_game') else 0


class REV_917:
    """Carving Chisel - 石雕凿刀
    After your hero attacks, summon a random basic Totem.
    在你的英雄攻击后，召唤一个随机的基础图腾。
    """
    events = Attack(FRIENDLY_HERO).after(
        Summon(CONTROLLER, RandomID(["CS2_050", "CS2_051", "CS2_052", "NEW1_009"]))
    )


class REV_920:
    """Convincing Disguise - 可信的伪装
    [x]Transform a friendly minion
into one that costs (2) more.
<b>Infuse (4):</b> Transform all
friendly minions instead.
    将一个友方随从变形成为一个法力值消耗多（2）点的随从。<b>注能(4)：</b>改为变形所有友方随从。
    """
    infuse = 4
    
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self, target=None):
        if self.infused:
            # 注能后：变形所有友方随从
            for minion in list(FRIENDLY_MINIONS.eval(self.game, self)):
                # 变形为费用+2的随从
                yield Morph(minion, RandomMinion(cost=minion.cost + 2))
        else:
            # 未注能：变形目标
            if target:
                yield Morph(target, RandomMinion(cost=target.cost + 2))


class REV_921:
    """The Stonewright - 锻石师
    <b>Battlecry:</b> For the rest of the game, your Totems have +2 Attack.
    <b>战吼：</b>在本局对战的剩余时间内，你的图腾获得+2攻击力。
    """
    def play(self):
        # 给控制者添加永久buff
        yield Buff(FRIENDLY_HERO, "REV_921e")


class REV_921e:
    """The Stonewright Effect - 锻石师效果"""
    # 给所有图腾+2攻击力
    # 使用 UPDATE 事件持续更新
    update = Refresh(FRIENDLY_MINIONS + TOTEM, {GameTag.ATK: +2})


class REV_923:
    """Muck Pools - 淤泥之池
    Transform a friendly minion into one that costs (1) more.
    将一个友方随从变形成为一个法力值消耗多（1）点的随从。
    """
    # LOCATION 地标
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def activate(self):
        # 变形为费用+1的随从
        if TARGET:
            yield Morph(TARGET, RandomMinion(cost=TARGET.cost + 1))


class REV_924:
    """Primordial Wave - 始源之潮
    [x]Transform enemy minions 
into ones that cost (1) less 
and friendly minions into 
ones that cost (1) more.
    将敌方随从变形成为法力值消耗少（1）点的随从，将友方随从变形成为法力值消耗多（1）点的随从。
    """
    def play(self):
        # 变形所有敌方随从（费用-1）
        for minion in list(ENEMY_MINIONS.eval(self.game, self)):
            new_cost = max(0, minion.cost - 1)
            yield Morph(minion, RandomMinion(cost=new_cost))
        
        # 变形所有友方随从（费用+1）
        for minion in list(FRIENDLY_MINIONS.eval(self.game, self)):
            yield Morph(minion, RandomMinion(cost=minion.cost + 1))


class REV_925:
    """Baroness Vashj - 瓦丝琪女男爵
    [x]If this would transform
into a minion, summon
that minion instead.
    如果该随从将要变形成为一个随从，改为召唤该随从。
    """
    # 使用新的 TRANSFORM_IMMUNE 标签
    # 核心的 Morph action 会检查这个标签
    from fireplace import enums
    tags = {enums.TRANSFORM_IMMUNE: True}


class REV_935:
    """Party Favor Totem - 派对图腾
    [x]At the end of your turn, 
summon a random basic 
Totem. <b>Infuse (2):</b> 
Summon two instead.
    在你的回合结束时，召唤一个随机的基础图腾。<b>注能(2):</b>改为召唤两个。
    """
    infuse = 2
    
    # 基础图腾列表
    BASIC_TOTEMS = ["CS2_050", "CS2_051", "CS2_052", "NEW1_009"]
    
    def _summon_totems(self, source):
        """在回合结束时召唤图腾"""
        # 根据是否注能，召唤不同数量的图腾
        count = 2 if self.infused else 1
        # 基础图腾列表
        totems = ["CS2_050", "CS2_051", "CS2_052", "NEW1_009"]
        for i in range(count):
            totem_id = self.game.random.choice(totems)
            yield Summon(CONTROLLER, totem_id)
    
    events = OWN_TURN_END.on(_summon_totems)


class REV_936:
    """Crud Caretaker - 粗暴的看管者
    <b>Battlecry</b>: Summon a 3/5 Elemental with <b>Taunt</b>.
    <b>战吼：</b>召唤一个3/5并具有<b>嘲讽</b>的元素。
    """
    play = Summon(CONTROLLER, "REV_936t")


class REV_936t:
    """Elemental - 元素"""
    # Token: 3/5 嘲讽元素
    tags = {GameTag.TAUNT: True}


