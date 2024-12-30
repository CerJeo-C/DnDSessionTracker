# Sergiu Cociuba
# 2024-12-24
"""
This is the main "Driver" of this code. Run this code with all files in the same folder. This provides a simple console UI to keep track 
of most things that would occur in a Dungeons and Dragons (DnD) session. Capable of saving and loading states to reload. This code 
doesn't actually fully simulate a DnD session, rolling isn't included. 
NOTE: This is desgined for a homebrew DARK SOULS III campaign, not for a traditional DND session. Eventually I will upload a standard DnD 
version
"""
import pickle
from Mob import mob
from Player import player
from Item import ring, armor, weapon, estus, souls, spell, consumable

class SessionDriver:
    """
    Instantiates an empty list of all players (player objects), mobs (mob objects), and items (item objects)
    """
    def __init__(self):
        self.players = []
        self.mobs = []
        self.items = []

    def interact(self):
        """
        This is a simple console UI that allows you to navigate through the options.
        """
        while True:
            try:
                print("\nSession Options:")
                print("1. Create")
                print("2. Manage Players")
                print("3. Manage Mobs")
                print("4. Manage Items")
                print("5. Combat")
                print("6. Save/Load Session")
                print("7. Exit")

                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    self.create_menu()
                elif choice == "2":
                    self.player_menu()
                elif choice == "3":
                    self.mob_menu()
                elif choice == "4":
                    self.item_menu()
                elif choice == "5":
                    self.combat_menu()
                elif choice == "6":
                    self.save_load_menu()
                elif choice == "7":
                    print("Exiting session.")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}. Operation canceled. You can continue your session.")
                
    def create_menu(self):
        """
        This handles the create menu UI, allowing the user to generate players, mobs, items, or spells
        """
        print("\nCreate Options:")
        print("1. Create Player")
        print("2. Create Mob")
        print("3. Create Item")
        print("4. Create Spell")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            self.create_player()
        elif choice == "2":
            self.create_mob()
        elif choice == "3":
            self.create_item()
        elif choice == "4":
            self.create_spell()
        else:
            print("Invalid choice.")

    def player_menu(self):
        """
        This handles the player menu UI, allowing the user to performs all actions related to a single player
        """
        print("\nPlayer Management:")
        print("1. View Players")
        print("2. Equip Spell")
        print("3. Unequip Spell")
        print("4. Equip Item")
        print("5. Unequip Item")
        print("6. Consume Soul")
        print("7. Remove Souls")
        print("8. Use item")
        print("9. Increment Item Amount")
        print("10. Level up")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            self.view_players()
        elif choice == "2":
            self.equip_spell()
        elif choice == "3":
            self.unequip_spell()
        elif choice == "4":
            self.equip_item()
        elif choice == "5":
            self.unequip_item()
        elif choice == "6":
            self.consume_souls()
        elif choice == "7":
            self.remove_souls()
        elif choice == "8":
            self.use_item()
        elif choice == "9":
            self.increment()
        elif choice == "10":
            self.increase_player_stats()
        else:
            print("Invalid choice.")

    def mob_menu(self):
        """
        This handles the mob menu UI, allowing the user to view and add "Weapons" to mobs. Giving a weapon to a mob is a way to give a mob
        "abilities". The weapons created for mobs just store the information related to the "ability" in their description 
        """
        print("\nMob Management:")
        print("1. View Mobs")
        print("2. Add Weapon to Mob")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            self.view_mobs()
        elif choice == "2":
            self.add_weapon_to_mob()
        else:
            print("Invalid choice.")

    def combat_menu(self):
        """
        This handles the combat menu UI, allowing the user to damage players and mobs. Also contains the option to rest at a bonfire to 
        restore all flasks
        """
        print("\nCombat Options:")
        print("1. Damage Player")
        print("2. Damage Mob")
        print("3. Rest at Bonfire")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            self.damage_player()
        elif choice == "2":
            self.damage_mob()
        elif choice == "3":
            self.rest_at_bonfire()
        else:
            print("Invalid choice.")
            
    def item_menu(self):
        """
        This handles the item menu UI, allowing the user to view any item that has been created. Creating objects means they exist in the
        world, and a player will need to pick up an item to be considered in their inventory. They can also drink from the Estus flask to 
        restore HP
        """
        print("\nItem Management:")
        print("1. View Items")
        print("2. Pick Up Item")
        print("3. Drink from Flask")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            self.view_item_details()
        elif choice == "2":
            self.pick_up_item()
        elif choice == "3":
            self.drink_from_flask()
        else:
            print("Invalid choice.")

    def save_load_menu(self):
        """
        This handles the save/load menu UI, allowing the user to save the state of a DnD session. It saves the file as a .pkl file
        which is a space efficient file format. Simplay start the program again and load the .pkl file you saved before to continue a session
        """
        print("\nSave/Load Session:")
        print("1. Save Session")
        print("2. Load Session")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            filename = input("Enter filename to save session (default: session.pkl): ") or "session.pkl"
            self.save_session(filename)
        elif choice == "2":
            filename = input("Enter filename to load session (default: session.pkl): ") or "session.pkl"
            try:
                loaded_session = self.load_session(filename)
                self.players = loaded_session.players
                self.mobs = loaded_session.mobs
                self.items = loaded_session.items
                print("Session loaded successfully.")
            except FileNotFoundError:
                print(f"File {filename} not found. Please check the filename and try again.")
        else:
            print("Invalid choice.")

    def save_session(self, filename="session.pkl"):
        """
        This code will save the session as a .pkl file inside the directory where the .py files are held.

        Parameters: 
        - filename (str): Filename to store the file as
        """
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
        print(f"Session saved to {filename}!")

    @staticmethod
    def load_session(filename="session.pkl"):
        """
        This code will load a session from a .pkl file. Ensure the .pkl file is found in the same location as the Driver.py

        Parameters: 
        - filename (str): name of the file to load the session
        """
        with open(filename, 'rb') as f:
            return pickle.load(f)

    def create_player(self):
        """
        This will allow the user to create a player object to add to the session. The user will be promted to add the stats, the name, 
        and the level of the player to be created
        """
        try:
            print("Enter player stats:")
            vigor = int(input("Vigor: "))
            attunement = int(input("Attunement: "))
            strength = int(input("Strength: "))
            dex = int(input("Dexterity: "))
            intelligence = int(input("Intelligence: "))
            faith = int(input("Faith: "))
            name = str(input("Name: "))
            level = int(input("Level: "))
            
            new_player = player(vigor, attunement, strength, dex, intelligence, faith, name, level=1)
            new_player.set_hp()
            new_player.set_mana(None)
            new_player.set_spell_slots(None)
            self.players.append(new_player)
            print("Player created successfully.")
        except ValueError:
            print("Invalid input. Please enter valid numeric values.")

    def use_item(self):
        """
        This will allow the user to consume a consumable item object that is inside a players inventory
        """
        if not self.players:
            print("No players created yet. Create a player first.")
            return

        # Select a player
        for idx, player_obj in enumerate(self.players):
            print(f"{idx + 1}: {player_obj.get_name()}")
        player_index = int(input("Enter the player number to consume an item from: ")) - 1

        if player_index < 0 or player_index >= len(self.players):
            print("Invalid player number.")
            return

        player_obj = self.players[player_index]

        # Select an item to consume
        consumable_items = [item for item in player_obj.get_inventory().values() if isinstance(item, consumable)]
        if not consumable_items:
            print(f"{player_obj.get_name()} has no consumable items in their inventory.")
            return

        for idx, consumable_item in enumerate(consumable_items):
            print(f"{idx + 1}: {consumable_item.get_name()} (Amount: {consumable_item.get_amount()})")

        try:
            consumable_index = int(input("Enter the consumable item number to consume: ")) - 1
            if consumable_index < 0 or consumable_index >= len(consumable_items):
                print("Invalid selection.")
                return

            consumable_item = consumable_items[consumable_index]
            if consumable_item.get_amount() - 1 <= 0:
                print(f"{consumable_item.get_name()} consumed. {player_obj.get_name()} now has {consumable_item.get_amount() - 1} left.")
                del player_obj.get_inventory()[consumable_item.get_name()]
            else:
                consumable_item.consume()
                print(f"{consumable_item.get_name()} consumed. {player_obj.get_name()} now has {consumable_item.get_amount()} left.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def increment(self):
        """
        This will allow the user to consume add quantity to a consumable item. For example, if a player has the consumable "FireBomb" with 5
        stored in the player's inventory, this function can be used to add to the amount of the consumable item when they pick up more of the
        same item. This is so you do not need to create a duplicate consumable objects.
        """
        if not self.players:
            print("No players created yet. Create a player first.")
            return

        # Select a player
        for idx, player_obj in enumerate(self.players):
            print(f"{idx + 1}: {player_obj.get_name()}")
        player_index = int(input("Enter the player number to consume an item from: ")) - 1

        if player_index < 0 or player_index >= len(self.players):
            print("Invalid player number.")
            return

        player_obj = self.players[player_index]

        # Select an item to increment
        consumable_items = [item for item in player_obj.get_inventory().values() if isinstance(item, consumable)]
        if not consumable_items:
            print(f"{player_obj.get_name()} has no consumable items in their inventory.")
            return

        for idx, consumable_item in enumerate(consumable_items):
            print(f"{idx + 1}: {consumable_item.get_name()} (Amount: {consumable_item.get_amount()})")

        try:
            consumable_index = int(input("Enter the consumable item number to increment: ")) - 1
            if consumable_index < 0 or consumable_index >= len(consumable_items):
                print("Invalid selection.")
                return
            consumable_item = consumable_items[consumable_index]
            add = int(input("Enter the amount to add: "))
            consumable_item.addMore(add)
            print(f"{consumable_item.get_name()} consumed. {player_obj.get_name()} now has {consumable_item.get_amount()} left.")
            return
        except ValueError:
            print("Invalid input. Please enter a number.")


    def create_mob(self):
        """
        This will create a mob. The user will be promted to enter the name, hp, and armor class of the mob
        """
        try:
            print("Enter mob stats:")
            name = str(input("Name: "))
            hp = int(input("HP: "))
            armor_class = int(input("Armor Class: "))
            new_mob = mob(hp, armor_class, name)
            self.mobs.append(new_mob)
            print("Mob created successfully.")
        except ValueError:
            print("Invalid input. Please enter valid numeric values.")

    def view_mobs(self):
        """
        Allow you to inspect the mobs you have created to view their Hp, name, and armor class
        """
        if not self.mobs:
            print("No mobs available.")
            return

        print("Mobs:")
        for idx, mob_obj in enumerate(self.mobs):
            print(f"Name: {mob_obj.get_name()}\nHP: {mob_obj.get_hp()}\nArmor Class: {mob_obj.get_armor_class()}")

    def create_item(self):
        """
        Allows the creation of different items. Allows the creatin of rings, weapons, armor, estus, souls, and consumables
        """
        try:
            print("Choose item type:")
            item_type = input("Type (ring, weapon, armor, estus, souls, consumable): ").strip().lower()

            if item_type == "ring":
                name = input("Name: ")
                description = input("Description: ")
                vigor = int(input("Vigor bonus: "))
                attunement = int(input("Attunement bonus: "))
                strength = int(input("Strength bonus: "))
                dex = int(input("Dexterity bonus: "))
                intelligence = int(input("Intelligence bonus: "))
                faith = int(input("Faith bonus: "))
                new_item = ring(description, name, vigor, attunement, strength, dex, intelligence, faith)

            elif item_type == "weapon":
                name = input("Name: ")
                description = input("Description: ")
                n = int(input("Dice rolls: "))
                dice = int(input("Dice type: "))
                strength = int(input("Required strength: "))
                dex = int(input("Required dexterity: "))
                intelligence = int(input("Required intelligence: "))
                faith = int(input("Required faith: "))
                new_item = weapon(description, name, n, dice, strength, dex, intelligence, faith)

            elif item_type == "armor":
                name = input("Name: ")
                description = input("Description: ")
                strength = int(input("Required strength: "))
                dex = int(input("Required dexterity: "))
                intelligence = int(input("Required intelligence: "))
                faith = int(input("Required faith: "))
                armor_class = int(input("Armor Class: "))
                item_type_code = int(input("Type (0=Helmet, 1=Arms, 2=Chest, 3=Legs, 4=Boots): "))
                new_item = armor(description, name, strength, dex, intelligence, faith, armor_class=armor_class, item_type=item_type_code)

            elif item_type == "estus":
                name = input("Name: ")
                description = input("Description: ")
                hp = int(input("HP restored: "))
                mana = int(input("Mana restored: "))
                charges = int(input("Charges: "))
                max_charges = int(input("Max Charges: "))
                modifier = int(input("Modifier: "))
                flask_type = int(input("Type (0=Health, 1=Mana): "))
                new_item = estus(name, description, hp, mana, charges, max_charges, modifier, flask_type)

            elif item_type == "souls":
                description = input("Description: ")
                value = int(input("Soul value: "))
                name = str(input("Name: "))
                new_item = souls(description, value, name)
            elif item_type == "consumable":
                name = str(input("Name: "))
                description = str(input("Description: "))
                amount = int(input("Amount: "))
                new_item = consumable(description, amount, name)

            else:
                print("Invalid item type.")
                return

            self.items.append(new_item)
            print(f"{item_type.capitalize()} created successfully.")
        except ValueError:
            print("Invalid input. Please enter valid numeric values.")

    def damage_player(self):
        """
        User is prompted to select a player to recieve damage.
        """
        if not self.players:
            print("No players created yet. Create a player first.")
            return

        try:
            for idx, player_obj in enumerate(self.players):
                print(f"{idx + 1}: {player_obj.get_name()} - HP: {player_obj.get_hp()}")
            player_index = int(input("Enter the player number to damage: ")) - 1

            if player_index < 0 or player_index >= len(self.players):
                print("Invalid player number.")
                return

            player_obj = self.players[player_index]
            damage = int(input(f"Enter damage to apply to {player_obj.get_name()}: "))
            player_obj.take_damage(damage)
            print(f"{player_obj.get_name()} took {damage} damage. Current HP: {player_obj.get_hp()}")
        except ValueError:
            print("Invalid input. Damage and player number must be numbers.")

    def damage_mob(self):
        """
        Allows the user to damage a mob.
        """
        if not self.mobs:
            print("No mobs created yet. Create a mob first.")
            return

        try:
            for idx, mob_obj in enumerate(self.mobs):
                print(f"{idx + 1}: Mob HP: {mob_obj.get_hp()}, Armor Class: {mob_obj.get_armor_class()}")
            mob_index = int(input("Enter the mob number to damage: ")) - 1

            if mob_index < 0 or mob_index >= len(self.mobs):
                print("Invalid mob number.")
                return

            mob_obj = self.mobs[mob_index]
            damage = int(input(f"Enter damage to apply to Mob {mob_index + 1}: "))
            mob_obj.take_damage(damage)
            print(f"Mob {mob_index + 1} took {damage} damage. Current HP: {mob_obj.get_hp()}")

            if mob_obj.get_hp() <= 0:
                print(f"Mob {mob_index + 1} has died.")
                self.mobs.pop(mob_index)

        except ValueError:
            print("Invalid input. Damage and mob number must be numbers.")
    def viewMobs(self):
        """
        Display all mobs in the session with their stats.
        """
        if not self.mobs:
            print("No mobs available.")
            return

        print("Mobs:")
        for idx, mobObj in enumerate(self.mobs):
            print(f"Name : {self.get_name()} HP: {mobObj.hp}, Armor Class: {mobObj.armor_class}")


    def pick_up_item(self):
        """
        Allows a player to pick up an item once they find it in your campaign
        """
        if not self.players:
            print("No players created yet. Create a player first.")
            return

        if not self.items:
            print("No items available to pick up. Create items first.")
            return

        try:
            # Select a player
            for idx, player_obj in enumerate(self.players):
                print(f"{idx + 1}: {player_obj.get_name()}")
            player_index = int(input("Enter the player number to pick up an item: ")) - 1

            if player_index < 0 or player_index >= len(self.players):
                print("Invalid player number.")
                return

            player_obj = self.players[player_index]

            # Show available items
            print("Available Items:")
            for idx, item_obj in enumerate(self.items):
                print(f"{idx + 1}: {item_obj.get_name()}")
            item_index = int(input("Enter the item number to pick up: ")) - 1

            if item_index < 0 or item_index >= len(self.items):
                print("Invalid item number.")
                return

            # Pick up the item
            item_obj = self.items.pop(item_index)  
            player_obj.get_inventory()[item_obj.get_name()] = item_obj  
            print(f"{player_obj.get_name()} picked up {item_obj.get_name()}.")
        except ValueError:
            print("Invalid input. Player and item numbers must be numbers.")

    def equip_item(self):
        """
        Allows a player to equip an item. The player must have the stat requirement to equip the item if its armor, weapon, or spells
        Stat bonuses will update the players stats
        """
        if not self.players:
            print("No players created yet. Create a player first.")
            return

        for idx, player_obj in enumerate(self.players):
            print(f"{idx + 1}: {player_obj.get_name()}")
        player_index = int(input("Enter the player number to equip an item: ")) - 1

        if player_index < 0 or player_index >= len(self.players):
            print("Invalid player number.")
            return

        player_obj = self.players[player_index]

        if not player_obj.get_inventory():
            print(f"{player_obj.get_name()} has no items in their inventory to equip.")
            return

        print(f"{player_obj.get_name()}'s Inventory:")
        for idx, item_name in enumerate(player_obj.get_inventory().keys()):
            print(f"{idx + 1}: {item_name}")

        item_index = int(input("Enter the item number to equip: ")) - 1

        if item_index < 0 or item_index >= len(player_obj.get_inventory()):
            print("Invalid item number.")
            return

        item_name = list(player_obj.get_inventory().keys())[item_index]
        item_obj = player_obj.get_inventory()[item_name]

        if isinstance(item_obj, armor):
            result = player_obj.equip_armor(item_obj)
        elif isinstance(item_obj, ring):
            result = player_obj.equip_ring(item_obj)
        elif isinstance(item_obj, weapon):
            result = player_obj.equip_weapon(item_obj)
        else:
            print("This item cannot be equipped.")
            return

        print(result)

    def unequip_item(self):
        """
        Allows a player to unequip an item. This will result in a loss of stats in the case of rings and will have their stats 
        updated appropriately.
        """
        if not self.players:
            print("No players created yet. Create a player first.")
            return

        for idx, player_obj in enumerate(self.players):
            print(f"{idx + 1}: {player_obj.get_name()}")
        player_index = int(input("Enter the player number to unequip an item: ")) - 1

        if player_index < 0 or player_index >= len(self.players):
            print("Invalid player number.")
            return

        player_obj = self.players[player_index]

        if not player_obj.get_inventory():
            print(f"{player_obj.get_name()} has no items in their inventory to unequip.")
            return

        print(f"{player_obj.get_name()}'s Inventory:")
        for idx, item_name in enumerate(player_obj.get_inventory().keys()):
            print(f"{idx + 1}: {item_name}")

        item_index = int(input("Enter the item number to unequip: ")) - 1

        if item_index < 0 or item_index >= len(player_obj.get_inventory()):
            print("Invalid item number.")
            return

        item_name = list(player_obj.get_inventory().keys())[item_index]
        item_obj = player_obj.get_inventory()[item_name]

        if isinstance(item_obj, armor):
            result = player_obj.unequip_armor(item_obj)
        elif isinstance(item_obj, ring):
            result = player_obj.unequip_ring(item_obj)
        elif isinstance(item_obj, weapon):
            result = player_obj.unequip_weapon(item_obj)
        else:
            print("This item cannot be unequipped.")
            return

        print(result)

    def rest_at_bonfire(self):
        """
        Iterate through all players and call the flask_bonfire method on each flask in their inventory.
        """
        if not self.players:
            print("No players created yet. Create a player first.")
            return

        for player_obj in self.players:
            player_obj.bonfire()
            inventory = player_obj.get_inventory()
            flasks = [item for item in inventory.values() if isinstance(item, estus)]

            if not flasks:
                print(f"{player_obj.get_name()} has no flasks in their inventory.")
                continue

            for flask in flasks:
                flask.flask_bonfire()
                print(f"{player_obj.get_name()} has restored the flask {flask.get_name()}.")



    def add_weapon_to_mob(self):
        """
        Adds a weapon to a mob. This just a trick to store abilities and attacks of mobs to view if needed.
        """
        if not self.mobs:
            print("No mobs created yet. Create a mob first.")
            return

        try:
            # Select a mob
            for idx, mob_obj in enumerate(self.mobs):
                print(f"{idx + 1}: Mob HP: {mob_obj.get_hp()}, Armor Class: {mob_obj.get_armor_class()}")
            mob_index = int(input("Enter the mob number to add a weapon to: ")) - 1

            if mob_index < 0 or mob_index >= len(self.mobs):
                print("Invalid mob number.")
                return

            mob_obj = self.mobs[mob_index]

            # Select a weapon
            weapons = [item for item in self.items if isinstance(item, weapon)]

            if not weapons:
                print("No weapons available to assign.")
                return

            for idx, weapon_obj in enumerate(weapons):
                print(f"{idx + 1}: {weapon_obj.get_name()}")
            weapon_index = int(input("Enter the weapon number to assign: ")) - 1

            if weapon_index < 0 or weapon_index >= len(weapons):
                print("Invalid weapon number.")
                return

            weapon_obj = weapons[weapon_index]
            mob_obj.add_ability(weapon_obj)
            self.items.remove(weapon_obj) 
            print(f"{weapon_obj.get_name()} added to Mob {mob_index + 1}.")
        except ValueError:
            print("Invalid input. Mob and weapon numbers must be numbers.")

    def view_item_details(self):
        """
        Allows the user to view the stats, amount, description of any item that has been created in the world, player inventory, or mob
        inventory
        """
        try:
            print("Select source to view item details:")
            print("1. World Items")
            print("2. Player Inventory")
            print("3. Mob Inventory")
            choice = int(input("Enter your choice: "))

            if choice == 1:
                if not self.items:
                    print("No items available in the world.")
                    return
                for idx, item in enumerate(self.items):
                    print(f"{idx + 1}: {item.get_name()}")
                item_index = int(input("Select item number to view details: ")) - 1
                if item_index < 0 or item_index >= len(self.items):
                    print("Invalid item number.")
                    return
                item = self.items[item_index]
                print(vars(item))

            elif choice == 2:
                if not self.players:
                    print("No players available.")
                    return
                for idx, player in enumerate(self.players):
                    print(f"{idx + 1}: {player.get_name()}")
                player_index = int(input("Select player number: ")) - 1
                if player_index < 0 or player_index >= len(self.players):
                    print("Invalid player number.")
                    return
                player = self.players[player_index]
                if not player.get_inventory():
                    print(f"{player.get_name()} has no items in their inventory.")
                    return
                for idx, item_name in enumerate(player.get_inventory().keys()):
                    print(f"{idx + 1}: {item_name}")
                item_index = int(input("Select item number to view details: ")) - 1
                item_name = list(player.get_inventory().keys())[item_index]
                item = player.get_inventory()[item_name]
                print(vars(item))

            elif choice == 3:
                if not self.mobs:
                    print("No mobs available.")
                    return
                for idx, mob in enumerate(self.mobs):
                    print(f"{idx + 1}: Mob with HP {mob.get_hp()}")
                mob_index = int(input("Select mob number: ")) - 1
                if mob_index < 0 or mob_index >= len(self.mobs):
                    print("Invalid mob number.")
                    return
                mob = self.mobs[mob_index]
                if not mob.get_inventory():
                    print("Mob has no items in their inventory.")
                    return
                for idx, item_name in enumerate(mob.get_inventory().keys()):
                    print(f"{idx + 1}: {item_name}")
                item_index = int(input("Select item number to view details: ")) - 1
                item_name = list(mob.get_inventory().keys())[item_index]
                item = mob.get_inventory()[item_name]
                print(vars(item))

            else:
                print("Invalid choice.")

        except (ValueError, IndexError):
            print("Invalid input. Please try again.")

    
    def drink_from_flask(self):
        """
        Allows a player to drink from their Estus flask to restore mana or health
        """
        try:
            if not self.players:
                print("No players available.")
                return

            # Select a player
            for idx, player in enumerate(self.players):
                print(f"{idx + 1}: {player.get_name()}")
            player_index = int(input("Select player number: ")) - 1

            if player_index < 0 or player_index >= len(self.players):
                print("Invalid player number.")
                return

            player = self.players[player_index]

            # Check for flask in inventory
            flasks = [item for item in player.get_inventory().values() if isinstance(item, estus)]
            if not flasks:
                print(f"{player.get_name()} has no flask in their inventory.")
                return

            # Select a flask
            for idx, flask in enumerate(flasks):
                print(f"{idx + 1}: {flask.get_name()} (HP: {flask.get_hp()}, Mana: {flask.get_mana()}, Charges: {flask.get_charges()})")
            flask_index = int(input("Select flask to drink from: ")) - 1

            if flask_index < 0 or flask_index >= len(flasks):
                print("Invalid flask number.")
                return

            flask = flasks[flask_index]

            # Check if the flask has charges
            if flask.charges <= 0:
                print(f"{flask.get_name()} has no charges left.")
                return

            # Drink from the flask
            flask.charges -= 1
            player.hp = min(player.get_HP(), player.get_hp() + flask.get_hp())  
            player.mana = min(player.get_MANA(), player.get_mana() + flask.get_mana())  

            print(f"{player.get_name()} drank from {flask.get_name()}. HP: {player.get_hp()}/{player.get_HP()}, Mana: {player.get_mana()}/{player.get_MANA()}, Remaining Charges: {flask.get_charges()}")

        except (ValueError, IndexError):
            print("Invalid input. Please try again.")

    def create_spell(self):
        """
        Allows the creation of a spell
        """
        name = input("Spell Name: ")
        description = input("Description: ")
        n = int(input("Dice Rolls: "))
        dice = int(input("Dice Type: "))
        strength = int(input("Required Strength: "))
        dex = int(input("Required Dexterity: "))
        intelligence = int(input("Required Intelligence: "))
        faith = int(input("Required Faith: "))
        mana_cost = int(input("Mana Cost: "))
        spell_slots_required = int(input("Spell Slots Required: "))

        new_spell = spell(description, name, n, dice, strength, dex, intelligence, faith, mana_cost, spell_slots_required)
        self.items.append(new_spell)
        print(f"Spell '{name}' created.")

    def equip_spell(self):
        """
        Allows a player to equip a spell if they have enough spell slots and meet the spell requirements
        """
        player_index = self.select_player()
        if player_index is None:
            return

        player_obj = self.players[player_index]

        # Filter spells from the player's inventory
        spells = [item for item in player_obj.get_inventory().values() if isinstance(item, spell)]
        if not spells:
            print("No spells available in the player's inventory.")
            return

        for idx, spell_obj in enumerate(spells):
            print(f"{idx + 1}: {spell_obj.get_name()}")

        try:
            spell_index = int(input("Select spell to equip: ")) - 1
            selected_spell = spells[spell_index]

            result = player_obj.equip_spell(selected_spell)
            print(result)
        except (ValueError, IndexError):
            print("Invalid selection.")

    def increase_player_stats(self):
        """
        Allows a player to level up. If they have enough "Souls", they can spend them to level up, with each level increasing the cost
        """
        if not self.players:
            print("No players created yet. Create a player first.")
            return

        try:
            for idx, player_obj in enumerate(self.players):
                print(f"{idx + 1}: {player_obj.get_name()} - Souls: {player_obj.get_souls()}, Level: {player_obj.get_level()}")
            player_index = int(input("Select the player to level up: ")) - 1

            if player_index < 0 or player_index >= len(self.players):
                print("Invalid player number.")
                return

            player_obj = self.players[player_index]
            print(f"Current Soul Cost: {player_obj.get_soul_cost()}")

            if player_obj.get_souls() < player_obj.get_soul_cost():
                print(f"Not enough souls. {player_obj.get_name()} has {player_obj.get_souls()} souls, but needs {player_obj.get_soul_cost()}.")
                return

            print("Select a stat to increase:")
            print("1. Vigor")
            print("2. Attunement")
            print("3. Strength")
            print("4. Dexterity")
            print("5. Intelligence")
            print("6. Faith")
            stat_choice = int(input("Enter your choice: "))

            if stat_choice == 1:
                player_obj.level_stat("vigor")
                print("Vigor increased by 1.")
            elif stat_choice == 2:
                player_obj.level_stat("attunement")
                print("Attunement increased by 1.")
            elif stat_choice == 3:
                player_obj.level_stat("strength")
                print("Strength increased by 1.")
            elif stat_choice == 4:
                player_obj.level_stat("dex")
                print("Dexterity increased by 1.")
            elif stat_choice == 5:
                player_obj.level_stat("intelligence")
                print("Intelligence increased by 1.")
            elif stat_choice == 6:
                player_obj.level_stat("faith")
                print("Faith increased by 1.")
            else:
                print("Invalid choice. No stats were increased.")
                return
            print(f"{player_obj.get_name()} leveled up to Level {player_obj.get_level()}. Remaining Souls: {player_obj.get_souls()}. New Soul Cost: {player_obj.get_soul_cost()}")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

    def unequip_spell(self):
        """
        Unequips a spell from the spell slot
        """
        player_index = self.select_player()
        if player_index is None:
            return

        player_obj = self.players[player_index]

        equipped_spells = [item for item in player_obj.get_inventory().values() if isinstance(item, spell) and item.equipped]
        if not equipped_spells:
            print("No spells equipped.")
            return

        for idx, spell_obj in enumerate(equipped_spells):
            print(f"{idx + 1}: {spell_obj.get_name()}")

        try:
            spell_index = int(input("Select spell to unequip: ")) - 1
            selected_spell = equipped_spells[spell_index]

            result = player_obj.unequipSpell(selected_spell)
            print(result)
        except (ValueError, IndexError):
            print("Invalid selection.")

    def select_player(self):
        """
        Provides logic for other methods to select a player they wish to perform an action on
        """
        if not self.players:
            print("No players available.")
            return None

        for idx, player_obj in enumerate(self.players):
            print(f"{idx + 1}: {player_obj.get_name()}")

        try:
            return int(input("Select player: ")) - 1
        except (ValueError, IndexError):
            print("Invalid player selection.")
            return None
    def delete_item(self):
        """
        Allows the user to delete items from a players inventory. 
        """
        if not self.players:
            print("No players created yet. Create a player first.")
            return

        # Select a player
        for idx, player_obj in enumerate(self.players):
            print(f"{idx + 1}: {player_obj.get_name()}")
        player_index = int(input("Enter the player number to delete an item from: ")) - 1

        if player_index < 0 or player_index >= len(self.players):
            print("Invalid player number.")
            return

        player_obj = self.players[player_index]

        if not player_obj.get_inventory():
            print(f"{player_obj.get_name()} has no items in their inventory.")
            return

        # Select an item to delete
        print(f"{player_obj.get_name()}'s Inventory:")
        for idx, item_name in enumerate(player_obj.get_inventory().keys()):
            print(f"{idx + 1}: {item_name}")

        item_index = int(input("Enter the item number to delete: ")) - 1

        if item_index < 0 or item_index >= len(player_obj.get_inventory()):
            print("Invalid item number.")
            return

        item_name = list(player_obj.get_inventory().keys())[item_index]
        del player_obj.get_inventory()[item_name]
        print(f"{item_name} has been deleted from {player_obj.get_name()}'s inventory.")

    def consume_mana(self):
        """
        When a player casts a spell, use this to drain their mana bar.
        """
        if not self.players:
            print("No players created yet. Create a player first.")
            return

        # Select a player
        for idx, player_obj in enumerate(self.players):
            print(f"{idx + 1}: {player_obj.get_name()}")
        player_index = int(input("Enter the player number to consume mana from: ")) - 1

        if player_index < 0 or player_index >= len(self.players):
            print("Invalid player number.")
            return

        player_obj = self.players[player_index]

        # Enter the amount of mana to consume
        try:
            mana_to_consume = int(input(f"Enter the amount of mana to consume from {player_obj.get_name()}: "))
            if mana_to_consume > player_obj.get_mana():
                print(f"Not enough mana. {player_obj.get_name()} has only {player_obj.get_mana()} mana.")
            else:
                player_obj.use_mana(mana_to_consume)
                print(f"{mana_to_consume} mana consumed. Remaining mana: {player_obj.get_mana()}/{player_obj.get_MANA()}")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def consume_souls(self):
        """
        Souls Items are items that store souls without them being lost when they die. They can consume this item to gain the souls to be able to 
        purchase goods.
        """
        if not self.players:
            print("No players created yet. Create a player first.")
            return

        # Select a player
        for idx, player_obj in enumerate(self.players):
            print(f"{idx + 1}: {player_obj.get_name()}")
        player_index = int(input("Enter the player number to consume souls: ")) - 1

        if player_index < 0 or player_index >= len(self.players):
            print("Invalid player number.")
            return

        player_obj = self.players[player_index]

        # Select a soul item to consume
        soul_items = [item for item in player_obj.get_inventory().values() if isinstance(item, souls)]
        if not soul_items:
            print(f"{player_obj.get_name()} has no soul items in their inventory.")
            return

        for idx, soul_item in enumerate(soul_items):
            print(f"{idx + 1}: {soul_item.get_name()} (Value: {soul_item.get_value()})")

        try:
            soul_index = int(input("Enter the soul item number to consume: ")) - 1
            if soul_index < 0 or soul_index >= len(soul_items):
                print("Invalid selection.")
                return

            soul_item = soul_items[soul_index]
            player_obj.add_souls(soul_item.get_value())
            del player_obj.get_inventory()[soul_item.get_name()]
            print(f"{soul_item.get_name()} consumed. {player_obj.get_name()} now has {player_obj.get_souls()} souls.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def remove_souls(self):
        """
        Logic for removing souls when a player dies.
        """
        if not self.players:
            print("No players created yet. Create a player first.")
            return

        # Select a player
        for idx, player_obj in enumerate(self.players):
            print(f"{idx + 1}: {player_obj.get_name()}")
        player_index = int(input("Enter the player number to remove souls from: ")) - 1

        if player_index < 0 or player_index >= len(self.players):
            print("Invalid player number.")
            return

        player_obj = self.players[player_index]

        try:
            souls_to_remove = int(input(f"Enter the amount of souls to remove from {player_obj.get_name()}: "))
            player_obj.remove_souls(souls_to_remove)
            print(f"{souls_to_remove} souls removed. Remaining souls: {player_obj.get_souls()}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def view_players(self):
        """
        Provides information about a players stats
        """
        if not self.players:
            print("No players available.")
            return

        print("Players:")
        for idx, player_obj in enumerate(self.players):
            print(
                f"Name: {player_obj.get_name()}\n"
                f"HP: {player_obj.get_hp()}/{player_obj.get_HP()}, "
                f"Mana: {player_obj.get_mana()}/{player_obj.get_MANA()}, "
                f"Vigor: {player_obj.get_stat('vigor')}, "
                f"Attunement: {player_obj.get_stat('attunement')}, "
                f"Strength: {player_obj.get_stat('strength')}, "
                f"Dexterity: {player_obj.get_stat('dex')}, "
                f"Intelligence: {player_obj.get_stat('intelligence')}, "
                f"Faith: {player_obj.get_stat('faith')}, "
                f"Souls: {player_obj.get_souls()}, "
                f"Level: {player_obj.get_level()}, "
                f"Armor Class: {player_obj.get_stat('armor_class')}, "
                f"Spell Slots: {player_obj.get_stat('spell_slots')}"
            )

if __name__ == "__main__":
    driver = SessionDriver()
    driver.interact()
