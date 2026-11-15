"""The ten mission events.

Every choice has effects on Power, Oxygen, Shielding and Science. A choice
that helps one thing always costs something else, so there is no "free" answer.

effects  : changes applied right away (can be negative or positive)
modifier : optional effect that continues for a few sols, for example
           {"resource": "oxygen", "amount": -3, "sols": 2, "label": "Refilling the air tank"}
facts    : ids from game/data.py shown to the player after they choose
lesson   : one-sentence takeaway for the final learning summary
"""

import random

EVENTS = [
    # 1 ------------------------------------------------------------ SOLAR FLARE
    {
        "id": "solar_flare",
        "title": "Solar Flare Alert!",
        "icon": "☀️",
        "category": "Solar flares",
        "story": "Mission Control is calling! The Sun just let out a big flash of energy called a "
                 "solar flare. Its light reaches the Moon in about 8 minutes, and speedy "
                 "particles might follow. What should the crew do?",
        "facts": ["donki_overview", "flare_classes", "may2024_storm"],
        "lesson": "Solar flares are ranked A, B, C, M and X, and NASA's DONKI database keeps a "
                  "record of them so crews can be warned.",
        "choices": [
            {
                "id": "shelter",
                "label": "Hide in the storm shelter",
                "detail": "Everyone squeezes into the thick-walled shelter.",
                "effects": {"power": -8, "oxygen": -2, "shielding": 8, "science": 0},
                "result": "The crew waited safely in the shelter. The heaters and lights used extra "
                          "power, and no science got done, but everyone is safe.",
            },
            {
                "id": "keep_working",
                "label": "Keep the experiments running",
                "detail": "Science does not stop for a little sunshine!",
                "effects": {"power": 0, "oxygen": 0, "shielding": -14, "science": 9},
                "result": "You collected great flare data, but the crew got a bigger dose of "
                          "radiation and the shield wall took a beating.",
            },
            {
                "id": "regolith_bags",
                "label": "Pile Moon-soil bags on the roof",
                "detail": "Extra soil makes the walls thicker.",
                "effects": {"power": -3, "oxygen": -7, "shielding": 12, "science": 0},
                "result": "Hauling heavy bags is hard work, so the crew breathed lots of air. The "
                          "thick layer of soil now blocks more radiation.",
            },
        ],
    },
    # 2 ------------------------------------------------------- RADIATION STORM
    {
        "id": "radiation_storm",
        "title": "Radiation Storm Warning",
        "icon": "☢️",
        "category": "Radiation",
        "story": "Space weather scouts spotted a cloud of fast particles heading for the Moon. "
                 "There is no magnetic bubble or thick air up here to block them, so your shield "
                 "wall has to do the job.",
        "facts": ["flare_speed", "sep_1972", "artemis1_mare"],
        "lesson": "The Moon has no magnetic field or thick air, so shielding matters. NASA tested "
                  "radiation protection on Artemis I using two mannequins.",
        "choices": [
            {
                "id": "fix_wall",
                "label": "Fix and thicken the shield wall",
                "detail": "A big repair job right now.",
                "effects": {"power": -10, "oxygen": -4, "shielding": 16, "science": 0},
                "result": "Robot arms and tired astronauts patched every crack. The wall is "
                          "much stronger, but the work used lots of power and air.",
            },
            {
                "id": "sleep_pod",
                "label": "Everyone naps in the shielded pod",
                "detail": "Switch off extra gear and rest.",
                "effects": {"power": 4, "oxygen": -6, "shielding": 9, "science": 0},
                "result": "Switching off machines saved power and the pod blocked the particles, "
                          "but a crowded pod used up air quickly.",
            },
            {
                "id": "measure_it",
                "label": "Record the storm with radiation sensors",
                "detail": "Scientists on Earth will love this data!",
                "effects": {"power": -4, "oxygen": 0, "shielding": -8, "science": 8},
                "result": "Your sensors recorded the whole storm, which is a science treasure, "
                          "but the crew had less protection while they worked.",
            },
        ],
    },
    # 3 ---------------------------------------------------- AIR FILTER CLOG
    {
        "id": "air_filter",
        "title": "Air Filter Clog",
        "icon": "🌬️",
        "category": "Life support",
        "story": "Beep, beep! The machine that removes carbon dioxide (the gas we breathe out) "
                 "is clogged. The air feels stuffy and everyone has a headache. You need cleaner "
                 "air soon!",
        "facts": ["apollo13_co2"],
        "lesson": "Life support must clean the air as well as supply oxygen. In 1970, Apollo 13's "
                  "crew and engineers built a filter fix using items on board.",
        "choices": [
            {
                "id": "rebuild",
                "label": "Rebuild the filter from spare parts",
                "detail": "Be creative, like the Apollo 13 team!",
                "effects": {"power": -4, "oxygen": 10, "shielding": -6, "science": 3},
                "result": "Clever engineering! You borrowed wall panels to build a filter. The air "
                          "is fresher and you learned a lot, but the shield wall is thinner.",
            },
            {
                "id": "backup_system",
                "label": "Turn on the backup air system",
                "detail": "It works well but gobbles electricity.",
                "effects": {"power": -14, "oxygen": 16, "shielding": 0, "science": 0},
                "result": "The backup system roared to life and the air is clean again. Your power "
                          "meter dropped a lot, though.",
            },
            {
                "id": "emergency_tank",
                "label": "Open the emergency air tank",
                "detail": "Quick fix, but the tank must be refilled later.",
                "effects": {"power": -2, "oxygen": 20, "shielding": 0, "science": 0},
                "result": "Fresh air poured out right away! Refilling the tank will keep draining "
                          "oxygen over the next two sols.",
                "modifier": {"resource": "oxygen", "amount": -3, "sols": 2,
                             "label": "Refilling the emergency air tank"},
            },
        ],
    },
    # 4 ---------------------------------------------------- OXYGEN MAKER
    {
        "id": "oxygen_maker",
        "title": "The Oxygen-Maker Experiment",
        "icon": "🧪",
        "category": "Research",
        "story": "Your team has a machine like MOXIE, the experiment on NASA's Perseverance rover "
                 "that made oxygen from carbon dioxide on Mars. It uses a LOT of electricity. "
                 "Do you run it?",
        "facts": ["moxie"],
        "lesson": "NASA's MOXIE experiment made oxygen from Mars air in 2021. Making air on "
                  "another world takes a lot of power.",
        "choices": [
            {
                "id": "run_all_day",
                "label": "Run it all day",
                "detail": "Lots of oxygen, lots of power.",
                "effects": {"power": -16, "oxygen": 18, "shielding": 0, "science": 4},
                "result": "The oxygen-maker hummed all day and filled the tanks. The power "
                          "batteries are much lower now.",
            },
            {
                "id": "short_test",
                "label": "Run a short test and record data",
                "detail": "Less air, more learning.",
                "effects": {"power": -6, "oxygen": 8, "shielding": 0, "science": 7},
                "result": "A short test gave you handy numbers about how well the machine works, "
                          "plus a little extra oxygen.",
            },
            {
                "id": "save_power",
                "label": "Leave it off and save power",
                "detail": "Keep the batteries full.",
                "effects": {"power": 8, "oxygen": -3, "shielding": 0, "science": 0},
                "result": "The batteries got a rest, but the crew used up some air and the "
                          "experiment waited for another day.",
            },
        ],
    },
    # 5 ---------------------------------------------------- MOON ICE
    {
        "id": "moon_ice",
        "title": "Moon Ice Expedition",
        "icon": "🧊",
        "category": "Research",
        "story": "Spacecraft and telescopes have found signs of water in the dusty Moon soil, "
                 "especially near the poles. Water could become drinking water and even oxygen "
                 "for future bases. Will you go looking for ice?",
        "facts": ["lcross", "sofia", "artemis_plan"],
        "lesson": "NASA's LCROSS (2009) and SOFIA (2020) found water on the Moon. Water could help "
                  "Artemis explorers live there.",
        "choices": [
            {
                "id": "long_trek",
                "label": "Send the rover on a long trek",
                "detail": "Big discoveries are far away.",
                "effects": {"power": -10, "oxygen": -8, "shielding": -6, "science": 14},
                "result": "The long trek found amazing samples! But the rover drained batteries, "
                          "the suited crew breathed lots of air, and the base was left unprotected.",
            },
            {
                "id": "drill_near",
                "label": "Drill a spot near the base",
                "detail": "A safer, shorter search.",
                "effects": {"power": -8, "oxygen": -2, "shielding": 0, "science": 8},
                "result": "The drill brought up some interesting soil close to home. A decent "
                          "discovery for a medium amount of power.",
            },
            {
                "id": "study_maps",
                "label": "Study satellite maps indoors",
                "detail": "Plan carefully before moving.",
                "effects": {"power": -3, "oxygen": -2, "shielding": 3, "science": 4},
                "result": "You made a smart map of where ice might be. It is not as exciting as "
                          "digging, but it was safe and used little power.",
            },
        ],
    },
    # 6 ---------------------------------------------------- DUSTY PANELS
    {
        "id": "dusty_panels",
        "title": "Dusty Solar Panels",
        "icon": "🌫️",
        "category": "Equipment failure",
        "story": "Moon dust is sharp and sticky! It has covered your solar panels, so they make "
                 "less electricity. Apollo astronauts and Mars rovers had dust troubles too.",
        "facts": ["apollo17_dust", "opportunity_dust"],
        "lesson": "Dust is a real danger to equipment. Apollo crews fought Moon dust, and "
                  "Opportunity lost power in a Mars dust storm.",
        "choices": [
            {
                "id": "spacewalk_brush",
                "label": "Brush the panels on a spacewalk",
                "detail": "Fast and effective, but risky.",
                "effects": {"power": 16, "oxygen": -8, "shielding": -6, "science": 0},
                "result": "The panels are sparkling and power is flowing! The spacewalk used a "
                          "lot of oxygen and left the crew out in the radiation.",
            },
            {
                "id": "robot_brush",
                "label": "Send the cleaning robot",
                "detail": "Slow, so the science robot is busy.",
                "effects": {"power": 10, "oxygen": 0, "shielding": 0, "science": -5},
                "result": "The robot cleaned the panels, but it was the same robot that "
                          "does science work. Some research time was lost.",
            },
            {
                "id": "coating",
                "label": "Spray on dust-repelling coating",
                "detail": "Uses spare shield material, but helps for days.",
                "effects": {"power": 6, "oxygen": 0, "shielding": -8, "science": 0},
                "result": "The coating helps dust slide right off, so the panels will make a bit "
                          "of extra power for a few sols. It used up some shield material.",
                "modifier": {"resource": "power", "amount": 2, "sols": 3,
                             "label": "Clean panels bonus"},
            },
        ],
    },
    # 7 ---------------------------------------------------- RATIONING
    {
        "id": "rationing",
        "title": "Supply Ship Is Late",
        "icon": "🍽️",
        "category": "Rationing",
        "story": "The next supply delivery is delayed. To stretch food and water, you have to "
                 "decide how the crew uses supplies. NASA's Mars Dune Alpha volunteers practised "
                 "tough choices just like this.",
        "facts": ["chapea", "iss_water"],
        "lesson": "Crews must plan for limited supplies. On the ISS, nearly all water is "
                  "recycled, and CHAPEA volunteers practised living with limits.",
        "choices": [
            {
                "id": "strict_rations",
                "label": "Small rations, extra rest",
                "detail": "Calm, quiet crew use less air.",
                "effects": {"power": 4, "oxygen": 8, "shielding": 0, "science": -6},
                "result": "A resting crew breathes slower and uses less energy. But tired "
                          "astronauts did less science today.",
            },
            {
                "id": "hot_meals",
                "label": "Cook hot meals for team spirit",
                "detail": "Happy astronauts do great work.",
                "effects": {"power": -8, "oxygen": -2, "shielding": 0, "science": 8},
                "result": "A hot dinner lifted everyone's mood and the team did excellent "
                          "research. The stove used plenty of power.",
            },
            {
                "id": "water_recycler",
                "label": "Boost the water recycler",
                "detail": "Reuse nearly all the water, like on the ISS.",
                "effects": {"power": -6, "oxygen": 6, "shielding": 0, "science": 2},
                "result": "The recycler turned used water into clean water, and made some "
                          "oxygen too. It took extra electricity to run.",
            },
        ],
    },
    # 8 ---------------------------------------------------- LUNAR NIGHT
    {
        "id": "lunar_night",
        "title": "The Long Lunar Night",
        "icon": "🌑",
        "category": "Power",
        "story": "Night is coming! A full day and night on the Moon lasts about 29.5 Earth days, "
                 "so the dark can last about two weeks and the solar panels go to sleep. It also "
                 "gets freezing cold. (In training, we speed up the clock!)",
        "facts": ["moon_day", "lro_cold"],
        "lesson": "A Moon night lasts about two weeks and it gets extremely cold, so bases must "
                  "store power and stay warm.",
        "choices": [
            {
                "id": "charge_up",
                "label": "Charge the batteries to the max",
                "detail": "Pause the experiments to charge.",
                "effects": {"power": 14, "oxygen": -4, "shielding": 0, "science": -5},
                "result": "The batteries are packed with energy for the dark. The experiments had "
                          "to wait, and the crew stayed bundled up.",
            },
            {
                "id": "heaters_low",
                "label": "Turn the heaters low and bundle up",
                "detail": "Cold stretches the walls and seals.",
                "effects": {"power": 10, "oxygen": 0, "shielding": -8, "science": 0},
                "result": "Low heat saved lots of electricity, but the cold made some seals "
                          "and shield panels crack.",
            },
            {
                "id": "night_science",
                "label": "Run night-time experiments",
                "detail": "Warm lamps and busy machines.",
                "effects": {"power": -12, "oxygen": -2, "shielding": 0, "science": 9},
                "result": "The experiments in the dark found some really cool results. Your "
                          "batteries paid the price.",
            },
        ],
    },
    # 9 ---------------------------------------------------- FITNESS CHECK
    {
        "id": "fitness_check",
        "title": "Crew Fitness Check",
        "icon": "🏃",
        "category": "Research",
        "story": "In low gravity, muscles and bones get weaker. Astronauts on the ISS exercise "
                 "about two hours every day. The doctor on Earth wants health data from your "
                 "crew, which scientists share in NASA's Open Science Data Repository.",
        "facts": ["bone_loss", "twins_study", "osdr_overview"],
        "lesson": "Exercise protects astronauts' bones and muscles. NASA's Twins Study and the "
                  "OSDR help scientists learn how space changes the body.",
        "choices": [
            {
                "id": "full_workout",
                "label": "Full workout and health tests",
                "detail": "Great data, but it is tiring.",
                "effects": {"power": -8, "oxygen": -8, "shielding": 0, "science": 10},
                "result": "The crew ran, lifted and tested, which gave scientists excellent "
                          "data. Exercise machines used power and breathing used air.",
            },
            {
                "id": "short_workout",
                "label": "Short workout, then repair the walls",
                "detail": "A little exercise and a little work.",
                "effects": {"power": -3, "oxygen": -4, "shielding": 5, "science": 2},
                "result": "A quick workout kept muscles active, and the extra time went into "
                          "repairing the shield wall.",
            },
            {
                "id": "skip_it",
                "label": "Skip exercise and rest",
                "detail": "Saves air and power today.",
                "effects": {"power": 4, "oxygen": 6, "shielding": -4, "science": -4},
                "result": "You saved air and power, but without exercise the crew felt weak and "
                          "slow, so repairs and research suffered.",
            },
        ],
    },
    # 10 ---------------------------------------------------- SPACE GARDEN
    {
        "id": "space_garden",
        "title": "The Space Garden",
        "icon": "🥬",
        "category": "Research",
        "story": "In 2015, ISS astronauts ate lettuce they grew in space! Your crew can plant a "
                 "small garden under glowing lights. Plants make fresh air and tasty food, but "
                 "grow lights need power.",
        "facts": ["veggie_lettuce", "osdr_overview"],
        "lesson": "Growing plants in space, like the ISS lettuce in 2015, helps NASA plan for "
                  "food on long trips. The data is shared through OSDR.",
        "choices": [
            {
                "id": "big_garden",
                "label": "Plant a big garden",
                "detail": "Many plants, many lights.",
                "effects": {"power": -14, "oxygen": 10, "shielding": 0, "science": 8},
                "result": "Green leaves everywhere! The garden gave fresh air and great plant "
                          "data, and it drank lots of electricity.",
            },
            {
                "id": "salad_box",
                "label": "Plant a small salad box",
                "detail": "A few plants, a few lights.",
                "effects": {"power": -5, "oxygen": 4, "shielding": 0, "science": 4},
                "result": "A little salad box now sits by the window. It is not much, but "
                          "it is cheap, and the crew loves it.",
            },
            {
                "id": "storage_wall",
                "label": "Use the garden space for soil-bag storage",
                "detail": "More bags means a thicker wall.",
                "effects": {"power": -2, "oxygen": -3, "shielding": 8, "science": 0},
                "result": "No garden, but your soil bags now add a thicker layer around "
                          "the base.",
            },
        ],
    },
]

