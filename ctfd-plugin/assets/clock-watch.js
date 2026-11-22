// Mission clock, on player pages. Players don't see a countdown. On the
// challenges page, this checks the clock every 10 seconds and reloads when the
// organizer starts it, ends it or puts it on standby, so the board opens and
// closes by itself. CTFd does the actual locking, so none of this is needed to
// keep anyone out.
(() => {
  if (window.__starsClockWatch) return;
  window.__starsClockWatch = true;
  if (!location.pathname.startsWith("/challenges")) return;

  let state = null;
  async function poll() {
    try {
      const reply = await fetch("/stars/timer/state", { cache: "no-store", credentials: "same-origin" });
      const next = (await reply.json()).state;
      if (state !== null && next !== state) location.reload();
      state = next;
    } catch (error) {
      // Try again on the next poll.
    }
  }

  poll();
  setInterval(poll, 10000);
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) poll();
  });
})();
