// On every admin page: the number of teams waiting for help, next to "Help
// Queue" in the menu. On Admin Panel > Statistics: who took first blood.
(() => {
  if (window.__starsAdminExtras) return;
  window.__starsAdminExtras = true;

  const pad = (n) => String(n).padStart(2, "0");
  const clockTime = (unix) => {
    const d = new Date(unix * 1000);
    return `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
  };
  const duration = (seconds) => {
    if (seconds == null) return "";
    const minutes = Math.floor(seconds / 60);
    return minutes >= 60 ? `${Math.floor(minutes / 60)} h ${minutes % 60} min` : minutes ? `${minutes} min` : `${seconds} s`;
  };
  const cell = (row, text, className) => {
    const td = document.createElement("td");
    td.textContent = text;
    if (className) td.className = className;
    row.appendChild(td);
  };

  // --- The waiting count in the menu ----------------------------------------
  async function badge() {
    const link = Array.from(document.querySelectorAll("a")).find((a) => a.getAttribute("href") === "/admin/stars-help");
    if (!link) return;
    try {
      const reply = await fetch("/admin/stars-help/list", { credentials: "same-origin", cache: "no-store" });
      const waiting = (await reply.json()).waiting || 0;
      let count = link.querySelector(".stars-help-count");
      if (!count) {
        count = document.createElement("span");
        count.className = "badge badge-pill badge-danger ml-1 stars-help-count";
        link.appendChild(count);
      }
      count.textContent = waiting;
      count.hidden = waiting === 0;
      count.title = `${waiting} waiting for help`;
    } catch (error) { /* try again next time */ }
  }

  // --- First blood on the statistics page -----------------------------------
  async function firstBlood() {
    const heading = Array.from(document.querySelectorAll("h3")).find((h) => h.textContent.trim().startsWith("Player Progression"));
    if (!heading) return;
    const reply = await fetch("/admin/stars/first-blood", { credentials: "same-origin", cache: "no-store" });
    const blood = (await reply.json()).first_blood;

    const row = document.createElement("div");
    row.className = "row mb-4";
    row.id = "stars-first-blood";
    const column = document.createElement("div");
    column.className = "col-md-12";
    const title = document.createElement("h3");
    title.textContent = "First Blood";
    column.appendChild(title);

    if (!blood) {
      const empty = document.createElement("p");
      empty.className = "text-muted";
      empty.textContent = "No one has solved a challenge yet.";
      column.appendChild(empty);
    } else {
      const table = document.createElement("table");
      table.className = "table table-striped table-sm";
      table.innerHTML = "<thead><tr><th>Team</th><th>Solved by</th><th>Challenge</th><th>Category</th><th>Time</th><th>After the start</th></tr></thead>";
      const body = document.createElement("tbody");
      const tr = document.createElement("tr");
      cell(tr, blood.team, "font-weight-bold");
      cell(tr, blood.player);
      cell(tr, blood.challenge);
      cell(tr, blood.category);
      cell(tr, blood.at ? clockTime(blood.at) : "");
      cell(tr, duration(blood.after_start), "text-muted");
      body.appendChild(tr);
      table.appendChild(body);
      column.appendChild(table);
    }
    row.appendChild(column);
    heading.closest(".row").before(row, document.createElement("hr"));
  }

  // --- Hide the third-party "Filter Matrix Data" grid -----------------------
  // That grid on the Statistics page is injected by a browser extension, not by
  // CTFd, and it shows nothing useful here (scores are hidden). This hides it so
  // it stops cluttering the page; the real grid is Admin > Score Matrix. It only
  // ever touches that extension's own blocks, found by their wording, and never
  // CTFd's sections or the First Blood block above. Does nothing if the
  // extension isn't installed.
  const CTFD_SECTION = /Solve Counts|Score Distribution|Player Progression|Submission Percentages|First Blood/;

  function hideMatrixExtension() {
    let acted = false;
    const kill = (wanted) => {
      // Document order lists ancestors first, so the first hit is the outermost
      // block that is all extension and no CTFd content: the whole widget.
      for (const el of document.querySelectorAll("div, section, aside, details")) {
        if (el.dataset.starsHidden) continue;
        const text = el.textContent || "";
        if (wanted.every((word) => text.includes(word)) && !CTFD_SECTION.test(text)) {
          el.style.display = "none";
          el.dataset.starsHidden = "1";
          acted = true;
          return;
        }
      }
    };
    kill(["Filter Matrix Data", "Filter Teams"]);        // the filter panel
    kill(["Place", "Team", "Score", "Opened"]);          // the legend + grid
    return acted;
  }

  function begin() {
    badge();
    setInterval(badge, 10000);
    if (location.pathname.startsWith("/admin/statistics")) {
      firstBlood().catch(() => {});
      // The extension injects after it fetches data, so keep checking briefly.
      let tries = 0, idle = 0;
      const sweep = setInterval(() => {
        idle = hideMatrixExtension() ? 0 : idle + 1;
        if (++tries >= 30 || idle >= 6) clearInterval(sweep);
      }, 500);
      hideMatrixExtension();
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", begin);
  else begin();
})();
