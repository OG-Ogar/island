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

def main():
    """Run the opening of the game"""
    show_title()
    player_name = get_player_name()

    energy = 5
    location = "Beach"
    inventory = []

    show_status(player_name, energy, location, inventory)

if __name__ =="__main__":
    main()

def get_choice(options):
    """show a number menu and return a valid choice as an int."""
    while True:
        for number, text in enumerate(options, start=1):
            print(f"{number}. {text}")

        answer = input("choose: ").strip()

        if answer.isdigit():
            choice = int(answer)
            if 1 <= choice <= len(options):
                return choice
        print("please enter a number from 1 to", len(options))

choice = get_choice(["Go to the Jungle", "Walk to the Old Bridge", "Quit"])
print("You chose", choice)