# Fix: Align Carousel Breakpoint with CSS Media Query

## Problem

The carousel JS breakpoint (1200px) disagrees with the CSS media query breakpoint (1250px), creating a 50px window where the carousel shows mobile behavior inside a desktop CSS layout.

| Source                              | Value    | Meaning                                  |
| ----------------------------------- | -------- | ---------------------------------------- |
| `WebContent/js/carousel.js:7`       | `1200px` | Switch from 2 testimonials to 1          |
| `WebContent/css/mediaqueries.css:1` | `1250px` | Switch from desktop to tablet CSS layout |

## Fix

Change `DESKTOP_BREAKPOINT` in `carousel.js` from `1200` to `1250` to match the CSS media query. Add a comment noting the CSS dependency.

```js
export const CAROUSEL_CONFIG = {
  DESKTOP_BREAKPOINT: 1250, // Must match mediaqueries.css @media breakpoint
  AUTO_SCROLL_INTERVAL_MS: 20000,
  TESTIMONIALS_DESKTOP: 2,
  TESTIMONIALS_MOBILE: 1,
};
```

## Testing

- Existing carousel unit tests should pass (they test logic with the config value, not the specific number)
- Existing responsive E2E tests should be reviewed to ensure they test at the correct breakpoint
- Manual verification: at 1225px viewport, carousel should now show 2 items (desktop) instead of 1 (mobile)

## Files Changed

| File                        | Change                                         |
| --------------------------- | ---------------------------------------------- |
| `WebContent/js/carousel.js` | `DESKTOP_BREAKPOINT: 1200` -> `1250` + comment |
