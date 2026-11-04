"""Mystery Island: a beginner-friendly text adventure.

This game only uses Python's built-in features.  The comments explain each
part so a new Python learner can follow the program from top to bottom.
"""


# Store every location description in one dictionary.
# A dictionary connects a key, such as "Beach", to a value, such as its text.
LOCATION_DESCRIPTIONS = {
    "Beach": "Waves crash beside your broken boat and scattered driftwood.",
    "Jungle": "Tall trees surround three paths, and strange berries grow nearby.",
    "Cave": "Cold air leaves the cave while water drips from the dark ceiling.",
    "Old Bridge": "A damaged bridge hangs above a deep rocky gorge.",
    "Lighthouse": "The silent lighthouse lamp waits at the top of the tower.",
}


def show_title():
    """Display the title, story, and instructions."""

    # A repeated equals sign creates a simple border around the title.
    print("=" * 60)
    # Print the name of the game.
    print("          MYSTERY ISLAND: THE LOST LIGHTHOUSE")
    # Print the bottom title border.
    print("=" * 60)
    # Print a blank line to make the text easier to read.
    print()
    # Explain why the player is on the island.
    print("A storm wrecked your boat, and you wake up on a strange beach.")
    # Explain the main problem.
    print("The lighthouse is dark, the old bridge is unsafe, and a rescue")
    # Explain the goal of the adventure.
    print("boat will only see you if you restore the lighthouse beacon.")
    # Separate the story from the instructions.
    print()
    # Print an instruction heading.
    print("HOW TO PLAY")
    # Explain how numbered menus work.
    print("- Type the number beside an action, then press Enter.")
    # Explain the energy system.
    print("- You start with 5 energy. Most movement costs 1 energy.")
    # Explain the losing condition.
    print("- If your energy reaches 0, you lose.")
    # Explain that objects are needed for puzzles.
    print("- Explore carefully and collect objects needed for the bridge")
    # Continue the previous instruction on another readable line.
    print("  and lighthouse.")
    # Explain the universal quit command.
    print("- Enter q or quit at any numbered menu to leave the game.")
    # Add space before asking for the player's name.
    print()


def read_input(prompt):
    """Read keyboard input safely and return None if input is interrupted."""

    # The try block runs code that could be interrupted by the user.
    try:
        # input() displays the prompt and waits for text from the keyboard.
        return input(prompt)
    # EOFError happens when an input stream closes unexpectedly.
    # KeyboardInterrupt happens when the user presses Ctrl+C.
    except (EOFError, KeyboardInterrupt):
        # Move to a clean line after an interrupted prompt.
        print("\nInput ended. Leaving the game safely.")
        # None is a special value meaning that no answer is available.
        return None


def get_player_name():
    """Ask repeatedly until the player enters a non-empty name."""

    # A while loop repeats until this function returns a name or None.
    while True:
        # Ask for text using the safe input function.
        answer = read_input("Enter your name (or q to quit): ")
        # Stop if keyboard input was closed or interrupted.
        if answer is None:
            return None
        # strip() removes accidental spaces before and after the name.
        name = answer.strip()
        # casefold() allows Q, q, QUIT, and quit to mean the same thing.
        if name.casefold() in ("q", "quit"):
            return None
        # A non-empty string is a valid beginner-friendly player name.
        if name:
            return name
        # Explain the problem instead of allowing a blank name.
        print("Please enter at least one visible character for your name.")


