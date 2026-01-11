from .i18n import _ as translate
import uuid
import inspect

from hearthstone.enums import CardType

from . import logging


class BaseEntity(object):
    base_events = []
    logger = logging.log
    ignore_scripts = False
    type = CardType.INVALID

    def __init__(self):
        self.manager = self.Manager(self)
        self.play_counter = 0
        self.tags = self.manager
        self.uuid = uuid.uuid4()
        self.event_args = None

        if self.data:
            self._events = self.data.scripts.events[:]
        else:
            self._events = []

    def dump(self):
        return {
            "entity_id": self.entity_id,
            "type": int(self.type),
        }

    def dump_hidden(self):
        return {
            "entity_id": self.entity_id,
        }

    def __int__(self):
        return self.entity_id

    @property
    def is_card(self):
        """
        True if the Entity is a real card (as opposed to a Player, Game, ...)
        """
        return self.type > CardType.PLAYER

    @property
    def events(self):
        return self.base_events + list(self._events)

    @property
    def update_scripts(self):
        if self.data and not self.ignore_scripts:
            yield from self.data.scripts.update

    def log(self, message, *args):
        self.logger.info(message, *args)

    def get_actions(self, name):
        actions = getattr(self.data.scripts, name)
        if callable(actions):
            actions = actions(self)
        return actions

    def _call_with_adaptive_args(self, action, args):
        """智能调用事件处理函数，自动适配参数数量
        
        Args:
            action: 事件处理函数
            args: 事件参数列表
            
        Returns:
            函数调用结果
        """
        try:
            # 获取函数签名
            sig = inspect.signature(action)
            params = list(sig.parameters.values())
            
            # 移除 'self' 参数（第一个参数）
            if params and params[0].name == 'self':
                params = params[1:]
            
            # 计算需要的参数数量
            needed = len(params)
            
            # 只传递函数需要的参数数量
            return action(self, *args[:needed])
        except (ValueError, TypeError) as e:
            # 如果签名检查失败，尝试传递所有参数
            try:
                return action(self, *args)
            except TypeError:
                # 如果还是失败，尝试不传参数
                try:
                    return action(self)
                except TypeError:
                    # 最后尝试：传递原始错误
                    raise e

    def trigger_event(self, source, event, args):
        """
        Trigger an event on the Entity
        * \a source: The source of the event
        * \a event: The event being triggered
        * \a args: A list of arguments to pass to the callback
        """
        actions = []
        for action in event.actions:
            if callable(action):
                # 使用智能参数适配
                ac = self._call_with_adaptive_args(action, args)
                if not ac:
                    # Handle falsy returns
                    continue
                if not hasattr(ac, "__iter__"):
                    actions.append(ac)
                else:
                    # 再次调用以获取完整结果
                    actions += self._call_with_adaptive_args(action, args)
            else:
                actions.append(action)
        ret = source.game.trigger(self, actions, args)
        if event.once:
            self._events.remove(event)

        return ret

    def get_damage(self, amount: int, target) -> int:
        """
        Override to modify the damage dealt to a target from the given amount.
        """
        if getattr(target, "dormant", False):
            self.log("%r is dormant to %s for %i damage", target, self, amount)
            return 0
        if target.immune:
            self.log("%r is immune to %s for %i damage", target, self, amount)
            return 0
        return amount

    def get_heal(self, amount: int, target) -> int:
        return amount


class BuffableEntity(BaseEntity):
    def __init__(self):
        super().__init__()
        self.buffs = []
        self.slots = []

    def _getattr(self, attr, i):
        i += getattr(self, "_" + attr, 0)
        for buff in self.buffs:
            i = buff._getattr(attr, i)
        for slot in self.slots:
            i = slot._getattr(attr, i)
        if self.ignore_scripts:
            return i
        script_attr = getattr(self.data.scripts, attr, lambda s, x: x)
        # 如果是可调用的，调用它；否则直接返回i
        if callable(script_attr):
            return script_attr(self, i)
        else:
            return i

    def clear_buffs(self):
        if self.buffs:
            self.log("Clearing buffs from %r", self)
            for buff in self.buffs[:]:
                buff.remove()


class Entity(BuffableEntity):
    pass


def slot_property(attr, f=any):
    @property
    def func(self):
        return f(getattr(slot, attr, False) for slot in self.slots)

    return func


def boolean_property(attr):
    @property
    def func(self):
        script_attr = getattr(self.data.scripts, attr, None)
        # 检查是否可调用,如果是 property 对象则不能调用
        if script_attr is not None and callable(script_attr) and not isinstance(script_attr, property):
            script_value = script_attr(self, False)
        else:
            script_value = False
        
        return (
            getattr(self, "_" + attr, False)
            or (any(getattr(buff, attr, False) for buff in self.buffs))
            or (any(getattr(slot, attr, False) for slot in self.slots))
            or script_value
        )

    @func.setter
    def func(self, value):
        setattr(self, "_" + attr, value)

    return func


def int_property(attr):
    @property
    def func(self):
        ret = self._getattr(attr, 0)
        return max(0, ret)

    @func.setter
    def func(self, value):
        setattr(self, "_" + attr, value)

    return func
