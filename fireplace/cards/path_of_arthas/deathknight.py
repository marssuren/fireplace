from ..utils import *

class RLK_042:
    """寒冬号角 (Horn of Winter)
    复原两个法力水晶。
    """
    def play(self):
        yield RefreshMana(CONTROLLER, 2)


class RLK_038:
    """冰冷触摸 (Icy Touch)
    对一个敌人造成2点伤害，并使其冻结。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_ENEMY_TARGET: 0
    }
    
    def play(self):
        yield Hit(TARGET, 2)
        yield Freeze(TARGET)


class RLK_110:
    """伊米亚破霜者 (Ymirjar Frostbreaker)
    战吼：你手牌中每有一张冰霜法术牌，便获得+1攻击力。
    机制: BATTLECRY
    """
    def play(self):
        # 统计手牌中的冰霜法术
        frost_spells = self.controller.hand.filter(type=CardType.SPELL, spell_school=SpellSchool.FROST)
        count = len(frost_spells)
        if count > 0:
            yield Buff(SELF, "RLK_110e") * count

class RLK_110e:
    """破霜者增益 (+1攻击)"""
    atk = 1


class RLK_516:
    """碎骨手斧 (Bone Breaker)
    在你的英雄攻击随从后，对敌方英雄造成2点伤害。
    """
    # 英雄攻击随从后触发
    events = Attack(FRIENDLY_HERO, MINION).after(
        Hit(ENEMY_HERO, 2)
    )


class RLK_018:
    """凋零打击 (Wither) / Defrost? (Checklist: 凋零打击 RLK_018)
    对一个随从造成3点伤害。如果消灭该随从，召唤一个2/2并具有突袭的僵尸。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        yield Hit(TARGET, 3)
        # 检查是否死亡
        if TARGET.dead or TARGET.health <= 0:
            yield Summon(CONTROLLER, "RLK_018t")

class RLK_018t:
    """僵尸 (Zombie)
    2/2 突袭
    """
    tags = {GameTag.RUSH: True}


class RLK_056:
    """邪恶狂热 (Unholy Frenzy)
    选择一个敌方随从，使你的所有随从攻击该随从。再次召唤死亡的友方随从。
    (Wait, checklist says: 选择一个敌方随从，使你的所有随从攻击该随从。再次召唤死亡的友方随从。)
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        # 记录当前场上的友方随从
        initial_friendlies = list(self.controller.field)
        
        # 让所有友方随从攻击目标
        # 注意：需要强制攻击，无视嘲讽等
        for minion in initial_friendlies:
            # 只有能攻击的随从才攻击（或者强制攻击？）
            # 炉石机制通常是强制攻击
            yield Attack(minion, TARGET)
        
        # 再次召唤在此过程中死亡的友方随从
        # 需要追踪在本次 Sequence 中死亡的随从
        # 简单实现：检查 initial_friendlies 中哪些死掉了
        # Step 2: Resurrect them.
        pass # TODO: 需要更复杂的事件追踪，甚至可能要在 Attack 序列后处理


class RLK_057:
    """黑暗突变 (Dark Transformation)
    将一个亡灵变形成为一个4/5并具有突袭的亡灵怪物。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.UNDEAD
    }
    play = Morph(TARGET, "RLK_057t")

class RLK_057t:
    """亡灵畸体 (Undead Monstrosity)
    4/5 突袭
    """
    tags = {GameTag.RUSH: True}


class RLK_066:
    """鲜血魔术师 (Hematurge)
    战吼：消耗一份残骸，发现一张鲜血符文牌。
    """
    def play(self):
        if self.controller.corpses >= 1:
            yield SpendCorpses(CONTROLLER, 1)
            # 发现鲜血符文牌 (简化为DK牌)
            yield Discover(CONTROLLER, RandomSpell(card_class=CardClass.DEATHKNIGHT))


class RLK_083:
    """死亡寒冰 (Deathchiller)
    在你施放一个法术后，随机对两个敌人造成1点伤害。
    """
    events = Play(CONTROLLER, SPELL).after(
        Hit(RANDOM(ENEMY_CHARACTERS) * 2, 1)
    )