_BY_ID = {event["id"]: event for event in EVENTS}


def event_ids():
    """All event ids in their default order."""
    return [event["id"] for event in EVENTS]


def shuffled_event_ids(rng=None):
    """A random order of all events - one event per sol."""
    rng = rng or random
    ids = event_ids()
    rng.shuffle(ids)
    return ids


def get_event(event_id):
    """Return the full event dictionary (including effects) or None."""
    return _BY_ID.get(event_id)


def get_choice(event_id, choice_id):
    """Return the choice dictionary for an event, or None."""
    event = get_event(event_id)
    if not event:
        return None
    for choice in event["choices"]:
        if choice["id"] == choice_id:
            return choice
    return None


def _hint(resource, amount):
    """Turn a number into a simple size (1-3) and direction for the UI."""
    size = 1 if abs(amount) <= 5 else 2 if abs(amount) <= 11 else 3
    return {"resource": resource, "direction": "up" if amount > 0 else "down", "size": size}


def public_event(event_id):
    """Event as sent to the browser: effects are shown as small arrows only.

    Kids see which resources go up or down (and roughly how much) but have to
    work out the best balance themselves. Exact numbers appear afterwards.
    """
    event = get_event(event_id)
    if not event:
        return None
    choices = []
    for choice in event["choices"]:
        hints = [_hint(res, amt) for res, amt in choice["effects"].items() if amt != 0]
        modifier = choice.get("modifier")
        choices.append({
            "id": choice["id"],
            "label": choice["label"],
            "detail": choice["detail"],
            "hints": hints,
            "later": modifier["label"] if modifier else None,
        })
    return {
        "id": event["id"],
        "title": event["title"],
        "icon": event["icon"],
        "category": event["category"],
        "story": event["story"],
        "choices": choices,
    }
