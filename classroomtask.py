A = (0, 0)
B = (1, 0)
C = (0, 1)
D = (1, 1)

rules = {
    (B, 'Dirty'): 'Clean',
    (B, 'Clean'): 'Go to D',
    (D, 'Dirty'): 'Clean',
    (D, 'Clean'): 'Go to A',
    (A, 'Clean'): 'Stop'
}

def rule_match(state, rules):
    return rules.get(state)

def simple_reflex_agent(percept):
    action = rule_match(percept, rules)
    return action

def run():
    print(simple_reflex_agent((B, 'Dirty')))
    print(simple_reflex_agent((B, 'Clean')))
    print(simple_reflex_agent((D, 'Dirty')))
    print(simple_reflex_agent((D, 'Clean')))
    print(simple_reflex_agent((A, 'Clean')))

run()