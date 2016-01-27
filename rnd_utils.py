import random


class RangedDictionary(dict):
    def __getitem__(self, key):
        for rng in self.keys():
            if key == rng:
                return super().__getitem__(key)
            if key in rng:
                return super().__getitem__(rng)
        return super().__getitem__(key)


def rnd_dic_rng(dic):
    min_v = min([key.start for key in dic.keys()])
    max_v = max([key.stop for key in dic.keys()])
    rnd = random.randint(min_v, max_v - 1)
    result = dic.__getitem__(rnd)
    # print(rnd, result)
    return result


class RandomDictionary:

    @classmethod
    def random(cls):
        return rnd_dic_rng(cls.dic)


class RoomItems(RandomDictionary):
    """
    Use RoomItems.random() to get a random item quantity roll.
    """
    dic = RangedDictionary({
        range(0, 70): 0,  # min <= x < max: 0 items
        range(70, 90): 1,  # min <= x < max: 1 item
        range(90, 100): 2  # min <= x < max: 2 items
    })


def set_rnd_dic(_class):
    dic = RangedDictionary()

    max_v = 0
    for name, template in _class.templates.items():
        rng = (100 - template['_rarity'])
        dic[range(max_v, max_v + rng)] = name
        max_v += rng

    return dic


class ItemTypes(RandomDictionary):
    """
    Use RoomItems.random() to get a random item quantity roll.
    """
    from sprite import Item
    dic = set_rnd_dic(Item)


class MonsterTypes(RandomDictionary):
    """
    Use RoomItems.random() to get a random item quantity roll.
    """
    from sprite import NPC
    dic = set_rnd_dic(NPC)


if __name__ == '__main__':
    print(MonsterTypes.dic)
    print(MonsterTypes.random())

    print()

    print(ItemTypes.dic)
    print(ItemTypes.random())