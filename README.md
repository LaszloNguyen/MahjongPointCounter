# Mahjong Scorer

Minimal Mahjong (MCR subset) scoring utilities, organized into modules.

## Structure
- `tiles.py`: Tile constants/utilities, normalization, multiset helpers
- `melds.py`: Meld detection helpers (`is_pung`, `is_chow`, `is_kong`)
- `partition.py`: Hand partitioning into sets and pair
- `scoring.py`: Scoring rules and `best_score`
- `main.py`: Runnable example

## Requirements
- Python 3.8+

## Usage
Run the example:

```bash
python main.py
```

Use as a library:

```python
from scoring import best_score

hand = [
    "B1","B2","B3",
    "B1","B2","B3",
    "C4","C5","C6",
    "D7","D8","D9",
    "DR","DR",
]
meta = {
    'seat_wind': 'E',
    'prevalent_wind': 'E',
    'win_by': 'self',
    'melds_open': False,
    'wait_type': None,
}
result = best_score(hand, meta)
print(result)
```

## Public API
If imported as a package, these names are exported via `__init__.py`:
- Tile helpers: `is_suit`, `suit`, `rank`, `normalize_hand`, `tiles_to_multiset`, `remove_tiles`
- Melds: `is_pung`, `is_chow`, `is_kong`
- Partition: `enumerate_partitions`, `enumerate_sets`
- Scoring: `best_score`, `score_partition`

## Notes
- Flowers contribute 1 point each but don't count toward the MCR minimum 8 points.
- Only a subset of MCR scoring rules is implemented; extend as needed.
