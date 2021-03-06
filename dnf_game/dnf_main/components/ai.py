"""Defines monster's behaviours."""

import random

from dnf_game.data.constants import CONFUSE_NUM_TURNS
from dnf_game.dnf_main.data_handler import get_color


class Ai:
    """..."""

    owner = None
    effect = None

    def __init__(self, owner):
        """..."""
        self.owner = owner


class Confused(Ai):
    """AI for a temporarily confused monster.

    It reverts to previous AI after a while).
    """

    def __init__(self, num_turns=CONFUSE_NUM_TURNS, **kwargs):
        """..."""
        self.num_turns = num_turns
        self.effect = True
        super().__init__(**kwargs)

    def take_turn(self):
        """..."""
        # some kind of lock to prevent double calling AND queueing of
        # same objects on a single turn.

        monster = self.owner

        monster.path = None

        if self.num_turns > 0:  # still confused...
            # move in a random direction, and decrease the number of turns
            # confused
            if monster.visible:
                monster.scene.msg_log.add(
                    (monster.name + " looks confused"), get_color("pink"))
            if random.randint(1, 100) > 33:
                monster.move_rnd()
            else:
                monster.move()
            self.num_turns -= 1

        # restore the previous AI (this one will be deleted because it's not
        # referenced anymore)
        else:
            self.effect = False
            monster.ai = monster.default_ai
            monster.color = monster.default_color
            monster.scene.msg_log.add(
                'The ' + monster.name + ' is no longer confused!',
                get_color("yellow"))


class Basic(Ai):
    """AI for a basic monster."""

    def take_turn(self):
        """A basic monster takes its turn."""
        # some kind of lock to prevent double calling AND queueing of
        # same objects on a single turn.

        monster = self.owner

        target = monster.scene.player
        distance = monster.distance_to(monster.scene.player)

        if not monster.visible and not monster.path:
            monster.move_rnd()
            print("AI1 (not visible not pathing): monster.move_rnd()")
        elif distance >= 2:  # implement reach here
            if monster.path:
                # continue following the path
                try:
                    old_path = list(monster.path)
                    moved = monster.move(monster.path.pop(2))
                except:
                    print("-AI2: failed to follow path")
                    moved = False
                else:
                    print("AI2: following path, dist {}".format(distance))
                    # show the path remaining
                    for i, pos in enumerate(old_path[2:-1]):

                        if i == 0:
                            color = get_color("orange")
                        elif i == 1:
                            color = get_color("yellow")
                        else:
                            color = get_color("green")
                        """
                        monster.scene.tile_fx.add(
                            coord=[pos],
                            color=color,
                            duration=1)
                        """
            else:
                moved = False

            if not moved:
                # find a new path
                monster.path = monster.move_towards(target=target)
                try:
                    """
                    monster.scene.tile_fx.add(
                        coord=monster.path[2:-1],
                        color=get_color("green"),
                        duration=1)
                    """
                    moved = monster.move(monster.path.pop(2))
                    print("AI3: new path {}, FROM {}, TO {}, DIST {}".format(
                        monster.path,
                        tuple(monster.pos),
                        tuple(monster.scene.player.pos),
                        distance))
                except:
                    monster.scene.pathing = []
                    monster.move_rnd()
                    print("AI4: path failed: monster.move_rnd()")

        # close enough, attack! (if the player is still alive.)
        elif target.combat.hit_points_current > 0:
            try:
                monster.combat.attack(target)
            except Exception as e:
                print(monster.combat.name)
                raise e
