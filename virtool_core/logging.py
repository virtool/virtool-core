from logging import INFO, DEBUG, captureWarnings

import coloredlogs


def configure_logs(debug: bool):
    """
    Configure logging for Virtool.

    * Use colored logging.
    * Set short or long line formatting based on configuration options.
    * Set logging level based on ``dev`` configuration option.
    :param debug: log debug messages

    """

    log_format = "{asctime:<20} {module:<11} {levelname:<8} {message}"

    if debug:
        log_format += " ({name}:{funcName}:{lineno})"

    captureWarnings(True)

    coloredlogs.install(level=DEBUG if debug else INFO, fmt=log_format, style="{")
