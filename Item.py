# Sergiu Cociuba 
# 2024-12-24
class item:
    """
    This is the parent class for all items.

    Parameters:
    - description (str): this is a description of the item
    """
    def __init__(self, description):
        self.description = description

    def get_item_type(self):
        """
        Default for an item that does not have an item type. Mainly for error checking
        """
        return None  
    def is_equipped(self):
        """
        Default for an item is that it is unequipped
        """
        return 0 

class weapon(item):
    """
    Logic for making a weapon
    
    Parameters:
    - description (str) : Description of the weapon
    - name (str): The name of the weapon
    - n (int): How many dice the weapon rolls
    - dice (int): What kind of dice this weapon rolls for damage
    - strength (int): Strength requirement to use this weapon
    - dex (int): Dex requirement to use this weapon
    - intelligence (int): Intelligence requirement to use this weapon
    - faith (int): Faith requirement to use this weapon
    """
    def __init__(self, description, name, n, dice, strength, dex, intelligence, faith):
        self.name = name
        super().__init__(description)
        self.n = n
        self.dice = dice
        self.strength = strength
        self.dex = dex
        self.intelligence = intelligence
        self.faith = faith
        self.equipped = 0

    def get_name(self):
        return self.name
    def is_equipped(self):  
        return self.equipped
    def get_stats(self):
        """
        Returns the requirements of the weapon
        """
        return self.strength, self.dex, self.intelligence, self.faith

class spell(weapon):
    """
    Logic for making a spell
    
    Parameters:
    - description (str) : Description of the weapon
    - name (str): The name of the weapon
    - n (int): How many dice the weapon rolls
    - dice (int): What kind of dice this weapon rolls for damage
    - strength (int): Strength requirement to use this weapon
    - dex (int): Dex requirement to use this weapon
    - intelligence (int): Intelligence requirement to use this weapon
    - faith (int): Faith requirement to use this weapon
    - mana_cost (int): How much mana the spell costs to cast
    - spell_slots_required (int): How many spell slots you need to equip the spell
    """
    
    def __init__(self, description, name, n, dice, strength, dex, intelligence, faith, mana_cost, spell_slots_required):
        self.name = name
        super().__init__(description, name, n, dice, strength, dex, intelligence, faith)
        self.mana_cost = mana_cost
        self.spell_slots_required = spell_slots_required

    def get_mana_cos(self):
        return self.mana_cost

    def get_spell_slot_cost(self):
        return self.spell_slots_required


class ring(item):
    """
    Logic for making a ring
    
    Parameters:
    - description (str) : Description of the ring
    - name (str): The name of the ring
    - strength (int): Strength bonus added to player stats
    - dex (int): Dex bonus added to player stats
    - intelligence (int): Intelligence bonus added to player stats
    - faith (int): Faith bonus added to player stats
    """
    def __init__(self, description, name, vigor, attunement, strength, dex, intelligence, faith):
        self.name = name
        super().__init__(description)
        self.vigor = vigor
        self.attunement = attunement
        self.strength = strength
        self.dex = dex
        self.intelligence = intelligence
        self.faith = faith
        self.equipped = 0

    def get_name(self):
        return self.name
    def get_stats(self):
        return self.vigor, self.attunement, self.strength, self.dex, self.intelligence, self.faith
    def is_equipped(self):  
        return self.equipped
    def set_equip_status(self, status):
        self.equipped = status

class armor(item):
    """
    Logic for making armor
    
    Parameters:
    - description (str) : Description of the weapon
    - name (str): The name of the weapon
    - n (int): How many dice the weapon rolls
    - dice (int): What kind of dice this weapon rolls for damage
    - strength (int): Strength requirement to use this weapon
    - dex (int): Dex requirement to use this weapon
    - intelligence (int): Intelligence requirement to use this weapon
    - faith (int): Faith requirement to use this weapon
    - armor_class (int): How much AC this armor adds to the player
    - item_type (int): A number from 0-4 to indicate which armor slot the item can be used in ( 0: Helmet, 1: Arms, 2: Chest, 3: Legs, 4: Boots)
    """
    def __init__(self, description, name, strength, dex, intelligence, faith, armor_class, item_type):
        self.name = name
        super().__init__(description)
        self.strength = strength
        self.dex = dex
        self.intelligence = intelligence
        self.faith = faith
        self.equipped = 0
        self.armor_class = armor_class
        self.item_type = item_type  # 0: Helmet, 1: Arms, 2: Chest, 3: Legs, 4: Boots

    def get_name(self):
        return self.name
    def get_stats(self):
        return self.strength, self.dex, self.intelligence, self.faith, self.armor_class, self.item_type
    def get_item_type(self):  
        return self.item_type
    def is_equipped(self):  
        return self.equipped

class estus(item):
    """
    A Special item that allows a player to heal their hp. Is permanent and refillable. Upgradable in the future

    Parameters:
    - name (str): The name of the Estus flask (Estus flask for hp, Ashen Estus flask for mana) Any name works
    - description (str): Description of the flask
    - hp (int): How much hp the flask will restore if its a health flask
    - mana (int): How much mana the flask will restore if its a mana flask
    - charges (int): Current number of charges of the flask
    - max_charges (int): Max number of charges of the flask
    - modifier (int): Going to be used for upgrading the flask
    - flask_type (int): To signify if the flask heals mana or health.
    """
    def __init__(self, name, description, hp, mana, charges, max_charges, modifier, flask_type):
        self.name = name
        super().__init__(description)
        self.hp = hp * (1.00 + (0.10 * modifier))
        self.mana = mana * (1.00 + (0.10 * modifier))
        self.charges = charges
        self.max_charges = max_charges
        self.flask_type = flask_type

    def drink(self):
        """
        Simulates the estus flask being drunk and providing Hp or mana

        Returns:
        - self.hp (int): Hp/Mana value to restore
        """
        if self.charges <= 0:
            print("You have no more flasks")
            return 0
        else:
            self.charges -= 1
            return self.hp if self.flask_type == 0 else self.mana

    def flask_bonfire(self):
        """
        Restores all charges when a player rests at a bonfire
        """
        self.charges = self.max_charges

    def increase_charges(self):
        self.max_charges += 1
        self.charges = self.max_charges
    def get_flask_type(self):
        return self.flask_type
    def get_hp(self):
        return self.hp
    def get_mana(self):
        return self.mana
    def get_charges(self):
        return self.charges
    def get_name(self):
        return self.name

class souls(item):
    """
    A soul item. These store the "Souls" of NPC's found in the world. Can be thought of gold in the real life, which has a value that can
    be converted into currency. These soul items are not lost when a player dies.

    Parameters:
    - description (str): Description of the item
    - value (int): How many souls to be given when consumed
    - name (str): Name of the item
    """
    def __init__(self, description, value, name):
        self.name = name
        super().__init__(description)
        self.value = value
        
    def get_value(self):
        return self.value
    def get_name(self):
        return self.name

class consumable(item):
    """
    A consumable item. Allows them to be stored in "stacks", with the consumable object storing how many you have at once.

    Parameters:
    - description (str): Description of the item
    - amount (int): How many of the item a player has
    - name (str): Name of the item
    """
    def __init__(self, description, amount, name):
        self.name = name
        super().__init__(description)
        self.amount = amount
    def consume(self):
        self.amount = self.amount - 1
    def get_amount(self):
        return self.amount
    def add_more(self, add):
        self.amount = self.amount + add
    def get_name(self):
        return self.name

        

