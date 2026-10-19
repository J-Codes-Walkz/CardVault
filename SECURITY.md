# Security policy

CardVault is a student project, but it holds real accounts, so
security reports are welcome and taken seriously.

## Supported versions

Only the live site and the `main` branch are supported. Fixes are
made on `main`, which deploys to the live site automatically.

| Version | Supported |
|---|---|
| Live site: [cardvault-0a18b8d773ca.herokuapp.com](https://cardvault-0a18b8d773ca.herokuapp.com/) | Yes |
| `main` branch | Yes |
| Any older commit | No |

## How CardVault protects you

No website can promise to be unhackable. These are the layers in
place, reviewed on 15 October 2026
([issue #50](https://github.com/J-Codes-Walkz/CardVault/issues/50))
and hardened on 19 October 2026
([issue #68](https://github.com/J-Codes-Walkz/CardVault/issues/68)).
The README's
[Security architecture](./README.md#security-architecture) section
shows how the layers fit together.

### What CardVault stores

Only a username, a password (stored as a salted PBKDF2 hash, never as
the password itself), and the cards and reviews you add. No email
address, real name or payment details are collected for an account
(the Contact page asks for a name and email address only so a reply
can be sent, and they are deleted once the enquiry is dealt with), and the date of
birth asked for at registration (to refuse under-13s) is checked and
thrown away, never stored. There is very little personal data to
lose, and you can delete all of it yourself (Delete my account, in
the footer). The site's own
[Privacy and cookies page](https://cardvault-0a18b8d773ca.herokuapp.com/privacy/)
explains this for users.

### Logging in

- Passwords must pass Django's four checks: at least 8 characters,
  not too common, not all numbers, not too like the username.
- Password guessing is rate limited by django-allauth: 3 wrong
  passwords lock that username for 15 minutes, whichever addresses
  they come from. One IP address may get 5 passwords wrong a minute
  and 20 an hour across any usernames, try to log in 10 times a
  minute, and register 10 accounts an hour. The limits are stored in
  the database, so they apply across every web process.
- Each limit counts the visitor's real IP address: the last entry of
  `X-Forwarded-For`, which Heroku's router adds and a visitor cannot
  fake (`ALLAUTH_TRUSTED_PROXY_COUNT = 1`).
- A failed log in never says whether the username or the password was
  wrong.
- The Django admin's own log in form is switched off: admin log ins go
  through the same rate-limited page, and only staff accounts can
  open the admin.
- Log out is a POST request with a CSRF token, so another site cannot
  log you out.

### Your data

- Every private page requires you to be logged in, and every query for
  your entries and reviews is filtered to your account: changing the ID
  in the address bar to someone else's record gives a 404 page. Two-user
  automated tests check this for viewing, editing and deleting.
- Every form is protected against cross-site request forgery (CSRF).
- The Contact page has a hidden trap field that bots fill in and
  people never see, and each visitor can send 5 messages an hour. The
  limit is kept against a one-way hash of the visitor's IP address,
  never the address itself. CardVault sends no email, so the form
  cannot be used to send mail to other people.
- The database is only reached through Django's ORM (no hand-written
  SQL), which prevents SQL injection.
- Django escapes everything users type before showing it, and a
  Content Security Policy stops the browser running any script that is
  not one of the site's own files, as a second line of defence against
  cross-site scripting.

### Heavy traffic

- gunicorn runs 2 workers with 4 threads each, and restarts each
  worker after about 1,000 requests.
- Postgres stops any query still running after 10 seconds, and
  searches are cut to 100 characters and 5 words.
- A load test of 2,000 visits to the live site, 25 at a time, had no
  errors (see TESTING.md).

### The database

- Reached only with the `DATABASE_URL` in Heroku's config vars, over
  TLS; Heroku encrypts the data on disk.
- Backed up daily at 03:00 UK time (`heroku pg:backups:schedule`).
- If the database password ever leaked, `heroku pg:credentials:rotate`
  replaces it.
- Expired rate limit notes, which hold IP addresses, are deleted on
  every release by `python manage.py clear_expired_cache`.

### The connection and the browser

- HTTPS only: plain HTTP is redirected, and HSTS tells browsers to use
  HTTPS for a year.
- Session and CSRF cookies are sent over HTTPS only and cannot be read
  by JavaScript.
- Pages cannot be shown inside another site's frame (clickjacking).
- A Permissions Policy turns off the camera, microphone, location and
  payment features the site never uses.
- `DEBUG` is off on the live site, so errors never show code or
  settings.

### Secrets, code and dependencies

- No secret is in the code or its history. `SECRET_KEY` and the
  database address live only in a local `.env` file (ignored by git)
  and in Heroku config vars. The whole git history was scanned for
  keys, tokens and passwords on 15 October 2026: none found.
- The site calls no outside API, so there is no API key to steal. Card
  data came from the Pokémon TCG API once, when the fixture was built.
- GitHub secret scanning with push protection blocks a push that
  contains a recognised key or token.
- Dependabot watches the pinned packages in `requirements.txt` and opens
  a pull request when a security fix is released. `pip-audit` found no
  known vulnerabilities on 15 October 2026.
- CodeQL scans the Python and JavaScript for security problems on every
  push.
- The `main` branch cannot be force-pushed or deleted.

## Reporting a vulnerability

Please report security problems **privately**, not in a public issue:

1. Open the repository's **Security** tab.
2. Choose **Report a vulnerability**
   ([direct link](https://github.com/J-Codes-Walkz/CardVault/security/advisories/new)).
3. Describe the problem, the page or URL involved, the steps to
   reproduce it, and what an attacker could do with it.

You will get a reply within 3 days. Once a fix is live, the report
is logged in [TESTING.md](./TESTING.md) under Bugs, crediting you if
you would like to be named.

## In scope

- The live site: accounts, My Cards, reviews and anything that lets
  one user see, change or delete another user's data.
- The code in this repository, including any secret committed by
  mistake.

## Out of scope

- Denial-of-service or high-volume automated scanning of the live
  site.
- Problems in Heroku, GitHub or Django themselves (please report
  those to the project concerned).
- Social engineering or physical attacks.

## Rewards

This is an educational project, so there is no paid bounty. Valid
reports are credited in the bug log, with thanks.

## Bugs that are not security issues

Open an issue using the **Bug report** template. Every bug is tracked
as an issue labelled
[`bug`](https://github.com/J-Codes-Walkz/CardVault/issues?q=label%3Abug)
and closed by the commit that fixes it.
