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
