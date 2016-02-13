"""Test for specific_weapons.py."""
import os
import sys
import unittest

try:
    import combat
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    import combat

import sprite


class TestCharacter(unittest.TestCase):

    def setUp(self):
        def dummy(*args, **kwargs):
            pass

        class Dummy:
            pass

        class Scene():
            add_obj = dummy
            rem_obj = dummy

            gfx = Dummy()

            gfx.msg_log = Dummy()
            gfx.msg_log.add = print

            gfx.hp_bar = Dummy()
            gfx.hp_bar.set_value = dummy

        self.scene = Scene()

        self.player = sprite.Player(scene=self.scene, x=0, y=0,
                                    _class="fighter",
                                    race="human")

    def tearDown(self):
        pass

    def test_human_fighter(self):
        player = self.player

        self.assertEqual(player.combat.race, "human")
        self.assertEqual(player.combat._class, "fighter")
        self.assertEqual(player.combat.feats.points, 3)

        player.combat.feats.on_equip()

        from tree_view import tree_view
        tree_view(player.combat.feats, expand=[combat.feats.FeatNode])


if __name__ == '__main__':
    unittest.main(verbosity=10)
