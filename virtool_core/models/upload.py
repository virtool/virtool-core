from datetime import datetime

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.searchresult import SearchResult
from virtool_core.models.user_base import UserNested


class UploadMinimal(BaseModel):
    """Model for user uploads."""

    id: int
    created_at: datetime
    name: str
    name_on_disk: str
    ready: bool
    removed: bool
    removed_at: datetime | None
    reserved: bool
    size: int | None
    type: str
    uploaded_at: datetime | None
    user: UserNested


Upload = UploadMinimal


class UploadSearchResult(SearchResult):
    items: list[UploadMinimal]
