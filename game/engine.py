"""Game engine for Junior Astronaut Mission Trainer.

The server keeps NO memory between requests. The whole game lives in a
GameState object that is turned into a plain dictionary (JSON), sent to the
browser, and sent back with every choice.

Turn order for each sol:
    1. apply_choice()      - the player's choice changes the resources
    2. check_game_over()   - did a resource hit 0?
    3. tick()              - the base uses power, air and shielding wears down
    4. check_game_over()   - again
    5. advance to the next sol (or finish the mission after sol 10)
"""

from dataclasses import dataclass, field

from . import events as event_data
from .data import facts_for

TOTAL_SOLS = 10
MIN_LEVEL = 0
MAX_LEVEL = 100
RESOURCES = ("power", "oxygen", "shielding")

# Difficulty settings: starting level for every meter and what the outpost
# uses or loses at the end of every sol.
DIFFICULTIES = {
    "easy": {"label": "Easy", "start": 85,
             "upkeep": {"power": -4, "oxygen": -4, "shielding": -3}},
    "normal": {"label": "Normal", "start": 75,
               "upkeep": {"power": -5, "oxygen": -5, "shielding": -4}},
    "hard": {"label": "Hard", "start": 65,
             "upkeep": {"power": -6, "oxygen": -6, "shielding": -5}},
}
DEFAULT_DIFFICULTY = "normal"
START_LEVEL = DIFFICULTIES[DEFAULT_DIFFICULTY]["start"]
DAILY_UPKEEP = DIFFICULTIES[DEFAULT_DIFFICULTY]["upkeep"]   # Normal upkeep (kept for reference)

RESOURCE_INFO = {
    "power": {"label": "Power", "icon": "⚡"},
    "oxygen": {"label": "Oxygen", "icon": "🫁"},
    "shielding": {"label": "Shielding", "icon": "🛡️"},
}

LOSS_MESSAGES = {
    "power": "Power ran out. The lights, heaters and air machines all switched off.",
    "oxygen": "Oxygen ran out. The crew could not breathe safely, so the mission ended.",
    "shielding": "The shield wall failed. The crew got too much radiation, so the mission ended.",
}

MAX_LOG_LINES = 40
SCIENCE_GOAL_COMPARE = 30   # science needed for a research-style comparison
HEALTHY_COMPARE = 40        # every meter at or above this = "all healthy"
TECH_DEMO_SCIENCE = 10      # science below this (with healthy meters) = tech demo
SCIENCE_GOAL = 25      # science points needed for the research star
HEALTHY_LEVEL = 20     # every resource at or above this earns the safety star


def clamp(value):
    """Keep a resource between 0 and 100."""
    return max(MIN_LEVEL, min(MAX_LEVEL, int(round(value))))


