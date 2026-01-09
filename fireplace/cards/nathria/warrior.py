"""纳斯利亚堡的悬案（Murder at Castle Nathria）卡牌实现"""
from ..utils import *


class MAW_027:
    """Call to the Stand - 传唤出庭
    Your opponent summons a random minion from their hand.
    你的对手从其手牌中随机召唤一个随从。
    """
    def play(self):
        # 对手从手牌中随机召唤一个随从
        opponent_minions = [card for card in self.controller.opponent.hand if card.type == CardType.MINION]
        if opponent_minions:
            minion = self.game.random.choice(opponent_minions)
            yield Summon(OPPONENT, minion)


class MAW_028:
    """Mawsworn Bailiff - 渊誓者法警
    <b><b>Taunt</b>.</b> <b>Battlecry:</b> If you have 4 or more Armor, gain +4/+4.
    <b>嘲讽，战吼：</b>如果你有4点或更多护甲值，便获得+4/+4。
    """
    tags = {GameTag.TAUNT: True}

    def play(self):
        # 检查护甲值
        if self.controller.hero.armor >= 4:
            yield Buff(SELF, "MAW_028e")


class MAW_028e:
    """Mawsworn Bailiff Buff - 渊誓者法警增益"""
    atk = 4
    max_health = 4


class MAW_029:
    """Weapons Expert - 武器专家
    <b>Battlecry:</b> If you have a weapon equipped, give it +1/+1. Otherwise, draw a weapon.
    <b>战吼：</b>如果你装备了武器，使其获得+1/+1。否则，抽一张武器牌。
    """
    def play(self):
        if self.controller.weapon:
            # 有武器：给予+1/+1
            yield Buff(self.controller.weapon, "MAW_029e")
        else:
            # 没有武器：抽一张武器牌
            yield Draw(CONTROLLER, FRIENDLY_DECK + WEAPON)


class MAW_029e:
    """Weapons Expert Buff - 武器专家增益"""
    atk = 1
    max_health = 1


class REV_006:
    """Suspicious Pirate - 可疑的海盗
    <b>Battlecry:</b> <b>Discover</b> a weapon. If your opponent guesses your choice, they get a copy.
    <b>战吼：</b><b>发现</b>一张武器牌。如果你的对手猜中了你的选择，其便获得一张复制。
    """
    # 使用 DiscoverWithPendingGuess 实现完整的"对手猜测"机制
    # 流程：
    # 1. 玩家发现一张武器（从3个选项中选择）
    # 2. 记录选项和选择到对手的 pending_guesses 队列
    # 3. 在对手回合开始时，对手从相同选项中猜测
    # 4. 如果猜中，对手也获得一张复制
    play = DiscoverWithPendingGuess(CONTROLLER, RandomWeapon())


class REV_316:
    """Remornia, Living Blade - 活体利刃蕾茉妮雅
    <b>Rush</b>
After this attacks, equip it.
    <b>突袭</b>。在其攻击后，将其装备。

    7费 4/10 随从
    攻击后装备 4/X 武器（X=当前生命值，满耐久）
    BUFF 不保留，只保留生命值作为最大耐久度
    转换不触发亡语
    """
    tags = {GameTag.RUSH: True}

    # 攻击后装备武器
    def _equip_weapon(self, source, target):
        if source == OWNER:
            # 记录当前生命值
            current_health = self.health

            # 静默移除随从（不触发亡语）
            self.zone = Zone.SETASIDE

            # 装备武器：4攻，最大耐久度=当前生命值
            weapon = yield Summon(CONTROLLER, "REV_316t")
            if weapon:
                # 设置最大耐久度（如果不是10）
                if current_health != 10:
                    # 通过 buff 修改最大耐久度
                    health_diff = current_health - 10
                    yield Buff(weapon, "REV_316e", health_bonus=health_diff)

    events = Attack(SELF).after(_equip_weapon)


