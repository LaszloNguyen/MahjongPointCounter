"""
Combines scoring breakdown by enforcing "Does not combine with" exclusions.

Provide a single entry point: process_exclusions(breakdown: dict) -> dict
It removes keys from breakdown that are excluded by any present rule.

Rule names must match those used in breakdown from score_partition.
"""

from typing import Dict


# Map: rule -> set[rules it excludes]
EXCLUSIONS = {
    # 8-point
    'Mixed Triple Chow': {
        'Mixed Double Chow',
    },
    'Reversible Tiles': {
        'One Voided Suit',
    },

    # 64/88-point high hands often exclude overlapping lower rules
    'Big Four Winds': {
        'Pung of Terminals/Honors (non-seat/prevalent)',
        'Prevalent Wind Pung/Kong',
        'Seat Wind Pung/Kong',
        'All Pungs',
        'Big Three Winds',
    },
    'Big Three Dragons': {
        'Dragon Pung/Kong',
        'Two Dragon Pungs',
    },
    'Four Kongs': {
        'Melded Kong',
        'Two Melded Kongs',
        'Three Kongs',
        'All Pungs',
        'Wait Type (edge/closed/pair)',
    },
    'Pure Terminal Chows': {
        'Pure Double Chow',
        'Two Terminal Chows',
        'One Voided Suit',
        'All Chows',
        'Half Flush',
        'Full Flush',
    },
    'Nine Gates': {
        'Pung of Terminals/Honors (non-seat/prevalent)',
        'One Voided Suit',
        'Concealed Hand (won by discard)',
        'Half Flush',
        'Full Flush',
    },
    'Seven Shifted Pairs': {
        'One Voided Suit',
        'No Honor Tiles',
        'Wait Type (edge/closed/pair)',
        'Concealed Hand (won by discard)',
        'Half Flush',
        'Full Flush',
    },
    'Big Three Winds': {
        'Seat Wind Pung/Kong',
        'Prevalent Wind Pung/Kong',
        'All Pungs',
        'Pung of Terminals/Honors (non-seat/prevalent)',
    },
    'Melded Hand': {
        'Concealed Hand (won by discard)',
    },
    'Mixed Shifted Pungs': {
        'Mixed Double Chow',
    },
    'Two Concealed Kongs': {
        'Melded Kong',
        'Two Melded Kongs',
    },
    'Last Tile Draw': {
        'Self-Drawn',
    },
    'Last Tile Claim': {
        'Concealed Hand (won by discard)',
    },
    'Out with Replacement Tile': {
        'Self-Drawn',
    },
    'Robbing the Kong': {
        'Concealed Hand (won by discard)',
    },
    'Chicken Hand': {
        # Chicken Hand doesn't exclude other rules since it's a fallback for 0-point hands
    },
    'Lesser Honors and Knitted Tiles': {
        # This rule allows winning without standard 4 triples and a pair
        # It doesn't exclude other rules since it's a special winning condition
    },
    'Knitted Straight': {
        'Mixed Straight',
    },
}


def process_exclusions(breakdown: Dict[str, int]) -> Dict[str, int]:
    """Return a new breakdown dict after applying exclusion rules.

    If a rule is present, all rules it excludes are removed (if present).
    """
    if not breakdown:
        return breakdown
    remaining = dict(breakdown)
    # Iterate deterministically by rule name for reproducibility
    for rule in sorted(list(breakdown.keys())):
        if rule not in remaining:
            continue
        for excluded in EXCLUSIONS.get(rule, set()):
            if excluded in remaining:
                del remaining[excluded]
    return remaining


