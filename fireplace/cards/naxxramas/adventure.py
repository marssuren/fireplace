from ..utils import *


##
# Hero Powers


class NAX1_04:
    """Skitter / 飞掠召唤
    召唤一个3/1的蛛魔。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "NAX1_03")


class NAX1h_04:
    """Skitter (Heroic)"""

    activate = Summon(CONTROLLER, "NAX1h_03")


class NAX2_03:
    """Rain of Fire / 火焰之雨
    你的对手每有一张手牌，便发射一枚飞弹。"""

    activate = Hit(RANDOM_ENEMY_MINION, 1) * Count(ENEMY_HAND)


class NAX2_03H:
    """Rain of Fire / 火焰之雨
    你的对手每有一张手牌，便发射一枚飞弹。"""

    activate = Hit(RANDOM_ENEMY_MINION, 1) * Count(ENEMY_HAND)


class NAX2_05:
    """Worshipper / 膜拜者
    你的英雄在你的回合拥有+1攻击力。"""

    update = CurrentPlayer(CONTROLLER) & Refresh(FRIENDLY_HERO, {GameTag.ATK: +1})


class NAX2_05H:
    """Worshipper / 膜拜者
    你的英雄在你的回合拥有+3攻击力。"""

    update = CurrentPlayer(CONTROLLER) & Refresh(FRIENDLY_HERO, {GameTag.ATK: +3})


class NAX3_02:
    """Web Wrap / 裹体之网
    随机将一个敌方随从移回对手的 手牌。"""

    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    activate = Bounce(RANDOM_ENEMY_MINION)


class NAX3_02H:
    """Web Wrap / 裹体之网
    随机将两个敌方随从移回对手的 手牌。"""

    activate = Bounce(RANDOM_ENEMY_MINION * 2)


class NAX4_04:
    """Raise Dead / 亡者复生
    被动 每当一个敌人死亡，召唤一个1/1的骷髅。"""

    events = Death(ENEMY + MINION).on(Summon(CONTROLLER, "NAX4_03"))


class NAX4_04H:
    """Raise Dead / 亡者复生
    被动 每当一个敌人死亡，召唤一个5/5的骷髅。"""

    events = Death(ENEMY + MINION).on(Summon(CONTROLLER, "NAX4_03H"))


class NAX5_02:
    """Eruption / 爆发
    对最左边的敌方随从造成2点伤害。"""

    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    activate = Hit(ENEMY_MINIONS[0], 2)


class NAX5_02H:
    """Eruption / 爆发
    对位于最左边的敌方随从造成3点 伤害。"""

    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 0}
    activate = Hit(ENEMY_MINIONS[0], 3)


class NAX6_02:
    """Necrotic Aura / 死灵光环
    对敌方英雄造成3点伤害。"""

    activate = Hit(ENEMY_HERO, 3)


class NAX6_02H:
    """Necrotic Aura / 死灵光环
    对敌方英雄造成3点伤害。"""

    activate = Hit(ENEMY_HERO, 3)


class NAX7_03:
    """Unbalancing Strike / 重压打击
    造成3点伤害。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Hit(TARGET, 3)


class NAX7_03H:
    """Unbalancing Strike / 重压打击
    造成4点伤害。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Hit(TARGET, 4)


class NAX8_02:
    """Harvest / 收割
    抽一张牌。"""

    activate = Draw(CONTROLLER)


class NAX8_02H:
    """Harvest / 收割
    抽一张牌。获得一个法力水晶。"""

    activate = Draw(CONTROLLER), GainMana(CONTROLLER, 1)


class NAX9_06:
    """Unholy Shadow / 邪恶之影
    抽两张牌。"""

    activate = Draw(CONTROLLER) * 2


class NAX10_03:
    """Hateful Strike / 仇恨打击
    消灭一个随从。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Destroy(TARGET)


