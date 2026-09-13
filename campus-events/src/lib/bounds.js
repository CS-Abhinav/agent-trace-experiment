/** Range helpers. All dates are ISO day strings ("YYYY-MM-DD"). */

function toISO(date) {
  return date.toISOString().slice(0, 10);
}

/** Monday through Sunday of the week containing `today`. */
export function weekBounds(today) {
  const date = new Date(`${today}T00:00:00Z`);
  const dayOfWeek = (date.getUTCDay() + 6) % 7; // Monday = 0 ... Sunday = 6
  const monday = new Date(date);
  monday.setUTCDate(date.getUTCDate() - dayOfWeek);
  const sunday = new Date(monday);
  sunday.setUTCDate(monday.getUTCDate() + 6);
  return { start: toISO(monday), end: toISO(sunday) };
}

/** First through last day of the month containing `today`. */
export function monthBounds(today) {
  const date = new Date(`${today}T00:00:00Z`);
  const first = new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), 1));
  const last = new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth() + 1, 0));
  return { start: toISO(first), end: toISO(last) };
}
