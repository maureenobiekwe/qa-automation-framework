# QA Automation Framework

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

## Design choices

- **Page objects** in `pages/` hold locators and actions. Tests hold the assertions.
- **Locators use `data-test` attributes** through `get_by_test_id` (configured in `tests/conftest.py`), not CSS or XPath chains, so layout changes don't break tests.
- **Web-first assertions** (`expect(...)`) auto-wait. No fixed sleeps.
- **Parametrised negative cases** keep each rule visible in the report as its own test id.
- **Markers** (`smoke`, `regression`, `negative`, `api`) let you run a slice: `pytest -m smoke`.
- **Traces and screenshots** are kept on failure under `test-results/` and uploaded as a CI artifact.

## Run it

```bash
python -m venv .venv
.venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

pytest                        # everything
pytest -m smoke               # critical path only
pytest --headed               # watch the browser
pytest --browser firefox      # run on another engine (after: playwright install firefox)
```

Open a failure trace with `playwright show-trace test-results/<test>/trace.zip`.

## CI

`.github/workflows/tests.yml` runs the suite on every push to `main`, on pull
requests, and on demand.

## Known limits

- SauceDemo and JSONPlaceholder are shared public sites. Rarely, a run fails on a network error rather than a product bug. Rerun before raising a defect.
- JSONPlaceholder fakes writes: the POST test checks the response only, not persistence.
- Not covered yet: the problem and performance-glitch demo users, visual checks, accessibility checks, parallel runs.

## Ideas for next steps

- Add `problem_user` and `performance_glitch_user` cases and report the defects found.
- Add `axe-core` accessibility checks to the inventory and checkout pages.
- Run in parallel with `pytest-xdist` and publish an HTML report.
