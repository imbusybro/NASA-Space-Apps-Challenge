/* Junior Astronaut Mission Trainer - browser code.
   The server keeps no memory. We keep the game `state` here and send it back
   with every choice. */

(function () {
  "use strict";

  var RES_ORDER = ["power", "oxygen", "shielding"];
  var RES_LABEL = { power: "⚡ Power", oxygen: "🫁 Oxygen", shielding: "🛡️ Shielding" };
  var RES_SPOKEN = { power: "Power", oxygen: "Oxygen", shielding: "Shielding", science: "Science" };
  var RES_ICON = { power: "⚡", oxygen: "🫁", shielding: "🛡️", science: "⭐" };

  var state = null;     // latest game state from the server
  var pending = null;   // what to show after the player reads the result {event, report}
  var aboutLoaded = false;

  function $(id) { return document.getElementById(id); }

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) { node.className = className; }
    if (text !== undefined && text !== null) { node.textContent = text; }
    return node;
  }

  function clear(node) {
    while (node.firstChild) { node.removeChild(node.firstChild); }
  }

  function show(id) { $(id).hidden = false; }
  function hide(id) { $(id).hidden = true; }

  function showScreen(name) {
    ["screen-intro", "screen-game", "screen-report"].forEach(function (id) {
      $(id).hidden = (id !== "screen-" + name);
    });
  }

  function focusHeading(node) {
    node.setAttribute("tabindex", "-1");
    node.focus({ preventScroll: false });
  }

  // ------------------------------------------------------------------ server
  function api(path, body) {
    var options = { method: body ? "POST" : "GET", headers: {} };
    if (body) {
      options.headers["Content-Type"] = "application/json";
      options.body = JSON.stringify(body);
    }
    return fetch(path, options).then(function (response) {
      return response.json().then(function (data) {
        if (!response.ok) { throw new Error(data.error || "Something went wrong."); }
        return data;
      });
    });
  }

  // ------------------------------------------------------------ start / restart
  function selectedDifficulty() {
    var chosen = document.querySelector('input[name="difficulty"]:checked');
    return chosen ? chosen.value : "normal";
  }

  // From the intro screen we read the selector; a restart keeps the current difficulty.
  function startGame(fromIntro) {
    var button = fromIntro ? $("start-btn") : null;
    var difficulty = fromIntro || !state ? selectedDifficulty() : state.difficulty;
    if (button) { button.disabled = true; }
    api("/api/start", { difficulty: difficulty }).then(function (data) {
      state = data.state;
      pending = null;
      hide("intro-error");
      showScreen("game");
      renderResources(state);
      renderTrack(state.sol, state.status);
      renderEvent(data.event);
      window.scrollTo(0, 0);
    }).catch(function (err) {
      var box = $("intro-error");
      box.textContent = "Could not start the mission: " + err.message + " Is the server running?";
      box.hidden = false;
      if (!fromIntro) { window.alert(box.textContent); }
    }).then(function () {
      if (button) { button.disabled = false; }
    });
  }

  // --------------------------------------------------------------- resources
  function levelFor(value) {
    if (value >= 55) { return "good"; }
    if (value >= 30) { return "caution"; }
    if (value >= 15) { return "danger"; }
    return "critical";
  }

  function renderResources(s) {
    RES_ORDER.forEach(function (name) {
      var value = s[name];
      var level = levelFor(value);
      var box = document.querySelector('.res[data-res="' + name + '"]');
      box.setAttribute("data-level", level);
      $("val-" + name).textContent = value;
      $("fill-" + name).style.width = value + "%";
      box.querySelector(".bar").setAttribute("aria-valuenow", value);
      var note = "";
      if (level === "danger") { note = "Getting low!"; }
      if (level === "critical") { note = "Almost empty!"; }
      $("note-" + name).textContent = note;
    });
    $("val-science").textContent = s.science;
    $("difficulty-badge").textContent = "Difficulty: " + (s.difficulty_label || "Normal");

    var pill = $("status-pill");
    pill.setAttribute("data-level", s.health.level);
    $("status-text").textContent = s.health.label;

    var effects = $("effects-list");
    clear(effects);
    s.modifiers.forEach(function (mod) {
      var sign = mod.amount > 0 ? "+" : "";
      effects.appendChild(el("li", null,
        mod.label + ": " + RES_SPOKEN[mod.resource] + " " + sign + mod.amount +
        " each sol for " + mod.sols + " more sol" + (mod.sols === 1 ? "" : "s")));
    });
    $("effects").hidden = s.modifiers.length === 0;

    var log = $("log-list");
    clear(log);
    s.log.forEach(function (line) { log.appendChild(el("li", null, line)); });
  }

  function renderTrack(sol, status) {
    var total = state.total_sols;
    $("sol-now").textContent = sol;
    $("sol-total").textContent = total;

    var stops = $("track-stops");
    clear(stops);
    for (var i = 1; i <= total; i++) {
      var li = el("li", null, String(i));
      if (status === "won" || i < sol) { li.className = "done"; }
      else if (i === sol && status === "playing") { li.className = "current"; li.setAttribute("aria-current", "step"); }
      stops.appendChild(li);
    }

    var progress = status === "won" ? 1 : (sol - 1) / (total - 1);
    $("astronaut").style.left = (2 + progress * 88) + "%";
  }

  // ------------------------------------------------------------------- event
  function hintText(hint) {
    var amount = hint.size === 3 ? "a lot" : hint.size === 2 ? "some" : "a little";
    return RES_SPOKEN[hint.resource] + (hint.direction === "up" ? " goes up " : " goes down ") + amount;
  }

  function renderEvent(event) {
    hide("result-card");
    show("event-card");

    $("event-icon").textContent = event.icon;
    $("event-cat").textContent = event.category;
    $("event-title").textContent = event.title;
    $("event-story").textContent = event.story;

    var wrap = $("choices");
    clear(wrap);
    event.choices.forEach(function (choice) {
      var button = el("button", "choice");
      button.type = "button";
      button.appendChild(el("span", "choice-label", choice.label));
      button.appendChild(el("span", "choice-detail", choice.detail));

      var hints = el("span", "hints");
      choice.hints.forEach(function (hint) {
        var arrows = new Array(hint.size + 1).join(hint.direction === "up" ? "▲" : "▼");
        var tag = el("span", "hint " + hint.direction, RES_ICON[hint.resource] + " " + arrows);
        tag.setAttribute("aria-label", hintText(hint));
        tag.title = hintText(hint);
        hints.appendChild(tag);
      });
      if (choice.later) {
        var later = el("span", "hint later", "⏳ Lasts a few sols");
        later.title = choice.later;
        hints.appendChild(later);
      }
      button.appendChild(hints);

      button.addEventListener("click", function () { choose(choice.id); });
      wrap.appendChild(button);
    });

    var old = $("event-error");
    if (old) { old.parentNode.removeChild(old); }
    focusHeading($("event-title"));
  }

  function choose(choiceId) {
    var buttons = document.querySelectorAll("#choices .choice");
    buttons.forEach(function (b) { b.disabled = true; });

    api("/api/choose", { state: state, choice_id: choiceId }).then(function (data) {
      state = data.state;
      pending = { event: data.next_event, report: data.report };
      renderResources(state);
      renderResult(data.result, state);
    }).catch(function (err) {
      buttons.forEach(function (b) { b.disabled = false; });
      var box = $("event-error");
      if (!box) {
        box = el("p", "small");
        box.id = "event-error";
        box.setAttribute("role", "alert");
        $("event-card").appendChild(box);
      }
      box.textContent = "Oops: " + err.message + " Please try again.";
    });
  }

  // ------------------------------------------------------------------ result
  function signed(n) { return n > 0 ? "+" + n : String(n); }

  function deltaCell(value, extraClass) {
    var cls = value > 0 ? "plus" : value < 0 ? "minus" : "zero";
    return el("td", cls + (extraClass ? " " + extraClass : ""), value === 0 ? "0" : signed(value));
  }

  function createFactCard(fact) {
    var card = el("div", "fact");
    card.appendChild(el("h4", null, "NASA fact: " + fact.title));
    card.appendChild(el("p", null, fact.text));

    var meta = el("dl");
    meta.appendChild(el("dt", null, "When: "));
    meta.appendChild(el("dd", null, fact.date));
    meta.appendChild(el("dt", null, "Source: "));
    meta.appendChild(el("dd", null, fact.source));
    var link = el("a", null, "Check it yourself");
    link.href = fact.url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    var dd = el("dd");
    dd.appendChild(link);
    meta.appendChild(dd);
    card.appendChild(meta);
    return card;
  }

  function renderResult(result, s) {
    hide("event-card");
    show("result-card");

    $("result-cat").textContent = result.event_icon + " Sol result";
    $("result-title").textContent = result.event_title;
    $("result-choice").textContent = "You chose: " + result.choice_label;
    $("result-text").textContent = result.text;

    var body = $("deltas-body");
    clear(body);
    RES_ORDER.forEach(function (name) {
      var row = el("tr");
      row.appendChild(el("td", null, RES_LABEL[name]));
      row.appendChild(deltaCell(result.choice_effects[name] || 0));
      row.appendChild(deltaCell(result.upkeep[name] || 0));
      row.appendChild(deltaCell(result.net[name], "total"));
      body.appendChild(row);
    });
    var sci = el("tr");
    sci.appendChild(el("td", null, "⭐ Science"));
    sci.appendChild(deltaCell(result.choice_effects.science || 0));
    sci.appendChild(el("td", "zero", "0"));
    sci.appendChild(deltaCell(result.science_change, "total"));
    body.appendChild(sci);

    var later = $("result-later");
    if (result.later_effect) {
      later.textContent = "⏳ Still going: " + result.later_effect +
        (result.later_detail ? " (" + result.later_detail + ")" : "") + ".";
      later.hidden = false;
    } else {
      later.hidden = true;
    }

    var facts = $("result-facts");
    clear(facts);
    result.facts.forEach(function (fact) { facts.appendChild(createFactCard(fact)); });

    var next = $("next-btn");
    if (s.status === "playing") {
      next.textContent = "Start sol " + s.sol;
    } else {
      next.textContent = "See my mission report";
    }
    focusHeading($("result-title"));
  }

  function nextStep() {
    if (!pending) { return; }
    if (pending.report) {
      renderTrack(state.sol, state.status);
      renderReport(pending.report);
      showScreen("report");
    } else {
      renderTrack(state.sol, state.status);
      renderEvent(pending.event);
    }
    pending = null;
    window.scrollTo(0, 0);
  }

  // ------------------------------------------------------------------ report
  function renderReport(report) {
    $("report-kicker").textContent = report.won ? "🚀 Mission report" : "🛰️ Mission report";
    $("report-headline").textContent = report.headline;
    $("report-message").textContent = report.message;

    var stars = $("report-stars");
    clear(stars);
    for (var i = 1; i <= 3; i++) {
      stars.appendChild(el("span", i <= report.stars ? "" : "off", "★"));
    }
    stars.setAttribute("aria-label", report.stars + " out of 3 stars");
    $("report-rank").textContent = "Rank: " + report.title +
      " (" + report.sols_completed + " of " + state.total_sols + " sols completed)";

    var comparison = $("report-comparison");
    var comparisonText = report.comparison && report.comparison.text;
    comparison.textContent = comparisonText || "";
    comparison.hidden = !comparisonText;

    var grid = $("final-grid");
    clear(grid);
    RES_ORDER.concat(["science"]).forEach(function (name) {
      var box = el("div", "final-box");
      box.setAttribute("data-res", name);
      var value = name === "science" ? report.science : report.final[name];
      box.appendChild(el("strong", null, String(value)));
      box.appendChild(el("span", null, RES_ICON[name] + " " + RES_SPOKEN[name]));
      grid.appendChild(box);
    });

    var choices = $("choice-list");
    clear(choices);
    report.choices_made.forEach(function (c) {
      choices.appendChild(el("li", null, "Sol " + c.sol + ": " + c.icon + " " + c.event_title + " - " + c.choice_label));
    });

    var lessons = $("lesson-list");
    clear(lessons);
    report.lessons.forEach(function (lesson) {
      var box = el("div", "lesson");
      box.appendChild(el("p", null, lesson.icon + " " + lesson.event_title + ": " + lesson.lesson));
      var details = el("details");
      details.appendChild(el("summary", null, "See the NASA facts (" + lesson.facts.length + ")"));
      lesson.facts.forEach(function (fact) { details.appendChild(createFactCard(fact)); });
      box.appendChild(details);
      lessons.appendChild(box);
    });

    var tips = $("tips-list");
    clear(tips);
    report.tips.forEach(function (tip) { tips.appendChild(el("li", null, tip)); });
    $("tips").hidden = report.tips.length === 0;

    focusHeading($("report-headline"));
  }

  // ------------------------------------------------------------------- about
  function renderAbout(data) {
    var body = $("about-body");
    clear(body);
    body.appendChild(el("p", null, data.disclaimer));

    body.appendChild(el("h3", null, "Where the facts come from"));
    var sources = el("dl");
    data.sources.forEach(function (src) {
      var dt = el("dt");
      var link = el("a", null, src.name);
      link.href = src.url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      dt.appendChild(link);
      sources.appendChild(dt);
      sources.appendChild(el("dd", null, src.description));
    });
    body.appendChild(sources);

    Object.keys(data.facts).forEach(function (group) {
      body.appendChild(el("h3", null, data.source_groups[group]));
      data.facts[group].forEach(function (fact) { body.appendChild(createFactCard(fact)); });
    });

    body.appendChild(el("h3", null, "Space words"));
    var words = el("dl");
    data.glossary.forEach(function (item) {
      words.appendChild(el("dt", null, item.word));
      words.appendChild(el("dd", null, item.meaning));
    });
    body.appendChild(words);
  }

  function openAbout() {
    var dialog = $("about-dialog");
    if (typeof dialog.showModal === "function") { dialog.showModal(); }
    else { dialog.setAttribute("open", ""); }

    if (aboutLoaded) { return; }
    api("/api/about").then(function (data) {
      renderAbout(data);
      aboutLoaded = true;
    }).catch(function (err) {
      $("about-body").textContent = "Could not load the NASA data page: " + err.message;
    });
  }

  function closeAbout() {
    var dialog = $("about-dialog");
    if (typeof dialog.close === "function") { dialog.close(); }
    else { dialog.removeAttribute("open"); }
  }

  // ------------------------------------------------------------------- wiring
  $("start-btn").addEventListener("click", function () { startGame(true); });
  $("restart-btn").addEventListener("click", function () { startGame(false); });
  $("restart-mid-btn").addEventListener("click", function () {
    if (window.confirm("Restart the mission from sol 1?")) { startGame(false); }
  });
  $("next-btn").addEventListener("click", nextStep);
  $("about-btn").addEventListener("click", openAbout);
  $("about-btn-2").addEventListener("click", openAbout);
  $("about-close").addEventListener("click", closeAbout);
  $("about-dialog").addEventListener("click", function (event) {
    if (event.target === $("about-dialog")) { closeAbout(); }   // click on the dark backdrop
  });
})();
