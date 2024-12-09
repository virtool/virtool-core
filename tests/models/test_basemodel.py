import pytest

from virtool_core.models.basemodel import BaseModel


class DummyModel(BaseModel):
    id: str
    name: str


@pytest.mark.parametrize("has_underscore_prefix", [True, False])
def test_id(has_underscore_prefix):
    """Tests if _id is converted to id and _id is no longer in the model.
    If id is already provided, nothing should occur.
    """
    data = {"_id": "magicians", "name": "Magicians"}

    if not has_underscore_prefix:
        data["id"] = data.pop("_id")

    model = DummyModel(**data)

    assert model.id == "magicians"

    with pytest.raises(AttributeError):
        model._id
