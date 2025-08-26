from collections import Counter

# ------------------------------
# Tile utilities
# ------------------------------
SUITS = {'B', 'C', 'D'}
WINDS = {'WE', 'WS', 'WW', 'WN'}
DRAGONS = {'DR', 'DG', 'DW'}
HONORS = WINDS | DRAGONS


def is_suit(tile):
    return tile[0] in SUITS and tile[1:].isdigit()


def suit(tile):
    return tile[0] if is_suit(tile) else None


def rank(tile):
    return int(tile[1:]) if is_suit(tile) else None


def is_honor(tile):
    return tile in HONORS


def is_flower(tile):
    return tile.startswith('F') or tile.startswith('S')


def normalize_hand(tiles):
    """Split flowers from the 14 tiles, return (main14, flowers)."""
    flowers = [t for t in tiles if is_flower(t)]
    main = [t for t in tiles if not is_flower(t)]
    return main, flowers


def tiles_to_multiset(tiles):
    return tuple(sorted(tiles))


def remove_tiles(pool, tiles):
    c = Counter(pool)
    for t in tiles:
        if c[t] == 0:
            return None
        c[t] -= 1
    res = []
    for t, n in c.items():
        res += [t] * n
    return tuple(sorted(res))


