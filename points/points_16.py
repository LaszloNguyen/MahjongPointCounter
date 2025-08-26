from melds import is_chow, is_kong
from tiles import suit, rank


def points_pure_straight(sets):
    chows = [s for s in sets if len(s) == 3 and is_chow(s)]
    bysuit = {}
    for c in chows:
        s = suit(c[0])
        r = min(rank(x) for x in c)
        bysuit.setdefault(s, set()).add(r)
    pts = 0
    for s, starts in bysuit.items():
        if {1, 4, 7}.issubset(starts):
            pts += 16
    return pts


def points_three_kongs(sets):
    k = sum(1 for s in sets if is_kong(s))
    return 16 if k == 3 else 0


def compute_points_16(sets, pair, all_tiles, meta):
    p16 = {
        'Pure Straight': points_pure_straight(sets),
        'Three Kongs': points_three_kongs(sets),
    }
    return sum(p16.values()), {k: v for k, v in p16.items() if v}