@dataclass
class GameState:
    """Everything about one game. Easy to convert to and from JSON."""

    sol: int = 1
    power: int = START_LEVEL
    oxygen: int = START_LEVEL
    shielding: int = START_LEVEL
    science: int = 0
    difficulty: str = DEFAULT_DIFFICULTY   # "easy", "normal" or "hard"
    status: str = "playing"          # "playing", "won" or "lost"
    reason: str = ""                  # why the game ended
    event_queue: list = field(default_factory=list)   # event ids, one per sol
    modifiers: list = field(default_factory=list)     # effects lasting several sols
    log: list = field(default_factory=list)           # mission log (text lines)
    history: list = field(default_factory=list)       # [{sol, event_id, choice_id}]

    # -- creating / saving ---------------------------------------------------
    @classmethod
    def new(cls, rng=None, difficulty=DEFAULT_DIFFICULTY):
        """Start a fresh game with the events in a random order."""
        if difficulty not in DIFFICULTIES:
            raise ValueError("Difficulty must be easy, normal or hard.")
        start = DIFFICULTIES[difficulty]["start"]
        state = cls(power=start, oxygen=start, shielding=start, difficulty=difficulty,
                    event_queue=event_data.shuffled_event_ids(rng))
        state.add_log("Mission begins! Your lunar outpost is ready.")
        return state

    @classmethod
    def from_dict(cls, data):
        """Rebuild a state from browser JSON, checking it is sensible."""
        if not isinstance(data, dict):
            raise ValueError("The game state is missing.")
        try:
            queue = list(data.get("event_queue", []))
            valid_ids = set(event_data.event_ids())
            if len(queue) != TOTAL_SOLS or set(queue) != valid_ids:
                raise ValueError("The event list is not valid.")

            status = data.get("status", "playing")
            if status not in ("playing", "won", "lost"):
                raise ValueError("The game status is not valid.")

            difficulty = data.get("difficulty", DEFAULT_DIFFICULTY)
            if difficulty not in DIFFICULTIES:
                raise ValueError("The difficulty is not valid.")

            sol = int(data.get("sol", 1))
            if not 1 <= sol <= TOTAL_SOLS:
                raise ValueError("The sol number is not valid.")

            modifiers = []
            for mod in list(data.get("modifiers", []))[:10]:
                if mod.get("resource") not in RESOURCES:
                    continue
                modifiers.append({
                    "resource": mod["resource"],
                    "amount": max(-10, min(10, int(mod.get("amount", 0)))),
                    "sols": max(1, min(5, int(mod.get("sols", 1)))),
                    "label": str(mod.get("label", ""))[:60],
                })

            history = []
            for item in list(data.get("history", []))[:TOTAL_SOLS]:
                history.append({
                    "sol": int(item["sol"]),
                    "event_id": str(item["event_id"]),
                    "choice_id": str(item["choice_id"]),
                })

            log = [str(line)[:240] for line in list(data.get("log", []))[-MAX_LOG_LINES:]]

            return cls(
                sol=sol,
                power=clamp(data.get("power", START_LEVEL)),
                oxygen=clamp(data.get("oxygen", START_LEVEL)),
                shielding=clamp(data.get("shielding", START_LEVEL)),
                science=max(0, min(999, int(data.get("science", 0)))),
                difficulty=difficulty,
                status=status,
                reason=str(data.get("reason", ""))[:240],
                event_queue=queue,
                modifiers=modifiers,
                log=log,
                history=history,
            )
        except (TypeError, KeyError, AttributeError):
            raise ValueError("The game state could not be read.")

    def to_dict(self):
        """Plain dictionary for JSON. Includes helpful extras for the UI."""
        return {
            "sol": self.sol,
            "total_sols": TOTAL_SOLS,
            "power": self.power,
            "oxygen": self.oxygen,
            "shielding": self.shielding,
            "science": self.science,
            "difficulty": self.difficulty,
            "difficulty_label": DIFFICULTIES[self.difficulty]["label"],
            "status": self.status,
            "reason": self.reason,
            "health": outpost_health(self),
            "current_event": self.current_event_id,
            "event_queue": list(self.event_queue),
            "modifiers": [dict(m) for m in self.modifiers],
            "log": list(self.log),
            "history": [dict(h) for h in self.history],
        }

    # -- helpers ---------------------------------------------------------------
    @property
    def current_event_id(self):
        if self.status != "playing":
            return None
        return self.event_queue[self.sol - 1]

    def resources(self):
        return {name: getattr(self, name) for name in RESOURCES}

    def change(self, resource, amount):
        setattr(self, resource, clamp(getattr(self, resource) + amount))

    def add_log(self, text):
        self.log.append(text)
        del self.log[:-MAX_LOG_LINES]


def outpost_health(state):
    """A friendly traffic-light summary based on the lowest resource."""
    lowest = min(state.resources().values())
    if state.status == "lost":
        return {"level": "critical", "label": "Mission over"}
    if state.status == "won":
        return {"level": "good", "label": "Mission complete"}
    if lowest >= 55:
        return {"level": "good", "label": "All systems go"}
    if lowest >= 30:
        return {"level": "caution", "label": "Keep an eye on things"}
    if lowest >= 15:
        return {"level": "danger", "label": "Danger! Something is low"}
    return {"level": "critical", "label": "Emergency!"}


def tick(state):
    """End-of-sol upkeep. Returns what changed, as {resource: number}.

    Every sol the base uses power and oxygen and the shield wall wears down.
    Lasting effects (modifiers) from earlier choices are applied here too, and
    counted down until they run out.
    """
    changes = dict(DIFFICULTIES[state.difficulty]["upkeep"])
    still_active = []
    for mod in state.modifiers:
        changes[mod["resource"]] += mod["amount"]
        mod["sols"] -= 1
        if mod["sols"] > 0:
            still_active.append(mod)
    state.modifiers = still_active

    for resource, amount in changes.items():
        state.change(resource, amount)
    return changes


