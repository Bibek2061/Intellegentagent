A = (0, 0)
B = (1, 0)

state = {
    A: "Unknown",
    B: "Unknown",
    "agent_location": None
}

goal = {
    A: "Clean",
    B: "Clean"
}

def match_rules(memory, location):
    if memory[A] == goal[A] and memory[B] == goal[B]:
        return "NoOp"

    if memory[location] == "Dirty":
        return "Clean"

    if location == A:
        return "Right"

    return "Left"

def update_state(state, location, status):
    state["agent_location"] = location
    state[location] = status
    return state

def model_based_reflex_agent(percept):
    location, status = percept
    update_state(state, location, status)
    action = match_rules(state, location)
    return action

def run():
    print(model_based_reflex_agent((B, "Dirty")))
    print(model_based_reflex_agent((B, "Clean")))
    print(model_based_reflex_agent((A, "Dirty")))
    print(model_based_reflex_agent((A, "Clean")))
    print(model_based_reflex_agent((B, "Clean")))
run()