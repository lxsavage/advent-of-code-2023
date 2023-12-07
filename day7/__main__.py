# Problem: https://adventofcode.com/2023/day/7
import sys
import time
import functools

VERBOSE = False


def parse_input(input: list[str]) -> list[dict]:
    # [{hand: [str], bid: int}]
    hands = []
    for line in input:
        if line == '':
            continue
        hand_bid = line.split(' ')
        hands.append({
            'hand': hand_bid[0],
            'bid': int(hand_bid[1])
        })
    return hands


# -- PART 1 -- #
def determine_hand_type(hand: str) -> int:
    """
    6: Five of a kind
    5: Four of a kind
    4: Full house
    3: Three of a kind
    2: Two pair
    1: One pair
    0: High card
    """
    hand_str = hand['hand']

    # Five of a kind
    if hand_str == ''.join([hand_str[0]] * 5):
        return 6

    card_matches = {}
    for card in hand_str:
        if card[0] in card_matches:
            card_matches[card[0]] += 1
        else:
            card_matches[card[0]] = 1

    # Four of a kind
    if 4 in card_matches.values():
        return 5

    # Full house
    if 3 in card_matches.values() and 2 in card_matches.values():
        return 4

    # Three of a kind
    if 3 in card_matches.values():
        return 3

    # Two pair
    if list(card_matches.values()).count(2) == 2:
        return 2

    # One pair
    if 2 in card_matches.values():
        return 1

    # High card
    return 0


def get_high_card(card1: str, card2: str) -> int:
    # Both number cards
    if card1.isdigit() and card2.isdigit():
        c1_int = int(card1)
        c2_int = int(card2)
        if c1_int > c2_int:
            return -1
        elif c1_int < c2_int:
            return 1
        else:
            return 0

    # One face card, one number
    if card1.isdigit():
        return 1
    elif card2.isdigit():
        return -1

    # Two face cards
    order = ['A', 'K', 'Q', 'J', 'T']
    if card1 in order and card2 in order:
        c1_int = order.index(card1)
        c2_int = order.index(card2)
        if c1_int < c2_int:
            return -1
        elif c1_int > c2_int:
            return 1

    return 0


def resolve(hand1: (int, str), hand2: (int, str)) -> int:
    """
    Returns -1 if hand1 wins, 1 if hand2 wins, 0 if identical hands
    """
    hand1_rank, hand1_struct = hand1
    hand2_rank, hand2_struct = hand2

    hand1_str = hand1_struct['hand']
    hand2_str = hand2_struct['hand']

    # Skip if hands are different types, resolve normally
    if hand1_rank > hand2_rank:
        return -1
    elif hand1_rank < hand2_rank:
        return 1

    # First card is different, find the max between the two
    for i in range(5):
        c1 = hand1_str[i]
        c2 = hand2_str[i]
        if get_high_card(c1, c2) == -1:
            return -1
        elif get_high_card(c1, c2) == 1:
            return 1

    return 0


def cmp_hand_power(hand1: str, hand2: str) -> int:
    """
    Comparator: Orders cards from weakest to strongest as defined by part 1
    """
    return resolve((determine_hand_type(hand1), hand1),
                   (determine_hand_type(hand2), hand2))


