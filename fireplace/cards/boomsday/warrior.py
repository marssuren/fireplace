from ..utils import *


##
# Minions


class BOT_059:
    """Eternium Rover / 恒金巡游者
    每当本随从受到伤害，获得2点护甲值。"""

    # Whenever this minion takes damage, gain 2_Armor.
    events = Damage(SELF).on(GainArmor(FRIENDLY_HERO, 2))


class BOT_104:
    """Dyn-o-matic / 掷弹机器人
    战吼：造成5点伤害，随机分配到所有非机械随从身上。"""

    # <b>Battlecry:</b> Deal 5 damage randomly split among all minions_except_Mechs.
    play = Hit(RANDOM(ALL_MINIONS - MECH), 1) * 5


class BOT_218:
    """Security Rover / 安保巡游者
    每当本随从受到伤害，召唤一个2/3并具有嘲讽的机械。"""

    # [x]Whenever this minion takes damage, summon a 2/3 Mech with <b>Taunt</b>.
    events = Damage(SELF).on(Summon(CONTROLLER, "BOT_218t"))


class BOT_237:
    """Beryllium Nullifier / 铍金毁灭者
    磁力。扰魔"""

    # <b>Magnetic</b> Can't be targeted by spells or Hero Powers.
    magnetic = MAGNETIC("BOT_237e")


BOT_237e = buff(cant_be_targeted_by_spells=True, cant_be_targeted_by_hero_powers=True)


##
# Spells


class BOT_042:
    """Weapons Project / 武器计划
    每个玩家装备一把2/3的武器，并获得6点护甲值。"""

    # Each player equips a 2/3 Weapon and gains 6 Armor.
    play = Summon(ALL_PLAYERS, "BOT_042t"), GainArmor(IN_PLAY + HERO, 6)


class BOT_067:
    """Rocket Boots / 火箭靴
    使一个随从获得突袭。抽 一张牌。"""

    # Give a minion <b>Rush</b>. Draw a card.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Buff(TARGET, "BOT_067e"), Draw(CONTROLLER)


BOT_067e = buff(rush=True)


class BOT_069:
    """The Boomship / 砰砰飞艇
    随机从你的手牌中召唤三个随从，并使其获得突袭。"""

    # Summon 3 random minions from your hand. Give them <b>Rush</b>.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + MINION) * 3).then(
        Buff(Summon.CARD, "BOT_069e")
    )


BOT_069e = buff(rush=True)


class BOT_299:
    """Omega Assembly / 欧米茄装配
    发现一张机械牌。如果你有十个法力水晶，改为保留全部三张牌。"""

    # [x]<b>Discover</b> a Mech. If you have 10 Mana Crystals, keep all 3 cards.
    powered_up = AT_MAX_MANA(CONTROLLER)
    play = powered_up & Give(CONTROLLER, RandomMech()) * 3 | DISCOVER(RandomMech())


##
# Weapons


class BOT_406:
    """Supercollider / 超级对撞器
    在你攻击一个随从后，迫使其攻击相邻的一个 随从。"""

    # [x]After you attack a minion, force it to attack one of its neighbors.
    events = Attack(FRIENDLY_HERO, MINION).after(
        Find(ADJACENT(Attack.DEFENDER))
        & Attack(Attack.DEFENDER, RANDOM(ADJACENT(Attack.DEFENDER)))
    )


##
# Heros


class BOT_238:
    """Dr. Boom, Mad Genius / “科学狂人”砰砰博士
    战吼：在本局对战的剩余时间内，你的所有机械拥有 突袭。"""

    # <b>Battlecry:</b> For the rest of the game, your Mechs have <b>Rush</b>.
    entourage = [
        "BOT_238p1",
        "BOT_238p2",
        "BOT_238p3",
        "BOT_238p4",
        "BOT_238p6",
    ]
    play = (Buff(CONTROLLER, "BOT_238e"), Summon(CONTROLLER, RandomEntourage()))


class BOT_238e:
    update = Refresh(FRIENDLY + MECH, {GameTag.RUSH: True})


