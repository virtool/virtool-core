from typing import Optional

import pytest
from pydantic import validator, ValidationError

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.validators import prevent_none


class DummyModel(BaseModel):
    name: str
    id: int
    count: Optional[int]

    _prevent_none_count = validator("count", allow_reuse=True)(prevent_none)


def test_prevent_null_validator():

    DummyModel(name="baz", id=0)

    DummyModel(name="bar", id=1, count=2)

    with pytest.raises(ValidationError) as err:
        DummyModel(name="foo", id=2, count=None)

    assert "Value may not be null" in str(err)
