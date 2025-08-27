from collections import Counter

from melds import is_chow, is_kong
from tiles import DRAGONS, HONORS, WINDS, is_suit, rank, suit, normalize_hand, tiles_to_multiset
from partition import enumerate_partitions
from points.points_1 import compute_points_1
from points.points_2 import compute_points_2
from points.points_4 import compute_points_4
from points.points_6 import compute_points_6
from points.points_8 import compute_points_8
from points.points_12 import compute_points_12
from points.points_16 import compute_points_16
from points.points_24 import compute_points_24
from points.points_64 import compute_points_64
from points.points_88 import compute_points_88
from combine_rules import process_exclusions


def count_flowers(flowers):
    return len(flowers)  # 1 point each (doesn't count toward 8)


def points_pure_double_chow(sets):
    # 1pt: two identical chows in same suit
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
    # 1pt: same numbers different suits
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
    # 1pt: two chows forming 1-6 straight in same suit
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
    # 1pt: have 123 and 789 in same suit
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
    # 1pt per Pung/Kong of terminals (1/9) or honor (non seat/prevalent wind)
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
    # 1pt per melded kong; we assume all kongs given in sets are melded unless flagged otherwise.
    return sum(1 for s in sets if is_kong(s))


def points_one_voided_suit(all_tiles):
    # 1pt: hand has no tiles from one suit (i.e., uses exactly 2 suits at most)
    suits_present = {suit(t) for t in all_tiles if is_suit(t)}
    return 1 if len(suits_present) <= 2 else 0


def points_no_honor(all_tiles):
    # 1pt: no honors
    return 1 if all(t not in HONORS for t in all_tiles) else 0


def points_self_drawn(win_by):
    # 1pt: self drawn
    return 1 if win_by == 'self' else 0


def points_wait_types(wait_type):
    # 1pt: edge, closed, or pair wait (only if single wait)
    return 1 if wait_type in {'edge', 'closed', 'pair'} else 0


def points_dragon_pung(sets):
    # 2pt per dragon pung/kong
    return sum(2 for s in sets if len(s) in (3, 4) and len(set(s)) == 1 and s[0] in DRAGONS)


def points_wind_pungs(sets, seat_wind, prevalent_wind):
    # 2pt for seat wind pung/kong; 2pt for prevalent wind pung/kong
    pts = 0
    for s in sets:
        if len(s) in (3, 4) and len(set(s)) == 1 and s[0] in WINDS:
            if s[0] == f"W{seat_wind}":
                pts += 2
            if s[0] == f"W{prevalent_wind}":
                pts += 2
    return pts


def points_concealed_hand(melds_open, win_by):
    # 2pt if no melded sets and win by discard (classic MCR)
    return 2 if (not melds_open and win_by == 'discard') else 0


# ------------------------------
# Additional rules (2, 6, 8, 16, 24, 88 point tiers)
# Reference: Chinese Official Mahjong Scoring Rules (MCR) — see https://playmahjong.io/chinese-official-rules
# ------------------------------

def points_all_chows(sets):
    # 2pt: all 4 melds are chows
    return 2 if all(len(s) == 3 and is_chow(s) for s in sets) else 0


def points_all_simples(all_tiles):
    # 2pt: no terminals (1/9) and no honors
    for t in all_tiles:
        if not is_suit(t):
            return 0
        r = rank(t)
        if r in (1, 9):
            return 0
    return 2


def points_all_pungs(sets):
    # 6pt: all melds are pungs/kongs
    if all((len(s) in (3, 4)) and (len(set(s)) == 1) for s in sets):
        return 6
    return 0


def points_mixed_shifted_chows(sets):
    # 6pt: three chows in different suits with starting ranks r, r+1, r+2
    chows = [s for s in sets if len(s) == 3 and is_chow(s)]
    starts_by_suit = {'B': set(), 'C': set(), 'D': set()}
    for c in chows:
        s = suit(c[0])
        r = min(rank(x) for x in c)
        if s in starts_by_suit:
            starts_by_suit[s].add(r)
    pts = 0
    # try all r and suit permutations
    suits = ['B', 'C', 'D']
    for r in range(1, 8):  # start ranks 1..7 valid for chows
        # check if there exists a bijection of suits to r,r+1,r+2
        from itertools import permutations
        found = False
        for perm in permutations(suits, 3):
            if (r in starts_by_suit[perm[0]] and
                (r + 1) in starts_by_suit[perm[1]] and
                (r + 2) in starts_by_suit[perm[2]]):
                found = True
                break
        if found:
            pts += 6
    return pts


