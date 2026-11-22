// The projector page (/timer): the countdown, large, with no controls. It plays
// the music (assets/music.js) when the Mission Clock page has "Projector page"
// chosen for music, once someone has clicked the page to allow sound.
(() => {
  const $ = (id) => document.getElementById(id);
  const label = $("label");
  const time = $("time");
  const fill = $("fill");
  const note = $("note");

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
    } else if (state === "open") {
      heading = "No time limit";
    }

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
