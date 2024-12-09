import pytest
from pydantic import ValidationError

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.validators import prevent_none


class DummyModel(BaseModel):
    count: int | None = None
    id: int | None = None
    name: str

    _prevent_none = prevent_none("count", "id")


def test_prevent_null_validator():
    """Tests the `prevent_none` validator for the `DummyModel` model prevents the
    provided fields from being `None`.
    """
    DummyModel(name="baz")
    DummyModel(name="bar", id=1, count=2)

    with pytest.raises(ValidationError) as count_err:
        DummyModel(name="foo", id=2, count=None)

    assert "Value may not be null" in str(count_err)

    with pytest.raises(ValidationError) as id_err:
        DummyModel(name="bob", id=None)

    assert "Value may not be null" in str(id_err)

    with pytest.raises(ValidationError) as err:
        DummyModel(name="baz_1", id=None, count=None)

    assert "Value may not be null" in str(err)