class REV_316e:
    """Remornia Durability Buff - 蕾茉妮雅耐久度调整"""
    def __init__(self, *args, health_bonus=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_health = health_bonus


class REV_316t:
    """Remornia Weapon - 蕾茉妮雅武器
    4/10 武器（基础）
    英雄攻击后召唤 4/X 随从（X=当前耐久度，满血）
    转换不触发亡语
    """
    # 英雄攻击后召唤随从
    def _summon_minion(self, source, target):
        if source == FRIENDLY_HERO:
            # 记录当前耐久度
            current_durability = self.durability

            # 静默移除武器（不触发亡语）
            self.zone = Zone.SETASIDE

            # 召唤随从：4攻，最大生命值=当前耐久度
            minion = yield Summon(CONTROLLER, "REV_316")
            if minion:
                # 设置最大生命值（如果不是10）
                if current_durability != 10:
                    # 通过 buff 修改最大生命值
                    health_diff = current_durability - 10
                    yield Buff(minion, "REV_316e", health_bonus=health_diff)

    events = Attack(FRIENDLY_HERO).after(_summon_minion)


class REV_332:
    """Anima Extractor - 心能提取者
    [x]Whenever a friendly
minion takes damage,
give a random minion in
your hand +1/+1.
    每当一个友方随从受到伤害时，随机使你手牌中的一个随从获得+1/+1。
    """
    # 监听友方随从受伤
    def _buff_hand_minion(self, source, target, amount, source_entity=None):
        # 随机选择手牌中的一个随从
        hand_minions = [card for card in self.controller.hand if card.type == CardType.MINION]
        if hand_minions:
            minion = self.game.random.choice(hand_minions)
            yield Buff(minion, "REV_332e")

    events = Damage(FRIENDLY_MINIONS).on(_buff_hand_minion)


class REV_332e:
    """Anima Extractor Buff - 心能提取者增益"""
    atk = 1
    max_health = 1


class REV_334:
    """Burden of Pride - 骄傲罪责
    [x]Summon three 1/3
Jailers with <b>Taunt</b>. If you
have 20 or less Health,
give them +1/+1.
    召唤三个1/3并具有<b>嘲讽</b>的狱卒。如果你的生命值为20点或更少，使其获得+1/+1。
    """
    def play(self):
        # 召唤三个狱卒
        jailers = []
        for i in range(3):
            jailer = yield Summon(CONTROLLER, "REV_334t")
            if jailer:
                jailers.append(jailer)

        # 检查生命值
        if self.controller.hero.health <= 20:
            for jailer in jailers:
                yield Buff(jailer, "REV_334e")


class REV_334t:
    """Jailer - 狱卒"""
    # Token: 1/3 嘲讽
    tags = {GameTag.TAUNT: True}


class REV_334e:
    """Burden of Pride Buff - 骄傲罪责增益"""
    atk = 1
    max_health = 1


class REV_337:
    """Riot! - 动乱
    [x]Your minions can't be
reduced below 1 Health
this turn. They each attack
a random enemy minion.
    在本回合中，你的随从的生命值无法被降至1点以下。每个随从随机攻击一个敌方随从。
    """
    def play(self):
        # 给所有友方随从添加buff（无法降至1点以下）
        for minion in list(FRIENDLY_MINIONS.eval(self.game, self)):
            yield Buff(minion, "REV_337e")

        # 让每个随从攻击随机敌方随从
        for minion in list(FRIENDLY_MINIONS.eval(self.game, self)):
            enemy_minions = list(ENEMY_MINIONS.eval(self.game, self))
            if enemy_minions and minion.can_attack():
                target = self.game.random.choice(enemy_minions)
                yield Attack(minion, target)


class REV_337e:
    """Riot! Effect - 动乱效果"""
    # 无法降至1点以下
    # 使用 MINIMUM_HEALTH 标签实现
    tags = {enums.MINIMUM_HEALTH: 1}

    # 回合结束时移除
    events = TURN_END.on(Destroy(SELF))


class REV_930:
    """Crazed Wretch - 疯狂的可怜鬼
    Has +2 Attack and <b>Charge</b> while damaged.
    在受伤时，获得+2攻击力和<b>冲锋</b>。
    """
    # 动态属性：受伤时+2攻击和冲锋
    # 使用 update 持续更新
    update = (
        Refresh(SELF + DAMAGED, {GameTag.ATK: +2, GameTag.CHARGE: True}),
        Refresh(SELF - DAMAGED, {GameTag.CHARGE: False})
    )


class REV_931:
    """Conqueror's Banner - 征服者战旗
    Reveal a card from each player's deck, three times. Draw any of yours that cost more.
    从双方牌库中各揭示一张牌，重复三次。抽出你的所有法力值消耗更多的牌。
    """
    def play(self):
        # 重复3次
        for i in range(3):
            # 揭示己方牌库的一张牌
            friendly_cards = list(FRIENDLY_DECK.eval(self.game, self))
            if friendly_cards:
                friendly_card = self.game.random.choice(friendly_cards)

                # 揭示对手牌库的一张牌
                enemy_cards = list(ENEMY_DECK.eval(self.game, self))
                if enemy_cards:
                    enemy_card = self.game.random.choice(enemy_cards)

                    # 如果己方卡牌费用更高，抽出它
                    if friendly_card.cost > enemy_card.cost:
                        yield Draw(CONTROLLER, friendly_card)


class REV_933:
    """Imbued Axe - 灌能战斧
    [x]After your hero attacks,
give your damaged minions
+1/+2. <b>Infuse (2):</b>
+2/+2 instead.
    在你的英雄攻击后，使你受伤的随从获得+1/+2。<b>注能(2)：</b>改为+2/+2。
    """
    infuse = 2

    # 英雄攻击后触发
    def _buff_damaged_minions(self, source, target):
        if source == FRIENDLY_HERO:
            # 根据是否注能，给予不同的buff
            # 直接检查 infused 属性（无需 __init__）
            buff_id = "REV_933e2" if getattr(self, 'infused', False) else "REV_933e"

            # 给所有受伤的友方随从buff
            for minion in FRIENDLY_MINIONS.eval(self.game, self):
                if minion.damage > 0:
                    yield Buff(minion, buff_id)

    events = Attack(FRIENDLY_HERO).after(_buff_damaged_minions)


class REV_933e:
    """Imbued Axe Buff - 灌能战斧增益"""
    atk = 1
    max_health = 2


class REV_933e2:
    """Imbued Axe Infused Buff - 灌能战斧注能增益"""
    atk = 2
    max_health = 2


class REV_934:
    """Decimator Olgra - 屠戮者奥格拉
    [x]<b>Battlecry:</b> Gain +1/+1
for each damaged minion,
 then attack all enemies.
    <b>战吼：</b>每有一个受伤的随从，便获得+1/+1，然后攻击所有敌人。
    """
    def play(self):
        # 计算受伤随从数量
        damaged_count = len([m for m in ALL_MINIONS.eval(self.game, self) if m.damage > 0])

        # 获得buff
        if damaged_count > 0:
            for i in range(damaged_count):
                yield Buff(SELF, "REV_934e")

        # 攻击所有敌人
        for enemy in list((ENEMY_MINIONS | ENEMY_HERO).eval(self.game, self)):
            if self.can_attack():
                yield Attack(SELF, enemy)


class REV_934e:
    """Decimator Olgra Buff - 屠戮者奥格拉增益"""
    atk = 1
    max_health = 1


class REV_990:
    """Sanguine Depths - 赤红深渊
    [x]Deal 1 damage to a
minion and give it
+2 Attack.
    对一个随从造成1点伤害，并使其获得+2攻击力。
    """
    # LOCATION 地标
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    def activate(self):
        # 造成1点伤害
        yield Hit(TARGET, 1)
        # 给予+2攻击力
        yield Buff(TARGET, "REV_990e")


class REV_990e:
    """Sanguine Depths Buff - 赤红深渊增益"""
    atk = 2


