// Load test for the JSONPlaceholder API (public demo service: keep the load small).
// Run: k6 run perf/posts_load.js
import http from "k6/http";
import { check, sleep } from "k6";

const BASE = "https://jsonplaceholder.typicode.com";

export const options = {
  stages: [
    { duration: "10s", target: 5 }, // ramp up
    { duration: "20s", target: 5 }, // hold: expected traffic
    { duration: "5s", target: 0 }, // ramp down
  ],
  thresholds: {
    http_req_failed: ["rate<0.01"], // under 1% errors
    http_req_duration: ["p(95)<800"], // p95 under 800 ms
    checks: ["rate>0.99"],
  },
};

export default function () {
  const list = http.get(`${BASE}/posts`);
  check(list, {
    "list is 200": (r) => r.status === 200,
    "list has 100 posts": (r) => r.json().length === 100,
  });

  const one = http.get(`${BASE}/posts/${1 + Math.floor(Math.random() * 100)}`);
  check(one, {
    "post is 200": (r) => r.status === 200,
    "post has id and title": (r) => r.json().id > 0 && r.json().title !== "",
  });

  sleep(1);
}
