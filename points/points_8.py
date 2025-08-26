from itertools import permutations
from melds import is_chow
from tiles import is_suit, rank, suit


def points_mixed_triple_chow(sets):
    chows = [s for s in sets if len(s) == 3 and is_chow(s)]
    starts_by_suit = {}
    for c in chows:
        s = suit(c[0])
        r = min(rank(x) for x in c)
        starts_by_suit.setdefault(s, set()).add(r)
    pts = 0
    suits = ['B', 'C', 'D']
    if all(s in starts_by_suit for s in suits):
        common = starts_by_suit[suits[0]] & starts_by_suit[suits[1]] & starts_by_suit[suits[2]]
        pts += 8 * len(common)
    return pts


def points_mixed_straight(sets):
    chows = [s for s in sets if len(s) == 3 and is_chow(s)]
    starts_by_suit = {'B': set(), 'C': set(), 'D': set()}
    for c in chows:
        s = suit(c[0])
        r = min(rank(x) for x in c)
        if s in starts_by_suit:
            starts_by_suit[s].add(r)
    for s1, s2, s3 in permutations(['B', 'C', 'D'], 3):
        if 1 in starts_by_suit[s1] and 4 in starts_by_suit[s2] and 7 in starts_by_suit[s3]:
            return 8
    return 0


def points_reversible_tiles(all_tiles):
    allowed = {'D1','D2','D3','D4','D5','D8','D9','B2','B4','B5','B6','B8','B9','DW'}
    for t in all_tiles:
        if t not in allowed:
            return 0
    return 8


def compute_points_8(sets, pair, all_tiles, meta):
    p8 = {
        'Mixed Triple Chow': points_mixed_triple_chow(sets),
        'Mixed Straight': points_mixed_straight(sets),
        'Reversible Tiles': points_reversible_tiles(all_tiles),
    }
    return sum(p8.values()), {k: v for k, v in p8.items() if v}


