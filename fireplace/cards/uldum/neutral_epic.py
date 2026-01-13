from ..utils import *


##
# Minions


class ULD_209:
    """Vulpera Scoundrel / 狐人恶棍
    战吼：发现一张法术牌或选择一个 神秘选项。"""

    # <b>Battlecry</b>: <b>Discover</b> a spell or pick a mystery choice.
    class VulperaScoundrelAction(Discover):
        TARGET = ActionArg()
        CARDS = CardArg()
        CARD = CardArg()

        def get_target_args(self, card):
            cards = super().get_target_args(source, target)
            cards[0].append(source.controller.card("ULD_209t"))
            return cards

    play = VulperaScoundrelAction(CONTROLLER, RandomSpell()).then(
        Find(VulperaScoundrelAction.CARD + ID("ULD_209t"))
        & (Give(CONTROLLER, RandomSpell()))
        | (Give(CONTROLLER, VulperaScoundrelAction.CARD))
    )


class ULD_229:
    """Mischief Maker / 捣蛋鬼
    战吼：交换你和对手的牌库顶的一张牌。"""

    # <b>Battlecry:</b> Swap the top card of your deck with your_opponent's.
    play = Swap(FRIENDLY_DECK[-1:], ENEMY_DECK[-1:])


class ULD_290:
    """History Buff / 历史爱好者
    每当你使用一张随从牌，随机使你手牌中的一张随从牌获得+1/+1。"""

    # Whenever you play a minion, give a random minion in your hand +1/+1.
    events = Play(CONTROLLER, MINION).on(
        Buff(RANDOM(FRIENDLY_HAND + MINION), "ULD_290e")
    )


ULD_290e = buff(+1, +1)


class ULD_309:
    """Dwarven Archaeologist / 矮人考古学家
    战吼：发现一张卡牌，其法力值消耗减少（1）点。"""

    # After you <b>Discover</b> a card, reduce its cost by (1).
    events = Give(CONTROLLER, source=FRIENDLY + HAS_DISCOVER).after(
        Buff(Give.CARD, "ULD_309e")
    )


class ULD_309e:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


class ULD_702:
    """Mortuary Machine / 机械法医
    在你的对手使用一张随从牌后，使其获得复生。"""

    # After your opponent plays a minion, give it <b>Reborn</b>.
    events = Play(OPPONENT, MINION).after(GiveReborn(Play.CARD))


class ULD_703:
    """Desert Obelisk / 沙漠方尖碑
    如果你在你的回合结束时控制3座沙漠方尖碑，随机对一个敌人造成5点伤害。"""

    # [x]If you control 3 of these at the end of your turn, deal 5 damage to a random
    # enemy.
    events = OWN_TURN_END.on(
        (Count(FRIENDLY_MINIONS + ID("ULD_703")) >= 3) & Hit(RANDOM_ENEMY_CHARACTER, 5)
    )


class ULD_705:
    """Mogu Cultist / 魔古信徒
    战吼：如果你的场上满是魔古信徒，则将其全部献祭，并召唤“莱，至高守护者”。"""

    # <b>Battlecry:</b> If your board is full of Mogu Cultists, sacrifice them all and
    # summon Highkeeper Ra.
    play = (Count(FRIENDLY_MINIONS + ID("ULD_705")) == 7) & (
        Destroy(FRIENDLY_MINIONS),
        Summon(CONTROLLER, "ULD_705t"),
    )


class ULD_705t:
    events = OWN_TURN_END.on(Hit(ENEMY_CHARACTERS, 20))


class ULD_706:
    """Blatant Decoy / 显眼的诱饵
    亡语：每个玩家从手牌中召唤法力值消耗最低的随从。"""

    # [x]<b>Deathrattle:</b> Each player summons the lowest Cost minion from their hand.
    deathrattle = (
        Summon(CONTROLLER, LOWEST_COST(FRIENDLY_HAND + MINION)),
        Summon(OPPONENT, LOWEST_COST(ENEMY_HAND + MINION)),
    )


class ULD_727:
    """Body Wrapper / 裹尸匠
    战吼：发现一个在本局对战中死亡的友方随从。将其洗入你的牌库。"""

    # <b>Battlecry:</b> <b>Discover</b> a friendly minion that died this game. Shuffle it
    # into your deck.
    play = Choice(
        CONTROLLER, Copy(RANDOM(DeDuplicate(FRIENDLY + KILLED + MINION)) * 3)
    ).then(Shuffle(CONTROLLER, Choice.CARD))
