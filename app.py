"""Junior Astronaut Mission Trainer - Flask server.

Run with:  python app.py   then open  http://localhost:5000
Optional environment variables: PORT (default 5000), FLASK_DEBUG (1 to turn on).

The server stores nothing. The browser sends the whole game state with each
choice, and the server sends back the new state.
"""

import os

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from game import data, engine, events

app = Flask(__name__)
CORS(app)


def error(message, code=400):
    """Return a friendly JSON error."""
    return jsonify({"error": message}), code


@app.route("/")
def index():
    """The game page."""
    return render_template("index.html")


@app.route("/health")
def health():
    """Simple check for hosting services."""
    return jsonify({"status": "ok"})


@app.route("/api/start", methods=["GET", "POST"])
def start():
    """Begin a new mission and return the first event."""
    body = request.get_json(silent=True)
    body = body if isinstance(body, dict) else {}
    difficulty = body.get("difficulty") or request.args.get("difficulty") or engine.DEFAULT_DIFFICULTY
    try:
        state = engine.GameState.new(difficulty=difficulty)
    except (ValueError, TypeError):
        return error("Difficulty must be easy, normal or hard.")
    return jsonify({
        "state": state.to_dict(),
        "event": events.public_event(state.current_event_id),
        "resource_info": engine.RESOURCE_INFO,
        "difficulties": {k: v["label"] for k, v in engine.DIFFICULTIES.items()},
    })


@app.route("/api/choose", methods=["POST"])
def choose():
    """Apply one choice. Body: {"state": {...}, "choice_id": "..."}"""
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return error("Please send JSON with a state and a choice_id.")

    choice_id = body.get("choice_id")
    if not isinstance(choice_id, str):
        return error("choice_id is missing.")

    try:
        state = engine.GameState.from_dict(body.get("state"))
        result = engine.play_turn(state, choice_id)
    except ValueError as problem:
        return error(str(problem))

    playing = state.status == "playing"
    return jsonify({
        "state": state.to_dict(),
        "result": result,
        "next_event": events.public_event(state.current_event_id) if playing else None,
        "report": None if playing else engine.build_report(state),
    })


@app.route("/api/about")
def about():
    """Where the NASA facts come from, plus a small glossary."""
    return jsonify({
        "title": "Junior Astronaut Mission Trainer",
        "disclaimer": data.DISCLAIMER,
        "sources": data.DATA_SOURCES,
        "source_groups": data.SOURCE_GROUPS,
        "facts": data.all_facts_grouped(),
        "glossary": data.GLOSSARY,
    })


@app.errorhandler(404)
def not_found(_):
    return error("Not found.", 404)


@app.errorhandler(500)
def server_problem(_):
    return error("Something went wrong on the server.", 500)


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "").strip().lower() in ("1", "true", "yes", "on")
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=debug)
