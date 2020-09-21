# virtool/utils.py

- function `get_static_hash` is only used by `virtool.http.errors.py`
    - leaving it out of virtool.utils with the intention of moving it to the 
      `virtool-core.http` package
- Instance check in `average_list` removed in favor of type hints