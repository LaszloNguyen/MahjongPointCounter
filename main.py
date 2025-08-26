from scoring import best_score


if __name__ == "__main__":
    # Example hand: B1 B2 B3  B1 B2 B3  C4 C5 C6  D7 D8 D9  DR DR  (self-drawn, no opens)
    hand = ["B1", "B2", "B3", "B1", "B2", "B3", "C4", "C5", "C6", "D7", "D8", "D9", "DR", "DR"]
    meta = {
        'seat_wind': 'E',
        'prevalent_wind': 'E',
        'win_by': 'self',
        'melds_open': False,
        'wait_type': None,
    }
    print(best_score(hand, meta))
