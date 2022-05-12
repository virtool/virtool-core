from virtool_core.logging import configure_logs
from logging import getLogger

logger = getLogger("testrf")


def test_configure_logs(caplog):
    configure_logs(False)
    print_logs()

    for record in caplog.records:
        assert record.levelname != "DEBUG"

    assert len(caplog.records) == 4

    caplog.clear()

    configure_logs(True)
    print_logs()

    assert "DEBUG" in caplog.text
    assert len(caplog.records) == 5
    caplog.clear()


def print_logs():
    logger.error("print error")
    logger.warning("print warning")
    logger.critical("print critical")
    logger.info("print info")
    logger.debug("print debug")
