# OWL Component Design — `direct_print_auto`

## Component overview

| Property | Value |
|----------|-------|
| Class name | `DirectPrintAction` |
| Registry | `@web/core/registry` → `actions` category |
| Tag | `direct_print_auto` |
| Template | inline `xml` tagged-template literal |
| File | `static/src/js/direct_print_action.js` |
| Template bundle file | `static/src/xml/direct_print_templates.xml` (placeholder) |

---

## Why a client action (not a service / not a component on the form view)?

A **client action** is Odoo's standard mechanism for "an action that
takes over the main content area". It's the right choice here because:

1. **Server-side trigger** — When the server returns
   `{type: "ir.actions.client", tag: "direct_print_auto", params: {...}}`,
   Odoo's web client automatically looks up the OWL component registered
   under `tag` and instantiates it with `props.action = the_dict`. This
   is the cleanest way to bridge the server-side override (which decides
   *whether* to print) with the browser-side print dialog (which actually
   does the printing).

2. **Full-screen takeover** — A client action occupies the main content
   area, which means we can show a loading spinner while the report
   HTML is being fetched, then a success message after the print dialog
   closes. This is far better UX than silently printing in the
   background with no feedback.

3. **Clean lifecycle** — The component's `setup()` runs once on
   instantiation, `onWillStart` runs before the first render, and the
   component is destroyed when the next action is dispatched. This
   gives us clear hooks for setup and teardown.

---

## Component API

### Props

```js
this.props.action = {
  type: "ir.actions.client",
  tag: "direct_print_auto",
  name: "Direct Print",
  params: {
    report_ref:  "sale.action_report_saleorder",   // required
    res_model:   "sale.order",                      // required
    res_ids:     [42],                              // required, ≥1
    next_action: <action dict> | false              // optional
  }
}
```

### State

```js
this.state = {
  loading: true,        // show spinner while report loads
  error:   false,       // error message string, or false
  frameSrc: ""          // URL assigned to iframe.src
}
```

### Methods

| Method | Purpose |
|--------|---------|
| `setup()` | OWL lifecycle hook — initializes services, state, and calls `_preparePrint()` via `onWillStart` |
| `_preparePrint()` | Reads params, validates them, builds the `/report/html/...` URL, assigns it to `state.frameSrc` |
| `onFrameLoad()` | Bound to the iframe's `load` event via `t-on-load` in the template. Calls `iframe.contentWindow.print()` after a 350ms delay (to let report CSS/fonts settle). After the print dialog closes, schedules `_dispatchNext()` after 400ms. |
| `_dispatchNext()` | Reads `params.next_action`. If truthy, dispatches it via `actionService.doAction()`. Otherwise dispatches `ir.actions.act_window_close` to close the client action. |
| `onClose()` | Bound to the "Close" button on the error view. Dispatches `ir.actions.act_window_close`. |

---

## Template

```js
const DIRECT_PRINT_TEMPLATE = xml`
    <div class="o_direct_print_auto d-flex flex-column align-items-center justify-content-center"
         style="min-height: 60vh;">
        <t t-if="state.error">
            <div class="alert alert-danger" role="alert">
                <t t-esc="state.error" />
            </div>
            <button class="btn btn-secondary mt-3" t-on-click="onClose">Close</button>
        </t>
        <t t-elif="state.loading">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading…</span>
            </div>
            <p class="mt-3 text-muted">Preparing print preview…</p>
        </t>
        <t t-else="">
            <i class="fa fa-check-circle text-success" style="font-size: 3rem;"></i>
            <p class="mt-3 text-muted">Print dialog closed. Continuing…</p>
        </t>
        <iframe t-ref="printFrame"
                t-on-load="onFrameLoad"
                style="position: absolute; width: 0; height: 0; border: 0; left: -9999px; top: -9999px;"
                t-att-src="state.frameSrc" />
    </div>`;
```

### Template decisions

1. **Three-state template** (`error` / `loading` / `done`) — gives
   the user clear feedback at each stage.

