// STARS mission clock: the projector page (/timer).
// Shows the countdown huge, with a matrix-style rain behind it, and plays the
// playlist (assets/playlist.json) through Spotify's embed while the clock runs,
// shuffled into a new random order every time the clock starts.
(() => {
  const ASSETS = window.STARS_ASSETS || "/plugins/stars/assets/";
  const $ = (id) => document.getElementById(id);
  const digits = $("digits");
  const status = $("status");
  const progress = $("progress");
  const sub = $("sub");
  const log = $("log");
  const sys = $("sys");

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
  let lastShown = null;
  const now = () => Date.now() / 1000 + offset;

  // --- Terminal log, bottom left -------------------------------------------
  const lines = [];
  function say(text) {
    const d = new Date();
    lines.push(`[${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}] ${text}`);
    while (lines.length > 7) lines.shift();
    log.textContent = lines.join("\n");
  }

  // --- Matrix rain ----------------------------------------------------------
  const canvas = $("rain");
  const ctx = canvas.getContext("2d");
  const glyphs = "STARS{}01アイウエオカキクケコサシスセソタチツテトナニヌネノ<>/\\=+*#$%";
  let columns = [];
  let fontSize = 18;
  function resize() {
    canvas.width = innerWidth;
    canvas.height = innerHeight;
    fontSize = Math.max(14, Math.round(innerWidth / 90));
    columns = Array.from({ length: Math.ceil(innerWidth / fontSize) }, () => Math.random() * -innerHeight / fontSize);
  }
  addEventListener("resize", resize);
  resize();
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  function rain() {
    const ink = getComputedStyle(document.body).getPropertyValue("--ink").trim() || "#39ff7a";
    ctx.fillStyle = "rgba(0, 0, 0, 0.09)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.font = `${fontSize}px Consolas, monospace`;
    columns.forEach((y, i) => {
      ctx.fillStyle = Math.random() < 0.04 ? "#d8ffe6" : ink;
      ctx.fillText(glyphs[Math.floor(Math.random() * glyphs.length)], i * fontSize, y * fontSize);
      columns[i] = y * fontSize > canvas.height && Math.random() > 0.975 ? 0 : y + 1;
    });
  }
  if (!still) setInterval(rain, 55);

  // --- The clock --------------------------------------------------------------
  function bar(fraction) {
    const width = 30;
    const full = Math.round(Math.max(0, Math.min(1, fraction)) * width);
    return `[${"█".repeat(full)}${"░".repeat(width - full)}] ${String(Math.round(fraction * 100)).padStart(3)}%`;
  }

  function effectiveState() {
    if (!clock) return "loading";
    if (clock.state === "running" && clock.end - now() <= 0) return "ended";
    return clock.state;
  }

  function render() {
    const d = new Date(now() * 1000);
    sys.textContent = `SYS ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
    const state = effectiveState();
    let text = "--:--:--";
    let mood = state;

    if (state === "standby") {
      text = hms(clock.duration);
      status.innerHTML = '&gt; AWAITING LAUNCH<span class="cursor">_</span>';
      progress.textContent = bar(1);
      sub.textContent = "challenges are locked until the organizer starts the clock";
    } else if (state === "scheduled") {
      text = hms(clock.start - now());
      status.innerHTML = '&gt; LAUNCH SEQUENCE ENGAGED<span class="cursor">_</span>';
      progress.textContent = bar(0);
      sub.textContent = `challenges unlock at ${clockTime(clock.start)}`;
    } else if (state === "running") {
      const left = clock.end - now();
      const total = Math.max(1, clock.end - clock.start);
      text = hms(left);
      status.innerHTML = '&gt; MISSION IN PROGRESS<span class="cursor">_</span>';
      progress.textContent = bar(left / total);
      sub.textContent = `flag submissions close at ${clockTime(clock.end)}`;
      if (left <= 60) mood = "crit";
      else if (left <= 600) mood = "warn";
    } else if (state === "ended") {
      text = "00:00:00";
      status.innerHTML = "&gt; TIME'S UP<span class=\"cursor\">_</span>";
      progress.textContent = bar(0);
      sub.textContent = "flag submissions are closed";
    } else if (state === "open") {
      text = "--:--:--";
      status.innerHTML = '&gt; NO CLOCK SET<span class="cursor">_</span>';
      progress.textContent = "";
      sub.textContent = "the CTF is open with no time limit";
    }

    if (digits.textContent !== text) {
      digits.textContent = text;
      digits.dataset.text = text;
    }
    document.body.className = `state-${mood}`;
    if (document.body.dataset.glitch) document.body.classList.add("glitch");

    if (state !== lastShown) {
      if (lastShown !== null) glitch();
      announce(state);
      lastShown = state;
    }
  }

  function glitch() {
    document.body.dataset.glitch = "1";
    setTimeout(() => {
      delete document.body.dataset.glitch;
      document.body.classList.remove("glitch");
    }, 1000);
  }

  function announce(state) {
    const messages = {
      standby: "standby: challenge grid locked, awaiting launch",
      scheduled: "launch sequence engaged",
      running: `mission clock started: ${hms(clock.end - clock.start)} on the clock`,
      ended: "time's up: flag submissions closed",
      open: "no clock set: CTF open with no time limit",
    };
    if (messages[state]) say(messages[state]);
  }

  async function poll() {
    try {
      const reply = await fetch("/stars/timer/state", { cache: "no-store", credentials: "same-origin" });
      const next = await reply.json();
      offset = next.now - Date.now() / 1000;
      const before = clock;
      clock = next;
      if (before && before.state === "running" && next.state === "running" && before.start !== next.start) {
        say("mission clock restarted");
        glitch();
      } else if (before && before.end && next.end && before.state === next.state && before.end !== next.end) {
        const change = next.end - before.end;
        say(`${change > 0 ? "+" : "-"}${hms(Math.abs(change))} ${change > 0 ? "added to" : "taken off"} the clock`);
      }
      music.update(next);
    } catch (error) {
      if (!clock) status.innerHTML = '&gt; NO UPLINK TO MISSION CONTROL<span class="cursor">_</span>';
    }
  }

  say("uplink established");
  poll();
  setInterval(poll, 3000);
  setInterval(render, 200);

  // --- Music --------------------------------------------------------------
  const music = (() => {
    const panel = $("music");
    const title = $("music-title");
    const arm = $("arm");
    const playButton = $("music-play");
    let tracks = [];
    let order = [];
    let position = -1;
    let armed = false;
    let controller = null;
    let session = null; // the clock start the current shuffle belongs to
    let wanted = false; // should music be playing now?
    let progressed = false;
    let advancing = false;
    let watchdog = null;
    let enabled = false;

    fetch(ASSETS + "playlist.json", { cache: "no-store" })
      .then((reply) => reply.json())
      .then((list) => {
        tracks = list.tracks || [];
        say(`audio deck loaded: ${tracks.length} tracks, ${list.name || "playlist"}`);
        if (clock) update(clock);
      })
      .catch(() => say("audio deck: playlist.json missing"));

    function shuffle() {
      order = tracks.map((_, i) => i);
      for (let i = order.length - 1; i > 0; i--) {
        const random = new Uint32Array(1);
        crypto.getRandomValues(random);
        const j = random[0] % (i + 1);
        [order[i], order[j]] = [order[j], order[i]];
      }
      position = -1;
    }

    function current() {
      return tracks[order[position]];
    }

    function play() {
      if (!controller || !tracks.length) return;
      position += 1;
      if (position >= order.length) {
        // Played them all: shuffle again and carry on.
        shuffle();
        position = 0;
      }
      const track = current();
      title.textContent = `${track.title} — ${track.artist}`;
      say(`now playing: ${track.title}`);
      progressed = false;
      advancing = false;
      controller.loadUri(track.uri);
      setTimeout(() => controller && wanted && controller.play(), 700);
      clearTimeout(watchdog);
      watchdog = setTimeout(() => {
        if (wanted && !progressed) playButton.hidden = false;
      }, 7000);
    }

    function pause() {
      wanted = false;
      clearTimeout(watchdog);
      playButton.hidden = true;
      if (controller) controller.pause();
    }

    function load() {
      if (controller || window.__spotifyLoading) return;
      window.__spotifyLoading = true;
      say("connecting to Spotify...");
      window.onSpotifyIframeApiReady = (api) => {
        const first = tracks[0] ? tracks[0].uri : "spotify:album:0HmBQ2vhh1fT3kaBi92Bip";
        api.createController($("spotify"), { uri: first, width: "100%", height: 80 }, (made) => {
          controller = made;
          say("Spotify linked");
          controller.addListener("playback_update", (event) => {
            const { isPaused, position: at, duration } = event.data || {};
            if (!isPaused && at > 0) {
              progressed = true;
              playButton.hidden = true;
            }
            // A track has finished: start another random one.
            const finished = progressed && duration > 0 && (at >= duration - 900 || (isPaused && at === 0));
            if (wanted && finished && !advancing) {
              advancing = true;
              setTimeout(play, 400);
            }
          });
          if (clock) update(clock);
        });
      };
      const script = document.createElement("script");
      script.src = "https://open.spotify.com/embed/iframe-api/v1";
      script.async = true;
      script.onerror = () => {
        title.textContent = "NO UPLINK: music needs internet on this PC";
        say("Spotify unreachable: the clock still runs, without music");
      };
      document.head.appendChild(script);
    }

    function doArm() {
      if (armed) return;
      armed = true;
      arm.hidden = true;
      say("audio armed");
      load();
    }
    arm.addEventListener("click", doArm);
    addEventListener("keydown", (event) => {
      if (!arm.hidden) doArm();
      if (event.key === "n" || event.key === "N") skip();
    });

    function skip() {
      if (controller && wanted) play();
    }
    $("skip").addEventListener("click", skip);
    playButton.addEventListener("click", () => {
      if (controller) controller.resume();
      playButton.hidden = true;
    });

    function update(next) {
      enabled = next.music && tracks.length > 0;
      panel.hidden = !enabled;
      if (!enabled) {
        arm.hidden = true;
        if (wanted) pause();
        return;
      }
      if (!armed) {
        arm.hidden = false;
        return;
      }
      const running = next.state === "running" && next.end - now() > 0;
      if (running && (!wanted || session !== next.start) && controller) {
        // Started or restarted: a fresh random order.
        session = next.start;
        wanted = true;
        shuffle();
        play();
      } else if (!running && wanted) {
        pause();
        title.textContent = "standing by";
      }
    }

    return { update };
  })();

  // --- Fullscreen -----------------------------------------------------------
  function fullscreen() {
    if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen().catch(() => {});
  }
  $("fullscreen").addEventListener("click", fullscreen);
  addEventListener("keydown", (event) => {
    if (event.key === "f" || event.key === "F") fullscreen();
  });
})();
