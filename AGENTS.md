# AGENTS Instructions

Additional guidance for AI coding agents working on `bakerydemo`.

## Project overview

`bakerydemo` is a Wagtail demo site for learning and showcasing common patterns.

The codebase is organized as a multi-app demo project:

- `bakerydemo/base/` for shared models, blocks, fixtures, and tests
- `bakerydemo/blog/`, `breads/`, `locations/`, `recipes/`, `people/`, `search/` for feature-specific apps
- `bakerydemo/templates/` and `bakerydemo/static/` for site-wide templates and frontend assets

## Key commands

```sh
npm ci            # Install frontend dependencies
make lint         # Ruff, djhtml, curlylint, frontend linting
make format       # Ruff, djhtml, frontend formatting/fixes
./manage.py check # Run Django system checks
./manage.py test  # Default local test run
prek install      # Install local git hooks
```

For render or template-focused Django tests, prefer the test settings:

```sh
env DJANGO_SETTINGS_MODULE=bakerydemo.settings.test ./manage.py test
```

This avoids manifest-staticfiles issues from `bakerydemo.settings.dev`.

## Frontend workflow

- JavaScript is intentionally minimal and framework-free.
- CSS is plain vanilla CSS, no Sass.
- When implementing theming, prefer built-in CSS and browser features such as `light-dark()` and `color-scheme` instead of a more complex custom theme system.
- Keep visual effect tokens (for example overlays, gradients, inverse-on-image text) separate from general page theme tokens.

## Testing guidance

- Render tests should generally live in `bakerydemo/<app>/tests/`.
- Prefer focused model and page setup over loading the full demo fixture, unless the fixture itself is under test.
- When testing search, remember `bakerydemo/search/views.py` intentionally hard-codes the searchable page models for the demo.

## Demo data and content

- The main demo fixture lives in `bakerydemo/base/fixtures/bakerydemo.json`.
- If fixture content changes, follow the documented fixture export and formatting steps in `CONTRIBUTING.md`.
- Avoid unnecessary fixture changes in unrelated pull requests.

## Pull request guidance

- Keep changes tightly scoped to the issue being worked on.
- Explain the "why" of the change, not only the implementation.
- Call out any areas that need careful visual or editorial review.
- Tell us how to test the changes.

## Bakerydemo-specific pitfalls

- Be careful when changing theme tokens: some existing tokens are used for fixed visual effects and should not become theme-dependent.
- The repo may have ongoing frontend-tooling migration work; if Stylelint or pre-commit config is mid-transition, prefer targeted checks and report the limitation clearly.
