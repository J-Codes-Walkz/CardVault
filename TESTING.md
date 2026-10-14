# Testing

Testing for [CardVault](./README.md): manual tests against each user story, the automated test suite, validator results and the bug log. Live site: [cardvault-0a18b8d773ca.herokuapp.com](https://cardvault-0a18b8d773ca.herokuapp.com/).

*This section needs real results once the app exists. The structure
below is ready to fill in.*

## Manual testing

Each user story's "Manual test" entry in `docs/USER_STORIES.md` is a
ready-made test case. Record results in a table like this (one row
per story, updated as you test):

| Story | Action | Expected | Actual | Pass? |
|---|---|---|---|---|
| US01 | Register with a new username and a strong password, then a duplicate username | New account created with success message; duplicate shows the "already taken" error | | |
| US02 | Log in with valid, then invalid, credentials | Welcome message + redirect; then the invalid-credentials error | | |
| &hellip; | | | | |

## Automated testing

Django's test runner (`python manage.py test`) should cover, at
minimum, one test per acceptance criterion that isn't purely visual:
registration (duplicate username, weak password, mismatched
passwords), login (valid/invalid), ownership checks (user B cannot
edit/delete user A's records &mdash; this is the most
important test in the whole suite, since it's a security boundary,
not just a feature), and the CRUD paths for `CollectionEntry`
(both the Owned and Wanted status) and `Review`.

**Current state (12 October 2026, end of Sprint 1 build):** 45
automated tests, all passing, covering registration (valid, duplicate
username, each of the four password rules, mismatched passwords),
login (valid, wrong password, unknown username, return to the
requested page), logout (POST logs out, GET does not, private pages
then redirect), the navigation's two states, every model constraint,
and the Base Set fixture loading twice without duplicates. They live
in `accounts/tests.py`, `cards/tests.py` and `collection/tests.py`.

Run with coverage:

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report -m
```

## Validators

- **HTML**: run every rendered template through the
  [W3C HTML validator](https://validator.w3.org/) (paste the page
  source, or validate by URL once deployed).
- **CSS**: run your stylesheet through
  [Jigsaw](https://jigsaw.w3.org/css-validator/).
- **Python**: `pip install flake8` and run `flake8 .` from the
  project root; fix or justify every warning (PEP8 line length is 79
  characters &mdash; see the note on wrapping model fields in
  [docs/DATABASE_SCHEMA.md](./docs/DATABASE_SCHEMA.md#pep8-and-the-models)).
- **Accessibility/performance**: run Lighthouse (Chrome DevTools) on
  each major page, logged in and out, and record the four scores.

Results so far (12 October 2026, run against the local site):

| Check | Scope | Result |
|---|---|---|
| W3C HTML validator | Home, Register, Log in, Log in with an error, Log out, My Cards | 0 errors, 0 warnings on each page |
| Jigsaw CSS validator | `static/css/style.css` | 0 errors (1 warning: `system-ui` is flagged as a vendor extension) |
| flake8 | Whole project (migrations excluded in `.flake8`) | 0 warnings |
| `manage.py check --deploy` | Production settings | 0 issues |

The home, register and log in pages were validated again by URL on
the live site after deployment, with the same result (0 errors).

*Re-run all of these on the finished site and add screenshots before
submission.*

## Known bugs

*(none logged yet)*
