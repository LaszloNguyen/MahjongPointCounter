from scoring import best_score

def test_knitted_straight():
    # Test case: Knitted Straight
    # Hand: B1 B2 B3 (regular chow) + C2 C3 C4 (regular chow) + D3 D4 D5 (regular chow) + B4 B5 B6 (regular chow) + DR DR (pair)
    # This should form a valid hand, and the knitted straight rule should check if there's a knitted pattern in the tiles
    hand = ["B1", "B4", "B7", "C2", "C5", "C8", "D3", "D6", "D9", "WE", "WE", "WE", "DR", "DR"]
    meta = {
        'seat_wind': 'E',
        'prevalent_wind': 'E',
        'win_by': 'discard',
        'melds_open': False,
        'wait_type': None,
    }
    
    result = best_score(hand, meta)
    print("Test Knitted Straight (should get 12 points):")
    print(f"Hand: {hand}")
    print(f"Meta: {meta}")
    print(f"Result: {result}")
    
    if 'Knitted Straight' in result['breakdown']:
        print("✓ Knitted Straight rule correctly applied!")
        print(f"Points from Knitted Straight: {result['breakdown']['Knitted Straight']}")
    else:
        print("✗ Knitted Straight rule not found in breakdown")
        print(f"Available rules: {list(result['breakdown'].keys())}")

def test_knitted_straight_invalid():
    # Test case: Invalid knitted straight (should NOT get points)
    # Hand: B1 B4 B7 (knitted chow 1) + C2 C5 C8 (knitted chow 2) + D3 D6 D8 (wrong pattern) + DR DR DR (pung) + B9 B9 (pair)
    hand = ["B1", "B4", "B7", "C2", "C5", "C8", "D3", "D6", "D8", "DR", "DR", "DR", "B9", "B9"]
    meta = {
        'seat_wind': 'E',
        'prevalent_wind': 'E',
        'win_by': 'discard',
        'melds_open': False,
        'wait_type': None,
    }
    
    result = best_score(hand, meta)
    print("\nTest Knitted Straight Invalid (should NOT get points):")
    print(f"Hand: {hand}")
    
    if 'Knitted Straight' in result.get('breakdown', {}):
        print("✗ Knitted Straight rule incorrectly applied!")
    else:
        print("✓ Knitted Straight rule correctly NOT applied")

def test_knitted_straight_wrong_structure():
    # Test case: Wrong hand structure (should NOT get points)
    # Hand: B1 B4 B7 (knitted chow 1) + C2 C5 C8 (knitted chow 2) + D3 D6 D9 (knitted chow 3) + B9 B9 (pair) - missing 4th set
    hand = ["B1", "B4", "B7", "C2", "C5", "C8", "D3", "D6", "D9", "B9", "B9"]
    meta = {
        'seat_wind': 'E',
        'prevalent_wind': 'E',
        'win_by': 'discard',
        'melds_open': False,
        'wait_type': None,
    }
    
    result = best_score(hand, meta)
    print("\nTest Knitted Straight Wrong Structure (should NOT get points):")
    print(f"Hand: {hand}")
    
    if result.get('valid', False) and 'Knitted Straight' in result.get('breakdown', {}):
        print("✗ Knitted Straight rule incorrectly applied!")
    else:
        print("✓ Knitted Straight rule correctly NOT applied")

if __name__ == "__main__":
    test_knitted_straight()
    test_knitted_straight_invalid()
    test_knitted_straight_wrong_structure()
