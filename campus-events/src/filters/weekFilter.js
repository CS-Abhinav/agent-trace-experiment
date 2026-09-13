import { getEventsInRange } from "../lib/dateRange.js";
import { weekBounds } from "../lib/bounds.js";

/** Events happening this week (Monday through Sunday). */
export function thisWeek(events, today) {
  const { start, end } = weekBounds(today);
  return getEventsInRange(events, start, end);
}