class RLK_711:
    """凶恶的血翼蝠 (Vicious Bloodworm)
    战吼：使你手牌中的一张随从牌获得等同于本随从攻击力的攻击力。
    (Buff hand minion with ATK)
    """
    def play(self):
        # 随机选择手牌中的一张随从
        hand_minions = self.controller.hand.filter(type=CardType.MINION)
        if hand_minions:
            target_card = self.game.random.choice(hand_minions)
            # 获得当前攻击力
            buff_amt = self.atk
            yield Buff(target_card, "RLK_711e", atk=buff_amt)

class RLK_711e:
    """血翼蝠增益"""
    pass # 动态属性由 Buff 调用设置


class RLK_712:
    """活力分流 (Blood Tap) (Checklist Name)
    使你手牌中的所有随从牌获得+1/+1。消耗3份残骸，再获得+1/+1。
    """
    def play(self):
        yield Buff(FRIENDLY_HAND + MINION, "RLK_712e")
        if self.controller.corpses >= 3:
            yield SpendCorpses(CONTROLLER, 3)
            yield Buff(FRIENDLY_HAND + MINION, "RLK_712e")

class RLK_712e:
    """活力分流增益 (+1/+1)"""
    atk = 1
    health = 1


class RLK_015:
    """凛风冲击 (Howling Blast) (Checklist Name mismatch? Checklist says RLK_015 is 凛风冲击?
     Wait. Checklist Says: [3费] 凛风冲击 (RLK_015).
     Let's trust checklist.)
    对一个敌人造成3点伤害并将其冻结。对所有其他敌人造成1点伤害。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_ENEMY_TARGET: 0
    }
    
    def play(self):
        yield Hit(TARGET, 3)
        yield Freeze(TARGET)
        # 所有其他敌人
        other_enemies = ENEMY_CHARACTERS - TARGET
        yield Hit(other_enemies, 1)


class RLK_087:
    """窒息 (Asphyxiate)
    消灭攻击力最高的敌方随从。
    """
    def play(self):
        targets = self.game.board.filter(controller=OPPONENT, type=CardType.MINION)
        if targets:
            max_atk = max(t.atk for t in targets)
            highest = [t for t in targets if t.atk == max_atk]
            yield Destroy(self.game.random.choice(highest))


class RLK_512:
    """冰川突进 (Glacial Advance)
    造成4点伤害。在本回合中，你的下一个法术法力值消耗减少（2）点。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_ENEMY_TARGET: 0
    }
    def play(self):
        yield Hit(TARGET, 4)
        self.controller.next_spell_cost_reduction = 2


class RLK_731:
    """黑暗堕落者新兵 (Darkfallen Neophyte)
    战吼：消耗一份残骸，使你手牌中的所有随从牌获得+2攻击力。
    Wait, checklist was RLK_731: "战吼：消耗一份残骸..."
    """
    play = (
        SpendCorpses(CONTROLLER, 1),
        Buff(FRIENDLY_HAND + MINION, "RLK_731e")
    )

class RLK_731e:
    """黑暗堕落者增益 (+2攻击)"""
    atk = 2


class RLK_062:
    """蛛魔护群守卫 (Nerubian Swarmguard)
    嘲讽。战吼：召唤本随从的两个复制。
    (Wait, checklist says: 4 cost 1/3 Taunt. Battlecry: Summon two copies.)
    """
    tags = {GameTag.TAUNT: True}
    play = (
        Summon(CONTROLLER, ExactCopy(SELF)),
        Summon(CONTROLLER, ExactCopy(SELF))
    )


class RLK_118:
    """坟墓守卫 (Tomb Guardians)
    召唤两个2/2并具有嘲讽的僵尸。消耗4份残骸，使其获得复生。
    """
    def play(self):
        # 召唤2个
        # 检查是否能消耗4尸体
        give_reborn = False
        if self.controller.corpses >= 4:
            yield SpendCorpses(CONTROLLER, 4)
            give_reborn = True
        
        # 召唤逻辑
        minion1 = yield Summon(CONTROLLER, "RLK_118t")
        minion2 = yield Summon(CONTROLLER, "RLK_118t")
        
        if give_reborn:
            yield Buff(minion1, "RLK_118e")
            yield Buff(minion2, "RLK_118e")

class RLK_118t:
    """僵尸 (Zombie) 2/2 嘲讽"""
    tags = {GameTag.TAUNT: True}