2. **Hidden iframe** — positioned at `left: -9999px; top: -9999px`
   with 0×0 dimensions. This is more reliable than `display: none`
   (which can prevent the iframe from loading in some browsers) or
   `visibility: hidden` (which can interfere with `contentWindow.print()`
   in older Chrome versions).

3. **`t-on-load`** — OWL's event binding syntax. The iframe's `load`
   event fires when the report HTML has been fetched and rendered
   inside the iframe.

4. **`t-ref="printFrame"`** — OWL's ref system. `useRef("printFrame")`
   gives us a reactive reference to the iframe DOM element, accessed
   via `this.printFrame.el`.

---

## Timing decisions

### 350ms delay before `print()`

When the iframe's `load` event fires, the report HTML has been fetched
but the report's own CSS and fonts may still be loading. Calling
`print()` immediately can produce a print-out with unstyled text
(the report's CSS hasn't applied yet) or with the wrong fonts.

The 350ms delay is empirically calibrated to be long enough for
Odoo's standard QWeb report CSS to apply, while short enough that
the user doesn't perceive a delay between clicking "Confirm" and
seeing the print dialog.

If your deployment uses heavy custom report CSS or web fonts, you
may need to increase this delay. The constant is at the top of
`onFrameLoad()`.

### 400ms delay before `_dispatchNext()`

After `print()` returns (which happens when the user closes the
print dialog), the browser's print pipeline is still cleaning up.
Dispatching the next action immediately can cause the iframe to be
removed from the DOM while the browser is still finalizing the
print job, which can cause silent failures.

The 400ms delay gives the browser time to finish before we navigate
away. This value is also empirically calibrated and may need
adjustment for very slow clients.

---

## Error handling

| Error case | How it's handled |
|------------|------------------|
| Missing `report_ref` or `res_ids` in params | `state.error` set, error message shown, user can click Close |
| Iframe fails to load (e.g. 403 ACL error, 404 missing report) | The `load` event still fires (with an error page inside the iframe), so `onFrameLoad()` runs. We don't currently distinguish between successful load and error-page load — the print dialog will open with the error page content. **Future improvement:** check `iframe.contentDocument.title` or the response status before calling `print()`. |
| `print()` throws (rare — happens in some embedded browsers) | Caught by `try/catch`, `state.error` set, user can click Close |
| `next_action` is malformed | `actionService.doAction()` will raise, which is caught by Odoo's standard error handler and shown as a red notification |

---

## Why the template is inline (not in the XML bundle file)

OWL supports two ways to define a component's template:

1. **Inline via `xml\`...\``** tagged-template literal in the JS file —
   what we use.
2. **In a separate `.xml` file** bundled via `web.assets_backend` —
   what the empty `direct_print_templates.xml` file is a placeholder
   for.

We chose inline because:

- The template is small (~30 lines) and tightly coupled to the
  component's state shape — separating it would just add a file hop.
- Inline templates are easier to refactor (you can see the template
  and the component logic in the same file).
- The XML bundle file is still present (and listed in `assets`) for
  future expansion — if the component grows sub-components with
  their own templates, those templates can live in the XML file
  without restructuring the JS.

---

## Browser compatibility

| Browser | Status | Notes |
|---------|--------|-------|
| Chrome 90+ | ✅ Full support | `iframe.contentWindow.print()` works as expected |
| Firefox 88+ | ✅ Full support | Same |
| Edge 90+ | ✅ Full support | Same (Chromium-based) |
| Safari 14+ | ⚠️ Partial | `iframe.contentWindow.print()` works but may open a separate print window instead of a dialog. The 400ms post-print delay may need to be increased. |
| Mobile browsers | ⚠️ Limited | Most mobile browsers either don't support `iframe.print()` or route it to a "save as PDF" flow. The module is designed for desktop use. |
| Embedded webviews (Electron, CEF) | ⚠️ Depends | Some embedded webviews disable `window.print()` for security. Test before deploying. |