class BOT_238p:
    """Dr. Boom 基础英雄技能
    每回合结束时随机切换到5种英雄技能之一"""
    entourage = BOT_238.entourage
    
    # 回合结束时随机切换英雄技能
    events = OWN_TURN_END.on(lambda self: self._switch_hero_power())
    
    def _switch_hero_power(self):
        """随机切换到一个新的英雄技能"""
        import random
        controller = self.controller
        
        # 随机选择一个新的英雄技能（从5个中选择）
        new_power_id = random.choice(self.entourage)
        
        # 创建新的英雄技能
        new_power = controller.card(new_power_id, source=controller.hero)
        
        # 替换英雄技能
        if controller.hero.power:
            controller.hero.power.zone = Zone.GRAVEYARD
        controller.hero.power = new_power
        new_power.controller = controller
        new_power.zone = Zone.PLAY


class BOT_238p1:
    """大红按钮 / Big Red Button
    造成$3点伤害"""
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    entourage = BOT_238.entourage
    activate = Hit(TARGET, 3)
    
    # 回合结束时切换英雄技能
    events = OWN_TURN_END.on(lambda self: self._switch_hero_power())
    
    def _switch_hero_power(self):
        """切换到另一个随机英雄技能（排除当前技能）"""
        import random
        controller = self.controller
        
        # 排除当前技能
        available_powers = [p for p in self.entourage if p != self.id]
        new_power_id = random.choice(available_powers)
        
        # 创建并替换英雄技能
        new_power = controller.card(new_power_id, source=controller.hero)
        if controller.hero.power:
            controller.hero.power.zone = Zone.GRAVEYARD
        controller.hero.power = new_power
        new_power.controller = controller
        new_power.zone = Zone.PLAY


class BOT_238p2:
    """轰炸装甲 / KABOOM!
    获得7点护甲值"""
    entourage = BOT_238.entourage
    activate = GainArmor(FRIENDLY_HERO, 7)
    
    events = OWN_TURN_END.on(lambda self: self._switch_hero_power())
    
    def _switch_hero_power(self):
        import random
        controller = self.controller
        available_powers = [p for p in self.entourage if p != self.id]
        new_power_id = random.choice(available_powers)
        new_power = controller.card(new_power_id, source=controller.hero)
        if controller.hero.power:
            controller.hero.power.zone = Zone.GRAVEYARD
        controller.hero.power = new_power
        new_power.controller = controller
        new_power.zone = Zone.PLAY


class BOT_238p3:
    """炸弹投掷器 / Zap Cannon
    对所有敌人造成$1点伤害"""
    entourage = BOT_238.entourage
    activate = Hit(ENEMY_CHARACTERS, 1)
    
    events = OWN_TURN_END.on(lambda self: self._switch_hero_power())
    
    def _switch_hero_power(self):
        import random
        controller = self.controller
        available_powers = [p for p in self.entourage if p != self.id]
        new_power_id = random.choice(available_powers)
        new_power = controller.card(new_power_id, source=controller.hero)
        if controller.hero.power:
            controller.hero.power.zone = Zone.GRAVEYARD
        controller.hero.power = new_power
        new_power.controller = controller
        new_power.zone = Zone.PLAY


class BOT_238p4:
    """交付无人机 / Delivery Drone
    发现一张机械牌"""
    requirements = {
        PlayReq.REQ_HAND_NOT_FULL: 0,
    }
    entourage = BOT_238.entourage
    activate = DISCOVER(RandomMech())
    
    events = OWN_TURN_END.on(lambda self: self._switch_hero_power())
    
    def _switch_hero_power(self):
        import random
        controller = self.controller
        available_powers = [p for p in self.entourage if p != self.id]
        new_power_id = random.choice(available_powers)
        new_power = controller.card(new_power_id, source=controller.hero)
        if controller.hero.power:
            controller.hero.power.zone = Zone.GRAVEYARD
        controller.hero.power = new_power
        new_power.controller = controller
        new_power.zone = Zone.PLAY


class BOT_238p6:
    """微型机器人工厂 / Micro-Squad
    召唤三个1/1的微型机器人"""
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    entourage = BOT_238.entourage
    activate = Summon(CONTROLLER, "BOT_312t") * 3
    
    events = OWN_TURN_END.on(lambda self: self._switch_hero_power())
    
    def _switch_hero_power(self):
        import random
        controller = self.controller
        available_powers = [p for p in self.entourage if p != self.id]
        new_power_id = random.choice(available_powers)
        new_power = controller.card(new_power_id, source=controller.hero)
        if controller.hero.power:
            controller.hero.power.zone = Zone.GRAVEYARD
        controller.hero.power = new_power
        new_power.controller = controller
        new_power.zone = Zone.PLAY

