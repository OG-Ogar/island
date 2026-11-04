"""Tests for the important winning, losing, and input-validation paths."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main


class MysteryIslandTests(unittest.TestCase):
    """Check the game rules without requiring a person to type answers."""

    def run_with_answers(self, function, answers, *arguments):
        """Run an interactive function with prepared keyboard answers."""

        output = io.StringIO()
        with patch("builtins.input", side_effect=answers):
            with redirect_stdout(output):
                result = function(*arguments)
        return result, output.getvalue()

    def test_all_required_locations_exist(self):
        """The game should contain every location from the requirements."""

        expected = {"Beach", "Jungle", "Cave", "Old Bridge", "Lighthouse"}
        self.assertTrue(expected.issubset(main.LOCATION_DESCRIPTIONS))

    def test_new_game_starts_with_required_state(self):
        """A new player should start on the Beach with 5 energy and no items."""

        state = main.create_game_state("Ada")
        self.assertEqual(state["energy"], 5)
        self.assertEqual(state["location"], "Beach")
        self.assertEqual(state["inventory"], [])

    def test_get_choice_recovers_from_unexpected_input(self):
        """Words and out-of-range numbers should not crash a menu."""

        result, output = self.run_with_answers(
            main.get_choice,
            ["hello", "99", "2"],
            ["First", "Second"],
        )
        self.assertEqual(result, 2)
        self.assertIn("Invalid choice", output)

    def test_items_can_only_be_added_once(self):
        """Rope and Lantern should never be duplicated in the inventory."""

        state = main.create_game_state("Ada")
        self.assertTrue(main.add_item(state, "Rope"))
        self.assertFalse(main.add_item(state, "Rope"))
        self.assertTrue(main.add_item(state, "Lantern"))
        self.assertFalse(main.add_item(state, "Lantern"))
        self.assertEqual(state["inventory"], ["Rope", "Lantern"])

    def test_bridge_requires_rope(self):
        """Crossing without Rope should fail and cost energy."""

        state = main.create_game_state("Ada")
        state["location"] = "Old Bridge"
        result, output = self.run_with_answers(main.visit_bridge, ["1"], state)
        self.assertEqual(result, "continue")
        self.assertEqual(state["location"], "Old Bridge")
        self.assertEqual(state["energy"], 4)
        self.assertIn("need Rope", output)

        main.add_item(state, "Rope")
        self.run_with_answers(main.visit_bridge, ["1"], state)
        self.assertEqual(state["location"], "Lighthouse")

    def test_lighthouse_requires_lantern(self):
        """The player cannot win without a Lantern."""

        state = main.create_game_state("Ada")
        state["location"] = "Lighthouse"
        result, output = self.run_with_answers(main.visit_lighthouse, ["1"], state)
        self.assertEqual(result, "continue")
        self.assertEqual(state["energy"], 4)
        self.assertIn("need a working Lantern", output)

        main.add_item(state, "Lantern")
        result, _ = self.run_with_answers(main.visit_lighthouse, ["1"], state)
        self.assertEqual(result, "win")

    def test_complete_winning_path(self):
        """A careful player can collect both objects and light the beacon."""

        answers = [
            "1",  # Beach: collect Rope.
            "2",  # Beach to Jungle.
            "1",  # Jungle to Cave.
            "1",  # Cave: collect Lantern.
            "3",  # Cave to Jungle.
            "2",  # Jungle to Old Bridge.
            "1",  # Cross the bridge with Rope.
            "1",  # Light the beacon with Lantern.
        ]
        result, output = self.run_with_answers(main.run_game, answers, "Ada")
        self.assertEqual(result, "win")
        self.assertIn("YOU WIN", output)
        self.assertIn("rescue boat", output)

    def test_complete_losing_path(self):
        """Several unsafe decisions should reduce energy to zero."""

        answers = [
            "3", "1",  # Beach: grab from the tide pool and get pinched.
            "2",       # Walk to the Jungle.
            "4", "1",  # Eat harmful red berries.
            "1",       # Walk to the Cave.
            "2",       # Enter the dangerous side passage.
        ]
        result, output = self.run_with_answers(main.run_game, answers, "Ada")
        self.assertEqual(result, "lose")
        self.assertIn("YOU LOSE", output)
        self.assertIn("run out of energy", output)

    def test_quit_works_inside_a_nested_menu(self):
        """The q command should work even inside a decision submenu."""

        result, output = self.run_with_answers(main.run_game, ["3", "q"], "Ada")
        self.assertEqual(result, "quit")
        self.assertIn("GAME ENDED", output)

    def test_replay_prompt_rejects_bad_input(self):
        """The replay question should recover from unexpected answers."""

        result, output = self.run_with_answers(main.ask_to_replay, ["maybe", "yes"])
        self.assertTrue(result)
        self.assertIn("Please enter", output)


if __name__ == "__main__":
    unittest.main()
