# Lighthouse test method

Lighthouse is a lab audit of one page load. It scores performance, accessibility, best practices and SEO. It does not pass or fail anything by itself: the pass/fail line is the threshold this document sets.

Based on QA Master Guide Playbook E (k6 + Lighthouse). Target pages: login, inventory, cart and checkout on SauceDemo.

## How a run is done

1. Open the page in an incognito window (extensions skew scores).
2. DevTools (F12) > Lighthouse tab. Choose Mobile, then repeat on Desktop. Tick Performance, Accessibility, Best practices, SEO. Click Analyze page load.
3. Command-line alternative, same engine:
   ```bash
   npm install -g lighthouse
   lighthouse https://www.saucedemo.com/ --preset=desktop --output=html --output=json --output-path=reports/lighthouse-login --chrome-flags="--headless"
   ```
   For a page behind login, use the DevTools "Timespan"/"Snapshot" modes after logging in, or Lighthouse CI with a Puppeteer login script.
4. Run each page 3 times and record the median. A single run varies by network and CPU.
5. Run once locally and once from CI. If both are slow, the page or server is slow. If only local is slow, it was the local network.
6. Save the HTML report as evidence and log the scores in the test summary.

## The four category scores (0 to 100)

| Score | Band | Meaning | Verdict |
|---|---|---|---|
| 90 to 100 | Good | Meets recommended practice | Pass |
| 50 to 89 | Needs improvement | Works, but users or search ranking are affected | Pass with a logged issue (Medium) |
| 0 to 49 | Poor | Real user impact | Fail, raise a defect (High) |

Project thresholds: Performance >= 80, Accessibility >= 90, Best Practices >= 90, SEO >= 80. Below the line is a fail.

## The metrics behind the Performance score

| Metric | What it measures | Good (pass) | Needs improvement | Poor (fail) |
|---|---|---|---|---|
| FCP, First Contentful Paint | Time until anything appears | <= 1.8 s | 1.8 to 3.0 s | > 3.0 s |
| LCP, Largest Contentful Paint | Time until the main content appears | <= 2.5 s | 2.5 to 4.0 s | > 4.0 s |
| TBT, Total Blocking Time | Time the page is frozen and ignores clicks (stands in for INP in the lab) | <= 200 ms | 200 to 600 ms | > 600 ms |
| CLS, Cumulative Layout Shift | How much content jumps while loading | <= 0.1 | 0.1 to 0.25 | > 0.25 |
| Speed Index | How quickly the page fills visually | <= 3.4 s | 3.4 to 5.8 s | > 5.8 s |

LCP, CLS and INP are the Core Web Vitals. A fail on any of them is reported even if the overall score is above 80.

## What each result means for the report

- **Pass:** all four category scores and all Core Web Vitals meet the thresholds on the median run.
- **Pass with issues:** a score is in the "needs improvement" band or a non-core metric (FCP, Speed Index) misses its target. Log it as Medium or Low and carry on.
- **Fail:** a category score is under its threshold, or LCP, CLS or TBT is in the poor band. Raise a defect with the report attached, the device preset, the median values, and the failing audit names (for example "Largest Contentful Paint element" or "Eliminate render-blocking resources").
- **Invalid run:** scores swing by more than 10 points between runs, or Lighthouse reports a flagged-run warning. Rerun before raising a defect, as with network flakes.

## Limits to state in every report

- Lab data, one device profile, one location. It is not what real users see.
- The Accessibility score is automated only. It overlaps with the axe tests and does not replace manual screen-reader checks.
- Scores depend on the machine. Compare runs on the same machine, or compare like with like in CI.

## Results: SauceDemo login page (25 Oct 2026, Lighthouse 13.5.0, median of 3 runs, headless Chrome, local machine)

| Measure | Desktop | Verdict | Mobile | Verdict |
|---|---|---|---|---|
| Performance | 77 | Fail (threshold 80, "needs improvement" band) | 80 | Pass (on the line) |
| Accessibility | 100 | Pass | 100 | Pass |
| Best Practices | 81 | Fail (threshold 90) | 81 | Fail |
| SEO | 63 | Fail (threshold 80) | 63 | Fail |
| FCP | 2.08 s | Needs improvement | 3.42 s | Poor |
| LCP | 2.08 s | Good | 3.86 s | Needs improvement |
| TBT | 0 ms | Good | 38 ms | Good |
| CLS | 0.002 | Good | 0.005 | Good |
| Speed Index | 2.29 s | Good | 4.26 s | Needs improvement |

Run-to-run spread was 2 to 4 points, so the runs are valid. No Core Web Vital is poor, so the page is not a Core Web Vitals fail.

Audits behind the failures: "Page is blocked from indexing" (SEO), "Uses deprecated APIs", "Missing source maps for large first-party JavaScript" and "Page prevented back/forward cache restoration" (Best Practices). SauceDemo is a demo site, so the indexing block is intended. Treat the SEO result as informational, not a defect.

Mobile FCP is the one metric in the poor band. It runs on Lighthouse's throttled mobile profile, so confirm on a second machine before raising it.

Raw JSON for each run is in `reports/lh-*.json` (git-ignored).