def apply_choice(state, choice_id):
    """Apply the player's choice to the current event.

    Returns a dictionary describing what happened. Raises ValueError for a
    bad choice or when the game is already over.
    """
    if state.status != "playing":
        raise ValueError("This mission is already over. Start a new one!")
    event = event_data.get_event(state.current_event_id)
    choice = event_data.get_choice(event["id"], choice_id)
    if choice is None:
        raise ValueError("That choice is not part of this event.")

    for resource in RESOURCES:
        state.change(resource, choice["effects"].get(resource, 0))
    state.science = max(0, state.science + choice["effects"].get("science", 0))

    modifier = choice.get("modifier")
    if modifier:
        state.modifiers.append(dict(modifier))

    state.history.append({"sol": state.sol, "event_id": event["id"], "choice_id": choice["id"]})
    state.add_log("Sol {}: {} - you chose \"{}\".".format(state.sol, event["title"], choice["label"]))
    return {"event": event, "choice": choice}


def check_game_over(state):
    """Set state.status to 'lost' if any resource has run out.

    Returns True when the game has ended in a loss.
    """
    if state.status == "lost":
        return True
    for resource in RESOURCES:
        if getattr(state, resource) <= MIN_LEVEL:
            state.status = "lost"
            state.reason = LOSS_MESSAGES[resource]
            state.add_log("Sol {}: {}".format(state.sol, state.reason))
            return True
    return False


def describe_modifier(modifier):
    """Plain-English description of a lasting effect, or None."""
    if not modifier:
        return None
    amount = modifier["amount"]
    return "{} {}{} each sol for {} sol{}".format(
        RESOURCE_INFO[modifier["resource"]]["label"],
        "+" if amount > 0 else "", amount,
        modifier["sols"], "" if modifier["sols"] == 1 else "s")


def mission_comparison(state):
    """Describe the finished mission. The first matching rule wins:

    1. Lost game                              -> learning_run
    2. Science >= 30, all meters >= 40        -> research_station
    3. Science >= 30, any meter < 40          -> dedicated_research_mission
    4. Science < 10,  all meters >= 40        -> tech_demo
    5. Anything else                          -> general_outpost
    """
    lowest = min(state.resources().values())
    if state.status == "lost":
        return {"kind": "learning_run",
                "text": "Learning run: the outpost did not make it this time, but every "
                        "problem you met teaches you something for your next mission."}
    if state.science >= SCIENCE_GOAL_COMPARE and lowest >= HEALTHY_COMPARE:
        return {"kind": "research_station",
                "text": "Research station: lots of science and every system stayed healthy."}
    if state.science >= SCIENCE_GOAL_COMPARE:
        return {"kind": "dedicated_research_mission",
                "text": "Dedicated research mission with crew trade-offs: lots of science, "
                        "but at least one system ran low."}
    if state.science < TECH_DEMO_SCIENCE and lowest >= HEALTHY_COMPARE:
        return {"kind": "tech_demo",
                "text": "Tech demo: the outpost systems stayed healthy, with little time "
                        "left over for science."}
    return {"kind": "general_outpost",
            "text": "General outpost: a balanced mix of keeping the crew safe and doing "
                    "some science."}


def play_turn(state, choice_id):
    """Run one full sol: choice, upkeep, game-over checks, next sol.

    Returns a result dictionary for the browser to display.
    """
    before = state.resources()
    science_before = state.science
    applied = apply_choice(state, choice_id)
    event, choice = applied["event"], applied["choice"]
    later_detail = describe_modifier(choice.get("modifier"))
    upkeep = {}

    if not check_game_over(state):
        upkeep = tick(state)
        if not check_game_over(state):
            state.add_log("Sol {} ends. Upkeep used power, air and shielding.".format(state.sol))
            if state.sol >= TOTAL_SOLS:
                state.status = "won"
                state.reason = "You kept the outpost running for all {} sols!".format(TOTAL_SOLS)
                state.add_log(state.reason)
            else:
                state.sol += 1

    after = state.resources()
    effects = dict(choice["effects"])
    return {
        "event_title": event["title"],
        "event_icon": event["icon"],
        "choice_label": choice["label"],
        "text": choice["result"],
        "choice_effects": effects,
        "upkeep": upkeep,
        "net": {name: after[name] - before[name] for name in RESOURCES},
        "science_change": state.science - science_before,
        "later_effect": choice["modifier"]["label"] if choice.get("modifier") else None,
        "later_detail": later_detail,
        "facts": facts_for(event["facts"]),
    }


