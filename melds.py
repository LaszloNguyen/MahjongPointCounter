from tiles import is_suit, suit, rank


def is_pung(m):
    return len(m) == 3 and len(set(m)) == 1


def is_chow(m):
    if len(m) != 3:
        return False
    if not all(is_suit(t) for t in m):
        return False
    s = suit(m[0])
    if any(suit(t) != s for t in m):
        return False
    rs = sorted(rank(t) for t in m)
    return rs[1] == rs[0] + 1 and rs[2] == rs[1] + 1


def is_kong(m):
    return len(m) == 4 and len(set(m)) == 1


