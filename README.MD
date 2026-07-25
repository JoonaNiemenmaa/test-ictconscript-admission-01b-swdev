# Software Development Backend API Task Submission

This is my submission for the ICT-conscript admission test.

The implementation is done with FastAPI and SQLModel. All project files can be found in ```./submission```

The app can be found deployed at https://logbook-production-347d.up.railway.app/

As this is a FastAPI application the API documentation can be accessed at https://logbook-production-347d.up.railway.app/docs

## Unit Tests

The submission includes four unit tests as one of the stretch goals.

Additional dependencies needed for the unit tests can be installed with ```submission/test_requirements.txt``` like so

```sh
$ pip install -r test_requirements.txt
```

And the tests can be run as follows

```sh
$ pytest tests.py
```

## Completed Requirements

All functional requirements and stretch goals have been implemented.

| ID | Requirement |
|----|-------------|
| **B-1** | **Database** to persist log entries. Example of what data should be held is at `sample-data/data.json`. |
| B-2 | `GET /entries` returns all entries, newest first (JSON array). |
| B-3 | `GET /entries/<id>` returns a single entry or `404` if not found. |
| B-4 | `POST /entries` accepts JSON:<br>  `title` (string ≤ 120),<br>  `body` (string),<br>  optional `lat`, `lon` (numbers).<br>The server assigns `id` and `isoTime`, inserts row, and returns it. |
| B-5 | `GET /health` returns status 200, body `"OK"`. |

| Idea | Hint |
|------|------|
| Unit tests  | ≥ 2 tests (e.g. pytest, Jest, Go test) covering happy & error paths. |
| CI pipeline | GitHub Actions: build image, run tests, push to container/image repo of choice. |
