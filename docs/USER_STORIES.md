# User stories

Every story follows the standard template: **As a** &lt;role&gt;, **I want** &lt;goal&gt;, **so that** &lt;benefit&gt;, with testable acceptance criteria underneath. Priorities use the MoSCoW method (**Must have**, **Should have**, **Could have**; nothing currently sits in Won't have). These stories map 1:1 onto the project's GitHub Issues, and the issues to the [GitHub Projects board](https://github.com/users/J-Codes-Walkz/projects/5).

Each user story's ID (for example `US01`) is used as its GitHub Issue title prefix and as a label on the project board, so a story, its issue and its card can always be matched up.

## All stories at a glance

| ID | Story | Epic | Priority |
|----|-------|------|----------|
| US01 | Register an account | Accounts and authentication | Must have |
| US02 | Log in | Accounts and authentication | Must have |
| US03 | Log out | Accounts and authentication | Must have |
| US04 | See whether I am logged in | Accounts and authentication | Must have |
| US05 | Keep my data private | Accounts and authentication | Must have |
| US06 | Understand the site's purpose on arrival | Browsing cards | Must have |
| US07 | Browse the card catalogue | Browsing cards | Must have |
| US08 | Search cards by name | Browsing cards | Must have |
| US09 | Filter cards by set and rarity | Browsing cards | Should have |
| US10 | View a card's details | Browsing cards | Must have |
| US11 | Add a card to My Cards | My cards (owned and wanted) | Must have |
| US12 | View my cards | My cards (owned and wanted) | Must have |
| US13 | Edit a card entry | My cards (owned and wanted) | Must have |
| US14 | Remove a card from My Cards | My cards (owned and wanted) | Must have |
| US15 | See my collection summary | My cards (owned and wanted) | Should have |
| US16 | Sort and filter my cards | My cards (owned and wanted) | Could have |
| US17 | Mark a wanted card as got it | My cards (owned and wanted) | Could have |
| US18 | Submit a review | Card reviews | Must have |
| US19 | Edit my review | Card reviews | Must have |
| US20 | Delete my review | Card reviews | Should have |
| US21 | Read reviews on a card | Card reviews | Must have |
| US22 | Use the site on any device | Quality, security and content | Must have |
| US23 | Read and use the site easily | Quality, security and content | Must have |
| US24 | Get feedback on every action | Quality, security and content | Must have |
| US25 | See helpful error pages | Quality, security and content | Should have |
| US26 | Keep secrets and debug mode safe | Quality, security and content | Must have |
| US27 | Populate the card catalogue | Quality, security and content | Must have |
| US28 | Manage data in Django admin | Quality, security and content | Should have |

## MoSCoW breakdown

- **Must have** (21): US01, US02, US03, US04, US05, US06, US07, US08, US10, US11, US12, US13, US14, US18, US19, US21, US22, US23, US24, US26, US27
- **Should have** (5): US09, US15, US20, US25, US28
- **Could have** (2): US16, US17
- **Won't have (this submission)**: nothing is scoped out yet within this story set — see [Potential upscale](./POTENTIAL_UPSCALE.md) for features deliberately parked for after submission.

## Stories by epic

## 1. Accounts and authentication

### US01 — Register an account

**Priority:** `Must have`

> As a **new visitor**, I want **to register with a username and password**, so that **I can build and keep my own card collection**.

**Acceptance criteria**

- [ ] The form asks for a username, a password and a password confirmation.
- [ ] After registering I am logged in straight away, taken to My Cards and see "Your account has been created. Welcome to CardVault, <username>!"
- [ ] If the username already exists I see "That username is already taken. Please choose another."
- [ ] If the password is too weak I am asked for a more complex one and told which rule it broke (minimum length, too common, numbers only, too similar to the username).
- [ ] If the two passwords differ I see an error and no account is created.

**Development tasks**

- [ ] Use Django's built-in User model with django-allauth's registration form (no custom user model needed).
- [ ] Include django-allauth's URLs and write the register template.
- [ ] Add the success and error messages (see the notification messages table in the README).
- [ ] Write tests for a duplicate username, a weak password and mismatched passwords.

**Manual test**

- Action: Register with a new username and a strong password. Then try an existing username, a short password and mismatched passwords.
- Expected result: The new account is created with the success message. Each bad attempt shows the matching error and creates no account.

### US02 — Log in

**Priority:** `Must have`

> As a **registered user**, I want **to log in with my username and password**, so that **I can reach my cards and reviews**.

**Acceptance criteria**

- [ ] A correct username and password logs me in and I see "Welcome back, <username>!".
- [ ] A wrong username or password shows "Invalid username or password. Please try again." and does not reveal which part was wrong.
- [ ] After logging in I land on My Cards, or on the page I was originally trying to reach.

**Development tasks**

- [ ] Add the login view and template.
- [ ] Configure the redirect after login.
- [ ] Add the welcome and error messages.
- [ ] Write tests for valid and invalid credentials.

**Manual test**

- Action: Log in with valid credentials, then with invalid credentials.
- Expected result: Valid: welcome message and redirect. Invalid: error message and I stay logged out.

### US03 — Log out

**Priority:** `Must have`

> As a **logged-in user**, I want **to log out**, so that **nobody else can use my account on a shared device**.

**Acceptance criteria**

- [ ] A Log out button is visible in the navigation whenever I am logged in.
- [ ] Logging out ends my session and shows "You have been logged out. See you soon!"
- [ ] Logout is sent as a POST request with a CSRF token (Django 5 does not allow logging out through a plain link).
- [ ] After logging out, my private pages redirect to the login page.

**Development tasks**

- [ ] Add a logout form (POST) to the navigation.
- [ ] Show the logged-out message and check it still displays after the session is cleared.
- [ ] Test that logged-out users are redirected from private pages.

**Manual test**

- Action: Click Log out, then try to open My Cards.
- Expected result: The logout message is shown and My Cards redirects to the login page.

### US04 — See whether I am logged in

**Priority:** `Must have`

> As a **visitor or user**, I want **to see at a glance whether I am logged in**, so that **I know whether I can use My Cards**.

**Acceptance criteria**

- [ ] When logged in, the navigation shows "Logged in as <username>", My Cards and Log out.
- [ ] When logged out, the navigation shows only Browse cards, Log in and Register (no private links).
- [ ] The same states appear in the mobile menu.

**Development tasks**

- [ ] Build the navigation in the base template using user.is_authenticated.
- [ ] Build the matching mobile menu.
- [ ] Check both states on every page.

**Manual test**

- Action: Compare the navigation logged out and logged in, on desktop and mobile widths.
- Expected result: Each state shows the correct links and the username when logged in.

### US05 — Keep my data private

**Priority:** `Must have`

> As a **registered user**, I want **only me to be able to view, edit and delete my card entries and reviews**, so that **nobody else can tamper with my records**.

**Acceptance criteria**

- [ ] A logged-out visitor opening a private page is sent to the login page with "Please log in to view that page."
- [ ] Changing the ID in the address bar to another user's record returns a 404 page and changes nothing.
- [ ] Edit and Remove buttons only appear on records I own.
- [ ] Tests with two users prove that user B cannot view, edit or delete user A's records.

**Development tasks**

- [ ] Protect every private view with LoginRequiredMixin (or login_required).
- [ ] Filter every private queryset by request.user so other users' IDs return 404.
- [ ] Only render Edit and Remove for the record owner.
- [ ] Write two-user tests for view, edit and delete.

**Manual test**

- Action: Log out and open /cards/mine/. Then log in as user B and open the URL of one of user A's card entries.
- Expected result: Logged out: redirected to login with the message. User B: 404 page and nothing is changed.

## 2. Browsing cards

### US06 — Understand the site's purpose on arrival

**Priority:** `Must have`

> As a **visitor**, I want **to see what the site does as soon as I arrive**, so that **I can decide whether to sign up**.

**Acceptance criteria**

- [ ] The home page headline and one-line description say what the site is for.
- [ ] Clear calls to action: "Create account" and "Browse cards" for visitors, "Go to My Cards" for logged-in users.
- [ ] A row of featured cards shows what the catalogue looks like.
- [ ] The navigation shows where everything is.

**Development tasks**

- [ ] Build the home view and template.
- [ ] Add the hero section and calls to action (different when logged in).
- [ ] Query a few featured cards for the home page.
- [ ] Test the page for logged-in and logged-out users.

**Manual test**

- Action: Open the home page logged out, then logged in.
- Expected result: The purpose is clear within a few seconds and the calls to action change with login state.

### US07 — Browse the card catalogue

**Priority:** `Must have`

> As a **visitor or user**, I want **to browse a catalogue of cards**, so that **I can discover cards and find the ones I own**.

**Acceptance criteria**

- [ ] Cards appear in a grid, 12 per page, each showing image, name, set, number and rarity.
- [ ] Previous, Next and page numbers let me move between pages.
- [ ] Each card links to its detail page.
- [ ] It works without logging in, images have alt text, and a missing image shows a placeholder.

**Development tasks**

- [ ] Build a paginated catalogue ListView.
- [ ] Create a reusable card tile template.
- [ ] Add a placeholder image for missing artwork.
- [ ] Test pagination.

**Manual test**

- Action: Open /cards/ and move between pages.
- Expected result: 12 cards per page, Previous and Next work, and clicking a card opens its page.

### US08 — Search cards by name

**Priority:** `Must have`

> As a **visitor or user**, I want **to search for a card by name**, so that **I can quickly find a specific card**.

**Acceptance criteria**

- [ ] A search box on the catalogue finds partial, case-insensitive matches (for example "char" finds Charizard).
- [ ] The number of results is shown.
- [ ] No match shows "No cards match '<term>'. Try a different name." with a link to clear the search.
- [ ] The search term stays in the box and in the pagination links.

**Development tasks**

- [ ] Add a search form (GET) to the catalogue.
- [ ] Filter the queryset with name__icontains.
- [ ] Keep the search term in pagination links.
- [ ] Write tests for a match and for no match.

**Manual test**

- Action: Search for "char", then search for a nonsense term.
- Expected result: Matching cards are shown with a count; the nonsense term shows the empty-state message.

### US09 — Filter cards by set and rarity

**Priority:** `Should have`

> As a **visitor or user**, I want **to filter the catalogue by set and by rarity**, so that **I can narrow down a large catalogue**.

**Acceptance criteria**

- [ ] Set and rarity dropdowns filter the catalogue.
- [ ] Filters combine with the name search.
- [ ] A Clear filters link resets everything.
- [ ] Filters are kept when I move between pages.

**Development tasks**

- [ ] Add the filter form and populate the dropdowns from the CardSet table and the Card rarity choices.
- [ ] Apply the filters to the queryset.
- [ ] Keep filters in pagination links.
- [ ] Write tests for combined filters.

**Manual test**

- Action: Choose a set and a rarity, then add a name search.
- Expected result: Only cards matching every filter are shown and Clear filters restores the full list.

### US10 — View a card's details

**Priority:** `Must have`

> As a **visitor or user**, I want **to open a card and see its details**, so that **I can decide whether to add or review it**.

**Acceptance criteria**

- [ ] The page shows a large image, name, set, number, rarity and market price (or "Price unavailable").
- [ ] The average rating and number of reviews are shown.
- [ ] When logged in I see the add-to-My-Cards and review controls.
- [ ] When logged out I see "Log in to add this card" instead of the controls.
- [ ] An unknown card ID shows a 404 page.

**Development tasks**

- [ ] Build the card DetailView and template.
- [ ] Show the controls only to logged-in users.
- [ ] Add the average rating and review count (Avg and Count).
- [ ] Write tests for logged-in, logged-out and unknown ID.

**Manual test**

- Action: View a card logged in and logged out.
- Expected result: Details are shown to both; controls appear only when logged in; logged-out users see the login prompt.

## 3. My cards (owned and wanted)

### US11 — Add a card to My Cards

**Priority:** `Must have`

> As a **logged-in user**, I want **to add a card to My Cards, as owned or wanted, with a quantity**, so that **I can track what I have and what I'm still after**.

**Acceptance criteria**

- [ ] The form lets me choose a status (Owned or Wanted, default Owned) and a quantity (minimum 1).
- [ ] Success shows "<Card> was added to your cards."
- [ ] Adding a card that's already on my list shows "You already have <Card> on your list. Edit that entry to change it." with a link to edit it.
- [ ] A quantity of 0 or less is rejected with an error.
- [ ] The new entry appears in My Cards under the status I chose.

**Development tasks**

- [ ] Create the CollectionEntry form and the create view (card taken from the URL).
- [ ] Handle duplicates with a friendly form error as well as the database's unique-together constraint on (user, card).
- [ ] Add the success and error messages.
- [ ] Write tests for create, duplicate and invalid quantity.

**Manual test**

- Action: Add a card as Owned with quantity 2. Add the same card again. Try quantity 0.
- Expected result: First add: success message and the entry is listed as Owned. Second: friendly duplicate error. Quantity 0: rejected.

### US12 — View my cards

**Priority:** `Must have`

> As a **logged-in user**, I want **to see every card on my list, owned and wanted**, so that **I know what I have and what I'm still looking for**.

**Acceptance criteria**

- [ ] Each entry shows image, name, set, status and quantity, newest first.
- [ ] A tab or filter switches between Owned, Wanted and All.
- [ ] Only my own entries are listed.
- [ ] An empty list shows "Your cards list is empty. Browse cards to add your first one." with a link to the catalogue.
- [ ] Every entry has Edit and Remove buttons.

**Development tasks**

- [ ] Build the My Cards ListView filtered by request.user, with a status query parameter.
- [ ] Build the table layout for desktop and stacked layout for mobile.
- [ ] Add the empty state (per status and overall).
- [ ] Test that users only see their own entries and that the status filter works.

**Manual test**

- Action: Log in as user A (with Owned and Wanted entries) and user B (with none). Switch between the Owned, Wanted and All tabs.
- Expected result: A sees only their own cards, grouped correctly by tab; B sees the empty-state message.

### US13 — Edit a card entry

**Priority:** `Must have`

> As a **logged-in user**, I want **to change the status, quantity or notes on a card on my list**, so that **my list stays accurate as my collection changes**.

**Acceptance criteria**

- [ ] Edit opens a pre-filled form (status, quantity and notes).
- [ ] Saving shows "Your entry for <Card> was updated."
- [ ] A quantity below 1 shows an error.
- [ ] I cannot edit another user's entry (404).

**Development tasks**

- [ ] Build the UpdateView limited to the current user's entries.
- [ ] Add the success message.
- [ ] Write tests for a valid edit, an invalid edit and another user's entry.

**Manual test**

- Action: Edit the quantity and status of an entry, then try quantity 0.
- Expected result: The valid change is saved with the message; the invalid change is rejected with an error.

### US14 — Remove a card from My Cards

**Priority:** `Must have`

> As a **logged-in user**, I want **to remove a card from my list**, so that **my list only shows cards I still have or still want**.

**Acceptance criteria**

- [ ] Remove opens a confirmation page that names the card.
- [ ] Confirming deletes the entry and shows "<Card> was removed from your cards."
- [ ] Cancel returns to My Cards with no changes.
- [ ] Deleting another user's entry returns a 404.
- [ ] The card itself stays in the catalogue.

**Development tasks**

- [ ] Build the DeleteView limited to the current user's entries.
- [ ] Create the confirmation template.
- [ ] Add the success message.
- [ ] Write tests for delete, cancel and another user's entry.

**Manual test**

- Action: Remove an entry and confirm. Repeat and press Cancel.
- Expected result: Confirmed: the entry is gone with the message. Cancel: nothing changes.

### US15 — See my collection summary

**Priority:** `Should have`

> As a **logged-in user**, I want **to see totals for the cards I own**, so that **I can see how big and how valuable my collection is**.

**Acceptance criteria**

- [ ] My Cards shows total owned cards (sum of quantities where status is Owned), unique entries and estimated value (market price x quantity).
- [ ] Wanted entries are excluded from the totals.
- [ ] Cards without a price are left out of the value and a note says how many were excluded.
- [ ] Values are shown as currency with 2 decimal places.

**Development tasks**

- [ ] Add aggregate queries (Sum with F expressions) filtered to status=OWNED.
- [ ] Add the summary section to the template.
- [ ] Write tests with known prices and quantities.

**Manual test**

- Action: Add Owned cards with known prices and quantities, one without a price, and a Wanted card.
- Expected result: Totals match a manual calculation of the Owned cards only, and the exclusion note appears.

### US16 — Sort and filter my cards

**Priority:** `Could have`

> As a **logged-in user**, I want **to sort and filter my cards**, so that **I can find cards in a large list**.

**Acceptance criteria**

- [ ] I can sort by name, set or date added.
- [ ] I can filter by set and by status.
- [ ] My choices appear in the address so the page can be bookmarked.

**Development tasks**

- [ ] Add the sort and filter form.
- [ ] Only allow known sort fields (whitelist).
- [ ] Write tests for sorting and filtering.

**Manual test**

- Action: Sort by name, then filter to Wanted only.
- Expected result: The order and the list change as chosen.

### US17 — Mark a wanted card as got it

**Priority:** `Could have`

> As a **logged-in user**, I want **to flip a wanted card to owned in one step**, so that **I do not have to remove it and re-add it**.

**Acceptance criteria**

- [ ] A "Got it!" button appears on Wanted entries.
- [ ] Pressing it changes that entry's status to Owned and asks for the quantity.
- [ ] Success shows "<Card> moved to your collection."
- [ ] I cannot flip another user's entry (404).

**Development tasks**

- [ ] Add a small status-change view limited to the current user's Wanted entries.
- [ ] Pre-fill the quantity field.
- [ ] Write tests for the status change and for another user's entry.

**Manual test**

- Action: Press "Got it!" on a Wanted card and confirm the quantity.
- Expected result: The entry now shows under Owned with the message, and no longer appears under Wanted.

## 4. Card reviews

### US18 — Submit a review

**Priority:** `Must have`

> As a **logged-in user**, I want **to rate a card from 1 to 5 and write a review**, so that **other collectors can read my opinion**.

**Acceptance criteria**

- [ ] The review form (rating 1-5 and text) is only shown to logged-in users.
- [ ] Submitting shows "Thank you for submitting your review!"
- [ ] I can only review a card once: if I already have, the form is replaced by my review and an Edit button.
- [ ] Rating and text are required.
- [ ] The review appears in the card's review list straight away.

**Development tasks**

- [ ] Create the ReviewForm and the create view.
- [ ] Enforce one review per user per card (form check as well as the database constraint).
- [ ] Add the success message.
- [ ] Write tests for create, duplicate and logged-out access.

**Manual test**

- Action: Submit a review on a card, then try to review the same card again.
- Expected result: First: thank-you message and the review is listed. Second: the form is replaced by my review with Edit.

### US19 — Edit my review

**Priority:** `Must have`

> As a **logged-in user**, I want **to go back and edit a review I wrote**, so that **I can correct or update my opinion**.

**Acceptance criteria**

- [ ] Edit opens a pre-filled form.
- [ ] Saving shows "Your review was updated successfully."
- [ ] An edited review is marked as edited in the list.
- [ ] I cannot edit anyone else's review (404).

**Development tasks**

- [ ] Build the UpdateView limited to the current user's reviews.
- [ ] Show an "edited" marker when updated_at differs from created_at.
- [ ] Add the success message.
- [ ] Write tests including another user's review.

**Manual test**

- Action: Edit my review and save.
- Expected result: The change is saved with the message and the review shows an edited marker.

### US20 — Delete my review

**Priority:** `Should have`

> As a **logged-in user**, I want **to delete a review I wrote**, so that **I can withdraw an opinion I no longer hold**.

**Acceptance criteria**

- [ ] Delete opens a confirmation page.
- [ ] Confirming shows "Your review was deleted."
- [ ] Cancel changes nothing.
- [ ] I cannot delete anyone else's review (404).

**Development tasks**

- [ ] Build the DeleteView limited to the current user's reviews.
- [ ] Create the confirmation template and message.
- [ ] Write tests for delete, cancel and another user's review.

**Manual test**

- Action: Delete my review and confirm. Repeat and press Cancel.
- Expected result: Confirmed: the review is gone with the message. Cancel: no change.

### US21 — Read reviews on a card

**Priority:** `Must have`

> As a **visitor or user**, I want **to read other collectors' reviews of a card**, so that **I can learn from their opinions**.

**Acceptance criteria**

- [ ] Reviews are listed newest first with username, star rating, text and date.
- [ ] The average rating and review count are shown at the top.
- [ ] No reviews shows "No reviews yet. Be the first to review this card."
- [ ] Reviews are visible to logged-out visitors.
- [ ] Edit and Delete only appear on my own reviews.

**Development tasks**

- [ ] Query the reviews for the card.
- [ ] Calculate the average rating and count.
- [ ] Build the review list template.
- [ ] Write tests for the list, the average and the empty state.

**Manual test**

- Action: View a card with several reviews, then one with none.
- Expected result: Reviews and the average appear; the empty state appears when there are none.

## 5. Quality, security and content

### US22 — Use the site on any device

**Priority:** `Must have`

> As a **visitor or user**, I want **the site to work on my phone, tablet and computer**, so that **I can use it wherever I am**.

**Acceptance criteria**

- [ ] Pages are usable and readable from 320px wide up to large desktop screens.
- [ ] The navigation collapses into a menu on small screens.
- [ ] There is no horizontal scrolling and images scale.
- [ ] Buttons and links are large enough to tap comfortably.

**Development tasks**

- [ ] Write mobile-first CSS with sensible breakpoints.
- [ ] Build the responsive navigation.
- [ ] Test at 320, 768, 1024 and 1440px and on a real phone.
- [ ] Run Lighthouse on mobile.

**Manual test**

- Action: Open every page at 320, 768, 1024 and 1440px wide.
- Expected result: No overlapping, cut-off or sideways-scrolling content at any width.

### US23 — Read and use the site easily

**Priority:** `Must have`

> As a **visitor or user**, I want **the site to be accessible and easy to read**, so that **everyone, including keyboard and screen reader users, can use it**.

**Acceptance criteria**

- [ ] Pages use header, nav, main and footer landmarks and a logical heading order.
- [ ] Every form field has a visible label.
- [ ] Card images have alt text (the card name).
- [ ] Text and controls meet WCAG AA colour contrast.
- [ ] Everything can be reached by keyboard with a visible focus outline.
- [ ] Interactive elements are recognisable without relying on colour alone.

**Development tasks**

- [ ] Audit every template for landmarks, headings, labels and alt text.
- [ ] Check the colour palette contrast.
- [ ] Test keyboard-only navigation.
- [ ] Run Lighthouse and WAVE and record the results.

**Manual test**

- Action: Use the whole site with the keyboard only, then run Lighthouse and WAVE on each page.
- Expected result: Every control is reachable with a visible focus and no critical accessibility errors are reported.

### US24 — Get feedback on every action

**Priority:** `Must have`

> As a **user**, I want **a message every time I log in, log out, register, create, edit or delete something**, so that **I know the action worked or what went wrong**.

**Acceptance criteria**

- [ ] Each of those actions shows a message (see the notification messages table in the README).
- [ ] Success and error messages look different, using an icon and text as well as colour.
- [ ] Messages are announced to screen readers (role="status" for success, role="alert" for errors).
- [ ] Messages stay visible until dismissed or the next page loads.

**Development tasks**

- [ ] Build a messages partial in the base template.
- [ ] Style success, info and error messages.
- [ ] Use Django's messages framework in every view that changes data.
- [ ] Write tests that the messages appear.

**Manual test**

- Action: Perform each action (register, log in, log out, create, edit, delete).
- Expected result: Each action shows the correct message in the correct style.

### US25 — See helpful error pages

**Priority:** `Should have`

> As a **visitor or user**, I want **a friendly page when something goes wrong**, so that **I know what happened and how to get back**.

**Acceptance criteria**

- [ ] Custom 404 (not found), 403 (forbidden) and 500 (server error) pages explain the problem in plain language.
- [ ] Each has a link back to the home page.
- [ ] They show no technical details and appear when DEBUG is False.

**Development tasks**

- [ ] Create 404.html, 403.html and 500.html.
- [ ] Keep the 500 page free of template logic that could fail.
- [ ] Test with DEBUG set to False.

**Manual test**

- Action: With DEBUG False, open a URL that does not exist.
- Expected result: The custom 404 page is shown with a link home.

### US26 — Keep secrets and debug mode safe

**Priority:** `Must have`

> As a **site owner**, I want **secret keys kept out of the code and debug switched off in production**, so that **the live site is secure**.

**Acceptance criteria**

- [ ] No SECRET_KEY, database password or API key is in the repository or its history.
- [ ] Settings read secrets from environment variables, and DEBUG is False unless explicitly set to True.
- [ ] .env is listed in .gitignore and a .env.example file lists the variable names without values.
- [ ] The live Heroku app holds its secrets as config vars and shows no debug pages.

**Development tasks**

- [ ] Load settings from environment variables.
- [ ] Add .env to .gitignore and create .env.example.
- [ ] Set the config vars on Heroku.
- [ ] Scan the repository for secrets before each submission.

**Manual test**

- Action: Search the repository and its history for secrets, then open a URL that does not exist on the live site.
- Expected result: No secrets are found and the live site shows the normal 404 page, not a debug page.

### US27 — Populate the card catalogue

**Priority:** `Must have`

> As a **site owner**, I want **the catalogue filled with real card data**, so that **users can find the cards they own**.

**Acceptance criteria**

- [ ] A JSON fixture (or entries typed into Django admin) provides enough Card rows to demo every feature.
- [ ] Loading the fixture with manage.py loaddata can be re-run safely (it replaces matching rows rather than duplicating them).
- [ ] The data covers more than one set and more than one rarity, so the filter and search stories have something to find.

**Development tasks**

- [ ] Decide fixture vs. admin entry (a fixture is easier to re-run after resetting the database).
- [ ] Write cards/fixtures/cards.json with a representative set of cards, or enter them in Django admin.
- [ ] Document the one command (python manage.py loaddata cards) needed to seed a fresh database.

**Manual test**

- Action: Reset the database, run migrations, then load the fixture (or re-enter the admin data).
- Expected result: The catalogue shows the seeded cards with no errors and no duplicates on a second load.

### US28 — Manage data in Django admin

**Priority:** `Should have`

> As a **site owner**, I want **to manage cards and users in the Django admin**, so that **I can fix mistakes without touching the database directly**.

**Acceptance criteria**

- [ ] Card, CollectionEntry and Review are registered with sensible list columns and search.
- [ ] Only superusers can log in to the admin.
- [ ] I can correct a wrong card detail from the admin.

**Development tasks**

- [ ] Register the models in each app's admin.py.
- [ ] Add list_display and search_fields.
- [ ] Create a superuser locally and on Heroku.

**Manual test**

- Action: Log in to /admin/ as a superuser and as an ordinary user.
- Expected result: The superuser can edit a card; the ordinary user is refused.