class NAX10_03H:
    """Hateful Strike / 仇恨打击
    消灭一个随从。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Destroy(TARGET)


class NAX11_02:
    """Poison Cloud / 毒云
    对所有随从造成1点伤害。每死亡一个随从，召唤一个泥浆怪。"""

    activate = Hit(ALL_MINIONS, 1).then(
        Dead(Hit.TARGET) & Summon(CONTROLLER, "NAX11_03")
    )


class NAX11_02H:
    """Poison Cloud / 毒云
    对所有敌人造成2点伤害。每死亡一个随从，召唤一个泥浆怪。"""

    activate = Hit(ENEMY_CHARACTERS, 2).then(
        Dead(Hit.TARGET) & Summon(CONTROLLER, "NAX11_03")
    )


class NAX12_02:
    """Decimate / 残杀
    将所有随从的生命值变为1。"""

    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    activate = Buff(ENEMY_MINIONS, "NAX12_02e")


class NAX12_02H:
    """Decimate / 残杀
    将所有敌方随从的生命值变为1。"""

    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    activate = Buff(ENEMY_MINIONS, "NAX12_02e")


class NAX12_02e:
    max_health = SET(1)


class NAX13_02:
    """Polarity Shift / 极性转换
    使所有随从的攻击力和生命值互换。"""

    activate = Buff(ALL_MINIONS, "NAX13_02e")


NAX13_02e = AttackHealthSwapBuff()


class NAX14_02:
    """Frost Breath / 冰霜吐息
    消灭所有没有被冻结的敌方随从。"""

    activate = Destroy(ENEMY_MINIONS - FROZEN - ADJACENT(ID("NAX14_03")))


class NAX15_02:
    """Frost Blast / 冰霜冲击
    对敌方英雄造成2点 伤害，并使其 冻结。"""

    activate = Hit(ENEMY_HERO, 2), Freeze(ENEMY_HERO)


class NAX15_02H:
    """Frost Blast / 冰霜冲击
    对敌方英雄造成3点 伤害，并使其 冻结。"""

    activate = Hit(ENEMY_HERO, 3), Freeze(ENEMY_HERO)


class NAX15_04:
    """Chains / 锁链
    随机夺取一个敌方随从的控制权，直到回合结束。"""

    activate = Steal(TARGET), Buff(TARGET, "NAX15_04a")


class NAX15_04a:
    events = TURN_END.on(Destroy(SELF))

    def destroy(self):
        self.controller.opponent.steal(self.owner)


class NAX15_04H:
    """Chains / 锁链
    随机夺取一个敌方随从的控制权。"""

    activate = Steal(RANDOM_ENEMY_MINION)


##
# Minions


class FP1_006:
    """Deathcharger / 死亡战马
    冲锋，亡语：对你的英雄造成3点伤害。"""

    deathrattle = Hit(FRIENDLY_HERO, 3)


class NAX8_03:
    """Unrelenting Trainee / 冷酷学徒
    亡语：为你的对手召唤一个鬼灵学徒。"""

    deathrattle = Summon(OPPONENT, "NAX8_03t")


class NAX8_03t:
    """Spectral Trainee"""

    events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_HERO, 1))


class NAX8_04:
    """Unrelenting Warrior / 冷酷战士
    亡语：为你的对手召唤一个鬼灵战士。"""

    deathrattle = Summon(OPPONENT, "NAX8_04t")


class NAX8_04t:
    """Spectral Warrior"""

    events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_HERO, 1))


class NAX8_05:
    """Unrelenting Rider / 冷酷骑兵
    亡语：为你的对手召唤一个鬼灵骑兵。"""

    deathrattle = Summon(OPPONENT, "NAX8_05t")


class NAX8_05t:
    """Spectral Rider"""

    events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_HERO, 1))


class NAX9_02:
    """Lady Blaumeux / 女公爵布劳缪克丝
    你的英雄免疫。"""

    update = Refresh(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: True})


class NAX9_02H:
    """Lady Blaumeux / 女公爵布劳缪克丝
    你的英雄免疫。"""

    update = Refresh(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: True})


class NAX9_03:
    """Thane Korth'azz / 库尔塔兹领主
    你的英雄免疫。"""

    update = Refresh(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: True})


class NAX9_03H:
    """Thane Korth'azz / 库尔塔兹领主
    你的英雄免疫。"""

    update = Refresh(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: True})


class NAX9_04:
    """Sir Zeliek / 瑟里耶克爵士
    你的英雄免疫。"""

    update = Refresh(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: True})


class NAX9_04H:
    """Sir Zeliek / 瑟里耶克爵士
    你的英雄免疫。"""

    update = Refresh(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: True})


class NAX14_03:
    """Frozen Champion / 被冰封的勇士
    被永久冻结。相邻的随从免疫冰霜吐息。"""

    update = Refresh(SELF, {GameTag.FROZEN: True})


class NAXM_001:
    """Necroknight / 死灵骑士
    亡语：消灭与本随从相邻的随从。"""

    deathrattle = Destroy(SELF_ADJACENT)


class NAXM_002:
    """Skeletal Smith / 骷髅铁匠
    亡语：摧毁对手的武器。"""

    deathrattle = Destroy(ENEMY_WEAPON)


##
# Spells


class NAX1_05:
    """Locust Swarm / 虫群风暴
    对所有敌方随从造成$3点伤害。为你的英雄恢复#3点生命值。"""

    play = Hit(ENEMY_MINIONS, 3), Heal(FRIENDLY_HERO, 3)


