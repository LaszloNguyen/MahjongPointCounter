from tiles import HONORS, is_suit, rank


def _set_is_outside(s, is_chow_fn):
    if len(s) in (3, 4) and len(set(s)) == 1:
        t = s[0]
        if t in HONORS:
            return True
        return is_suit(t) and rank(t) in (1, 9)
    if len(s) == 3 and is_chow_fn(s):
        rs = sorted(rank(x) for x in s)
        return rs[0] == 1 or rs[-1] == 9
    return False


def points_outside_hand(sets, pair, is_chow_fn):
    if not all(_set_is_outside(s, is_chow_fn) for s in sets):
        return 0
    p = pair[0]
    if p in HONORS:
        return 4
    if is_suit(p) and rank(p) in (1, 9):
        return 4
    return 0


def points_fully_concealed_hand(melds_open, win_by):
    return 4 if (not melds_open and win_by == 'self') else 0


def points_two_melded_kongs(sets, is_kong_fn):
    return 4 if sum(1 for s in sets if is_kong_fn(s)) == 2 else 0



def compute_points_4(sets, pair, all_tiles, meta, is_chow_fn, is_kong_fn):
    p4 = {
        'Outside Hand': points_outside_hand(sets, pair, is_chow_fn),
        'Two Melded Kongs': points_two_melded_kongs(sets, is_kong_fn),
        'Fully Concealed Hand (self-draw)': points_fully_concealed_hand(meta.get('melds_open', False), meta.get('win_by')),
    }
    return sum(p4.values()), {k: v for k, v in p4.items() if v}


