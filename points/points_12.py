from tiles import HONORS, is_suit, rank, suit


def points_lesser_honors_and_knitted_tiles(all_tiles):
    """
    12 points: The hand is entirely composed of single (unpaired) honors and single tiles 
    from different knitted sequences. If this rule is satisfied, the player can win without 
    the standard 4 triples and a pair.
    
    Knitted sequences are singles of 1,4,7 in one suit, 2,5,8 in a second suit and 3,6,9 in the third suit.
    """
    # Check if all tiles are single (unpaired)
    tile_counts = {}
    for tile in all_tiles:
        tile_counts[tile] = tile_counts.get(tile, 0) + 1
    
    # All tiles must appear exactly once (unpaired)
    if any(count != 1 for count in tile_counts.values()):
        return 0
    
    # Separate honors and suit tiles
    honors = [t for t in all_tiles if t in HONORS]
    suit_tiles = [t for t in all_tiles if is_suit(t)]
    
    # Check knitted sequences
    # Sequence 1: 1,4,7 in one suit
    # Sequence 2: 2,5,8 in a second suit  
    # Sequence 3: 3,6,9 in the third suit
    
    suits_present = {suit(t) for t in suit_tiles}
    if len(suits_present) != 3:
        return 0  # Need exactly 3 suits
    
    # Group tiles by suit and rank
    tiles_by_suit = {'B': set(), 'C': set(), 'D': set()}
    for t in suit_tiles:
        s = suit(t)
        r = rank(t)
        if s in tiles_by_suit:
            tiles_by_suit[s].add(r)
    
    # Check if we have the correct knitted sequences
    sequence1_ranks = {1, 4, 7}
    sequence2_ranks = {2, 5, 8}
    sequence3_ranks = {3, 6, 9}
    
    # Find which suit has which sequence
    suits_with_sequences = []
    
    for s in ['B', 'C', 'D']:
        ranks = tiles_by_suit[s]
        if ranks == sequence1_ranks:
            suits_with_sequences.append(('sequence1', s))
        elif ranks == sequence2_ranks:
            suits_with_sequences.append(('sequence2', s))
        elif ranks == sequence3_ranks:
            suits_with_sequences.append(('sequence3', s))
    
    # Must have exactly one of each sequence
    if len(suits_with_sequences) != 3:
        return 0
    
    # Check that we have one of each sequence
    sequences_found = {seq for seq, _ in suits_with_sequences}
    if sequences_found != {'sequence1', 'sequence2', 'sequence3'}:
        return 0
    
    # All conditions met: single honors + single tiles from different knitted sequences
    return 12


def points_knitted_straight(sets, all_tiles):
    """
    12 points: Winning with a hand that has 1,4,7 in one suit, 2,5,8 in a second suit and 3,6,9 in the third suit. 
    This knitted straight is considered to be 3 Chows for the requirement of 4 triples and a pair.
    """
    # Check if we have exactly 4 sets (the knitted straight counts as 3 chows + 1 other set)
    if len(sets) != 4:
        return 0
    
    # Check if the knitted straight pattern exists in the tiles
    # We need to find 1,4,7 in one suit, 2,5,8 in a second suit, and 3,6,9 in the third suit
    suit_tiles = [t for t in all_tiles if is_suit(t)]
    
    # Group tiles by suit and rank
    tiles_by_suit = {'B': set(), 'C': set(), 'D': set()}
    for t in suit_tiles:
        s = suit(t)
        r = rank(t)
        if s in tiles_by_suit:
            tiles_by_suit[s].add(r)
    
    # Check if we have the correct knitted sequences
    sequence1_ranks = {1, 4, 7}
    sequence2_ranks = {2, 5, 8}
    sequence3_ranks = {3, 6, 9}
    
    # Find which suit has which sequence
    suits_with_sequences = []
    
    for s in ['B', 'C', 'D']:
        ranks = tiles_by_suit[s]
        if ranks == sequence1_ranks:
            suits_with_sequences.append(('sequence1', s))
        elif ranks == sequence2_ranks:
            suits_with_sequences.append(('sequence2', s))
        elif ranks == sequence3_ranks:
            suits_with_sequences.append(('sequence3', s))
    
    # Must have exactly one of each sequence
    if len(suits_with_sequences) != 3:
        return 0
    
    # Check that we have one of each sequence
    sequences_found = {seq for seq, _ in suits_with_sequences}
    if sequences_found != {'sequence1', 'sequence2', 'sequence3'}:
        return 0
    
    # All conditions met: knitted straight pattern found
    return 12


def _is_knitted_chow(s):
    """Check if a set is a knitted chow (1,4,7 or 2,5,8 or 3,6,9 in one suit)"""
    if len(s) != 3:
        return False
    
    # Must be a chow (consecutive ranks in same suit)
    if not all(is_suit(t) for t in s):
        return False
    
    suit_name = suit(s[0])
    if not all(suit(t) == suit_name for t in s):
        return False
    
    ranks = sorted(rank(t) for t in s)
    
    # Check if it's one of the knitted patterns
    knitted_patterns = [{1, 4, 7}, {2, 5, 8}, {3, 6, 9}]
    return set(ranks) in knitted_patterns


def _forms_knitted_straight(sets):
    """Check if the given sets form a complete knitted straight (1,4,7 + 2,5,8 + 3,6,9 in different suits)"""
    if len(sets) != 3:
        return False
    
    # Each set must be a knitted chow
    if not all(_is_knitted_chow(s) for s in sets):
        return False
    
    # Must be in different suits
    suits = {suit(s[0]) for s in sets}
    if len(suits) != 3:
        return False
    
    # Must have the three different knitted patterns
    patterns = []
    for s in sets:
        ranks = sorted(rank(t) for t in s)
        patterns.append(set(ranks))
    
    required_patterns = [{1, 4, 7}, {2, 5, 8}, {3, 6, 9}]
    return all(pattern in patterns for pattern in required_patterns)


def compute_points_12(sets, pair, all_tiles, meta):
    p12 = {
        'Lesser Honors and Knitted Tiles': points_lesser_honors_and_knitted_tiles(all_tiles),
        'Knitted Straight': points_knitted_straight(sets, all_tiles),
    }
    return sum(p12.values()), {k: v for k, v in p12.items() if v}
