# Potential upscale

Ideas beyond the submitted scope, framed as the "what ifs" a tutor or assessor might ask about — grouped using MoSCoW's later tiers: **Should if**, **Could if** and **Won't if**. None of these are built yet; they show the project has a realistic road map beyond the capstone deadline, and that trade-offs were considered deliberately rather than ignored.

Effort is a rough shirt size: **Small** fits in an existing view or template; **Medium** needs a new model or a new package; **Large** needs new infrastructure (a scheduled job, a second service, a payments provider).

## Should if — next in line

The natural next features once the Must and Should have stories above are done. Each builds on tables that already exist, so none of them need a redesign of the schema in docs/DATABASE_SCHEMA.md.

| Feature | What if… | What it would need | Effort |
|---|---|---|---|
| **Download my data** | What if I want a copy of everything CardVault holds about me? | A view that builds a JSON or CSV file of your account, My Cards list and reviews (the UK GDPR right of access and data portability). Left out on 15 October 2026 because deleting your account already covers the rights this project needs. | Small |
| **Two-factor log in for the admin** | What if an admin's password were stolen? | django-allauth's `mfa` app: an authenticator-app code, required for superusers and optional for everyone else. Strongest single step after the rate limits added on 19 October 2026. | Medium |
| **A firewall and CAPTCHA in front of the site** | What if an attack came from thousands of addresses at once? | The rate limits stop one address or one username, but a large botnet spreads its attempts thin. A service such as Cloudflare in front of Heroku (needs a custom domain) blocks known bad traffic and floods before they reach the app, and can show a CAPTCHA after repeated failures. | Medium |
| **A bigger database plan** | What if the site needed separate database users, or to undo a mistake from an hour ago? | Heroku Postgres Standard: extra credentials (for example a read-only one for reports), point-in-time rollback and followers. About $50 a month, so out of scope for now. | Small |
| **A dedicated CardVault mailbox** | What if replies to Contact messages came from a CardVault address, not a personal one? | A free mailbox (for example a Gmail account) used only for CardVault, with two-step verification switched on, so the owner's personal address is never shown to the people who write in. No code changes: replies are already sent by hand. It is also the first step towards the automatic reply below. Left for later on 16 October 2026. | Small |
| **Automatic reply to Contact messages** | What if people got an email confirming their message arrived? | Left out on 16 October 2026: the on-screen thank you already says when to expect a reply. Sending email needs a mail service (for example a dedicated mailbox with an app password, or a transactional email provider) with its password kept in Heroku's config vars, a sender domain set up so replies are not marked as spam, and protection so the form cannot be used to send mail to addresses that never asked for it, for example by replying only once the address is confirmed. | Medium |
| **Password reset by email** | What if someone forgets their password? | Email service (SMTP) and Django's built-in reset views; an email address becomes a required field. | Medium |
| **Set completion tracker** | What if I want to know how close I am to finishing a set? | Count owned cards per set against `CardSet.quantity`; a progress bar on each set's cards. No new tables. | Small |
| **CSV export of my cards** | What if I want a backup or to use a spreadsheet? | A view that streams a CSV using Python's csv module. Import can follow later with validation. | Small |
| **Price history and trend charts** | What if I want to see how a card's value changes over time? | New CardPrice table (card, price, source, recorded_at), a scheduled job to record prices, and a chart library such as Chart.js. | Large |
| **Public profile and shareable collection** | What if I want to show my collection to a friend? | A Profile table with an is_public flag and a slug; a read-only page built from the Owned entries. Private by default. | Medium |

## Could if — worth exploring later

Good ideas that need a new table or a genuinely new skill (scheduled jobs, charts, theming). Worth a spike before committing to one.