def get_choice(options):
    """Display a menu and return a valid option number or None for quit."""

    # Keep asking until the player enters a valid menu number or quits.
    while True:
        # enumerate() gives each option a number, beginning with 1.
        for number, text in enumerate(options, start=1):
            # An f-string places the number and option text into one line.
            print(f"{number}. {text}")

        # Ask the player to choose from the displayed options.
        answer = read_input("Choose an action: ")
        # Treat interrupted or closed input like a safe quit request.
        if answer is None:
            return None
        # Clean spaces and make word commands lowercase.
        cleaned_answer = answer.strip().casefold()
        # Allow the player to quit from every numbered menu.
        if cleaned_answer in ("q", "quit"):
            return None

        # try attempts to convert the player's text into an integer.
        try:
            choice = int(cleaned_answer)
        # ValueError means the text was not a whole number.
        except ValueError:
            # Give a helpful message and let the loop ask again.
            print("Invalid choice. Enter a menu number, q, or quit.")
            continue

        # Accept only numbers that belong to the current menu.
        if 1 <= choice <= len(options):
            return choice
        # Reject numbers that are too small or too large without crashing.
        print(f"Invalid choice. Enter a number from 1 to {len(options)}.")


def create_game_state(player_name):
    """Create and return all information that changes during one game."""

    # A dictionary keeps related game values together under named keys.
    return {
        # Remember the name entered by the player.
        "name": player_name,
        # Every new game begins with exactly 5 energy.
        "energy": 5,
        # Every new game begins on the Beach.
        "location": "Beach",
        # The inventory begins as an empty list.
        "inventory": [],
        # This flag prevents the tide-pool event from being repeated.
        "tide_pool_checked": False,
        # This flag prevents the berry event from being repeated.
        "berries_checked": False,
        # This flag prevents repeated energy loss in the cave passage.
        "cave_passage_checked": False,
    }


def show_status(state):
    """Print the player's current energy, location, and inventory."""

    # Print a small heading for the status information.
    print("\n--- PLAYER STATUS ---")
    # Read the player's name from the state dictionary.
    print(f"Name: {state['name']}")
    # Read the current energy from the state dictionary.
    print(f"Energy: {state['energy']}")
    # Read the current location from the state dictionary.
    print(f"Location: {state['location']}")
    # Check whether the inventory list contains any objects.
    if state["inventory"]:
        # join() combines the object names into readable comma-separated text.
        print("Inventory: " + ", ".join(state["inventory"]))
    else:
        # Clearly tell the player when no objects have been collected.
        print("Inventory: empty")
    # Print a closing line under the status information.
    print("---------------------\n")


def has_item(state, item_name):
    """Return True when an item is already in the inventory."""

    # The in operator checks whether a value exists inside a list.
    return item_name in state["inventory"]


def add_item(state, item_name):
    """Add an inventory object once and report whether it was added."""

    # Do not add a second copy if the player already owns this object.
    if has_item(state, item_name):
        # False tells the caller that the inventory did not change.
        return False
    # append() places the new object at the end of the inventory list.
    state["inventory"].append(item_name)
    # True tells the caller that the object was successfully added.
    return True


def change_energy(state, amount, reason):
    """Increase or decrease energy and explain why it changed."""

    # Add a positive amount or subtract a negative amount from energy.
    state["energy"] += amount
    # Prevent the displayed energy from becoming a confusing negative number.
    if state["energy"] < 0:
        state["energy"] = 0
    # Print the story reason for the change.
    print(reason)
    # Describe an energy gain with a plus sign.
    if amount > 0:
        print(f"Energy +{amount}. Current energy: {state['energy']}")
    # Describe an energy cost or injury with its negative number.
    elif amount < 0:
        print(f"Energy {amount}. Current energy: {state['energy']}")


def move_player(state, destination):
    """Move to a normal destination and spend 1 energy."""

    # Change the player's current location.
    state["location"] = destination
    # Normal travel always costs one energy point.
    change_energy(state, -1, f"You travel to the {destination}.")


