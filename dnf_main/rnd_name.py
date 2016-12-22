"""..."""

import os
import random

from dnf_game.util import packer, RangedDictionary


class NameGen(dict):
    """..."""

    @classmethod
    def __init__(cls):
        """..."""
        _path = os.path.join(os.path.dirname(__file__), '..', 'data')

        cls.names_db = packer.unpack_json(os.path.join(_path, 'names.bzp'))

        cls.name_dict = {
            'human': {
                'names': RangedDictionary({
                    range(0, 75): 'human',
                    range(75, 100): 'generic'
                }),
                'surnames': RangedDictionary({
                    range(0, 75): 'human',
                    range(75, 100): 'generic'
                })
            },
            'dwarf': {
                'names': RangedDictionary({
                    range(0, 100): 'dwarf'
                }),
                'surnames': RangedDictionary({
                    range(0, 100): 'dwarf'
                })
            },
            'elf': {
                'names': RangedDictionary({
                    range(0, 100): 'elf'
                }),
                'surnames': RangedDictionary({
                    range(0, 70): None,
                    range(70, 85): 'generic',
                    range(85, 90): 'human',
                    range(90, 95): 'gnome',
                    range(95, 100): 'halfling'
                })
            },
            'gnome': {
                'names': RangedDictionary({
                    range(0, 100): 'gnome'
                }),
                'surnames': RangedDictionary({
                    range(0, 100): 'gnome'
                })
            },
            'halfling': {
                'names': RangedDictionary({
                    range(0, 100): 'halfling'
                }),
                'surnames': RangedDictionary({
                    range(0, 100): 'halfling'
                })
            },
            'half-elf': {
                'names': RangedDictionary({
                    range(0, 25): 'human',
                    range(25, 50): 'generic',
                    range(50, 100): 'elf'
                }),
                'surnames': RangedDictionary({
                    range(0, 30): None,
                    range(30, 60): 'generic',
                    range(60, 90): 'human',
                    range(90, 95): 'gnome',
                    range(95, 100): 'halfling'
                })
            },
            'half-orc': {
                'names': RangedDictionary({
                    range(0, 25): 'human',
                    range(25, 50): 'generic',
                    range(50, 100): 'orc'
                }),
                'surnames': RangedDictionary({
                    range(0, 25): 'human',
                    range(25, 50): 'generic',
                    range(50, 100): 'orc'
                })
            }
        }

    @classmethod
    def get_name(cls, race=None, gender=None, number=1):
        """..."""
        if race is None:
            race = random.choice(list(cls.name_dict.keys()))
        if gender is None:
            gender = random.choice(['male', 'female'])

        name_list = []
        surname_list = []

        surnames = cls.name_dict[race]['surnames']
        names = cls.name_dict[race]['names']

        for x in range(number):
            try:
                name_key = names[random.randint(0, 99)]
                surname_key = surnames[random.randint(0, 99)]
            except KeyError:
                print("Race {}, Gender {}, Key {}".format(race, gender, x))
                raise

            if name_key == 'generic':
                name_list.append(
                    random.choice(cls.names_db[name_key]['names']))
            else:
                name_list.append(
                    random.choice(cls.names_db[name_key]['names'][gender]))
            if surname_key is None:
                surname_list.append("")
            else:
                surname_list.append(
                    random.choice(cls.names_db[surname_key]['surnames']))

        return name_list, surname_list

NameGen()

if __name__ == '__main__':
    name_list, surname_list = NameGen.get_name(
        race='human', number=1)
    for name, surname in zip(name_list, surname_list):
        print(name, surname)