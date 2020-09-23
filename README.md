Core utilities for Virtool and associated packages.

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f04b88f74f2640588ba7dec5022c9b51)](https://www.codacy.com/gh/virtool/virtool-core/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=virtool/virtool-core&amp;utm_campaign=Badge_Grade)

# Install

```
    git clone https://github.com/virtool/virtool-core
    cd virtool-core && pip install .
```

## ToDos



## Contributing 

### Running Tests

The testing framework used is [pytest](https://docs.pytest.org/en/stable/) 

Install it using

```
pip install pytest
```

And run the tests using `pytest .`
from the root directory

#### MongoDB

some tests require an instance of MongoDB to be running on the 
local machine. If you do not have MongoDB installed you can use
the [run_mongo_with_tests.sh](tests/run_mongo_with_tests.sh) script
to run mongo using docker. The docker container used to run mongo
will be stopped and removed once the tests have completed. 

### Documentation

For docstrings use the **Sphinx** docstring format as described [here](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html)

#### Markdown for Sphinx

[recommonmark](https://github.com/readthedocs/recommonmark) is used so that Sphinx can 
render documentation from *markdown* files as well as *rst* files. It will need to 
be installed before running `sphinx-build`

```
pip install recommonmark
```

To use sphinx rst [directives](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html) in a *markdown* file use the 
`eval_rst` [code block](https://recommonmark.readthedocs.io/en/latest/auto_structify.html#embed-restructuredtext)


#### Building the documentation

```
make html
```

The rendered HTML files are found under [build/html](build/html)