class RLK_118e:
    """复生增益"""
    tags = {GameTag.REBORN: True}


class RLK_713:
    """亡语者女士 (Lady Deathwhisper)
    亡语：复制你手牌中的所有冰霜法术牌。
    """
    def deathrattle(self):
        # 找到手牌里的冰霜法术
        frost_spells = self.controller.hand.filter(type=CardType.SPELL, spell_school=SpellSchool.FROST)
        for card in frost_spells:
            yield Give(CONTROLLER, Copy(card))


class RLK_740:
    """米奈希尔之力 (Might of Menethil)
    战吼：消耗最多3份残骸，冻结等量的敌方随从。
    """
    def play(self):
        count = min(self.controller.corpses, 3)
        if count > 0:
            yield SpendCorpses(CONTROLLER, count)
            # 冻结 count 个敌方随从
            yield Freeze(RANDOM(ENEMY_MINIONS) * count)


class RLK_745:
    """恶毒恐魔 (Malignant Horror)
    复生。在你的回合结束时，消耗一份残骸，召唤一个本随从的复制。
    """
    tags = {GameTag.REBORN: True}
    
    events = OwnTurnEnds(CONTROLLER).on(
        lambda self: (
            SpendCorpses(CONTROLLER, 1) &
            Summon(CONTROLLER, ExactCopy(SELF))
        ) if self.controller.corpses >= 1 else None
    )


class RLK_504:
    """僵尸新娘 (Corpse Bride)
    战吼：消耗最多10份残骸，召唤一个攻击力和生命值等同于消耗残骸数并具有嘲讽的复活的新郎。
    """
    def play(self):
        count = min(self.controller.corpses, 10)
        yield SpendCorpses(CONTROLLER, count)
        yield Summon(CONTROLLER, "RLK_504t", atk=count, max_health=count)

class RLK_504t:
    """复活的新郎"""
    tags = {GameTag.TAUNT: True}


class RLK_730:
    """血液沸腾 (Blood Boil)
    吸血。感染所有敌方随从。在你的回合结束时，使其受到2点伤害。
    """
    tags = {GameTag.LIFESTEAL: True}
    play = Buff(ENEMY_MINIONS, "RLK_730e")

class RLK_730e:
    """感染"""
    tags = {GameTag.LIFESTEAL: True}
    events = OwnTurnEnds(CONTROLLER).on(Hit(OWNER, 2))


class RLK_086:
    """霜之哀伤 (Frostmourne)
    亡语：召唤被该武器消灭的所有随从。
    """
    # 监听英雄攻击随从后，如果随从死亡，则记录该随从到 Buff 中
    events = Attack(FRIENDLY_HERO, ALL_MINIONS).after(
        Dead(Attack.DEFENDER) & StoringBuff(SELF, "RLK_086e", Attack.DEFENDER)
    )


class RLK_086e:
    """霜之哀伤灵魂存储 (Frostmourne Soul Storage)"""
    tags = {GameTag.DEATHRATTLE: True}
    # 亡语：召唤存储的随从
    deathrattle = Summon(CONTROLLER, Copy(STORE_CARD)) 


class RLK_505:
    """髓骨使御者 (Marrow Manipulator)
    战吼：消耗最多5份残骸。每消耗一份残骸，随机对一个敌人造成2点伤害。
    """
    def play(self):
        count = min(self.controller.corpses, 5)
        if count > 0:
            yield SpendCorpses(CONTROLLER, count)
            yield Hit(RANDOM(ENEMY_CHARACTERS), 2) * count


class RLK_063:
    """冰霜巨龙之怒 (Frostwyrm's Fury)
    造成5点伤害，冻结所有敌方随从。召唤一条5/5的冰霜巨龙。
    """
    play = (
        Hit(TARGET, 5), # Note: Checklist says "Deal 5 damage", usually targetable
        Freeze(ENEMY_MINIONS),
        Summon(CONTROLLER, "RLK_063t")
    )

class RLK_063t:
    """冰霜巨龙 5/5"""
    race = Race.DRAGON


class RLK_122:
    """天灾军团 (The Scourge)
    用随机亡灵填满你的面板。
    """
    play = Summon(CONTROLLER, RandomMinion(race=Race.UNDEAD)) * 7
