from ..utils import *


##
# Minions


class ULD_262:
    """High Priest Amet / 高阶祭司阿门特
    每当你召唤一个随从，将其生命值变为与本随从相同。"""

    # [x]Whenever you summon a minion, set its Health equal to this minion's.
    events = Summon(CONTROLLER, MINION).on(SetStateBuff(Summon.CARD, "ULD_262e"))


class ULD_262e:
    max_health = lambda self, _: self._xhealth


class ULD_266:
    """Grandmummy / 木奶伊
    复生，亡语：随机使一个友方随从获得+1/+1。"""

    # [x]<b>Reborn</b> <b>Deathrattle:</b> Give a random friendly minion +1/+1.
    deathrattle = Buff(RANDOM_OTHER_FRIENDLY_MINION, "ULD_266e")


ULD_266e = buff(+1, +1)


class ULD_268:
    """Psychopomp / 接引冥神
    战吼：随机召唤一个在本局对战中死亡的友方随从。使其获得 复生。"""

    # [x]<b>Battlecry:</b> Summon a random friendly minion that died this game. Give it
    # <b>Reborn</b>.
    play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION))).then(
        GiveReborn(Summon.CARD)
    )


class ULD_269:
    """Wretched Reclaimer / 卑劣的回收者
    战吼：消灭一个友方随从，然后将其复活，并具有所有生命值。"""

    # [x]<b>Battlecry:</b> Destroy a friendly minion, then return it to life with full
    # Health.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Destroy(TARGET), Summon(CONTROLLER, Copy(TARGET))


class ULD_270:
    """Sandhoof Waterbearer / 沙蹄搬水工
    在你的回合结束时，为一个受伤的友方角色恢复#5点生命值。"""

    # At the end of your turn, restore #5 Health to a damaged friendly character.
    events = OWN_TURN_END.on(Heal(RANDOM(FRIENDLY + DAMAGED_CHARACTERS), 5))


##
# Spells


class ULD_265:
    """Embalming Ritual / 防腐仪式
    使一个随从获得复生。"""

    # Give a minion <b>Reborn</b>.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = GiveReborn(TARGET)


class ULD_272:
    """Holy Ripple / 神圣涟漪
    对所有敌人造成$1点伤害，为所有友方角色 恢复#1点生命值。"""

    # Deal $1 damage to all enemies. Restore #1_Health to all friendly characters.
    play = Hit(ENEMY_CHARACTERS, 1), Heal(FRIENDLY_CHARACTERS, 1)


class ULD_714:
    """Penance / 苦修
    吸血 对一个随从造成$3点伤害。"""

    # <b>Lifesteal</b> Deal $3 damage to a_minion.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3)


class ULD_718:
    """Plague of Death / 死亡之灾祸
    沉默并消灭所有随从。"""

    # <b>Silence</b> and destroy all_minions.
    play = Silence(ALL_MINIONS), Destroy(ALL_MINIONS)


class ULD_724:
    """Activate the Obelisk / 激活方尖碑
    任务：恢复15点生命值。奖励：方尖碑之眼。"""

    # <b>Quest:</b> Restore 15_Health. <b>Reward:</b> Obelisk's Eye.
    progress_total = 15
    quest = Heal(source=FRIENDLY).after(AddProgress(SELF, Heal.TARGET, Heal.AMOUNT))
    reward = Summon(CONTROLLER, "ULD_724p")


class ULD_724p:
    """Obelisk's Eye"""

    # <b>Hero Power</b> Restore #3 Health. If you target a minion, also give it +3/+3.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    activate = Find(TARGET + MINION) & (Heal(TARGET, 3), Buff(TARGET, "ULD_724e")) | (
        Heal(TARGET, 3)
    )


ULD_724e = buff(+3, +3)
