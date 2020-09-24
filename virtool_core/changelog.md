# virtool/utils.py

- function `get_static_hash` is only used by `virtool.http.errors.py`
    - leaving it out of virtool.utils with the intention of moving it to the 
      `virtool-core.http` package
- `average_list` was removed as it is only used once in the virtool source
    - It will be inlined 
- `to_bool` was not ported over as it only has two usages and can be 
   easily inlined
- `coerce_list` is only used from `virtool.api.utils`. It has been removed and
  will be inlined. 
  
- `get_client_path` is only used in startup.py and will be inlined there

- `get_temp_dir` is equivalent to `tempfile.TemporaryDirectory`.
   did not port over in favor of using `tempfile.TemporaryDirectory`
   directly. 
   
# virtool/db/core.py

- added type hints to Collection arguments
- removed `silent` option in favor of `enqueue_change` defaulting to 
  None
- move `virtool.utils.base_processor` to `virtool-core.db.utils`

# virtool/caches/utils.py

- functions `join_cache_path` and `join_cache_read_path` require the application settings
  as a parameter but only use the string `settings["data_path"]`. Suggest changing the parameter
  to a string. 
    - same for `samples.join_sample_path` and `samples.join_legacy_read_path`