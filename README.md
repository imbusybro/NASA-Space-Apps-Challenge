# Junior Astronaut Mission Trainer

A browser game for kids aged 7-12, made for the NASA Space Apps Challenge.
You manage a lunar outpost for **10 sols** (mission days) and keep three meters
above zero:

| Meter | What it does |
|-------|--------------|
| Power | Runs lights, heaters and air machines |
| Oxygen | What the crew breathes |
| Shielding | Blocks harmful space radiation |

Each sol brings one event (solar flares, radiation storms, a clogged air filter,
dusty solar panels, rationing and more). **Every choice helps one thing and costs
another.** At the end you get a mission report, a star rating, and a learning
summary of the real NASA science behind each event.

## Run it

You need Python 3.9 or newer.

```bash
# 1. (optional but tidy) make a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. install the only two packages needed
pip install -r requirements.txt

# 3. start the game
python app.py
```

Open **http://localhost:5000** in your browser and press **Launch the mission**.

## How to play

1. Read the event, then pick one of the choices.
2. The arrows on each button show what changes: ▲ helps, ▼ costs (more arrows = bigger change).
3. After you choose, you see exactly what changed, plus the **sol upkeep**: every sol the
   outpost automatically uses 5 power, 5 oxygen and 4 shielding.
4. Read the **NASA fact** cards, then start the next sol.
5. If any meter hits **0** the mission ends. Survive all 10 sols to win.

Difficulty (chosen on the first screen, kept on restart): Easy starts at 85 with upkeep 4/4/3, Normal starts at 75 with 5/5/4, Hard starts at 65 with 6/6/5.

Stars: ★ for finishing, ★★ if every meter ends at 20 or more, ★★★ if you also earn 25+ science points.

## Project layout

```
app.py              Flask server and the four routes
game/engine.py      GameState, tick(), apply_choice(), check_game_over(), report
game/events.py      The 10 events and their choices
game/data.py        NASA facts with dates, sources and links
templates/index.html  Game page
static/style.css    Space theme, responsive layout
static/game.js      Game screens (plain JavaScript, no libraries)
```

## API

All responses are JSON. The server stores nothing: the browser sends the whole game
state with every choice.

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | The game page |
| `/api/start` | GET or POST | New game. Optional `{"difficulty": "easy|normal|hard"}`. Returns `state` and the first `event` |
| `/api/choose` | POST | Body: `{"state": {...}, "choice_id": "shelter"}`. Returns new `state`, `result`, `next_event`, and a `report` when the game ends |
| `/health` | GET | Returns `{"status":"ok"}` for hosting checks |
| `/api/about` | GET | Data sources, every NASA fact, glossary and a disclaimer |

Try it from a terminal:

```bash
curl -s http://localhost:5000/api/start
```

## About the NASA data

The NASA facts in `game/data.py` come from three areas:

* **DONKI** (NASA's space weather database): solar flare classes and timing, the May 2024
  geomagnetic storm, the August 1972 solar particle event.
* **OSDR** (Open Science Data Repository): space biology and health, including the Twins Study,
  exercise and bone loss, and plants grown on the ISS.
* **Artemis and Mars/Moon research**: Artemis I radiation mannequins (2022), LCROSS (2009) and SOFIA
  (2020) water discoveries, MOXIE oxygen on Mars (2021-2023), Curiosity radiation measurements,
  CHAPEA (2023-2024), Apollo 13 and Apollo 17 lessons, and ISS water recycling (2023).

Each fact lists its **date** and **source** and links to an official NASA or NOAA page.
The links point to NASA landing pages, so use the site search there to find the original
articles. The game's numbers (meters 0-100, upkeep, science points) are **invented for play**
and are not real measurements. Time is also sped up: real Moon days last about 29.5 Earth days.

Before presenting, re-check each fact against its source. Edit `game/data.py` to fix or add facts.

## Changing the game

* **Difficulty**: edit `DAILY_UPKEEP`, `START_LEVEL` and the star goals at the top of `game/engine.py`.
* **New event**: add a dictionary to `EVENTS` in `game/events.py` (copy an existing one). Give each
  choice `effects` for `power`, `oxygen`, `shielding` and `science`, and list fact ids from
  `game/data.py` in `facts`. Keep exactly 10 events (one per sol) or change `TOTAL_SOLS`.
* **New fact**: add an entry to `_FACT_LIST` in `game/data.py` with `id`, `group`, `title`, `text`,
  `date`, `source` and `url`.

## Deployment

`python app.py` listens on `0.0.0.0` and reads two optional environment variables:
`PORT` (default `5000`) and `FLASK_DEBUG` (`1` turns debug mode on; off by default).
`/health` returns `{"status":"ok"}` for hosting health checks.
