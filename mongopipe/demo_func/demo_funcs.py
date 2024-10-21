def identity(doc: dict):
    return doc

def cap_interests(doc: dict):
    capped_interests = [interest.capitalize() for interest in doc["interests"]]
    return {"interests": capped_interests}

# Hard Coded, for demo purposes only
def correct_city_and_state(doc: dict):
    city = doc["address"]["city"]
    state_map = {
        "San Francisco": "CA",
        "New York": "NY",
        "Chicago": "IL",
        "Los Angeles": "CA",
        "Seattle": "WA",
        "Boston": "MA",
        "Houston": "TX",
        "Miami": "FL",
        "Austin": "TX",
        "Portland": "OR"
    }
    state = state_map.get(city, "Unknown")
    return {"address": {"state": state}}