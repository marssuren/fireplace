from ...cards import get_script_definition
from ..utils import *


##
# Minions


class ICC_021:
    """Exploding Bloatbat / 自爆肿胀蝠
    亡语：对所有敌方随从造成2点伤害。"""

    deathrattle = Hit(ENEMY_MINIONS, 2)


class ICC_204:
    """Professor Putricide / 普崔塞德教授
    在你使用一个奥秘后，随机将一个猎人的奥秘置入战场。"""

    events = Play(CONTROLLER, SECRET).after(
        Summon(
            CONTROLLER,
            RandomSpell(
                secret=True, card_class=CardClass.HUNTER, exclude=FRIENDLY_SECRETS
            ),
        )
    )


class ICC_243:
    """Corpse Widow / 巨型尸蛛
    你的亡语牌的法力值消耗减少（2）点。"""

    update = Refresh(FRIENDLY_HAND + DEATHRATTLE, {GameTag.COST: -2})


class ICC_415:
    """Stitched Tracker / 缝合追踪者
    战吼： 从你的牌库中发现一张随从牌的复制。"""

    play = GenericChoice(
        CONTROLLER, Copy(RANDOM(DeDuplicate(FRIENDLY_DECK + MINION)) * 3)
    )


class ICC_825:
    """Abominable Bowman / 憎恶弓箭手
    亡语：随机召唤一个在本局对战中死亡的友方野兽。"""

    deathrattle = Summon(CONTROLLER, Copy(FRIENDLY + KILLED + BEAST))


##
# Spells


class ICC_049:
    """Toxic Arrow / 剧毒箭矢
    对一个随从造成$2点伤害，如果它依然存活，则使其获得剧毒。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 2), Dead(TARGET) | GivePoisonous(TARGET)


class ICC_052:
    """Play Dead / 装死
    触发一个友方随从的亡语。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Deathrattle(TARGET)


class ICC_200:
    """Venomstrike Trap / 眼镜蛇陷阱
    奥秘：当你的随从受到攻击时，召唤一条2/3并具有剧毒的眼镜蛇。"""

    secret = Attack(None, FRIENDLY_MINIONS).on(
        FULL_BOARD | (Reveal(SELF), Summon(CONTROLLER, "EX1_170"))
    )


##
# Heros


class ICC_828:
    """Deathstalker Rexxar / 死亡猎手雷克萨
    战吼： 对所有敌方随从造成2点伤害。"""

    play = Hit(ENEMY_MINIONS, 2)


class ICC_828p:
    class CreateZombeast(MultipleChoice):
        PLAYER = ActionArg()
        choose_times = 2

        def do(self, source, player):
            beast_ids = RandomBeast(
                card_class=[CardClass.HUNTER, CardClass.NEUTRAL], cost=range(0, 6)
            ).find_cards(source)
            self.first_ids = []
            self.second_ids = []
            for id in beast_ids:
                if get_script_definition(id):
                    self.first_ids.append(id)
                else:
                    self.second_ids.append(id)
            super().do(source, player)

        def do_step1(self):
            self.cards = [
                self.player.card(id)
                for id in self.source.game.random.sample(self.first_ids, 3)
            ]

        def do_step2(self):
            self.cards = [
                self.player.card(id)
                for id in self.source.game.random.sample(self.second_ids, 3)
            ]

        def done(self):
            card1 = self.choosed_cards[0]
            card2 = self.choosed_cards[1]

            zombeast = self.player.card("ICC_828t")
            zombeast.custom_card = True

            def create_custom_card(zombeast):
                zombeast.tags[GameTag.CARDTEXT_ENTITY_0] = card2.description
                zombeast.tags[GameTag.CARDTEXT_ENTITY_1] = card1.description
                zombeast.data.scripts = card1.data.scripts

                for k in zombeast.silenceable_attributes:
                    v1 = getattr(card1, k)
                    v2 = getattr(card2, k)
                    setattr(zombeast, k, v1 + v2)

                zombeast.cost = card1.cost + card2.cost
                zombeast.atk = card1.atk + card2.atk
                zombeast.max_health = card1.max_health + card2.max_health

            zombeast.create_custom_card = create_custom_card
            zombeast.create_custom_card(zombeast)
            self.player.give(zombeast)

        def choose(self, card):
            if card not in self.cards:
                raise InvalidAction(
                    "%r is not a valid choice (one of %r)" % (card, self.cards)
                )
            else:
                self.choosed_cards.append(card)
                if len(self.choosed_cards) == 1:
                    self.do_step2()
                elif len(self.choosed_cards) == 2:
                    self.player.choice = None
                    self.done()
                    self.trigger_choice_callback()

    requirements = {
        PlayReq.REQ_HAND_NOT_FULL: 0,
    }
    activate = CreateZombeast(CONTROLLER)
