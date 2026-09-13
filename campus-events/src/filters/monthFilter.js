import { getEventsInRange } from "../lib/dateRange.js";
import { monthBounds } from "../lib/bounds.js";

/** Events happening this month (1st through the last day). */
export function upcomingThisMonth(events, today) {
  const { start, end } = monthBounds(today);
  return getEventsInRange(events, start, end);
}
