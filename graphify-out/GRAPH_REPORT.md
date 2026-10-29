# Graph Report - cardvault-docs  (2026-10-29)

## Corpus Check
- 86 files · ~60,293 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1052 nodes · 1614 edges · 99 communities (31 shown, 68 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 144 edges (avg confidence: 0.91)
- Token cost: 134,463 input · 0 output

## Community Hubs (Navigation)
- Account Adapter and Allauth
- Settings, Deployment and Docs
- Page Templates and Error Pages
- Migrations, Cache Clean-up, Tests
- Log In and Delete Tests
- Card Sets and Fixtures
- Admin Log In and Account Views
- Home and Browse Catalogue
- My Cards URLs and Views
- User Stories and Wireframes
- Error Page Tests
- Privacy, Age Check, Accessibility
- Review Form and URLs
- App Configurations
- Poké Ball Rating Tags
- CI and Notification Messages
- Card Model Tests
- Review Create View
- Forms and View Modules
- Review CRUD Tests
- Catalogue Search Tests
- CollectionEntry Model
- My Cards User Stories
- Review Model
- My Cards Sort Tests
- Add to My Cards View
- Delete Account Form and View
- Card Model and Rarity
- Add Card Tests
- Contact Page Tests
- ContactMessage Model
- Upscale Ideas and Contact Data
- Form Error Mixin and Contact URLs
- Age Check Tests
- Login Rate Limit Tests
- Navigation and Cache Tests
- Card Page and Review Stories
- Card Admin
- Review Model Tests
- Visitor Key and Rate Limit
- CI Jobs and Security Scans
- Admin Login Tests
- Admin Site Tests
- Catalogue Tests
- Got It Tests
- My Cards View Tests
- Contact Form
- Database Schema
- Privacy Page Tests
- Base Set Fixture Tests
- Card Detail View
- Security Headers Middleware
- Collection Summary Tests
- Edit Entry Tests
- My Cards Rating Tests
- Delete Account Tests
- Remove Entry Tests
- Contact Admin
- Security Header Tests
- Collection Test Helpers
- Home and Contact Link Tests
- Clear Expired Cache Command
- Login Message Mixin
- Collection Admin
- Planning-Stage ERD
- Feedback Messages Stories
- Admin Link Tests
- Contact Admin Tests
- Database Settings Tests
- Username Rule Tests
- Menu and Theme Script
- Allauth Layout
- Issue Template Config
- Card Rating Summary
- Card List Pagination
- dj-database-url
- Django
- gunicorn
- psycopg
- python-dotenv
- Whitenoise
- Featured Cards Section

## God Nodes (most connected - your core abstractions)
1. `User stories doc` - 40 edges
2. `Card` - 34 edges
3. `CardSet` - 30 edges
4. `CollectionEntry` - 26 edges
5. `Review` - 21 edges
6. `Base Layout Template` - 20 edges
7. `SearchAndFilterTests` - 19 edges
8. `SortAndFilterTests` - 19 edges
9. `README` - 19 edges
10. `ReviewCrudTests` - 18 edges

## Surprising Connections (you probably didn't know these)
- `Login Template (US02)` --shares_data_with--> `LoginForm`  [INFERRED]
  templates/account/login.html → accounts/forms.py
- `Signed-up message template (account created)` --conceptually_related_to--> `AccountAdapter`  [INFERRED]
  templates/account/messages/signed_up.txt → accounts/adapter.py
- `Card detail My Cards panel` --shares_data_with--> `CollectionEntryForm`  [INFERRED]
  cards/templates/cards/card_detail.html → collection/forms.py
- `Card detail My Cards panel` --shares_data_with--> `CollectionEntry`  [INFERRED]
  cards/templates/cards/card_detail.html → collection/models.py
- `Home hero section` --references--> `CardListView`  [EXTRACTED]
  templates/home.html → cards/views.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Card reviewing: User writes Reviews of Cards** — docs_images_erd_user_table, docs_images_erd_card_table, docs_images_erd_review_table [EXTRACTED 1.00]
- **Collection ownership: User holds Cards via Collection Entries** — docs_images_erd_user_table, docs_images_erd_card_table, docs_images_erd_collection_entry_table [EXTRACTED 1.00]
- **Responsive My Cards layout** — docs_wireframes_05_my_cards_entries_table, docs_wireframes_07_mobile_stacked_rows, docs_wireframes_07_mobile_mobile_menu, docs_wireframes_01_home_navigation_bar [INFERRED 0.75]
- **Browse catalogue and add card to My Cards** — docs_wireframes_03_catalogue_search_by_name, docs_wireframes_03_catalogue_set_rarity_filters, docs_wireframes_03_catalogue_card_grid, docs_wireframes_04_card_detail_card_info, docs_wireframes_04_card_detail_add_to_my_cards, docs_wireframes_06_forms_confirmations_add_edit_entry_form, docs_wireframes_05_my_cards_success_message [INFERRED 0.85]
- **Manage My Cards entries (edit, remove, confirm)** — docs_wireframes_05_my_cards_entries_table, docs_wireframes_06_forms_confirmations_add_edit_entry_form, docs_wireframes_06_forms_confirmations_remove_confirmation, docs_wireframes_06_forms_confirmations_message_styles [INFERRED 0.85]
- **Fail-safe production security settings** — docs_settings_snippet_secret_key_no_default, docs_settings_snippet_debug_default_false, docs_settings_snippet_production_hardening, docs_user_stories_us26 [INFERRED 0.85]
- **CI-gated Heroku deployment pipeline** — _github_workflows_ci_test, _github_workflows_ci_security, readme_wait_for_ci, readme_heroku_deployment [EXTRACTED 1.00]
- **My Cards CRUD stories on CollectionEntry** — docs_user_stories_us11, docs_user_stories_us12, docs_user_stories_us13, docs_user_stories_us14, docs_user_stories_us17, docs_database_schema_collectionentry [EXTRACTED 1.00]
- **Login abuse defence layers** — readme_rate_limiting, readme_trusted_proxy_count, readme_django_allauth, testing_bug_66, readme_django_admin [INFERRED 0.85]
- **Custom HTTP error pages** — templates_400, templates_403, templates_403_csrf, templates_404, templates_429, templates_500, templates_errors_error_base [EXTRACTED 1.00]
- **My Cards collection management flow** — collection_templates_collection_my_cards, collection_templates_collection_entry_form, collection_templates_collection_entry_confirm_delete, collection_templates_collection_got_it, cards_templates_cards_card_detail [INFERRED 0.95]
- **Allauth account authentication pages** — templates_account_login, templates_account_logout, templates_account_signup, templates_account_signup_closed [INFERRED 0.95]

## Communities (99 total, 68 thin omitted)

### Community 0 - "Account Adapter and Allauth"
Cohesion: 0.05
Nodes (15): AccountAdapter, age_on(), LoginForm, SignupForm, settings.py reference, US01 Register an account, US02 Log in, US26 Keep secrets and debug mode safe (+7 more)

### Community 1 - "Settings, Deployment and Docs"
Cohesion: 0.07
Nodes (10): Catalogue fixtures (pokemon_cardsets, base_set_cards, tester_cards), US27 Populate the card catalogue, main(), Pokemon TCG API, fetch_cards(), fetch_page(), main(), to_fixture() (+2 more)

### Community 2 - "Page Templates and Error Pages"
Cohesion: 0.09
Nodes (33): Delete Account Template (US30), Card Detail Template (US10, US21), Card List / Browse Template (US07-US09), Review Confirm Delete Template (US20), Review Form Template (US18, US19), Entry Confirm Delete Template (US14), Entry Form Template (US11, US13), Got It Template (US17) (+25 more)

### Community 3 - "Migrations, Cache Clean-up, Tests"
Cohesion: 0.12
Nodes (4): Migration, Migration, Migration, Migration

### Community 4 - "Log In and Delete Tests"
Cohesion: 0.09
Nodes (4): LoginTests, LogoutTests, message_texts(), RegisterTests

### Community 5 - "Card Sets and Fixtures"
Cohesion: 0.08
Nodes (8): CardSet, Meta, BaseSetFixtureTests, CardSetTests, HomePageTests, ImageFallbackTests, RarityBadgeTests, TesterFixtureTests

### Community 6 - "Admin Log In and Account Views"
Cohesion: 0.10
Nodes (4): admin_allowed(), admin_login(), SignupView, favicon()

### Community 7 - "Home and Browse Catalogue"
Cohesion: 0.08
Nodes (8): Card name search form, CardListView, HomeView, search_cards(), My Cards status filter tabs, MyCardsView, Site navigation, Home hero section

### Community 8 - "My Cards URLs and Views"
Cohesion: 0.08
Nodes (5): Card detail My Cards panel, EntryDelete, EntryEdit, EntryGotIt, OwnEntryMixin

### Community 9 - "User Stories and Wireframes"
Cohesion: 0.10
Nodes (25): Bug report issue template, bug label, User stories doc, US04 See whether I am logged in, US06 Understand the site's purpose on arrival, US07 Browse the card catalogue, US08 Search cards by name, US09 Filter cards by set and rarity (+17 more)

### Community 10 - "Error Page Tests"
Cohesion: 0.10
Nodes (5): BadRequestPageTests, FormExpiredPageTests, NotFoundPageTests, PermissionDeniedPageTests, ServerErrorPageTests

### Community 11 - "Privacy, Age Check, Accessibility"
Cohesion: 0.10
Nodes (22): US29 Check my age when I register, US32 Use CardVault with low vision, hearing loss or a keyboard, Age check (under-13 refusal, COPPA/Children's Code), Brand and design (collector's vault), clear_expired_cache release command, Database security management, Heavy traffic handling (gunicorn 2x4, 10s query timeout), ALLAUTH_TRUSTED_PROXY_COUNT = 1 (+14 more)

### Community 12 - "Review Form and URLs"
Cohesion: 0.10
Nodes (6): ReviewForm, Meta, Card detail reviews section, OwnReviewMixin, ReviewDelete, ReviewEdit

### Community 13 - "App Configurations"
Cohesion: 0.10
Nodes (4): AccountsConfig, CardsConfig, CollectionConfig, ContactConfig

### Community 14 - "Poké Ball Rating Tags"
Cohesion: 0.14
Nodes (4): ball(), ball_icon(), balls(), PokeBallRatingTests

### Community 15 - "CI and Notification Messages"
Cohesion: 0.13
Nodes (16): CI workflow (ci.yml), Notification messages doc, django.contrib.messages framework, US25 See helpful error pages, US28 Manage data in Django admin, README, Agile methodology (GitHub Projects board), CardVault web app (+8 more)

### Community 16 - "Card Model Tests"
Cohesion: 0.13
Nodes (3): CardTests, make_card(), ReviewEditedTests

### Community 18 - "Forms and View Modules"
Cohesion: 0.16
Nodes (4): CollectionEntryForm, Meta, GotItForm, Meta

### Community 21 - "CollectionEntry Model"
Cohesion: 0.12
Nodes (4): CollectionEntry, Meta, Status, CollectionEntryTests

### Community 22 - "My Cards User Stories"
Cohesion: 0.15
Nodes (17): US12 View my cards, US13 Edit a card entry, US14 Remove a card from My Cards, US15 See my collection summary, US16 Sort and filter my cards, US17 Mark a wanted card as got it, My Cards wireframe, Empty state message (+9 more)

### Community 23 - "Review Model"
Cohesion: 0.12
Nodes (3): Review, Meta, CardDetailTests

### Community 27 - "Card Model and Rarity"
Cohesion: 0.13
Nodes (3): Card, Meta, Rarity

### Community 30 - "ContactMessage Model"
Cohesion: 0.16
Nodes (3): ContactMessage, Meta, ContactMessageModelTests

### Community 31 - "Upscale Ideas and Contact Data"
Cohesion: 0.18
Nodes (11): ContactMessage model, Potential upscale doc, Two-factor login for the admin (allauth mfa), Could if tier, Dedicated CardVault mailbox / auto reply, Should if tier, US05 Keep my data private, US34 Contact CardVault (+3 more)

### Community 35 - "Navigation and Cache Tests"
Cohesion: 0.18
Nodes (3): ClearExpiredCacheTests, NavigationTests, SignupRateLimitTests

### Community 36 - "Card Page and Review Stories"
Cohesion: 0.22
Nodes (11): US10 View a card's details, US18 Submit a review, US21 Read reviews on a card, Featured cards row, Card grid, Card detail wireframe, Add to My Cards control, Card info panel (+3 more)

### Community 37 - "Card Admin"
Cohesion: 0.20
Nodes (3): CardAdmin, CardSetAdmin, ReviewAdmin

### Community 40 - "CI Jobs and Security Scans"
Cohesion: 0.25
Nodes (7): CI PostgreSQL 18 service container, CI job: Security scans, CI job: Lint and test, Bandit, flake8 (PEP8 lint), pip-audit, Secrets via .env and Heroku config vars

### Community 47 - "Database Schema"
Cohesion: 0.44
Nodes (8): Database schema doc, Card model, CardSet model, CollectionEntry model, Entity-relationship diagram, Review model, User (django.contrib.auth), Scaling up to every Pokemon set

### Community 64 - "Planning-Stage ERD"
Cohesion: 1.00
Nodes (5): CARD entity (id PK, name, set_name, number, rarity, market_price, image_url), COLLECTION_ENTRY entity (id PK, user_id FK, card_id FK, status, quantity), CardVault Planning-Stage Entity-Relationship Diagram, REVIEW entity (id PK, user_id FK, card_id FK, rating, body), USER entity (id PK, username UK, email, password)

### Community 65 - "Feedback Messages Stories"
Cohesion: 0.50
Nodes (4): US23 Read and use the site easily, US24 Get feedback on every action, Success message banner, Message styles

## Knowledge Gaps
- **40 isolated node(s):** `Logged-in message template (Welcome back)`, `Logged-out message template (See you soon)`, `Django 5.2.18`, `django-allauth 65.19.7`, `gunicorn 26.2.0` (+35 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 500 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **68 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Notification messages doc` connect `CI and Notification Messages` to `Account Adapter and Allauth`, `Feedback Messages Stories`?**
  _High betweenness centrality (0.188) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `Card` (e.g. with `AdminSiteTests` and `DeleteAccountTests`) actually correct?**
  _`Card` has 19 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Logged-in message template (Welcome back)`, `Logged-out message template (See you soon)`, `Django 5.2.18` to the rest of the system?**
  _40 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Account Adapter and Allauth` be split into smaller, more focused modules?**
  _Cohesion score 0.0467687074829932 - nodes in this community are weakly interconnected._
- **Why does `README` connect `CI and Notification Messages` to `User Stories and Wireframes`, `Privacy, Age Check, Accessibility`, `Upscale Ideas and Contact Data`, `Database Schema`?**
  _High betweenness centrality (0.174) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `CardSet` (e.g. with `AdminSiteTests` and `DeleteAccountTests`) actually correct?**
  _`CardSet` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Should `Settings, Deployment and Docs` be split into smaller, more focused modules?**
  _Cohesion score 0.06533776301218161 - nodes in this community are weakly interconnected._