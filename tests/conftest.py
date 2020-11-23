pytest_plugins = [
    "tests.fixtures.db",
    "tests.fixtures.core",
    "tests.fixtures.history",
    "tests.fixtures.otus",
]


def pytest_addoption(parser):
    parser.addoption(
        "--db-connection-string",
        action="store",
        default="mongodb://localhost:27017"
    )

    parser.addoption(
        "--redis-connection-string",
        action="store",
        default="redis://localhost:6379"
    )
