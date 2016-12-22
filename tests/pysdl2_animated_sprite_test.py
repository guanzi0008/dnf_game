"""Test Scene for manager using pysdl2."""

import random
import unittest

import sdl2

if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data.constants import TILE_W, TILE_H
from scene_manager.manager import Manager, TextureSprite
from scene_manager.scenes import base_scenes


class TilesTextPySDL2(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(
            scene=SceneTilesTextPySDL2, test=False).execute()


class SceneTilesTextPySDL2(base_scenes.SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        self.ignore_regular_update = True
        manager = self.manager
        factory = manager.factory

        self.sprite = factory.from_tileset(area=(
            0, 3 * TILE_H, 10 * TILE_W, TILE_H))
        self.sprite.set_animation(10, 1, TILE_W, TILE_H)
        self.sprite.position = 128, 128
        self.on_update()

    def on_key_press(self, event, mod):
        """..."""
        if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
            self.quit()
        self.sprite.step(col=1)
        self.on_update()

    def on_update(self):
        """..."""
        manager = self.manager
        manager.renderer.clear()

        manager.spriterenderer.render(sprites=self.sprite)
        manager.present()


def tile_shuffler(w, h):
    """Create the xy coordinates in the possible range and shuffle them.

    Args:
        w (int): width of the tileset
        h (int): height of the tileset

    Returns:
        list of tuples with coordinates (x, y)

    """
    l = [(x * TILE_W, y * TILE_H) for x in range(w) for y in range(h)]
    random.shuffle(l)
    return l

if __name__ == '__main__':
    unittest.main(verbosity=2)