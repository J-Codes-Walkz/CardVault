# Graph Report - cardvault-docs  (2026-10-12)

## Corpus Check
- Corpus is ~24,051 words - fits in a single context window. You may not need a graph.

## Summary
- 336 nodes · 578 edges · 19 communities (13 shown, 6 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 93 edges (avg confidence: 0.88)
- Token cost: 215,676 input · 0 output

## Community Hubs (Navigation)
- Catalogue Models and Admin
- Auth Adapter and Forms
- Account Tests
- My Cards User Stories
- Collection Entry Model
- Browsing and Review Stories
- Project Settings and Config
- Settings and Schema Docs
- My Cards View and Messages
- URLs and Collection Admin
- Review Model and Tests
- App Configs
- Register and Login Wireframe
- Planning-Stage ERD

## God Nodes (most connected - your core abstractions)
1. `CollectionEntry` - 24 edges
2. `CardSet` - 20 edges
3. `Card` - 20 edges
4. `CardVault README` - 17 edges
5. `Wireframe 05: My Cards, logged in (route /cards/mine/)` - 16 edges
6. `Review` - 15 edges
7. `CollectionEntryTests` - 13 edges
8. `RegisterTests` - 12 edges
9. `ReviewTests` - 12 edges
10. `CardTests` - 11 edges

## Surprising Connections (you probably didn't know these)
- `Usage of AI log (Claude for planning, building, debugging, tests)` --rationale_for--> `LoginForm`  [INFERRED]
  README.md → accounts/forms.py
- `Log in template (account/login.html)` --shares_data_with--> `LoginForm`  [INFERRED]
  templates/account/login.html → accounts/forms.py
- `Set completion tracker` --references--> `CardSet`  [EXTRACTED]
  docs/potential-upscale.md → cards/models.py
- `Base Set fixture (cards/fixtures/pokemon_cardsets.json)` --shares_data_with--> `CardSet`  [INFERRED]
  README.md → cards/models.py
- `US18 Submit a review` --conceptually_related_to--> `Review`  [INFERRED]
  docs/user-stories.md → cards/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **django-allauth register / log in / log out flow** — templates_account_signup, templates_account_login, templates_account_logout, templates_base_site_nav, templates_account_messages_signed_up, templates_account_messages_logged_in, templates_account_messages_logged_out, accounts_adapter_accountadapter, accounts_forms_loginform, docs_settings_snippet_authentication_django_allauth [INFERRED 0.85]
- **CardVault five-table schema (User, CardSet, Card, CollectionEntry, Review)** — docs_database_schema_django_user_model, cards_models_cardset, cards_models_card, collection_models_collectionentry, cards_models_review [EXTRACTED 1.00]
- **User feedback message pipeline (wording, framework, display rules, partial)** — docs_notification_messages_notification_messages, docs_notification_messages_django_messages_framework, docs_notification_messages_display_rules, templates_includes_messages, templates_base, docs_user_stories_us24 [INFERRED 0.85]
- **My Cards entry add / edit / remove flow** — docs_wireframes_04_card_detail_add_to_my_cards_control, docs_wireframes_06_forms_confirmations_add_edit_entry_form, docs_wireframes_06_forms_confirmations_remove_confirmation, docs_wireframes_05_my_cards_card_entries_table, docs_wireframes_05_my_cards_success_message [INFERRED 0.85]
- **Catalogue discovery: search, filter, browse grid, open card detail** — docs_wireframes_03_catalogue_search_by_name, docs_wireframes_03_catalogue_set_rarity_filters, docs_wireframes_03_catalogue_paginated_card_grid, docs_wireframes_04_card_detail_card_details_panel [INFERRED 0.85]
- **Responsive My Cards layout (desktop table to mobile stacked rows and collapsed menu)** — docs_wireframes_05_my_cards_card_entries_table, docs_wireframes_07_mobile_stacked_rows, docs_wireframes_07_mobile_collapsed_mobile_menu, docs_wireframes_01_home_navigation_bar [INFERRED 0.85]
- **Collection ownership: User holds Cards via Collection Entries** — docs_images_erd_user_table, docs_images_erd_card_table, docs_images_erd_collection_entry_table [EXTRACTED 1.00]
- **Card reviewing: User writes Reviews of Cards** — docs_images_erd_user_table, docs_images_erd_card_table, docs_images_erd_review_table [EXTRACTED 1.00]

## Communities (19 total, 6 thin omitted)

### Community 0 - "Catalogue Models and Admin"
Cohesion: 0.06
Nodes (14): CardAdmin, CardSetAdmin, ReviewAdmin, Migration, Card, Meta, Rarity, CardSet (+6 more)

### Community 1 - "Auth Adapter and Forms"
Cohesion: 0.06
Nodes (26): AccountAdapter, LoginForm, Database schema document, Django built-in User model, Entity-relationship diagram (Mermaid), Notification messages reference, In-app marketplace and payments, Password reset by email (+18 more)

### Community 2 - "Account Tests"
Cohesion: 0.08
Nodes (5): LoginTests, LogoutTests, message_texts(), NavigationTests, RegisterTests

### Community 3 - "My Cards User Stories"
Cohesion: 0.16
Nodes (26): Epic 3: My cards (owned and wanted), US04 See whether I am logged in, US11 Add a card to My Cards, US12 View my cards, US13 Edit a card entry, US14 Remove a card from My Cards, US15 See my collection summary, US16 Sort and filter my cards (+18 more)

### Community 4 - "Collection Entry Model"
Cohesion: 0.10
Nodes (10): CollectionEntry, Meta, Status, CollectionEntryTests, MyCardsViewTests, Condition and variant tracking, Could if: worth exploring later, Multiple binders (Binder table) (+2 more)

### Community 5 - "Browsing and Review Stories"
Cohesion: 0.13
Nodes (25): Epic 2: Browsing cards, Epic 4: Card reviews, US06 Understand the site's purpose on arrival, US07 Browse the card catalogue, US08 Search cards by name, US09 Filter cards by set and rarity, US10 View a card's details, US18 Submit a review (+17 more)

### Community 6 - "Project Settings and Config"
Cohesion: 0.11
Nodes (3): main(), epic_label(), main()

### Community 7 - "Settings and Schema Docs"
Cohesion: 0.11
Nodes (19): Populating the catalogue (JSON fixtures with explicit primary keys), settings.py reference, Epic 1: Accounts and authentication, Epic 5: Quality, security and content, US05 Keep my data private, US25 See helpful error pages, US26 Keep secrets and debug mode safe, US27 Populate the card catalogue (+11 more)

### Community 8 - "My Cards View and Messages"
Cohesion: 0.20
Nodes (14): My Cards template (collection/my_cards.html), my_cards(), Django messages framework (django.contrib.messages), US03 Log out, US23 Read and use the site easily (accessibility), Log in template (account/login.html), Log out confirmation template (account/logout.html), Logged-out message template (See you soon) (+6 more)

### Community 10 - "Review Model and Tests"
Cohesion: 0.22
Nodes (3): Review, Meta, ReviewTests

### Community 11 - "App Configs"
Cohesion: 0.20
Nodes (3): AccountsConfig, CardsConfig, CollectionConfig

### Community 12 - "Register and Login Wireframe"
Cohesion: 0.38
Nodes (7): US02 Log in, Calls to action (Create account, Browse cards), Log in form, Wireframe 02: Register / log in (route /accounts/register/), Registration form (username, password, confirm password), Registration validation states (username taken, weak password, password mismatch), Logged-in message template (Welcome back)

### Community 13 - "Planning-Stage ERD"
Cohesion: 1.00
Nodes (5): CARD entity (id PK, name, set_name, number, rarity, market_price, image_url), COLLECTION_ENTRY entity (id PK, user_id FK, card_id FK, status, quantity), CardVault Planning-Stage Entity-Relationship Diagram, REVIEW entity (id PK, user_id FK, card_id FK, rating, body), USER entity (id PK, username UK, email, password)

## Ambiguous Edges - Review These
- `CardVault README` → `Pokemon TCG API (candidate card data source)`  [AMBIGUOUS]
  README.md · relation: references
- `US17 Mark a wanted card as got it` → `'Got it!' button on Wanted entries`  [AMBIGUOUS]
  docs/wireframes/05-my-cards.svg · relation: implements

## Knowledge Gaps
- **14 isolated node(s):** `Code Institute Capstone Pre-Submission Checklist`, `Collectr (project concept inspiration)`, `Pokemon TCG API (candidate card data source)`, `Entity-relationship diagram (Mermaid)`, `REST API and separate front end` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 115 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CollectionEntry` connect `Collection Entry Model` to `Catalogue Models and Admin`, `Auth Adapter and Forms`, `My Cards User Stories`, `Settings and Schema Docs`, `My Cards View and Messages`, `URLs and Collection Admin`?**
  _High betweenness centrality (0.189) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `CollectionEntry` (e.g. with `Card` and `My Cards template (collection/my_cards.html)`) actually correct?**
  _`CollectionEntry` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Code Institute Capstone Pre-Submission Checklist`, `Collectr (project concept inspiration)`, `Pokemon TCG API (candidate card data source)` to the rest of the system?**
  _14 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Catalogue Models and Admin` be split into smaller, more focused modules?**
  _Cohesion score 0.0593990216631726 - nodes in this community are weakly interconnected._
- **Why does `CardVault README` connect `Auth Adapter and Forms` to `Catalogue Models and Admin`, `Review Model and Tests`, `Collection Entry Model`, `Settings and Schema Docs`?**
  _High betweenness centrality (0.176) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `CardVault README` and `Pokemon TCG API (candidate card data source)`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `US17 Mark a wanted card as got it` and `'Got it!' button on Wanted entries`?**
  _Edge tagged AMBIGUOUS (relation: implements) - confidence is low._