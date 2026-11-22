// Ask for help: a button in the corner of the challenges page. Players choose
// the challenge (the one they have open is chosen for them) and can say what
// they've tried. Organizers see it on Admin Panel > Help Queue. Each team has
// one request at a time; asking again changes it.
(() => {
  if (window.__starsHelp) return;
  window.__starsHelp = true;
  if (!location.pathname.startsWith("/challenges")) return;

  const headers = () => ({ "Content-Type": "application/json", "CSRF-Token": (window.init && window.init.csrfNonce) || "" });
  let current = null; // the team's open request, or null
  let timer = null;

  const root = document.createElement("div");
  root.className = "position-fixed bottom-0 end-0 m-3 d-flex flex-column align-items-end";
  // Above the challenge window, so it can be pressed while one is open.
  root.style.zIndex = "1060";
  root.innerHTML = `
    <div class="card shadow mb-2" id="sh-panel" style="width: 340px; max-width: calc(100vw - 2rem);" hidden>
      <div class="card-body">
        <h6 class="card-title mb-3">Ask an organizer for help</h6>
        <div id="sh-form">
          <label class="form-label small mb-1" for="sh-challenge">Challenge</label>
          <select class="form-select form-select-sm mb-2" id="sh-challenge"></select>
          <label class="form-label small mb-1" for="sh-message">What have you tried so far? (optional)</label>
          <textarea class="form-control form-control-sm mb-3" id="sh-message" rows="3" maxlength="300"></textarea>
          <div class="d-flex gap-2">
            <button type="button" class="btn btn-primary btn-sm" id="sh-send">Send</button>
            <button type="button" class="btn btn-outline-secondary btn-sm" id="sh-close">Close</button>
          </div>
        </div>
        <div id="sh-status" hidden>
          <p class="mb-1" id="sh-status-text"></p>
          <p class="small text-muted mb-3" id="sh-status-what"></p>
          <div class="d-flex gap-2 flex-wrap">
            <button type="button" class="btn btn-outline-secondary btn-sm" id="sh-change">Change</button>
            <button type="button" class="btn btn-outline-secondary btn-sm" id="sh-cancel">We don't need help now</button>
            <button type="button" class="btn btn-link btn-sm" id="sh-hide">Hide</button>
          </div>
        </div>
        <p class="small text-danger mt-2 mb-0" id="sh-error" hidden></p>
      </div>
    </div>
    <button type="button" class="btn btn-primary shadow" id="sh-button">Ask for help</button>`;

  const $ = (id) => root.querySelector("#" + id);
  const panel = $("sh-panel");

  function openChallengeId() {
    // CTFd puts the open challenge in the address as #Name-ID.
    const hash = decodeURIComponent(location.hash.slice(1));
    const id = hash.slice(hash.lastIndexOf("-") + 1);
    return /^\d+$/.test(id) ? id : "";
  }

  async function fillChallenges(selected) {
    const select = $("sh-challenge");
    select.replaceChildren(new Option("Not about one challenge", ""));
    try {
      const reply = await fetch("/api/v1/challenges", { credentials: "same-origin" });
      const list = (await reply.json()).data || [];
      const groups = {};
      for (const challenge of list) (groups[challenge.category] = groups[challenge.category] || []).push(challenge);
      for (const category of Object.keys(groups).sort()) {
        const group = document.createElement("optgroup");
        group.label = category;
        for (const challenge of groups[category]) group.appendChild(new Option(challenge.name, String(challenge.id)));
        select.appendChild(group);
      }
    } catch (error) { /* the "not about one challenge" choice still works */ }
    select.value = selected && select.querySelector(`option[value="${selected}"]`) ? selected : "";
  }

  function error(text) {
    $("sh-error").textContent = text || "";
    $("sh-error").hidden = !text;
  }

  function render() {
    const button = $("sh-button");
    if (!current) {
      button.textContent = "Ask for help";
      button.className = "btn btn-primary shadow";
      $("sh-form").hidden = false;
      $("sh-status").hidden = true;
      return;
    }
    const coming = current.status === "coming";
    button.textContent = coming ? "Help is on the way" : "Waiting for help";
    button.className = "btn btn-success shadow";
    $("sh-status-text").textContent = coming
      ? "An organizer is on the way to your team."
      : `Your team is waiting for an organizer${current.position ? ` (number ${current.position} in the queue)` : ""}.`;
    $("sh-status-what").textContent = current.challenge ? `About: ${current.challenge}` : "Not about one challenge";
    $("sh-form").hidden = true;
    $("sh-status").hidden = false;
  }

  async function refresh() {
    try {
      const reply = await fetch("/stars/help", { credentials: "same-origin", cache: "no-store" });
      const before = current;
      current = (await reply.json()).request;
      if (before && !current) {
        // Marked as done by an organizer.
        panel.hidden = true;
      }
      render();
    } catch (error) { /* try again on the next poll */ }
    clearTimeout(timer);
    timer = setTimeout(refresh, current ? 8000 : 30000);
  }

  async function post(path, body) {
    const reply = await fetch(path, { method: "POST", credentials: "same-origin", headers: headers(), body: JSON.stringify(body || {}) });
    const data = await reply.json().catch(() => ({}));
    if (!reply.ok || data.success === false) throw new Error(data.error || "That didn't send. Try again.");
    return data;
  }

  // A challenge window keeps the keyboard to itself, so it has to close before
  // anyone can type in the form. Bootstrap ignores a close while the window is
  // still opening, so this tries again a moment later.
  function closeChallengeWindow(tries) {
    const close = document.querySelector('.modal.show [data-bs-dismiss="modal"]');
    if (!close || tries <= 0) return;
    close.click();
    setTimeout(() => closeChallengeWindow(tries - 1), 350);
  }

  async function show(editing) {
    const selected = openChallengeId() || (current && current.challenge_id ? String(current.challenge_id) : "");
    closeChallengeWindow(4);
    error("");
    if (!current || editing) {
      await fillChallenges(selected);
      $("sh-message").value = editing && current ? current.message : "";
      $("sh-form").hidden = false;
      $("sh-status").hidden = true;
    } else {
      render();
    }
    panel.hidden = false;
  }

  $("sh-button").addEventListener("click", () => (panel.hidden ? show(false) : (panel.hidden = true)));
  $("sh-close").addEventListener("click", () => { panel.hidden = true; render(); });
  $("sh-hide").addEventListener("click", () => { panel.hidden = true; });
  $("sh-change").addEventListener("click", () => show(true));
  $("sh-send").addEventListener("click", async () => {
    $("sh-send").disabled = true;
    try {
      const data = await post("/stars/help", { challenge_id: $("sh-challenge").value, message: $("sh-message").value });
      current = data.request;
      error("");
      render();
      refresh();
    } catch (problem) {
      error(problem.message);
    } finally {
      $("sh-send").disabled = false;
    }
  });
  $("sh-cancel").addEventListener("click", async () => {
    try {
      await post("/stars/help/cancel");
      current = null;
      panel.hidden = true;
      render();
    } catch (problem) {
      error(problem.message);
    }
  });

  function begin() {
    document.body.appendChild(root);
    refresh();
  }
  if (document.body) begin();
  else document.addEventListener("DOMContentLoaded", begin);
})();
