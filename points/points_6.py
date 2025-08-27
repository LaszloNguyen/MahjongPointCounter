from itertools import permutations
from tiles import HONORS, is_suit, rank, suit


def points_all_pungs(sets):
    if all((len(s) in (3, 4)) and (len(set(s)) == 1) for s in sets):
        return 6
    return 0


def points_half_flush(all_tiles):
    suits_present = {suit(t) for t in all_tiles if is_suit(t)}
    has_honor = any(t in HONORS for t in all_tiles)
    if len(suits_present) == 1 and has_honor:
        return 6
    return 0


def points_mixed_shifted_chows(sets, is_chow_fn, suit_fn, rank_fn):
    chows = [s for s in sets if len(s) == 3 and is_chow_fn(s)]
    starts_by_suit = {'B': set(), 'C': set(), 'D': set()}
    for c in chows:
        s = suit_fn(c[0])
        r = min(rank_fn(x) for x in c)
        if s in starts_by_suit:
            starts_by_suit[s].add(r)
    pts = 0
    for r in range(1, 8):
        found = False
        for perm in permutations(['B', 'C', 'D'], 3):
            if (r in starts_by_suit[perm[0]] and
                (r + 1) in starts_by_suit[perm[1]] and
                (r + 2) in starts_by_suit[perm[2]]):
                found = True
                break
        if found:
            pts += 6
    return pts


def points_all_types(all_tiles, is_suit_fn, suit_fn, honors_set):
    suits_present = {suit_fn(t) for t in all_tiles if is_suit_fn(t)}
    has_honor = any(t in honors_set for t in all_tiles)
    if suits_present == {'B', 'C', 'D'} and has_honor:
        return 6
    return 0


def points_two_dragon_pungs(sets):
    dragons = set()
    for s in sets:
        if len(s) in (3, 4) and len(set(s)) == 1 and s[0] in {'DR', 'DG', 'DW'}:
            dragons.add(s[0])
    return 6 if len(dragons) >= 2 else 0


def points_melded_hand(sets, melds_open, win_by):
    # 6 points: Four melded groups and is won by discard
    if melds_open and win_by == 'discard' and len(sets) == 4:
        return 6
    return 0


def compute_points_6(sets, pair, all_tiles, meta, is_chow_fn, suit_fn, rank_fn, honors_set):
    p6 = {
        'All Pungs': points_all_pungs(sets),
        'Half Flush': points_half_flush(all_tiles),
        'Mixed Shifted Chows': points_mixed_shifted_chows(sets, is_chow_fn, suit_fn, rank_fn),
        'Two Dragon Pungs': points_two_dragon_pungs(sets),
        'All Types': points_all_types(all_tiles, lambda t: t[0] in {'B','C','D'} and t[1:].isdigit(), suit_fn, honors_set),
        'Melded Hand': points_melded_hand(sets, meta.get('melds_open', False), meta.get('win_by')),
    }
    return sum(p6.values()), {k: v for k, v in p6.items() if v}