def points_two_dragon_pungs(sets):
    # 6pt: two distinct dragon pungs/kongs
    dragons = set()
    for s in sets:
        if len(s) in (3, 4) and len(set(s)) == 1 and s[0] in DRAGONS:
            dragons.add(s[0])
    return 6 if len(dragons) >= 2 else 0


def points_all_types(all_tiles):
    # 6pt: has B, C, D suits and at least one honor
    suits_present = {suit(t) for t in all_tiles if is_suit(t)}
    has_honor = any(t in HONORS for t in all_tiles)
    if suits_present == {'B', 'C', 'D'} and has_honor:
        return 6
    return 0


def points_mixed_triple_chow(sets):
    # 8pt: same-number chows in all three suits
    chows = [s for s in sets if len(s) == 3 and is_chow(s)]
    starts_by_suit = {}
    for c in chows:
        s = suit(c[0])
        r = min(rank(x) for x in c)
        starts_by_suit.setdefault(s, set()).add(r)
    suits = ['B', 'C', 'D']
    pts = 0
    if all(s in starts_by_suit for s in suits):
        common = starts_by_suit[suits[0]] & starts_by_suit[suits[1]] & starts_by_suit[suits[2]]
        pts += 8 * len(common)
    return pts


def points_pure_straight(sets):
    # 16pt: have 123, 456, 789 in the same suit
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


def points_mixed_straight(sets):
    # 8pt: 123, 456, 789 each in a different suit (uses all three suits)
    chows = [s for s in sets if len(s) == 3 and is_chow(s)]
    starts_by_suit = {'B': set(), 'C': set(), 'D': set()}
    for c in chows:
        s = suit(c[0])
        r = min(rank(x) for x in c)
        if s in starts_by_suit:
            starts_by_suit[s].add(r)
    from itertools import permutations
    for s1, s2, s3 in permutations(['B', 'C', 'D'], 3):
        if 1 in starts_by_suit[s1] and 4 in starts_by_suit[s2] and 7 in starts_by_suit[s3]:
            return 8
    return 0


def points_half_flush(all_tiles):
    # 6pt: one suit plus honors
    suits_present = {suit(t) for t in all_tiles if is_suit(t)}
    has_honor = any(t in HONORS for t in all_tiles)
    if len(suits_present) == 1 and has_honor:
        return 6
    return 0


def points_full_flush(all_tiles):
    # 24pt: one suit only, no honors
    suits_present = {suit(t) for t in all_tiles if is_suit(t)}
    has_honor = any(t in HONORS for t in all_tiles)
    if len(suits_present) == 1 and not has_honor:
        return 24
    return 0


def points_big_three_dragons(sets):
    # 88pt: pungs/kongs of all 3 dragons
    dragons = set()
    for s in sets:
        if len(s) in (3, 4) and len(set(s)) == 1 and s[0] in DRAGONS:
            dragons.add(s[0])
    return 88 if len(dragons) == 3 else 0


def points_big_four_winds(sets):
    # 88pt: pungs/kongs of all 4 winds
    winds = set()
    for s in sets:
        if len(s) in (3, 4) and len(set(s)) == 1 and s[0] in WINDS:
            winds.add(s[0])
    return 88 if len(winds) == 4 else 0


def points_three_kongs(sets):
    # 16pt: exactly 3 kongs
    k = sum(1 for s in sets if is_kong(s))
    return 16 if k == 3 else 0


def points_four_kongs(sets):
    # 88pt: exactly 4 kongs
    k = sum(1 for s in sets if is_kong(s))
    return 88 if k == 4 else 0


def points_big_three_winds(sets):
    # 64pt: pungs/kongs of 3 different winds
    winds = set()
    for s in sets:
        if len(s) in (3, 4) and len(set(s)) == 1 and s[0] in WINDS:
            winds.add(s[0])
    return 64 if len(winds) == 3 else 0


def points_all_terminals_and_honors(all_tiles):
    # 64pt: tiles are all terminals or honors
    for t in all_tiles:
        if t in HONORS:
            continue
        if not is_suit(t) or rank(t) not in (1, 9):
            return 0
    return 64


