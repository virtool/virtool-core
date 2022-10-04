from datetime import datetime

from pydantic import ValidationError

from virtool_core.models.history import HistoryMinimal, HistoryIndex, HistoryOTU
from virtool_core.models.reference import ReferenceMinimal, ReferenceBuild
from virtool_core.models.user import UserMinimal
from virtool_core.models.task import Task
import pytest


def test_history_model():
    """
    Tests the 'method_name' field for the 'HistoryMinimal' model

    """

    HistoryMinimal(
        created_at=datetime.now(),
        description="test_model",
        id="goat",
        index=HistoryIndex(id="foo", version=87),
        method_name="remove",
        otu=HistoryOTU(id="foo", name="hello", version="removed"),
        reference=ReferenceMinimal(
            created_at=datetime.now(),
            data_type="genome",
            groups=[],
            id="bar",
            internal_control="in",
            latest_build=ReferenceBuild(
                created_at=datetime.now(),
                id="zoo",
                version=90,
                user=UserMinimal(administrator=True, active=True, id="ian", handle="ian"),
                has_json=True
            ),
            name="virus",
            organism="covid",
            otu_count=89,
            task=Task(
                complete=True,
                context={"hello": 2022},
                count=26,
                created_at=datetime.now(),
                id=6,
                progress=45,
                step="saihsiah",
                type="any"
            ),
            unbuilt_change_count=34,
            user=UserMinimal(administrator=True, active=True, id="ian", handle="ian"),
            users=[]
        ),
        user=UserMinimal(administrator=True, active=True, id="ian", handle="ian")
    )

    with pytest.raises(ValidationError) as err:
        HistoryMinimal(
            created_at=datetime.now(),
            description="test_model",
            id="goat",
            index=HistoryIndex(id="foo", version=87),
            method_name="invalid",
            otu=HistoryOTU(id="foo", name="hello", version="removed"),
            reference=ReferenceMinimal(
                created_at=datetime.now(),
                data_type="genome",
                groups=[],
                id="bar",
                internal_control="in",
                latest_build=ReferenceBuild(
                    created_at=datetime.now(),
                    id="zoo",
                    version=90,
                    user=UserMinimal(administrator=True, active=True, id="ian", handle="ian"),
                    has_json=True
                ),
                name="virus",
                organism="covid",
                otu_count=89,
                task=Task(
                    complete=True,
                    context={"hello": 2022},
                    count=26,
                    created_at=datetime.now(),
                    id=6,
                    progress=45,
                    step="messiahs",
                    type="any"
                ),
                unbuilt_change_count=34,
                user=UserMinimal(administrator=True, active=True, id="ian", handle="ian"),
                users=[]
            ),
            user=UserMinimal(administrator=True, active=True, id="ian", handle="ian")
        )

        assert "method_name value is not a valid enumeration member" in err
