# virtool-core

Core utilities for Virtool and associated packages.

[![Build Status](https://cloud.drone.io/api/badges/virtool/virtool-core/status.svg)](https://cloud.drone.io/virtool/virtool-core)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f04b88f74f2640588ba7dec5022c9b51)](https://www.codacy.com/gh/virtool/virtool-core/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=virtool/virtool-core&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/f04b88f74f2640588ba7dec5022c9b51)](https://www.codacy.com/gh/virtool/virtool-core/dashboard?utm_source=github.com&utm_medium=referral&utm_content=virtool/virtool-core&utm_campaign=Badge_Coverage)

## Install

```shell script
git clone https://github.com/virtool/virtool-core
cd virtool-core && pip install .
```

## Contribute 

### Running Tests

The testing framework used is [pytest](https://docs.pytest.org/en/stable/). Install it using:
```shell script
pip install pytest
```

Run the tests from the root directory:
```shell script
pytest
```

### MongoDB

Some tests require an instance of MongoDB to be running on the 
local machine.

If you do not have MongoDB installed you can use
the [run_mongo_with_tests.sh](tests/run_mongo_with_tests.sh) script
to run mongo using docker. The docker container used to run mongo
will be stopped and removed once the tests have completed. 

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
