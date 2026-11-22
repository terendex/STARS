// On every admin page: the number of teams waiting for help, next to "Help
// Queue" in the menu. On Admin Panel > Statistics: the first bloods table.
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

  // --- First bloods on the statistics page ----------------------------------
  async function firstBloods() {
    const heading = Array.from(document.querySelectorAll("h3")).find((h) => h.textContent.trim().startsWith("Player Progression"));
    if (!heading) return;
    const reply = await fetch("/admin/stars/first-bloods", { credentials: "same-origin", cache: "no-store" });
    const data = await reply.json();
    const bloods = data.first_bloods || [];

    const row = document.createElement("div");
    row.className = "row mb-4";
    row.id = "stars-first-bloods";
    const column = document.createElement("div");
    column.className = "col-md-12";
    const title = document.createElement("h3");
    title.textContent = "First Bloods ";
    const note = document.createElement("sup");
    note.className = "text-muted";
    note.textContent = `(${bloods.length} of ${data.challenges} challenges solved)`;
    title.appendChild(note);
    column.appendChild(title);

    if (!bloods.length) {
      const empty = document.createElement("p");
      empty.className = "text-muted";
      empty.textContent = "No challenge has been solved yet.";
      column.appendChild(empty);
    } else {
      const table = document.createElement("table");
      table.className = "table table-striped table-sm";
      table.innerHTML = "<thead><tr><th>Challenge</th><th>Category</th><th>Team</th><th>Solved by</th><th>Time</th><th>After the start</th></tr></thead>";
      const body = document.createElement("tbody");
      for (const blood of bloods) {
        const tr = document.createElement("tr");
        cell(tr, blood.challenge, "font-weight-bold");
        cell(tr, blood.category);
        cell(tr, blood.team);
        cell(tr, blood.player);
        cell(tr, blood.at ? clockTime(blood.at) : "");
        cell(tr, duration(blood.after_start), "text-muted");
        body.appendChild(tr);
      }
      table.appendChild(body);
      column.appendChild(table);
    }
    row.appendChild(column);
    heading.closest(".row").before(row, document.createElement("hr"));
  }

  function begin() {
    badge();
    setInterval(badge, 10000);
    if (location.pathname.startsWith("/admin/statistics")) firstBloods().catch(() => {});
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", begin);
  else begin();
})();
