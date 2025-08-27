from melds import is_kong
from tiles import DRAGONS, WINDS, HONORS, is_suit, rank


def points_dragon_pung(sets):
    return sum(2 for s in sets if len(s) in (3, 4) and len(set(s)) == 1 and s[0] in DRAGONS)


def points_seat_wind_pung(sets, seat_wind):
    if not seat_wind:
        return 0
    return sum(2 for s in sets if len(s) in (3, 4) and len(set(s)) == 1 and s[0] == f"W{seat_wind}")


def points_prevalent_wind_pung(sets, prevalent_wind):
    if not prevalent_wind:
        return 0
    return sum(2 for s in sets if len(s) in (3, 4) and len(set(s)) == 1 and s[0] == f"W{prevalent_wind}")


def points_concealed_hand(melds_open, win_by):
    return 2 if (not melds_open and win_by == 'discard') else 0


def points_all_chows(sets, is_chow_fn):
    return 2 if all(len(s) == 3 and is_chow_fn(s) for s in sets) else 0


def points_tile_hog(sets, all_tiles):
    # 2pt: holds all 4 copies of any tile without using them as a Kong
    from collections import Counter
    cnt = Counter(all_tiles)
    hogs = {t for t, n in cnt.items() if n == 4}
    if not hogs:
        return 0
    for s in sets:
        if is_kong(s) and s[0] in hogs:
            hogs.discard(s[0])
    return 2 if hogs else 0


def points_double_pung(sets):
    # 2pt: exactly one award if there exists a rank with pungs/kongs in ≥2 suits
    by_rank_to_suits = {}
    for s in sets:
        if len(s) in (3, 4) and len(set(s)) == 1 and is_suit(s[0]):
            r = rank(s[0])
            suit_char = s[0][0]
            by_rank_to_suits.setdefault(r, set()).add(suit_char)
    for suits in by_rank_to_suits.values():
        if len(suits) >= 2:
            return 2
    return 0


def points_two_concealed_pungs(sets, concealed_mask):
    """2pt if there are at least two concealed pungs or kongs.
    concealed_mask: Optional[List[bool]] aligned with sets (True means concealed).
    """
    if not isinstance(concealed_mask, (list, tuple)) or len(concealed_mask) != len(sets):
        return 0
    cnt = 0
    for idx, s in enumerate(sets):
        if concealed_mask[idx] and len(s) in (3, 4) and len(set(s)) == 1:
            cnt += 1
    return 2 if cnt >= 2 else 0


def points_concealed_kong(sets, concealed_mask):
    """2pt per concealed kong.
    concealed_mask: Optional[List[bool]] aligned with sets (True means concealed).
    """
    if not isinstance(concealed_mask, (list, tuple)) or len(concealed_mask) != len(sets):
        return 0
    return 2 * sum(1 for idx, s in enumerate(sets) if concealed_mask[idx] and len(s) == 4 and len(set(s)) == 1)


def points_all_simples(all_tiles):
    for t in all_tiles:
        if not is_suit(t):
            return 0
        r = rank(t)
        if r in (1, 9):
            return 0
    return 2


def compute_points_2(sets, pair, all_tiles, meta, is_chow_fn):
    seat_wind = meta.get('seat_wind')
    prevalent_wind = meta.get('prevalent_wind')
    win_by = meta.get('win_by')
    concealed_mask = meta.get('concealed_melds')  # Optional[List[bool]] same length as sets
    p2 = {
        'Dragon Pung/Kong': points_dragon_pung(sets),
        'Seat Wind Pung/Kong': points_seat_wind_pung(sets, seat_wind),
        'Prevalent Wind Pung/Kong': points_prevalent_wind_pung(sets, prevalent_wind),
        'Concealed Hand (won by discard)': points_concealed_hand(meta.get('melds_open', False), win_by),
        'All Chows': points_all_chows(sets, is_chow_fn),
        'Tile Hog': points_tile_hog(sets, all_tiles),
        'Double Pung': points_double_pung(sets),
        'Two Concealed Pungs': points_two_concealed_pungs(sets, concealed_mask),
        'Concealed Kong': points_concealed_kong(sets, concealed_mask),
        'All Simples': points_all_simples(all_tiles),
    }
    return sum(p2.values()), {k: v for k, v in p2.items() if v}