class NAX3_03:
    """Necrotic Poison / 死灵毒药
    消灭一个随从。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Destroy(TARGET)


class NAX4_05:
    """Plague / 瘟疫
    消灭所有不是骷髅的随从。"""

    play = Destroy(ALL_MINIONS - ID("NAX4_03") - ID("NAX4_03H"))


class NAX5_03:
    """Mindpocalypse / 心智末日
    双方玩家各抽两张牌，获得一个法力水晶。"""

    play = Draw(ALL_PLAYERS) * 2, GainMana(ALL_PLAYERS, 1)


class NAX6_03:
    """Deathbloom / 死亡之花
    对一个随从造成$5点伤害。召唤一个孢子。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 5), Summon(CONTROLLER, "NAX6_03t")


class NAX6_03t:
    deathrattle = Buff(ENEMY_MINIONS, "NAX6_03te")


NAX6_03te = buff(atk=8)


class NAX6_04:
    """Sporeburst / 孢子爆发
    对所有敌方随从造成$1点伤害。召唤一个孢子。"""

    play = Hit(ENEMY_MINIONS, 1), Summon(CONTROLLER, "NAX6_03t")


class NAX7_05:
    """Mind Control Crystal / 精神控制水晶
    激活水晶来控制死亡学员！"""

    play = Steal(ENEMY_MINIONS + ID("NAX7_02"))


class NAX9_07:
    """Mark of the Horsemen / 骑士印记
    使你的所有随从和武器获得+1/+1。"""

    play = Buff(FRIENDLY + (WEAPON | MINION), "NAX9_07e")


NAX9_07e = buff(+1, +1)


class NAX11_04:
    """Mutating Injection / 变异注射
    使一个随从获得+4/+4和嘲讽。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "NAX11_04e")


NAX11_04e = buff(+4, +4, taunt=True)


class NAX12_04:
    """Enrage / 激怒
    在本回合中，使你的英雄获得+6攻击力。"""

    play = Buff(SELF, "NAX12_04e")


NAX12_04e = buff(atk=6)


class NAX13_03:
    """Supercharge / 增压
    使你的所有随从获得+2生命值。"""

    play = Buff(FRIENDLY_MINIONS, "NAX13_03e")


NAX13_03e = buff(health=2)


class NAX14_04:
    """Pure Cold / 极寒之击
    对敌方英雄造成$8点伤害，并使其冻结。"""

    play = Hit(ENEMY_HERO, 8), Freeze(ENEMY_HERO)


##
# Weapons


class NAX7_04:
    """Massive Runeblade / 符文巨剑
    对英雄造成双倍伤害。"""

    update = Attacking(FRIENDLY_HERO, HERO) & Refresh(SELF, {GameTag.ATK: +5})


class NAX7_04H:
    """Massive Runeblade / 符文巨剑
    对英雄造成双倍伤害。"""

    update = Attacking(FRIENDLY_HERO, HERO) & Refresh(SELF, {GameTag.ATK: +10})


class NAX9_05:
    """Runeblade / 符文剑
    如果其他天启骑士死亡，拥有 +3攻击力。"""

    update = Find(ID("NAX9_02") | ID("NAX9_03") | ID("NAX9_04")) & Refresh(
        SELF, {GameTag.ATK: +3}
    )


class NAX9_05H:
    """Runeblade / 符文剑
    如果其他天启骑士死亡，拥有 +6攻击力。"""

    update = Find(ID("NAX9_02H") | ID("NAX9_03H") | ID("NAX9_04H")) & Refresh(
        SELF, {GameTag.ATK: +6}
    )


class NAX10_02:
    """Hook / 铁钩
    亡语：将这把武器移回你的手牌。"""

    deathrattle = Give(CONTROLLER, "NAX10_02")


class NAX10_02H:
    """Hook / 铁钩
    风怒，亡语： 将这把武器移回你的手牌。"""

    deathrattle = Give(CONTROLLER, "NAX10_02H")


class NAX12_03:
    """Jaws / 巨颚
    每当一个具有亡语的随从死亡，便获得+2攻击力。"""

    events = Death(MINION + DEATHRATTLE).on(Buff(SELF, "NAX12_03e"))


class NAX12_03H:
    """Jaws / 巨颚
    每当一个具有亡语的随从死亡，便获得+2攻击力。"""

    events = Death(MINION + DEATHRATTLE).on(Buff(SELF, "NAX12_03e"))


NAX12_03e = buff(atk=2)
