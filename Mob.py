# Sergiu Cociuba
# 2024-12-24

class mob:
    """
    Mob class that can hold abilities in its inventory and take damage

    Parameters:
    - hp (int): How much hp the boss has
    - armor_class (int): The armor class of the boss
    - name (str): name of the boss
    """
    def __init__(self, hp, armor_class, name):
        self.hp = hp
        self.armor_class = armor_class
        self.inventory = {}
        self.name = name
    def add_ability(self, item):
        self.inventory[item.get_name()] = item

    def remove_ability(self,item):
        del self.inventory[item.get_name()]

    def take_damage(self, damage):
        self.hp = self.hp - damage
        if self.hp <= 0:
            print("Boss has died")

    def heal_boss(self, hp):
        self.hp = self.hp + hp
        print("Boss has healed")

    def get_name(self):
        return self.name

    def get_hp(self):
        return self.hp

    def get_armor_class(self):
        return self.armor_class
    def get_inventory(self):
        return self.inventory