def visit_beach(state):
    """Show and process the Beach menu."""

    # Build the choices that are available at the Beach.
    options = [
        "Search the broken boat",
        "Walk into the Jungle",
        "Examine the tide pools",
        "Show player status",
    ]
    # Ask the player to choose one Beach action.
    choice = get_choice(options)
    # None means the player entered q, quit, or interrupted input.
    if choice is None:
        return "quit"

    # Choice 1 searches for the bridge item.
    if choice == 1:
        # add_item() makes sure Rope can only be collected once.
        if add_item(state, "Rope"):
            print("Under a torn sail, you find a strong Rope and take it.")
        else:
            print("You already searched the boat and took its useful Rope.")
    # Choice 2 moves to another required location.
    elif choice == 2:
        move_player(state, "Jungle")
    # Choice 3 starts a decision with a helpful or harmful consequence.
    elif choice == 3:
        # Propagate a quit request made inside the tide-pool menu.
        if explore_tide_pool(state) == "quit":
            return "quit"
    # Choice 4 displays information without costing energy.
    elif choice == 4:
        show_status(state)
    # The game should continue after every non-quit Beach action.
    return "continue"


def explore_tide_pool(state):
    """Run the one-time tide-pool decision."""

    # Stop the player from repeating this event for unlimited energy.
    if state["tide_pool_checked"]:
        print("The tide pool is now empty. There is nothing else to find.")
        return "continue"
    # Explain the two visible approaches.
    print("A silver shape flashes between sharp rocks as a crab watches you.")
    # Ask whether the player acts quickly or carefully.
    choice = get_choice([
        "Grab the silver shape quickly",
        "Search the shore carefully instead",
        "Leave the tide pool alone",
    ])
    # Returning None here quits from the nested menu as well.
    if choice is None:
        # Send the nested quit request back to the main location loop.
        return "quit"
    # A completed risky or careful search can happen only once.
    if choice in (1, 2):
        state["tide_pool_checked"] = True
    # The quick choice causes an injury and costs energy.
    if choice == 1:
        change_energy(state, -1, "A crab pinches your hand; the silver shape was only a shell.")
    # The careful choice finds food and restores energy.
    elif choice == 2:
        change_energy(state, 1, "You avoid the crab and find a fresh coconut to drink.")
    # The safe choice changes nothing.
    else:
        print("You decide that saving your energy is more important.")
    # Tell the Beach menu that normal play should continue.
    return "continue"


def visit_jungle(state):
    """Show and process the Jungle menu."""

    # Display paths to two locations plus the Beach.
    choice = get_choice([
        "Follow the rocky path to the Cave",
        "Follow the gorge path to the Old Bridge",
        "Return to the Beach",
        "Inspect the strange berries",
        "Show player status",
    ])
    # Allow quitting from this menu.
    if choice is None:
        return "quit"
    # Travel to the Cave and spend energy.
    if choice == 1:
        move_player(state, "Cave")
    # Travel to the Old Bridge and spend energy.
    elif choice == 2:
        move_player(state, "Old Bridge")
    # Travel back to the Beach and spend energy.
    elif choice == 3:
        move_player(state, "Beach")
    # Examine berries in a separate decision.
    elif choice == 4:
        # Propagate a quit request made inside the berry menu.
        if inspect_berries(state) == "quit":
            return "quit"
    # Display status without changing the game.
    elif choice == 5:
        show_status(state)
    # Continue after the selected Jungle action.
    return "continue"


def inspect_berries(state):
    """Run the one-time berry decision."""

    # The result cannot be repeated to gain endless energy.
    if state["berries_checked"]:
        print("You already tested the berries and should leave the bush alone.")
        return "continue"
    # Give the player a clue instead of making the decision completely random.
    print("Birds happily eat the dark blue berries but avoid the bright red ones.")
    # Ask the player to use the clue.
    choice = get_choice([
        "Eat the bright red berries",
        "Eat the dark blue berries",
        "Do not eat any berries",
    ])
    # Do nothing if the player quits the nested menu.
    if choice is None:
        return "quit"
    # Mark the bush as checked only after an eating choice.
    if choice in (1, 2):
        state["berries_checked"] = True
    # Red berries make the player ill.
    if choice == 1:
        change_energy(state, -1, "The red berries taste bitter and make you feel sick.")
    # Blue berries safely restore energy.
    elif choice == 2:
        change_energy(state, 1, "The blue berries are sweet and restore your strength.")
    # Leaving is safe but provides no energy.
    else:
        print("You leave the berries untouched.")
    # Tell the Jungle menu that normal play should continue.
    return "continue"


