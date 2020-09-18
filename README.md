Core utilities for Virtool and associated packages.

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
