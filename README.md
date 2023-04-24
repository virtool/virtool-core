# virtool-core

Core utilities for Virtool and associated packages.

![Tests](https://github.com/virtool/virtool-core/workflows/Tests/badge.svg?branch=master&event=push)
[![PyPI version](https://badge.fury.io/py/virtool-core.svg)](https://badge.fury.io/py/virtool-core)

## Install

Install `virtool_core` with `pip`:

```
pip install virtool-core
```

## Contributing

### Commits

All commits must follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0) specification.

These standardized commit messages are used to automatically publish releases using [`semantic-release`](https://semantic-release.gitbook.io/semantic-release)
after commits are merged to `main` from successful PRs.

**Example**

```text
feat: add API support for assigning labels to existing samples
```

Descriptive bodies and footers are required where necessary to describe the impact of the commit. Use bullets where appropriate.

Additional Requirements
1. **Write in the imperative**. For example, _"fix bug"_, not _"fixed bug"_ or _"fixes bug"_.
2. **Don't refer to issues or code reviews**. For example, don't write something like this: _"make style changes requested in review"_.
Instead, _"update styles to improve accessibility"_.
3. **Commits are not your personal journal**. For example, don't write something like this: _"got server running again"_
or _"oops. fixed my code smell"_.

From Tim Pope: [A Note About Git Commit Messages](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)

### Tests

1. Install Tox

   `tox` is used to run the tests in a fresh virtual environment with all of the test dependencies. To install it use;

   ```shell script
   pip install tox tox-poetry
   ```

2. Run Tests

   ```shell script
   tox
   ```

Any arguments given to tox after a `--` token will be supplied to pytest:
```shell script
tox -- --log-cli-level=DEBUG
```

### Documentation

For docstrings, use the [**Sphinx** docstring format](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html).

Build the documentation with:
```shell script
cd sphinx && make html
```

The rendered HTML files are found under `sphinx/build/html`