def points_pure_terminal_chows(sets):
    # 64pt: two 123 chows, two 789 chows and a pair of 5s in one suit
    chows = [s for s in sets if len(s) == 3 and is_chow(s)]
    if len(chows) != 4:
        return 0
    bysuit = {}
    for c in chows:
        s = suit(c[0])
        r = min(rank(x) for x in c)
        bysuit.setdefault(s, []).append(r)
    for s, starts in bysuit.items():
        if starts.count(1) == 2 and starts.count(7) == 2:
            return 64
    return 0


def points_all_green(all_tiles):
    # 88pt: only 2,3,4,6,8 of Bamboo and Green Dragon
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
    # 88pt: concealed, one suit, tiles 1112345678999 + any same-suit tile
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
    # Need at least the multiset: 1x3, 2..8 at least 1, 9x3
    from collections import Counter as _C
    c = _C(ranks)
    need = {1: 3, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 3}
    for r, n in need.items():
        if c[r] < n:
            return 0
    # and total is 14
    if len(ranks) != 14:
        return 0
    return 88


def points_thirteen_orphans(all_tiles, melds_open):
    # 88pt: terminals and honors 13 unique + one duplicate; concealed
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


def points_seven_shifted_pairs(all_tiles, melds_open):
    # 88pt: seven pairs in one suit, ranks r..r+6
    if melds_open:
        return 0
    from collections import Counter as _C
    c = _C(all_tiles)
    pairs = [t for t, n in c.items() if n == 2 and is_suit(t)]
    if len(pairs) != 7:
        return 0
    suits = {suit(t) for t in pairs}
    if len(suits) != 1:
        return 0
    ranks = sorted(rank(t) for t in pairs)
    base = ranks[0]
    if ranks == list(range(base, base + 7)):
        return 88
    return 0


# ------------------------------
# 8-point rules
# ------------------------------
def points_reversible_tiles(all_tiles):
    # 8pt: only reversible tiles
    allowed = {
        # Circles/Dots (assumed suit 'D')
        'D1','D2','D3','D4','D5','D8','D9',
        # Bamboo (suit 'B')
        'B2','B4','B5','B6','B8','B9',
        # White Dragon
        'DW',
    }
    for t in all_tiles:
        if t not in allowed:
            return 0
    return 8

# ------------------------------
# 4-point rules
# ------------------------------
def _set_is_outside(s):
    # returns True if set contains a terminal or honor
    if len(s) in (3, 4) and len(set(s)) == 1:
        t = s[0]
        if t in HONORS:
            return True
        return is_suit(t) and rank(t) in (1, 9)
    # chow case
    if len(s) == 3 and is_chow(s):
        rs = sorted(rank(x) for x in s)
        return rs[0] == 1 or rs[-1] == 9
    return False


def points_outside_hand(sets, pair):
    # 4pt: every meld and the pair are terminals/honors-inclusive
    if not all(_set_is_outside(s) for s in sets):
        return 0
    p = pair[0]
    if p in HONORS:
        return 4
    if is_suit(p) and rank(p) in (1, 9):
        return 4
    return 0


def points_two_melded_kongs(sets):
    # 4pt: exactly two kongs (treated as melded in this model)
    return 4 if sum(1 for s in sets if is_kong(s)) == 2 else 0


def points_fully_concealed_hand(melds_open, win_by):
    # 4pt: fully concealed hand winning by self-draw
    return 4 if (not melds_open and win_by == 'self') else 0