# -- PART 2 -- #
def determine_hand_type_with_joker(hand: str) -> int:
    """
    6: Five of a kind
    5: Four of a kind
    4: Full house
    3: Three of a kind
    2: Two pair
    1: One pair
    0: High card
    """
    def first_non_joker():
        for card in hand_str:
            if card != 'J':
                return card

    hand_str = hand['hand']

    # Five of a kind
    if hand_str == 'JJJJJ':
        return 6
    else:
        first_card = first_non_joker()
        first_card_seq = first_card * 5
        hand_str_alt = hand_str.replace('J', first_card)
        print(f'"{first_card_seq}"', f'"{hand_str_alt}"')
        if hand_str_alt == first_card_seq:
            vprint(f'Five of a kind: {hand_str}')
            return 6

    card_matches = {}
    for card in hand_str:
        if card[0] in card_matches:
            card_matches[card[0]] += 1
        else:
            card_matches[card[0]] = 1

    # Create the best hand possible with the joker
    joker_count = card_matches['J'] if 'J' in card_matches else 0
    card_matches['J'] = 0

    # Four of a kind
    if 4 in card_matches.values() or \
            max(card_matches.values()) + joker_count >= 4:
        vprint(f'Four of a kind: {hand_str}')
        return 5

    # Full house
    # AABBJJ is only possible way, given A and B are any non-joker cards
    if (3 in card_matches.values() and 2 in card_matches.values()) or (
            joker_count == 1 and
            (max(card_matches.values()) == 2 and
             sum(1 for x in card_matches.values() if x == 2) == 2)):
        vprint(f'Full house: {hand_str}')
        return 4

    # Three of a kind
    if 3 in card_matches.values() or \
            max(card_matches.values()) + joker_count >= 3:
        vprint(f'Three of a kind: {hand_str}')
        return 3

    # Two pair
    if list(card_matches.values()).count(2) == 2 or joker_count >= 2:
        vprint(f'Two pair: {hand_str}')
        return 2

    # One pair
    if 2 in card_matches.values() or joker_count > 0:
        vprint(f'One pair: {hand_str}')
        return 1

    # High card
    vprint(f'High card: {hand_str}')
    return 0


def get_high_card_with_joker(card1: str, card2: str) -> int:
    # Both number cards
    if card1.isdigit() and card2.isdigit():
        c1_int = int(card1)
        c2_int = int(card2)
        print(c1_int, c2_int, card1, card2)
        if c1_int < c2_int:
            return 1
        elif c1_int > c2_int:
            return -1
        else:
            return 0

    order = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
    if card1 in order and card2 in order:
        c1_int = order.index(card1)
        c2_int = order.index(card2)
        if c1_int < c2_int:
            return 1
        elif c1_int > c2_int:
            return -1

    return 0


def resolve_p2(hand1: (int, str), hand2: (int, str)) -> int:
    """
    Returns -1 if hand1 wins, 1 if hand2 wins, 0 if identical hands
    """
    hand1_rank, hand1_struct = hand1
    hand2_rank, hand2_struct = hand2

    hand1_str = hand1_struct['hand']
    hand2_str = hand2_struct['hand']

    # Skip if hands are different types, resolve normally
    if hand1_rank > hand2_rank:
        return -1
    elif hand1_rank < hand2_rank:
        return 1

    # First card is different, find the max between the two
    vprint(f'\tConflict: {hand1_str} vs {hand2_str}')
    for i in range(5):
        c1 = hand1_str[i]
        c2 = hand2_str[i]
        if get_high_card_with_joker(c1, c2) == -1:
            vprint(f'b\t\t{c1} > {c2}')
            vprint(f'\t\t{hand1_str} > {hand2_str}')
            return -1
        elif get_high_card_with_joker(c1, c2) == 1:
            vprint(f'a\t\t{c1} < {c2}')
            vprint(f'\t\t{hand1_str} < {hand2_str}')
            return 1

    return 0


def cmp_hand_power_p2(hand1: str, hand2: str) -> int:
    """
    Comparator: Orders cards from weakest to strongest as defined by part 1
    """
    return resolve_p2((determine_hand_type_with_joker(hand1), hand1),
                      (determine_hand_type_with_joker(hand2), hand2))


# -- END PART 2 -- #
def vprint(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)


def get_winnings(input: list[dict], part2: bool = False):
    comparator = cmp_hand_power_p2 if part2 else cmp_hand_power
    weakest_to_strongest = sorted(input,
                                  key=functools.cmp_to_key(comparator))
    vprint('Ranking of hands from weakest to strongest:')
    total_bid = 0
    hand_count = len(weakest_to_strongest)
    for i, hand in enumerate(weakest_to_strongest):
        total_bid += hand['bid'] * (hand_count - i)
        vprint(f'{i + 1}: {hand["hand"]}\t{hand["bid"]} * {hand_count - i}')
    print(f'Total winnings: {total_bid}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <input_file>')
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        input = parse_input([line.strip() for line in f.readlines()])

    start_time = time.time()
    get_winnings(input, len(sys.argv) > 2 and sys.argv[2] == '2')
    completion_time = round(time.time() - start_time, 4)
    print(f'--- Completed in {completion_time} seconds ---')
