
multipliers = {
    "health": [],
    "attack": [],
    "defense": [],
    "item": []
}


class Statistic:
    """
    Represents a statistic. Duration is indefinite if 0.
    """
    def __init__(self, name: str = "Mysterious Aura", multiplier: float = 1, duration: int = 0):
        self.name = name
        self.multiplier = multiplier
        self.duration = duration

    @staticmethod
    def get_multiplier(ext_multipliers: dict = None, stat_type: str = "health", is_monster=False, is_item=False) -> float:
        """
        Calculates the total Stat multiplier for a specific type of stat.
        :param is_item: Must be True if the multiplier is for an item.
        :param is_monster: Must be set to True if the character is a monster.
        :param ext_multipliers: Dictionary that contains key, list pairs where the list contains Stat objects.
        :param stat_type: "health", "attack", "defense"
        :return:
        """
        if ext_multipliers is None:
            ext_multipliers = {}

        if stat_type not in ext_multipliers.keys() and stat_type not in multipliers.keys():
            raise ValueError("Invalid multiplier type given.")

        mult = 1.0
        if is_monster or is_item:
            for stat in multipliers.get(stat_type):
                mult *= stat.multiplier

        # Returns if it is an item, since it would not have separate multipliers.
        if is_item or ext_multipliers == {}:
            return mult

        for stat in ext_multipliers.get(stat_type):
            mult *= stat.multiplier
        return mult

