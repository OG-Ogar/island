def show_title():
    """print the game title and instructions"""
    print("=" * 50)
    print(" MYSTERY ISLAND: THE LOST LIGHTHOUSE")
    print("=" * 50)
    print()
    print("A storm has  wrecked your boat and you wake up on a")
    print("strange island. The lighthouse is dark and the bridge")
    print("is locked. A rescue boat will only come if you restore")
    print("the beacon.")
    print()
    print("HOW to PLAY")
    print("  - Type the number of a menu option and press Enter.")
    print("  - Moving and risky actions cost energy.")
    print("  - If your energy reaches 0, you lose.")
    print("  - Find the right items, cross the Old Bridge, and")
    print("  - Light the Lighthouse.")
    print("  - Type 'q' at any menu to quit")
    print()

def get_player_name():
    """Ask for the player's name until a none-blank one is given."""
    while True:
        name = input("Enter your name: ").strip()
        if name != "":
            return name
        print("please fill in your name")

player_name = get_player_name()
print("Welcome,", player_name)

def show_status(name, energy, location, inventory):
    """print the player's current status."""
    print("---STATUS---")
    print("Name: ", name)
    print("Energy: ", energy)
    print("Location: ", location)
    if inventory:
        print("Inventory: ", ", ".join(inventory))
    else:
        print("Inventory: empty")

show_status("Sam", 5, "Beach", [])
show_status("Sam", 4, "Jungle", ["rope", "lantern"])