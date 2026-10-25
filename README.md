# QA Automation Framework
![tests](https://github.com/maureenobiekwe/qa-automation-framework/actions/workflows/tests.yml/badge.svg)
![api-regression](https://github.com/maureenobiekwe/qa-automation-framework/actions/workflows/api-regression.yml/badge.svg)


You can check out other repos: https://github.com/maureenobiekwe/qa-autopilot

https://github.com/maureenobiekwe/qa-playbook

Playwright + pytest suite in Python, using the Page Object Model. It covers the
SauceDemo web shop (UI) and the JSONPlaceholder API. Both are public demo
sites, so no real or client data is involved.

## What it covers

| Area | Tests | Types |
|---|---|---|
| Login | valid login, locked-out user, 5 invalid-credential cases, direct URL access without login | smoke, negative |
| Inventory | sort by price (both directions) and name, cart badge on add/remove | regression |
| Checkout | full purchase, total = subtotal + tax, 3 missing-field validations | smoke, regression, negative |
| API | list, get, 404, create, filter by user | api |
| API contract | JSON schema on one and all posts, response-time threshold, chained flow, update/delete, invalid IDs | api, performance, negative |
| API security | 5000-character payload, script in a field, sensitive fields in a response | security |
| Accessibility | axe-core WCAG 2.1 AA scan of login and inventory, keyboard-only login, focus indicator | a11y |
| Faulty demo users | `problem_user` images and sorting, `performance_glitch_user` login time | regression, performance |

## Design choices

- **Page objects** in `pages/` hold locators and actions. Tests hold the assertions.
- **Locators use `data-test` attributes** through `get_by_test_id` (configured in `tests/conftest.py`), not CSS or XPath chains, so layout changes don't break tests.
- **Web-first assertions** (`expect(...)`) auto-wait. No fixed sleeps.
- **Parametrised negative cases** keep each rule visible in the report as its own test id.
- **Markers** (`smoke`, `regression`, `negative`, `api`) let you run a slice: `pytest -m smoke`.
- **Strict xfail for known defects.** A defect found in the demo site is recorded as `xfail(strict=True)` with the reason, so the run stays green and a fix is noticed.
- **Test data rules** are in [docs/TEST_DATA.md](docs/TEST_DATA.md).
- **Traces and screenshots** are kept on failure under `test-results/` and uploaded as a CI artifact.

## Run it

```bash
python -m venv .venv
.venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

pytest                        # everything
pytest -m smoke               # critical path only
pytest -m "a11y or security"  # accessibility and security slice
pytest -n auto                # run in parallel
k6 run perf/posts_load.js     # API load test (5 users, 35 s, thresholds on p95 and errors)
pytest --headed               # watch the browser
pytest --browser firefox      # run on another engine (after: playwright install firefox)
```

An HTML report is written to `reports/report.html` on every run. Open a failure trace with `playwright show-trace test-results/<test>/trace.zip`.

## CI

`.github/workflows/tests.yml` runs the suite in parallel on every push to `main`, on pull
requests, and on demand. The HTML report is uploaded on every run, traces and screenshots on failure.

## Known limits

- SauceDemo and JSONPlaceholder are shared public sites. Rarely, a run fails on a network error rather than a product bug. Rerun before raising a defect.
- JSONPlaceholder fakes writes: the POST test checks the response only, not persistence.
- axe-core is automated and finds about a third of accessibility issues. Screen-reader and zoom checks are still manual.
- Not covered yet: visual regression, cross-browser runs in CI, k6 in CI.

## Performance

- **k6** (`perf/posts_load.js`): 5 virtual users for 35 s against JSONPlaceholder. Last run: 200 requests, 0% errors, 400/400 checks, p95 290 ms against an 800 ms threshold. The load is kept small because the service is public.
- **Lighthouse**: method, thresholds and measured scores for the login page are in [docs/LIGHTHOUSE.md](docs/LIGHTHOUSE.md).

## Findings so far

- `problem_user`: every product shows the same image, and sorting does nothing.
- Login page: the username field has no visible focus indicator (WCAG 2.4.7).

## Ideas for next steps

- Run Lighthouse on the inventory and checkout pages (needs a logged-in session).
- Add visual regression snapshots and a Firefox/WebKit matrix in CI.
