from melds import is_kong
from tiles import DRAGONS, WINDS, HONORS, is_suit, rank, suit


def points_big_three_dragons(sets):
    dragons = set()
    for s in sets:
        if len(s) in (3, 4) and len(set(s)) == 1 and s[0] in DRAGONS:
            dragons.add(s[0])
    return 88 if len(dragons) == 3 else 0


def points_big_four_winds(sets):
    winds = set()
    for s in sets:
        if len(s) in (3, 4) and len(set(s)) == 1 and s[0] in WINDS:
            winds.add(s[0])
    return 88 if len(winds) == 4 else 0


def points_four_kongs(sets):
    k = sum(1 for s in sets if is_kong(s))
    return 88 if k == 4 else 0


def points_all_green(all_tiles):
    green_suits = {'B2', 'B3', 'B4', 'B6', 'B8'}
    for t in all_tiles:
        if t == 'DG':
            continue
        if t in green_suits:
            continue
        if is_suit(t) and suit(t) == 'B' and rank(t) in (2, 3, 4, 6, 8):
            continue
        return 0
    return 88


def points_nine_gates(all_tiles, melds_open):
    if melds_open:
        return 0
    suit_counts = {}
    for t in all_tiles:
        if not is_suit(t):
            return 0
        suit_counts.setdefault(suit(t), []).append(rank(t))
    if len(suit_counts) != 1:
        return 0
    ranks = sorted(next(iter(suit_counts.values())))
    from collections import Counter as _C
    c = _C(ranks)
    need = {1: 3, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 3}
    for r, n in need.items():
        if c[r] < n:
            return 0
    if len(ranks) != 14:
        return 0
    return 88


def points_thirteen_orphans(all_tiles, melds_open):
    if melds_open:
        return 0
    terminals = {f"B{r}" for r in (1, 9)} | {f"C{r}" for r in (1, 9)} | {f"D{r}" for r in (1, 9)}
    key_tiles = terminals | HONORS
    if len(all_tiles) != 14:
        return 0
    if any(t not in key_tiles for t in all_tiles):
        return 0
    from collections import Counter as _C
    c = _C(all_tiles)
    if sum(1 for t in key_tiles if c[t] >= 1) != 13:
        return 0
    if sum(1 for t in key_tiles if c[t] == 2) != 1:
        return 0
    return 88


def points_seven_shifted_pairs(all_tiles, melds_open, is_suit_fn, suit_fn, rank_fn):
    if melds_open:
        return 0
    from collections import Counter as _C
    c = _C(all_tiles)
    pairs = [t for t, n in c.items() if n == 2 and is_suit_fn(t)]
    if len(pairs) != 7:
        return 0
    suits = {suit_fn(t) for t in pairs}
    if len(suits) != 1:
        return 0
    ranks = sorted(rank_fn(t) for t in pairs)
    base = ranks[0]
    if ranks == list(range(base, base + 7)):
        return 88
    return 0


def compute_points_88(sets, pair, all_tiles, meta, is_suit_fn, suit_fn, rank_fn):
    p88 = {
        'Big Four Winds': points_big_four_winds(sets),
        'Big Three Dragons': points_big_three_dragons(sets),
        'Four Kongs': points_four_kongs(sets),
        'All Green': points_all_green(all_tiles),
        'Nine Gates': points_nine_gates(all_tiles, meta.get('melds_open', False)),
        'Thirteen Orphans': points_thirteen_orphans(all_tiles, meta.get('melds_open', False)),
        'Seven Shifted Pairs': points_seven_shifted_pairs(all_tiles, meta.get('melds_open', False), is_suit_fn, suit_fn, rank_fn),
    }
    return sum(p88.values()), {k: v for k, v in p88.items() if v}