def visit_cave(state):
    """Show and process the Cave menu."""

    # Display the Cave actions.
    choice = get_choice([
        "Pick up the old Lantern near the entrance",
        "Squeeze through a narrow side passage",
        "Return to the Jungle",
        "Read the markings on the wall",
        "Show player status",
    ])
    # Allow quitting from the Cave.
    if choice is None:
        return "quit"
    # Choice 1 collects the lighthouse item.
    if choice == 1:
        # add_item() prevents duplicate Lantern objects.
        if add_item(state, "Lantern"):
            print("You take the Lantern. It still contains a little lamp oil.")
        else:
            print("The Lantern is already safely stored in your inventory.")
    # Choice 2 is a risky exploration decision.
    elif choice == 2:
        # Prevent the same falling-rock injury from happening repeatedly.
        if state["cave_passage_checked"]:
            print("The collapsed side passage is still blocked.")
        else:
            # Remember that the passage has now been explored.
            state["cave_passage_checked"] = True
            # Apply the consequence of the risky decision.
            change_energy(state, -1, "Loose stones fall, and you barely escape the passage.")
    # Choice 3 returns to the Jungle.
    elif choice == 3:
        move_player(state, "Jungle")
    # Choice 4 gives useful puzzle clues.
    elif choice == 4:
        print("The markings show Rope over a bridge and a Lantern beside a beacon.")
    # Choice 5 displays current information.
    elif choice == 5:
        show_status(state)
    # Continue after the Cave action.
    return "continue"


def visit_bridge(state):
    """Show and process the Old Bridge menu."""

    # Display actions for the bridge puzzle.
    choice = get_choice([
        "Try to cross toward the Lighthouse",
        "Return to the Jungle",
        "Inspect the damaged bridge",
        "Show player status",
    ])
    # Allow quitting from the bridge.
    if choice is None:
        return "quit"
    # Choice 1 attempts to solve the bridge puzzle.
    if choice == 1:
        # Rope is specifically required to cross safely.
        if has_item(state, "Rope"):
            # Crossing with Rope does not cost energy because it creates a safe line.
            state["location"] = "Lighthouse"
            # Explain why this special movement is free.
            print("You secure the Rope, repair a handline, and cross safely.")
        else:
            # Trying without Rope has a meaningful harmful consequence.
            change_energy(state, -1, "A plank breaks! You jump back, exhausted. You need Rope.")
    # Choice 2 uses normal movement and costs energy.
    elif choice == 2:
        move_player(state, "Jungle")
    # Choice 3 provides the puzzle clue.
    elif choice == 3:
        print("The handline is missing. Strong Rope could make the crossing safe.")
    # Choice 4 displays player information.
    elif choice == 4:
        show_status(state)
    # Continue after the bridge action.
    return "continue"


def visit_lighthouse(state):
    """Show and process the Lighthouse menu."""

    # Display actions for the final puzzle.
    choice = get_choice([
        "Try to light the beacon",
        "Inspect the beacon machinery",
        "Cross back to the Old Bridge",
        "Show player status",
    ])
    # Allow quitting from the final location.
    if choice is None:
        return "quit"
    # Choice 1 attempts to finish the game.
    if choice == 1:
        # Lantern is specifically required to light the old beacon.
        if has_item(state, "Lantern"):
            # Returning win tells the main loop that the adventure is complete.
            return "win"
        # A failed attempt wastes precious energy.
        change_energy(state, -1, "The dark mechanism will not ignite. You need a working Lantern.")
    # Choice 2 gives a final direct clue.
    elif choice == 2:
        print("The beacon has oil but no flame. A Lantern could ignite it.")
    # Choice 3 lets the player leave without an extra crossing cost.
    elif choice == 3:
        state["location"] = "Old Bridge"
        print("You use your secured Rope to cross back to the Old Bridge.")
    # Choice 4 displays current information.
    elif choice == 4:
        show_status(state)
    # Continue if the player has not won.
    return "continue"


