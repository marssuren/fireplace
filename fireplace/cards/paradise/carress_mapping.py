"""
Paradise Shaman - Carress, Cabaret Star 完整变形形态实现

根据官方数据，Carress有21种变形形态（7个派系选2的组合）
每种形态具有不同的战吼效果组合

派系效果：
- Arcane: Draw 2 cards
- Fel: Deal 2 damage to all enemy minions
- Fire: Deal 6 damage to the enemy hero
- Frost: Freeze three random enemy minions
- Holy: Restore 6 Health to your hero
- Nature: Gain +2/+2 and Taunt
- Shadow: Destroy 2 random enemy minions

变形形态映射：
VAC_449t   - Arcane + Fire
VAC_449t2  - Arcane + Nature
VAC_449t3  - Arcane + Fel
VAC_449t4  - Arcane + Frost
VAC_449t5  - Arcane + Holy
VAC_449t6  - Arcane + Shadow
VAC_449t7  - Fire + Nature
VAC_449t8  - Fire + Fel
VAC_449t9  - Fire + Frost
VAC_449t10 - Fire + Holy
VAC_449t11 - Fire + Shadow
VAC_449t12 - Holy + Frost
VAC_449t13 - Holy + Nature
VAC_449t14 - Shadow + Frost
VAC_449t15 - Shadow + Nature
VAC_449t16 - Shadow + Fel
VAC_449t17 - Frost + Nature
VAC_449t18 - Holy + Shadow
VAC_449t19 - Frost + Fel
VAC_449t20 - Holy + Fel
VAC_449t21 - Nature + Fel
"""

# 派系到Token ID的映射
SCHOOL_TO_TOKEN_MAP = {
    # Arcane组合
    (SpellSchool.ARCANE, SpellSchool.FIRE): "VAC_449t",
    (SpellSchool.ARCANE, SpellSchool.NATURE): "VAC_449t2",
    (SpellSchool.ARCANE, SpellSchool.FEL): "VAC_449t3",
    (SpellSchool.ARCANE, SpellSchool.FROST): "VAC_449t4",
    (SpellSchool.ARCANE, SpellSchool.HOLY): "VAC_449t5",
    (SpellSchool.ARCANE, SpellSchool.SHADOW): "VAC_449t6",
    # Fire组合
    (SpellSchool.FIRE, SpellSchool.NATURE): "VAC_449t7",
    (SpellSchool.FIRE, SpellSchool.FEL): "VAC_449t8",
    (SpellSchool.FIRE, SpellSchool.FROST): "VAC_449t9",
    (SpellSchool.FIRE, SpellSchool.HOLY): "VAC_449t10",
    (SpellSchool.FIRE, SpellSchool.SHADOW): "VAC_449t11",
    # Holy组合
    (SpellSchool.HOLY, SpellSchool.FROST): "VAC_449t12",
    (SpellSchool.HOLY, SpellSchool.NATURE): "VAC_449t13",
    (SpellSchool.HOLY, SpellSchool.SHADOW): "VAC_449t18",
    (SpellSchool.HOLY, SpellSchool.FEL): "VAC_449t20",
    # Shadow组合
    (SpellSchool.SHADOW, SpellSchool.FROST): "VAC_449t14",
    (SpellSchool.SHADOW, SpellSchool.NATURE): "VAC_449t15",
    (SpellSchool.SHADOW, SpellSchool.FEL): "VAC_449t16",
    # Frost组合
    (SpellSchool.FROST, SpellSchool.NATURE): "VAC_449t17",
    (SpellSchool.FROST, SpellSchool.FEL): "VAC_449t19",
    # Nature组合
    (SpellSchool.NATURE, SpellSchool.FEL): "VAC_449t21",
}

def get_carress_token_id(school1, school2):
    """根据两个派系获取对应的Token ID"""
    # 确保顺序一致（使用排序）
    schools = tuple(sorted([school1, school2], key=lambda x: x.value))
    return SCHOOL_TO_TOKEN_MAP.get(schools, "VAC_449t")  # 默认返回第一个形态