def build_report(state):
    """Final mission report with rating, choices made and a learning summary."""
    won = state.status == "won"
    low_resource = min(state.resources().values())

    stars = 0
    if won:
        stars = 1
        if low_resource >= HEALTHY_LEVEL:
            stars += 1
        if state.science >= SCIENCE_GOAL:
            stars += 1

    titles = {
        3: "Moon Base Commander",
        2: "Flight Engineer",
        1: "Junior Astronaut",
        0: "Astronaut in Training",
    }
    if won:
        headline = "Mission complete!"
        message = "Your crew lived through all {} sols on the Moon.".format(TOTAL_SOLS)
    else:
        headline = "Mission ended early"
        message = state.reason or "The outpost ran into trouble."

    tips = []
    if not won:
        tips.append("Try watching the lowest bar. Fixing the smallest resource first often saves a mission.")
    if state.science < SCIENCE_GOAL:
        tips.append("Look for choices that give science when your bars are healthy. Research earns stars!")
    if won and low_resource < HEALTHY_LEVEL:
        tips.append("You made it, but one bar got very low. Next time try to balance all three.")
    if won and stars == 3:
        tips.append("Perfect balance of safety and science. Can you do it again with a different event order?")

    choices_made = []
    lessons = []
    for entry in state.history:
        event = event_data.get_event(entry["event_id"])
        choice = event_data.get_choice(entry["event_id"], entry["choice_id"])
        if not event or not choice:
            continue
        choices_made.append({
            "sol": entry["sol"],
            "icon": event["icon"],
            "event_title": event["title"],
            "choice_label": choice["label"],
        })
        lessons.append({
            "icon": event["icon"],
            "event_title": event["title"],
            "lesson": event["lesson"],
            "facts": facts_for(event["facts"]),
        })

    return {
        "won": won,
        "headline": headline,
        "message": message,
        "stars": stars,
        "title": titles[stars],
        "difficulty": state.difficulty,
        "sols_completed": TOTAL_SOLS if won else max(0, state.sol - 1),
        "final": state.resources(),
        "science": state.science,
        "choices_made": choices_made,
        "lessons": lessons,
        "tips": tips,
        "comparison": mission_comparison(state),
    }


def simulate_difficulty(difficulty, trials=1000):
    """MANUAL TESTING ONLY: play random choices and report the averages.

    Example (from the project folder):
        python -c "from game.engine import simulate_difficulty as s; print(s('hard'))"

    Returns win_rate (0 to 1) and the average final power, oxygen, shielding and
    science over ALL trials (a lost game counts its final values, often 0).
    """
    import random

    if difficulty not in DIFFICULTIES:
        raise ValueError("Difficulty must be easy, normal or hard.")
    if trials < 1:
        raise ValueError("trials must be at least 1.")

    rng = random.Random()
    wins = 0
    totals = {"power": 0, "oxygen": 0, "shielding": 0, "science": 0}
    for _ in range(trials):
        state = GameState.new(rng, difficulty)
        while state.status == "playing":
            event = event_data.get_event(state.current_event_id)
            play_turn(state, rng.choice(event["choices"])["id"])
        wins += 1 if state.status == "won" else 0
        for name in RESOURCES:
            totals[name] += getattr(state, name)
        totals["science"] += state.science

    return {
        "difficulty": difficulty,
        "trials": trials,
        "win_rate": wins / trials,
        "avg_power": totals["power"] / trials,
        "avg_oxygen": totals["oxygen"] / trials,
        "avg_shielding": totals["shielding"] / trials,
        "avg_science": totals["science"] / trials,
    }
