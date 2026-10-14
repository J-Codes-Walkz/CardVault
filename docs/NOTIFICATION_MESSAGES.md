# Notification messages

Every action that changes data, or that the checklist asks to be
confirmed (log in, log out, create, edit, delete), shows a message
using Django's `django.contrib.messages` framework. Register, log in
and log out are handled by django-allauth; their wording is set in
`accounts/adapter.py` and `templates/account/messages/`. This is the
single reference for the exact wording, so templates and views stay
consistent instead of drifting as the app grows. `{card}` and similar
are placeholders filled in per request.

| Situation | Type | Message | Story |
|---|---|---|---|
| Register: success (the new user is logged in straight away) | Success | Your account has been created. Welcome to CardVault, {username}! | US01 |
| Register: username already used | Error | That username is already taken. Please choose another. | US01 |
| Register: password too weak | Error | Django's own validator message naming the rule that was broken, for example "This password is too short. It must contain at least 8 characters.", "This password is too common.", "This password is entirely numeric." or "The password is too similar to the username." | US01 |
| Register: passwords differ | Error | You must type the same password each time. | US01 |
| Log in: success | Success | Welcome back, {username}! | US02 |
| Log in: wrong details | Error | Invalid username or password. Please try again. | US02 |
| Log out | Success | You have been logged out. See you soon! | US03 |
| Private page while logged out | Info | Please log in to view that page. | US05 |
| My Cards: add | Success | {card} was added to your cards. | US11 |
| My Cards: duplicate | Error | You already have {card} on your list. Edit that entry to change it. | US11 |
| My Cards: edit | Success | Your entry for {card} was updated. | US13 |
| My Cards: remove | Success | {card} was removed from your cards. | US14 |
| My Cards: got it! (Wanted &rarr; Owned) | Success | {card} moved to your collection. | US17 |
| Review: submit | Success | Thank you for submitting your review! | US18 |
| Review: edit | Success | Your review was updated successfully. | US19 |
| Review: delete | Success | Your review was deleted. | US20 |
| Any form with errors | Error | Please correct the errors below and try again. | US24 |

## Display rules (US24)

- Success and error messages are visually distinct using an icon and
  a word ("Success:", "Error:") as well as colour, never colour
  alone, per the accessibility story (US23).
- Success messages use `role="status"`; error messages use
  `role="alert"`, so screen readers announce them without the user
  needing to find them.
- A message stays visible until the user dismisses it or navigates to
  the next page — see wireframe 06 (`docs/wireframes/06-forms-confirmations.svg`)
  for the visual pattern.

## Suggested Django pattern

```python
from django.contrib import messages

messages.success(request, "Your entry for "
                           f"{entry.card.name} was updated.")
messages.error(request, "You already have "
                         f"{card.name} on your list. Edit that "
                         "entry to change it.")
```

Keep the wording itself in one place (for example a small
`messages_text.py` per app, or inline as above) so a tester checking
this table against the running site is checking the same strings the
views actually use.
