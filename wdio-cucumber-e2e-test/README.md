# wdio-cucumber-e2e-test

A small repository for WebdriverIO + Cucumber E2E tests (minimal starter).

This repo currently contains a simple `hello.js` and a minimal `package.json`.

## What’s included

- `hello.js` — a tiny demo file that you can run with Node.
- `package.json` — project metadata and scripts. At present the `test` script is the npm default (prints an error).

## Prerequisites

- Node.js (v14+ recommended) and npm installed.

## Install

From the project root, run:

```bash
npm install
```

(If you later add test dependencies like WebdriverIO, run `npm install` after updating `package.json`.)

## Run the demo

To run the simple `hello.js` file:

```bash
node hello.js
```

## Tests

Currently `package.json` contains the default `test` script that exits with an error. To run tests once you add them, use:

```bash
npm test
```

To add a typical WebdriverIO + Cucumber setup you might add dependencies and scripts such as:

```json
"scripts": {
  "wdio": "wdio run wdio.conf.js",
  "test": "npm run wdio"
}
```

## Contributing

If you want to add tests or examples:

- Create a feature file under `./features/` for Cucumber scenarios.
- Add step definitions under `./features/step-definitions/`.
- Add or update `wdio.conf.js` with your browser capabilities.

## Git: add and commit README

After creating or updating the README, run:

```bash
git add README.md
git commit -m "chore: add README.md"
git push origin Test
```

(Replace `Test` with your branch name if different.)

## License

This project uses the ISC license (see `package.json`).

---

If you want, I can also:

- Expand the README with a usage example from `hello.js` (I can insert the file contents and expected output).
- Update `package.json` with a friendly `start` or `demo` script like `"start": "node hello.js"` and run it to verify.
- Commit the README for you.

Tell me which of these you'd like next.