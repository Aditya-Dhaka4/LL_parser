# parser_logic.py

parsing_table = {
    'S': {
        'i': ['i', 'E', 't', 'S', 'X'],
        'a': ['a']
    },
    'X': {
        'e': ['e', 'S'],
        '$': []  # ε
    },
    'E': {
        'b': ['b']
    }
}

def parse(input_string):
    stack = ['$', 'S']
    input_string += '$'
    pointer = 0
    steps = []

    while stack:
        top = stack[-1]
        current_input = input_string[pointer]

        step_info = {
            "stack": ''.join(stack),
            "input": input_string[pointer:],
            "action": ""
        }

        if top == current_input:
            stack.pop()
            pointer += 1
            step_info["action"] = f"Match '{top}'"
        elif top in parsing_table:
            if current_input in parsing_table[top]:
                stack.pop()
                production = parsing_table[top][current_input]
                step_info["action"] = f"{top} → {' '.join(production) if production else 'ε'}"
                for symbol in reversed(production):
                    if symbol != '':
                        stack.append(symbol)
            else:
                step_info["action"] = f"Error: no rule for ({top}, {current_input})"
                steps.append(step_info)
                break
        else:
            step_info["action"] = f"Error: terminal mismatch ({top}, {current_input})"
            steps.append(step_info)
            break

        steps.append(step_info)

        if stack == ['$'] and input_string[pointer] == '$':
            steps.append({"stack": '$', "input": '$', "action": "Accepted"})
            break

    return steps


def get_parsing_table():
    return {
        "S": {"i": "S → iEtSX", "a": "S → a"},
        "X": {"e": "X → eS", "$": "X → ε"},
        "E": {"b": "E → b"}
    }
