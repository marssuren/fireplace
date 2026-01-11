from ..utils import *

# --- 乐句系统辅助类 ---

class UpdateLastRiff(Action):
    def do(self, source, riff_card):
        # 存储当前打出的乐句ID
        source.controller.last_played_riff = riff_card.id

class PlayLastRiff(Action):
    def do(self, source, target=None):
        controller = source.controller
        if hasattr(controller, 'last_played_riff') and controller.last_played_riff:
            # 创建该乐句的复制并施放
            # 注意：我们需要从ID创建一个新的卡牌对象
            riff = controller.card(controller.last_played_riff)
            source.game.queue_actions(source, [CastSpell(riff)])

# --- 卡牌实现 ---

class ETC_035:
    """Drum Soloist - 鼓乐独演者
    5费 3/5 嘲讽
    战吼：如果你没有控制其他随从，获得+2/+2和突袭。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
        GameTag.TAUNT: True,
    }
    def play(self):
        # 检查是否没有其他友方随从
        others = [m for m in self.controller.field if m is not self]
        if not others:
            yield Buff(SELF, "ETC_035e")

class ETC_035e:
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.RUSH: True,
    }

class JAM_013:
    """Jam Session - 即兴演奏
    2费法术
    使一个友方随从获得+3/+3。对所有其他随从造成1点伤害。过载：(1)。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.OVERLOAD: 1,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = (
        Buff(TARGET, "JAM_013e"),
        Hit(ALL_MINIONS - TARGET, 1)
    )

class JAM_013e:
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
    }

class ETC_355:
    """Razorfen Rockstar - 剃刀沼泽摇滚明星
    1费 1/3
    在你获得护甲值后，再获得2点。
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 3,
        GameTag.COST: 1,
    }
    # 事件：获得护甲 -> 额外获得2点
    # 注意：为了防止无限循环（如果这2点被视为新的获得护甲事件），需要小心处理。
    # Fireplace 的事件系统通常允许这种触发链。
    events = GainArmor(FRIENDLY_HERO).after(GainArmor(FRIENDLY_HERO, 2))

class ETC_363:
    """Verse Riff - 主歌乐句
    1费法术
    在本回合中，使你的英雄获得+2攻击力。获得2点护甲值。
    压轴：演奏你的上一个乐句。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    def play(self):
        # 本回合英雄+2攻击力（使用临时buff）
        yield Buff(FRIENDLY_HERO, "ETC_363e")
        yield GainArmor(FRIENDLY_HERO, 2)
        
        # 压轴效果：如果当前剩余法力值为0
        if self.controller.mana == 0:
            yield PlayLastRiff(SELF)
        
        # 更新最后打出的乐句（在效果结算后）
        yield UpdateLastRiff(SELF)

class ETC_363e:
    """主歌乐句攻击力增益（本回合）"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
    }
    # 回合结束时移除
    events = OWN_TURN_END.on(Destroy(SELF))


class JAM_014:
    """Backstage Bouncer - 后台保镖
    4费 3/4 嘲讽
    战吼：将一个友方随从变形成为本随从的复制。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
        GameTag.TAUNT: True,
    }
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_NONSELF_TARGET: 0,
    }
    play = Morph(TARGET, ExactCopy(SELF))

class ETC_364:
    """Chorus Riff - 副歌乐句
    3费法术
    抽一张随从牌，使其获得+3/+3。
    压轴：演奏你的上一个乐句。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    def play(self):
        yield Draw(CONTROLLER, RANDOM_MINION).then(Buff(Draw.CARD, "ETC_364e"))
        
        # 压轴检查
        if self.controller.mana == 0:
            yield PlayLastRiff(SELF)
            
        yield UpdateLastRiff(SELF)

class ETC_364e:
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
    }

class ETC_520:
    """Kodohide Drumkit - 科多兽皮组鼓
    4费 0/3 武器
    亡语：对所有随从造成1点伤害。（装备期间，获得护甲值以提升此效果！）
    """
    tags = {
        GameTag.ATK: 0,
        GameTag.HEALTH: 3,
        GameTag.COST: 4,
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.TAG_SCRIPT_DATA_NUM_1: 1, # 基础伤害值
    }
    
    # 亡语：造成等同于 TAG_SCRIPT_DATA_NUM_1 的伤害
    deathrattle = Hit(ALL_MINIONS, Attr(SELF, GameTag.TAG_SCRIPT_DATA_NUM_1))
    
    # 升级逻辑：装备期间，获得护甲时增加伤害
    # 这里的"提升效果"通常指伤害+1
    events = GainArmor(FRIENDLY_HERO).on(
        # 只有当武器在场（装备中）时才会触发
        Buff(SELF, "ETC_520e") 
    )

class ETC_520e:
    tags = {
        GameTag.TAG_SCRIPT_DATA_NUM_1: 1,
    }

class ETC_408:
    """Power Slider - 滑铲铁腿
    3费 1/2 突袭
    战吼：在本局对战中，你每使用过一个不同类型的随从牌，便获得+1/+1。
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
        GameTag.RUSH: True,
    }
    def play(self):
        # 统计本局对战使用的不同随从类型（种族）
        races = set()
        for card in self.controller.cards_played_this_game:
            if card.type == CardType.MINION:
                if card.race != Race.INVALID:
                    races.add(card.race)
        
        count = len(races)
        if count > 0:
            yield Buff(SELF, "ETC_408e") * count

