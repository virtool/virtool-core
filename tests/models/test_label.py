from virtool_core.models.label import Label
import pytest


def test_label_model():
    """
    Tests the 'color' field validator for the
    'Label' model

    """

    Label(
        color="#FFFFFF",
        count=0,
        description="dsRNA/Ab",
        id=22,
        name="foo"
    )

    with pytest.raises(ValueError) as err:
        Label(
            color="#12345aa",
            count=0,
            description="dsRNA/Ab",
            id=22,
            name="foo"
        )
        assert "The format of the color code is invalid" in err
