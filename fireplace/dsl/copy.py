from hearthstone.enums import CardType, GameTag

from ..logging import log
from .lazynum import LazyValue


class Copy(LazyValue):
    """
    Lazily return a list of copies of the target
    """

    def __init__(self, selector):
        self.selector = selector

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.selector)

    def copy(self, source, entity):
        """
        Return a copy of \a entity
        """
        log.info("Creating a copy of %r", entity)
        new_entity = source.controller.card(entity.id, source)
        if entity.custom_card:
            new_entity.custom_card = True
            new_entity.create_custom_card = entity.create_custom_card
            new_entity.create_custom_card(new_entity)
        
        # 设置复制追踪
        # 如果原卡已经是复制，则使用其 copy_group_id
        # 否则使用原卡的 entity_id 作为 copy_group_id
        if entity.copy_group_id is not None:
            new_entity.copy_group_id = entity.copy_group_id
        else:
            new_entity.copy_group_id = entity.entity_id
        new_entity.original_entity_id = entity.entity_id
        
        # 检测是否从对手复制
        # 如果原卡的控制者是当前玩家的对手，设置 COPIED_FROM_OPPONENT 标签
        from .. import enums
        if hasattr(entity, 'controller') and hasattr(source, 'controller'):
            if entity.controller != source.controller:
                # 从对手复制的卡牌，设置标签
                new_entity.tags[enums.COPIED_FROM_OPPONENT] = True
        
        return new_entity

    def evaluate(self, source) -> list[str]:
        if isinstance(self.selector, LazyValue):
            entity = self.selector.evaluate(source)
            entities = [entity] if entity else []
        else:
            entities = self.selector.eval(source.game, source)

        return [self.copy(source, e) for e in entities]


class ExactCopy(Copy):
    """
    Lazily create an exact copy of the target.
    An exact copy will include buffs and all tags.
    """

    def __init__(self, selector, id=None):
        self.id = id
        self.selector = selector

    def copy(self, source, entity):
        ret = super().copy(source, entity)
        if self.id:
            ret = source.controller.card(self.id, source)
            # 如果使用了不同的 ID，仍然需要设置复制追踪
            if entity.copy_group_id is not None:
                ret.copy_group_id = entity.copy_group_id
            else:
                ret.copy_group_id = entity.entity_id
            ret.original_entity_id = entity.entity_id
        for buff in entity.buffs:
            # Recreate the buff stack
            new_buff = source.controller.card(buff.id)
            new_buff.source = buff.source
            attributes = [
                "atk",
                "max_health",
                "_xatk",
                "_xhealth",
                "_xcost",
                "store_card",
            ]
            for attribute in attributes:
                if hasattr(buff, attribute):
                    setattr(new_buff, attribute, getattr(buff, attribute))
            new_buff.additional_deathrattles = buff.additional_deathrattles[:]
            new_buff.apply(ret)
            if buff in source.game.active_aura_buffs:
                new_buff.tick = buff.tick
                source.game.active_aura_buffs.append(new_buff)
        if entity.type == CardType.MINION:
            for k in entity.silenceable_attributes:
                v = getattr(entity, k)
                setattr(ret, k, v)
            ret.additional_deathrattles = entity.additional_deathrattles[:]
            ret.silenced = entity.silenced
            ret.damage = entity.damage
        return ret


class KeepMagneticCopy(Copy):
    """
    Kangor's Endless Army
    They keep any <b>Magnetic</b> upgrades
    """

    def __init__(self, selector, id=None):
        self.id = id
        self.selector = selector

    def copy(self, source, entity):
        ret = super().copy(source, entity)
        if self.id:
            ret = source.controller.card(self.id, source)
        for buff in entity.buffs:
            if getattr(buff.source, "has_magnetic", False):
                buff.source.buff(ret, buff.id, atk=buff.atk, max_health=buff.max_health)
        return ret


class RebornCopy(Copy):
    def copy(self, source, entity):
        ret = super().copy(source, entity)
        ret.reborn = False
        ret.set_current_health(1)
        return ret