def show_location(state):
    """Display the current location heading and description."""

    # Read the current location once for simpler lines below.
    location = state["location"]
    # Print a clear heading around the location name.
    print(f"\n=== {location.upper()} ===")
    # Look up and print this location's description.
    print(LOCATION_DESCRIPTIONS[location])
    # Remind the player of remaining energy every turn.
    print(f"Energy remaining: {state['energy']}")


def run_game(player_name):
    """Run one complete game and return win, lose, or quit."""

    # Create fresh state so replaying never reuses old items or energy.
    state = create_game_state(player_name)
    # Connect location names to the functions that handle their menus.
    location_handlers = {
        "Beach": visit_beach,
        "Jungle": visit_jungle,
        "Cave": visit_cave,
        "Old Bridge": visit_bridge,
        "Lighthouse": visit_lighthouse,
    }

    # Continue taking turns while the player still has energy.
    while state["energy"] > 0:
        # Show where the player is before each decision.
        show_location(state)
        # Find the correct menu function for the current location.
        handler = location_handlers[state["location"]]
        # Run one action and store its result.
        result = handler(state)
        # Stop immediately when the lighthouse is lit.
        if result == "win":
            # Print a clear success message.
            print("\n*** YOU WIN! ***")
            print(f"{player_name} lights the beacon. The rescue boat sees it")
            print("and carries you safely away from Mystery Island!")
            return "win"
        # Stop immediately when the player chooses to quit.
        if result == "quit":
            # Print a clear quit message that is different from losing.
            print("\n*** GAME ENDED ***")
            print("You leave Mystery Island for another day.")
            return "quit"

    # Reaching this line means the while condition failed at zero energy.
    print("\n*** YOU LOSE! ***")
    # Explain the exact losing condition.
    print(f"{player_name} has run out of energy before lighting the beacon.")
    # Encourage another attempt.
    print("The rescue boat passes the dark island. Try a safer path next time.")
    # Return the outcome so tests and main() can understand what happened.
    return "lose"


def ask_to_replay():
    """Ask whether the player wants another fresh game."""

    # Repeat until yes, no, or interrupted input is received.
    while True:
        # Ask a short replay question.
        answer = read_input("\nWould you like to play again? (y/n): ")
        # Closed input means no replay.
        if answer is None:
            return False
        # Normalize spaces and letter case.
        cleaned_answer = answer.strip().casefold()
        # Accept common forms of yes.
        if cleaned_answer in ("y", "yes"):
            return True
        # Accept no and the normal quit commands.
        if cleaned_answer in ("n", "no", "q", "quit"):
            return False
        # Unexpected text receives help instead of causing a crash.
        print("Please enter y for yes or n for no.")


def main():
    """Display the introduction and control new games and replays."""

    # Show the title and instructions once when the program starts.
    show_title()
    # Keep starting games while the player chooses replay.
    while True:
        # Ask for a new name at the beginning of each game.
        player_name = get_player_name()
        # End safely if the player quits at the name prompt.
        if player_name is None:
            print("Thanks for visiting Mystery Island. Goodbye!")
            return
        # Run one complete adventure for this player.
        run_game(player_name)
        # Stop if the player does not request another game.
        if not ask_to_replay():
            print("Thanks for playing Mystery Island. Goodbye!")
            return
        # Separate the replay from the previous ending.
        print("\nStarting a new adventure with full energy and no items...\n")


# This condition is True only when this file is run directly.
if __name__ == "__main__":
    # Start the program.
    main()