def score_partition(sets, pair, all_tiles, meta):
    """Apply implemented rules and return (base_points_without_flowers, flower_points, breakdown dict)."""
    seat_wind = meta.get('seat_wind')  # 'E','S','W','N'
    prevalent_wind = meta.get('prevalent_wind')  # 'E','S','W','N'
    win_by = meta.get('win_by')  # 'self' or 'discard'
    melds_open = meta.get('melds_open', False)
    wait_type = meta.get('wait_type')  # None|'edge'|'closed'|'pair'
    flowers = meta.get('flowers', [])

    # 1-point rules (module)
    p1_total, p1 = compute_points_1(sets, pair, all_tiles, meta)

    # 2-point rules (module)
    p2_total, p2 = compute_points_2(sets, pair, all_tiles, meta, is_chow)
    
    # 4-point rules (module)
    p4_total, p4 = compute_points_4(sets, pair, all_tiles, meta, is_chow, is_kong)
    
    # 6-point rules (module)
    p6_total, p6 = compute_points_6(sets, pair, all_tiles, meta, is_chow, suit, rank, HONORS)

    # 8-point rules (module)
    p8_total, p8 = compute_points_8(sets, pair, all_tiles, meta)

    # 12-point rules (module)
    p12_total, p12 = compute_points_12(sets, pair, all_tiles, meta)

    # Exclusions: Mixed Triple Chow does not combine with Mixed Double Chow
    if p8.get('Mixed Triple Chow', 0) and p1.get('Mixed Double Chow', 0):
        p4_adj = 0  # no 4-pt impact here, but keep variable for pattern
        p1_total -= p1['Mixed Double Chow']
        del p1['Mixed Double Chow']

    # Reversible Tiles excludes One Voided Suit
    if p8.get('Reversible Tiles', 0) and p1.get('One Voided Suit', 0):
        p1_total -= p1['One Voided Suit']
        del p1['One Voided Suit']

    # 16-point rules (module)
    p16_total, p16 = compute_points_16(sets, pair, all_tiles, meta)

    # 24-point rules (module)
    p24_total, p24 = compute_points_24(sets, pair, all_tiles, meta)

    # 64-point rules (module)
    p64_total, p64 = compute_points_64(sets, pair, all_tiles, meta, is_chow, suit, rank)

    # 88-point rules (module)
    p88_total, p88 = compute_points_88(sets, pair, all_tiles, meta, is_suit, suit, rank)

    flowers_pts = count_flowers(flowers)

    breakdown = {**{k: v for k, v in p1.items() if v},
                 **{k: v for k, v in p2.items() if v},
                 **{k: v for k, v in p4.items() if v},
                 **{k: v for k, v in p6.items() if v},
                 **{k: v for k, v in p8.items() if v},
                 **{k: v for k, v in p12.items() if v},
                 **{k: v for k, v in p16.items() if v},
                 **{k: v for k, v in p24.items() if v},
                 **{k: v for k, v in p64.items() if v},
                 **{k: v for k, v in p88.items() if v}}

    # Apply global exclusions across tiers
    breakdown = process_exclusions(breakdown)

    total = p1_total + p2_total + p4_total + p6_total + p8_total + p12_total + p16_total + p24_total + p64_total + p88_total
    return total, flowers_pts, breakdown


def best_score(hand14, meta):
    main, flowers = normalize_hand(hand14)
    meta = dict(meta)
    meta['flowers'] = flowers
    if len(main) != 14:
        raise ValueError("Need 14 non-flower tiles (flowers are allowed separately).")
    
    # Check for special "Lesser Honors and Knitted Tiles" rule first
    from points.points_12 import points_lesser_honors_and_knitted_tiles
    lesser_honors_points = points_lesser_honors_and_knitted_tiles(main)
    if lesser_honors_points > 0:
        # This is a valid hand under the Lesser Honors and Knitted Tiles rule
        flowers_pts = count_flowers(flowers)
        breakdown = {'Lesser Honors and Knitted Tiles': lesser_honors_points}
        valid_min8 = lesser_honors_points >= 8
        return {
            'valid': True,
            'meets_min_8': valid_min8,
            'base_points': lesser_honors_points,
            'flower_points': flowers_pts,
            'total_points_display': lesser_honors_points,
            'breakdown': breakdown,
            'sets': (),  # No standard sets for this special hand
            'pair': (),  # No standard pair for this special hand
            'flowers': flowers
        }
    
    # Standard mahjong hand processing
    parts = enumerate_partitions(tiles_to_multiset(tuple(sorted(main))))
    best = None
    for sets, pair in parts:
        pts, fpts, br = score_partition(sets, pair, main, meta)
        if best is None or pts > best[0]:
            best = (pts, fpts, br, sets, pair)
    if best is None:
        return {'valid': False, 'reason': 'No valid 4-sets+pair partition found.'}
    base_pts, flowers_pts, breakdown, sets, pair = best
    valid_min8 = base_pts >= 8  # flowers don't count toward min-8
    return {
        'valid': True,
        'meets_min_8': valid_min8,
        'base_points': base_pts,
        'flower_points': flowers_pts,
        'total_points_display': base_pts,  # display total (ex-flowers) per MCR min-8
        'breakdown': breakdown,
        'sets': sets,
        'pair': pair,
        'flowers': flowers
    }


