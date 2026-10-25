# API regression with Postman and Newman

A small collection that runs in CI against a public demo API (JSONPlaceholder). It shows the pattern I use on real projects:

- **Exact status codes.** Each test asserts one code (200, 201, 404), never "any 2xx", so a wrong code fails.
- **Chaining.** TC-02 saves `userId` from one response and TC-03 uses it, so the tests prove the data links up.
- **A unique id per run** (`runId`) on created data, so parallel or repeated runs never collide.
- **Response-time check** on the read endpoints.
- **No secrets in files.** The target is public. For a private API the workflow shows how to pass credentials from repository secrets.
- **Pinned Newman major (`newman@6`)** and a JUnit report uploaded as a build artifact.

JSONPlaceholder fakes writes (a POST is echoed but not stored), so the write tests check the response only.

## Run it

```bash
npx newman@6 run api-regression/demo-api.postman_collection.json -e api-regression/demo.postman_environment.json
```

Last run: 8 requests, 19 assertions, 0 failed.

## Files

- `demo-api.postman_collection.json`: the 8 test cases (TC-01 to TC-08).
- `demo.postman_environment.json`: `baseUrl` only.
- `../.github/workflows/api-regression.yml`: runs on push, pull request, a weekday schedule and by hand.
