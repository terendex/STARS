// The projector page (/timer): the countdown, large, with no controls. It plays
// the music (assets/music.js) when the Mission Clock page has "Projector page"
// chosen for music, once someone has clicked the page to allow sound.
(() => {
  const $ = (id) => document.getElementById(id);
  const label = $("label");
  const time = $("time");
  const fill = $("fill");
  const note = $("note");
  const scores = $("scores");
  const clockMain = document.querySelector("main.clock");

  const pad = (n) => String(n).padStart(2, "0");
  const hms = (s) => {
    s = Math.max(0, Math.ceil(s));
    return `${pad(Math.floor(s / 3600))}:${pad(Math.floor((s % 3600) / 60))}:${pad(s % 60)}`;
  };
  const clockTime = (unix) => {
    const d = new Date(unix * 1000);
    return `${pad(d.getHours())}:${pad(d.getMinutes())}`;
  };

  let clock = null;
  let offset = 0;
  const now = () => Date.now() / 1000 + offset;

  const music = window.StarsMusic({
    assets: window.STARS_ASSETS || "/plugins/stars/assets/",
    now,
    here: "projector",
    askEarly: true,
    panel: $("music"),
    title: $("music-title"),
    soundButton: $("arm"),
    playButton: $("music-play"),
    embed: $("spotify"),
  });
  $("arm").addEventListener("click", () => music.arm());
  $("skip").addEventListener("click", () => music.skip());

  function render() {
    let state = clock ? clock.state : "loading";
    if (state === "running" && clock.end - now() <= 0) state = "ended";
    let text = "--:--:--";
    let heading = label.textContent;
    let detail = "";
    let mood = "idle";
    let width = 0;

    if (state === "standby") {
      heading = "Starting soon";
      text = hms(clock.duration);
      detail = "The challenges open when the clock starts";
    } else if (state === "scheduled") {
      heading = "Starts in";
      text = hms(clock.start - now());
      detail = `Starts at ${clockTime(clock.start)}`;
    } else if (state === "running") {
      const left = clock.end - now();
      heading = "Time left";
      text = hms(left);
      detail = `Ends at ${clockTime(clock.end)}`;
      width = Math.max(0, Math.min(100, (left / Math.max(1, clock.end - clock.start)) * 100));
      mood = left <= 60 ? "stop" : left <= 600 ? "warn" : "run";
    } else if (state === "ended") {
      heading = "Time's up";
      text = "00:00:00";
      detail = "Flag submissions are closed";
      mood = "stop";
    } else if (state === "intermission") {
      heading = "Scores";
      text = hms(clock.left || 0);
      detail = "Timer paused";
    } else if (state === "open") {
      heading = "No time limit";
    }

    showScores(state === "intermission", clock ? clock.left : 0);
    if (label.textContent !== heading) label.textContent = heading;
    if (time.textContent !== text) time.textContent = text;
    if (note.textContent !== detail) note.textContent = detail;
    fill.style.width = `${width}%`;
    document.body.className = mood;
  }

  async function poll() {
    try {
      const reply = await fetch("/stars/timer/state", { cache: "no-store", credentials: "same-origin" });
      const next = await reply.json();
      offset = next.now - Date.now() / 1000;
      clock = next;
      music.update(next);
    } catch (error) {
      if (!clock) label.textContent = "Can't reach CTFd";
    }
  }

  // --- Scoreboard break ------------------------------------------------------
  // While the clock is paused, the projector shows the standings instead of the
  // countdown. The scores come from /stars/standings, which only answers during
  // a break, so the scoreboard isn't exposed the rest of the time.
  let standingsTimer = null;

  function fillList(id, items) {
    const ol = $(id);
    ol.textContent = "";
    if (!items || !items.length) {
      const li = document.createElement("li");
      li.className = "scores-empty";
      li.textContent = "No scores yet";
      ol.appendChild(li);
      return;
    }
    for (const item of items) {
      const li = document.createElement("li");
      const name = document.createElement("span");
      name.className = "scores-name";
      name.textContent = item.name;
      const score = document.createElement("span");
      score.className = "scores-score";
      score.textContent = `${item.score} pt`;
      li.append(name, score);
      ol.appendChild(li);
    }
  }

  async function pollStandings() {
    try {
      const reply = await fetch("/stars/standings", { cache: "no-store", credentials: "same-origin" });
      const data = await reply.json();
      if (!data.intermission) return;
      const hasTeams = (data.teams || []).length > 0;
      $("scores-teams-col").hidden = !hasTeams;
      if (hasTeams) fillList("scores-teams", data.teams);
      fillList("scores-users", data.users);
    } catch (error) { /* try again on the next poll */ }
  }

  function showScores(on, left) {
    if (on) {
      $("scores-sub").textContent = left ? `Timer paused · ${hms(left)} on the clock` : "Timer paused";
      if (scores.hidden) {
        scores.hidden = false;
        clockMain.hidden = true;
        pollStandings();
      }
      if (!standingsTimer) standingsTimer = setInterval(pollStandings, 5000);
    } else {
      if (!scores.hidden) {
        scores.hidden = true;
        clockMain.hidden = false;
      }
      if (standingsTimer) {
        clearInterval(standingsTimer);
        standingsTimer = null;
      }
    }
  }

  // --- First blood -----------------------------------------------------------
  // The one first solve of the whole event. Announced once, when it happens
  // while this page is open; a page opened afterwards doesn't replay it.
  const blood = $("blood");
  let announced = null;

  // The stinger that plays with the banner. Drop any sound at
  // assets/first-blood.mp3 (the Dota "First Blood!" clip, say) and it plays
  // here; with no file, the banner just shows in silence. Browsers only let it
  // play after someone has clicked the page, which arming the music already does.
  const assets = window.STARS_ASSETS || "/plugins/stars/assets/";
  const bloodSound = new Audio(`${assets}first-blood.mp3`);
  bloodSound.preload = "auto";

  function announce(next) {
    $("blood-team").textContent = next.team;
    $("blood-what").textContent = `solved ${next.challenge} · ${next.category}`;
    document.body.dataset.blood = `${next.team} | ${next.challenge}`;
    try {
      bloodSound.currentTime = 0;
      bloodSound.play().catch(() => {});
    } catch (error) { /* no sound file, or not allowed yet */ }
    blood.hidden = false;
    requestAnimationFrame(() => requestAnimationFrame(() => blood.classList.add("on")));
    setTimeout(() => {
      blood.classList.remove("on");
      setTimeout(() => {
        blood.hidden = true;
        delete document.body.dataset.blood;
      }, 450);
    }, 8000);
  }

  async function pollBlood() {
    try {
      const reply = await fetch("/stars/first-blood", { cache: "no-store", credentials: "same-origin" });
      const next = (await reply.json()).first_blood;
      if (announced === null) {
        // First poll: remember what's already there without announcing it.
        announced = next ? next.id : 0;
        return;
      }
      if (next && next.id !== announced) {
        announced = next.id;
        announce(next);
      }
    } catch (error) {
      // Try again on the next poll.
    }
  }
  pollBlood();
  setInterval(pollBlood, 4000);

  function fullscreen() {
    if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen().catch(() => {});
  }
  $("fullscreen").addEventListener("click", fullscreen);
  addEventListener("keydown", (event) => {
    if (!$("arm").hidden) music.arm();
    if (event.key === "f" || event.key === "F") fullscreen();
    if (event.key === "n" || event.key === "N") music.skip();
  });

  poll();
  setInterval(poll, 3000);
  setInterval(render, 200);
})();
