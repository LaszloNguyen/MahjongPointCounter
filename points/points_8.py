from itertools import permutations
from melds import is_chow, is_kong
from tiles import is_suit, rank, suit


def points_mixed_straight(sets):
    chows = [s for s in sets if len(s) == 3 and is_chow(s)]
    starts_by_suit = {'B': set(), 'C': set(), 'D': set()}
    for c in chows:
        s = suit(c[0])
        r = min(rank(x) for x in c)
        if s in starts_by_suit:
            starts_by_suit[s].add(r)
    for s1, s2, s3 in permutations(['B', 'C', 'D'], 3):
        if 1 in starts_by_suit[s1] and 4 in starts_by_suit[s2] and 7 in starts_by_suit[s3]:
            return 8
    return 0


def points_reversible_tiles(all_tiles):
    allowed = {'D1','D2','D3','D4','D5','D8','D9','B2','B4','B5','B6','B8','B9','DW'}
    for t in all_tiles:
        if t not in allowed:
            return 0
    return 8


def points_mixed_triple_chow(sets):
    chows = [s for s in sets if len(s) == 3 and is_chow(s)]
    starts_by_suit = {}
    for c in chows:
        s = suit(c[0])
        r = min(rank(x) for x in c)
        starts_by_suit.setdefault(s, set()).add(r)
    pts = 0
    suits = ['B', 'C', 'D']
    if all(s in starts_by_suit for s in suits):
        common = starts_by_suit[suits[0]] & starts_by_suit[suits[1]] & starts_by_suit[suits[2]]
        pts += 8 * len(common)
    return pts


def points_mixed_shifted_pungs(sets):
    # 8 points: Three Pungs or Kongs in the three different suits, shifted up by one
    pungs_by_suit = {'B': set(), 'C': set(), 'D': set()}
    
    for s in sets:
        if len(s) in (3, 4) and len(set(s)) == 1:  # Pung or Kong
            t = s[0]
            if is_suit(t):
                s_suit = suit(t)
                s_rank = rank(t)
                if s_suit in pungs_by_suit:
                    pungs_by_suit[s_suit].add(s_rank)
    
    # Check for shifted pungs: rank, rank+1, rank+2 in different suits
    for base_rank in range(1, 8):  # Can't have rank 9 shifted up
        ranks_needed = {base_rank, base_rank + 1, base_rank + 2}
        suits_found = set()
        
        for s_suit, ranks in pungs_by_suit.items():
            if ranks_needed & ranks:  # If this suit has any of the needed ranks
                for rank_val in ranks_needed & ranks:
                    suits_found.add((s_suit, rank_val))
        
        # Check if we have exactly one pung from each of the three suits
        if len(suits_found) == 3:
            suit_ranks = list(suits_found)
            # Verify they are in different suits and properly shifted
            suits_used = {sr[0] for sr in suit_ranks}
            ranks_used = {sr[1] for sr in suit_ranks}
            
            if len(suits_used) == 3 and ranks_used == ranks_needed:
                return 8
    
    return 0


def points_two_concealed_kongs(sets, concealed_mask):
    # 8 points: Two concealed Kongs
    if concealed_mask is None:
        return 0  # Can't determine if kongs are concealed
    
    concealed_kongs = 0
    for i, s in enumerate(sets):
        if is_kong(s) and i < len(concealed_mask) and concealed_mask[i]:
            concealed_kongs += 1
    
    return 8 if concealed_kongs >= 2 else 0


def points_last_tile_draw(meta):
    # 8 points: Winning by draw on the last tile of the wall
    last_tile_draw = meta.get('last_tile_draw', False)
    win_by = meta.get('win_by')
    return 8 if last_tile_draw and win_by == 'self' else 0


def points_last_tile_claim(meta):
    # 8 points: Winning by discard after the last tile of the wall is drawn
    last_tile_claim = meta.get('last_tile_claim', False)
    win_by = meta.get('win_by')
    return 8 if last_tile_claim and win_by == 'discard' else 0


def points_out_with_replacement_tile(meta):
    # 8 points: Winning on the replacement tile from declaring a Kong
    replacement_tile_win = meta.get('replacement_tile_win', False)
    return 8 if replacement_tile_win else 0


def points_robbing_the_kong(meta):
    # 8 points: Winning off the tile that another player attempts to use to promote a Pung to a Kong
    robbing_kong = meta.get('robbing_kong', False)
    return 8 if robbing_kong else 0


def points_chicken_hand(sets, pair, all_tiles, meta):
    # 8 points: Winning with a hand that would otherwise be worth 0 points other than flowers
    # This is a complex rule that requires checking if the hand would score 0 without this rule
    
    # First, let's check if this is explicitly marked as a chicken hand
    chicken_hand = meta.get('chicken_hand', False)
    if chicken_hand:
        return 8
    
    # Alternative implementation: check if the hand has no other scoring patterns
    # This is a simplified check - in practice, this would require a full scoring analysis
    # without the chicken hand rule to see if it would score 0
    
    # For now, we'll rely on the meta flag being set
    return 0


def compute_points_8(sets, pair, all_tiles, meta):
    p8 = {
        'Mixed Triple Chow': points_mixed_triple_chow(sets),
        'Mixed Straight': points_mixed_straight(sets),
        'Reversible Tiles': points_reversible_tiles(all_tiles),
        'Mixed Shifted Pungs': points_mixed_shifted_pungs(sets),
        'Two Concealed Kongs': points_two_concealed_kongs(sets, meta.get('concealed_melds')),
        'Last Tile Draw': points_last_tile_draw(meta),
        'Last Tile Claim': points_last_tile_claim(meta),
        'Out with Replacement Tile': points_out_with_replacement_tile(meta),
        'Robbing the Kong': points_robbing_the_kong(meta),
        'Chicken Hand': points_chicken_hand(sets, pair, all_tiles, meta),
    }
    return sum(p8.values()), {k: v for k, v in p8.items() if v}


