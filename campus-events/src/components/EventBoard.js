import { thisWeek } from "../filters/weekFilter.js";
import { upcomingThisMonth } from "../filters/monthFilter.js";

function renderList(events) {
  if (events.length === 0) return "<p class='empty'>No events.</p>";
  return `<ul>${events
    .map((e) => `<li><strong>${e.title}</strong> — ${e.date} · ${e.venue}</li>`)
    .join("")}</ul>`;
}

export function renderEventBoard(events, today) {
  return `
    <section>
      <h2>This week</h2>
      ${renderList(thisWeek(events, today))}
    </section>
    <section>
      <h2>Upcoming this month</h2>
      ${renderList(upcomingThisMonth(events, today))}
    </section>
  `;
}
