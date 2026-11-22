// STARS mission clock: the strip along the bottom of every player page.
// It asks the server for the clock every 10 seconds and ticks on its own in
// between. When the organizer starts the clock, the challenges page reloads so
// the board appears; when it reaches zero, the page says so and reloads, and
// CTFd then shows that the CTF has ended. CTFd does the actual locking, so
// none of this is needed to keep anyone out.
(() => {
  if (window.__starsClock) return;
  window.__starsClock = true;
  const path = location.pathname;
  if (path.startsWith("/timer") || path.startsWith("/admin")) return;

  const style = document.createElement("style");
  style.textContent = `
    #stars-clock { position: fixed; left: 0; right: 0; bottom: 0; z-index: 1040;
      display: none; align-items: center; gap: 14px; padding: 8px 16px;
      background: rgba(1, 8, 4, 0.95); border-top: 1px solid rgba(57, 255, 122, 0.35);
      box-shadow: 0 -6px 24px rgba(0, 255, 100, 0.12);
      color: #39ff7a; text-shadow: 0 0 6px rgba(57, 255, 122, 0.6);
      font: 600 14px/1.25 "Cascadia Mono", Consolas, "Courier New", monospace; letter-spacing: 0.05em; }
    #stars-clock.sc-on { display: flex; }
    #stars-clock .sc-tag { opacity: 0.75; white-space: nowrap; }
    #stars-clock .sc-time { font-size: 21px; font-weight: 700; font-variant-numeric: tabular-nums; white-space: nowrap; }
    #stars-clock .sc-msg { opacity: 0.85; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    #stars-clock .sc-cursor { animation: sc-blink 1s steps(1) infinite; }
    #stars-clock .sc-bar { flex: 1; min-width: 60px; height: 6px; background: rgba(57, 255, 122, 0.12);
      border: 1px solid rgba(57, 255, 122, 0.3); }
    #stars-clock .sc-fill { height: 100%; width: 0; background: currentColor; box-shadow: 0 0 8px currentColor; transition: width 0.25s linear; }
    #stars-clock.sc-warn { color: #ffb000; text-shadow: 0 0 6px rgba(255, 176, 0, 0.6); border-top-color: rgba(255, 176, 0, 0.5); }
    #stars-clock.sc-crit, #stars-clock.sc-over { color: #ff3b3b; text-shadow: 0 0 8px rgba(255, 59, 59, 0.8); border-top-color: rgba(255, 59, 59, 0.6); }
    #stars-clock.sc-crit .sc-time { animation: sc-pulse 1s ease-in-out infinite; }
    body.sc-pad { padding-bottom: 52px; }
    body.sc-pad .footer { margin-bottom: 46px; }
    #stars-timeup { position: fixed; inset: 0; z-index: 2000; display: flex; flex-direction: column;
      align-items: center; justify-content: center; gap: 18px; background: rgba(0, 0, 0, 0.9);
      color: #ff3b3b; text-shadow: 0 0 18px rgba(255, 59, 59, 0.8); text-align: center; padding: 16px;
      font: 700 16px/1.4 "Cascadia Mono", Consolas, "Courier New", monospace; letter-spacing: 0.08em; }
    #stars-timeup b { font-size: clamp(40px, 10vw, 110px); animation: sc-pulse 1s ease-in-out infinite; }
    @keyframes sc-blink { 50% { opacity: 0; } }
    @keyframes sc-pulse { 50% { opacity: 0.45; } }
    @media (max-width: 640px) { #stars-clock .sc-bar, #stars-clock .sc-msg { display: none; } }
  `;
  document.head.appendChild(style);

  const bar = document.createElement("div");
  bar.id = "stars-clock";
  bar.setAttribute("role", "timer");
  bar.innerHTML = `<span class="sc-tag">&gt; MISSION CLOCK</span><span class="sc-time"></span>
    <span class="sc-bar"><span class="sc-fill"></span></span><span class="sc-msg"></span>`;
  const time = bar.querySelector(".sc-time");
  const fill = bar.querySelector(".sc-fill");
  const message = bar.querySelector(".sc-msg");
  const tag = bar.querySelector(".sc-tag");

  let clock = null;
  let offset = 0;
  let shownTimeUp = false;
  let checkingEnd = false;
  const onBoard = path.startsWith("/challenges");

  const pad = (n) => String(n).padStart(2, "0");
  const hms = (s) => {
    s = Math.max(0, Math.ceil(s));
    return `${pad(Math.floor(s / 3600))}:${pad(Math.floor((s % 3600) / 60))}:${pad(s % 60)}`;
  };
  const now = () => Date.now() / 1000 + offset;

  function reload(delay) {
    setTimeout(() => location.reload(), delay || 0);
  }

  function timeUp() {
    if (shownTimeUp || !onBoard) return;
    shownTimeUp = true;
    const cover = document.createElement("div");
    cover.id = "stars-timeup";
    cover.innerHTML = "<b>TIME'S UP</b><span>&gt; flag submissions are closed_</span>";
    document.body.appendChild(cover);
    reload(5000);
  }

  function render() {
    if (!clock || clock.state === "open") {
      bar.classList.remove("sc-on");
      document.body.classList.remove("sc-pad");
      return;
    }
    bar.classList.add("sc-on");
    document.body.classList.add("sc-pad");
    bar.classList.remove("sc-warn", "sc-crit", "sc-over");
    let state = clock.state;
    const left = clock.end ? clock.end - now() : null;
    if (state === "running" && left <= 0) state = "ended";

    if (state === "standby") {
      tag.textContent = "> STANDBY";
      time.innerHTML = `AWAITING LAUNCH<span class="sc-cursor">_</span>`;
      fill.style.width = "0";
      message.textContent = `challenges unlock when the organizer starts the clock (${hms(clock.duration)})`;
    } else if (state === "scheduled") {
      tag.textContent = "> LAUNCH IN";
      time.textContent = hms(clock.start - now());
      fill.style.width = "0";
      message.textContent = "challenges unlock when this reaches zero";
      if (clock.start - now() <= 0 && onBoard) reload(1500);
    } else if (state === "running") {
      tag.textContent = "> MISSION CLOCK";
      time.textContent = hms(left);
      const total = Math.max(1, clock.end - clock.start);
      fill.style.width = `${Math.max(0, Math.min(100, (left / total) * 100))}%`;
      message.textContent = "time left to submit flags";
      if (left <= 60) bar.classList.add("sc-crit");
      else if (left <= 600) bar.classList.add("sc-warn");
    } else {
      bar.classList.add("sc-over");
      tag.textContent = "> MISSION CLOCK";
      time.innerHTML = `TIME'S UP<span class="sc-cursor">_</span>`;
      fill.style.width = "0";
      message.textContent = "flag submissions are closed";
      if (clock.state === "running" && !checkingEnd) {
        // Reached zero here first: check with the server in a moment.
        checkingEnd = true;
        timeUp();
        setTimeout(poll, 1500);
      }
    }
  }

  async function poll() {
    try {
      const reply = await fetch("/stars/timer/state", { cache: "no-store", credentials: "same-origin" });
      const next = await reply.json();
      offset = next.now - Date.now() / 1000;
      const before = clock;
      clock = next;
      if (!before || before.end !== next.end) checkingEnd = false;
      if (before && onBoard && before.state !== next.state) {
        if (next.state === "ended") timeUp();
        else reload(); // started, reopened or put back on standby
      }
    } catch (error) {
      // Keep ticking on the last answer; the next poll will catch up.
    }
    render();
  }

  function begin() {
    document.body.appendChild(bar);
    poll();
    setInterval(poll, 10000);
    setInterval(render, 250);
    document.addEventListener("visibilitychange", () => {
      if (!document.hidden) poll();
    });
  }

  if (document.body) begin();
  else document.addEventListener("DOMContentLoaded", begin);
})();
