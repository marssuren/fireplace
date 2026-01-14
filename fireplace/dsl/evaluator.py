import copy

from hearthstone.enums import CardType, CardClass

from ..logging import log


class Evaluator:
    """
    Lazily evaluate a condition at runtime.

    Evaluators must implement the check() method, which determines whether they
    evaluate to True in the current state.
    """

    def __init__(self):
        self._if = None
        self._else = None
        self._neg = False

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.selector)

    def __neg__(self):
        ret = copy.copy(self)
        ret._neg = not self._neg
        return ret

    def __and__(self, action):
        ret = copy.copy(self)
        ret._if = action
        return ret

    def __or__(self, action):
        ret = copy.copy(self)
        ret._else = action
        return ret

    def evaluate(self, source):
        """
        Evaluates the board state from `source` and returns an iterable of
        Actions as a result.
        """
        ret = self.check(source)
        if self._neg:
            ret = not ret
        if ret:
            if self._if:
                return self._if
        elif self._else:
            return self._else

    def trigger(self, source):
        """
        Triggers all actions meant to trigger on the board state from `source`.
        """
        actions = self.evaluate(source)
        if actions:
            if not hasattr(actions, "__iter__"):
                actions = (actions,)
            source.game.trigger_actions(source, actions)


class Attacking(Evaluator):
    """
    Evaluates to True if any target in \a selector1 is attacking
    any target in \a selector2.
    """

    def __init__(self, selector1, selector2):
        super().__init__()
        self.selector1 = selector1
        self.selector2 = selector2

    def __repr__(self):
        return "%s(%r %r)" % (self.__class__.__name__, self.selector1, self.selector2)

    def check(self, source):
        t1 = self.selector1.eval(source.game, source)
        t2 = self.selector2.eval(source.game, source)
        for entity in t1:
            if entity.attacking:
                return entity.attack_target in t2
        return False


class ChooseBoth(Evaluator):
    """
    Evaluates to True if the selector `choose_both` is true
    Selector must evaluate to only one player.
    """

    def __init__(self, selector):
        super().__init__()
        self.selector = selector

    def check(self, source):
        player = self.selector.eval(source.game, source)[0]
        if player.choose_both:
            return True
        return False


class CurrentPlayer(Evaluator):
    """
    Evaluates to True if the selector is the current player.
    Selector must evaluate to only one player.
    """

    def __init__(self, selector):
        super().__init__()
        self.selector = selector

    def check(self, source):
        for target in self.selector.eval(source.game, source):
            if not target.controller.current_player:
                return False
        return True


class Dead(Evaluator):
    """
    Evaluates to True if every target in \a selector is dead
    """

    def __init__(self, selector):
        super().__init__()
        self.selector = selector

    def check(self, source):
        from .selector import Selector

        if isinstance(self.selector, Selector):
            entities = self.selector.eval(source.game, source)
        else:
            entity = self.selector.evaluate(source)
            # entity 可能是 None、单个实体、或者实体列表
            if entity is None:
                entities = []
            elif isinstance(entity, list):
                entities = entity
            else:
                entities = [entity]
        for target in entities:
            # 处理 target 也可能是列表的情况
            if isinstance(target, list):
                for t in target:
                    if hasattr(t, 'dead') and t.dead:
                        return True
            elif hasattr(target, 'dead') and target.dead:
                return True
        return False


class Alive(Evaluator):
    """
    Evaluates to True if every target in \a selector is alive (not dead)
    """

    def __init__(self, selector):
        super().__init__()
        self.selector = selector

    def check(self, source):
        from .selector import Selector

        if isinstance(self.selector, Selector):
            entities = self.selector.eval(source.game, source)
        else:
            entity = self.selector.evaluate(source)
            # entity 可能是 None、单个实体、或者实体列表
            if entity is None:
                entities = []
            elif isinstance(entity, list):
                entities = entity
            else:
                entities = [entity]
        for target in entities:
            # 处理 target 也可能是列表的情况
            if isinstance(target, list):
                for t in target:
                    if hasattr(t, 'dead') and t.dead:
                        return False
            elif hasattr(target, 'dead') and target.dead:
                return False
        return True