class ETC_408e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }

class JAM_015:
    """Remixed Tuning Fork - 混搭音叉
    2费 3/2 武器
    在你的手牌中时会获得一项额外效果，该效果每回合都会改变。
    """
    # 占位符实现：如果有具体的轮换ID，应使用手牌变形逻辑
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.CARDTYPE: CardType.WEAPON,
    }
    pass

class JAM_017:
    """Through Fel and Flames - 突破邪火
    0费法术
    使一个随从获得突袭。压轴：以及+1/+1。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 0,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    def play(self):
        # 给予突袭
        yield SetAttr(TARGET, GameTag.RUSH, True)
        
        # 压轴检查
        if self.controller.mana == 0:
            yield Buff(TARGET, "JAM_017e")

class JAM_017e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }

class ETC_365:
    """Bridge Riff - 过渡乐句
    5费法术
    召唤一个3/4并具有嘲讽的乐手和一个4/3并具有突袭的乐手。
    压轴：演奏你的上一个乐句。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
    }
    def play(self):
        yield Summon(CONTROLLER, "ETC_365t")
        yield Summon(CONTROLLER, "ETC_365t2")
        
        if self.controller.mana == 0:
            yield PlayLastRiff(SELF)
            
        yield UpdateLastRiff(SELF)

class ETC_365t:
    """Rocker (Taunt) - 摇滚乐手（嘲讽）"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
        GameTag.TAUNT: True,
    }

class ETC_365t2:
    """Rocker (Rush) - 摇滚乐手（突袭）"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
        GameTag.RUSH: True,
    }

class ETC_372:
    """Roaring Applause - 掌声雷动
    2费法术
    抽一张牌。你每控制一个不同类型的随从，重复一次。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    def play(self):
        yield Draw(CONTROLLER)
        
        # 统计场上随从的种族类型
        races = set()
        for m in self.controller.field:
            if m.race != Race.INVALID:
                races.add(m.race)
        
        count = len(races)
        if count > 0:
            yield Draw(CONTROLLER) * count

class ETC_417:
    """Blackrock 'n' Roll - 黑石摇滚
    5费法术
    使你牌库中的所有随从牌获得等同于其法力值消耗的攻击力和生命值。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
    }
    
    def play(self):
        # 遍历牌库中的随从
        minions = [c for c in self.controller.deck if c.type == CardType.MINION]
        for m in minions:
             cost = m.cost
             if cost > 0:
                 yield Buff(m, "ETC_417e", atk=cost, max_health=cost)

class ETC_417e:
    """Blackrock Effect - 黑石摇滚效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_121:
    """Rock Master Voone - 摇滚教父沃恩
    4费 4/3
    战吼：复制你手牌中每个不同类型的随从牌各一张。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 3,
        GameTag.COST: 4,
    }
    
    def play(self):
        # 识别手牌中的种族
        hand_minions = [c for c in self.controller.hand if c.type == CardType.MINION]
        by_race = {}
        for m in hand_minions:
            if m.race != Race.INVALID: # 通常只计算有具体种族的
                if m.race not in by_race:
                    by_race[m.race] = []
                by_race[m.race].append(m)
        
        for race, minions in by_race.items():
            if minions:
                # 随机选择一张复制
                target = self.game.random.choice(minions)
                yield Give(CONTROLLER, ExactCopy(target))
