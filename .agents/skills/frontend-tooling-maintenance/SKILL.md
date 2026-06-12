---
name: frontend-tooling-maintenance
description: Maintain or upgrade bakerydemo frontend linting, formatting, and theme-related tooling with minimal churn
license: MIT
---

## Overview

Use this skill for `bakerydemo` frontend tooling tasks such as Prettier, Stylelint, ESLint, prek integration, and small native-CSS theme infrastructure updates.

## Methodology

### Preferred approach

- Keep changes minimal and reviewable.
- Prefer the repo's actual commands and workflows: `make lint`, `make format`, `npm run ...`, `prek`.
- When adopting stricter lint rules, use incremental overrides rather than forcing large unrelated CSS rewrites in one PR.

### Useful commands

- Install frontend dependencies with `npm ci`.
- Run repo-wide frontend checks with:
  - `npm run lint:css`
  - `npm run lint:js`
  - `npm run lint:format`
- Run targeted checks when only a few files changed or repo-wide tooling is noisy:
  - `npx stylelint bakerydemo/static/css/main.css`
  - `npx stylelint --fix bakerydemo/static/css/main.css`
  - `npx eslint bakerydemo/static/js/main.js`
  - `npx prettier --check bakerydemo/static/css/main.css bakerydemo/static/js/main.js`
- Use `make lint` or `make format` when you need the broader project-level workflow, not only frontend checks.

### Quality checks

- Run the smallest targeted lint commands needed for confidence.
- If repo-wide tooling is mid-migration, document any blocked checks and run focused file-level validation instead.

### Pitfalls

- Local environment directories such as `uvenv/` inside the repo can confuse glob-based frontend scripts.
- Keep theme tokens for text, surfaces, borders, and links separate from fixed effect tokens such as overlays, gradients, shadows, and inverse-on-image text.