| Feature | What if… | What it would need | Effort |
|---|---|---|---|
| **Condition and variant tracking** | What if I want to record a card's condition, or that I own a holo or graded copy? | Condition, variant and optional grading fields on CollectionEntry; the uniqueness rule changes from `(user, card)` to `(user, card, variant)`. | Medium |
| **Priority on wanted cards** | What if I want to rank my Wanted cards by how badly I want them? | A priority field on CollectionEntry, only meaningful when status is WANTED; sort Wanted by priority. | Small |
| **Multiple binders** | What if I keep separate collections (for example trade binder and display binder)? | A Binder table; CollectionEntry gets a binder foreign key and the uniqueness rule changes to include it. | Medium |
| **Card prices** | What if each card showed what it is worth? | Removed on purpose on 15 October 2026 (issue #48) to keep the project focused on CRUD. Adding prices back needs: a price source (the Pokémon TCG API includes TCGplayer prices in US dollars and Cardmarket prices in euros), a choice of currency per user with exchange rates, a scheduled job to refresh prices, a "price as of" date on every figure, and a note that prices are estimates. | Large |
| **Collection value over time** | What if I want to see my total value rise and fall? | Needs price history first, then a snapshot of the total per day and a line chart. | Large |
| **Price drop alerts** | What if I want to be told when a wanted card gets cheaper? | A target price field on CollectionEntry (for WANTED rows), price history, a scheduled job and email or in-app notifications. | Large |
| **Trade matching** | What if one collector has what another wants? | Compare one user's Owned cards with another's Wanted cards; Trade tables; strong privacy and abuse controls. | Large |
| **Dark mode and high-contrast theme** | What if bright pages are uncomfortable? | CSS custom properties for colours and a theme switch saved in the browser. | Small |
| **Installable app (PWA)** | What if I want to open it from my home screen? | A web app manifest and service worker; offline support is optional. | Medium |
| **Serve card pictures ourselves** | What if the Pokémon TCG image server went down for good, or became slow? | Today every picture is linked from `images.pokemontcg.io`, and a script shows CardVault's placeholder if the server cannot be reached, so the site keeps working. The full fix: download each picture once (as the card data already is), store it in cloud storage such as Amazon S3 or Cloudinary (not in the repository or on Heroku's temporary disk), serve it through a CDN, and update the Content Security Policy's `img-src`. Card artwork is copyrighted, so check the terms before hosting copies. | Medium |
| **Containerise with Docker** | What if the site had to run somewhere other than Heroku, or alongside extra services? | A `Dockerfile` that packages the app with its exact Python version and libraries into an image, built and stored in GitHub's Container Registry (free for public images), then run on any container host (Heroku, AWS, Google Cloud, Fly.io). Useful for moving hosts, matching every developer's setup exactly, and running extra containers such as a background import job (see "Scaling up" below). It does not by itself speed the site up or reduce image traffic: more traffic is handled by running more copies of the app and a bigger database, which Heroku already offers without Docker. Not needed while Heroku builds the app from `requirements.txt`. | Medium |
| **Other card games** | What if collectors want Magic or Yu-Gi-Oh! too? | A game field on CardSet, plus a data source for each game. | Large |
| **REST API and separate front end** | What if a mobile app or a React front end should use the same data? | Django REST Framework, token or session authentication and API tests. | Large |

## Scaling up: every Pokémon set

CardVault ships with one real set, the Base Set (102 cards), built
**once** from the [Pokémon TCG API](https://pokemontcg.io) by
`scripts/build_base_set_fixture.py`. The live site never calls the
API. What if collectors wanted every set (well over 150 sets and
more than 15,000 cards)?

| Step | What changes | Why |
|---|---|---|
| 1. Store each set's API id | Add `api_id` (for example `base1`) and `release_date` to `CardSet`, and `api_id` (for example `base1-4`) to `Card`, each unique. | Matching on the API's own ids lets an import update a card instead of creating a duplicate, and sorts sets by release. |
| 2. An import command instead of a fixture | A management command, `python manage.py import_sets`, that pages through the API (250 cards per request) and uses `update_or_create` on the API ids. | A 15,000-card fixture file is too big to review or reload by hand; a command can import one set or all of them, and can be re-run safely. |
| 3. An API key and rate limits | Register a free API key, store it as a Heroku config var (never in the code), and pause between requests. | Without a key the API allows far fewer requests per day. The key would be a secret like `SECRET_KEY`, protected the same way. |
| 4. Run the import on a schedule | Heroku Scheduler runs the command once a week to pick up new sets. | New sets are released several times a year; nobody has to remember to import them. |
| 5. Card numbers as text | Change `Card.number` from a whole number to text, with a separate sort key. | Newer sets have numbers such as `TG01` or `SV001` that are not plain integers. |
| 6. Rarities | Replace the four fixed rarity choices with a `Rarity` table, or a longer list. | Newer sets add rarities such as "Illustration Rare" and "Special Illustration Rare". |
| 7. Images | Keep linking to the API's image host with lazy loading and the placeholder fallback (both already done), or serve copies through a CDN (see "Serve card pictures ourselves"). | Thousands of images should not be stored in the repository or on Heroku's temporary disk. |
| 7b. Many users, same card | Nothing to change: each user's copy is a small `CollectionEntry` row pointing at the one shared `Card` (see [Design decisions](./DATABASE_SCHEMA.md#design-decisions-worth-knowing)). | More collectors means more small rows, never more copies of cards or pictures. |
| 8. Browsing at scale | Filter by set and rarity (US09), add database indexes on `name` and `card_set`, and keep 12 cards per page. | Searching 15,000 cards by name needs an index to stay fast; the existing pagination already copes. |
| 9. Hosting | Check the Heroku Postgres plan's storage limit and move up from `essential-0` if needed. | The smallest plan has the least storage; 15,000 cards plus users' entries and reviews would use much more than one set does. |

Effort: **Large** overall. Steps 1 to 3 (Medium) are enough to
import any chosen set on demand; steps 4 to 9 matter only for the
full catalogue.

## Won't if — deliberately out of scope

Interesting, but each one pulls in a dependency (payments, machine learning, a second codebase, real-time infrastructure) that is disproportionate to a learning project. Listed so the reasoning is on record, not because they are planned.

| Feature | What if… | What it would need | Effort |
|---|---|---|---|
| **In-app marketplace and payments** | What if collectors could buy and sell on the site? | Payments, fraud prevention, seller verification and legal obligations. Out of scope for a learning project. | Large |
| **Image recognition and barcode scanning** | What if I could scan a card to add it? | A machine-learning or third-party recognition service; accuracy and cost need research. | Large |
| **Native mobile apps** | What if there were iOS and Android apps? | Separate codebases or a cross-platform framework, plus an API. | Large |
| **Real-time chat between collectors** | What if collectors could message each other? | WebSockets, moderation and safeguarding. Not needed for the core idea. | Large |
