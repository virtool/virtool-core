from pydantic import BaseModel as PydanticBaseModel
from pydantic import model_validator


class BaseModel(PydanticBaseModel):
    @model_validator(mode="before")
    def convert_id(cls, values):
        """Converts the "_id" field to "id"."""
        if "_id" in values:
            values["id"] = values.pop("_id")

        return values
