import pytest
from structlog import get_logger
from structlog.testing import capture_logs

from virtool_core.logging import configure_logs


@pytest.mark.parametrize("debug,expected", [(False, 4), (True, 5)])
def test_configure_logs(debug, expected):
    configure_logs(debug)
    with capture_logs() as cap:
        logger = get_logger("ryanf")

        logger.error("print error")
        logger.warning("print warning")
        logger.critical("print critical")
        logger.info("print info")
        logger.debug("print debug")

        assert len(cap) == expected
