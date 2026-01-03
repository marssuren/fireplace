"""巫妖王的进军 - 德鲁伊 (March of the Lich King - Druid)"""
from ..utils import *


class RLK_650:
    """盘桓僵尸 (Lingering Zombie)
    亡语：召唤一个1/1并具有"亡语：召唤一个1/1的僵尸"的徒手僵尸。
    机制: DEATHRATTLE
    """
    deathrattle = Summon(CONTROLLER, "RLK_650t")


class RLK_650t:
    """徒手僵尸 (Unarmed Zombie)
    1/1 亡语：召唤一个1/1的僵尸
    """
    deathrattle = Summon(CONTROLLER, "RLK_650t2")


class RLK_650t2:
    """僵尸 (Zombie)
    1/1
    """
    # Token 卡牌
    pass


class RLK_651:
    """地穴看守者 (Crypt Keeper)
    嘲讽。你每有1点护甲值，本牌的法力值消耗便减少（1）点。
    机制: TAUNT
    """
    tags = {GameTag.TAUNT: True}

    class Hand:
        # 根据护甲值减费
        def cost_mod(self, source, game):
            return -source.controller.hero.armor


class RLK_652:
    """无尽虫群 (Unending Swarm)
    复活所有法力值消耗小于或等于（2）点的友方随从。
    """
    def play(self):
        # 获取所有费用<=2的死亡友方随从
        targets = [card for card in self.controller.graveyard
                   if card.type == CardType.MINION and card.cost <= 2]
        # 复活所有符合条件的随从
        for target in targets:
            yield Summon(CONTROLLER, target.id)


class RLK_654:
    """甲虫通灵术 (Beetlemancy)
    抉择：获得12点护甲值；或者召唤两只3/3并具有嘲讽的甲虫。
    机制: CHOOSE_ONE
    """
    choose = ("RLK_654a", "RLK_654b")


class RLK_654a:
    """甲虫通灵术（选项1）- 获得护甲"""
    play = Armor(CONTROLLER, 12)


class RLK_654b:
    """甲虫通灵术（选项2）- 召唤甲虫"""
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "RLK_654t") * 2


class RLK_654t:
    """甲虫 (Beetle)
    3/3 嘲讽
    """
    # Token 卡牌
    pass


class RLK_655:
    """枯萎 (Wither)
    选择一个随从。每个友方亡灵各从选中的随从处偷取1点攻击力和生命值。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }

    def play(self):
        # 获取所有友方亡灵
        undeads = self.controller.field.filter(race=Race.UNDEAD)
        count = len(undeads)

        if count > 0:
            # 目标失去攻击力和生命值
            yield Buff(TARGET, "RLK_655e", atk=-count, health=-count)
            # 每个亡灵获得+1/+1
            for undead in undeads:
                yield Buff(undead, "RLK_655e2")


class RLK_655e:
    """枯萎减益 (Wither Debuff)"""
    # 动态设置攻击力和生命值减少
    pass


class RLK_655e2:
    """枯萎增益 (Wither Buff)"""
    atk = 1
    health = 1


class RLK_656:
    """壳质护板 (Chitinous Plating)
    获得4点护甲值。在你的下个回合开始时，再获得4点。
    """
    def play(self):
        # 立即获得4点护甲
        yield Armor(CONTROLLER, 4)
        # 给控制器添加buff，下回合开始时再获得4点护甲
        yield Buff(FRIENDLY_HERO, "RLK_656e")


class RLK_656e:
    """壳质护板增益 (Chitinous Plating Buff)"""
    events = OwnTurnBegin(CONTROLLER).on(
        Armor(CONTROLLER, 4),
        Destroy(SELF)  # 触发后移除buff
    )


class RLK_657:
    """地底虫王 (Underking)
    突袭。战吼，亡语：获得6点护甲值。
    机制: BATTLECRY, DEATHRATTLE, RUSH
    """
    tags = {GameTag.RUSH: True}
    play = Armor(CONTROLLER, 6)
    deathrattle = Armor(CONTROLLER, 6)


class RLK_658:
    """纳多克斯长老 (Elder Nadox)
    战吼：消灭一个友方亡灵，你的所有随从获得其攻击力。
    机制: BATTLECRY
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.UNDEAD
    }

    def play(self):
        if TARGET:
            # 获取目标的攻击力
            atk = TARGET.atk
            # 消灭目标
            yield Destroy(TARGET)
            # 所有友方随从获得攻击力
            if atk > 0:
                yield Buff(FRIENDLY_MINIONS, "RLK_658e", atk=atk)


class RLK_658e:
    """纳多克斯长老增益 (Elder Nadox Buff)"""
    # 动态设置攻击力
    pass


class RLK_659:
    """阿努布雷坎 (Anub'Rekhan)
    战吼：获得5点护甲值。在本回合中，你的下3张随从牌消耗护甲值而非法力值。
    机制: BATTLECRY
    """
    def play(self):
        # 获得5点护甲
        yield Armor(CONTROLLER, 5)
        # 给控制器添加buff，下3张随从消耗护甲而非法力
        yield Buff(FRIENDLY_HERO, "RLK_659e")


class RLK_659e:
    """阿努布雷坎增益 (Anub'Rekhan Buff)
    追踪打出的随从数量，前3张随从消耗护甲而非法力
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minions_played = 0

    # 监听随从打出事件
    events = [
        # 随从打出后：消耗护甲值（等于随从费用）
        Play(CONTROLLER, MINION).after(
            lambda self, source, card: [
                SpendArmor(FRIENDLY_HERO, card.cost),  # 使用核心扩展的 SpendArmor
                setattr(self, 'minions_played', getattr(self, 'minions_played', 0) + 1),
                Destroy(SELF) if getattr(self, 'minions_played', 0) >= 3 else None
            ]
        ),
        # 回合结束时移除
        OWN_TURN_END.on(Destroy(SELF))
    ]

    class Hand:
        # 修改随从的费用计算方式：费用变为0（因为用护甲支付）
        def cost_mod(self, source, game):
            if source.type == CardType.MINION:
                # 检查是否有足够的护甲
                if source.controller.hero.armor >= source.cost:
                    return -source.cost
                else:
                    # 护甲不足，不减费（无法打出）
                    return 0


class RLK_956:
    """蛛魔飞虫 (Nerubian Flyer)
    战吼：如果在你的上回合之后有友方亡灵死亡，召唤一个2/2的蛛魔。
    机制: BATTLECRY
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}

    def play(self):
        # 检查上回合之后是否有友方亡灵死亡
        if self.controller.undead_died_last_turn:
            yield Summon(CONTROLLER, "RLK_956t")


class RLK_956t:
    """蛛魔 (Nerubian)
    2/2
    """
    # Token 卡牌
    pass


