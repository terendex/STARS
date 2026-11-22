// Plays the playlist (assets/playlist.json) through Spotify's embed while the
// mission clock runs: a new random order every time the clock starts or
// restarts, and another random track whenever one ends. Both the Mission Clock
// admin page ("admin") and the projector page ("projector") use it, and the
// admin page chooses which one plays, so the music never plays twice.
//
// Browsers only allow sound after a click on the page, so nothing plays until
// arm() is called from a click (Start, Restart, or the Turn on sound button).
// Only the browser where that happened plays, so a second tab stays quiet.
// askEarly shows the Turn on sound button before the clock starts too, for the
// projector page, which has no Start button to click. body[data-music] says
// what it's doing, for checking from a script.
window.StarsMusic = (options) => {
  const { assets, now, here, askEarly, panel, title, nowPlaying, soundButton, playButton, embed } = options;
  const elsewhere = here === "admin" ? "Playing on the projector page" : "Playing on the Mission Clock page";
  const status = (value) => { document.body.dataset.music = value; };
  let tracks = [];
  let order = [];
  let position = -1;
  let armed = false;
  let loading = false;
  let controller = null;
  let session = null; // the clock start the current shuffle belongs to
  let wanted = false; // should music be playing now?
  let progressed = false;
  let advancing = false;
  let watchdog = null;
  let last = null; // the latest clock state

  fetch(assets + "playlist.json", { cache: "no-store" })
    .then((reply) => reply.json())
    .then((list) => {
      tracks = list.tracks || [];
      if (last) update(last);
    })
    .catch(() => status("no playlist"));

  function show(text, playing) {
    title.textContent = text;
    if (nowPlaying) nowPlaying.textContent = playing ? `Now playing: ${text}` : "";
  }

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

  function play() {
    if (!controller || !tracks.length) return;
    position += 1;
    if (position >= order.length) {
      // Played them all: shuffle again and carry on.
      shuffle();
      position = 0;
    }
    const track = tracks[order[position]];
    show(`${track.title} — ${track.artist}`, true);
    status("playing");
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
    status("paused");
  }

  function load() {
    if (controller || loading) return;
    loading = true;
    status("loading");
    window.onSpotifyIframeApiReady = (api) => {
      const first = tracks[0] ? tracks[0].uri : "spotify:album:0HmBQ2vhh1fT3kaBi92Bip";
      api.createController(embed, { uri: first, width: "100%", height: 80 }, (made) => {
        controller = made;
        status("ready");
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
        if (last) update(last);
      });
    };
    const script = document.createElement("script");
    script.src = "https://open.spotify.com/embed/iframe-api/v1";
    script.async = true;
    script.onerror = () => {
      show("No internet, so no music", false);
      status("offline");
    };
    document.head.appendChild(script);
  }

  // Call from a click: lets this browser play sound.
  function arm() {
    armed = true;
    soundButton.hidden = true;
    load();
    if (last) update(last);
  }

  function skip() {
    if (controller && wanted) play();
  }

  playButton.addEventListener("click", () => {
    if (controller) controller.resume();
    playButton.hidden = true;
  });

  function update(clock) {
    last = clock;
    const running = clock.state === "running" && clock.end - now() > 0;
    const mine = clock.music === here;
    if (panel) panel.hidden = !mine;
    if (!mine || !tracks.length) {
      if (wanted) pause();
      soundButton.hidden = true;
      show(clock.music === "0" ? "Music is off" : mine ? "Loading the playlist" : elsewhere, false);
      return;
    }
    if (!armed) {
      soundButton.hidden = !(running || askEarly);
      show(running ? "Sound is off in this browser" : "Plays while the clock runs", false);
      return;
    }
    if (running && (!wanted || session !== clock.start) && controller) {
      // Started or restarted: a fresh random order.
      session = clock.start;
      wanted = true;
      shuffle();
      play();
    } else if (!running) {
      if (wanted) pause();
      show("Plays while the clock runs", false);
    }
  }

  return { arm, skip, update };
};
