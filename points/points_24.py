from tiles import HONORS, is_suit, suit


def points_full_flush(all_tiles):
    suits_present = {suit(t) for t in all_tiles if is_suit(t)}
    has_honor = any(t in HONORS for t in all_tiles)
    if len(suits_present) == 1 and not has_honor:
        return 24
    return 0


def compute_points_24(sets, pair, all_tiles, meta):
    p24 = {
        'Full Flush': points_full_flush(all_tiles),
    }
    return sum(p24.values()), {k: v for k, v in p24.items() if v}


