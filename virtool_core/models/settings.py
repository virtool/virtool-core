from virtool_core.models.basemodel import BaseModel


class Settings(BaseModel):
    sample_group: str = None
    sample_group_read: bool = True
    sample_group_write: bool = False
    sample_all_read: bool = True
    sample_all_write: bool = False
    sample_unique_names: bool = True
    hmm_slug: str = "virtool/virtool-hmm"
    enable_api: bool = False
    enable_sentry: bool = True
    minimum_password_length: int = 8
    default_source_types: list = ["isolate", "strain"]
