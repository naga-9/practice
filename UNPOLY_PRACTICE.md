# Unpoly Practice Plan

[Unpoly](https://unpoly.com) is a progressive-enhancement JS library. The server keeps rendering
full HTML; Unpoly swaps only the relevant fragments, handles forms, opens overlays, and
manages navigation — without a JSON API or a frontend framework.

Each scenario below is a small, self-contained thing to build in the `core` app. The goal is
to touch every major Unpoly feature once, then combine them in a realistic mini-app.

Legend: **[server]** = Django-side work needed, **[client]** = mostly `up-*` attributes in templates.

---

## 1. Setup & fundamentals

- [x] **Load Unpoly** — add CSS/JS via CDN to `base.html`, verify `up.version` in console. *[client]*
- [x] **Fragment links** — `<a href="/about" up-target="main">`. Only `<main>` is swapped, navbar stays.
      Confirm the request header `X-Up-Target: main` arrives at Django. *[client, server]*
- [ ] **Navigation vs. plain update** — `up-follow` vs `up-target` alone. Observe URL/history/scroll
      differences. *[client]*
- [ ] **Multiple targets** — `up-target="main, .flash"` to update two fragments in one round-trip. *[client]*
- [x] **Partial rendering on the server** — read `request.headers["X-Up-Target"]` and render only the
      fragment (skip `base.html`) to save bandwidth. Use `{% extends %}` conditionally or a helper. *[server]*
- [ ] **Fallback when target missing** — `up-fallback`, and `up-target` pointing at an element the
      response doesn't contain. See how Unpoly recovers. *[client]*
- [x] **Loading state** — `.up-active` / `.up-loading` classes, add a spinner/progress bar via CSS. *[client]*

## 2. Forms

- [ ] **Submit a form via Unpoly** — `<form up-submit up-target="#form-area">`. On validation error,
      Django re-renders the form; Unpoly swaps it in place. Note: Django must return a non-2xx
      (e.g. `422`) or Unpoly will treat it as success — try `up-fail-target` too. *[server, client]*
- [ ] **Successful submit redirects** — POST → `redirect()` → Unpoly follows and updates the target.
      Check the `X-Up-Location` header behaviour. *[server]*
- [ ] **Live validation** — `up-validate` on individual fields; Django responds to
      `X-Up-Validate` by running form validation without saving. *[server, client]*
- [ ] **Dependent fields** — `up-validate` on a `<select>` to re-render a second select
      (e.g. country → city). *[server, client]*
- [ ] **Watch fields / autosubmit** — `up-autosubmit` on a search box with `up-watch-delay`. *[client]*
- [ ] **Disable while submitting** — `up-disable`, and `up-watch-disable`. *[client]*
- [ ] **CSRF** — confirm Django's CSRF works with `up-submit` (token in form) and with
      `up.request()` POSTs (needs `X-CSRFToken` via `up.protocol.config.csrfToken`). *[server, client]*
- [ ] **File uploads** — multipart form via `up-submit`. *[server, client]*

## 3. Layers (modals, drawers, popups)

- [ ] **Open a modal** — `<a href="/items/new" up-layer="new" up-mode="modal">`. Same view serves
      full page and modal content. *[client]*
- [ ] **Drawer / popup / cover modes** — try each `up-mode`. *[client]*
- [ ] **Form inside a modal** — submit; on success close the layer and update the parent list
      (`up-accept-location`, or `X-Up-Accept-Layer` header from Django). *[server, client]*
- [ ] **Return a value from a layer** — `up-accept-event` / `X-Up-Accept-Layer: {"id": 5}` →
      parent picks the new record into a select. *[server, client]*
- [ ] **Dismiss vs accept** — `up-dismiss`, `X-Up-Dismiss-Layer`, and handling `up:layer:dismissed`. *[client]*
- [ ] **Nested layers** — open a modal from a modal. Note `up-layer="parent"`/`"root"` targeting. *[client]*
- [ ] **Layer context** — `up-context` and `X-Up-Context` header to pass state to the server. *[client, server]*
- [ ] **Layer-aware rendering** — Django reads `X-Up-Mode` to omit the page chrome in overlays. *[server]*

## 4. Navigation, history & caching

- [ ] **History** — `up-history`, back/forward button restoring fragments. *[client]*
- [ ] **Cache** — repeat a `GET`; observe instant render + background revalidation.
      Tune `up.network.config.cacheExpireAge`. *[client]*
- [ ] **Cache expiry after mutation** — after a POST, confirm cached GETs are expired;
      try `X-Up-Expire-Cache` from Django. *[server]*
- [ ] **Preloading** — `up-preload` on hover; `up-instant` on mousedown. *[client]*
- [ ] **Redirect detection** — `X-Up-Location` / `X-Up-Method` after a POST-redirect-GET. *[server]*
- [ ] **Aborting** — navigating away mid-request, `up-abortable`. *[client]*
- [ ] **Unpoly-aware `Vary`** — send `Vary: X-Up-Target` so full and partial responses don't collide
      in browser/proxy caches. *[server]*

## 5. Feedback & transitions

- [ ] **Current-link highlighting** — `.up-current` on nav links; `up-alias`. *[client]*
- [ ] **Animations** — `up-transition="cross-fade"`, `up-animation` on layers. *[client]*
- [ ] **Scroll behaviour** — `up-scroll="target"`, `"reset"`, revealing an element after update. *[client]*
- [ ] **Focus management** — `up-focus`; confirm keyboard/screen-reader behaviour after a swap. *[client]*
- [ ] **Flash messages** — Django `messages` framework rendered into a `.flash` fragment that is
      always included in updates (`up-hungry`). *[server, client]*

## 6. Advanced fragment updates

- [ ] **`up-hungry`** — a fragment that updates whenever it appears in any response (nav counter, flash). *[client]*
- [ ] **`up-poll`** — periodically refresh a fragment (e.g. task status). *[client, server]*
- [ ] **Deferred / lazy loading** — `up-defer` to load a slow partial after the page renders. *[client, server]*
- [ ] **`up-keep`** — preserve an element (video, third-party widget) across swaps. *[client]*
- [ ] **Compilers** — `up.compiler('.datepicker', ...)` to initialise JS widgets on newly inserted
      fragments; `up.destructor` for cleanup. *[client]*
- [ ] **Data attributes** — `up-data` passed into compilers. *[client]*
- [ ] **Events** — `up:fragment:loaded`, `up:request:late` (show "slow" banner), `up:link:follow`. *[client]*
- [ ] **JS API** — `up.render()`, `up.reload()`, `up.request()` from custom JS. *[client]*

## 7. Server-side integration (Django)

- [ ] **Header helper** — small util / middleware exposing `request.up.target`, `.mode`, `.validate`,
      `.layer`, etc. Possibly compare with an existing package. *[server]*
- [ ] **Response helper** — functions to set `X-Up-Accept-Layer`, `X-Up-Expire-Cache`, `X-Up-Events`. *[server]*
- [ ] **Server-sent events** — `X-Up-Events` header to emit `up:` events from a response. *[server, client]*
- [ ] **Error pages** — how Unpoly handles 404/500 HTML from Django (`up-fail-target`, `up.network.config.fail`). *[server, client]*
- [ ] **Login redirect** — hitting a `@login_required` view from a fragment link; ensure the login
      page renders correctly inside/outside layers. *[server, client]*

## 8. Capstone mini-app

Combine everything in a small CRUD app (e.g. **Tasks** or **Notes**):

- List page with search (autosubmit), pagination via fragment links, and a "new" button opening a modal.
- Create/edit forms in modals with live validation; on save close the layer and update the list.
- Delete with confirmation (`up-confirm`) and flash message via `up-hungry`.
- Task status polling for a "running" state.
- Full progressive enhancement: everything still works with JS disabled.

---

## Notes / questions to resolve while practising

### Learned so far

- **Partial responses must still be full documents if you want `<title>` updated.** Unpoly only reads
  `<title>`/`<head>` from a response whose first tag is `<!DOCTYPE` or `<html>` (see `up.ResponseDoc`).
  A bare `<main>` response swaps fine but leaves the tab title stale. `templates/partial.html` is
  therefore a minimal `<html><head><title></head><body><main></body></html>`. Alternative: send an
  `X-Up-Title` response header (JSON-encoded string).
- Pattern for one view serving both full and fragment responses: page templates
  `{% extends "base.html" %}`, and `base.html` is a one-liner `{% extends base_template %}` where a
  context processor sets `base_template` to `layout.html` or `partial.html` based on `X-Up-Target`.
- `.up-current` is applied to nav links matching the current URL with zero configuration.

- Best way to serve both full-page and fragment-only responses from one view.
- Whether a `django-unpoly` style package is worth it vs. a 30-line helper.
- How Django's `422`/`400` for form errors interacts with `up.network.config.fail`.