class Find(Evaluator):
    """
    Evaluates to True if \a selector has a match.
    """

    def __init__(self, selector, count=1):
        super().__init__()
        self.selector = selector

    def check(self, source):
        # 如果selector是Evaluator类型(如LazyNumEvaluator),调用其check方法
        if isinstance(self.selector, Evaluator):
            return self.selector.check(source)
        # 否则假设它是Selector,调用eval方法
        try:
            return bool(len(self.selector.eval(source.game, source)))
        except AttributeError as e:
            # selector 不是 Selector 对象，可能是 function 或其他类型
            import sys
            import traceback
            error_msg = (
                f"\n{'='*80}\n"
                f"ATTRIBUTEERROR in Find.check (selector type error)\n"
                f"{'='*80}\n"
                f"Selector: {self.selector}\n"
                f"Selector type: {type(self.selector)}\n"
                f"Selector repr: {repr(self.selector)}\n"
                f"Source: {source}\n"
                f"Source type: {type(source).__name__}\n"
                f"Source ID: {getattr(source, 'id', 'N/A')}\n"
                f"Exception: {e}\n"
                f"Stacktrace:\n"
            )
            print(error_msg, file=sys.stderr)
            traceback.print_stack(file=sys.stderr)
            print(f"{'='*80}\n", file=sys.stderr)
            raise


class FindAll(Evaluator):
    """
    Evaluates to True if \a selector has a match.
    """

    def __init__(self, *selectors):
        super().__init__()
        self.selectors = selectors

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.selectors)

    def check(self, source):
        return all(
            bool(len(selector.eval(source.game, source))) for selector in self.selectors
        )


class FindDuplicates(Evaluator):
    """
    Evaluates to True if \a selector has duplicates.
    """

    def __init__(self, selector, count=1):
        super().__init__()
        self.selector = selector

    def check(self, source):
        entities = self.selector.eval(source.game, source)
        ids = [entity.id for entity in entities]
        return len(set(ids)) < len(ids)


class EvenCost(Evaluator):
    """
    Evaluates to True if the cost of \a selector are all even cost.
    """

    def __init__(self, selector, count=1):
        super().__init__()
        self.selector = selector

    def check(self, source):
        entities = self.selector.eval(source.game, source)
        for entity in entities:
            if entity.cost % 2 == 1:
                return False
        return True


class OddCost(Evaluator):
    """
    Evaluates to True if the cost of \a selector are all odd cost.
    """

    def __init__(self, selector, count=1):
        super().__init__()
        self.selector = selector

    def check(self, source):
        entities = self.selector.eval(source.game, source)
        for entity in entities:
            if entity.cost % 2 == 0:
                return False
        return True


class JoustEvaluator(Evaluator):
    """
    Compare the sum of the costs of \a selector versus \a selector2.
    Considers the joust won if the mana cost of \a selector1 is higher.
    If a side is empty, it automatically loses.
    A draw is treated as a loss.
    """

    def __init__(self, selector1, selector2):
        super().__init__()
        self.selector1 = selector1
        self.selector2 = selector2

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.selector1, self.selector2)

    def check(self, source):
        challenger = self.selector1.evaluate(source)
        defender = self.selector2.evaluate(source)
        if not challenger:
            return False
        if not defender:
            return True
        return challenger.cost > defender.cost


class Lethal(Evaluator):
    """
    Evaluates to True if \a amount damage would destroy *all* entities
    in \a selector (including armor).
    """

    def __init__(self, selector, amount):
        super().__init__()
        self.selector = selector
        self.amount = amount

    def check(self, source):
        entities = self.selector.eval(source.game, source)
        amount = self.amount.evaluate(source)
        for entity in entities:
            health = entity.health
            if entity.type == CardType.HERO:
                health += entity.armor
            if health > amount:
                return False
        return True


class Actived(Evaluator):
    def __init__(self, selector, count=1):
        super().__init__()
        self.selector = selector

    def check(self, source):
        entities = self.selector.eval(source.game, source)
        for entity in entities:
            if not getattr(entity, "actived", False):
                return False
        return True


class WithSecrets(Evaluator):
    """
    Evaluates to True if \a controller class has secret
    """

    def __init__(self):
        super().__init__()

    def check(self, source):
        return source.controller.hero.card_class in [
            CardClass.MAGE,
            CardClass.HUNTER,
            CardClass.PALADIN,
            CardClass.ROGUE,
        ]


WITH_SECRECTS = WithSecrets()


class HasTarget(Evaluator):
    def __init__(self):
        super().__init__()

    def check(self, source):
        return bool(source.target)


HAS_TARGET = HasTarget()
