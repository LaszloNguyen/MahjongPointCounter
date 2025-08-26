from melds import is_chow, is_kong
from tiles import HONORS, WINDS, DRAGONS, is_suit, rank, suit


def points_pure_double_chow(sets):
    chows = [s for s in sets if len(s) == 3 and is_chow(s)]
    seen = set()
    pts = 0
    for i in range(len(chows)):
        for j in range(i + 1, len(chows)):
            if chows[i] == chows[j] and chows[i] not in seen:
                pts += 1
                seen.add(chows[i])
    return pts


def points_mixed_double_chow(sets):
    chows = [s for s in sets if len(s) == 3 and is_chow(s)]
    pts = 0
    for i in range(len(chows)):
        for j in range(i + 1, len(chows)):
            r1 = min(rank(x) for x in chows[i])
            r2 = min(rank(x) for x in chows[j])
            if r1 == r2 and suit(chows[i][0]) != suit(chows[j][0]):
                pts += 1
    return pts


def points_short_straight(sets):
    chows = [s for s in sets if len(s) == 3 and is_chow(s)]
    pts = 0
    used = set()
    for i in range(len(chows)):
        s1 = suit(chows[i][0])
        r1 = min(rank(x) for x in chows[i])
        for j in range(i + 1, len(chows)):
            s2 = suit(chows[j][0])
            r2 = min(rank(x) for x in chows[j])
            if s1 == s2 and {r1, r2} in ({1, 4}, {2, 5}, {3, 6}, {4, 7}):
                key = tuple(sorted([(s1, r1), (s2, r2)]))
                if key not in used:
                    pts += 1
                    used.add(key)
    return pts


def points_two_terminal_chows(sets):
    chows = [s for s in sets if len(s) == 3 and is_chow(s)]
    bysuit = {}
    for c in chows:
        s = suit(c[0])
        r = min(rank(x) for x in c)
        bysuit.setdefault(s, set()).add(r)
    pts = 0
    for s, starts in bysuit.items():
        if 1 in starts and 7 in starts:
            pts += 1
    return pts


def points_pung_term_or_honor(sets, seat_wind=None, prevalent_wind=None):
    pts = 0
    for s in sets:
        if len(s) in (3, 4) and len(set(s)) == 1:
            t = s[0]
            if is_suit(t) and rank(t) in (1, 9):
                pts += 1
            elif t in WINDS:
                if t != f"W{seat_wind}" and t != f"W{prevalent_wind}":
                    pts += 1
    return pts


def points_melded_kong(sets):
    return sum(1 for s in sets if is_kong(s))


def points_one_voided_suit(all_tiles):
    suits_present = {suit(t) for t in all_tiles if is_suit(t)}
    return 1 if len(suits_present) <= 2 else 0


def points_no_honor(all_tiles):
    return 1 if all(t not in HONORS for t in all_tiles) else 0


def points_self_drawn(win_by):
    return 1 if win_by == 'self' else 0


def points_wait_types(wait_type):
    return 1 if wait_type in {'edge', 'closed', 'pair'} else 0


def compute_points_1(sets, pair, all_tiles, meta):
    seat_wind = meta.get('seat_wind')
    prevalent_wind = meta.get('prevalent_wind')
    win_by = meta.get('win_by')
    wait_type = meta.get('wait_type')
    p1 = {
        'Pure Double Chow': points_pure_double_chow(sets),
        'Mixed Double Chow': points_mixed_double_chow(sets),
        'Short Straight': points_short_straight(sets),
        'Two Terminal Chows': points_two_terminal_chows(sets),
        'Pung of Terminals/Honors (non-seat/prevalent)': points_pung_term_or_honor(sets, seat_wind, prevalent_wind),
        'Melded Kong': points_melded_kong(sets),
        'One Voided Suit': points_one_voided_suit(all_tiles),
        'No Honor Tiles': points_no_honor(all_tiles),
        'Self Drawn': points_self_drawn(win_by),
        'Wait Type (edge/closed/pair)': points_wait_types(wait_type),
    }
    return sum(p1.values()), {k: v for k, v in p1.items() if v}


