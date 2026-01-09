from .actions import *
from .dsl.selector import *


OWN_CARD_PLAY = Play(CONTROLLER)
OWN_MINION_PLAY = Play(CONTROLLER, MINION)
OWN_SECRET_PLAY = Play(CONTROLLER, SECRET)
OWN_SPELL_PLAY = Play(CONTROLLER, SPELL)

TURN_BEGIN = BeginTurn()
OWN_TURN_BEGIN = BeginTurn(CONTROLLER)

TURN_END = EndTurn()
OWN_TURN_END = EndTurn(CONTROLLER)

# 别名 - 为了兼容不同的命名风格
Inspire = PlayHeroPower  # TGT expansion - Inspire mechanic

SELF_DAMAGE = Damage(SELF)
