from collections import Counter
from functools import lru_cache

from melds import is_chow
from tiles import is_suit, suit, rank, tiles_to_multiset, remove_tiles


@lru_cache(maxsize=None)
def enumerate_partitions(pool):
    """Yield partitions as tuples: (sets_list, pair) where sets_list has 4 melds (pung/chow/kong), pair is 2 identical tiles.
       Kongs are recorded as sets too (len 4)."""
    tiles = list(pool)
    if len(tiles) == 0:
        return []
    out = []
    cnt = Counter(tiles)
    # choose pair
    pairs = [t for t, n in cnt.items() if n >= 2]
    for p in pairs:
        rem = remove_tiles(pool, (p, p))
        if rem is None:
            continue
        for sets_list in enumerate_sets(rem, need_sets=4):
            out.append((sets_list, (p, p)))
    return out


@lru_cache(maxsize=None)
def enumerate_sets(pool, need_sets):
    if need_sets == 0:
        return [tuple()] if len(pool) == 0 else []
    tiles = list(pool)
    out = []
    # try pung
    cnt = Counter(tiles)
    for t, n in list(cnt.items()):
        if n >= 3:
            rem = remove_tiles(pool, (t, t, t))
            for rest in enumerate_sets(rem, need_sets - 1):
                out.append(((t, t, t),) + rest)
        # try kong
        if n >= 4:
            rem = remove_tiles(pool, (t, t, t, t))
            for rest in enumerate_sets(rem, need_sets - 1):
                out.append(((t, t, t, t),) + rest)
    # try chow (only suit tiles)
    suit_tiles = [t for t in set(tiles) if is_suit(t)]
    for t in suit_tiles:
        s = suit(t)
        r = rank(t)
        if r <= 7:
            a = (f"{s}{r}", f"{s}{r+1}", f"{s}{r+2}")
            if all(Counter(tiles)[x] > 0 for x in a):
                rem = remove_tiles(pool, a)
                if rem is not None:
                    for rest in enumerate_sets(rem, need_sets - 1):
                        out.append((tuple(sorted(a)),) + rest)
    return out


