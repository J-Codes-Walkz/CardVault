# Testing

Testing for [CardVault](./README.md). Live site:
[cardvault-0a18b8d773ca.herokuapp.com](https://cardvault-0a18b8d773ca.herokuapp.com/).

CardVault is tested in four ways:

| Method | What it covers | Result (14 October 2026) |
|---|---|---|
| [Manual testing](#manual-testing) | Every front-end action a user can take, done in a real browser on the live site | 39 of 39 checks passed |
| [Responsive testing](#responsive-testing) | Layout at 320, 375, 768, 1024 and 1440px | No sideways scrolling at any width |
| [Automated testing](#automated-testing) | 96 Django tests, including two-user ownership tests | 96 passed |
| [Validators](#validators) | HTML (W3C), CSS (Jigsaw), JavaScript, Python (PEP8) | 0 errors |

Every bug found is logged as a GitHub issue labelled `bug`; see
[Bugs](#bugs).

## Manual testing

### How the tests were run

Each test below follows a user story's "Manual test" in
[docs/USER_STORIES.md](./docs/USER_STORIES.md), using only the front
end (no Django admin). The tests were run on the live Heroku site on
14 October 2026 by driving a real Chrome browser with a script: it
typed into the same fields and pressed the same buttons a person
would, checked what the page showed afterwards, and took the
screenshots linked below. A throwaway account, `cardvault_tester`,
was registered for the run and deleted afterwards.

Catalogue cards used: the three tester cards **AAA**, **BBB** and
**CCC** from `cards/fixtures/tester_cards.json` (see
[Populating the catalogue](./docs/DATABASE_SCHEMA.md#populating-the-catalogue)).

Jamie also registered, logged out and logged in by hand on the live
site on 12 October 2026, with the expected message at each step
([issue #40](https://github.com/J-Codes-Walkz/CardVault/issues/40)).

### Accounts (US01 to US05)

| Story | Test | Expected | Result | Screenshot |
|---|---|---|---|---|
| US05 | Open My Cards while logged out | Sent to Log in with "Please log in to view that page." | Pass | [login-required-message](./docs/images/screenshots/login-required-message.png) |
| US01 | Register with the password `abc12` | No account; error names the rule broken ("too short") | Pass | [register-weak-password](./docs/images/screenshots/register-weak-password.png) |
| US01 | Register with two different passwords | No account; "You must type the same password each time." | Pass | [register-password-mismatch](./docs/images/screenshots/register-password-mismatch.png) |
| US01 | Register with a new username and a strong password | Logged in, "Your account has been created. Welcome to CardVault, cardvault_tester!" | Pass | [register-success](./docs/images/screenshots/register-success.png) |
| US04 | Look at the navigation after registering | "Logged in as cardvault_tester", My Cards and Log out | Pass | [register-success](./docs/images/screenshots/register-success.png) |
| US03 | Log out | "You have been logged out. See you soon!" | Pass | [logout-success](./docs/images/screenshots/logout-success.png) |
| US02 | Log in with a wrong password | "Invalid username or password. Please try again." | Pass | [login-invalid](./docs/images/screenshots/login-invalid.png) |
| US02 | Log in with the right password | "Welcome back, cardvault_tester!" and My Cards | Pass | [login-success](./docs/images/screenshots/login-success.png) |

### Browsing cards (US06 to US10)

| Story | Test | Expected | Result | Screenshot |
|---|---|---|---|---|
| US06 | Open the home page logged out | Headline says what the site is for; Create account and Browse cards buttons; featured cards | Pass | [home-logged-out](./docs/images/screenshots/home-logged-out.png) |
| US07 | Open Browse cards | AAA, BBB and CCC tiles with set, number, rarity and a placeholder image | Pass | [catalogue](./docs/images/screenshots/catalogue.png) |
| US08 | Search for `bb` | Only BBB, with "1 card found" | Pass | [search-result](./docs/images/screenshots/search-result.png) |
| US08 | Search for `zzz` | 'No cards match "zzz". Try a different name.' | Pass | |
| US10 | Open a card | Image, set, number, rarity, price, rating summary, add and review forms | Pass | [card-detail](./docs/images/screenshots/card-detail.png) |

### My Cards: create, read, update, delete (US11 to US14)

| Story | Test | Expected | Result | Screenshot |
|---|---|---|---|---|
| US11 | Add a card with quantity 0 | Not saved; "Please correct the errors below and try again." | Pass | [add-card-invalid-quantity](./docs/images/screenshots/add-card-invalid-quantity.png) |
| US11 | Add a card as Owned, quantity 2, with a note | "AAA was added to your cards." and it is listed in My Cards | Pass | [add-card-success](./docs/images/screenshots/add-card-success.png) |
| US12 | View My Cards on a phone (320 and 375px) | Each entry stacks as a labelled card, no sideways scrolling | Pass | [my-cards-mobile](./docs/images/screenshots/my-cards-mobile.png) |
| US11 | Open the same card again | Card page says "On your list" instead of showing the add form | Pass | |
| US11 | Try to add the same card again | Sent to that entry's edit page with "You already have AAA on your list. Edit that entry to change it." | Pass | |
| US13 | Edit the entry to Wanted, quantity 3 | "Your entry for AAA was updated." and the list shows Wanted, 3 | Pass | [edit-card-form](./docs/images/screenshots/edit-card-form.png), [edit-card-success](./docs/images/screenshots/edit-card-success.png) |
| US12 | Open the Owned tab | "You have no owned cards yet." | Pass | |
| US14 | Remove the entry | Confirmation page names the card; then "AAA was removed from your cards." and the list is empty | Pass | [remove-card-confirm](./docs/images/screenshots/remove-card-confirm.png), [remove-card-success](./docs/images/screenshots/remove-card-success.png) |

### Reviews: comment and star rating (US18 to US21)

| Story | Test | Expected | Result | Screenshot |
|---|---|---|---|---|
| US18 | Submit an empty review | The browser blocks it: rating and comment are required | Pass | |
| US18 | Give 4 stars with a comment | "Thank you for submitting your review!"; the review shows ★★★★☆ and the comment; the average updates | Pass | [review-success](./docs/images/screenshots/review-success.png) |
| US19 | Edit the review to 5 stars | "Your review was updated successfully." and ★★★★★ | Pass | [review-edit-form](./docs/images/screenshots/review-edit-form.png) |
| US20 | Delete the review | Confirmation page; then "Your review was deleted." and "No reviews yet" | Pass | [review-delete-confirm](./docs/images/screenshots/review-delete-confirm.png) |

### Security checks (US05)

Changing the ID in the address bar to another user's entry or review
is covered by automated two-user tests (see
[Automated testing](#automated-testing)): every such request returns
a 404 page and changes nothing.

## Responsive testing

Run in the same live browser session (US22):

| Check | Expected | Result | Screenshot |
|---|---|---|---|
| Browse cards at 320, 375, 768, 1024 and 1440px | No sideways scrolling at any width | Pass (0px overflow at each) | |
| My Cards at 320 and 375px | No sideways scrolling | Pass | [my-cards-mobile](./docs/images/screenshots/my-cards-mobile.png) |
| Phone width: navigation | Links hidden behind a Menu button | Pass | [mobile-menu-closed](./docs/images/screenshots/mobile-menu-closed.png) |
| Phone width: press Menu | Links appear; the button reports `aria-expanded="true"` | Pass | [mobile-menu-open](./docs/images/screenshots/mobile-menu-open.png) |
| Short page (Log out) at 1440 x 900 | Footer's bottom edge at the bottom of the window (900px) | Pass | [logout-success](./docs/images/screenshots/logout-success.png) |

## Automated testing

Run with:

```bash
python manage.py test
```

96 tests, all passing on 14 October 2026:

| File | Tests | What they check |
|---|---|---|
| `accounts/tests.py` | 19 | Register (valid, taken username, each of the four password rules, mismatched passwords), log in (valid, wrong password, unknown username, return to the requested page, no password-reset link), log out (POST logs out, GET does not), navigation in both states |
| `cards/tests.py` | 48 | Model constraints (unique set names, unique number per set, rating 1 to 5 in the form and the database, one review per user per card), the Base Set and tester fixtures (load twice without duplicates), the star filter, the "edited" marker, catalogue paging and search, the card page logged in and out, average rating, and review create, edit and delete, including another user's review returning 404 |
| `collection/tests.py` | 29 | Entry constraints (one per user per card, quantity at least 1), My Cards tabs and empty states, add (owned, wanted, quantity 0, duplicate, unknown card, logged out), edit and remove, including another user's entry returning 404 and staying unchanged |

The two-user tests are the most important: they prove one user
cannot view, change or delete another user's records by guessing an
ID, which is a security boundary rather than just a feature.

For a coverage report:

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report -m
```

## Validators

### HTML: W3C Nu validator

Every page was validated in each state a user can reach, using the
rendered source (logged-in pages need a session, so they cannot be
validated by URL). The logged-out pages (home, Browse cards, a search
with no results, two card pages, Log in and Register) were also
validated by URL on the live site: 0 errors, 0 warnings.

| Pages | Errors | Warnings |
|---|---|---|
| Home (logged out and logged in) | 0 | 0 |
| Browse cards (logged out, logged in, search with results, search with no results) | 0 | 0 |
| Card page (logged out, logged in with forms, logged in with own entry and review) | 0 | 0 |
| My Cards (with entries, empty tab) | 0 | 0 |
| Add, edit and remove entry pages, including add with errors | 0 | 0 |
| Write, edit and delete review pages, including review with errors | 0 | 0 |
| Register (empty and with errors), Log in, Log out | 0 | 0 |

The validator first reported "Article lacks heading" on card tiles;
each card name is now a heading.

### CSS: W3C Jigsaw

`static/css/style.css`: **0 errors**. One warning remains:
`system-ui` and `-apple-system` in the font list are reported as
vendor extensions. They are deliberate, so the site uses each
device's own system font, with `Arial, sans-serif` as the fallback.

### JavaScript

`static/js/nav.js` (the Menu button) passes a syntax check with
JavaScriptCore. It uses `const`, strict equality and no globals.

### Python: PEP8

`flake8 .` reports nothing. Generated migrations are excluded in
`.flake8`. Statements are written on single lines where they fit;
lists and calls laid out one item per line use PEP8's standard
hanging indent (see [issue #44](https://github.com/J-Codes-Walkz/CardVault/issues/44)).

### Deployment settings

`python manage.py check --deploy` with production settings: no
issues.

### Still to do

Lighthouse (performance, accessibility, best practices, SEO) on
each main page, mobile and desktop, is still to be run and recorded
(US22, US23).

## Bugs

Every bug is a GitHub issue labelled
[`bug`](https://github.com/J-Codes-Walkz/CardVault/issues?q=label%3Abug),
closed by the commit that fixes it. Security problems are reported
privately, as described in [SECURITY.md](./SECURITY.md).

| Issue | Bug | Fix | Status |
|---|---|---|---|
| [#41](https://github.com/J-Codes-Walkz/CardVault/issues/41) | Heroku never deployed pushes from GitHub: "Wait for CI" was on, but there was no CI, so every commit stayed "pending" | Option switched off until the GitHub Actions workflow (#39) exists | Fixed |
| [#42](https://github.com/J-Codes-Walkz/CardVault/issues/42) | Log in page linked to a password reset that could never work (no email addresses are collected) | Link removed in `accounts/forms.py`; covered by a test | Fixed |
| [#43](https://github.com/J-Codes-Walkz/CardVault/issues/43) | `.gitignore` was GitHub's generic 240-line template | Cut to the 35 lines this project uses; the ignored files are unchanged | Fixed |
| [#44](https://github.com/J-Codes-Walkz/CardVault/issues/44) | Some Python statements were split across lines with non-standard indentation | Rewritten as single lines | Fixed |
| [#45](https://github.com/J-Codes-Walkz/CardVault/issues/45) | README used a hand-written table of contents | Removed; GitHub builds the outline from the headings | Fixed |
| [#46](https://github.com/J-Codes-Walkz/CardVault/issues/46) | Markdown file names were not in capitals | Renamed with `git mv`; testing moved into this file | Fixed |
| [#47](https://github.com/J-Codes-Walkz/CardVault/issues/47) | Footer floated mid-page on short pages; navigation did not collapse on phones | Sticky-footer CSS and a Menu button | Fixed |

Found and fixed while building, before they reached the live site:

- **Edit and Remove buttons broke the My Cards table row** on desktop,
  because the table cell itself was made a flex container. The buttons
  now sit in a wrapper inside the cell.
- **The mentor's sticky-footer CSS used `.html, body`**, which targets
  a class called `html` rather than the `<html>` element, so the
  footer would not have moved. Corrected to `html, body`.

### Known bugs

None open.
