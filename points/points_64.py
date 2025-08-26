from melds import is_chow, is_kong
from tiles import HONORS, WINDS, is_suit, rank, suit


def points_big_three_winds(sets):
    winds = set()
    for s in sets:
        if len(s) in (3, 4) and len(set(s)) == 1 and s[0] in WINDS:
            winds.add(s[0])
    return 64 if len(winds) == 3 else 0


def points_all_terminals_and_honors(all_tiles):
    for t in all_tiles:
        if t in HONORS:
            continue
        if not is_suit(t) or rank(t) not in (1, 9):
            return 0
    return 64


def points_pure_terminal_chows(sets, is_chow_fn, suit_fn, rank_fn):
    chows = [s for s in sets if len(s) == 3 and is_chow_fn(s)]
    if len(chows) != 4:
        return 0
    bysuit = {}
    for c in chows:
        s = suit_fn(c[0])
        r = min(rank_fn(x) for x in c)
        bysuit.setdefault(s, []).append(r)
    for s, starts in bysuit.items():
        if starts.count(1) == 2 and starts.count(7) == 2:
            return 64
    return 0


def compute_points_64(sets, pair, all_tiles, meta, is_chow_fn, suit_fn, rank_fn):
    p64 = {
        'Big Three Winds': points_big_three_winds(sets),
        'All Terminals and Honors': points_all_terminals_and_honors(all_tiles),
        'Pure Terminal Chows': points_pure_terminal_chows(sets, is_chow_fn, suit_fn, rank_fn),
    }
    return sum(p64.values()), {k: v for k, v in p64.items() if v}


