/**
 * Shared date-range helper.
 *
 * Returns every event that falls inside the given range.
 * Dates are ISO day strings ("YYYY-MM-DD"), so string comparison
 * is equivalent to chronological comparison.
 */
export function getEventsInRange(events, start, end) {
  return events.filter((event) => event.date >= start && event.date < end);
}
