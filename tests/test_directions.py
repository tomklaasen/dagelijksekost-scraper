#!/usr/bin/env python3
"""Tests for dagelijksekost.directions, against a saved copy of a recipe page.

Run with: python -m unittest discover tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from dagelijksekost import directions

FIXTURE_HTML = (Path(__file__).parent / "fixtures" / "dagelijksekost_veggie_okonomiyaki.html").read_text(encoding="utf-8")

FIRST_STEP = "Laat de gedroogde paddenstoelen en de kombu minstens een uur weken in koud water."
LAST_STEP  = "Werk af met streepjes okonomiyakisaus en kewpie mayonaise."


class DirectionsTest(unittest.TestCase):
    def test_extracts_every_step_from_the_rsc_payload(self):
        steps = [s for s in directions(FIXTURE_HTML).split("\n") if not s.startswith("Tip: ")]

        self.assertEqual(15, len(steps))
        self.assertEqual(FIRST_STEP, steps[0])
        self.assertEqual(LAST_STEP, steps[-1])

    def test_keeps_the_tip_that_belongs_to_a_step(self):
        lines = directions(FIXTURE_HTML).split("\n")

        self.assertIn("Tip: Of laat een scheut olie heet worden in een anti-kleefpan, schep het beslag in de pan, "
                      "laat de onderkant zacht bakken, draai de pannenkoek om en bak ze nog even op de andere kant.",
                      lines)

    def test_returns_none_when_the_page_has_no_rsc_payload(self):
        self.assertIsNone(directions(FIXTURE_HTML.replace("self.__next_f.push", "self.__removed.push")))

    def test_returns_none_for_a_page_that_is_not_a_recipe(self):
        self.assertIsNone(directions("<html><body>geen payload</body></html>"))


if __name__ == "__main__":
    unittest.main()
