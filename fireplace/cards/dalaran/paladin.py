from ..utils import *


##
# Minions


class DAL_146:
    """Bronze Herald / 青铜传令官
    亡语：将两张4/4的“青铜龙”置入你的手牌。"""

    # <b>Deathrattle:</b> Add two 4/4 Dragons to your hand.
    deathrattle = Give(CONTROLLER, "DAL_146t") * 2


class DAL_147:
    """Dragon Speaker / 龙语者
    战吼：使你手牌中的所有龙牌获得+3/+3。"""

    # <b>Battlecry:</b> Give all Dragons in your hand +3/+3.
    play = Buff(FRIENDLY_HAND + DRAGON, "DAL_147e")


DAL_147e = buff(+3, +3)


class DAL_573:
    """Commander Rhyssa / 指挥官蕾撒
    你的奥秘会触发 两次。"""

    # Your <b>Secrets</b> trigger twice.
    update = Refresh(CONTROLLER, {enums.EXTRA_TRIGGER_SECRET: True})


class DAL_581:
    """Nozari / 诺萨莉
    战吼：为双方英雄恢复所有生命值。"""

    # <b>Battlecry:</b> Restore both heroes to full Health.
    play = FullHeal(ALL_HEROES)


##
# Spells


class DAL_141:
    """Desperate Measures / 孤注一掷
    双生法术 随机施放一个圣骑士奥秘。"""

    # <b>Twinspell</b> Cast a random Paladin <b>Secret</b>.
    requirements = {
        PlayReq.REQ_SECRET_ZONE_CAP_FOR_NON_SECRET: 0,
    }
    play = CastSpell(RandomSpell(secret=True, card_class=CardClass.PALADIN))


class DAL_141ts(DAL_141):
    pass


class DAL_568:
    """Lightforged Blessing / 光铸祝福
    双生法术 使一个友方随从获得吸血。"""

    # <b>Twinspell</b> Give a friendly minion <b>Lifesteal</b>.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = GiveLifesteal(TARGET)


class DAL_568ts(DAL_568):
    pass


class DAL_570:
    """Never Surrender! / 永不屈服
    奥秘：当你的对手施放一个法术时，使你的所有随从获得+2生命值。"""

    # <b>Secret:</b> When your opponent casts a spell, give your minions +2_Health.
    secret = Play(OPPONENT, SPELL).on(Reveal(SELF), Buff(FRIENDLY_MINIONS, "DAL_570e"))


DAL_570e = buff(health=2)


class DAL_727:
    """Call to Adventure / 冒险号角
    从你的牌库中抽取法力值消耗最低的随从牌，使其获得+2/+2。"""

    # Draw the lowest Cost minion from your deck. Give it +2/+2.
    # 注：选择费用最低的随从（如果有多个同费用，随机选择一个）
    def play(self):
        minions = self.controller.deck.filter(type=CardType.MINION)
        if minions:
            lowest_cost_minion = min(minions, key=lambda c: c.cost)
            yield ForceDraw(lowest_cost_minion).then(
                Buff(ForceDraw.TARGET, "DAL_727e")
            )


DAL_727e = buff(+2, +2)


class DAL_731:
    """Duel! / 决斗
    从每个玩家的牌库中各召唤一个随从，并使其互相 攻击！"""

    # Summon a minion from each player's deck. They fight!
    requirements = {
        PlayReq.REQ_BOARD_NOT_COMPLETELY_FULL: 0,
    }
    play = Attack(
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)),
        Summon(OPPONENT, RANDOM(ENEMY_DECK + MINION)),
    )


##
# Weapons


class DAL_571:
    """Mysterious Blade / 神秘之刃
    战吼： 如果你控制一个奥秘，便获得+1攻击力。"""

    # <b>Battlecry:</b> If you control a <b>Secret</b>, gain +1 Attack.
    powered_up = Find(FRIENDLY_SECRETS)
    play = powered_up & Buff(SELF, "DAL_571e")


DAL_571e = buff(atk=1)
