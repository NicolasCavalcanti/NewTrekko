import { useState, useEffect } from "react";

/**
 * Returns a debounced copy of `value` that only updates after `delay` ms of
 * inactivity.  Use the debounced value for API queries so that rapid keystrokes
 * do not fire a new request on every character typed.
 *
 * @param value  The raw value to debounce (typically a controlled input state).
 * @param delay  Milliseconds to wait after the last change before updating.
 *               Defaults to 300 ms — enough to avoid flooding the server while
 *               still feeling responsive.
 */
export function useDebounce<T>(value: T, delay = 300): T {
  const [debounced, setDebounced] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
}
