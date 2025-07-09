# parsing_table_builder.py

grammar = {
    "S": [["i", "E", "t", "S", "S'"], ["a"]],
    "S'": [["e", "S"], []],
    "E": [["b"]]
}

non_terminals = list(grammar.keys())


def compute_first(grammar):
    first = {nt: set() for nt in grammar}

    def first_of(symbol):
        if symbol not in grammar:
            return {symbol}
        result = set()
        for production in grammar[symbol]:
            if not production:
                result.add('ε')
                continue
            for sym in production:
                sym_first = first_of(sym)
                result |= sym_first - {'ε'}
                if 'ε' not in sym_first:
                    break
            else:
                result.add('ε')
        return result

    changed = True
    while changed:
        changed = False
        for nt in grammar:
            before = set(first[nt])
            for prod in grammar[nt]:
                prod_first = set()
                for symbol in prod:
                    sym_first = first_of(symbol)
                    prod_first |= sym_first - {'ε'}
                    if 'ε' not in sym_first:
                        break
                else:
                    prod_first.add('ε')
                first[nt] |= prod_first
            if before != first[nt]:
                changed = True

    return first


def compute_follow(grammar, first_sets, start_symbol='S'):
    follow = {nt: set() for nt in grammar}
    follow[start_symbol].add('$')

    def first_of_sequence(seq):
        result = set()
        for symbol in seq:
            symbol_first = first_sets[symbol] if symbol in grammar else {symbol}
            result |= symbol_first - {'ε'}
            if 'ε' not in symbol_first:
                break
        else:
            result.add('ε')
        return result

    changed = True
    while changed:
        changed = False
        for head, productions in grammar.items():
            for prod in productions:
                for i, B in enumerate(prod):
                    if B in grammar:
                        rest = prod[i+1:]
                        trailer = first_of_sequence(rest)
                        before = set(follow[B])
                        follow[B] |= trailer - {'ε'}
                        if 'ε' in trailer or not rest:
                            follow[B] |= follow[head]
                        if follow[B] != before:
                            changed = True

    return follow


def build_parsing_table(grammar, first_sets, follow_sets):
    table = {nt: {} for nt in grammar}
    for head, productions in grammar.items():
        for prod in productions:
            first_alpha = set()
            if not prod:
                first_alpha = {'ε'}
            else:
                for symbol in prod:
                    sym_first = first_sets[symbol] if symbol in grammar else {symbol}
                    first_alpha |= sym_first - {'ε'}
                    if 'ε' not in sym_first:
                        break
                else:
                    first_alpha.add('ε')

            for terminal in first_alpha - {'ε'}:
                table[head][terminal] = prod
            if 'ε' in first_alpha:
                for terminal in follow_sets[head]:
                    table[head][terminal] = []

    return table


def get_first_follow_and_table():
    first = compute_first(grammar)
    follow = compute_follow(grammar, first)
    table = build_parsing_table(grammar, first, follow)
    return first, follow, table
