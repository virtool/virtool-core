# virtool-core

Core utilities for Virtool and associated packages.

![Tests](https://github.com/virtool/virtool-core/workflows/Tests/badge.svg?branch=master&event=push)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f04b88f74f2640588ba7dec5022c9b51)](https://www.codacy.com/gh/virtool/virtool-core/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=virtool/virtool-core&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/f04b88f74f2640588ba7dec5022c9b51)](https://www.codacy.com/gh/virtool/virtool-core/dashboard?utm_source=github.com&utm_medium=referral&utm_content=virtool/virtool-core&utm_campaign=Badge_Coverage)

## Install

### Last Stable Release

```shell script
pip install virtool-core
```

### Latest Changes

```shell script
pip install git+https://github.com/virtool/virtool-core.git
```

## Contribute 

### Unit Tests

#### Install Tox

`tox` is used to run the tests in a fresh virtual environment with all of the test dependencies. To install it use;

```shell script
pip install tox tox-poetry
```

#### Run Tests

```shell script
tox
```

Any arguments given to tox after a `--` token will be supplied to pytest.

```shell script
tox -- --log-cli-level=DEBUG
```

### Documentation

For docstrings, use the [**Sphinx** docstring format](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html).

The packages `sphinx_rtd_theme` and `sphinx_autoapi` are used in rendering the documentation. 

```  shell script
pip install sphinx_rtd_theme sphinx_autoapi
```

#### Markdown for Sphinx

[recommonmark](https://github.com/readthedocs/recommonmark) is used so that Sphinx can 
render documentation from *markdown* files as well as *rst* files. It will need to 
be installed before running `sphinx-build`:

```shell script
pip install recommonmark
```

To use sphinx rst [directives](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html) in a *markdown* file use the 
`eval_rst` [code block](https://recommonmark.readthedocs.io/en/latest/auto_structify.html#embed-restructuredtext)


#### Building the documentation

```shell script
cd sphinx && make html
```

The rendered HTML files are found under `sphinx/build/html`
