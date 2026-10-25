# Test data rules

Follows the six data categories and the automation-suitability test in the QA Fundamentals and Standards Training Guide.

| Data | Category | Reset method | Used by |
|---|---|---|---|
| `standard_user`, `locked_out_user`, `problem_user`, `performance_glitch_user` (public SauceDemo accounts) | Fixed baseline | None needed: the site keeps no server-side state | UI tests |
| Cart contents and checkout details | Disposable | Each test gets a fresh browser context, so the cart starts empty | UI tests |
| JSONPlaceholder posts and users | Fixed baseline | Read-only: writes are faked and never persist | API tests |
| Payloads built inside tests | Disposable | Created per test | API tests |

## Suitability check

A data item is automated only if it is stable, has a known starting state, cannot be changed by manual testing mid-cycle, has a reset method, exposes no secrets, and lets a data failure be told apart from a product defect. All data above passes. The demo password is a public credential published on saucedemo.com.

## Rules for adding tests

- No real user data, ever. Secrets come from environment variables or GitHub Secrets, never from code.
- A test whose data fails the check above is marked `provisional` or left out. It is not shipped as green.
- Known product defects use `xfail(strict=True)` with the defect in the reason, so the run stays green and a fix is noticed.
