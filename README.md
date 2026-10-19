# CardVault

A full-stack web app for Pok&eacute;mon card collectors: track the
cards you own, keep a wishlist of the ones you want, and read and
write reviews &mdash; built with Django and PostgreSQL, and deployed
to Heroku. The project exists to demonstrate full CRUD (Create, Read,
Update, Delete) behind a real login system, as the Code Institute
capstone checklist requires.

**Live site: [cardvault-0a18b8d773ca.herokuapp.com](https://cardvault-0a18b8d773ca.herokuapp.com/)**

Found a bug? Open an issue with the **Bug report** template. Found a
security problem? Please report it privately, as described in the
[security policy](./SECURITY.md).

> Educational project. Not affiliated with, endorsed by or
> sponsored by Nintendo, Game Freak or The Pok&eacute;mon Company.
> "Pok&eacute;mon" and all card names are trademarks of their
> respective owners, used here for identification only.

## UX design

### Purpose and audience

CardVault is for Pok&eacute;mon TCG collectors who currently track
their collection in a spreadsheet, a notes app, or memory. The site
has one job on arrival: make it obvious that you can create an
account and start tracking cards in under a minute. Every page
answers three questions the checklist asks for directly: what is this
for, can I tell if I'm logged in, and can I get back to where I need
to be.

### User stories

The full set of 34 user stories, written as `As a / I want / so that`
with acceptance criteria, development tasks and a manual test for
each, lives in **[docs/USER_STORIES.md](./docs/USER_STORIES.md)**.
They're prioritised with MoSCoW:

| Priority | Count |
|---|---|
| Must have | 24 |
| Should have | 8 |
| Could have | 2 |

Ideas that came up but were deliberately left out of this submission
are in **[docs/POTENTIAL_UPSCALE.md](./docs/POTENTIAL_UPSCALE.md)**
("Should if / Could if / Won't if"), answering the "what ifs" a tutor
is likely to ask.

### Wireframes

Low-fidelity wireframes for the core screens, covering desktop and
mobile layouts, logged-in and logged-out states, and the success/error
messages from each user story:

| # | Screen | |
|---|---|---|
| 1 | Home (logged out) | [docs/wireframes/01-home.svg](./docs/wireframes/01-home.svg) |
| 2 | Register and log in | [docs/wireframes/02-register-login.svg](./docs/wireframes/02-register-login.svg) |
| 3 | Browse cards (catalogue, search, filters) | [docs/wireframes/03-catalogue.svg](./docs/wireframes/03-catalogue.svg) |
| 4 | Card detail (add to My Cards, reviews) | [docs/wireframes/04-card-detail.svg](./docs/wireframes/04-card-detail.svg) |
| 5 | My Cards (Owned/Wanted tabs, summary, table, CRUD) | [docs/wireframes/05-my-cards.svg](./docs/wireframes/05-my-cards.svg) |
| 6 | Edit/delete forms and message banners | [docs/wireframes/06-forms-confirmations.svg](./docs/wireframes/06-forms-confirmations.svg) |
| 7 | Mobile layouts (nav menu, stacked My Cards) | [docs/wireframes/07-mobile.svg](./docs/wireframes/07-mobile.svg) |

Home page, as an example:

![Wireframe of the CardVault home page, showing the navigation bar, a hero section with Create account and Browse cards buttons, three feature blocks and a row of featured card tiles](./docs/wireframes/01-home.svg)

Blue tags on every wireframe (e.g. `US11`) link that part of the
screen back to its user story in `docs/USER_STORIES.md`.

Wireframes 4 and 5 still show a card price and a collection value.
Prices were dropped on 15 October 2026
([issue #48](https://github.com/J-Codes-Walkz/CardVault/issues/48)),
so the built pages differ there; the wireframes are kept as the
record of the original plan.

*Replace the wireframes above with real screenshots here as each
screen is built, and keep the wireframes in `docs/wireframes/` for
the record of how the design evolved &mdash; the checklist's Features
section asks for screenshots of the finished site, not the plan.*

### Brand and design

Agreed with Jamie in a design session on 15 October 2026 (issues
#59 to #63). The aim: a premium **collector's vault**, calm enough
that the card artwork is always the star, with small Game Boy-style
red, yellow and blue accents.

<p>
  <img src="./static/images/emblem.svg" alt="The CardVault emblem: a navy card back with a gold oval and a ship-wheel vault lock" width="90">
  &nbsp;
  <img src="./static/images/favicon.svg" alt="The CardVault favicon: an original Poké Ball-style icon" width="64">
</p>

- **Emblem and logo:** an original card back (navy, a soft swirl and a
  gold oval) with an old-school ship-wheel vault lock in the centre,
  beside the wordmark Card**Vault**. Inspired by the back of a
  Pokémon card, not a copy of it.
- **Favicon:** an original Poké Ball-style icon (SVG, 32px PNG, an
  Apple touch icon and `favicon.ico`).
- **Colours, each with one job:**

  | Colour | Light mode | Dark mode | Used for |
  |---|---|---|---|
  | Navy | `#0f1f3d` | `#060c18` | Header, emblem, cosmic hero |
  | Red | `#c8102e` | `#e0283d` | Buttons, active tab, Poké Ball ratings, "Vault" |
  | Blue | `#1d4ed8` | `#8ab4ff` | Links and the keyboard focus outline |
  | Yellow | `#f5c518` | `#ffd23f` | Small highlights only: the line under the header, Rare Holo badges |
  | Ink | `#162034` | `#e8edf6` | Text |
  | Page | `#f5f7fb` | `#0b1220` | Background |

  Every text colour pair passes WCAG AA in both modes (see
  [TESTING.md](./TESTING.md#brand-and-design-testing)). Yellow is
  never used for text on white.
- **Light and dark mode:** follows the device setting, with a
  sun/moon toggle in the header that the browser remembers. A
  high-contrast style switches on when the device asks for more
  contrast, in both modes.
- **Typography:** Poppins (bold, rounded and geometric) for headings
  and the logo, served from this site; the device's own system font
  for body text, so pages stay fast.
- **Ratings:** Poké Balls instead of stars, full or empty, and five
  clickable balls on the review form.
- **Rarity badges:** the 1999 Base Set symbols with the word: ●
  Common, ◆ Uncommon, ★ Rare, ★ Rare Holo (gold).
- **Movement, kept small:** card tiles lift on hover or keyboard
  focus, Rare Holo cards shimmer once, and the home page plays a
  short Poké Ball intro on a visitor's first visit (skippable). The
  faint rarity symbols behind the home page banner float slowly, each
  on its own path, with a "Pause animation" button in the corner
  (WCAG 2.2.2). All of it switches off when the device asks for
  reduced motion.
- **Layout:** a responsive grid for card tiles (4 columns desktop, 2
  tablet, 1 mobile), and a table for My Cards on wide screens that
  becomes stacked cards below 900px.

![The first-visit intro: the vault emblem and an Enter the vault button on the cosmic starfield](./docs/images/screenshots/intro.png)

![A card page in dark mode, with the Rare Holo badge and Poké Ball ratings](./docs/images/screenshots/card-detail-dark.png)

## Database design

PostgreSQL in every environment, reached entirely through Django's
ORM. Full write-up, the entity-relationship diagram and the reasoning
behind each constraint are in
**[docs/DATABASE_SCHEMA.md](./docs/DATABASE_SCHEMA.md)**.

```mermaid
erDiagram
    CARD_SET ||--o{ CARD : contains
    USER ||--o{ COLLECTION_ENTRY : adds
    CARD ||--o{ COLLECTION_ENTRY : "held as"
    USER ||--o{ REVIEW : writes
    CARD ||--o{ REVIEW : "reviewed in"
```

Five tables, deliberately kept simple: `User` (Django's built-in auth,
with no custom fields), `CardSet` and `Card` (shared reference data,
seeded from a fixture or Django admin rather than user-entered), and
two user-owned tables that carry full CRUD &mdash; `CollectionEntry`
(a card the user owns or wants, told apart by a `status` field) and
`Review`. The models live in `cards/models.py` and
`collection/models.py`. What was considered and set aside (a custom
user model, and owned/wanted as two tables instead of one), and why
`CardSet` was cut and then brought back, is explained in
[Why simplify](./docs/DATABASE_SCHEMA.md#why-simplify).

## Security architecture

CardVault is built in layers, so that if one protection fails another
still stands. Every request passes through each layer in turn:

```mermaid
flowchart TD
    A[Visitor's browser] -->|HTTPS only, HSTS| B[Heroku router]
    B -->|adds the visitor's real IP address to X-Forwarded-For| C[gunicorn: 2 workers x 4 threads]
    C --> D[Django security middleware<br>HTTPS redirect, CSP, Permissions Policy,<br>no framing, CSRF check, secure cookies]
    D --> E[Rate limits<br>log in, registration, Contact,<br>kept in the shared database cache]
    E --> F[Views<br>log in required, every query filtered<br>to the logged-in user, 404 otherwise]
    F --> G[Django ORM<br>no hand-written SQL]
    G -->|TLS, 10-second query limit| H[(Heroku Postgres<br>encrypted at rest, daily backups)]
```

The full list of protections, and how to report a problem privately,
is in [SECURITY.md](./SECURITY.md). This section explains the main
decisions.

### Stopping password guessing

| Attack | Protection |
|---|---|
| Guessing one person's password | **3 wrong passwords lock that username for 15 minutes**, whichever computers the guesses come from. At most 12 guesses an hour, against a password that must pass Django's checks (8+ characters, not one of the 20,000 most common, not all numbers, not like the username). |
| One computer trying thousands of log ins | One IP address may get **5 passwords wrong a minute and 20 an hour**, across any usernames, and try to log in **10 times a minute**. After that it sees "Too many failed log in attempts" until the time is up. |
| Mass account creation | **10 registrations an hour** per IP address; anything more gets a "Too many attempts" page (HTTP 429). |
| Bots flooding the Contact form | A hidden trap field and **5 messages an hour** per visitor. |
| Finding out which usernames exist | A failed log in always says "Invalid username or password", never which part was wrong. |
| Guessing the admin password | The Django admin's own log in page is switched off; admins log in through the same rate-limited page. |

The limits are counted in a cache table in the database, shared by
every web process and kept across restarts. Each limit is counted per
visitor because `ALLAUTH_TRUSTED_PROXY_COUNT = 1` tells django-allauth
to use the address Heroku's router adds to `X-Forwarded-For`. That
address cannot be faked: a visitor can send their own
`X-Forwarded-For`, but the router always adds the real address last.
Before this setting, every visitor shared one count
([bug #66](https://github.com/J-Codes-Walkz/CardVault/issues/66)).

**The trade-off:** locking a username after 3 wrong passwords means
someone who knows your username can keep your account locked by
getting your password wrong on purpose. They still cannot get in, and
each wrong password stops counting after 15 minutes, so they would
have to keep trying every few minutes; attempts made while locked do
not count. For a hobby site
this is the right balance; a bank would add a second factor instead
(see [POTENTIAL_UPSCALE.md](./docs/POTENTIAL_UPSCALE.md)).

![The fourth wrong password: logging in is paused](./docs/images/screenshots/login-locked.png)

### Handling heavy traffic

- **More requests at once:** gunicorn runs 2 worker processes with 4
  threads each, so one web dyno serves 8 requests at the same time
  instead of 2. Each worker restarts after about 1,000 requests, so a
  slow memory leak can never build up.
- **Database connections are reused** for up to 10 minutes and
  checked before reuse, rather than opened fresh for every page. At
  most 8 connections per dyno, well inside the plan's limit of 20.
- **No query can run away:** Postgres stops any query still running
  after 10 seconds, and searches are cut to 100 characters and 5
  words, as each word adds a filter
  ([bug #67](https://github.com/J-Codes-Walkz/CardVault/issues/67)).
- **Efficient pages:** lists use `select_related` and a fixed number
  of queries however many cards there are (tested), and are split
  into pages of 12.
- **Static files** (CSS, JavaScript, fonts, icons) are compressed and
  served by Whitenoise with long cache times, so returning visitors
  load them from their own browser.
- **Card pictures** come from the Pokémon TCG image server, not from
  CardVault, so the heaviest files never touch our dyno.

**Load test, 19 October 2026:** 2,000 page visits to the live site,
25 at a time, spread across the home page, Browse cards, a search and
a card page: **all 2,000 succeeded, about 112 pages a second, median
0.21 seconds, 95% within 0.33 seconds**. Details in
[TESTING.md](./TESTING.md#load-testing).

**To grow further**, Heroku can run more dynos (`heroku ps:scale
web=2`) or bigger ones, and the database plan can be upgraded, without
changing any code.

### Database security management

| Area | How CardVault handles it |
|---|---|
| Access | The database address and password exist only in Heroku's config vars (`DATABASE_URL`) and, for the local database, in a `.env` file that git ignores. Neither is ever in the code or its history. |
| Connection | Encrypted with TLS (`sslmode=require`) on the live site. |
| Storage | Heroku Postgres encrypts the data on disk. |
| Queries | Only through Django's ORM, which sends every value separately from the SQL, so SQL injection is not possible. The one hand-written statement is a fixed clean-up in `clear_expired_cache`, which takes no user input. |
| Rate limit notes | The log in limits keep IP addresses in the cache table. Django only clears expired rows once there are more than 300, so `clear_expired_cache` deletes them on every release (see the `Procfile`). |
| Integrity | Rules are enforced by the database itself, not only by forms: one entry per user per card, quantities of at least 1, ratings from 1 to 5, unique card numbers per set. |
| Least data | No email address or real name for an account; the date of birth is checked and thrown away; passwords are stored only as salted PBKDF2 hashes. |
| Deletion | Deleting an account deletes its My Cards entries and reviews with it (`on_delete=CASCADE`). Contact messages are deleted once handled. |
| Backups | A full backup every day at 03:00 (UK time), set up with `heroku pg:backups:schedule`, plus Heroku's own continuous protection. The first backup (19 October 2026) was checked: it contains all 18 tables. Restore with `heroku pg:backups:restore`. |
| If the password leaked | `heroku pg:credentials:rotate` issues a new database password and Heroku updates `DATABASE_URL` and restarts the app. |
| Admin | Only staff accounts can open the Django admin, through the rate-limited log in page. Contact messages are read-only there. |
| Errors | A database error shows the plain 500 page, never the error itself, and the full traceback goes to Heroku's logs (`heroku logs --tail`) for investigation. |

**Known limits:** the Essential database plan has a single database
user, so the app cannot have a separate read-only login, and it has
no point-in-time rollback. Both come with Heroku's Standard plans.

## Project mind map

A knowledge graph of the whole project (code, templates, docs and
wireframes) is kept in `graphify-out/`, built with
[graphify](https://github.com/Graphify-Labs/graphify). It is used as a
mind map: it shows which models, tests, user stories and wireframes
connect to each other, and which parts everything else depends on.

| File | What it is |
|---|---|
| [graphify-out/graph.html](./graphify-out/graph.html) | The interactive graph. GitHub shows this file as source code, so download it (or clone the repo) and open it in a browser. It loads one script from the internet, so it needs a connection. |
| [graphify-out/GRAPH_REPORT.md](./graphify-out/GRAPH_REPORT.md) | A plain-language report: the most connected nodes, surprising connections and questions worth asking. |
| [graphify-out/graph.json](./graphify-out/graph.json) | The raw graph data. |

First built on 12 October 2026 from 56 files (336 nodes, 578 links,
19 clusters) and updated on 14 October 2026 after the front-end CRUD
work: it now has 597 nodes, 1,120 links and 48 clusters. The most
connected nodes are the README, the user stories, TESTING.md and the
`Card`, `CollectionEntry`, `CardSet` and `Review` models, which
matches the design: the CRUD stories are built on those tables. Links
the report marks as "inferred" were reasoned by the AI rather than
read directly from a file, so treat the graph as a guide, not a
complete map. Screenshots are left out of the graph (see
`.graphifyignore`), because they are test evidence rather than
project structure.

To refresh it after new work, run `/graphify . --update` in Claude
Code. Only the three files above are committed; the cache stays local
(see `.gitignore`).

*Add a screenshot of the graph here.*

## Features

Everything below is live on
[the Heroku site](https://cardvault-0a18b8d773ca.herokuapp.com/) and
was tested there on 14 October 2026 (see [TESTING.md](./TESTING.md)).
Screenshots are from that test run, using the Base Set and the AAA, BBB and CCC tester
cards.

### Accounts

- **Register** (US01): username, password and password confirmation
  through django-allauth. A new user is logged in straight away with
  "Your account has been created. Welcome to CardVault,
  &lt;username&gt;!". A taken username, a weak password (naming the
  rule it broke) or mismatched passwords each show an error and
  create no account.
- **Log in and log out** (US02, US03): "Welcome back,
  &lt;username&gt;!" and "You have been logged out. See you soon!".
  A wrong password shows one generic error that does not reveal
  which part was wrong. Log out is a POST form with a CSRF token.
- **Always know if you are logged in** (US04): the navigation shows
  "Logged in as &lt;username&gt;", My Cards and Log out, or Log in
  and Register.
- **Private data stays private** (US05): logged-out visitors are sent
  to Log in with "Please log in to view that page.", and another
  user's entries and reviews return a 404 page.

![The registration success message and logged-in navigation](./docs/images/screenshots/register-success.png)

### Browsing cards

- **Home page** (US06): says what the site is for, with Create
  account and Browse cards buttons (Go to My Cards when logged in)
  and a row of featured cards.
- **Catalogue** (US07): a responsive grid, 12 cards a page with
  page links; a placeholder image when a card has no picture.
- **Search** (US08): type any part of a card's name, set or rarity,
  in any order: "char" finds Charizard, Charmeleon and Charmander;
  "holo", "holo rare" and "rare holo" all find the holo cards;
  "common" finds Commons but not Uncommons. Shows a result count and
  a clear link.
- **Filters** (US09): Rarity and Set dropdowns that combine with the
  search and stay selected when moving between pages.
- **Card page** (US10): set, number, rarity, average star rating and
  every review.

![Browse cards showing the first 12 Base Set cards with their pictures](./docs/images/screenshots/catalogue.png)

### My Cards: full front-end CRUD

From any card's page a logged-in user can:

- **Create** (US11): add the card to My Cards as Owned or Wanted, with
  a quantity (at least 1) and notes. Adding a card already on the
  list goes to that entry's edit page instead of creating a second
  one.
- **Read** (US12): My Cards lists every entry with All, Owned and
  Wanted tabs. Each row shows your own star rating for the card (or a
  Rate it link) and a one-line preview of your notes; hover for the
  whole note, or open Edit. On phones and small tablets each row
  stacks into a labelled card showing the full note.
- **Update** (US13): change the status, quantity or notes.
- **Delete** (US14): remove the entry after a confirmation page that
  names the card. The card itself stays in the catalogue.

![My Cards after adding Alakazam, with Edit and Remove buttons](./docs/images/screenshots/add-card-success.png)

### Reviews: comments and star ratings

- **Create** (US18): press Write a review on a card's page, then rate
  it from 1 to 5 stars and write a comment on the review page. Each
  page has only one form, so nothing you type can be lost. Each user
  reviews a card once; after that the button is replaced by their
  review with Edit and Delete buttons.
- **Read** (US21): reviews are listed newest first with the
  username, stars, date and comment, under the card's average rating.
- **Update** (US19): edit your own review; it is then marked
  "(edited)".
- **Delete** (US20): delete your own review after a confirmation
  page.

![A 4-star review with its comment and the card's average rating](./docs/images/screenshots/review-success.png)

### Privacy, safety and accessibility

- **Age check** (US29): registration asks for a date of birth and
  refuses anyone under 13 ("Sorry, you need to be 13 or older to
  create a CardVault account."), then stays closed for that browser
  session. The date is checked and thrown away, never stored. This
  follows COPPA in the US and the UK Children's Code.
- **Delete my account** (US30): a footer link, a page listing what
  will be deleted, and a password check; then the account, its cards
  and reviews are deleted.
- **Privacy and cookies** (US31): a plain-English page listing what is
  stored, the only two cookies (`sessionid` and `csrftoken`, both
  strictly necessary, so no cookie banner is needed) and the other
  services involved.
- **Accessibility** (US32): works at 200% zoom, switches to a
  high-contrast style when the device asks for it, passes an automated
  WCAG 2.2 AA check on every page, and has an accessibility statement.
  CardVault has no audio or video, so nothing depends on hearing.

![Registration refused for an under-13 date of birth](./docs/images/screenshots/signup-under-13.png)

### Navigation and contact

- **Home link** (US33): "Home" is the first link in the header on
  every page, as well as the logo. The link for the page you are on
  has a yellow underline and `aria-current="page"` for screen readers.
- **Contact page** (US34): linked in the header and footer. It asks
  for a name, email address and message (logged-in users find their
  username already filled in), then returns to the home page with:
  "Thank you for your enquiry. We aim to reply within 2 to 3 days. If
  nothing arrives in your inbox, please check your junk or spam
  folder." Messages are saved in a `ContactMessage` table and read in
  the Django admin, where they can be marked as handled but not
  changed. Replies are sent by hand, so the site itself sends no email
  and holds no mail password. A dedicated CardVault mailbox to reply
  from is planned; see [POTENTIAL_UPSCALE.md](./docs/POTENTIAL_UPSCALE.md).
- **Spam protection:** a hidden trap field that bots fill in and
  people never see (bots get the same thank you, but nothing is
  saved), and a limit of 5 messages an hour per visitor, counted
  against a one-way hash of the IP address. An automatic email reply
  was considered and left out on purpose; see
  [POTENTIAL_UPSCALE.md](./docs/POTENTIAL_UPSCALE.md).

### Quality and security

- **Responsive** (US22): mobile first, no sideways scrolling from
  320px up. Below 1024px the navigation collapses behind a Menu button,
  and the footer sits at the bottom of the window on short pages.
- **Feedback on every action** (US24): a success, error or info
  message with a word ("Success:", "Error:") as well as colour, and
  `role="status"` or `role="alert"` for screen readers.
- **Secrets and debug** (US26): every secret read from environment
  variables, `DEBUG` off by default, and a [security policy](./SECURITY.md)
  for reporting vulnerabilities privately.
- **Helpful error pages** (US25): branded pages for every error a
  visitor can meet, each in plain language with a way back, and never
  any technical detail:

  | Error | When | Page says |
  |---|---|---|
  | 404 | The address does not exist, or the card or entry does not (or is someone else's) | "We couldn't find that page", with a card search |
  | 403 | A logged-in user who is not staff opens the admin | "You don't have permission to see this page" |
  | 403 (form expired) | A form is sent after its session ended, for example after logging out in another tab | "This form has expired", and how to fix it |
  | 400 | A malformed request, such as an unknown web address for the site | "Something about that request wasn't right" |
  | 429 | Too many log in or registration attempts | "Too many attempts" |
  | 500 | Something breaks on the server | "Something went wrong on our side" |

  The 500 page is plain HTML with every link written out, as Django
  shows it without any context: whatever broke (even the database)
  cannot break the error page too. Every crash is written to Heroku's
  logs with its traceback
  ([bug #69](https://github.com/J-Codes-Walkz/CardVault/issues/69)).

<p>
  <img src="./docs/images/screenshots/error-404.png" alt="The 404 page with a card search" width="480">
  <img src="./docs/images/screenshots/error-500-mobile.png" alt="The 500 page on a phone in dark mode" width="180">
</p>

<p>
  <img src="./docs/images/screenshots/mobile-menu-closed.png" alt="Phone width with the menu closed" width="240">
  <img src="./docs/images/screenshots/mobile-menu-open.png" alt="Phone width with the menu open" width="240">
  <img src="./docs/images/screenshots/my-cards-mobile.png" alt="My Cards stacked on a phone" width="240">
</p>

### Still to build

- My Cards totals, sorting and a one-click "Got it!" (US15 to US17)

Every notification message the app shows (login success, duplicate
username, "thank you for your review", and so on) is written out
exactly in **[docs/NOTIFICATION_MESSAGES.md](./docs/NOTIFICATION_MESSAGES.md)**,
so the UI text stays consistent across views as it's built.

## Agile methodology

This project is tracked with a public **GitHub Projects** board and
GitHub Issues, one issue per user story.

**Project board:
[github.com/users/J-Codes-Walkz/projects/5](https://github.com/users/J-Codes-Walkz/projects/5)**
&mdash; four columns (`Backlog`, `To do`, `In progress`, `Done`), with
every user story and development task as an
[issue](https://github.com/J-Codes-Walkz/CardVault/issues), labelled by
MoSCoW priority and epic, and grouped into three sprint
[milestones](https://github.com/J-Codes-Walkz/CardVault/milestones).

1. **Create the board.** On the repository, go to the Projects tab
   and create a new board. Set its visibility to **public** (Settings
   on the board &rarr; Visibility) &mdash; the checklist specifically
   asks for this.
2. **Give it at least three columns.** `Backlog`, `In progress` and
   `Done` is the minimum; `To do` as a fourth (between Backlog and In
   progress) makes sprint planning easier.
3. **Create one issue per user story.** Each issue title starts with
   the story ID, e.g. `US01: Register an account`, with the
   acceptance criteria and tasks from `docs/USER_STORIES.md` pasted
   into the issue body as a checklist. **[docs/github-issues.csv](./docs/github-issues.csv)**
   has every story pre-formatted (title, epic, priority, body), and
   **[scripts/create_github_issues.py](./scripts/create_github_issues.py)**
   creates them all with the GitHub CLI instead of typing 28 issues
   by hand. Create the labels it expects first, preview with
   `--dry-run`, then run it for real:

   ```bash
   gh auth login        # once, if you haven't already

   # Create the labels the script applies (one-off, per repo):
   for lbl in priority:must priority:should priority:could \
              epic:accounts-and-authentication epic:browsing-cards \
              epic:my-cards-owned-and-wanted \
              epic:card-reviews epic:quality-security-and-content; do
     gh label create "$lbl" --color "ededed" 2>/dev/null || true
   done

   python scripts/create_github_issues.py --dry-run   # preview, creates nothing
   python scripts/create_github_issues.py              # actually create all 28
   ```

   Add `--only US01 US02` to create just specific stories.

   **Done on 12 October 2026:** all 28 stories now exist as issues
   #1 to #28 (issue #1 is US01, and so on), followed by eight
   development-task issues, #29 to #36, each naming the stories it
   supports. Running the script again would create duplicates. The
   issues were added to the board with the GitHub CLI
   (`gh project item-add`).

   **Added on 15 October 2026:** four more stories, US29 to US32
   (age check, delete my account, privacy and cookies, accessibility),
   in a sixth epic, "Privacy, safety and accessibility". They are
   issues #52 to #55, so from here on the issue number and the story
   number differ; each issue title still starts with its story ID.

   **Added on 16 October 2026:** US33 (a Home link) and US34 (a
   Contact page), in a seventh epic, "Navigation and contact", as
   issues #64 and #65.
4. **Move cards as you work**: `Backlog` &rarr; `To do` when you
   start a sprint/session, `In progress` while coding, `Done` once
   its manual test passes. The `priority:*` and `epic:*` labels from
   step 3 make the MoSCoW breakdown visible directly on the board,
   not just in the docs &mdash; group or filter the board by label.
5. **Link this README** to the board once it exists, and update the
   "GitHub Projects board" link near the top of
   `docs/USER_STORIES.md`.

### Sprints

Three sprints, tracked as GitHub milestones, ending before the
submission deadline of Monday 2 November 2026, 12:00 midday:

| Sprint | Due | Goal |
|---|---|---|
| 1: Foundations | Wed 14 Oct | Project scaffold, early Heroku deploy, register / log in / log out on the live site, data models, Base Set fixture |
| 2: Core features | Fri 23 Oct | Browse the catalogue, My Cards CRUD, brand and favicon |
| 3: Reviews, polish and testing | Fri 30 Oct | Reviews, should/could-haves, accessibility, validation, testing write-up |

Work runs roughly in epic order, since later epics depend on earlier ones
(you need accounts before My Cards CRUD means anything, and cards
in the catalogue before reviews mean anything):

1. Accounts and authentication (US01&ndash;US05)
2. Browsing cards (US06&ndash;US10) &mdash; needs the catalogue
   seeded first (US27)
3. My Cards (US11&ndash;US17)
4. Reviews (US18&ndash;US21)
5. Quality, security and content polish (US22&ndash;US28) &mdash;
   some of this (US24, US26) is really ongoing throughout, not a
   final step; treat it as a checklist you run against every PR.

## Testing

The full testing write-up is in **[TESTING.md](./TESTING.md)**: manual tests for every user story, the automated test suite, validator results (HTML, CSS, Python) and every bug found, each logged as a GitHub issue labelled [`bug`](https://github.com/J-Codes-Walkz/CardVault/issues?q=label%3Abug).

## Deployment

### Local setup

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
createdb cardvault                 # a local PostgreSQL database
cp .env.example .env               # then fill in SECRET_KEY and DATABASE_URL
python manage.py migrate
python manage.py loaddata pokemon_cardsets
python manage.py loaddata base_set_cards
python manage.py loaddata tester_cards
python manage.py createsuperuser
python manage.py test
python manage.py runserver
```

`.env` is never committed (see `.gitignore`); `.env.example` lists
the variable names only. The settings that read these variables are
in **[docs/SETTINGS_SNIPPET.md](./docs/SETTINGS_SNIPPET.md)**.

### Heroku

**Deployed on 12 October 2026** as the app `cardvault` (EU region,
Basic dyno, Heroku Postgres `essential-0`) at
[https://cardvault-0a18b8d773ca.herokuapp.com/](https://cardvault-0a18b8d773ca.herokuapp.com/).
The steps below are the ones that were followed, using the Heroku
CLI. After the first deploy the live site was checked for: HTTP
redirecting to HTTPS, static files loading, a non-existent URL
returning a plain 404 rather than a debug page, and a full register,
log out and log in.

1. **Create the app.**
   ```bash
   heroku create your-app-name
   ```
2. **Add Heroku Postgres** (the Essential tier is the cheapest paid
   option; there is no longer a free tier):
   ```bash
   heroku addons:create heroku-postgresql:essential-0
   ```
   This sets the `DATABASE_URL` config var automatically &mdash; you
   don't set it yourself.
3. **Set the remaining config vars:**
   ```bash
   heroku config:set SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```
4. **Push to deploy:**
   ```bash
   git push heroku main
   ```
   The `Procfile`'s `release` line runs `migrate` automatically on
   every deploy, so the schema stays in sync without a manual step.

   **Since 14 October 2026 deploys are automatic from GitHub.** On the
   app's Deploy tab in the Heroku dashboard, the deployment method is
   GitHub (repository `J-Codes-Walkz/CardVault`), with **Automatic
   deploys** from `main`. Every push to `main` on GitHub now deploys by itself,
   so `git push heroku main` is no longer needed. Each deploy is also
   recorded on GitHub, under **Deployments** on the repository's main
   page and as an environment under Settings &rarr; Environments.

   **Bug found while setting this up:** **Wait for CI to pass before
   deploy** was ticked, but the repository had no CI yet. GitHub then
   reports every commit's checks as "pending" for ever, so Heroku
   received each push and never deployed it. The option was switched
   off; it goes back on once the GitHub Actions workflow (issue #39)
   is running, so that a commit with failing tests can never reach the
   live site.
5. **Create a superuser on Heroku** (one-off, after the first
   deploy):
   ```bash
   heroku run python manage.py createsuperuser
   ```
6. **Seed the catalogue** (US27) from
   `cards/fixtures/pokemon_cardsets.json`:
   ```bash
   heroku run python manage.py loaddata pokemon_cardsets
   heroku run python manage.py loaddata base_set_cards
   heroku run python manage.py loaddata tester_cards
   ```
   The tester cards (AAA, BBB and CCC) were loaded on the live site on
   14 October 2026 for front-end CRUD testing.
   (Or add the cards through `/admin/` instead &mdash; see
   [Populating the catalogue](./docs/DATABASE_SCHEMA.md#populating-the-catalogue).)
7. **Verify production settings**: visit a URL that doesn't exist on
   the live app and confirm you get the custom 404 page, not a Django
   debug page. If you see a debug page, `DEBUG` is still `True` on
   Heroku &mdash; fix the config var before doing anything else.

### Forking/cloning

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
# then follow "Local setup" above
```

## Credits

### Code

- Built with [Django](https://www.djangoproject.com/) 5.2 LTS and
  [PostgreSQL](https://www.postgresql.org/).
- Register, log in and log out use
  [django-allauth](https://docs.allauth.org/). Its templates, message
  wording and login form are overridden in `templates/account/`,
  `accounts/adapter.py` and `accounts/forms.py`.
- Deployment uses [Whitenoise](https://whitenoise.readthedocs.io/)
  for static files and [Gunicorn](https://gunicorn.org/) as the
  application server, following
  [Heroku's Python support docs](https://devcenter.heroku.com/categories/python-support).
- *(Add any tutorial, Stack Overflow answer, or snippet you lean on
  directly, with a link, as you build &mdash; the checklist wants
  externally used code credited specifically, not just frameworks.)*

### Content

- Card data and card images: the
  [Pok&eacute;mon TCG API](https://pokemontcg.io), a free,
  community-run, unofficial API. It was called **once**, by
  `scripts/build_base_set_fixture.py`, to build
  `cards/fixtures/base_set_cards.json` (the 102 Base Set cards). The
  live site never calls the API, so it keeps working if the API goes
  down. Card pictures are linked from the API's image host,
  `images.pokemontcg.io`; if that server cannot be reached, a small
  script (`static/js/image-fallback.js`) shows CardVault's own
  placeholder instead. Pok&eacute;mon card names
  and artwork belong to their owners (see the disclaimer at the top of
  this README).
- Emblem, favicon, Poké Ball rating icons and the placeholder card
  image: original drawings made for this project as SVG. The Poké
  Ball design itself belongs to Nintendo, Creatures and Game Freak;
  it is used here in a simple fan-made style for a non-commercial,
  educational project (see the disclaimer at the top of this README).
- Rarity symbols (● ◆ ★): the shapes used on 1999 Base Set cards.
- Font: [Poppins](https://github.com/itfoundry/Poppins) by the
  Indian Type Foundry, under the SIL Open Font License
  (`static/fonts/OFL.txt`), served from this site.

### Acknowledgements

- Learning outcomes and checklist: Code Institute, *CI Bootcamps |
  Capstone Project &mdash; Pre-Submission Checklist*.
- Project concept inspired by [Collectr](https://app.getcollectr.com/)
  (not affiliated; CardVault is an independent, from-scratch build
  for a learning capstone, not a clone of Collectr's code or design).

## Usage of AI

AI (Claude, via Claude.ai for planning and Claude Code for building) was used throughout this project as a
collaborator for planning, debugging, and reviewing &mdash; not as a
replacement for understanding the code. Keep adding to this log as
you build, covering all three areas the checklist asks about:
**debugging**, **developing features**, and **automated tests**. A
short line per session is enough; specificity is what makes this
section credible to an assessor.

| Date | Used for | What happened |
|---|---|---|
| 2026-10 | Planning | Designed the initial PostgreSQL schema (6 tables, constraints and relationships) from a plain-language feature description; generated the ERD, the 32 MoSCoW user stories, low-fidelity wireframes for 8 key screens, and this documentation set (README, database/testing/deployment docs) against the Code Institute capstone checklist. |
| 2026-10 | Planning | Simplified the schema from 6 tables to 4 (dropped the custom `User` model, the `CardSet` table, and merged `CollectionItem`/`WishlistItem` into one `CollectionEntry` with a `status` field) after judging the original over-engineered for what the checklist actually asks for; regenerated the ERD, the user stories (32 &rarr; 28), the wireframes, this README and the rest of `docs/` to match. |
| 2026-10-12 | Planning (Agile) | Claude Code created the GitHub labels, three sprint milestones, 28 user-story issues and 8 task issues from `docs/github-issues.csv`, then built the public Projects board with the GitHub CLI. Claude proposed which stories go in which sprint; I set the Wednesday target for Sprint 1 and supplied the submission deadline. |
| 2026-10-12 | Developing features | Claude Code scaffolded the Django project and the `accounts`, `cards` and `collection` apps, wrote the settings, the four models and their admin, and the django-allauth templates. I chose django-allauth rather than hand-written auth views. I left the `CardSet` decision to Claude, which brought the table back to match my Base Set fixture. Changed from the original plan: a new user is logged in straight after registering (allauth's normal behaviour) instead of being sent to the login page, so US01 and the notification messages were updated to match. |
| 2026-10-12 | Debugging | Caught before it bit: the planned static-file setting (Whitenoise's hashed-filename storage everywhere) breaks any test that renders a template, because the test runner never runs `collectstatic`. Fix: use that storage only in production and Django's plain storage when `DEBUG` or the test runner is active. Also removed allauth's "Forgot your password?" link, which pointed at an email reset that cannot work without email addresses. |
| 2026-10-12 | Automated tests | Claude Code wrote 45 tests alongside the Sprint 1 code. Verified by running `python manage.py test` (all pass) and by a real register, log out, failed log in and log in against the running site. |
| 2026-10-12 | Deployment | Claude Code created the Heroku app and Postgres add-on with the Heroku CLI, set the config vars (a new `SECRET_KEY` generated straight into Heroku, `DEBUG=False`, `ALLOWED_HOSTS`), deployed with `git push heroku main` and loaded the Base Set fixture. It then tested the live site by registering, logging out and logging in with a throwaway account, which it deleted afterwards. I signed in to GitHub and Heroku myself; no password or key was shared with the AI. |
| 2026-10-12 | Planning (mind map) | Used the graphify skill in Claude Code to build a knowledge graph of the project (`graphify-out/`). Code was parsed structurally; docs, templates and wireframes were read by AI sub-agents. Before committing, the outputs were scanned to confirm they contain no secrets and no local file paths. |
| 2026-10-14 | Debugging | Heroku stopped deploying after the GitHub connection was made. Claude Code checked GitHub's webhook deliveries (Heroku received every push) and the commit status ("pending", with no checks at all), and found "Wait for CI to pass" was waiting for a CI that does not exist yet. Logged as bug #41 and fixed by switching the option off until #39. |
| 2026-10-14 | Debugging | Acted on an assessor's masterclass feedback: logged each point as a bug issue (#43 to #46), then fixed them (trimmed `.gitignore`, single-line Python, no table of contents, capitalised Markdown names). Claude also spotted that the mentor's sticky-footer CSS selector `.html, body` should be `html, body`. |
| 2026-10-14 | Developing features | Claude Code built the front-end CRUD (browse and search cards, card pages, add/edit/remove My Cards entries, 1 to 5 star reviews with comments) and the responsive header and footer. I chose the scope (frontend CRUD with tester cards AAA, BBB, CCC) and the sticky footer. |
| 2026-10-14 | Automated tests | Claude Code wrote 51 more tests (96 in total), including two-user tests proving one user cannot edit or delete another's records. It then drove a real Chrome browser through every user action on the live site (39 checks, all passing) and took the screenshots used in this README and TESTING.md. It found and fixed a table layout bug on My Cards that the unit tests could not see. |
| 2026-10-15 | Developing features | Decided with Claude to drop card prices (currencies and exchange rates were out of proportion to the project) and to build the Base Set once from the Pokémon TCG API. Claude Code wrote `scripts/build_base_set_fixture.py`; when the API kept returning server errors it switched to pages of 25 with retries, and when the API gave the six Energy cards no rarity it marked them Common, as printed, rather than guessing silently. |
| 2026-10-15 | Debugging | The browser test reported only 4 of 12 card pictures loading. Rather than accept or hide it, Claude checked each image: all 12 load in a fresh tab, and the headless browser was treating the long-running test tab as in the background, so lazy images never started. Fixed in the test harness (focus emulation), not the site. |
| 2026-10-15 | Security | Asked Claude to review security end to end. It added a Content Security Policy and Permissions Policy, routed the Django admin log in through allauth's rate limiting, moved rate limits to a shared database cache, scanned the git history for secrets, ran `pip-audit`, and turned on Dependabot, CodeQL and a branch rule on GitHub. 12 security tests added. |
| 2026-10-15 | Design | Used the grilling skill in Claude Code to agree the brand in four short rounds of questions (look, colours, dark mode, logo, ratings, badges, motion, intro). Jamie chose dark mode against my first recommendation, asked for a card-back emblem with a ship-wheel vault lock instead of a Poké Ball logo, and the 1999 rarity symbols. Claude checked every colour pair for contrast before writing any CSS, drew the emblem and icons as SVG, and kept the intro from becoming a gate page. |
| 2026-10-15 | Debugging | A keyboard-only test of the new Poké Ball picker found that Tab landed on the 5th ball and the left arrow moved right, a side effect of the CSS trick first used to fill the balls. Rebuilt with the CSS `:has()` selector in natural 1 to 5 order (after checking the CSS validator accepts it), then re-tested with real key presses and mouse clicks. |
| 2026-10-16 | Design | Asked Claude to make the rarity symbols in the home page banner float rather than sit still. Claude pointed out that endless movement needs a way to pause it (WCAG 2.2.2) and that the Accessibility page promised movement "never loops", so it added a "Pause animation" button, updated that page, and checked that the button never covers the banner's text from 320px up, that pausing really stops the symbols, and that reduced motion still switches everything off. |
| 2026-10-16 | Developing features | Asked Claude for a Home link and a Contact page (name, email, message, and a thank-you banner telling people to check their junk folder), and whether an automatic no-reply email was worth it. Claude advised against the email for now: anyone can type any address, so the form could be used to send mail to strangers, new senders often land in junk, and it would mean keeping a mail password on Heroku. I agreed to save messages for the admin instead and reply by hand from a dedicated mailbox. Claude built a `contact` app with a hidden bot trap and a 5-an-hour limit (storing a hash of the IP address, not the address), 19 tests, and updated the Privacy page, which had said we never ask for an email address. A browser check found the extra links pushed the logged-in header onto two rows at tablet widths, so the Menu button now appears below 1024px. |
| 2026-10-19 | Security | Asked Claude to harden the site against password guessing and heavy traffic, cut log in tries to 3, and manage the database properly. Claude found that the existing per-IP limits never saw real visitors on Heroku: every request arrives from Heroku's router, so all visitors shared one count and 10 wrong passwords could pause logging in for everyone (bug #66). It set `ALLAUTH_TRUSTED_PROXY_COUNT`, wrote tests proving a faked `X-Forwarded-For` does not help, capped searches that could build huge queries (bug #67), added a 10-second query limit, threaded gunicorn workers and a branded 429 page, and found the live database had no backups, so scheduled daily ones and checked the first contained every table. It load tested the live site and, when a heavier run stalled, checked Heroku's router logs before blaming the site: the stalled requests never reached Heroku. |
| 2026-10-19 | Developing features | Built the custom error pages (US25) with Claude. Claude made the 500 page plain HTML because Django renders it without context, and noticed while writing it that the page's promise ("the problem has been recorded") was untrue: with `DEBUG` off, Django logged nothing, so live crashes left no trace (bug #69). It added logging, then ran the site locally in production mode, starting a second copy pointed at a database that does not exist to cause a real 500. A first run showed every page failing; rather than change the site, Claude traced it to its own mistake (static files collected with `DEBUG` on) and redid the check properly. |
| | Debugging | *(log each real debugging session: what broke, what you asked AI, what the actual fix was and why &mdash; "AI suggested X, but the real cause was Y" is a stronger log entry than "AI fixed it")* |
| | Developing features | *(log which views/templates/models you built with AI assistance, and what you changed or rejected from its suggestions)* |
| | Automated tests | *(log where AI helped write or review test cases, and how you verified the tests actually test the right thing)* |

A good entry names the actual prompt or problem, not just "used AI
for X" &mdash; for example: *"Asked Claude to review the ownership
check in `CollectionEntryUpdateView`; it pointed out the original
`get_queryset` didn't filter by `request.user`, which would have let
any logged-in user edit any other user's entries by guessing the ID.
Fixed by adding `.filter(user=self.request.user)` and added US05's
two-user test to catch a regression."*
