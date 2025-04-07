VIGOR_CHART = {
    "brn": {
        "effect_type": "Status",
        "damage": 1/8,  # 1/8 of max HP per turn
        "attack_modifier": 0.5,  # Halves physical attack
        "severity": 2  # Scale of 1-3 for severity
    },
    "par": {
        "effect_type": "Status",
        "speed_modifier": 0.25,  # Reduces speed
        "move_chance": 0.75,  # 75% chance to move
        "severity": 2
    },
    "slp": {
        "effect_type": "Status",
        "duration": range(2, 5),  # 1-3 turns
        "move_chance": 0,  # Cannot move while asleep
        "severity": 3
    },
    "frz": {
        "effect_type": "Status",
        "move_chance": 0.2,  # 20% chance to thaw each turn
        "severity": 3
    },
    "psn": {
        "effect_type": "Status",
        "damage": 1/8,  # 1/8 of max HP per turn
        "severity": 1
    },
    "tox": {
        "effect_type": "Status",
        "damage": 1/16,  # Starts at 1/16, increases each turn
        "stacking": True,  # Damage increases each turn
        "severity": 3
    }
}