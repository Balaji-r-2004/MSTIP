class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.connections = {}
        self.items = []
        self.enemy = None

    def connect(self, direction, other_room):
        self.connections[direction] = other_room

    def describe(self):
        print(f"\n🗺️ You are in {self.name}")
        print(self.description)
        if self.items:
            print("Items here:", ", ".join(item.name for item in self.items))
        if self.enemy:
            print(f"⚔️ Enemy present: {self.enemy.name}")
        print("Exits:", ", ".join(self.connections.keys()))

class Item:
    def __init__(self, name):
        self.name = name

class Enemy:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    def take_damage(self, dmg):
        self.hp -= dmg
        return self.hp <= 0

class Player:
    def __init__(self, start_room):
        self.current_room = start_room
        self.inventory = []

    def move(self, direction):
        if direction in self.current_room.connections:
            self.current_room = self.current_room.connections[direction]
            print(f"You move {direction}.")
        else:
            print("🚫 You can't go that way.")

    def take_item(self, item_name):
        for item in self.current_room.items:
            if item.name.lower() == item_name:
                self.inventory.append(item)
                self.current_room.items.remove(item)
                print(f"✅ You took the {item.name}.")
                return
        print("No such item here.")

    def fight(self):
        enemy = self.current_room.enemy
        if enemy:
            print(f"You attack {enemy.name}!")
            defeated = enemy.take_damage(10)
            if defeated:
                print(f"🎉 You defeated {enemy.name}!")
                self.current_room.enemy = None
            else:
                print(f"{enemy.name} has {enemy.hp} HP left.")
        else:
            print("No enemy to fight here.")

def setup_game():
    # Create rooms
    foyer = Room("Foyer", "A dusty entrance with creaky floors.")
    hall = Room("Hall", "A grand hallway with faded portraits.")
    armory = Room("Armory", "Racks of rusty weapons.")
    
    # Connect rooms
    foyer.connect("north", hall)
    hall.connect("south", foyer)
    hall.connect("east", armory)
    armory.connect("west", hall)

    # Add items
    foyer.items.append(Item("key"))
    armory.items.append(Item("sword"))

    # Add enemy
    hall.enemy = Enemy("Goblin", 20)

    return Player(foyer)

def main():
    print("⚔️ Welcome to Dungeon Explorer!")
    player = setup_game()

    while True:
        player.current_room.describe()
        command = input("\n> ").strip().lower()

        if command.startswith("go "):
            direction = command[3:]
            player.move(direction)
        elif command.startswith("take "):
            item_name = command[5:]
            player.take_item(item_name)
        elif command == "fight":
            player.fight()
        elif command == "inventory":
            items = ", ".join(item.name for item in player.inventory)
            print("🧺 Inventory:", items if items else "Empty")
        elif command == "look":
            player.current_room.describe()
        elif command == "quit":
            print("👋 Thanks for playing!")
            break
        else:
            print("❓ Unknown command. Try: go, take, fight, inventory, look, quit.")

if __name__ == "__main__":
    main()
