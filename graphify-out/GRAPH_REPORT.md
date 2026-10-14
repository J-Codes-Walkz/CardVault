# Graph Report - cardvault-docs  (2026-10-14)

## Corpus Check
- 49 files · ~30,997 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 597 nodes · 1120 edges · 48 communities (25 shown, 23 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 148 edges (avg confidence: 0.88)
- Token cost: 172,791 input · 0 output

## Community Hubs (Navigation)
- My Cards Add Tests
- Auth Adapter and Forms
- Card Model and Admin
- Agile and Bug Tracking
- Login and Account Tests
- Project Settings and Config
- Shared View Mixins
- Catalogue Page and Search
- Catalogue Admin and Reviews
- Card Detail and Review Form
- My Cards Stories and Messages
- Account and Quality Stories
- Review CRUD Tests
- Card and Review URLs
- Potential Upscale Ideas
- My Cards Edit and Remove
- Card Model Tests
- Security and Bug Log
- Models and Migrations
- Star Rating Helpers
- Fixture and Home Tests
- Review Create View
- My Cards Add View
- Review Stories and Wireframes
- App Configs
- Card Sets and Tester Cards
- Card Page Tests
- My Cards Wireframe Stories
- Catalogue Tests
- Security Settings
- Browsing Stories
- Home Page
- Planning-Stage ERD
- Validators
- Database URL Library
- PostgreSQL Driver
- Dotenv Library

## God Nodes (most connected - your core abstractions)
1. `CardVault README` - 66 edges
2. `User stories doc` - 40 edges
3. `Testing write-up` - 39 edges
4. `Card` - 38 edges
5. `CollectionEntry` - 33 edges
6. `CardSet` - 25 edges
7. `Review` - 25 edges
8. `Notification messages doc` - 20 edges
9. `Potential upscale doc` - 20 edges
10. `ReviewCrudTests` - 18 edges

## Surprising Connections (you probably didn't know these)
- `Usage of AI log` --rationale_for--> `LoginForm`  [INFERRED]
  README.md → accounts/forms.py
- `Signed-up message template (account created)` --conceptually_related_to--> `AccountAdapter`  [INFERRED]
  templates/account/messages/signed_up.txt → accounts/adapter.py
- `Base Set fixture (cards/fixtures/pokemon_cardsets.json)` --shares_data_with--> `CardSet`  [INFERRED]
  README.md → cards/models.py
- `US05: Keep my data private` --references--> `LoginMessageMixin`  [INFERRED]
  docs/USER_STORIES.md → accounts/mixins.py
- `US24: Get feedback on every action` --references--> `FormErrorMixin`  [INFERRED]
  docs/USER_STORIES.md → accounts/mixins.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Card reviewing: User writes Reviews of Cards** — docs_images_erd_user_table, docs_images_erd_card_table, docs_images_erd_review_table [EXTRACTED 1.00]
- **Collection ownership: User holds Cards via Collection Entries** — docs_images_erd_user_table, docs_images_erd_card_table, docs_images_erd_collection_entry_table [EXTRACTED 1.00]
- **My Cards full CRUD on CollectionEntry** — docs_user_stories_us11, docs_user_stories_us12, docs_user_stories_us13, docs_user_stories_us14, collection_models_collectionentry [INFERRED 0.95]
- **Review CRUD on Review model** — docs_user_stories_us18, docs_user_stories_us19, docs_user_stories_us20, docs_user_stories_us21, cards_models_review [INFERRED 0.95]
- **Fail-safe production security settings** — docs_settings_snippet_secret_key_no_default, docs_settings_snippet_debug_default_false, docs_settings_snippet_production_hardening, docs_user_stories_us26, testing_check_deploy [INFERRED 0.85]
- **Review create/edit/delete flow** — cards_templates_cards_card_detail_reviews_section, cards_templates_cards_review_form_template, cards_templates_cards_review_confirm_delete_template, cards_views_reviewcreate, cards_views_reviewedit, cards_views_reviewdelete, cards_forms_reviewform [INFERRED 0.85]
- **My Cards entry add/edit/remove flow** — cards_templates_cards_card_detail_my_cards_panel, collection_templates_collection_entry_form_template, collection_templates_collection_entry_confirm_delete_template, collection_templates_collection_my_cards_template, collection_views_entrycreate, collection_views_entryedit, collection_views_entrydelete [INFERRED 0.85]
- **Card browsing via card tiles** — templates_home_template, cards_templates_cards_card_list_template, templates_includes_card_tile_template, cards_templates_cards_card_detail_template [INFERRED 0.85]
- **Browse catalogue and add card to My Cards** — docs_wireframes_03_catalogue_search_by_name, docs_wireframes_03_catalogue_set_rarity_filters, docs_wireframes_03_catalogue_card_grid, docs_wireframes_04_card_detail_card_info, docs_wireframes_04_card_detail_add_to_my_cards, docs_wireframes_06_forms_confirmations_add_edit_entry_form, docs_wireframes_05_my_cards_success_message [INFERRED 0.85]
- **Manage My Cards entries (edit, remove, confirm)** — docs_wireframes_05_my_cards_entries_table, docs_wireframes_06_forms_confirmations_add_edit_entry_form, docs_wireframes_06_forms_confirmations_remove_confirmation, docs_wireframes_06_forms_confirmations_message_styles [INFERRED 0.85]
- **Responsive My Cards layout** — docs_wireframes_05_my_cards_entries_table, docs_wireframes_07_mobile_stacked_rows, docs_wireframes_07_mobile_mobile_menu, docs_wireframes_01_home_navigation_bar [INFERRED 0.75]

## Communities (48 total, 23 thin omitted)

### Community 0 - "My Cards Add Tests"
Cohesion: 0.06
Nodes (6): EntryCreateTests, EntryDeleteTests, EntryEditTests, make_card(), message_texts(), MyCardsViewTests

### Community 1 - "Auth Adapter and Forms"
Cohesion: 0.07
Nodes (20): AccountAdapter, LoginForm, Password reset by email, US01: Register an account, US02: Log in, US06: Understand the site's purpose on arrival, Home wireframe, Calls to action (Create account / Browse cards) (+12 more)

### Community 2 - "Card Model and Admin"
Cohesion: 0.07
Nodes (15): Card, Meta, Rarity, CollectionEntryAdmin, CollectionEntry, Meta, Status, CollectionEntryTests (+7 more)

### Community 3 - "Agile and Bug Tracking"
Cohesion: 0.09
Nodes (31): Bug report issue template, bug label, Issue template config, Populating the catalogue (fixtures), GitHub Projects board, US27: Populate the card catalogue, Automated testing (45 Django tests), Heroku automatic deploys from GitHub (+23 more)

### Community 4 - "Login and Account Tests"
Cohesion: 0.09
Nodes (5): LoginTests, LogoutTests, message_texts(), NavigationTests, RegisterTests

### Community 5 - "Project Settings and Config"
Cohesion: 0.10
Nodes (4): main(), docs/github-issues.csv, epic_label(), main()

### Community 6 - "Shared View Mixins"
Cohesion: 0.13
Nodes (3): FormErrorMixin, LoginMessageMixin, django.contrib.messages framework

### Community 7 - "Catalogue Page and Search"
Cohesion: 0.12
Nodes (11): account_logout URL (allauth), account_signup URL (allauth), Card list pagination, Card name search form, CardListView, My Cards entry table, My Cards status filter tabs, MyCardsView (+3 more)

### Community 8 - "Catalogue Admin and Reviews"
Cohesion: 0.15
Nodes (6): CardAdmin, CardSetAdmin, ReviewAdmin, Review, Meta, ReviewTests

### Community 9 - "Card Detail and Review Form"
Cohesion: 0.18
Nodes (9): account_login URL (allauth), ReviewForm, Meta, Card detail My Cards panel, Card rating summary, Card detail reviews section, CardDetailView, CollectionEntryForm (+1 more)

### Community 10 - "My Cards Stories and Messages"
Cohesion: 0.20
Nodes (15): Notification messages doc, Epic: My cards (owned and wanted), US11: Add a card to My Cards, US13: Edit a card entry, US14: Remove a card from My Cards, US17: Mark a wanted card as got it, US24: Get feedback on every action, Add to My Cards control (+7 more)

### Community 11 - "Account and Quality Stories"
Cohesion: 0.19
Nodes (16): User stories doc, Epic: Accounts and authentication, Epic: Quality, security and content, US03: Log out, US04: See whether I am logged in, US22: Use the site on any device, US23: Read and use the site easily, US25: See helpful error pages (+8 more)

### Community 13 - "Card and Review URLs"
Cohesion: 0.13
Nodes (4): OwnReviewMixin, ReviewDelete, ReviewEdit, US20: Delete my review

### Community 14 - "Potential Upscale Ideas"
Cohesion: 0.14
Nodes (15): Potential upscale doc, Collection value over time, Condition and variant tracking, CSV export of my cards, Dark mode and high-contrast theme, Image recognition and barcode scanning, Multiple binders, Native mobile apps (+7 more)

### Community 15 - "My Cards Edit and Remove"
Cohesion: 0.14
Nodes (3): EntryDelete, EntryEdit, OwnEntryMixin

### Community 16 - "Card Model Tests"
Cohesion: 0.18
Nodes (3): CardTests, make_card(), ReviewEditedTests

### Community 17 - "Security and Bug Log"
Cohesion: 0.19
Nodes (13): US05: Keep my data private, Security scope (in / out), Testing write-up, Automated Django test suite (96 tests), Bug #43: Generic .gitignore template, Bug #44: Non-standard Python line splits, Bug #45: Hand-written README table of contents, Bug #46: Markdown file names not capitalised (+5 more)

### Community 21 - "Fixture and Home Tests"
Cohesion: 0.17
Nodes (3): BaseSetFixtureTests, CardSetTests, HomePageTests

### Community 24 - "Review Stories and Wireframes"
Cohesion: 0.21
Nodes (12): Epic: Card reviews, US10: View a card's details, US18: Submit a review, US19: Edit my review, US21: Read reviews on a card, Featured cards row, Card grid, Card detail wireframe (+4 more)

### Community 25 - "App Configs"
Cohesion: 0.20
Nodes (3): AccountsConfig, CardsConfig, CollectionConfig

### Community 26 - "Card Sets and Tester Cards"
Cohesion: 0.20
Nodes (5): CardSet, Meta, TesterFixtureTests, pokemon_cardsets fixture (Base Set), Other card games

### Community 28 - "My Cards Wireframe Stories"
Cohesion: 0.22
Nodes (10): Set completion tracker, US12: View my cards, US15: See my collection summary, US16: Sort and filter my cards, My Cards wireframe, Sort control, Status tabs (All / Owned / Wanted), Collection summary figures (+2 more)

### Community 30 - "Security Settings"
Cohesion: 0.28
Nodes (4): settings.py reference, US26: Keep secrets and debug mode safe, Whitenoise, manage.py check --deploy

### Community 31 - "Browsing Stories"
Cohesion: 0.28
Nodes (9): Epic: Browsing cards, US07: Browse the card catalogue, US08: Search cards by name, US09: Filter cards by set and rarity, Catalogue (Browse cards) wireframe, Pagination controls, Search by name, Set and rarity filters (+1 more)

### Community 33 - "Planning-Stage ERD"
Cohesion: 1.00
Nodes (5): CARD entity (id PK, name, set_name, number, rarity, market_price, image_url), COLLECTION_ENTRY entity (id PK, user_id FK, card_id FK, status, quantity), CardVault Planning-Stage Entity-Relationship Diagram, REVIEW entity (id PK, user_id FK, card_id FK, rating, body), USER entity (id PK, username UK, email, password)

## Ambiguous Edges - Review These
- `Pokemon TCG API (candidate card data source)` → `CardVault README`  [AMBIGUOUS]
  README.md · relation: references

## Knowledge Gaps
- **39 isolated node(s):** `Django 5.2.18`, `allauth layout base template (allauth/layouts/base.html)`, `Agile methodology (GitHub Projects board and issues)`, `Code Institute Capstone Pre-Submission Checklist`, `Collectr (inspiration)` (+34 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 253 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CardVault README` connect `Agile and Bug Tracking` to `Auth Adapter and Forms`, `Card Model and Admin`, `Project Settings and Config`, `Catalogue Admin and Reviews`, `My Cards Stories and Messages`, `Account and Quality Stories`, `Card and Review URLs`, `Potential Upscale Ideas`, `Security and Bug Log`, `Review Stories and Wireframes`, `Card Sets and Tester Cards`, `My Cards Wireframe Stories`, `Security Settings`, `Browsing Stories`?**
  _High betweenness centrality (0.339) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `Card` (e.g. with `card_detail.html` and `CardTests`) actually correct?**
  _`Card` has 20 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Django 5.2.18`, `allauth layout base template (allauth/layouts/base.html)`, `Agile methodology (GitHub Projects board and issues)` to the rest of the system?**
  _39 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `My Cards Add Tests` be split into smaller, more focused modules?**
  _Cohesion score 0.056910569105691054 - nodes in this community are weakly interconnected._
- **Why does `Card` connect `Card Model and Admin` to `Home Page`, `My Cards Add Tests`, `Agile and Bug Tracking`, `Shared View Mixins`, `Catalogue Page and Search`, `Catalogue Admin and Reviews`, `Card Detail and Review Form`, `Card Model Tests`, `Test Suites`, `Models and Migrations`, `Review Create View`, `My Cards Add View`, `Review Stories and Wireframes`, `Card Sets and Tester Cards`, `Catalogue Tests`, `Browsing Stories`?**
  _High betweenness centrality (0.220) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `CollectionEntry` (e.g. with `Card detail My Cards panel` and `CollectionEntryForm`) actually correct?**
  _`CollectionEntry` has 15 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Pokemon TCG API (candidate card data source)` and `CardVault README`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._