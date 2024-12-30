# Sergiu Cociuba
# 2024-12-24

class player:
    def __init__(self, vigor, attunement, strength, dex, intelligence, faith, name, level):
        self.vigor = vigor
        self.attunement = attunement
        self.strength = strength
        self.dex = dex
        self.intelligence = intelligence
        self.faith = faith
        self.hp = None
        self.mana = None
        self.spell_slots = None
        self.armor_class = 0
        self.inventory = {}
        self.HP = None
        self.MANA = None
        self.souls = 0
        self.RING = 0
        self.HELMET = None
        self.ARM = None
        self.LEG = None
        self.CHEST = None
        self.BOOT = None
        self.WEAPON = None
        self.name = name
        self.level = level
        self.soul_cost = 500
    def calculate_hp(self,vigor, base_hp = 0, growth_factor = 2, threshold = 40, diminishing_factor = 0.2):
        """
        Calculate max HP based on the Vigor stat.

        Parameters:
        - vigor (int): The Vigor level.
        - base_hp (int): The base HP value. Default is 0.
        - growth_factor (int): HP growth per Vigor point. Default is 2.
        - threshold (int): The Vigor level where diminishing returns start. Default is 10.
        - diminishing_factor (float): Reduces HP growth after threshold. Default is 0.2.

        Returns:
        - hp (float): The calculated HP.
        """
        if vigor <= threshold:
            return base_hp + (growth_factor * vigor)
        else:
            diminishing_pentalty = ((vigor - threshold) ** 2) * diminishing_factor
            return base_hp + (growth_factor * vigor) - diminishing_pentalty
    def set_hp(self):
        self.hp = self.calculate_hp(self.vigor)
        self.HP = self.calculate_hp(self.vigor)
    def set_HP(self, HP):
        self.HP = HP
    def calculate_mana(self, attunement, base_mana = 0, growth_factor = 25, threshold = 40, diminishing_factor = 0.2):
        """
        Calculate mana based on the attunement stat.

        Parameters:
        - attunement (int): The attunement level.
        - base_mana (int): The base mana value. Default is 0.
        - growth_factor (int): Mana growth per attunement point. Default is 25.
        - threshold (int): The attunement level where diminishing returns start. Default is 40.
        - diminishing_factor (float): Reduces mana growth after threshold. Default is 0.2.

        Returns:
        - mana (int): The calculated mana.
        """
        if attunement <= threshold:
            return base_mana + (growth_factor * attunement)
        else:
            diminishing_pentalty = ((attunement - threshold) ** 2) * diminishing_factor
            return base_mana + (growth_factor * attunement) - diminishing_pentalty
    def set_mana(self, mana):
        self.mana = self.calculate_mana(self.attunement)
        self.MANA = self.calculate_mana(self.attunement)

    def calculate_spell_slots(self, attunement, base_slots = 0):
        """
        Calculate spell slots based on the attunement stat.

        Parameters:
        - attunement (int): The attunement level.
        - base_slots (int): The base spell slots. Default is 0.

        Returns:
        - slots (int): The calculated spell slots.
        """
        return base_slots + (attunement // 5)
    def set_spell_slots(self, spell_slots):
        self.spell_slots = self.calculate_spell_slots(self.attunement)
    
    def take_damage(self, damage):
        self.hp = self.hp - damage
        if self.hp <= 0:
            print("Player has died")

    def flask(self,flask): 
        if flask.get_flask_type() == 0:
            if self.hp + flask.drink() >= self.HP:
                self.hp = self.HP
            else:
                self.hp = self.hp + flask.drink()
        else:
            if self.mana + flask.drink() >= self.MANA:
                self.mana = self.mana
            else:
                self.mana = self.mana + flask.drink()
        print("You have sucessfully drank a flask")
    
       
    def obtain_item(self, item):
        self.inventory[item.get_name()] = item
    def remove_item(self,item):
        if item.is_equipped == 1:
            print("unequip this item first")
        else:
            del self.inventory[item.get_name()]

    def unequip_ring(self, ring):
        if self.RING == 0:
            print("There are no rings equipped.")
            return

        if ring.is_equipped == 0:
            print("The specified ring is not equipped.")
            return

        vigor, attunement, strength, dex, intelligence, faith = ring.get_stats()

        self.vigor = max(0, self.vigor - vigor)
        self.HP = self.calculate_hp(self.vigor)
        if self.hp > self.HP:  
            self.hp = self.HP

        self.attunement = max(0, self.attunement - attunement)
        self.MANA = self.calculate_mana(self.attunement)
        if self.mana > self.MANA:  
            self.mana = self.MANA

        self.strength = max(0, self.strength - strength)
        self.dex = max(0, self.dex - dex)
        self.intelligence = max(0, self.intelligence - intelligence)
        self.faith = max(0, self.faith - faith)
        self.RING = self.RING - 1
        ring.set_equip_status(0)
        print(f"Ring '{ring.get_name()}' unequipped.")

    def equip_ring(self, ring):
        if self.RING == 4:
            print("You must unequip a ring before equipping a new ring")
        else:
            vigor, attunement, strength, dex, intelligence, faith = ring.get_stats()  
            self.vigor = max(0, self.vigor + vigor)
            self.HP = self.calculate_hp(self.vigor)    
            self.attunement = max(0, self.attunement + attunement)
            self.MANA = self.calculate_mana(self.attunement)   
            self.RING = self.RING + 1
            ring.set_equip_status(1)
            print(f"Ring '{ring.get_name()}' equipped.")
    def unequip_armor(self, armor):
        # Extract armor stats and type
        strength, dexterity, intelligence, faith, armor_class, item_type = armor.get_stats()

        # Armor slot mapping
        armor_slots = {
            0: "HELMET",
            1: "ARM",
            2: "CHEST",
            3: "LEG",
            4: "BOOT"
        }

        if item_type in armor_slots:
            slot_name = armor_slots[item_type]

            # Check if the armor slot is equipped
            if getattr(self, slot_name) is None:  # Slot is not equipped
                return f"{slot_name.capitalize()} slot is already empty."

            # Unequip the armor
            setattr(self, slot_name, None)  # Set slot to unequipped
            self.armor_class -= armor_class  # Update armor class
            self.armor_class = max(0, self.armor_class)  # Ensure armor class doesn't go below zero
            return f"{slot_name.capitalize()} unequipped successfully."
        else:
            return "Invalid item type."


    def equip_armor(self, armor):
        strength, dexterity, intelligence, faith, armor_class, item_type = armor.get_stats()

        # Check stat requirements
        if self.strength < strength:
            return f"You do not have enough strength to equip this item. Your strength is {self.strength}, but this item requires {strength} strength."
        if self.dex < dexterity:
            return f"You do not have enough dexterity to equip this item. Your dexterity is {self.dex}, but this item requires {dexterity} dexterity."
        if self.intelligence < intelligence:
            return f"You do not have enough intelligence to equip this item. Your intelligence is {self.intelligence}, but this item requires {intelligence} intelligence."
        if self.faith < faith:
            return f"You do not have enough faith to equip this item. Your faith is {self.faith}, but this item requires {faith} faith."

        # Armor slot mapping
        armor_slots = {
            0: "HELMET",
            1: "ARM",
            2: "CHEST",
            3: "LEG",
            4: "BOOT"
        }

        # Check if item_type is valid
        if item_type not in armor_slots:
            return "Invalid armor type."

        slot_name = armor_slots[item_type]

        # Check if the slot is already occupied
        if getattr(self, slot_name) is not None:  # Check if a slot is occupied
            return f"{slot_name.capitalize()} slot already equipped. Unequip it first."

        # Equip the armor
        setattr(self, slot_name, armor)  # Store the armor object in the slot
        self.armor_class += armor_class  # Update the armor class

        return f"{slot_name.capitalize()} equipped successfully."

    def equip_weapon(self, weapon):
        strength, dexterity, intelligence, faith = weapon.get_stats()

        if self.strength < strength:
            return f"You do not have enough strength to equip this item. Your strength is {self.strength}, but this item requires {strength} strength."
        if self.dex < dexterity:
            return f"You do not have enough dexterity to equip this item. Your dexterity is {self.dex}, but this item requires {dexterity} dexterity."
        if self.intelligence < intelligence:
            return f"You do not have enough intelligence to equip this item. Your intelligence is {self.intelligence}, but this item requires {intelligence} intelligence."
        if self.faith < faith:
            return f"You do not have enough faith to equip this item. Your faith is {self.faith}, but this item requires {faith} faith."

        if getattr(self, "WEAPON") is not None:  
            return f"WEAPON slot already equipped. Unequip it first."

        setattr(self, "WEAPON", weapon)  

        return f"WEAPON equipped successfully."
    def unequip_weapon(self, weapon):
        strength, dexterity, intelligence, faith = weapon.get_stats()
        if getattr(self, "WEAPON") is None:
            return f"WEAPON slot is already empty."
        elif getattr(self, "WEAPON") is not None:
            setattr(self, "WEAPON", None) 
            return f"WEAPON unequipped successfully."
        else:
            return "Invalid item type."

    def bonfire(self):
        self.hp = self.HP
        self.mana = self.MANA

    def equip_spell(self, spell):
        if spell.spell_slots_required > self.spell_slots:
            return "Not enough spell slots."

        self.spell_slots -= spell.spell_slots_required
        self.inventory[spell.name] = spell
        spell.equipped = 1
        return f"Spell '{spell.name}' equipped."

    def unequip_spell(self, spell):
        if spell.name not in self.inventory or not spell.equipped:
            return "This spell is not equipped."

        self.spell_slots += spell.spell_slots_required
        spell.equipped = 0
        return f"Spell '{spell.name}' unequipped."

    def use_mana(self, amount):
        if amount > self.mana:
            return

        self.mana -= amount
        return 
    def add_souls(self, amount):
        self.souls = self.souls + amount
    def remove_souls(self, amount):
        self.souls = max(0, self.souls - amount)

    def get_name(self):
        return self.name
    def get_hp(self):
        return self.hp
    def get_HP(self):
        return self.HP
    def get_mana(self):
        return self.mana
    def get_MANA(self):
        return self.MANA
    def get_level(self):
        return self.level
    def get_souls(self):
        return self.souls
    def get_soul_cost(self):
        return self.soul_cost
 
    def level_stat(self, stat_name):
        current_value = getattr(self, stat_name, None)
        if current_value is not None:
            setattr(self, stat_name, current_value + 1)
            if stat_name == "vigor":
                self.set_hp()  
            elif stat_name == "attunement":
                self.set_mana()  
            self.level = self. level + 1
            self.souls = max(0,self.souls - self.soul_cost)
            self.soul_cost = int(self.soul_cost * 1.1)  
        else:
            print(f"Attribute '{stat_name}' not found.")

    def get_stat(self, stat_name):
        return getattr(self, stat_name, None)
    def get_inventory(self):
        return self.inventory









         

    

