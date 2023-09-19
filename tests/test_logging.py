import pytest

from virtool_core.logging import configure_logs
from structlog import get_logger


@pytest.mark.parametrize("debug,expected", [(False, 4), (True, 5)])
def test_configure_logs(debug, expected, caplog):
    logger = get_logger("ryanf")

    configure_logs(debug)

    logger.error("print error")
    logger.warning("print warning")
    logger.critical("print critical")
    logger.info("print info")
    logger.debug("print debug")

    assert len(caplog.records) == expected
